index.html
<!DOCTYPE html>
<html lang="hr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Okretaji – auto, moto, motosport, tehnologija i energija</title>
<meta name="description" content="Okretaji donose novosti iz auto-moto svijeta, najave utrka Formule 1 sa statistikom i obrisom staze, priče iza kacige i motorute po Hrvatskoj i regiji.">
<meta name="theme-color" content="#0D2B3E">
<link rel="canonical" href="https://okretaji.com/">
<meta property="og:type" content="website">
<meta property="og:title" content="Okretaji – pokrećemo znatiželju">
<meta property="og:description" content="Auto, moto, motosport, tehnologija i energija pod povećalom.">
<meta property="og:url" content="https://okretaji.com/">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E%F0%9F%8F%81%3C/text%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@700;800;900&family=Barlow:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#EAF3F8; --card:#FFFFFF; --ink:#0D2B3E; --muted:#4F6979; --line:#D3E2EA;
  --orange:#F05A1A; --powder:#A9D3EB; --navy:#0D2B3E; --deep:#0D2B3E;
  --red:#D7261E; --blue:#1C5A86; --yellow:#E8890C; --green:#23794A;
  --onorange:#FFFFFF; --shadow:0 1px 2px rgba(13,43,62,.06),0 8px 24px -12px rgba(13,43,62,.25);
  color-scheme:light;
  box-sizing:border-box;
  padding-top:env(safe-area-inset-top,0px);
  padding-bottom:env(safe-area-inset-bottom,0px);
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --bg:#081923; --card:#10283A; --ink:#E7F1F7; --muted:#93AEC0; --line:#1E3B4E;
    --orange:#FF7433; --powder:#6FAED3; --navy:#E7F1F7; --deep:#0B2232;
    --red:#FF5A4F; --blue:#7DBCE6; --yellow:#FFB347; --green:#5FCB8B;
    --onorange:#081923; --shadow:0 1px 2px rgba(0,0,0,.3),0 10px 30px -14px rgba(0,0,0,.7);
    color-scheme:dark;
  }
}
:root[data-theme="dark"]{
  --bg:#081923; --card:#10283A; --ink:#E7F1F7; --muted:#93AEC0; --line:#1E3B4E;
  --orange:#FF7433; --powder:#6FAED3; --navy:#E7F1F7; --deep:#0B2232;
  --red:#FF5A4F; --blue:#7DBCE6; --yellow:#FFB347; --green:#5FCB8B;
  --onorange:#081923; --shadow:0 1px 2px rgba(0,0,0,.3),0 10px 30px -14px rgba(0,0,0,.7);
  color-scheme:dark;
}
*,*::before,*::after{box-sizing:inherit}
html{scroll-padding-top:calc(env(safe-area-inset-top,0px) + 64px)}
@media (prefers-reduced-motion:no-preference){html{scroll-behavior:smooth}}
body{margin:0;background:var(--bg);color:var(--ink);font-family:"Barlow",system-ui,-apple-system,"Segoe UI",sans-serif;font-size:17px;line-height:1.5;-webkit-font-smoothing:antialiased}
a{color:inherit}
img{max-width:100%;display:block}
.D{font-family:"Big Shoulders Display","Arial Narrow",Impact,sans-serif}
.wrap{max-width:1240px;margin:0 auto;padding:0 22px}
:focus-visible{outline:3px solid var(--orange);outline-offset:3px}

/* ---------- top bar ---------- */
.bar{position:sticky;top:env(safe-area-inset-top,0px);z-index:30;background:color-mix(in srgb,var(--bg) 86%,transparent);backdrop-filter:saturate(1.4) blur(12px);-webkit-backdrop-filter:saturate(1.4) blur(12px);border-bottom:1px solid var(--line)}
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:31;background:var(--bg)}
.bar .wrap{display:flex;align-items:center;gap:22px;height:56px}
.mini{font:900 1.6rem/1 "Big Shoulders Display",Impact,sans-serif;text-decoration:none;display:flex;align-items:center;gap:6px;flex:none}
.mini svg{width:26px;height:20px}
.nav{display:flex;gap:4px;overflow-x:auto;scrollbar-width:none;flex:1}
.nav::-webkit-scrollbar{display:none}
.nav a{white-space:nowrap;text-decoration:none;font-weight:600;font-size:.95rem;padding:6px 12px;border-radius:999px;color:var(--muted)}
.nav a:hover,.nav a[aria-current="true"]{color:var(--ink);background:var(--card)}
.upd{font-size:.78rem;color:#6F8C9E;margin-top:14px}

/* ---------- masthead ---------- */
.mast{position:relative;overflow:hidden;padding:26px 0 8px}
.livery{position:absolute;left:-10%;right:-10%;top:58px;height:96px;transform:skewY(-4deg);pointer-events:none}
.livery i{display:block;height:50%}
.livery i:first-child{background:var(--orange)}
.livery i:last-child{background:var(--powder);opacity:.85}
.mast .wrap{position:relative}
.logo{margin:0;font:900 clamp(4.2rem,14vw,10.5rem)/.8 "Big Shoulders Display",Impact,sans-serif;letter-spacing:-.01em;color:var(--navy);display:flex;align-items:flex-end;gap:.08em}
.logo svg{width:.6em;height:.6em;margin-bottom:.06em;flex:none}
.tag{margin:22px 0 0;font-weight:600;font-size:1.02rem;color:var(--muted);max-width:60ch}
#needle{transform-origin:50px 54px;transform:rotate(30deg)}
@media (prefers-reduced-motion:no-preference){
  #needle{animation:rev 1.6s cubic-bezier(.3,.7,.2,1) .2s both}
  @keyframes rev{0%{transform:rotate(-120deg)}55%{transform:rotate(108deg)}75%{transform:rotate(80deg)}100%{transform:rotate(30deg)}}
}

/* ---------- shared bits ---------- */
.plate{display:inline-flex;align-items:center;font-weight:700;font-size:.78rem;letter-spacing:.02em;padding:3px 10px;border-radius:999px;color:#fff;background:var(--pc,var(--ink))}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .plate{color:#081923}}
:root[data-theme="dark"] .plate{color:#081923}
.src{font-size:.85rem;color:var(--muted)}
.src a{color:var(--ink);font-weight:600;text-decoration-color:var(--orange);text-decoration-thickness:2px;text-underline-offset:3px}
.credit{font-size:.72rem;color:var(--muted);line-height:1.3;margin-top:6px}
.credit a{color:inherit}
.ph{position:relative;aspect-ratio:16/9;overflow:hidden;background:var(--deep)}
.ph img{width:100%;height:100%;object-fit:cover;transition:transform .5s ease}
.ph.fallback{background:repeating-linear-gradient(-28deg,var(--pc,var(--orange)) 0 26px,color-mix(in srgb,var(--pc,var(--orange)) 70%,var(--deep)) 26px 52px)}
.ph.fallback > .fb{position:absolute;inset:0;display:grid;place-items:center;font:900 clamp(2.2rem,5vw,3.4rem)/1 "Big Shoulders Display",Impact,sans-serif;color:#fff;text-shadow:0 2px 0 rgba(0,0,0,.15)}
.mini-card .ph.fallback > .fb{font-size:1.5rem}
.lead .ph.fallback > .fb{display:none}
a.card:hover .ph img,.lead:hover .ph img{transform:scale(1.04)}

/* ---------- hero ---------- */
.hero{display:grid;grid-template-columns:minmax(0,1.7fr) minmax(0,1fr);gap:22px;margin:30px 0 0}
.lead{position:relative;border-radius:10px;overflow:hidden;box-shadow:var(--shadow);background:var(--deep);min-height:480px;display:flex;align-items:flex-end;color:#fff}
.lead .ph{position:absolute;inset:0;aspect-ratio:auto}
.lead .ph::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(5,20,30,0) 25%,rgba(5,20,30,.55) 55%,rgba(5,20,30,.92) 100%)}
.lead .txt{position:relative;padding:30px 32px 26px;z-index:1}
.lead h2{font:900 clamp(2.3rem,4.6vw,3.9rem)/.92 "Big Shoulders Display",Impact,sans-serif;margin:14px 0 12px;max-width:18ch;text-wrap:balance}
.lead h2 a{text-decoration:none}
.lead p{margin:0 0 12px;max-width:60ch;font-size:1.07rem;color:#E3EEF5}
.lead .src,.lead .src a,.lead .credit{color:#C8DCE8}
.side{display:grid;gap:22px;align-content:start}
.mini-card{display:grid;grid-template-columns:140px 1fr;gap:14px;background:var(--card);border-radius:10px;overflow:hidden;box-shadow:var(--shadow);text-decoration:none}
.mini-card .ph{aspect-ratio:auto;height:100%;min-height:120px}
.mini-card .t{padding:14px 14px 14px 0}
.mini-card h3{margin:8px 0 0;font:800 1.35rem/1.02 "Big Shoulders Display",Impact,sans-serif}

/* ---------- sections ---------- */
section{padding:70px 0 0}
.sh{display:grid;grid-template-columns:auto 1fr;align-items:end;gap:6px 18px;margin-bottom:22px}
.gear{font:900 clamp(4.6rem,10vw,7.5rem)/.75 "Big Shoulders Display",Impact,sans-serif;color:var(--orange);grid-row:span 2}
.sh h2{margin:0;font:900 clamp(2.3rem,4.6vw,3.4rem)/.9 "Big Shoulders Display",Impact,sans-serif}
.sh p{margin:0;color:var(--muted);font-weight:500}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 20px}
.chip{font:600 .92rem "Barlow",sans-serif;border:1.5px solid var(--line);background:var(--card);color:var(--ink);padding:6px 14px;border-radius:999px;cursor:pointer;display:inline-flex;align-items:center;gap:7px}
.chip[aria-pressed="true"]{background:var(--ink);color:var(--bg);border-color:var(--ink)}
.chip .dot{width:9px;height:9px;border-radius:50%}

/* ---------- race preview band ---------- */
.race{background:var(--deep);color:#E7F1F7;margin-top:70px;padding:56px 0 60px;position:relative;overflow:hidden}
.race::before{content:"";position:absolute;right:-8%;top:-30px;width:55%;height:46px;background:var(--orange);transform:skewY(-4deg)}
.race .sh h2{color:#fff}.race .sh p{color:#9FBBCC}
.rgrid{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:28px}
.rcard{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.09);border-radius:10px;padding:22px 24px}
.rcard h3{margin:0 0 14px;font:800 1.5rem/1 "Big Shoulders Display",Impact,sans-serif;color:#fff}
.rname{font:900 clamp(2.2rem,4.4vw,3.4rem)/.9 "Big Shoulders Display",Impact,sans-serif;margin:6px 0 6px;color:#fff}
.rmeta{color:#A9C3D2;font-weight:500}
.count{display:flex;gap:10px;margin:18px 0 6px}
.count div{background:rgba(255,255,255,.07);border-radius:6px;padding:8px 12px 6px;min-width:70px;text-align:center}
.count b{display:block;font:900 2.4rem/.9 "Big Shoulders Display",Impact,sans-serif;color:var(--orange)}
.count span{font-size:.78rem;color:#A9C3D2}
.track{position:relative;margin-top:10px}
.track svg{width:100%;height:auto;max-height:380px;display:block}
.track path.base{fill:none;stroke:rgba(255,255,255,.12);stroke-width:26;stroke-linejoin:round;stroke-linecap:round}
.track path.line{fill:none;stroke:#fff;stroke-width:9;stroke-linejoin:round;stroke-linecap:round}
.track path.run{fill:none;stroke:var(--orange);stroke-width:9;stroke-linejoin:round;stroke-linecap:round}
.facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:10px;margin-top:8px}
.facts div{border-top:2px solid var(--orange);padding-top:6px}
.facts b{display:block;font:800 1.6rem/1 "Big Shoulders Display",Impact,sans-serif;color:#fff}
.facts span{font-size:.8rem;color:#A9C3D2}
.sess{list-style:none;margin:0;padding:0;display:grid;gap:6px;font-size:.95rem}
.sess li{display:flex;justify-content:space-between;gap:10px;border-bottom:1px dashed rgba(255,255,255,.12);padding-bottom:6px}
.sess span{color:#A9C3D2}
.winners{list-style:none;margin:0;padding:0;display:grid;gap:2px}
.winners li{display:grid;grid-template-columns:70px 1fr auto;align-items:baseline;gap:12px;padding:8px 0;border-bottom:1px solid rgba(255,255,255,.08)}
.winners .y{font:900 1.7rem/1 "Big Shoulders Display",Impact,sans-serif;color:var(--orange)}
.winners .n{font-weight:700;color:#fff}
.winners .tm{font-size:.85rem;color:#A9C3D2;text-align:right}
.bars{display:grid;gap:7px}
.brow{display:grid;grid-template-columns:22px 52px 1fr 54px;align-items:center;gap:10px;font-size:.9rem}
.brow .p{color:#A9C3D2;text-align:right;font-weight:600}
.brow .c{font:800 1.15rem/1 "Big Shoulders Display",Impact,sans-serif;color:#fff}
.brow .tr{height:16px;background:rgba(255,255,255,.07);border-radius:3px;overflow:hidden}
.brow .f{height:100%;width:0;background:#6FAED3;border-radius:3px;transition:width 1.1s cubic-bezier(.3,.7,.2,1)}
.brow:first-child .f{background:var(--orange)}
.brow .pt{text-align:right;font-weight:700;color:#fff}
.rnote{font-size:.78rem;color:#86A3B5;margin:14px 0 0}
.rnote a{color:inherit}
.sched{list-style:none;margin:0;padding:0}
.sched li{display:grid;grid-template-columns:64px 1fr;gap:12px;align-items:center;padding:8px 0;border-bottom:1px solid rgba(255,255,255,.08)}
.sched .d{background:var(--orange);color:#fff;font:800 1.05rem/1 "Big Shoulders Display",Impact,sans-serif;text-align:center;padding:6px 4px;border-radius:4px}
.sched .w{font-weight:600;line-height:1.2;color:#fff}
.sched small{display:block;font-weight:400;color:#A9C3D2;font-size:.82rem}

/* ---------- news grid ---------- */
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:22px}
.card{background:var(--card);border-radius:10px;overflow:hidden;box-shadow:var(--shadow);display:flex;flex-direction:column}
.card .ph .plate{position:absolute;left:12px;top:12px;z-index:1}
.card .body{padding:16px 18px 16px;display:flex;flex-direction:column;gap:8px;flex:1}
.card .dt{font-size:.8rem;color:var(--muted);font-weight:600}
.card h3{margin:0;font:800 1.5rem/1 "Big Shoulders Display",Impact,sans-serif}
.card h3 a{text-decoration:none}
.card h3 a:hover{text-decoration:underline;text-decoration-color:var(--orange)}
.card p{margin:0;font-size:.96rem}
.card details summary{cursor:pointer;font-weight:700;font-size:.9rem;color:var(--orange)}
.card details div{margin-top:8px;font-size:.95rem;white-space:pre-line}
.card .src{margin-top:auto;padding-top:6px}
.subh{font:800 1.6rem/1 "Big Shoulders Display",Impact,sans-serif;margin:0 0 14px}
.dgrid{margin-bottom:34px}
.empty{background:var(--card);padding:28px;border-radius:10px;color:var(--muted)}
.more{display:flex;justify-content:center;margin-top:26px}
.more button{font:700 1rem "Barlow",sans-serif;background:var(--ink);color:var(--bg);border:0;border-radius:999px;padding:11px 22px;cursor:pointer}

/* ---------- stats ---------- */
.stats{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}
.stat{background:var(--card);border-radius:10px;padding:24px 26px;box-shadow:var(--shadow)}
.stat.wide{grid-column:1/-1}
.stat .eyebrow{margin:0;font-weight:700;font-size:.78rem;letter-spacing:.06em;text-transform:uppercase;color:var(--orange)}
.stat h3{margin:6px 0 16px;font:900 2rem/1 "Big Shoulders Display",Impact,sans-serif}
.sbars{display:grid;gap:9px}
.sbar{display:grid;grid-template-columns:150px 1fr 80px;align-items:center;gap:12px}
.sbar .l{font-weight:600}
.sbar .t{height:22px;background:var(--bg);border-radius:4px;overflow:hidden}
.sbar .f{height:100%;width:0;background:var(--powder);border-radius:4px;transition:width 1.2s cubic-bezier(.3,.7,.2,1)}
.sbar.hl .f{background:var(--orange)}
.sbar.hl .l,.sbar.hl .v{color:var(--orange)}
.sbar .v{white-space:nowrap;text-align:right;font:800 1.35rem/1 "Big Shoulders Display",Impact,sans-serif}
.stack .barline{display:flex;height:34px;border-radius:6px;overflow:hidden}
.stack .seg{height:100%;width:0;transition:width 1.2s cubic-bezier(.3,.7,.2,1)}
.stack .leg{list-style:none;margin:14px 0 0;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px 14px;font-size:.92rem}
.stack .leg li{display:flex;align-items:center;gap:8px}
.stack .leg i{width:12px;height:12px;border-radius:3px;flex:none}
.stack .leg b{margin-left:auto;font:800 1.15rem/1 "Big Shoulders Display",Impact,sans-serif}
.big3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}
.big3 div{border-top:3px solid var(--orange);padding-top:8px}
.big3 b{display:block;font:900 clamp(2rem,4vw,2.8rem)/1 "Big Shoulders Display",Impact,sans-serif}
.big3 span{font-size:.86rem;color:var(--muted);line-height:1.3;display:block;margin-top:4px}
.snote{margin:16px 0 0;font-size:.95rem}
.ssrc{margin:10px 0 0;font-size:.8rem;color:var(--muted)}
.ssrc a{color:inherit}

/* ---------- explainers, people, routes ---------- */
.explain-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:18px}
.explain{background:var(--card);border-radius:10px;padding:22px;box-shadow:var(--shadow);border-top:5px solid var(--pc)}
.explain .eyebrow{margin:0;font-weight:700;font-size:.8rem;color:var(--pc);text-transform:uppercase;letter-spacing:.06em}
.explain h3{margin:6px 0 8px;font:800 1.6rem/1 "Big Shoulders Display",Impact,sans-serif}
.explain p{margin:0 0 12px;font-size:.96rem}
.explain a{font-weight:700;font-size:.9rem;text-decoration-color:var(--pc)}
.editorial-note{color:var(--muted);font-size:.88rem;margin-top:16px;max-width:80ch}
.people{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:18px}
.person{background:var(--card);border-radius:10px;padding:22px 24px 20px;position:relative;overflow:hidden;box-shadow:var(--shadow)}
.person .ini{position:absolute;right:-6px;top:-18px;font:900 8rem/1 "Big Shoulders Display",Impact,sans-serif;color:transparent;-webkit-text-stroke:2px var(--pc);opacity:.4;pointer-events:none}
.person h3{position:relative;margin:0;font:900 2.2rem/.9 "Big Shoulders Display",Impact,sans-serif;max-width:9ch}
.person .team{position:relative;margin:8px 0 16px;font-weight:600;font-size:.9rem;color:var(--pc)}
.person dl{margin:0;display:grid;gap:12px;position:relative}
.person dt{font-weight:700;font-size:.9rem}
.person dd{margin:2px 0 0;font-size:.95rem}
.person .src{display:block;margin-top:16px}
.routes{display:grid;gap:18px}
.route{background:var(--card);border-radius:10px;padding:24px 26px;display:grid;grid-template-columns:minmax(0,1fr) 230px;gap:10px 30px;box-shadow:var(--shadow)}
.route header{grid-column:1/-1;display:flex;align-items:baseline;flex-wrap:wrap;gap:6px 16px}
.route h3{margin:0;font:900 2rem/.95 "Big Shoulders Display",Impact,sans-serif}
.route .km{font:800 1.25rem "Big Shoulders Display",Impact,sans-serif;color:var(--orange)}
.line{list-style:none;margin:18px 0;padding:0;display:flex;position:relative}
.line::before{content:"";position:absolute;left:9px;right:9px;top:7px;height:4px;background:var(--orange);border-radius:2px}
.line li{flex:1;position:relative;padding-top:24px;font-size:.86rem;font-weight:600;line-height:1.2;padding-right:6px}
.line li::before{content:"";position:absolute;top:0;left:0;width:18px;height:18px;border-radius:50%;background:var(--card);border:4px solid var(--orange)}
.line li:last-child{flex:0 0 auto;text-align:right;padding-right:0}
.line li:last-child::before{left:auto;right:0;background:var(--orange)}
.route .desc{margin:0;max-width:64ch}
.rfacts{list-style:none;margin:0;padding:0;font-size:.92rem;align-self:start}
.rfacts li{display:flex;justify-content:space-between;gap:10px;padding:6px 0;border-bottom:1px solid var(--line)}
.rfacts span{color:var(--muted)}
.go{display:inline-block;margin-top:14px;font-weight:700;font-size:.95rem;text-decoration:none;background:var(--orange);color:#fff;padding:9px 16px;border-radius:999px}
.warn{display:inline-block;margin-top:12px;font-size:.84rem;font-weight:700;padding:3px 10px;border-radius:3px;border:2px dashed var(--orange)}

footer{margin-top:90px;padding:30px 0 130px;background:var(--deep);color:#A9C3D2;font-size:.9rem}
footer p{margin:0 0 8px;max-width:80ch}
.footerlinks{display:flex;gap:18px;margin-top:14px}
.footerlinks a{color:#fff;font-weight:600}

/* ---------- gear shifter ---------- */
.shifter{position:fixed;right:18px;bottom:calc(18px + env(safe-area-inset-bottom,0px));z-index:20;background:#0D2B3E;color:#A9D3EB;border-radius:14px;padding:12px 14px 10px;box-shadow:0 10px 30px -10px rgba(5,25,40,.6);border:1px solid rgba(169,211,235,.25)}
.gate{position:relative;width:132px;height:96px}
.gate svg{position:absolute;inset:0}
.gate button{position:absolute;width:30px;height:30px;margin:-15px 0 0 -15px;border-radius:50%;border:0;background:transparent;color:inherit;font:800 .95rem "Big Shoulders Display",Impact,sans-serif;cursor:pointer;z-index:2;display:grid;place-items:center}
.gate button[aria-current="true"]{color:#fff}
.knob{position:absolute;width:30px;height:30px;margin:-15px 0 0 -15px;border-radius:50%;background:var(--orange);z-index:1;left:110px;top:82px;box-shadow:inset 0 -3px 0 rgba(0,0,0,.2)}
@media (prefers-reduced-motion:no-preference){.knob{transition:left .28s cubic-bezier(.5,0,.2,1),top .28s cubic-bezier(.5,0,.2,1)}}
.gearname{margin-top:6px;font-weight:700;font-size:.8rem;text-align:center}

@media (max-width:980px){
  .hero{grid-template-columns:1fr}
  .side{grid-template-columns:repeat(auto-fit,minmax(260px,1fr))}
  .rgrid{grid-template-columns:1fr}
  .stats{grid-template-columns:1fr}
  .route{grid-template-columns:1fr}
}
@media (max-width:620px){
  .lead{min-height:420px}
  .lead .txt{padding:22px 20px 20px}
  .mini-card{grid-template-columns:110px 1fr}
  .line{flex-direction:column;gap:12px;margin:14px 0}
  .line::before{left:7px;right:auto;top:9px;bottom:9px;width:4px;height:auto}
  .line li{padding:0 0 0 30px;text-align:left!important}
  .line li:last-child::before{left:0;right:auto}
  .shifter{right:10px;transform:scale(.8);transform-origin:bottom right}
  .person .ini{font-size:6rem}
  .brow{grid-template-columns:20px 44px 1fr 46px;gap:8px}
  .sbar{grid-template-columns:96px 1fr 62px;gap:8px}
  .sbar .l{font-size:.88rem}
}
</style>
</head>
<body>
<header class="bar">
  <div class="wrap">
    <a class="mini" href="#vrh" aria-label="Okretaji – na vrh"><svg viewBox="0 0 100 70" aria-hidden="true"><path d="M14 58 A40 40 0 0 1 75 20" fill="none" stroke="currentColor" stroke-width="11" stroke-linecap="round"/><path d="M75 20 A40 40 0 0 1 88 58" fill="none" stroke="var(--orange)" stroke-width="11" stroke-linecap="round"/></svg>Okretaji</a>
    <nav class="nav" aria-label="Rubrike">
      <a href="#novosti">Novosti</a><a href="#utrka">Sljedeća utrka</a><a href="#brojke">U brojkama</a><a href="#vozaci">Iza kacige</a><a href="#rute">Motorute</a>
    </nav>
  </div>
</header>

<div class="mast" id="vrh">
  <div class="livery" aria-hidden="true"><i></i><i></i></div>
  <div class="wrap">
    <h1 class="logo">
      <svg viewBox="0 0 100 70" aria-hidden="true">
        <path d="M14 58 A40 40 0 0 1 75 20" fill="none" stroke="currentColor" stroke-width="9" stroke-linecap="round"/>
        <path d="M75 20 A40 40 0 0 1 88 58" fill="none" stroke="var(--orange)" stroke-width="9" stroke-linecap="round"/>
        <g id="needle"><line x1="50" y1="54" x2="50" y2="18" stroke="var(--orange)" stroke-width="6" stroke-linecap="round"/></g>
        <circle cx="50" cy="54" r="8" fill="currentColor"/>
      </svg>Okretaji</h1>
    <p class="tag">Auto, moto i motosport, tehnologija i energija – plus ceste koje vrijedi odvoziti.</p>
  </div>
</div>

<main>
  <div class="wrap">
    <div class="hero" id="novosti">
      <article class="lead" id="lead"></article>
      <div class="side" id="side"></div>
    </div>
  </div>

  <section class="race" id="utrka" aria-labelledby="h-utrka" hidden>
    <div class="wrap">
      <div class="sh"><span class="gear" aria-hidden="true">2</span><h2 id="h-utrka">Sljedeća utrka</h2><p>Formula 1 – staza, brojke i raspored vikenda.</p></div>
      <div class="rgrid">
        <div class="rcard">
          <div class="rmeta" id="raceRound"></div>
          <div class="rname" id="raceName"></div>
          <div class="rmeta" id="raceWhere"></div>
          <div class="count" id="count" aria-live="polite"></div>
          <div class="track" id="track"></div>
          <div class="facts" id="trackFacts"></div>
        </div>
        <div style="display:grid;gap:22px;align-content:start">
          <div class="rcard"><h3>Pobjednici ovdje – zadnjih 5 utrka</h3><ol class="winners" id="winners"></ol></div>
          <div class="rcard"><h3 id="standTitle">Poredak prvenstva</h3><div class="bars" id="bars"></div></div>
        </div>
      </div>
      <div class="rgrid" style="margin-top:22px">
        <div class="rcard"><h3>Raspored vikenda (tvoje vrijeme)</h3><ul class="sess" id="sess"></ul></div>
        <div class="rcard"><h3>Nadolazeće utrke</h3><ol class="sched" id="sched"></ol></div>
      </div>
      <p class="rnote">Podaci: <a href="https://github.com/jolpica/jolpica-f1" target="_blank" rel="noopener">Jolpica F1 API</a>; obris staze: <a href="https://github.com/bacinger/f1-circuits" target="_blank" rel="noopener">bacinger/f1-circuits</a> (MIT licenca).</p>
    </div>
  </section>

  <div class="wrap">
    <section id="brojke" aria-labelledby="h-brojke">
      <div class="sh"><span class="gear" aria-hidden="true">3</span><h2 id="h-brojke">U brojkama</h2><p>Promet, emisije i električna vozila – činjenice bez navijanja.</p></div>
      <div class="stats">
        <article class="stat wide">
          <p class="eyebrow">Emisije stakleničkih plinova, 2024.</p>
          <h3>Tko zagađuje svijet?</h3>
          <div class="sbars" data-bars='[["Kina",29.2],["SAD",11.1],["Indija",8.2],["Europska unija",5.9],["Ostatak svijeta",45.6]]' data-hl="Europska unija" data-unit="%"></div>
          <p class="snote">Svijet je 2024. ispustio rekordnih 53,2 milijarde tona CO₂e (+1,3 %). EU je jedno od rijetkih velikih gospodarstava koje je smanjilo emisije (−1,8 %) i sad je 35 % ispod razine iz 1990.</p>
          <p class="ssrc">Izvor: <a href="https://edgar.jrc.ec.europa.eu/report_2025" target="_blank" rel="noopener">EDGAR / JRC, 2025.</a></p>
        </article>
        <article class="stat">
          <p class="eyebrow">Novi automobili u EU, 2025.</p>
          <h3>Što Europljani kupuju?</h3>
          <div class="stack" data-stack='[["Hibridi",34.5,"var(--blue)"],["Benzin",26.6,"var(--muted)"],["Električni",17.4,"var(--green)"],["Plug-in hibridi",9.4,"var(--powder)"],["Dizel",8.9,"var(--ink)"],["Ostalo",3.2,"var(--line)"]]'></div>
          <p class="snote">Benzin i dizel zajedno pali su na 35,5 % tržišta, s 45,2 % godinu ranije.</p>
          <p class="ssrc">Izvor: <a href="https://www.acea.auto/pc-registrations/new-car-registrations-1-8-in-2025-battery-electric-17-4-market-share/" target="_blank" rel="noopener">ACEA, 2026.</a></p>
        </article>
        <article class="stat">
          <p class="eyebrow">Udio električnih među novim autima, 2025.</p>
          <h3>Europa u dvije brzine</h3>
          <div class="big3">
            <div><b>96 %</b><span>Norveška</span></div>
            <div><b>17,4 %</b><span>prosjek EU</span></div>
            <div><b>6 %</b><span>Italija</span></div>
          </div>
          <p class="ssrc">Izvor: ACEA, prema <a href="https://www.best-selling-cars.com/europe/2025-full-year-europe-bev-electric-car-sales-per-european-country/" target="_blank" rel="noopener">best-selling-cars.com</a></p>
        </article>
        <article class="stat">
          <p class="eyebrow">Promet i klima u EU, 2023.</p>
          <h3>Koliko zagađuje promet?</h3>
          <div class="big3">
            <div><b>31 %</b><span>svih emisija EU dolazi iz prometa</span></div>
            <div><b>73 %</b><span>prometnih emisija nastaje na cestama</span></div>
            <div><b>52 %</b><span>prometnih emisija čine automobili i kombiji</span></div>
          </div>
          <p class="snote">Za razliku od industrije i energetike, emisije prometa danas su veće nego 1990.</p>
          <p class="ssrc">Izvor: <a href="https://www.eea.europa.eu/en/analysis/publications/sustainability-of-europes-mobility-systems-2025/climate" target="_blank" rel="noopener">Europska agencija za okoliš, 2025.</a></p>
        </article>
      </div>
      <h3 class="subh" style="margin-top:34px">Tehnika i energija – vodiči</h3>
      <div class="explain-grid">
      <article class="explain" style="--pc:var(--blue)">
        <p class="eyebrow">Tehnologija</p><h3>Električni ili benzinski pogon?</h3>
        <p>Usporedba ima smisla tek kad se gledaju cijeli životni ciklus, veličina vozila, kilometraža i izvor električne energije — ne samo emisije iz auspuha.</p>
        <a href="https://www.iea.org/reports/global-ev-outlook-2024" target="_blank" rel="noopener">Podaci i analiza IEA-e</a>
      </article>
      <article class="explain" style="--pc:var(--green)">
        <p class="eyebrow">Energija</p><h3>Koliko je energija stvarno zelena?</h3>
        <p>Solarne i vjetroelektrane imaju emisije pri proizvodnji, gradnji i zbrinjavanju. Za poštenu usporedbu treba računati emisije po proizvedenom kilovatsatu kroz cijeli vijek trajanja.</p>
        <a href="https://www.ipcc.ch/report/ar6/wg3/" target="_blank" rel="noopener">IPCC: ublažavanje klimatskih promjena</a>
      </article>
      <article class="explain" style="--pc:var(--orange)">
        <p class="eyebrow">Baterije</p><h3>Što se događa s baterijom?</h3>
        <p>Rudarstvo, rafiniranje i proizvodnja baterija imaju utjecaj na okoliš. Važni su i trajnost, popravak, ponovna uporaba te stvarna stopa recikliranja — ne samo teorijska mogućnost.</p>
        <a href="https://www.iea.org/topics/batteries-and-secure-energy-transitions" target="_blank" rel="noopener">IEA: baterije i energetska tranzicija</a>
      </article>
      <article class="explain" style="--pc:var(--red)">
        <p class="eyebrow">Provjera tvrdnji</p><h3>Brojke prije slogana</h3>
        <p>Razlikujemo izravne emisije, emisije tijekom životnog ciklusa, potrošnju energije i lokalno onečišćenje zraka. Svaka tvrdnja treba imati izvor, godinu i jasnu metodologiju.</p>
        <a href="https://ourworldindata.org/energy" target="_blank" rel="noopener">Our World in Data: energija</a>
      </article>
    </div>
    <p class="editorial-note">Kratki vodiči za snalaženje u temi. Svaka tvrdnja ima izvor, a izmjerene podatke odvajamo od procjena i prognoza.</p>
    </section>

    <section id="sve-vijesti" aria-labelledby="h-novosti" style="padding-top:60px">
      <div class="sh"><span class="gear" aria-hidden="true">1</span><h2 id="h-novosti">Sve vijesti</h2><p>Izbor najvažnijeg iz auto-moto svijeta i motosporta.</p></div>
      <div class="chips" id="newsChips" role="group" aria-label="Filtriraj novosti"></div>
      <div class="grid" id="newsList"></div>
      <div class="more" id="moreWrap" hidden><button type="button" id="moreBtn">Prikaži još</button></div>
    </section>

    <section id="vozaci" aria-labelledby="h-vozaci">
      <div class="sh"><span class="gear" aria-hidden="true">4</span><h2 id="h-vozaci">Iza kacige</h2><p>Što voze kad nisu na stazi, čime se bave i što sami objavljuju.</p></div>
      <div id="driverNewsWrap" hidden><h3 class="subh">Najnovije iz života vozača</h3><div class="grid dgrid" id="driverNews"></div></div>
      <div class="people" id="peopleList"></div>
    </section>

    <section id="rute" aria-labelledby="h-rute">
      <div class="sh"><span class="gear" aria-hidden="true">5</span><h2 id="h-rute">Motorute</h2><p>Od istarskih brežuljaka do najviših alpskih prijevoja.</p></div>
      <div class="chips" id="routeChips" role="group" aria-label="Filtriraj rute"></div>
      <div class="routes" id="routeList"></div>
    </section>


  </div>
</main>

<footer>
  <div class="wrap">
    <p>Vijesti se automatski prikupljaju iz RSS izvora navedenih uz svaku vijest; sažeci su orijentacija, a cijeli kontekst je u izvornom članku.</p>
    <p>Ilustrativne fotografije su slike pod licencama Creative Commons pronađene preko Openversea, uz navedenog autora i licencu. Ne prikazuju nužno točno događaj iz vijesti.</p>
    <p>Kilometraže ruta su približne. Prije alpskih prijevoja provjeri je li cesta otvorena – većina se zatvara od studenog do svibnja.</p>
    <p class="upd" id="updated"></p>
    <nav class="footerlinks" aria-label="Informacije o portalu"><a href="o-nama.html">O nama</a><a href="kontakt.html">Kontakt</a><a href="privatnost.html">Privatnost</a></nav>
  </div>
</footer>

<nav class="shifter" aria-label="Mjenjač – navigacija po sekcijama">
  <div class="gate">
    <svg viewBox="0 0 132 96" aria-hidden="true"><path d="M22 14 V82 M66 14 V82 M110 14 V82 M22 48 H110" fill="none" stroke="currentColor" stroke-opacity=".45" stroke-width="5" stroke-linecap="round"/></svg>
    <span class="knob" id="knob"></span>
    <button type="button" data-t="novosti" data-n="1: Novosti" style="left:22px;top:14px" aria-label="Novosti">1</button>
    <button type="button" data-t="utrka" data-n="2: Sljedeća utrka" style="left:22px;top:82px" aria-label="Sljedeća utrka">2</button>
    <button type="button" data-t="brojke" data-n="3: U brojkama" style="left:66px;top:14px" aria-label="U brojkama">3</button>
    <button type="button" data-t="vozaci" data-n="4: Iza kacige" style="left:66px;top:82px" aria-label="Iza kacige">4</button>
    <button type="button" data-t="rute" data-n="5: Motorute" style="left:110px;top:14px" aria-label="Motorute">5</button>
    <button type="button" data-t="vrh" data-n="R: na vrh" style="left:110px;top:82px" aria-label="Na vrh stranice">R</button>
  </div>
  <div class="gearname" id="gearname">N: start</div>
</nav>

<script>
const CATS = {
  f1:{name:"Formula 1",color:"var(--red)",short:"F1"},
  motogp:{name:"MotoGP",color:"var(--blue)",short:"MotoGP"},
  auto:{name:"Automobili",color:"var(--orange)",short:"Auto"},
  moto:{name:"Motocikli",color:"var(--yellow)",short:"Moto"},
  reli:{name:"Reli",color:"var(--green)",short:"Reli"},
  tech:{name:"Tehnologija",color:"var(--blue)",short:"Tech"},
  energy:{name:"Energija",color:"var(--green)",short:"Energija"},
  kaciga:{name:"Iza kacige",color:"var(--yellow)",short:"Iza kacige"}
};
const CAT_FALLBACK={name:"Vijesti",color:"var(--orange)",short:"Vijesti"};
const REGIONS = {istra:"Istra i Kvarner", hr:"Ostatak Hrvatske", slo:"Slovenija", ita:"Italija"};

function gm(points){
  const enc = p => encodeURIComponent(p);
  const o = points[0], d = points[points.length-1], w = points.slice(1,-1);
  return "https://www.google.com/maps/dir/?api=1&travelmode=driving&origin="+enc(o)+"&destination="+enc(d)+(w.length?"&waypoints="+w.map(enc).join("%7C"):"");
}

const ROUTES = [
  {r:"istra", n:"Gradići na brežuljcima", km:"70", pts:["Žminj","Pazin","Motovun","Grožnjan","Buje"],
   desc:"Klasični krug unutrašnjosti Istre: serpentine prema Motovunu, kamene kuće Grožnjana i pogled na dolinu Mirne. Mali promet izvan sezone, puno mjesta za kavu i tartufe.",
   tip:"Zavoji, sela", season:"Cijele godine", diff:"Lagano"},
  {r:"istra", n:"Učka i plominska obala", km:"75", pts:["Lupoglav","Poklon, Učka","Lovran","Mošćenička Draga","Plomin","Labin"],
   desc:"Preko prijevoja Poklon spuštaš se na opatijsku rivijeru, pa uz more prema Plominu i Labinu. Gornji dio Učke ima zavoje uz šumu i otvoren pogled na Kvarner.",
   tip:"Prijevoj, obala", season:"Ožujak – studeni", diff:"Srednje"},
  {r:"istra", n:"Cres i Lošinj", km:"80", pts:["Porozina","Cres","Osor","Mali Lošinj"],
   desc:"Trajektom iz Brestove na Porozinu, pa hrptom otoka kroz kamenjar i pašnjake. Kod Osora prelaziš pokretni most na Lošinj.",
   tip:"Otok, trajekt", season:"Travanj – listopad", diff:"Lagano"},
  {r:"hr", n:"Magistrala i Velebit", km:"200", pts:["Rijeka","Senj","Karlobag","Baške Oštarije","Gospić"],
   desc:"Jadranska magistrala od Rijeke do Karlobaga s morem zdesna cijelim putem, pa uspon serpentinama na Baške Oštarije. Pazi na buru – na ovoj dionici zna biti opasna.",
   tip:"Obala, prijevoj", season:"Travanj – listopad", diff:"Srednje", warn:"Bura – provjeri HAK prije polaska"},
  {r:"hr", n:"Gorski kotar i dolina Kupe", km:"90", pts:["Grobnik","Fužine","Lokve","Delnice","Brod na Kupi"],
   desc:"Šumske ceste kroz Gorski kotar, uz jezera Bajer i Lokvarka, pa spust u dolinu Kupe uz granicu sa Slovenijom. Ljeti osvježenje, ujesen prekrasne boje.",
   tip:"Šuma, rijeka", season:"Svibanj – listopad", diff:"Lagano"},
  {r:"hr", n:"Biokovo – Sveti Jure", km:"25", pts:["Makarska","Park prirode Biokovo","Sveti Jure, Biokovo"],
   desc:"Uska cesta do 1762 m iznad Makarske, s jednim od najljepših pogleda na Jadran. Naplata ulaza u park, promet ograničen.",
   tip:"Planinska cesta", season:"Svibanj – listopad", diff:"Zahtjevno"},
  {r:"slo", n:"Vršič", km:"50", pts:["Kranjska Gora","Vršič","Trenta","Bovec"],
   desc:"Najviši cestovni prijevoj u Sloveniji, 1611 m, s 50 numeriranih serpentina – na sjevernoj strani popločenih kockom. Spust prema Trenti vodi u dolinu Soče.",
   tip:"Prijevoj, serpentine", season:"Svibanj – listopad", diff:"Zahtjevno", warn:"Zimi zatvoren"},
  {r:"slo", n:"Mangartsko sedlo", km:"12", pts:["Log pod Mangartom","Mangartsko sedlo"],
   desc:"Najviša cesta Slovenije penje se do oko 2050 m kroz tunele isklesane u stijeni. Kratka, ali spektakularna; lako se spaja s Vršičem i Predilom.",
   tip:"Visokoplaninska", season:"Lipanj – listopad", diff:"Zahtjevno", warn:"Cestarina, zimi zatvoren"},
  {r:"ita", n:"Sella Ronda, Dolomiti", km:"55", pts:["Passo Sella","Passo Pordoi","Passo Campolongo","Passo Gardena"],
   desc:"Krug oko masiva Sella preko četiri prijevoja iznad 1800 m. Dolomiti u punom sjaju, ali ljeti vrlo prometno – kreni rano ujutro.",
   tip:"Četiri prijevoja", season:"Lipanj – rujan", diff:"Srednje", warn:"Zimi zatvoreno"},
  {r:"ita", n:"Passo dello Stelvio", km:"50", pts:["Prato allo Stelvio","Passo dello Stelvio","Bormio"],
   desc:"Legendarni prijevoj na 2757 m s 48 serpentina na strani od Prata. Spust prema Bormiu je brži i otvoreniji. Za motoriste obavezna stanica barem jednom.",
   tip:"Legenda Alpa", season:"Lipanj – rujan", diff:"Zahtjevno", warn:"Zimi zatvoren"}
];

const PEOPLE = [
  {n:"Max Verstappen", team:"F1, Red Bull – četverostruki prvak", c:"var(--blue)",
   car:"Nema stalni auto za svaki dan, nego se izmjenjuje po kolekciji: Aston Martin Valkyrie, Porsche 911 GT3 RS, Honda NSX Type S (Hondin poklon za drugi naslov). Prvi auto bio mu je žuti Renault Clio.",
   hobby:"Sim racing. Od 2015. vozi za virtualni tim Redline, a utrke odvozi i u hotelskoj sobi za vikend utrke. Simulator kod kuće vrijedi desetke tisuća dolara.",
   fact:"Želi kroz vlastiti GT3 tim dovesti talentirane sim vozače u pravi motosport, jer si mnogi ne mogu priuštiti karting.",
   src:"PlanetF1", u:"https://www.planetf1.com/features/max-verstappen-car-collection"},
  {n:"Charles Leclerc", team:"F1, Ferrari", c:"var(--red)",
   car:"Kao Ferrarijev vozač u javnosti se vozi Ferrarijima.",
   hobby:"Klavir i komponiranje. Objavio je EP s francuskim pijanistom Sofianeom Pamartom, a skladbe poput MC24 i SIN24 posvetio je svojim pobjedama. Strastveni je šahist.",
   fact:"Ima vlastitu marku niskokaloričnog sladoleda LEC, pokrenutu 2024. s talijanskim Gromom.",
   src:"PlanetF1", u:"https://www.planetf1.com/news/charles-leclerc-releases-new-music-2024-season"},
  {n:"Lewis Hamilton", team:"F1, Ferrari – sedmerostruki prvak", c:"var(--red)",
   car:"Godinama je skupljao rijetke automobile, ali je 2019. prodao privatni avion i otad naglašava ekološki osvješteniji život.",
   hobby:"Glazba – producira vlastite pjesme i svira klavir i gitaru. Uz to moda i dizajn.",
   fact:"Jedan od rijetkih vozača s ozbiljnim glazbenim radom izvan staze, uz Leclerca.",
   src:"PlanetF1", u:"https://www.planetf1.com/news/charles-leclerc-music-release-hint"},
  {n:"Fernando Alonso", team:"F1, Aston Martin – dvostruki prvak", c:"var(--green)",
   car:"Većina njegove kolekcije – bolidi, kartovi i trofeji – izložena je javno, u muzeju u rodnoj Asturiji.",
   hobby:"Biciklizam. Vozi cestovni bicikl za kondiciju i veliki je ljubitelj tog sporta.",
   fact:"Muzej i karting staza u Llaneri kraj Ovieda imaju više od 300 predmeta, od kartinga s kojim je počeo s tri godine do F1 bolida. Stazu je pomogao dizajnirati sam.",
   src:"Wikipedia", u:"https://en.wikipedia.org/wiki/Fernando_Alonso_Sports_Complex"},
  {n:"Lando Norris", team:"F1, McLaren", c:"var(--yellow)",
   car:"Kao McLarenov vozač u javnosti se pojavljuje u McLarenovim cestovnim automobilima.",
   hobby:"Gaming i streaming. Iz toga je izrastao Quadrant, njegova marka za gaming i lifestyle.",
   fact:"Quadrant je jedan od najuspješnijih primjera da vozač gradi vlastiti brend izvan F1.",
   src:"The Paddock Journal", u:"https://thepaddockjournal.substack.com/p/charles-leclercs-side-quests-how"},
  {n:"Valentino Rossi", team:"Legenda MotoGP-a, vlasnik tima VR46", c:"var(--yellow)",
   car:"I dalje se utrkuje – obnovio je ugovor s BMW-om na tri godine za GT World Challenge Europe. WEC i prekooceanske utrke napustio je kako bi više vremena provodio s obitelji.",
   hobby:"Vožnja na svom ranču u Tavulliji, zemljanoj stazi među vinogradima i maslinama koju je sam osmislio.",
   fact:"Na ranču trenira VR46 Akademija – Bagnaia, Bezzecchi i Morbidelli redovito se ondje utrkuju s njim između utrka MotoGP-a.",
   src:"Moto.it", u:"https://www.moto.it/MotoGP/bagnaia-e-bezzecchi-al-ranch-di-valentino-rossi-allenamento-in-vista-del-gp-del-brasile.html"}
];


let NEWS=[], DRIVERS=[], newsFilter="all", routeFilter="all", shown=6;
const $=id=>document.getElementById(id);
function fmt(iso){const d=new Date(iso);return isNaN(d)?"":d.getDate()+". "+(d.getMonth()+1)+".";}
function el(tag,cls,txt){const e=document.createElement(tag);if(cls)e.className=cls;if(txt!=null)e.textContent=txt;return e;}
function cat(n){return CATS[n.c]||CAT_FALLBACK;}

function photo(n,withCredit){
  const c=cat(n), box=el("div","ph"); box.style.setProperty("--pc",c.color);
  const frag=document.createDocumentFragment(); frag.appendChild(box);
  if(n.img&&n.img.src){
    const im=new Image(); im.loading="lazy"; im.decoding="async"; im.alt=""; im.src=n.img.src;
    im.onerror=()=>{im.remove();box.classList.add("fallback");box.appendChild(el("span","fb",c.short));};
    box.appendChild(im);
    if(withCredit){
      const cr=el("div","credit"); cr.append("Foto: ");
      const a=el("a",null,n.img.by); a.href=n.img.link||n.img.src; a.target="_blank"; a.rel="noopener";
      cr.append(a, ", "+n.img.lic+" (ilustracija)"); frag.appendChild(cr);
    }
  } else { box.classList.add("fallback"); box.appendChild(el("span","fb",c.short)); }
  return frag;
}
function srcLine(n){const p=el("div","src");p.append("Izvor: ");const a=el("a",null,n.src);a.href=n.u;a.target="_blank";a.rel="noopener";p.append(a," · "+fmt(n.date));return p;}
function plate(n){const c=cat(n),p=el("span","plate",c.name);p.style.setProperty("--pc",c.color);return p;}

function renderHero(){
  const n=NEWS[0], lead=$("lead"); lead.innerHTML=""; if(!n){lead.append(el("div","txt","Vijesti se trenutno ne mogu učitati."));return;}
  const ph=photo(n,false); lead.append(ph);
  const t=el("div","txt"); t.append(plate(n));
  const h=el("h2"); const a=el("a",null,n.t); a.href=n.u; a.target="_blank"; a.rel="noopener"; h.append(a); t.append(h, el("p",null,n.s), srcLine(n));
  if(n.img){const cr=el("div","credit");cr.append("Foto: ");const ca=el("a",null,n.img.by);ca.href=n.img.link||n.img.src;ca.target="_blank";ca.rel="noopener";cr.append(ca,", "+n.img.lic+" (ilustracija)");t.append(cr);}
  lead.append(t);
  const side=$("side"); side.innerHTML="";
  // sekundarne vijesti: po jedna iz različitih kategorija
  const seen=new Set([n.c]), picks=[];
  for(const x of NEWS.slice(1)){ if(!seen.has(x.c)){seen.add(x.c);picks.push(x);} if(picks.length===3)break; }
  for(const x of picks){
    const a=el("a","mini-card"); a.href=x.u; a.target="_blank"; a.rel="noopener";
    a.append(photo(x,false)); const tt=el("div","t"); tt.append(plate(x), el("h3",null,x.t), el("div","src",x.src+" · "+fmt(x.date))); a.append(tt);
    side.append(a);
  }
  window._heroIds=new Set([n.u,...picks.map(p=>p.u)]);
}

function chip(label,val,cur,color){const b=el("button","chip");b.type="button";b.dataset.v=val;b.setAttribute("aria-pressed",String(val===cur));if(color){const s=el("span","dot");s.style.background=color;b.append(s);}b.append(label);return b;}
function renderNewsChips(){const box=$("newsChips");box.innerHTML="";box.append(chip("Sve","all",newsFilter));const present=new Set(NEWS.map(n=>n.c));for(const [k,v] of Object.entries(CATS)) if(present.has(k)) box.append(chip(v.name,k,newsFilter,v.color));}
function renderNews(){
  const list=$("newsList"); list.innerHTML="";
  const hero=window._heroIds||new Set();
  const items=NEWS.filter(n=>(newsFilter==="all"?!hero.has(n.u):n.c===newsFilter));
  if(!items.length){list.append(el("div","empty","Nema novosti u ovoj kategoriji."));$("moreWrap").hidden=true;return;}
  for(const n of items.slice(0,shown)){
    const card=el("article","card");
    const ph=photo(n,false); card.append(ph); card.querySelector(".ph").append(plate(n));
    const b=el("div","body");
    const h=el("h3"); const a=el("a",null,n.t); a.href=n.u; a.target="_blank"; a.rel="noopener"; h.append(a);
    b.append(el("div","dt",fmt(n.date)), h, el("p",null,n.s));
    if(n.body){const d=el("details");d.append(el("summary",null,"Pročitaj cijelu vijest"),el("div",null,n.body));b.append(d);}
    b.append(srcLine(n));
    if(n.img){const cr=el("div","credit");cr.append("Foto: ");const ca=el("a",null,n.img.by);ca.href=n.img.link||n.img.src;ca.target="_blank";ca.rel="noopener";cr.append(ca,", "+n.img.lic+" (ilustracija)");b.append(cr);}
    card.append(b); list.append(card);
  }
  $("moreWrap").hidden=items.length<=shown;
}
$("newsChips").addEventListener("click",e=>{const b=e.target.closest(".chip");if(!b)return;newsFilter=b.dataset.v;shown=6;renderNewsChips();renderNews();});
$("moreBtn").addEventListener("click",()=>{shown+=6;renderNews();});

/* ---------- race ---------- */
const SESS={FirstPractice:"1. trening",SecondPractice:"2. trening",ThirdPractice:"3. trening",SprintQualifying:"Sprint kvalifikacije",SprintShootout:"Sprint kvalifikacije",Sprint:"Sprint",Qualifying:"Kvalifikacije"};
function when(d,t){return new Date(d+"T"+(t||"12:00:00Z"));}
function renderRace(r,schedule){
  if(!r||!r.name) return;
  $("utrka").hidden=false;
  $("raceRound").textContent=`Formula 1 · ${r.round}. od ${r.rounds} utrka sezone ${r.season}`;
  $("raceName").textContent=r.name.replace("Grand Prix","GP");
  const start=when(r.date,r.time);
  $("raceWhere").textContent=`${r.circuit} · ${r.locality||""}${r.country?", "+r.country:""} · ${start.toLocaleString("hr-HR",{weekday:"long",day:"numeric",month:"long",hour:"2-digit",minute:"2-digit"})}`;
  const cnt=$("count");
  function tick(){const ms=start-Date.now();cnt.innerHTML="";if(ms<=0){cnt.append(el("div",null,"Utrka je u tijeku ili završena"));return;}
    const d=Math.floor(ms/864e5),h=Math.floor(ms/36e5)%24,m=Math.floor(ms/6e4)%60;
    for(const [v,l] of [[d,"dana"],[h,"sati"],[m,"minuta"]]){const b=el("div");b.append(el("b",null,String(v)),el("span",null,l));cnt.append(b);}}
  tick(); setInterval(tick,30000);
  // obris staze
  const tr=$("track"); tr.innerHTML="";
  if(r.track&&r.track.path){
    const ns="http://www.w3.org/2000/svg", svg=document.createElementNS(ns,"svg");
    svg.setAttribute("viewBox","0 0 1000 1000"); svg.setAttribute("role","img"); svg.setAttribute("aria-label","Obris staze "+r.circuit);
    for(const c of ["base","line","run"]){const p=document.createElementNS(ns,"path");p.setAttribute("d",r.track.path);p.setAttribute("class",c);svg.append(p);}
    const st=document.createElementNS(ns,"circle");st.setAttribute("cx",r.track.start[0]);st.setAttribute("cy",r.track.start[1]);st.setAttribute("r",18);st.setAttribute("fill","#fff");st.setAttribute("stroke","#F05A1A");st.setAttribute("stroke-width",8);svg.append(st);
    tr.append(svg);
    const run=svg.querySelector(".run"), L=run.getTotalLength();
    const seg=L*0.08; run.style.strokeDasharray=`${seg} ${L}`; run.style.strokeDashoffset="0";
    if(!matchMedia("(prefers-reduced-motion: reduce)").matches){
      run.animate([{strokeDashoffset:0},{strokeDashoffset:-L}],{duration:9000,iterations:Infinity,easing:"linear"});
    }
  }
  const f=$("trackFacts"); f.innerHTML="";
  const facts=[];
  if(r.track&&r.track.length_m) facts.push([(r.track.length_m/1000).toFixed(3).replace(".",",")+" km","duljina kruga"]);
  if(r.track&&r.track.firstgp) facts.push([String(r.track.firstgp),"prva VN Formule 1"]);
  if(r.track&&r.track.opened) facts.push([String(r.track.opened),"otvorena"]);
  if(r.track&&r.track.altitude!=null) facts.push([r.track.altitude+" m","nadmorska visina"]);
  for(const [b,s] of facts){const d=el("div");d.append(el("b",null,b),el("span",null,s));f.append(d);}
  // pobjednici
  const w=$("winners"); w.innerHTML="";
  if(!(r.winners||[]).length) w.append(el("li",null,"Nova staza – još nema pobjednika."));
  for(const x of r.winners||[]){const li=el("li");li.append(el("span","y",x.season),el("span","n",x.driver),el("span","tm",x.team+(x.grid?` · start ${x.grid}.`:"")));w.append(li);}
  // poredak
  const bars=$("bars"); bars.innerHTML="";
  const s=r.standings||[]; const max=s.length?s[0].points:1;
  if(r.standings_round) $("standTitle").textContent=`Poredak prvenstva nakon ${r.standings_round}. utrke`;
  for(const x of s){
    const row=el("div","brow"); row.title=`${x.driver} (${x.team}) – ${x.points} bodova, ${x.wins} pobjeda`;
    const trk=el("div","tr"), fill=el("div","f"); trk.append(fill);
    row.append(el("span","p",x.pos+"."), el("span","c",x.code||x.driver.split(" ").pop().slice(0,3).toUpperCase()), trk, el("span","pt",String(Math.round(x.points))));
    bars.append(row); requestAnimationFrame(()=>requestAnimationFrame(()=>{fill.style.width=(x.points/max*100)+"%";}));
  }
  // sesije
  const ss=$("sess"); ss.innerHTML="";
  const list=Object.entries(r.sessions||{}).map(([k,v])=>[SESS[k]||k,when(v.date,v.time)]);
  list.push(["Utrka",start]); list.sort((a,b)=>a[1]-b[1]);
  for(const [k,d] of list){const li=el("li");li.append(el("strong",null,k),el("span",null,d.toLocaleString("hr-HR",{weekday:"short",day:"numeric",month:"numeric",hour:"2-digit",minute:"2-digit"})));ss.append(li);}
  renderSchedule(schedule);
}
function renderSchedule(list){
  const ol=$("sched"); ol.innerHTML=""; const today=new Date().toISOString().slice(0,10);
  for(const e of (list||[]).filter(e=>e.date>=today).slice(0,6)){
    const li=el("li"); const w=el("span","w",e.title); w.append(el("small",null,e.note||""));
    li.append(el("span","d",fmt(e.date)), w); ol.append(li);
  }
}

/* ---------- people & routes ---------- */
function renderDriverNews(){
  const box=$("driverNews"); box.innerHTML="";
  const items=DRIVERS.slice(0,4); $("driverNewsWrap").hidden=!items.length;
  for(const n of items){
    const card=el("article","card");
    card.append(photo(n,false));
    const b=el("div","body"); const h=el("h3"); const a=el("a",null,n.t); a.href=n.u; a.target="_blank"; a.rel="noopener"; h.append(a);
    b.append(el("div","dt",fmt(n.date)),h,el("p",null,n.s),srcLine(n));
    if(n.img){const cr=el("div","credit");cr.append("Foto: ");const ca=el("a",null,n.img.by);ca.href=n.img.link||n.img.src;ca.target="_blank";ca.rel="noopener";cr.append(ca,", "+n.img.lic+" (ilustracija)");b.append(cr);}
    card.append(b); box.append(card);
  }
}
function renderPeople(){const list=$("peopleList");list.innerHTML="";for(const p of PEOPLE){const e=el("article","person");e.style.setProperty("--pc",p.c);
  e.innerHTML=`<span class="ini" aria-hidden="true"></span><h3></h3><p class="team"></p><dl><div><dt>Što vozi privatno</dt><dd class="a"></dd></div><div><dt>Hobiji</dt><dd class="b"></dd></div><div><dt>Zanimljivost</dt><dd class="f"></dd></div></dl><span class="src">Izvor: <a target="_blank" rel="noopener"></a></span>`;
  e.querySelector(".ini").textContent=p.n.split(" ").map(w=>w[0]).join("");e.querySelector("h3").textContent=p.n;e.querySelector(".team").textContent=p.team;
  e.querySelector(".a").textContent=p.car;e.querySelector(".b").textContent=p.hobby;e.querySelector(".f").textContent=p.fact;const a=e.querySelector("a");a.href=p.u;a.textContent=p.src;list.append(e);}}
function renderRouteChips(){const box=$("routeChips");box.innerHTML="";box.append(chip("Sve","all",routeFilter));for(const [k,v] of Object.entries(REGIONS)) box.append(chip(v,k,routeFilter));}
function renderRoutes(){const list=$("routeList");list.innerHTML="";for(const r of ROUTES.filter(x=>routeFilter==="all"||x.r===routeFilter)){const e=el("article","route");
  e.innerHTML=`<header><h3></h3><span class="km">oko ${r.km} km</span></header><div><ol class="line"></ol><p class="desc"></p>${r.warn?'<span class="warn"></span>':''}</div><div><ul class="rfacts"><li><span>Regija</span>${REGIONS[r.r]}</li><li><span>Karakter</span>${r.tip}</li><li><span>Sezona</span>${r.season}</li><li><span>Zahtjevnost</span>${r.diff}</li></ul><a class="go" target="_blank" rel="noopener">Otvori u Google kartama</a></div>`;
  e.querySelector("h3").textContent=r.n;const ol=e.querySelector(".line");for(const p of r.pts) ol.append(el("li",null,p));e.querySelector(".desc").textContent=r.desc;if(r.warn)e.querySelector(".warn").textContent=r.warn;e.querySelector(".go").href=gm(r.pts);list.append(e);}}
$("routeChips").addEventListener("click",e=>{const b=e.target.closest(".chip");if(!b)return;routeFilter=b.dataset.v;renderRouteChips();renderRoutes();});

/* ---------- stats ---------- */
function hr(n){return String(n).replace(".",",");}
function renderStats(){
  document.querySelectorAll(".sbars").forEach(box=>{
    const data=JSON.parse(box.dataset.bars), max=Math.max(...data.map(d=>d[1])), hl=box.dataset.hl, u=box.dataset.unit||"";
    for(const [l,v] of data){const r=el("div","sbar"+(l===hl?" hl":""));const t=el("div","t"),f=el("div","f");f.dataset.w=(v/max*100);t.append(f);r.append(el("span","l",l),t,el("span","v",hr(v)+" "+u));box.append(r);}
  });
  document.querySelectorAll(".stack").forEach(box=>{
    const data=JSON.parse(box.dataset.stack); const line=el("div","barline"); line.setAttribute("role","img");
    line.setAttribute("aria-label",data.map(d=>d[0]+" "+hr(d[1])+" %").join(", "));
    const leg=el("ul","leg");
    for(const [l,v,c] of data){const sg=el("div","seg");sg.style.background=c;sg.dataset.w=v;sg.title=l+": "+hr(v)+" %";line.append(sg);
      const li=el("li");const i=el("i");i.style.background=c;li.append(i,l,el("b",null,hr(v)+" %"));leg.append(li);}
    box.append(line,leg);
  });
  const grow=root=>root.querySelectorAll("[data-w]").forEach(x=>x.style.width=x.dataset.w+"%");
  const so=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){grow(e.target);so.unobserve(e.target);}}),{threshold:.3});
  document.querySelectorAll(".stat").forEach(x=>so.observe(x));
}
renderStats();

/* ---------- load ---------- */
async function getJSON(f){const r=await fetch(f+"?v="+Date.now(),{cache:"no-store"});if(!r.ok)throw new Error(r.status);return r.json();}
async function load(){
  let sched=[];
  try{const d=await getJSON("news.json");const all=d.items||[];DRIVERS=all.filter(n=>n.c==="kaciga");NEWS=all.filter(n=>n.c!=="kaciga");sched=d.schedule||[];
    const u=new Date(d.updated);if(!isNaN(u))$("updated").textContent="Vijesti osvježene "+u.toLocaleString("hr-HR",{day:"numeric",month:"numeric",hour:"2-digit",minute:"2-digit"});
  }catch(e){}
  renderHero();renderNewsChips();renderNews();renderDriverNews();
  try{renderRace(await getJSON("race.json"),sched);}catch(e){}
}
renderPeople();renderRouteChips();renderRoutes();load();

/* ---------- gear shifter ---------- */
const knob=$("knob"),gname=$("gearname"),gears=[...document.querySelectorAll(".gate button")];
function setGear(id){const b=gears.find(g=>g.dataset.t===id);if(!b)return;knob.style.left=b.style.left;knob.style.top=b.style.top;gears.forEach(g=>g.setAttribute("aria-current",String(g===b)));gname.textContent=b.dataset.n;
  document.querySelectorAll(".nav a").forEach(a=>a.setAttribute("aria-current",String(a.getAttribute("href")==="#"+id)));}
gears.forEach(b=>b.addEventListener("click",()=>{const t=$(b.dataset.t);setGear(b.dataset.t);if(t&&!t.hidden)t.scrollIntoView();}));
const io=new IntersectionObserver(es=>{for(const e of es) if(e.isIntersecting) setGear(e.target.id);},{rootMargin:"-45% 0px -50% 0px"});
["vrh","novosti","utrka","brojke","vozaci","rute"].forEach(id=>{const x=$(id);if(x)io.observe(x);});
const NAVMAP={"sve-vijesti":"novosti"};
</script>
</body>
</html>

feeds.json
{
  "feeds": [
    {
      "url": "https://www.motorsport.com/rss/f1/news/",
      "cat": "f1",
      "source": "Motorsport.com"
    },
    {
      "url": "https://www.autosport.com/rss/f1/news/",
      "cat": "f1",
      "source": "Autosport"
    },
    {
      "url": "https://www.motorsport.com/rss/motogp/news/",
      "cat": "motogp",
      "source": "Motorsport.com"
    },
    {
      "url": "https://www.motorsport.com/rss/wrc/news/",
      "cat": "reli",
      "source": "Motorsport.com"
    },
    {
      "url": "https://www.motor1.com/rss/news/all/",
      "cat": "auto",
      "source": "Motor1"
    },
    {
      "url": "https://www.rideapart.com/rss/news/all/",
      "cat": "moto",
      "source": "RideApart"
    },
    {
      "url": "https://feeds.arstechnica.com/arstechnica/index",
      "cat": "tech",
      "source": "Ars Technica"
    },
    {
      "url": "https://electrek.co/feed/",
      "cat": "energy",
      "source": "Electrek"
    },
    {
      "url": "https://www.carbonbrief.org/feed/",
      "cat": "energy",
      "source": "Carbon Brief"
    },
    {
      "url": "https://cleantechnica.com/feed/",
      "cat": "energy",
      "source": "CleanTechnica"
    },
    {
      "url": "https://news.google.com/rss/search?q=%28Verstappen%20OR%20Hamilton%20OR%20Leclerc%20OR%20Norris%20OR%20Alonso%20OR%20Antonelli%20OR%20Piastri%20OR%20%22Marc%20Marquez%22%20OR%20%22Valentino%20Rossi%22%29%20%28hobby%20OR%20golf%20OR%20music%20OR%20Instagram%20OR%20%22car%20collection%22%20OR%20charity%20OR%20%22off%20track%22%20OR%20fashion%20OR%20%22social%20media%22%29&hl=en-US&gl=US&ceid=US:en",
      "cat": "kaciga",
      "source": "Google News",
      "use_item_source": true
    }
  ],
  "max_age_days": 7,
  "max_per_category": 4,
  "events": [
    {
      "date": "2026-11-01",
      "title": "MotoGP – VN Malezije",
      "note": "Sepang"
    },
    {
      "date": "2026-11-08",
      "title": "MotoGP – VN Katara",
      "note": "Lusail"
    },
    {
      "date": "2027-04-08",
      "title": "WRC – Croatia Rally",
      "note": "8. – 11. travnja"
    }
  ]
}
scripts/update_news.py
"""Okretaji – automatsko osvježavanje vijesti.

Čita RSS izvore, dohvaća tekst članka kad je dostupan i uz Gemini izrađuje
hrvatski naslov, sažetak i originalno formuliranu vijest od 150–300 riječi.
Izvorni tekst koristi se samo kao kontekst; na portal se sprema AI-urednički tekst i poveznica na izvor.
"""
import html, json, os, re, sys, time, unicodedata
from datetime import datetime, timedelta, timezone

import feedparser
import requests
import trafilatura

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FEEDS = os.path.join(ROOT, "feeds.json")
OUT = os.path.join(ROOT, "news.json")
UA = "Mozilla/5.0 (Okretaji news bot; +https://github.com)"
NOW = datetime.now(timezone.utc)


def clean(text, limit=260):
    text = html.unescape(re.sub(r"<[^>]+>", " ", text or ""))
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > limit:
        text = text[:limit].rsplit(" ", 1)[0] + "…"
    return text


def norm(title):
    # Normalizacija dijakritike pomaže ukloniti duplikate među izvorima.
    title = unicodedata.normalize("NFKD", title.lower())
    title = "".join(ch for ch in title if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]", "", title)[:80]


def load_old():
    try:
        with open(OUT, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"items": []}


def extract_rss_text(entry):
    """Uzima najdulji tekst koji RSS već isporučuje; bez dodatnog HTTP poziva."""
    chunks = []
    for part in entry.get("content", []) or []:
        value = clean(part.get("value", ""), 12000)
        if value:
            chunks.append(value)
    summary = clean(entry.get("summary") or entry.get("description"), 12000)
    if summary:
        chunks.append(summary)
    return max(chunks, key=len, default="")[:10000]


def extract_page_text(link, current_text=""):
    """Dohvaća stranicu samo za članke koji se stvarno šalju na AI obradu."""
    text = current_text or ""
    if len(text) >= 900:
        return text[:10000]
    try:
        response = requests.get(link, headers={"User-Agent": UA}, timeout=18)
        response.raise_for_status()
        extracted = trafilatura.extract(
            response.text, include_comments=False, include_tables=False,
            favor_precision=True, deduplicate=True
        )
        if extracted and len(extracted) > len(text):
            text = extracted
    except Exception as exc:
        print(f"  ! tekst članka nije dohvaćen ({link}): {exc}", file=sys.stderr)
    return clean(text, 10000)


def word_count(text):
    return len(re.findall(r"\b[\wÀ-ž]+(?:[’'-][\wÀ-ž]+)*\b", text or ""))


def fetch_feed(feed, max_age):
    items = []
    try:
        r = requests.get(feed["url"], headers={"User-Agent": UA}, timeout=20)
        r.raise_for_status()
        parsed = feedparser.parse(r.content)
    except Exception as e:
        print(f"  ! {feed['url']}: {e}", file=sys.stderr)
        return items
    for e in parsed.entries[:20]:
        t = e.get("published_parsed") or e.get("updated_parsed")
        when = datetime.fromtimestamp(time.mktime(t), timezone.utc) if t else NOW
        if NOW - when > timedelta(days=max_age) or when > NOW + timedelta(days=1):
            continue
        title = clean(e.get("title"), 200)
        link = e.get("link")
        if not title or not link:
            continue
        items.append({
            "c": feed["cat"], "t": title, "s": clean(e.get("summary") or e.get("description")),
            "src": ((e.get("source") or {}).get("title") if feed.get("use_item_source") else None) or feed["source"], "u": link, "date": when.isoformat(timespec="minutes"),
            "orig_t": title,
            "_source_text": extract_rss_text(e),
        })
    print(f"  {feed['source']} ({feed['cat']}): {len(items)}")
    return items


def call_gemini(prompt):
    """Gemini API; koristi se besplatna kvota ako je dostupna za projekt/model."""
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY nije postavljen")
    model = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash-lite")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    r = requests.post(
        url,
        headers={"x-goog-api-key": key, "content-type": "application/json"},
        json={
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.2, "maxOutputTokens": 6500,
                             "responseMimeType": "application/json"},
        },
        timeout=120,
    )
    r.raise_for_status()
    data = r.json()
    return "".join(part.get("text", "") for part in data["candidates"][0]["content"]["parts"])


def call_claude(prompt):
    """Plaćena rezervna opcija; radi samo ako je izričito omogućena."""
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise RuntimeError("ANTHROPIC_API_KEY nije postavljen za rezervnu opciju")
    r = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"},
        json={"model": os.environ.get("CLAUDE_MODEL", "claude-haiku-4-5"), "max_tokens": 6500,
              "messages": [{"role": "user", "content": prompt}]},
        timeout=120,
    )
    r.raise_for_status()
    return "".join(b.get("text", "") for b in r.json()["content"])


def translate(items, old_by_link):
    """Gemini prvo; Claude se može uključiti kao rezervna opcija uz izričitu postavku."""
    key = os.environ.get("GEMINI_API_KEY")
    todo = []
    for it in items:
        old = old_by_link.get(it["u"])
        if old and old.get("hr") and old.get("orig_t") == it["orig_t"] and (old.get("body") or old.get("nb")):
            it["t"], it["s"], it["hr"] = old["t"], old["s"], True
            if old.get("body"):
                it["body"] = old["body"]
            else:
                it["nb"] = True
            if old.get("img_q"):
                it["img_q"] = old["img_q"]
        else:
            # Zadrži stari prijevod sažetka, ali pokušaj nadograditi ga člankom ako ga nema.
            if old and old.get("hr") and old.get("orig_t") == it["orig_t"]:
                it["t"], it["s"] = old["t"], old["s"]
            todo.append(it)
    if not key or not todo:
        if not key:
            print("  ! GEMINI_API_KEY nije postavljen; nove vijesti ostaju bez AI prijevoda.")
        return
    # Ograničenja čuvaju trošak i sprječavaju da jedan workflow postane predug.
    if len(todo) > 12:
        print(f"  ! Za kontrolu troška prevodim 12 od {len(todo)} novih članaka u ovom pokretanju.")
        todo = todo[:12]
    # Manji batchovi smanjuju rizik od neispravnog JSON-a kod dugih članaka.
    for i in range(0, len(todo), 3):
        batch = todo[i:i + 3]
        payload = []
        for n, it in enumerate(batch):
            source_text = extract_page_text(it["u"], it.get("_source_text") or it.get("s"))
            payload.append({"id": n, "title": it["orig_t"], "rss_summary": it.get("s", ""), "source_text": source_text})
        prompt = (
            "Ti si hrvatski urednik regionalnog auto-moto, tehnologija i energetika portala Okretaji. "
            "Za svaku stavku napiši: t (precizan, prirodan hrvatski naslov), s (sažetak od 1–2 rečenice, do 45 riječi) "
            "i body (originalno formulirana kratka vijest od 150 do 300 riječi na hrvatskom jeziku). "
            "Koristi samo činjenice koje izričito podupire dostavljeni naslov, RSS sažetak i tekst izvora. "
            "Ne dodaj pozadinske tvrdnje, datume, brojke, citate ili zaključke koji nisu u izvoru. "
            "Ako izvor nema dovoljno podataka za vjerodostojan tekst od najmanje 150 riječi, vrati body kao prazan niz; "
            "nemoj umjetno produžavati tekst. Parafraziraj, ne prevodi rečenicu po rečenicu. "
            "Sačuvaj točne nazive vozača, timova, modela, tvrtki, jedinice i brojke. "
            "Ne izmišljaj citate. Bez senzacionalizma. Vrati SAMO JSON listu objekata "
            "{\"id\":0,\"t\":\"...\",\"s\":\"...\",\"body\":\"...\",\"q\":\"...\"}. "
            "Polje q je kratak ENGLESKI upit za pretragu ilustrativne fotografije (2–4 riječi, npr. ime vozača, tima, "
            "modela automobila ili motocikla, ili općeniti pojam poput 'rally car forest'). "
            "Ne uključuj URL-ove ni bibliografiju u body; izvorna poveznica prikazuje se zasebno.\n\n"
            + json.dumps(payload, ensure_ascii=False)
        )
        try:
            try:
                text = call_gemini(prompt)
                provider = "Gemini"
            except Exception as gemini_error:
                # Nikada ne pokreći plaćeni Claude fallback bez eksplicitne dozvole.
                if os.environ.get("ENABLE_CLAUDE_FALLBACK", "false").lower() == "true" and os.environ.get("ANTHROPIC_API_KEY"):
                    print(f"  ! Gemini nije uspio ({gemini_error}); pokušavam izričito omogućeni Claude fallback.", file=sys.stderr)
                    text = call_claude(prompt)
                    provider = "Claude fallback"
                else:
                    raise gemini_error
            text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip()).strip()
            rows = json.loads(text)
            print(f"  AI obrada uspješna: {provider}")
            for row in rows:
                idx = int(row["id"])
                if idx < 0 or idx >= len(batch):
                    continue
                it = batch[idx]
                title = clean(row.get("t", ""), 180)
                it["img_q"] = clean(row.get("q", ""), 60)
                summary = clean(row.get("s", ""), 400)
                body = (row.get("body") or "").strip()
                wc = word_count(body)
                if title and summary:
                    it["t"], it["s"], it["hr"] = title, summary, True
                if 150 <= wc <= 300:
                    it["body"] = body
                    it["body_words"] = wc
                else:
                    it.pop("body", None)
                    it["nb"] = True
                    it.pop("body_words", None)
                    print(f"  ! {it['src']}: nema dovoljno provjerljivih podataka za članak 150–300 riječi (dobiveno {wc}); prikazat će se samo sažetak.")
        except Exception as e:
            print(f"  ! AI obrada nije uspjela: {e}", file=sys.stderr)
    # Interni tekst izvora ne smije završiti u javnom news.json.
    for it in items:
        it.pop("_source_text", None)


def f1_schedule():
    try:
        r = requests.get("https://api.jolpi.ca/ergast/f1/current/races/?format=json",
                         headers={"User-Agent": UA}, timeout=20)
        r.raise_for_status()
        races = r.json()["MRData"]["RaceTable"]["Races"]
    except Exception as e:
        print(f"  ! F1 kalendar: {e}", file=sys.stderr)
        return []
    out = []
    for race in races:
        loc = race.get("Circuit", {}).get("Location", {})
        out.append({"date": race["date"], "title": "F1 – " + race["raceName"].replace("Grand Prix", "GP"),
                    "note": ", ".join(x for x in [loc.get("locality"), loc.get("country")] if x)})
    return out


def main():
    cfg = json.load(open(FEEDS, encoding="utf-8"))
    old = load_old()
    old_by_link = {it["u"]: it for it in old.get("items", [])}

    items, seen = [], set()
    for feed in cfg["feeds"]:
        for it in fetch_feed(feed, cfg.get("max_age_days", 10)):
            k = norm(it["t"])
            if it["u"] in seen or k in seen:
                continue
            seen.update([it["u"], k])
            items.append(it)

    if not items:
        print("Nijedan izvor nije vratio vijesti – news.json ostaje nepromijenjen.")
        return

    items.sort(key=lambda x: x["date"], reverse=True)
    per_cat, kept = {}, []
    for it in items:
        per_cat[it["c"]] = per_cat.get(it["c"], 0) + 1
        if per_cat[it["c"]] <= cfg.get("max_per_category", 9):
            kept.append(it)

    # glavna vijest: najnovija iz F1 ili MotoGP-a
    lead = next((it for it in kept if it["c"] in ("f1", "motogp")), kept[0])
    kept.remove(lead)
    kept.insert(0, lead)

    translate(kept, old_by_link)
    for it in kept:
        it.pop("_source_text", None)

    today = NOW.date().isoformat()
    events = [e for e in f1_schedule() + cfg.get("events", []) if e["date"] >= today]
    events.sort(key=lambda e: e["date"])

    data = {"updated": NOW.isoformat(timespec="minutes"), "items": kept, "schedule": events[:6]}
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print(f"Zapisano {len(kept)} vijesti i {len(events[:6])} događaja.")


if __name__ == "__main__":
    main()

scripts/add_images.py
"""Dodaje ilustrativne fotografije vijestima u news.json.

Fotografije se traže na Openverseu (openverse.org) – samo slike pod
Creative Commons licencama, uz autora i licencu koje stranica prikazuje.
Pronađene slike pamte se u images.json pa se ista vijest ne pretražuje ponovno.
"""
import json, os, re, sys, time
import requests

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NEWS = os.path.join(ROOT, "news.json")
CACHE = os.path.join(ROOT, "images.json")
UA = "Okretaji/1.0 (https://okretaji.com)"
API = "https://api.openverse.org/v1/images/"

FALLBACK_Q = {
    "f1": "formula one car", "motogp": "motogp motorcycle racing", "auto": "sports car",
    "moto": "motorcycle road", "reli": "rally car", "tech": "technology circuit board",
    "energy": "wind turbines solar",
    "kaciga": "racing driver portrait",
}


def load(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def search(q, used):
    params = {"q": q, "page_size": 12, "mature": "false",
              "license_type": "all-cc", "aspect_ratio": "wide", "size": "large"}
    r = requests.get(API, params=params, headers={"User-Agent": UA}, timeout=20)
    r.raise_for_status()
    for res in r.json().get("results", []):
        if res.get("id") in used or not res.get("thumbnail"):
            continue
        lic = (res.get("license") or "").upper()
        ver = res.get("license_version") or ""
        lic = "CC0" if lic == "CC0" else ("Javno vlasništvo" if lic == "PDM" else f"CC {lic} {ver}".strip())
        return {
            "id": res["id"],
            "src": res["thumbnail"],
            "by": (res.get("creator") or "nepoznat autor")[:60],
            "lic": lic,
            "link": res.get("foreign_landing_url") or res.get("url"),
        }
    return None


def main():
    data = load(NEWS, None)
    if not data:
        print("news.json ne postoji"); return
    cache = load(CACHE, {})
    used = {v["id"] for v in cache.values() if v}
    found = calls = 0
    for it in data.get("items", []):
        key = it["u"].split("?")[0]
        if key in cache:
            if cache[key]:
                it["img"] = cache[key]
            continue
        if calls >= 25:      # pristojno prema besplatnom API-ju
            continue
        queries = [q for q in [it.get("img_q"), FALLBACK_Q.get(it["c"])] if q]
        img, failed = None, False
        for q in queries:
            try:
                calls += 1
                img = search(q, used)
                time.sleep(1.2)
            except Exception as e:
                print(f"  ! Openverse ({q}): {e}", file=sys.stderr)
                failed = True
                break
            if img:
                break
        if failed:           # greška API-ja: pokušaj ponovno u sljedećem pokretanju
            continue
        cache[key] = img
        if img:
            used.add(img["id"]); it["img"] = img; found += 1
    # stari unosi koji više nisu u vijestima brišu se iz predmemorije
    live = {it["u"].split("?")[0] for it in data.get("items", [])}
    cache = {k: v for k, v in cache.items() if k in live}
    with open(CACHE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=1)
    with open(NEWS, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print(f"Fotografije: {found} novih, {calls} upita.")


if __name__ == "__main__":
    main()

