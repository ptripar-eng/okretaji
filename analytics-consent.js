/* Okretaji.com — jedinstvena analitika uz prethodnu privolu (HR/EN/DE).
   Svi HTML dokumenti pozivaju ovu skriptu s /analytics-consent.js.
   Google Analytics se NE ucitava prije izricitog prihvacanja. */
(function () {
  'use strict';
  if (window.__okretajiConsentInitialized) return;
  window.__okretajiConsentInitialized = true;

  var KEY = 'okretaji_analytics_consent';
  var GA_ID = 'G-426646FTQH';
  var lang = (document.documentElement.lang || 'hr').slice(0, 2);
  var copy = {
    hr: {
      title: 'Analitika posjeta',
      body: 'Uz tvoju privolu koristimo Google Analytics kako bismo razumjeli čitanost članaka. Analitika se neće učitati ako odbiješ.',
      privacy: 'Informacije o privatnosti',
      accept: 'Prihvaćam analitiku',
      decline: 'Odbijam',
      settings: 'Promijeni postavke analitike',
      privacyUrl: '/privatnost.html'
    },
    en: {
      title: 'Website analytics',
      body: 'With your consent, we use Google Analytics to understand which stories are read. No analytics will load if you decline.',
      privacy: 'Privacy information',
      accept: 'Accept analytics',
      decline: 'Decline',
      settings: 'Change analytics preferences',
      privacyUrl: '/en/privatnost.html'
    },
    de: {
      title: 'Website-Analyse',
      body: 'Mit deiner Einwilligung nutzen wir Google Analytics, um zu verstehen, welche Artikel gelesen werden. Ohne Zustimmung wird keine Analyse geladen.',
      privacy: 'Datenschutzhinweise',
      accept: 'Analyse akzeptieren',
      decline: 'Ablehnen',
      settings: 'Analyse-Einstellungen ändern',
      privacyUrl: '/de/privatnost.html'
    }
  }[lang] || null;
  if (!copy) copy = {
    title: 'Analitika posjeta', body: 'Google Analytics upotrebljavamo samo uz tvoju privolu.',
    privacy: 'Privatnost', accept: 'Prihvaćam analitiku', decline: 'Odbijam',
    settings: 'Postavke analitike', privacyUrl: '/privatnost.html'
  };

  function readChoice() {
    try { return localStorage.getItem(KEY); } catch (e) { return null; }
  }
  function saveChoice(value) {
    try { localStorage.setItem(KEY, value); } catch (e) { /* Storage may be blocked. */ }
  }
  function loadAnalytics() {
    if (window.__okretajiAnalyticsLoaded) return;
    window.__okretajiAnalyticsLoaded = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', GA_ID, { anonymize_ip: true });
    var script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(GA_ID);
    document.head.appendChild(script);
  }

  var css = document.createElement('style');
  css.textContent = '#okretaji-consent{position:fixed;z-index:9999;left:16px;right:16px;bottom:16px;max-width:760px;margin:auto;padding:18px;background:#fff;color:#0D2B3E;border:1px solid #D3E2EA;border-radius:14px;box-shadow:0 8px 32px rgba(0,0,0,.22);font:16px/1.5 system-ui,sans-serif}' +
    '#okretaji-consent[hidden]{display:none}' +
    '#okretaji-consent p{margin:0 0 12px}' +
    '#okretaji-consent a{color:#1C5A86}' +
    '#okretaji-consent .actions{display:flex;gap:10px;flex-wrap:wrap}' +
    '#okretaji-consent button{padding:10px 14px;border-radius:8px;border:1px solid #0D2B3E;font-weight:700;cursor:pointer}' +
    '#okretaji-consent button.accept{background:#0D2B3E;color:#fff}' +
    '#okretaji-consent button.decline{background:#fff;color:#0D2B3E}' +
    '#okretaji-consent-manage{margin:8px 0;padding:8px 12px;cursor:pointer}';
  document.head.appendChild(css);

  var dialog = document.createElement('section');
  dialog.id = 'okretaji-consent';
  dialog.setAttribute('role', 'dialog');
  dialog.setAttribute('aria-label', copy.title);
  dialog.hidden = true;

  var intro = document.createElement('p');
  var title = document.createElement('strong');
  title.textContent = copy.title;
  intro.appendChild(title);
  intro.appendChild(document.createElement('br'));
  intro.appendChild(document.createTextNode(copy.body));

  var linkParagraph = document.createElement('p');
  var link = document.createElement('a');
  link.href = copy.privacyUrl;
  link.textContent = copy.privacy;
  linkParagraph.appendChild(link);

  var actions = document.createElement('div');
  actions.className = 'actions';
  var yes = document.createElement('button');
  yes.type = 'button'; yes.className = 'accept'; yes.textContent = copy.accept;
  var no = document.createElement('button');
  no.type = 'button'; no.className = 'decline'; no.textContent = copy.decline;
  actions.appendChild(yes);
  actions.appendChild(no);
  dialog.appendChild(intro);
  dialog.appendChild(linkParagraph);
  dialog.appendChild(actions);
  document.body.appendChild(dialog);

  yes.addEventListener('click', function () {
    saveChoice('granted');
    dialog.hidden = true;
    loadAnalytics();
  });
  no.addEventListener('click', function () {
    var wasGranted = readChoice() === 'granted';
    saveChoice('denied');
    dialog.hidden = true;
    // Once GA is loaded it cannot be unloaded; refresh to stop further tracking.
    if (wasGranted && window.__okretajiAnalyticsLoaded) location.reload();
  });

  if (/\/privatnost\.html$/.test(location.pathname)) {
    var manage = document.createElement('button');
    manage.type = 'button';
    manage.id = 'okretaji-consent-manage';
    manage.textContent = copy.settings;
    manage.addEventListener('click', function () {
      dialog.hidden = false;
      yes.focus();
    });
    var heading = document.querySelector('h2');
    if (heading) heading.parentNode.insertBefore(manage, heading.nextSibling);
    else document.body.appendChild(manage);
  }

  var saved = readChoice();
  if (saved === 'granted') loadAnalytics();
  else if (saved !== 'denied') dialog.hidden = false;
})();
