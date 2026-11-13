// Deputable AI - shared site behaviour (no framework, no build step)

document.addEventListener('DOMContentLoaded', () => {
  initMobileNav();
  initDemos();
  initConsent();
});

/* ---------------- Mobile nav toggle ---------------- */
function initMobileNav() {
  const toggle = document.querySelector('.mobile-toggle');
  const nav = document.querySelector('nav.main-nav');
  if (!toggle || !nav) return;
  toggle.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    toggle.textContent = open ? 'Close' : 'Menu';
  });
}

/* ---------------- Demos: tabs, and the hero's run ----------------
   A demo is a set of tabs over panels that all sit in one grid cell
   (so nothing below moves when they change). Every panel's content is
   written into the page by scripts/generate_site.py, so the page reads
   in full without this script; here we only switch panels and, for the
   hero's run demo (data-demo="auto"), light a workflow's steps one after
   another and then let the messages arrive on the phone.

   Autoplay runs only while the demo is on screen, moves on to the next
   workflow by itself until the visitor picks a tab, and never runs
   under prefers-reduced-motion (everything is simply there). */
function initDemos() {
  document.querySelectorAll('[data-demo]').forEach(initDemo);
}

function initDemo(root) {
  const tabs = Array.from(root.querySelectorAll('[data-demo-tab]'));
  const panels = Array.from(root.querySelectorAll('[data-demo-panel]'));
  const nameEl = root.querySelector('[data-demo-name]');
  const viaEl = root.querySelector('[data-demo-via]');
  if (!tabs.length || tabs.length !== panels.length) return;

  const autoplay = root.dataset.demo === 'auto';
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const FIRST_MS = 350;       // before the first step
  const STEP_MS = 950;        // between a workflow's steps
  const PERSON_MS = 1500;     // the step that waits for a person
  const MSG_MS = 1400;        // between the messages on the phone
  const HOLD_MS = 5200;       // the finished run, before moving on

  let current = 0;
  let timers = [];
  let inView = false;
  let auto = autoplay;        // false once the visitor picks a tab
  let playing = false;

  const revealables = (panel) => Array.from(panel.querySelectorAll('[data-rv]'));

  function clearTimers() {
    timers.forEach(clearTimeout);
    timers = [];
    playing = false;
  }

  function settle(panel) {
    // show everything, with no animation pending
    panel.classList.remove('is-armed');
    revealables(panel).forEach(el => el.classList.remove('is-in'));
  }

  function select(i) {
    current = i;
    tabs.forEach((t, j) => {
      t.setAttribute('aria-selected', j === i ? 'true' : 'false');
      t.tabIndex = j === i ? 0 : -1;
    });
    panels.forEach((p, j) => {
      p.classList.toggle('is-active', j === i);
      settle(p);
    });
    if (nameEl && panels[i].dataset.name) nameEl.textContent = panels[i].dataset.name;
    if (viaEl && panels[i].dataset.via) viaEl.textContent = panels[i].dataset.via;
  }

  function play(i) {
    clearTimers();
    select(i);
    if (!autoplay || reduceMotion.matches || !inView) return;

    const panel = panels[i];
    panel.classList.add('is-armed');
    playing = true;

    let at = FIRST_MS;
    revealables(panel).forEach((el) => {
      timers.push(setTimeout(() => el.classList.add('is-in'), at));
      if (el.classList.contains('msg')) at += MSG_MS;
      else at += el.classList.contains('person') ? PERSON_MS : STEP_MS;
    });
    timers.push(setTimeout(() => {
      playing = false;
      if (auto && inView) play((i + 1) % panels.length);
    }, at + HOLD_MS));
  }

  tabs.forEach((tab, i) => {
    tab.addEventListener('click', () => { auto = false; play(i); });
    tab.addEventListener('keydown', (evt) => {
      if (evt.key !== 'ArrowRight' && evt.key !== 'ArrowLeft') return;
      evt.preventDefault();
      const next = (i + (evt.key === 'ArrowRight' ? 1 : tabs.length - 1)) % tabs.length;
      auto = false;
      play(next);
      tabs[next].focus();
    });
  });

  select(0);
  if (!autoplay) return;

  // Start at once if the demo is already on screen at load, rather than
  // waiting for the observer's first report (which follows a rendered
  // frame and can lag in a background or embedded tab).
  const box = root.getBoundingClientRect();
  const seen = Math.min(box.bottom, window.innerHeight) - Math.max(box.top, 0);
  if (box.height > 0 && seen / box.height >= 0.25) {
    inView = true;
    play(0);
  }

  const observer = new IntersectionObserver((entries) => {
    inView = entries[0].isIntersecting;
    if (inView) {
      if (!playing) play(current);
    } else {
      // off screen: stop the clock and leave the whole run readable
      clearTimers();
      settle(panels[current]);
    }
  }, { threshold: 0.25 });
  observer.observe(root);

  reduceMotion.addEventListener('change', () => {
    clearTimers();
    settle(panels[current]);
    if (!reduceMotion.matches && inView) play(current);
  });
}

/* ---------------- Analytics consent (only rendered when GA is set) ---- */
function initConsent() {
  const bar = document.querySelector('[data-consent-bar]');
  if (!bar) return;
  const KEY = 'deputable-consent';

  let stored = null;
  try { stored = localStorage.getItem(KEY); } catch (e) { /* blocked storage */ }

  function grant() {
    if (typeof gtag === 'function') {
      gtag('consent', 'update', { analytics_storage: 'granted' });
    }
  }

  if (stored === 'granted') { grant(); return; }
  if (stored === 'denied') return;

  bar.classList.remove('hidden');
  bar.querySelector('[data-consent-accept]').addEventListener('click', () => {
    try { localStorage.setItem(KEY, 'granted'); } catch (e) {}
    grant();
    bar.classList.add('hidden');
  });
  bar.querySelector('[data-consent-decline]').addEventListener('click', () => {
    try { localStorage.setItem(KEY, 'denied'); } catch (e) {}
    bar.classList.add('hidden');
  });
}
