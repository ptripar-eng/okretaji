# Okretaji Reels – produkcijski sustav bez API ključa

Ovaj postupak koristi lokalno pripremljene/licencirane videoisječke. Ne preuzima automatski tuđe snimke s društvenih mreža niti zaobilazi ograničenja stock servisa.

## Izvori kadrova
- Mixkit: https://mixkit.co/free-stock-video/
- Pixabay: https://pixabay.com/videos/
- Wikimedia Commons: https://commons.wikimedia.org/

Za svaki preuzeti kadar prije uporabe:
1. Otvoriti stranicu konkretnog zapisa i pročitati licencu koja vrijedi za taj zapis.
2. Spremiti originalni URL, autora, naziv, licencu i datum preuzimanja u `assets/reels/credits.json`.
3. Provjeriti dopušta li licenca komercijalnu uporabu i izmjene te zahtijeva li atribuciju.
4. Ne koristiti snimke TV prijenosa, tuđe YouTube/Instagram objave ili kadar koji samo izgleda kao stvarna utrka, a nije.
5. Za stvarne natjecateljske kadrove koristiti samo materijal s izričitim dopuštenjem nositelja prava ili jasno licenciran arhivski materijal.

## Predložena struktura
```
assets/reels/
  clips/                 # licencirani MP4 kadrovi
  credits.json           # obvezna evidencija prava
  projects/
    primjer.json         # plan montaže i tekstovi
reels/                   # gotovi MP4-ovi za pregled
```

## Standard Okretaji
- 1080 × 1920, 9:16, H.264 MP4
- 25 ili 30 fps
- Hrvatska naracija i titlovi (SRT/ASS)
- Rezovi svakih 1–3 sekunde; bez lažnog predstavljanja stock kadrova kao određene utrke/vozača
- Glazba samo iz Meta Sound Collection ili drugog izvora s dokumentiranom licencom
- Svaki Reel završava kratkim Okretaji potpisom i pozivom na praćenje
- Prvo se sprema kao nacrt za ljudski pregled; automatska objava nije uključena

## Evidencija licence
Primjer zapisa u `credits.json`:
```json
{
  "clip-001.mp4": {
    "source_url": "URL konkretne stranice videa",
    "creator": "Ime autora ako je navedeno",
    "license": "Točan naziv licence",
    "commercial_use": true,
    "attribution_required": false,
    "downloaded_at": "YYYY-MM-DD",
    "notes": "Opis kadra i ograničenja"
  }
}
```

## Važno
Stock snimka motocikla nije dokaz da je prikazani vozač ili model sudjelovao u događaju iz teksta. Za vijesti koje ovise o konkretnom događaju koristimo vlastite infografike, službene materijale s dopuštenjem ili izričito licencirane snimke.
