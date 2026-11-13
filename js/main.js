// Deputable AI - shared site behaviour (no framework, no build step)

document.addEventListener('DOMContentLoaded', () => {
  initMobileNav();
  initThreadDemo();
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

/* ---------------- Homepage: the thread demo ----------------
   The scenarios and their messages are written into the page by
   scripts/generate_site.py (DEMO_SCENARIOS), so the page reads in full
   without this script. Here we only reveal a scenario's messages one
   after another, the way they would arrive on a phone, and switch
   scenarios from the tabs.

   Autoplay runs only while the demo is on screen, moves on to the next
   scenario by itself until the visitor picks a tab, and never runs
   under prefers-reduced-motion (the messages are simply all there). */
function initThreadDemo() {
  const root = document.querySelector('[data-demo]');
  if (!root) return;

  const tabs = Array.from(root.querySelectorAll('[data-demo-tab]'));
  const panels = Array.from(root.querySelectorAll('[data-demo-panel]'));
  const nameEl = root.querySelector('[data-demo-name]');
  const viaEl = root.querySelector('[data-demo-via]');
  if (!tabs.length || !panels.length) return;

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const FIRST_MS = 400;       // before the first message
  const DEPUTY_MS = 1600;     // dwell after one of the deputy's messages
  const YOU_MS = 1100;        // dwell after one of the person's
  const HOLD_MS = 5200;       // the finished thread, before moving on

  let current = 0;
  let timers = [];
  let inView = false;
  let auto = true;            // false once the visitor picks a tab
  let playing = false;

  function clearTimers() {
    timers.forEach(clearTimeout);
    timers = [];
    playing = false;
  }

  function settle(panel) {
    // show everything, with no animation pending
    panel.classList.remove('is-armed');
    Array.from(panel.children).forEach(c => c.classList.remove('is-in'));
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
    nameEl.textContent = panels[i].dataset.name;
    viaEl.textContent = panels[i].dataset.via;
  }

  function play(i) {
    clearTimers();
    select(i);
    if (reduceMotion.matches || !inView) return;

    const panel = panels[i];
    const msgs = Array.from(panel.children);
    panel.classList.add('is-armed');
    playing = true;

    let at = FIRST_MS;
    msgs.forEach((m) => {
      timers.push(setTimeout(() => m.classList.add('is-in'), at));
      at += m.classList.contains('you') ? YOU_MS : DEPUTY_MS;
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

  const observer = new IntersectionObserver((entries) => {
    inView = entries[0].isIntersecting;
    if (inView) {
      if (!playing) play(current);
    } else {
      // off screen: stop the clock and leave the whole thread readable
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

  select(0);
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
