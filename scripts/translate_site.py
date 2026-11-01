#!/usr/bin/env python3
"""Izradi engleske (/en/) i njemačke (/de/) inačice svih hrvatskih stranica.

Hrvatske stranice u korijenu repozitorija ostaju jedini izvornik. Skripta iz njih
izdvaja tekst (HTML, atribute i tekstualne nizove u JavaScriptu), prevodi ga preko
prevodilačke memorije i18n/<jezik>.json, a nedostajuće nizove šalje Geminiju.
Ako prijevod nije dostupan, ostavlja se hrvatski izvornik i pokušava ponovno u
sljedećem pokretanju. U sve inačice dodaje prekidač jezika i hreflang poveznice.

Pokretanje:  python scripts/translate_site.py            (gradi sve)
             python scripts/translate_site.py --extract  (ispiše nizove bez prijevoda)
"""
import glob, json, os, re, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
I18N = os.path.join(ROOT, "i18n")
SITE = "https://okretaji.com"
LANGS = {"en": {"name": "English", "locale": "en-GB", "label": "EN"},
         "de": {"name": "Deutsch", "locale": "de-DE", "label": "DE"}}
API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL = os.getenv("GEMINI_MODEL", "gemini-flash-lite-latest")
SKIP_PAGES = set()          # stranice koje se ne prevode (prazno = sve)
TR_ATTRS = {"data-hl", "alt", "title", "aria-label", "placeholder", "data-n", "data-label", "data-title"}
META_TR = {"description", "og:title", "og:description", "twitter:title", "twitter:description",
           "og:image:alt", "twitter:image:alt"}
INLINE = {"a", "b", "strong", "em", "i", "span", "small", "abbr", "sup", "sub", "code", "br",
          "mark", "time", "u", "s", "q", "cite", "wbr"}
MARK = re.compile(r"⟦\d+⟧")

# ---------------------------------------------------------------- tokenizacija
TAG_RE = re.compile(r"<!--.*?-->|<![^>]*>|<(script|style)\b[^>]*>.*?</\1\s*>|"
                    r"</?[a-zA-Z][^<>\"']*(?:(?:\"[^\"]*\"|'[^']*')[^<>\"']*)*>", re.S | re.I)
ATTR_RE = re.compile(r"([^\s=/>]+)(\s*=\s*(\"[^\"]*\"|'[^']*'|[^\s>]+))?")


def has_letters(s):
    s = re.sub(r"<[^>]*>|<[^>]*$|^[^<]*>|&[#\w]+;", " ", s)
    s = MARK.sub(" ", s)
    return len(re.findall(r"[^\W\d_]", s)) >= 2


def js_natural(s):
    """Je li JS niz tekst za čitatelja, a ne ključ, selektor, URL ili kod."""
    if not has_letters(s):
        return False
    t = s.strip()
    if re.match(r"^[\[.#(]", t) or re.fullmatch(r"[a-z]+[A-Z][A-Za-z0-9]*", t) or "var(--" in t:
        return False
    if re.fullmatch(r"[^a-z\s]*\d[^a-z\s]*", t) or not re.sub(r"-?[\d.]+(px|%|em|rem|vh|vw|ms|s)?", "", t).strip(" -"):
        return False
    if re.fullmatch(r"[\"'\s]*([\w-]+=[\"'][^\"']*[\"']\s*)*[\w-]+=[\"']?\s*", t):
        return False
    if re.fullmatch(r"[\w+.-]+/[\w+.-]+", t) or t.startswith("&") or t in ("Escape", "Enter", "viewBox", "noopener noreferrer"):
        return False
    if "<" in t and re.search(r"</?[a-zA-Z]", t):
        return True
    if re.match(r"^(https?:|mailto:|data:|#|\.|/)", t) or re.search(r"\.(html|json|svg|png|jpe?g|webp|js|css)\b", t):
        return False
    if re.fullmatch(r"[a-z0-9_\-.:]+", t):            # ključevi, kategorije, ID-jevi
        return False
    if re.fullmatch(r"([\w-]+\s*:\s*[^;]+;?\s*)+", t) and not re.search(r"\s\w+\s\w+\s", t):
        return False
    if re.fullmatch(r"[\w\-]+(\s*[,>+~]\s*[\w\-.#:\[\]=\"]+)+", t) or re.search(r"[{}]|=>|\$\(|;\s*[\w.]+\s*[=(]", t):
        return False
    if re.fullmatch(r"[a-z]{2}-[A-Z]{2}", t):
        return False
    return True


JS_CODE_CTX = re.compile(r"(className\s*[+]?=|\.rel\s*=|classList\.\w+\(|getElementById\(|\$\(|querySelector(All)?\(|"
                         r"setAttribute\(|getAttribute\(|hasAttribute\(|removeAttribute\(|matchMedia\(|addEventListener\(|"
                         r"createElement(NS)?\(|new Error\(|Error\(|[!=]==?|case|\.key\s*[!=]==?|\.dataset\.\w+\s*=|closest\(|matches\(|\.replace(All)?\(|\.split\(|\.includes\(|\.startsWith\(|\.endsWith\(|\.indexOf\()\s*$")


def tag_name(tag):
    m = re.match(r"</?\s*([a-zA-Z0-9]+)", tag)
    return m.group(1).lower() if m else ""


class Translator:
    def __init__(self, lang, memory, collect=None):
        self.lang, self.mem, self.collect = lang, memory, collect

    def t(self, s):
        """Prevedi jedan niz (s očuvanim razmacima na rubovima)."""
        core = s.strip()
        if not core or not has_letters(core):
            return s
        lead, trail = s[:len(s) - len(s.lstrip())], s[len(s.rstrip()):]
        key = re.sub(r"\s+", " ", core)
        if self.collect is not None:
            self.collect.setdefault(key, None)
            return s
        out = self.mem.get(key)
        return lead + (out if out else core) + trail

    # ------------------------------------------------------------ HTML
    def html(self, src, js_ctx=False):
        if js_ctx:
            m = re.match(r"^([^<]*?>)?(.*?)(<[^>]*)?$", src, re.S)
            pre, mid, post = m.group(1) or "", m.group(2), m.group(3) or ""
            if pre or post:
                return pre + self.html(mid) + post
        toks, pos = [], 0
        for m in TAG_RE.finditer(src):
            if m.start() > pos:
                toks.append(("text", src[pos:m.start()]))
            toks.append(("tag", m.group(0)))
            pos = m.end()
        if pos < len(src):
            toks.append(("text", src[pos:]))
        out, i = [], 0
        while i < len(toks):
            kind, val = toks[i]
            if kind == "text" and has_letters(val):
                # niz teksta s ugrađenim (inline) oznakama
                j = i
                while j + 1 < len(toks) and (toks[j + 1][0] == "text" or
                                              (tag_name(toks[j + 1][1]) in INLINE and not toks[j + 1][1].startswith("<!"))):
                    j += 1
                while j > i and toks[j][0] == "tag":       # bez završnih oznaka
                    j -= 1
                run = toks[i:j + 1]
                k = len(out)                                # uključi otvarajuće inline oznake ispred
                pre = []
                while k > 0 and isinstance(out[k - 1], tuple) and out[k - 1][0] == "rawtag" and \
                        tag_name(out[k - 1][1]) in INLINE and not out[k - 1][1].startswith("</"):
                    k -= 1
                    pre.insert(0, out[k][1])
                if pre and self._balanced(pre + [v for _, v in run]):
                    del out[k:]
                    run = [("tag", p) for p in pre] + run
                if len(run) > 1 and not self._balanced([v for _, v in run]):
                    for kk, vv in run:
                        out.append(("rawtag", self.tag(vv)) if kk == "tag" else ("txt", self.t(vv)))
                    i = j + 1
                    continue
                raw = "".join(v for _, v in run)
                res = re.sub(r"<[^>]+>", lambda mm: self.attrs(mm.group(0)), self.t_run(raw))
                out.append(("txt", res))
                i = j + 1
                continue
            if kind == "tag":
                out.append(("rawtag", self.tag(val)))
            else:
                out.append(("txt", val))
            i += 1
        return "".join(v for _, v in out)

    def t_run(self, raw):
        res = self.t(raw)
        if res is raw or res == raw:
            return raw
        if sorted(re.findall(r"<[^>]+>", res)) != sorted(re.findall(r"<[^>]+>", raw)) or \
                sorted(MARK.findall(res)) != sorted(MARK.findall(raw)):
            return raw
        return res

    @staticmethod
    def _balanced(parts):
        st = []
        for p in parts:
            if not p.startswith("<"):
                continue
            n = tag_name(p)
            if n in ("br", "wbr") or p.endswith("/>"):
                continue
            if p.startswith("</"):
                if not st or st[-1] != n:
                    return False
                st.pop()
            else:
                st.append(n)
        return not st

    def tag(self, tag):
        low = tag[:8].lower()
        if tag.startswith("<!--") or tag.startswith("<!"):
            return tag
        if low.startswith("<script"):
            m = re.match(r"(<script\b[^>]*>)(.*?)(</script\s*>)$", tag, re.S | re.I)
            if not m:
                return tag
            open_t = self.attrs(m.group(1))
            ty = re.search(r"type\s*=\s*[\"']?([^\"'\s>]+)", m.group(1), re.I)
            if ty and ty.group(1).lower() not in ("text/javascript", "module", "application/ld+json", "application/json"):
                return open_t + m.group(2) + m.group(3)
            return open_t + self.js(m.group(2)) + m.group(3)
        if low.startswith("<style"):
            return tag
        return self.attrs(tag)

    def attrs(self, tag):
        name = tag_name(tag)
        is_meta = name == "meta" and re.search(r"(name|property)\s*=\s*[\"']([^\"']+)[\"']", tag) and \
            re.search(r"(name|property)\s*=\s*[\"']([^\"']+)[\"']", tag).group(2).lower() in META_TR

        def rep(m):
            an, rest, v = m.group(1), m.group(2), m.group(3)
            if not rest or not v:
                return m.group(0)
            q = v[0] if v[0] in "\"'" else ""
            val = v[1:-1] if q else v
            if an.lower().startswith("data-") and val.lstrip()[:1] in ("[", "{"):
                nv = self.js(val.replace("&quot;", '"').replace("&#39;", "'"))
                nv = nv.replace('"', "&quot;") if q == '"' else nv.replace("'", "&#39;") if q == "'" else nv
                return m.group(0).replace(v, q + nv + q, 1)
            if an.lower() in TR_ATTRS or (is_meta and an.lower() == "content"):
                nv = self.t(val.replace("&quot;", '"'))
                if q == '"':
                    nv = nv.replace('"', "&quot;")
                elif q == "'":
                    nv = nv.replace("'", "&#39;")
                return m.group(0).replace(v, q + nv + q, 1)
            return m.group(0)
        head = re.match(r"<\s*/?\s*[a-zA-Z0-9]+", tag)
        if not head:
            return tag
        return head.group(0) + ATTR_RE.sub(rep, tag[head.end():])

    # ------------------------------------------------------------ JavaScript
    def js(self, code):
        out, i, n = [], 0, len(code)
        last = ""                     # zadnji značajni znak (za prepoznavanje regexa)
        while i < n:
            c = code[i]
            if code.startswith("//", i) and not self._regex_ctx(last):
                j = code.find("\n", i)
                j = n if j < 0 else j
                out.append(code[i:j]); i = j; continue
            if code.startswith("/*", i):
                j = code.find("*/", i + 2)
                j = n if j < 0 else j + 2
                out.append(code[i:j]); i = j; continue
            if c in "\"'":
                j = i + 1
                while j < n and code[j] != c:
                    j += 2 if code[j] == "\\" else 1
                body = code[i + 1:j]
                ctx = code[max(0, i - 40):i]
                if JS_CODE_CTX.search(ctx):
                    out.append(code[i:j + 1])
                else:
                    out.append(c + self.js_str(body, c) + c)
                i = j + 1; last = "s"; continue
            if c == "`":
                j, parts, exprs, buf = i + 1, [], [], ""
                while j < n and code[j] != "`":
                    if code[j] == "\\":
                        buf += code[j:j + 2]; j += 2; continue
                    if code.startswith("${", j):
                        depth, k = 1, j + 2
                        while k < n and depth:
                            ch = code[k]
                            if ch in "\"'`":
                                k = self._skip_str(code, k); continue
                            depth += ch == "{"
                            depth -= ch == "}"
                            k += 1
                        exprs.append(code[j + 2:k - 1])
                        buf += "⟦%d⟧" % (len(exprs) - 1)
                        j = k; continue
                    buf += code[j]; j += 1
                exprs = [self.js(e) for e in exprs]
                tr = self.js_str(buf, "`") if js_natural(MARK.sub(" ", buf)) else buf
                if sorted(MARK.findall(tr)) != sorted(MARK.findall(buf)):
                    tr = buf
                tr = MARK.sub(lambda m: "${" + exprs[int(m.group(0)[1:-1])] + "}", tr)
                out.append("`" + tr + "`")
                i = j + 1; last = "s"; continue
            if c == "/" and self._regex_ctx(last):
                j, cls = i + 1, False
                while j < n and (code[j] != "/" or cls):
                    if code[j] == "\\":
                        j += 2; continue
                    cls = (cls or code[j] == "[") and code[j] != "]"
                    j += 1
                j += 1
                while j < n and code[j].isalpha():
                    j += 1
                out.append(code[i:j]); i = j; last = "r"; continue
            out.append(c)
            if not c.isspace():
                last = c if not (c.isalnum() or c in "_$") else "w"
                if last == "w":
                    m = re.match(r"[\w$]+", code[i:])
                    word = m.group(0)
                    out.append(word[1:]); i += len(word)
                    last = "kw" if word in ("return", "typeof", "case", "in", "of", "else", "do", "void") else "w"
                    continue
            i += 1
        return "".join(out)

    @staticmethod
    def _regex_ctx(last):
        return last in ("", "kw") or last in "(,=:[!&|?{};+-*%<>~^"

    @staticmethod
    def _skip_str(code, k):
        q, k = code[k], k + 1
        while k < len(code) and code[k] != q:
            k += 2 if code[k] == "\\" else 1
        return k + 1

    def js_str(self, body, q):
        plain = MARK.sub(" ", body)
        res = self.path(body)
        if res != body:
            return res
        if self.locale(body) != body:
            return self.locale(body)
        if not js_natural(plain):
            return body
        text = body.replace("\\" + q, q) if q != "`" else body
        if "<" in text and re.search(r"</?[a-zA-Z]", text):
            tr = self.html(text, js_ctx=True)
        else:
            tr = self.t(text)
        if q != "`":
            tr = re.sub(r"(?<!\\)" + re.escape(q), "\\" + q, tr)
        return tr

    # hooks (prepisuju se u Builderu)
    def path(self, v):
        return v

    def locale(self, v):
        return v


# ---------------------------------------------------------------- izgradnja
ROOT_FILES = None


def root_files():
    global ROOT_FILES
    if ROOT_FILES is None:
        ROOT_FILES = {os.path.basename(p) for p in glob.glob(os.path.join(ROOT, "*")) if os.path.isfile(p)}
    return ROOT_FILES


class Builder(Translator):
    def path(self, v):
        if self.collect is not None or not self.lang:
            return v
        base = re.split(r"[?#]", v, maxsplit=1)[0]
        if not base or base.endswith(".html") or "/" in base and not re.match(r"(assets|social|scripts)/", base):
            return v
        if re.match(r"(assets|social)/", base) or (base in root_files() and not base.endswith(".html")):
            if base == "news.json":
                return "../news_%s.json" % self.lang + v[len(base):]
            return "../" + v
        return v

    def locale(self, v):
        if self.collect is not None or not self.lang:
            return v
        if v in ("hr-HR", "hr"):
            return LANGS[self.lang]["locale"] if v == "hr-HR" else self.lang
        return v

    def attrs(self, tag):
        tag = Translator.attrs(self, tag)
        if self.collect is not None or not self.lang:
            return tag

        def rep(m):
            an, q, val = m.group(1), m.group(2), m.group(3)
            low = an.lower()
            if low in ("src", "href", "poster", "data-src", "content"):
                if val.startswith(SITE + "/"):
                    rest = val[len(SITE) + 1:]
                    if rest == "" or rest.split("?")[0].split("#")[0].endswith(".html"):
                        val = "%s/%s/%s" % (SITE, self.lang, rest)
                elif low == "href" and val.startswith("/") and not val.startswith("//"):
                    pth = re.split(r"[?#]", val, maxsplit=1)[0]
                    if pth == "/" or pth.endswith(".html"):
                        val = "/%s%s" % (self.lang, val)
                elif low != "content":
                    val = self.path(val)
            return "%s=%s%s%s" % (an, q, val, q)
        return re.sub(r"([\w:-]+)=([\"'])(.*?)\2", rep, tag)


SW_CSS = ("<style id=\"lang-sw-css\">.lang-sw{display:flex;justify-content:flex-end;gap:4px;padding:5px 16px;"
          "background:#0D2B3E;border-bottom:1px solid #ffffff14;font:700 .74rem/1.4 Barlow,system-ui,sans-serif;letter-spacing:.08em}"
          ".lang-sw a{color:#cfe3ef;text-decoration:none;padding:2px 8px;border-radius:999px}"
          ".lang-sw a:hover,.lang-sw a:focus-visible{color:#fff;background:#ffffff1f}"
          ".lang-sw a[aria-current=true]{background:var(--orange,#F05A1A);color:#fff}</style>")


def switcher(page, cur):
    links = []
    for code, label, href in (("hr", "HR", "/" + page), ("en", "EN", "/en/" + page), ("de", "DE", "/de/" + page)):
        href = href.replace("index.html", "")
        cur_attr = ' aria-current="true"' if code == cur else ""
        links.append('<a href="%s" hreflang="%s" lang="%s"%s>%s</a>' % (href, code, code, cur_attr, label))
    aria = {"hr": "Jezik", "en": "Language", "de": "Sprache"}[cur]
    keep = ("<script>document.querySelectorAll('.lang-sw a').forEach(function(a){"
            "a.href=a.getAttribute('href')+location.search+location.hash})</script>")
    return '<!--lang-sw--><nav class="lang-sw" aria-label="%s">%s</nav>%s<!--/lang-sw-->' % (aria, "".join(links), keep)


def hreflang(page):
    p = "" if page == "index.html" else page
    rows = ['<link rel="alternate" hreflang="hr" href="%s/%s">' % (SITE, p),
            '<link rel="alternate" hreflang="en" href="%s/en/%s">' % (SITE, p),
            '<link rel="alternate" hreflang="de" href="%s/de/%s">' % (SITE, p),
            '<link rel="alternate" hreflang="x-default" href="%s/%s">' % (SITE, p)]
    return "<!--hreflang-->" + "".join(rows) + SW_CSS + "<!--/hreflang-->"


def strip_injected(html):
    html = re.sub(r"<!--lang-sw-->.*?<!--/lang-sw-->", "", html, flags=re.S)
    return re.sub(r"<!--hreflang-->.*?<!--/hreflang-->", "", html, flags=re.S)


def inject(html, page, lang):
    html = strip_injected(html)
    html = re.sub(r"</head>", hreflang(page) + "</head>", html, count=1, flags=re.I)
    html = re.sub(r"(<body\b[^>]*>)", lambda m: m.group(1) + switcher(page, lang), html, count=1, flags=re.I)
    return html


def pages():
    out = []
    for p in sorted(glob.glob(os.path.join(ROOT, "*.html"))):
        name = os.path.basename(p)
        if name not in SKIP_PAGES and not re.search(r"google[\w]*\.html$", name):
            out.append(name)
    return out


def load_mem(lang):
    p = os.path.join(I18N, lang + ".json")
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}


def save_mem(lang, mem):
    os.makedirs(I18N, exist_ok=True)
    with open(os.path.join(I18N, lang + ".json"), "w", encoding="utf-8") as f:
        json.dump(dict(sorted(mem.items())), f, ensure_ascii=False, indent=0)
        f.write("\n")


def valid(src, tr):
    if not isinstance(tr, str) or not tr.strip():
        return False
    if sorted(re.findall(r"<[^>]+>", src)) != sorted(re.findall(r"<[^>]+>", tr)):
        return False
    if sorted(MARK.findall(src)) != sorted(MARK.findall(tr)):
        return False
    return True


PROMPT = """You translate the Croatian website Okretaji (cars, motorcycles, motorsport, technology, energy) into {name}.
Return ONLY a JSON array with exactly {n} strings, the translations of the input array in the same order.
Rules: natural, idiomatic {name} for readers of a motoring news site; keep the meaning exactly; do not add or omit facts or numbers.
Keep every HTML tag (e.g. <b>, <a href="...">, <br>) and every placeholder like ⟦0⟧ exactly as in the source, including attributes.
Keep HTML entities (&nbsp; &amp; …), emojis, units, numbers and arrows. Do not translate brand names, model names, people, teams, series names (MotoGP, F1), or the site name OKRETAJI/Okretaji.
Croatian place names: use the established {name} exonym only when common (e.g. Istra → Istria / Istrien), otherwise keep them.
Short UI labels stay short. {extra}
INPUT:
{data}"""


def gemini(batch, lang):
    import requests
    extra = "German: use 'Sie' only when direct address is unavoidable; otherwise neutral phrasing." if lang == "de" else \
        "English: use British spelling."
    prompt = PROMPT.format(name=LANGS[lang]["name"], n=len(batch), extra=extra,
                           data=json.dumps(batch, ensure_ascii=False))
    url = "https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent" % MODEL
    payload = {"contents": [{"parts": [{"text": prompt}]}],
               "generationConfig": {"responseMimeType": "application/json", "temperature": 0.1}}
    for attempt in range(3):
        try:
            r = requests.post(url, headers={"x-goog-api-key": API_KEY}, json=payload, timeout=90)
            if r.status_code == 429:
                time.sleep(30); continue
            r.raise_for_status()
            txt = r.json()["candidates"][0]["content"]["parts"][0]["text"]
            arr = json.loads(txt[txt.find("["):txt.rfind("]") + 1])
            if isinstance(arr, list) and len(arr) == len(batch):
                return arr
            print("Gemini vratio pogrešan broj prijevoda (%s)." % lang)
        except Exception as e:
            print("Gemini prijevod nije uspio:", type(e).__name__)
            time.sleep(5)
    return None


def fill_missing(lang, mem, wanted):
    missing = [s for s in wanted if s not in mem]
    if not missing:
        return 0
    if not API_KEY:
        print("%s: %d nizova bez prijevoda, GEMINI_API_KEY nije postavljen." % (lang, len(missing)))
        return 0
    done = 0
    for k in range(0, len(missing), 40):
        batch = missing[k:k + 40]
        res = gemini(batch, lang)
        time.sleep(5)
        if not res:
            continue
        for s, t in zip(batch, res):
            if valid(s, t):
                mem[s] = re.sub(r"\s+", " ", t.strip()); done += 1
            else:
                print("Odbačen neispravan prijevod:", s[:60])
    return done


def main():
    names = pages()
    if "--extract" in sys.argv:
        coll = {}
        for name in names:
            src = strip_injected(open(os.path.join(ROOT, name), encoding="utf-8").read())
            Builder(None, {}, coll).html(src)
        lang = sys.argv[sys.argv.index("--extract") + 1] if len(sys.argv) > sys.argv.index("--extract") + 1 else None
        mem = load_mem(lang) if lang else {}
        json.dump([k for k in coll if k not in mem], sys.stdout, ensure_ascii=False, indent=0)
        return
    coll = {}
    sources = {}
    for name in names:
        src = strip_injected(open(os.path.join(ROOT, name), encoding="utf-8").read())
        sources[name] = src
        Builder(None, {}, coll).html(src)
    for lang in LANGS:
        mem = load_mem(lang)
        n = fill_missing(lang, mem, list(coll))
        if n:
            save_mem(lang, mem)
        os.makedirs(os.path.join(ROOT, lang), exist_ok=True)
        miss = 0
        for name, src in sources.items():
            out = Builder(lang, mem).html(src)
            out = re.sub(r"(<html\b[^>]*\blang=)([\"'])hr\2", r"\1\2%s\2" % lang, out, count=1, flags=re.I)
            out = inject(out, name, lang)
            with open(os.path.join(ROOT, lang, name), "w", encoding="utf-8") as f:
                f.write(out)
        miss = sum(1 for s in coll if s not in mem)
        print("%s: %d stranica, %d nizova, %d bez prijevoda, %d novo prevedeno." % (lang, len(sources), len(coll), miss, n))
        # obriši inačice stranica kojih više nema u izvorniku
        for p in glob.glob(os.path.join(ROOT, lang, "*.html")):
            if os.path.basename(p) not in sources:
                os.remove(p)
    for name, src in sources.items():
        path = os.path.join(ROOT, name)
        new = inject(open(path, encoding="utf-8").read(), name, "hr")
        if new != open(path, encoding="utf-8").read():
            with open(path, "w", encoding="utf-8") as f:
                f.write(new)
    update_sitemap()


def update_sitemap():
    p = os.path.join(ROOT, "sitemap.xml")
    if not os.path.exists(p):
        return
    xml = open(p, encoding="utf-8").read()
    locs = [l for l in re.findall(r"<loc>([^<]+)</loc>", xml) if not re.match(SITE + r"/(en|de)/", l)]
    rows = []
    for l in locs:
        rest = l[len(SITE) + 1:] if l.startswith(SITE + "/") else None
        rows.append("  <url><loc>%s</loc></url>" % l)
        if rest is not None:
            for lang in LANGS:
                rows.append("  <url><loc>%s/%s/%s</loc></url>" % (SITE, lang, rest))
    new = ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + "\n".join(rows) + "\n</urlset>\n")
    if new != xml:
        open(p, "w", encoding="utf-8").write(new)


if __name__ == "__main__":
    main()
