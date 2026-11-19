# Okretaji — sedmodnevni pokus privlacenja hrvatske publike
**Pripremljeno:** 19.11.2026. **Status:** interni urednicki plan; nista nije javno objavljeno.

## Polazno stanje (izvor: Windsor.ai, povezani Meta i GA4)
- Facebook: 11 Reelsa, prosjecno 263 prikazivanja; 32 ostale objave, prosjecno 30 prikazivanja. To nisu jedinstveni gledatelji.
- Instagram: 14 Reelsa prosjecno 151 pregled i 121 jedinstveni doseg; 20 drugih medija prosjecno 53 pregleda i 32 jedinstveni doseg. Medijan preskakanja u prve 3 sekunde 64,5 %.
- Instagram 331 pratitelj, samo 43 iz Hrvatske (13 %). **Cilj:** relevantni citatelji iz Hrvatske i regije, ne lazno veliki globalni broj.
- GA4 je prije migracije 19.11. nedovoljno pokrivao clanke (dio stranica bez GA koda), stoga povijesna citanost clanaka nije usporediva. Potrebna je zasebna provjera GA4 page_view nakon consent klika.

## Tri urednicke teme za tjedan
To su **koncepti i produkcijski nalozi, a ne gotovi videi**. Sljedece korake provesti tek uz kvalitetan dovrseni materijal i urednikovo izricito odobrenje za objavu.

### A — Tehnika / 1,0 turbo naspram 1,6 atmosferca
- Cilj: hrvatski vlasnici automobila, prakticna tehnicka publika.
- Prva sekunda: **'115 KS. Nekad 1,6 litara, danas 999 kubika.'**
- Vizual: stvarne fotografije pogonskih jedinica ili autorizirane originalne ilustracije, bez laznih usporedbi prikazanih konkretnih automobila.
- 15–25 s: (1) usporedi obujam i jednaku deklariranu snagu, (2) objasni sto turbopunjac mijenja, (3) razlikuj trajnost od same zapremnine.
- Zavrsni kadar: 'Kako radi i sto se troši? Analiza: Okretaji.com'.
- Postojeci članak: `/kako-smo-dosli-do-1-0-turba.html`.
- Testni klikabilni URL za FB: `python3 scripts/utm_links.py --path /kako-smo-dosli-do-1-0-turba.html --source facebook --campaign hr_tehnika_202611 --content reel_turbo_01`.
- Testni IG URL (za profilni link / Story link sticker, ne za neklikabilan caption): isto s `--source instagram`.

### B — MotoGP / Michelin i Pirelli 2027.
- Cilj: tehnicke zanimljivosti o MotoGP-u. Cinjenice prije snimanja ponovno potvrditi iz sluzbenog izvora.
- Prva sekunda: **'Promijene se gume. Promijeni se i MotoGP?'**
- Vizual: shematska, originalno nacrtana povrsina kontakta gume i staze; ako se koristi stvarna fotografija, provjeriti licenciju i kredit.
- 15–25 s: sto se mijenja u ponasanju motocikla, sto vozaci moraju iznova uciti i zasto rezultati proslih sezona nisu garancija.
- Pozadina: `/motogp-gume-2027-pirelli-umjesto-michelina.html`.
- Kampanja: `hr_motogp_202611`, kreativni ID `reel_gume_01`.

### C — F1 / sto se mijenja zvukom i energijom 2026.
- Cilj: hrvatski F1 fanovi uz jednostavno tehnicko objasnjenje.
- Prva sekunda: **'F1 je brza. Ali zasto vise ne vristi kao V10?'**
- Vizual: vlastita animirana shema V6 turbo i hibridnog sustava s oznakom ilustracija, bez oponasanja zasticenih zvukova i koristenja tudih snimki bez prava.
- 15–25 s: V6 turbo naspram starog atmosferskog V10, ulozi hibridne energije i suptilna poanta o performansama i dozivljaju.
- Provjeriti aktualni tehnicki pravilnik i brojke prije javne objave. Treba pripremiti vlastiti originalni istrazivacki clanak ili povezati postojeci provjereni tehnicki materijal; ne izmisliti izvor.
- Kampanja: `hr_f1_202611`, kreativni ID `reel_f1_v6_01`.

## Operativna pravila
1. Bez generickih AI fraza, emotikona ili nametljivih pitanja na kraju. Tekst hrvatski, prirodan i izravan.
2. Sva tri Reela moraju biti potpuna 1080x1920 (9:16) videa, s provjerenim kadrovima, citljivim titlovima, bez glazbe bez prava, te vizualnom provjerom prvog i zadnjeg kadra. **Ne oznacavati kao FINAL prije pregleda.**
3. **Nijedan javni clanak, video, Story ni FB/IG tekst ne smije se objaviti bez urednikova odobrenja.** 0 € placenih oglasa.
4. Pri svakoj odobrenoj objavi zabiljeziti datum, kanal, URL objave, UTM oznaku, broj pregleda/doseg/interakcije, skip rate gdje postoji, te GA4 landing pages / organic search / hr promet, s izvorom i datumom ocitanja.
5. Cilj mjerenja: stvarni klikovi i aktivno citanje clanaka, ne samo pregledi ili broj pratitelja.
6. Usporediti rezultate na 7. dan. Ako GA4 `page_view` i dalje nije provjeren, ne donositi tvrdnje da Reelsi generiraju nula citatelja.

## Neposredni tehnicki rad
- U repo je dodan `scripts/utm_links.py` koji proizvodi HTTPS oznacene poveznice samo za okretaji.com i provjerava se u GitHub Actions workflowu `.github/workflows/utm-link-check.yml`.
- Dnevni analiticki pregled postavljen je na sedam izvodenja, od 20.11.2026. oko 08:00 po Zagrebu. Odluke zapisivati u README.
- Ne mijenjati IG bio bez odobrenja urednika, posebno ako se stavlja UTM link koji je javno vidljiv.
