// Deputable AI - shared site behaviour (no framework, no build step)

document.addEventListener('DOMContentLoaded', () => {
  initMobileNav();
  initFlowDemo();
  initConsent();
});

/* ---------------- Mobile nav toggle ---------------- */
function initMobileNav() {
  const toggle = document.querySelector('.mobile-toggle');
  const nav = document.querySelector('nav.main-nav');
  if (!toggle || !nav) return;
  toggle.addEventListener('click', () => {
    nav.classList.toggle('open');
  });
}

/* ---------------- Homepage: animated workflow diagram ----------------
   Steps are strings, or {t, human:true} for the approval steps a person
   must pass - those render amber and the animation dwells on them. */
const FLOW_MODES = [
  {
    label: 'New enquiry', entry: 'Customer calls', route: 'AI answers',
    lanes: [
      { name: 'Known caller · fast path', steps: ['Match record', 'Give update', 'Log note'] },
      { name: 'New enquiry', steps: ['Qualify enquiry', 'Capture details', 'Check diary', 'Propose slot', { t: 'Approve & price', human: true }, 'Confirm by email', 'CRM updated'] },
      { name: 'Callback requested', steps: ['Take number', 'Note the reason', 'Suggest times', { t: 'Person calls back', human: true }, 'Log outcome'] }
    ]
  },
  {
    label: 'Job booked to done', entry: 'New job', route: 'Agent organises',
    lanes: [
      { name: 'Routine job · fast path', steps: ['Take details', 'Check diary', 'Book slot'] },
      { name: 'New booking', steps: ['Take details', 'Check diary', 'Book slot', { t: 'Approve dispatch', human: true }, 'Notify engineer', 'Records updated'] },
      { name: 'Urgent call-out', steps: ['Triage urgency', 'Safety checks', 'Find engineer', { t: 'Human decision', human: true }, 'Dispatch', 'Records updated'] }
    ]
  },
  {
    label: 'After the job', entry: 'Job complete', route: 'Agent drafts',
    lanes: [
      { name: 'Paperwork · fast path', steps: ['Transcribe notes', 'Draft report', 'File'] },
      { name: 'Follow-up', steps: ['Draft follow-up email', 'Prepare survey', { t: 'Approve & send', human: true }, 'Send & log replies'] },
      { name: 'Invoice', steps: ['Cost parts & hours', 'Draft invoice', { t: 'Approve', human: true }, 'Raise invoice', 'Records updated'] }
    ]
  }
];

function initFlowDemo() {
  const root = document.querySelector('[data-flow-demo]');
  if (!root) return;

  const norm = (s) => (typeof s === 'string' ? { t: s, human: false } : s);
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const STEP_MS = 900;
  const HUMAN_MS = 1800;
  const LANE_HOLD_MS = 1500;
  const RESUME_MS = 12000;

  const tabsEl = root.querySelector('[data-flow-tabs]');
  const entryEl = root.querySelector('[data-flow-entry]');
  const routeEl = root.querySelector('[data-flow-route]');
  const lanesEl = root.querySelector('[data-flow-lanes]');
  const legendEl = root.querySelector('[data-flow-legend]');

  let modeIdx = 0;
  let laneEls = [];
  let stepEls = [];        // stepEls[lane][step]
  let timer = null;
  let cursor = { lane: 0, step: -1 };
  let inView = false;
  let userPaused = false;
  let resumeTimer = null;

  tabsEl.innerHTML = FLOW_MODES.map((m, i) =>
    `<button type="button" class="flow-tab${i === 0 ? ' active' : ''}" data-mode="${i}">${m.label}</button>`
  ).join('');

  function buildMode(i) {
    modeIdx = i;
    const mode = FLOW_MODES[i];
    entryEl.textContent = mode.entry;
    routeEl.textContent = mode.route;

    lanesEl.innerHTML = mode.lanes.map((lane, li) => {
      const steps = lane.steps.map(norm).map(s =>
        `<div class="flow-step${s.human ? ' human' : ''}"><div class="t">${s.t}</div></div>`
      ).join('');
      return `<div class="flow-lane" data-lane="${li}">
        <div class="flow-lane-name">${lane.name}</div>
        ${steps}
      </div>`;
    }).join('');

    legendEl.innerHTML = mode.lanes.map((lane, li) =>
      `<button type="button" data-lane="${li}"><span class="dot"></span>${lane.name}</button>`
    ).join('');

    tabsEl.querySelectorAll('[data-mode]').forEach(btn =>
      btn.classList.toggle('active', Number(btn.dataset.mode) === i));

    laneEls = Array.from(lanesEl.querySelectorAll('.flow-lane'));
    stepEls = laneEls.map(l => Array.from(l.querySelectorAll('.flow-step')));
    cursor = { lane: 0, step: -1 };
  }

  function clearLit() {
    laneEls.forEach(l => l.classList.remove('playing', 'active'));
    stepEls.flat().forEach(s => s.classList.remove('lit'));
    legendEl.querySelectorAll('button').forEach(b => b.classList.remove('active'));
  }

  function stop() {
    if (timer) { clearTimeout(timer); timer = null; }
  }

  function shouldPlay() {
    return inView && !userPaused && !reduceMotion.matches;
  }

  function play() {
    stop();
    if (!shouldPlay()) return;
    tick();
  }

  function tick() {
    if (!shouldPlay()) { stop(); return; }
    const lane = laneEls[cursor.lane];
    const steps = stepEls[cursor.lane];

    cursor.step += 1;
    if (cursor.step >= steps.length) {
      // lane complete: hold, then clear and move on
      timer = setTimeout(() => {
        lane.classList.remove('playing');
        steps.forEach(s => s.classList.remove('lit'));
        cursor = { lane: (cursor.lane + 1) % laneEls.length, step: -1 };
        tick();
      }, LANE_HOLD_MS);
      return;
    }

    lane.classList.add('playing');
    const el = steps[cursor.step];
    el.classList.add('lit');
    timer = setTimeout(tick, el.classList.contains('human') ? HUMAN_MS : STEP_MS);
  }

  function selectLane(li) {
    stop();
    clearLit();
    laneEls[li].classList.add('active');
    legendEl.querySelectorAll('button').forEach(b =>
      b.classList.toggle('active', Number(b.dataset.lane) === li));
  }

  function pauseForUser() {
    userPaused = true;
    if (resumeTimer) clearTimeout(resumeTimer);
    resumeTimer = setTimeout(() => {
      userPaused = false;
      if (reduceMotion.matches) return;   // stay on the manual view
      clearLit();
      cursor = { lane: 0, step: -1 };
      play();
    }, RESUME_MS);
  }

  root.addEventListener('click', (evt) => {
    const modeBtn = evt.target.closest('[data-mode]');
    if (modeBtn) {
      buildMode(Number(modeBtn.dataset.mode));
      if (reduceMotion.matches || userPaused) selectLane(Math.min(1, laneEls.length - 1));
      else { clearLit(); play(); }
      if (!reduceMotion.matches) pauseForUser();
      return;
    }
    const laneBtn = evt.target.closest('[data-lane]');
    if (laneBtn) {
      selectLane(Number(laneBtn.dataset.lane));
      pauseForUser();
    }
  });

  const observer = new IntersectionObserver((entries) => {
    inView = entries[0].isIntersecting;
    if (inView) play(); else stop();
  }, { threshold: 0.3 });
  observer.observe(root);

  reduceMotion.addEventListener('change', () => {
    if (reduceMotion.matches) { stop(); clearLit(); selectLane(Math.min(1, laneEls.length - 1)); }
    else { clearLit(); cursor = { lane: 0, step: -1 }; play(); }
  });

  buildMode(0);
  if (reduceMotion.matches) selectLane(Math.min(1, laneEls.length - 1));
  // autoplay starts when the observer reports the diagram in view
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
