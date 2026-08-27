# Deputable AI — website

Plain HTML/CSS/JS site, no build step. All pages are **generated** by
`scripts/generate_site.py` (see CLAUDE.md — never hand-edit the HTML):

- `index.html` — Home (hero, Smart Call Handling, animated workflow diagram, honesty section)
- `services.html` — Services (Smart Call Handling flagship, website chat, workflow automation, readiness)
- `how-it-works.html` — five-step process/timeline
- `about.html` — the "deputable" narrative + founders
- `trust.html` — trust & security Q&A (FAQPage JSON-LD)
- `contact.html` — two-step demo flow (Zoho form → book a call / skip)
- `privacy.html` — privacy notice (linked from the footer)
- `zoho-thanks.html` — hidden helper page: the Zoho form's post-submission
  redirect target; signals "submitted" to the contact page (not in sitemap)
- `sitemap.xml`, `llms.txt` — regenerated on every run; `robots.txt` is static

## Run locally

No build tools needed. From this folder:

```
python3 scripts/generate_site.py   # regenerate after any content change
python3 -m http.server 8080
```

then open `http://localhost:8080`.

## Placeholder constants (top of `scripts/generate_site.py`)

- `GA_MEASUREMENT_ID` — paste the GA4 `G-…` id once the property exists.
  Until then **no analytics or consent banner is emitted at all**. When set,
  GA4 loads with Consent Mode v2 default-denied and a lightweight
  accept/decline banner (PECR-compliant).
- `ZOHO_BOOKINGS_URL` — paste the Zoho Bookings booking-page URL. Until then
  the contact flow skips the "book a call" step and shows a plain
  confirmation (no dead button ships).
- `ASSET_VER` — bump to cache-bust the favicon/logo after changing artwork.

## Contact form (Zoho)

The demo-request form is a Zoho Forms iframe (`DemoRequest`, EU-hosted) —
edit its fields at forms.zoho.eu, not here. Two-step flow: after submit the
page offers "Book a Call" (Zoho Bookings) or "Skip — we'll call you back".
Submission is detected two ways: deterministically, once the form's
post-submission rule is set to redirect to
`https://deputable.ai/zoho-thanks.html`; and by a load-count fallback that
works even before that rule is configured. Anyone who submits without
booking should be called back — the lead is already in Zoho.

## Assets

`scripts/make_assets.py` (needs Pillow, dev-only) rebuilds the favicon set,
apple-touch icon and the optimised logo from `assets/deputable-logo.png`.
`scripts/og-template.html` is the source for `assets/og-image.png`
(1200×630 social-share image) — the capture command is in its header comment.

## Deploy to GitHub Pages with the deputable.ai domain

1. Push to `main` — GitHub Pages serves the repo root (`CNAME` holds
   `deputable.ai`, `.nojekyll` disables Jekyll).
2. DNS: `A` records for the apex to `185.199.108.153`, `185.199.109.153`,
   `185.199.110.153`, `185.199.111.153`; optional `www` CNAME to
   `<github-username>.github.io`; Enforce HTTPS in Settings → Pages.

## Founder to-dos (site works without them; each upgrades one feature)

- Zoho Forms: fields → Name, Company, Email, Phone, "What do you hope to
  get out of this?"; post-submission redirect → `https://deputable.ai/zoho-thanks.html`.
- Zoho Bookings: create a 45-minute "Demo call" booking page (Rohit's
  calendar), paste URL into `ZOHO_BOOKINGS_URL`, regenerate.
- GA4: create property, paste id into `GA_MEASUREMENT_ID`, regenerate;
  then Google Search Console + submit `sitemap.xml`.
- Founder photos for the About page (portrait placeholders were removed
  until real photos exist); privacy-page text sign-off; reverse-image
  check on the logo (TinEye / Google Images).
- The footer says "© Deputable AI · London" (no "Ltd", no "Registered in
  England & Wales") until incorporation actually happens — restore the
  registered line in `footer()` after Companies House registration.
