# Okretaji – postavljanje i automatizacija

## Što je u paketu
- `index.html` – responzivna naslovnica i prikaz vijesti.
- `news.json` – vijesti i raspored događaja; bot ga osvježava.
- `feeds.json` – RSS izvori i ručno održavani događaji.
- `scripts/update_news.py` – dohvat, deduplikacija, izdvajanje teksta izvora i AI urednička obrada.
- `.github/workflows/osvjezi-vijesti.yml` – automatizacija svaka tri sata.
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
