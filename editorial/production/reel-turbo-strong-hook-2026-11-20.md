# Okretaji — jači uvod za Reel o 1,0 turbomotoru

**Datum:** 20.11.2026.  
**Status:** potpuno proizvedeno i lokalno provjereno; **nije javno objavljeno**; čeka uredničku provjeru.

## Ishod

- Originalni Reel `okretaji_reel_turbo_115ks_1080x1920.mp4`, 22,00 s, zadržan kao prethodna verzija.
- Novi izlaz `okretaji_reel_turbo_115ks_novi_pocetak_1080x1920.mp4`: **1080×1920**, MP4 **H.264 + AAC**, približno **20,716 s**, **496 video kadrova**, 1.938.873 bajta.
- Nova naslovnica `okretaji_reel_turbo_novi_pocetak_naslovnica.jpg`: JPEG **1080×1920** iz početnog kadra.
- Na početku je originalna potpuno animirana **2,25-sekundna** scena s jasnim hookom već u prvom kadru: „ISTIH 115 KS”, „ALI 38 % MANJE KUBIKAŽE”, „1,6 L BEZ TURBA” naspram „1,0 L S TURBOM”. Obje pojednostavljene animirane grupe klipova i turbine kreću se u prvoj sekundi. Tekst je prirodan hrvatski.
- Izvorni edukativni dio videa od otprilike **3,55. sekunde originala do kraja** ostao je sadržajno nepromijenjen. Sastavljen je u novi cjeloviti MP4 s originalnim sintetskim nenametljivim zvukom i novim, izvorno sintetiziranim audio hookom. Nema tuđe glazbe ni tuđih videozapisa.
- 38 % je zaokruživanje razlike između **1,6 L i 1,0 L**: (1,6 − 1,0) / 1,6 = 37,5 %. Služi kao usporedba primjera dviju generacija benzinskih motora, **ne tvrdnja da je isti mehanički motor dobio turbinu**.
- Klipovi su samo **shematski prikaz**: nisu kinematički nacrt stvarnoga motora. Ne dodavati identitet proizvođača ili stvarnu fotografiju bez provjere.
- Napravljeno iz izvornog MP4-a u radnom kontejneru uz produkcijsku Python skriptu `/mnt/data/okretaji_reels/improve_turbo_hook.py`. Skripta i MP4 su razgovorni artefakti, **nisu datoteke u GitHubu**. Za ponovni render koriste se izvorni MP4 i Python3/Pillow/NumPy/OpenCV/ffmpeg; skripta je dostupna u razgovornom radnom direktoriju dok je sesija aktivna.

## QA

- `ffprobe` potvrđuje streamove H.264 1080×1920 24 fps (r_frame_rate), AAC i ukupnu trajnost 20,716 s.
- `ffmpeg -v error -i ... -f null -` završio je bez greške dekodiranja.
- `cv2.VideoCapture` može pročitati vremenske oznake 0, 1, 2, 3,1, 7, 15 i 20 s te 496 ukupnih frameova; naslovnica JPEG ima 1080×1920.
- Kontaktni list uvodnih i prvih obrazovnih kadrova vizualno je pregledan, uključujući skok iz novog hooka u postojeći segment.
- Mjerljiva učinkovitost **nije dokazana**: zbog ranijeg Pirelli Reela s 81,3 % ranog preskakanja nova verzija ciljano skraćuje uvod, ali rezultat treba usporediti tek nakon urednikove odobrene objave.

## Poveznica i objavljivanje

- Članak: https://okretaji.com/kako-smo-dosli-do-1-0-turba.html
- Objaviti **samo nakon posebnog uredničkog odobrenja**. Ne reciklirati istu objavu automatski na svim mrežama i ne pokretati plaćene oglase.
- Instagram UTM (za Story link sticker/bio): `utm_source=instagram&utm_medium=social&utm_campaign=hr_tehnika_202611&utm_content=reel_turbo_hook2`.
- Facebook UTM (poveznica u dopuštenom tekstu objave): `utm_source=facebook&utm_medium=social&utm_campaign=hr_tehnika_202611&utm_content=reel_turbo_hook2`.
