# Okretaji — produkcijska evidencija Reela: MotoGP 2027., Michelin → Pirelli

**Datum:** 19. studenoga 2026.  
**Status:** ANIMIRANI VIDEO DOVRŠEN I TEHNIČKI PROVJEREN; ČEKA IZRIČITO UREDNIČKO ODOBRENJE. NIJE JAVNO OBJAVLJEN.

## Isporuka u aktualnom ChatGPT razgovoru

- **Video:** `okretaji_reel_motogp_pirelli_2027_1080x1920.mp4`; 23,000 s, 1080 × 1920 (9:16), 24 fps, **552 frameova**, H.264/yuv420p, AAC mono 48 kHz, 13.779.123 bajta.
- **Naslovnica:** `okretaji_reel_motogp_pirelli_2027_naslovnica.jpg`; JPEG 1080 × 1920, 380.739 bajta. 
- Datoteke su dostupne putem **sandbox artefakata aktualnog razgovora**, **nisu prenesene u GitHub repozitorij**; ovdje se ne smije predstavljati da se video može preuzeti iz GitHuba.
- Lokalna reproducibilna Python skripta za animaciju i originalni zvučni efekt je u razgovornom radnom direktoriju `/mnt/data/okretaji_reels/make_motogp_2027_reel.py`. Ta lokalna putanja nije trajni repozitorijski artefakt; Claude za ponovno renderiranje treba odgovarajuću kopiju koda ili novu implementaciju prema ovom storyboardu.
- Svi kadrovi i zvuk su izvorno proceduralno animirani i sintetizirani. Nisu korištene tuđe snimke, glazba ni Pirelli/Michelin logotip. Grafike su **shematska ilustracija, ne snimka stvarnoga motocikla**, i to je označeno unutar videa.

## Provjerene činjenice i izvor

1. Michelin ostaje ekskluzivni dobavljač za kraljevsku klasu MotoGP do kraja 2026.; **Pirelli preuzima od 2027.** — službeni MotoGP: https://www.motogp.com/en/news/2025/3/6/pirelli-sera-el-proveedor-de-neumaticos-de-motogp-a-partir-de-2027/521153
2. Uz ostale promjene pravila 2027., maksimalni obujam MotoGP motora mijenja se **s 1000 na 850 cm³**, uz smanjenu aerodinamiku — FIM tehnička odluka: https://www.fim-moto.com/fileadmin/user_upload/Documents/2024/Decisions_of_the_Grand_Prix_Commission__06_May_2024.pdf?t=1714990607 ; MotoGP opis: https://www.motogp.com/en/news/2025/06/02/what-is-motogp-engine-displacementx/751342
3. Promjena konstrukcije gume, dostupnog gripa i osjećaja pri kočenju/ulasku u zavoj jest **inženjerski problem i područje testiranja**, ali **nije dokaz** da će jedan dobavljač biti bolji, lošiji ili da će pojedini vozač pobjeđivati. Primjer službenog Pirelli prvog testa na pet proizvođača: https://press.pirelli.com/pirelli-completa-a-misano-il-primo-test-sui-pneumatici-per-la-motogp/

## Storyboard — 23 sekunde

- 0:00–0:03,6 — velik animirani kotač; „2027. NOVE GUME. NOVA PRAVILA IGRE.” i „MotoGP mijenja dobavljača”.
- 0:03,6–0:07,2 — dva rotirajuća kotača, zamjena „MICHELIN → PIRELLI”; do kraja 2026. / od 2027.
- 0:07,2–0:12,0 — dinamična shema gume, kontakt s asfaltom, kočenje; „GUMA JE VIŠE OD CRNOG KRUGA.”; „PROFIL • GRIP • OSJEĆAJ”.
- 0:12,0–0:17,0 — stilizirani animirani MotoGP motocikl i linije asfalta; važnost prilagodbe šasije i postavki, testovi daju odgovor.
- 0:17,0–0:20,15 — tehnička promjena: „1000 → 850 cm³”, manji motori, manje aerodinamike.
- 0:20,15–0:23,0 — urednički zaključak: „PITANJE NIJE ČIJA JE GUMA. NEGO TKO ĆE SE PRILAGODITI.”; poziv na članak Okretaji.com.

## Tehnički QA i publikacijska ograničenja

- **PASS:** `ffprobe`: H.264 1080×1920 / 24 fps / 552 frames, AAC 48 kHz; trajanje točno 23,000 s. `ffmpeg -v error -i video.mp4 -f null -` završio bez greške dekodiranja. `cv2.VideoCapture` potvrdio otvaranje datoteke, točan broj frameova i dekodiranje uzoraka od početka do zadnjeg framea. Naslovnica JPEG otvorena i potvrđena na 1080×1920.
- Izvorni storyboard snimljen je u šest vizualno pregledanih presjeka. Ne predstavljati shematske kotače kao Pirellijevu ili Michelinovu stvarnu konstrukciju; nisu točni tehnički nacrti.
- Objave **isključivo nakon urednikova izričitog odobrenja**; bez plaćenih oglasa, bez automatiziranog postanja prije odobrenja. Samotestirani video nije dokaz da će ostvariti određeni broj pregleda.
- Predloženi tekst objave i hashtagovi nalaze se u ChatGPT razgovoru; za FB i IG odvojeno uključiti UTM poveznice `utm_source=facebook|instagram&utm_medium=social&utm_campaign=hr_motogp_202611&utm_content=reel_gume_01`. Na Instagramu poveznica ide u Story link sticker ili bio, ne u neklikabilan opis.
- U GA4 promatrati prijavljene dolaske nakon privole te IG reach/views, skip rate i FB impressions; ne zbrajati različite metrike kao jedinstvene posjetitelje.
