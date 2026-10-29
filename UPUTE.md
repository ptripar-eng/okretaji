# Okretaji – postavljanje i automatizacija

## Što je u paketu
- `index.html` – responzivna naslovnica i prikaz vijesti.
- `news.json` – vijesti i raspored događaja; bot ga osvježava.
- `feeds.json` – RSS izvori i ručno održavani događaji.
- `scripts/update_news.py` – dohvat, deduplikacija, izdvajanje teksta izvora i AI urednička obrada.\n- `scripts/add_images.py` i `scripts/check_news.py` – relevantne fotografije s atribucijom, uklanjanje duplikata i kontrola podataka.\n- `scripts/post_facebook.py` i `scripts/post_instagram.py` – odabir i objava sadržaja na društvenim mrežama.
- `.github/workflows/osvjezi-vijesti.yml` – automatizacija svaka šest sati.
- `o-nama.html`, `kontakt.html`, `privatnost.html` – početni predlošci stranica.
- `robots.txt`, `sitemap.xml` – osnovne SEO datoteke.

## 1. Objavi besplatno na GitHub Pages
1. Na GitHubu napravi javni repozitorij `okretaji`.
2. Učitaj sadržaj ove mape, uključujući skrivenu mapu `.github`.
3. Otvori **Settings → Pages**; odaberi **Deploy from a branch**, branch `main`, folder `/(root)` i spremi.
4. U **Settings → Actions → General → Workflow permissions** uključi **Read and write permissions**.
5. U kartici **Actions** pokreni workflow **Osvježi vijesti** ručno i provjeri zapisnik.
6. Besplatna adresa prvo će biti `https://TVOJE-IME.github.io/okretaji/`.

## 2. Poveži domenu okretaji.com
U repozitoriju otvori **Settings → Pages → Custom domain** i upiši `okretaji.com`. Kod registrara postavi DNS zapise koje GitHub Pages prikaže. Za apex domenu obično se koriste A zapisi koje navodi GitHub, a za `www` CNAME prema `TVOJE-IME.github.io`; obavezno prati aktualne upute u GitHubu. Nakon DNS provjere uključi HTTPS. Dok domena nije povezana, `canonical` i sitemap adrese u HTML-u treba prilagoditi privremenoj GitHub Pages adresi ili pričekati DNS.

## 3. Besplatni AI prijevod i novinarska obrada
1. Otvori [Google AI Studio](https://aistudio.google.com/apikey), izradi API ključ i dodaj ga u repozitorij kao **Settings → Secrets and variables → Actions → New repository secret**, naziv `GEMINI_API_KEY`.
2. Workflow koristi `gemini-2.5-flash-lite` kao primarni model. Google nudi besplatnu kvotu za odabrane modele, ali kvote, dostupnost i ograničenja mogu se promijeniti; provjeri svoj projekt u AI Studio.
3. AI izrađuje prirodan hrvatski naslov, sažetak i parafraziranu vijest od 150–300 riječi. Ako izvor nema dovoljno činjenica ili model vrati tekst izvan raspona, portal zadržava sažetak i ne prikazuje dugi tekst.
4. U svakoj vijesti ostaje poveznica na izvor. AI obrada nije neovisna provjera činjenica; redovito pregledavaj logove i objavljeni sadržaj.
5. Skripta obrađuje najviše 12 novih članaka po pokretanju. Ako besplatna kvota bude iscrpljena ili API poziv ne uspije, taj članak neće dobiti novu AI obradu u tom pokretanju.

**Troškovi i privatnost:** GitHub Actions/GitHub Pages i Gemini API mogu biti besplatni unutar važećih uvjeta i kvota, ali besplatna kvota nije zajamčena bez ograničenja. U Gemini API besplatnoj razini poslani sadržaj može se koristiti za poboljšavanje Googleovih proizvoda; nemoj slati povjerljive podatke. Plaćeni Claude fallback je isključen po zadanim postavkama i neće se koristiti osim ako namjerno postaviš `ENABLE_CLAUDE_FALLBACK=true` i dodaš `ANTHROPIC_API_KEY`. Nikad ne stavljaj API ključ u HTML, `news.json` ili javni repozitorij.

## 4. RSS izvori i kategorije
U `feeds.json` `cat` mora biti jedan od: `f1`, `motogp`, `auto`, `moto`, `reli`, `tech`, `energy`. Feed koji ne radi bot će preskočiti; provjeri **Actions → Osvježi vijesti → log**. Prije javnog pokretanja provjeri da pojedini RSS feed dopušta pristup i da poveznice vode na konkretne izvorne članke.

## 5. Važne napomene
- Automatizirani članci mogu pogriješiti. Povremeno provjeravaj zapisnike i objavljene vijesti; nemoj tretirati AI obradu kao neovisnu provjeru činjenica.
- Puni tekst članka prikazuje se samo kad AI vrati 150–300 riječi. Ako nema dovoljno izvornog materijala, prikazuje se samo kratki sažetak.
- Poštuj pravila RSS izvora i njihove uvjete korištenja. Na portal spremamo vlastitim riječima formuliran sažetak, ne kopiju cijelog izvornog članka.
- Poštuj autorska prava: kratki sažetak vlastitim riječima i poveznica na izvor, ne kopiranje cijelog teksta ili fotografija.
- Stranice O nama, Kontakt i Privatnost su početni predlošci. Prije oglašavanja ili analitike popuni stvarne podatke i provjeri obveze koje se primjenjuju na tvoju situaciju.
- GitHub Pages je statični hosting. Nema ugrađenog CMS-a ni korisničkog računa; promjene se rade kroz GitHub.
- Nema jamstva prihoda. Za oglašavanje i affiliate suradnje treba prvo izgraditi publiku i provjeriti uvjete programa.

## 6. Automatizacija Facebooka i Instagrama

Workflow se pokreće automatski svakih šest sati. Facebook i Instagram objave ostaju u sigurnom probnom načinu dok nisu postavljeni potrebni GitHub Secrets. U repozitoriju otvori **Settings → Secrets and variables → Actions**.

### Facebook
Postavi:
- `FB_PAGE_ID` – ID Facebook stranice Okretaji.
- `FB_PAGE_TOKEN` – važeći pristupni token koji smije objavljivati na stranici.

Skripta objavljuje najviše dvije objave dnevno, vodi evidenciju i ne ponavlja isti izvorni članak. Bez oba secreta workflow samo ispiše plan i ne objavljuje.

### Instagram
Postavi:
- `IG_USER_ID` – Instagram Professional Account ID, ne korisničko ime.
- `IG_ACCESS_TOKEN` – Meta token s dozvolom za objavljivanje sadržaja na Instagramu.

Instagram račun mora biti **Professional (Business ili Creator)** i povezan s Facebook stranicom. U Meta for Developers aplikaciji konfiguriraj Instagram Graph API i potrebne dozvole, uključujući `instagram_content_publish` te pristup povezanoj stranici prema aktualnim Meta zahtjevima. Token mora biti valjan i imati odgovarajuće dozvole. Ne šalji tokene u chat, kod ili javne datoteke.

Instagram skripta objavljuje najviše jednu fotografsku objavu dnevno. Objavljuje samo članak s hrvatskim sažetkom, javno dostupnom fotografijom i potpunom atribucijom te sprema ID objave kako bi spriječila duplikate. Ako nema odgovarajuće fotografije ili Meta odbije objavu, workflow bilježi grešku i nastavlja dalje. Objave na Instagramu sadrže poveznicu na izvor i kredit fotografije; poveznice u opisu nisu klikabilne, zato profil treba imati poveznicu na portal.

**Važno:** dodavanje skripte samo po sebi ne daje pristup tvom Instagram računu. Dok ne postaviš `IG_USER_ID` i `IG_ACCESS_TOKEN`, Instagram će ostati u probnom načinu. Automatizacija ne može sigurno izraditi te tajne umjesto tebe.

### Kontrola fotografija i sadržaja
Prije spremanja vijesti workflow provjerava strukturu podataka, uklanja ponovljene fotografije iz pojedinih članaka i provjerava sintaksu Python skripti. Ako nema odgovarajuće fotografije, stranica prikazuje svoju brendiranu ilustraciju umjesto ponavljanja iste slike. Fotografije iz Openversea moraju imati podatke o autoru, licenci i izvornoj stranici.
