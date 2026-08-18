// Deputable AI — shared site behaviour (no framework, no build step)

document.addEventListener('DOMContentLoaded', () => {
  initMobileNav();
  initFlowDemo();
  initContactForm();
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

/* ---------------- Services page: interactive flow demo ---------------- */
const FLOW_MODES = [
  {
    label: 'Lead generation', entry: 'New enquiry', route: 'Lead triage',
    lanes: [
      { name: 'Repeat customer · fast path', steps: ['Match record', 'Book slot', 'Diary → CRM'] },
      { name: 'New enquiry', steps: ['Qualify lead', 'Call back', 'Capture detail', 'Human decision', 'System of record', 'Complete'] },
      { name: 'Outbound list', steps: ['Research', 'Verify contact', 'Draft approach', 'Human decision', 'Send & follow up', 'Complete'] }
    ]
  },
  {
    label: 'Inbound calls', entry: 'Customer calls', route: 'AI answers',
    lanes: [
      { name: 'Known caller · fast path', steps: ['Match job', 'Give update', 'Log note'] },
      { name: 'New job', steps: ['Take details', 'Check diary', 'Book slot', 'Notify engineer', 'System of record', 'Complete'] },
      { name: 'Urgent call-out', steps: ['Triage urgency', 'Safety checks', 'Find engineer', 'Human decision', 'Dispatch', 'Complete'] }
    ]
  },
  {
    label: 'Internal systems', entry: 'System event', route: 'Agent acts',
    lanes: [
      { name: 'Auto update · fast path', steps: ['Read system', 'Update record', 'Complete'] },
      { name: 'Stock reorder', steps: ['Check levels', 'Flag shortfall', 'Draft order', 'Human decision', 'Place order', 'Complete'] },
      { name: 'Job paperwork', steps: ['Transcribe notes', 'Draft report', 'Cost parts & hours', 'Human decision', 'Raise invoice', 'Complete'] }
    ]
  }
];

function initFlowDemo() {
  const root = document.querySelector('[data-flow-demo]');
  if (!root) return;

  let modeIdx = 0;
  let laneIdx = 1;

  const tabsEl = root.querySelector('[data-flow-tabs]');
  const entryEl = root.querySelector('[data-flow-entry]');
  const routeEl = root.querySelector('[data-flow-route]');
  const lanesEl = root.querySelector('[data-flow-lanes]');
  const legendEl = root.querySelector('[data-flow-legend]');

  function render() {
    const mode = FLOW_MODES[modeIdx];

    tabsEl.innerHTML = FLOW_MODES.map((m, i) =>
      `<button type="button" class="flow-tab${i === modeIdx ? ' active' : ''}" data-mode="${i}">${m.label}</button>`
    ).join('');

    entryEl.textContent = mode.entry;
    routeEl.textContent = mode.route;

    lanesEl.innerHTML = mode.lanes.map((lane, li) => {
      const steps = lane.steps.map(s => `<div class="flow-step"><div class="t">${s}</div></div>`).join('');
      return `<div class="flow-lane${li === laneIdx ? ' active' : ''}" data-lane="${li}">
        <div class="flow-lane-name">${lane.name}</div>
        ${steps}
      </div>`;
    }).join('');

    legendEl.innerHTML = mode.lanes.map((lane, li) =>
      `<button type="button" class="${li === laneIdx ? 'active' : ''}" data-lane="${li}"><span class="dot"></span>${lane.name}</button>`
    ).join('');

    root.querySelectorAll('[data-mode]').forEach(btn => {
      btn.addEventListener('click', () => {
        modeIdx = Number(btn.dataset.mode);
        laneIdx = Math.min(laneIdx, FLOW_MODES[modeIdx].lanes.length - 1);
        render();
      });
    });

    root.querySelectorAll('[data-lane]').forEach(el => {
      el.addEventListener('click', () => {
        laneIdx = Number(el.dataset.lane);
        render();
      });
    });
  }

  render();
}

/* ---------------- Contact form ---------------- */
function initContactForm() {
  const form = document.querySelector('[data-contact-form]');
  if (!form) return;
  const confirmBox = document.querySelector('[data-contact-confirm]');

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    // No backend wired up yet — swap this for a real submit (e.g. Formspree,
    // a serverless function, or mailto) when ready to go live.
    form.classList.add('hidden');
    if (confirmBox) confirmBox.classList.remove('hidden');
  });
}
