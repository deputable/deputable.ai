# Deputable AI website

Static marketing site for deputable.ai — plain HTML/CSS/JS, no framework, no build step.
Deployed via GitHub Pages from the repo root (custom domain in `CNAME`, `.nojekyll` present).

## How this repo works — IMPORTANT

**Do not hand-edit the generated files.** `scripts/generate_site.py` holds the shared
header/footer/nav and all page content in one place and writes them out.

To change anything:

1. Edit `scripts/generate_site.py` (content, nav, structure) and/or `css/style.css` / `js/main.js` (styling, behaviour).
2. Regenerate: `python3 scripts/generate_site.py` (writes to the repo root).
3. Preview: `python3 -m http.server 8080` from the repo root.

Generated: `index.html`, `services.html`, `how-it-works.html`, `about.html`, `trust.html`,
`contact.html`, `privacy.html`, `zoho-thanks.html`, `sitemap.xml`, `llms.txt`.
Hand-maintained: `css/style.css`, `js/main.js`, `assets/`, `robots.txt`, `CNAME`, `.nojekyll`,
`README.md`, `scripts/make_assets.py` (Pillow, dev-only), `scripts/og-template.html`.

Placeholder constants at the top of the generator (`GA_MEASUREMENT_ID`,
`ZOHO_BOOKINGS_URL`, `ASSET_VER`) degrade gracefully while unset — see README.

## Positioning rules (adopted 2026-08-27 — do not drift)

- The phone product is **"Smart Call Handling"** — never "AI receptionist" (job-threatening
  framing). Features are outcome-named; the stance line is "empower and enable people,
  never replace them".
- **No pricing** on the site. **No invented social proof** — no testimonials, stats, client
  names or case studies until real ones exist (the homepage "Pilot results" panel is the
  designated slot). No SMS/WhatsApp claims (listed under "What we don't do").
- Business model on the page: turn-key solutions integrated with the client's existing
  systems; optional ongoing-support contract; clean handover — the client owns what we build.
- Footer says "© Deputable AI · London" — no "Ltd"/"Registered in England & Wales" until
  the company is actually incorporated at Companies House.

## Behaviour notes

- Contact form is a Zoho Forms iframe with a two-step flow (form → book/skip) in
  `js/main.js` (`initDemoFlow`). Submission signal: `zoho-thanks.html` postMessage
  (once the Zoho redirect is configured) with a load-count fallback. Edit form fields
  at forms.zoho.eu, not here.
- The animated workflow diagram lives on the **homepage** (`FLOW_MODES` in `js/main.js`);
  human-approval steps are `{t, human:true}` objects and render amber. Autoplay pauses
  off-viewport and under `prefers-reduced-motion`; services links to `index.html#flow`.
- Repo is public (GitHub Pages): never commit secrets or `.idea/` (gitignored).

## Brand/style quick reference

Fonts: Schibsted Grotesk (body/headings), IBM Plex Mono (eyebrows/labels).
Core colours: navy `#0E2A4A`, ink `#0B1A2B`, teal `#16BFA0`, blue `#00B4FF`,
background `#FBFBF9`, human-in-the-loop amber `#E8A13D`.
Tone: plain-spoken, UK English, human-centric — AI assists and a person stays accountable;
avoid hype language that would put off AI-averse SME owners. Honesty is the brand: never
add a claim the company cannot demonstrate today.
