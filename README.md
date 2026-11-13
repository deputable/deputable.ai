# Deputable AI - website

Plain HTML/CSS/JS site, no build step. All pages are **generated** by
`scripts/generate_site.py` (see CLAUDE.md - never hand-edit the HTML):

- `index.html` - Home (hero with the thread demo, the doors, what happens on a call,
  approvals, workflows, a deputy of your own, learning, trust, honesty section)
- `business.html` - A deputy for your business (Smart Call Handling, WhatsApp and text,
  the note after a call, approvals and commands, workflows, your team)
- `personal.html` - A deputy of your own (mail, diary, reminders, lists, errands)
- `features.html` - everything it does, each row marked live, built or next and tied
  to an id in the Deputy platform's `docs/features.md`
- `how-it-works.html` - six steps from a first call to go-live, plus the assessment
- `about.html` - the "deputable" narrative + founders
- `trust.html` - trust & security Q&A (FAQPage JSON-LD) and the supplier table
- `contact.html` - the booking page: Zoho Bookings calendar embedded directly
  (its booking form collects name, email, phone, company and the process to
  discuss - one form, no separate enquiry step)
- `privacy.html` - privacy notice (linked from the footer)
- `services.html` - a redirect to `business.html`, kept so old links work
- `sitemap.xml`, `llms.txt` - regenerated on every run; `robots.txt` is static

## Run locally

No build tools needed. From this folder:

```
python3 scripts/generate_site.py   # regenerate after any content change
python3 -m http.server 8080
```

then open `http://localhost:8080`.

## Placeholder constants (top of `scripts/generate_site.py`)

- `GA_MEASUREMENT_ID` - paste the GA4 `G-…` id once the property exists.
  Until then **no analytics or consent banner is emitted at all**. When set,
  GA4 loads with Consent Mode v2 default-denied and a lightweight
  accept/decline banner (PECR-compliant).
- `ZOHO_BOOKINGS_URL` / `ZOHO_BOOKINGS_EMBED_URL` - the live Demo Call
  booking page (public link and Zoho's frameable portal-embed variant).
  If ever unset, the contact page degrades to an email fallback panel.
- `ASSET_VER` - bump to cache-bust the favicon/logo after changing artwork.
  (css/js bust automatically via content-hash query strings.)

## Booking (Zoho Bookings)

The contact page embeds the Zoho Bookings "Demo Call" calendar directly -
one form, managed at bookings.zoho.eu (workspace "Deputable.ai"): 45-minute
one-on-one, 15-min post-buffer, 4-hour minimum notice, booking form fields
Name / Email / Contact Number / Company / "The process you'd like to
discuss". Slots follow the staff member's working hours; bookings sync with
their Zoho Calendar. The old Zoho Forms enquiry form is retired (the
DemoRequest form still exists at forms.zoho.eu but nothing links to it).

## The shareable booking link: deputable.ai/book

`book/index.html` (generated) redirects to the Zoho Bookings Demo Call page.
Use `deputable.ai/book` on ANYTHING printed, spoken, or signed - cards, flyers,
email signatures, QR codes - never the raw Zoho URL or a third-party shortener:
this repo controls where /book points, so printed material survives a change of
booking provider. `assets/book-qr.svg` (vector master) and `assets/book-qr.png`
(2048px, branded) encode it - regenerate with `scripts/make_qr.py` and re-run
its scan check if the artwork ever changes.

## Assets

`scripts/make_assets.py` (needs Pillow, dev-only) rebuilds the favicon set,
apple-touch icon and the optimised logo from `assets/deputable-logo.png`.
`scripts/og-template.html` is the source for `assets/og-image.png`
(1200×630 social-share image) - the capture command is in its header comment.

Colours and fonts are in `CLAUDE.md` (brand quick reference) and as tokens at the
top of `css/style.css`; the palette is the logo's.

## Deploy to GitHub Pages with the deputable.ai domain

1. Push to `main` - GitHub Pages serves the repo root (`CNAME` holds
   `deputable.ai`, `.nojekyll` disables Jekyll).
2. DNS: `A` records for the apex to `185.199.108.153`, `185.199.109.153`,
   `185.199.110.153`, `185.199.111.153`; optional `www` CNAME to
   `<github-username>.github.io`; Enforce HTTPS in Settings → Pages.

## Founder to-dos (site works without them; each upgrades one feature)

- Zoho Forms: fields → Name, Company, Email, Phone, "What do you hope to
  get out of this?"; post-submission redirect → `https://deputable.ai/zoho-thanks.html`.
- **Zoho Bookings setup (Rohit, ~15 min)** - note: plain Zoho Calendar has
  no public booking page; Zoho Bookings is the Zoho product for that and
  syncs two-way with Zoho Calendar (its free tier covers one staff member):
  1. Sign in at bookings.zoho.eu (same Zoho org as the forms account).
  2. Create a workspace, add Rohit as staff, and connect his Zoho
     Calendar under staff → calendar sync - his events then block slots,
     and bookings land back in his calendar.
  3. Create one service: "Demo call", **45 minutes**, one-on-one; set
     working hours, a buffer (e.g. 15 min), and minimum notice; enable
     email confirmations (and meeting-link generation if wanted).
  4. Copy the service's public booking-page URL (Share → copy link) into
     `ZOHO_BOOKINGS_URL` in `scripts/generate_site.py`, regenerate, push.
  Once the URL is set, contact-page step 2 embeds the calendar inline
  (with a new-tab fallback link); while unset, the flow degrades to a
  plain "we'll be in touch" confirmation.
- GA4: create property, paste id into `GA_MEASUREMENT_ID`, regenerate;
  then Google Search Console + submit `sitemap.xml`.
- Founder photos for the About page (portrait placeholders were removed
  until real photos exist); privacy-page text sign-off; reverse-image
  check on the logo (TinEye / Google Images).
- The footer says "© Deputable AI · London" (no "Ltd", no "Registered in
  England & Wales") until incorporation actually happens - restore the
  registered line in `footer()` after Companies House registration.
