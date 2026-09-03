// Deputable AI - shared site behaviour (no framework, no build step)

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

/* ---------------- Contact form (Zoho Forms embed) ---------------- */
function initContactForm() {
  const frame = document.querySelector('[data-zoho-form]');
  if (!frame) return;
  const clip = document.querySelector('[data-zoho-clip]');
  const confirmBox = document.querySelector('[data-contact-confirm]');
  const FOOTER_CROP = 208; // hides Zoho's disclaimer/branding strip

  // Zoho (with zf_rszfm=1) posts "<perma>|<height>" whenever the form's
  // content height changes. Size the iframe to fit and clip the footer.
  window.addEventListener('message', (evt) => {
    if (typeof evt.data !== 'string' || evt.data.indexOf('|') === -1) return;
    if (frame.src.indexOf(evt.data.split('|')[0]) === -1) return;
    const h = parseInt(evt.data.split('|')[1], 10);
    if (!h || h < 300) return;
    frame.style.height = (h + 15) + 'px';
    if (clip) clip.style.height = Math.max(h + 15 - FOOTER_CROP, 300) + 'px';
  });

  // The iframe loads once with the blank form; any later load is the
  // post-submit page, so we swap in our own confirmation instead of
  // showing Zoho's thank-you screen.
  let loads = 0;
  frame.addEventListener('load', () => {
    loads += 1;
    if (loads > 1 && confirmBox) {
      if (clip) clip.classList.add('hidden');
      frame.classList.add('hidden');
      confirmBox.classList.remove('hidden');
    }
  });
}
