# Deputable AI website

Static marketing site for deputable.ai - plain HTML/CSS/JS, no framework, no build step.
Deployed via GitHub Pages from the repo root (custom domain in `CNAME`, `.nojekyll` present).

## How this repo works - IMPORTANT

**Do not hand-edit the generated files.** `scripts/generate_site.py` holds the shared
header/footer/nav and all page content in one place and writes them out.

To change anything:

1. Edit `scripts/generate_site.py` (content, nav, structure) and/or `css/style.css` / `js/main.js` (styling, behaviour).
2. Regenerate: `python3 scripts/generate_site.py` (writes to the repo root).
3. Preview: `python3 -m http.server 8080` from the repo root.

Generated: `index.html`, `platform.html`, `workflows.html`, `personal.html`,
`features.html`, `how-it-works.html` (nav label "Getting started"), `about.html`,
`trust.html`, `contact.html`, `privacy.html`,
`services.html` (a redirect to `platform.html`, so old links keep working),
`book/index.html` (the permanent `deputable.ai/book` redirect to the booking calendar -
print/QR/spoken links all point here), `demo/index.html` (the permanent `deputable.ai/demo`
link), `sitemap.xml`, `llms.txt`.
Hand-maintained: `css/style.css`, `js/main.js`, `assets/`, `robots.txt`, `CNAME`, `.nojekyll`,
`README.md`, `scripts/make_assets.py` + `scripts/make_qr.py` (dev-only; the QR encodes
`deputable.ai/book`, never the Zoho URL), `scripts/og-template.html`.

Placeholder constants at the top of the generator (`GA_MEASUREMENT_ID`,
`ZOHO_BOOKINGS_URL`, `ASSET_VER`) degrade gracefully while unset - see README.

## The source of truth is the platform

The product is the Deputy platform (`~/code/deputy`). Its master feature list,
`docs/features.md`, gives every feature a stable id and says where it runs and whether
it is proven. **The site may claim only what that list supports.**

- `FEATURES` (the Features page) and `CATALOGUE` (the Workflows page) in the generator
  carry each row's id (written into the HTML as `data-id`) and one of three statuses,
  which must match the list: **live** (in production, used on real calls or messages),
  **built** (built and tested, switched on with the first clients), **next** (agreed and
  drawn, not built). Rows with a `CORE-*` id describe the engine itself, read from the
  code (`squad/`, `members/_base/tools.py`), which the list does not number.
- Workflow steps on the site use the platform's own words and the platform's own way of
  drawing them: each step coloured by who does it (what starts it, plain code, an AI
  model, a person, "not yet"). The sources are `service/workflows.py` (the `Flow`
  declarations, the draft page), `config/workflow_parts.yaml` (what a business can
  build itself) and `docs/workflows.md` and `docs/learning.md` (why).
- When a feature ships or changes in the platform, change its row here in step.
- The Trust page states how the platform runs today. Before changing it, read the
  platform's `docs/legal/README.md`, which lists what is not yet true.

## Positioning rules (2026-08-27; revised 2026-11-13 for the Deputy platform)

- **Deputable is agentic workflow orchestration for SMEs, tailored to each business**
  (Prashant 2026-11-13: "it is coming off as an AI call answering system but it's so
  much more"). Lead with workflows: a deputy, its squad of specialists, and the work
  they run. **Call answering is one feature of many** - one door, one of six kinds of
  work - and never the headline, the first example in a list, or the page title.
- The headline stays "Delegate the busywork. Own the decisions." (Prashant 2026-11-13).
- **Always show the two tiers and why:** a business writes the simple workflows itself
  in a sentence, from parts the deputy already has; anything needing a new tool, a new
  specialist, a new kind of document or anything that pays or signs is built, tested and
  signed by Deputable. The reason is the point: the deputy never writes its own code.
- The product is **a deputy**: "a deputy for your business" and "a deputy of your own".
  The phone part keeps its name, **"Smart Call Handling"** - never "AI receptionist"
  (job-threatening framing). The stance line is "empower and enable people, never
  replace them".
- Say "agentic workflows" once where it positions the company (the eyebrow, the
  Platform page, page titles). Everywhere else use the plain words: workflow, squad,
  specialist, step. Internal names (officer, console, captain, pipeline, playbook,
  requisition) never appear on the site.
- **No pricing** on the site. **No invented social proof** - no testimonials, stats, client
  names or case studies until real ones exist (the homepage "Pilot results" panel is the
  designated slot). Example threads are illustrations and say so; they use made-up
  people and the 07700 900xxx drama range.
- **WhatsApp and text are claimed** (revised 2026-11-13: both are live in the platform).
  Channels and features that are not built are either absent or marked **next** on the
  Features page - never described as available. No "what we don't do" walls; positives
  only.
- **Not claimed yet**, deliberately: a UK-and-EU-only option, the AI suppliers'
  no-training terms (ours is stated; theirs waits on the confirmed contracts), website
  chat, bookings, CRM logging, a student deputy.
- Business model on the page: a deputy run as a service, set up around the client's own
  hours, people and rules; workflows drawn with the client before they are built; data
  that leaves with the client.
- Footer says "© Deputable AI · London" - no "Ltd"/"Registered in England & Wales" until
  the company is actually incorporated at Companies House.

## Behaviour notes

- The contact page embeds the Zoho Bookings calendar directly (one form - its booking
  form carries Company + "The process you'd like to discuss"; edit fields at
  bookings.zoho.eu, not here). No enquiry form, no JS state machine. Don't add
  "email us instead" prompts to the booking flow (Prashant 2026-08-27) - the footer
  contact line and the privacy notice keep the email.
- The homepage hero carries **the run demo**: four workflows, each started a different
  way (a call, a photo, an email, a schedule), shown as the steps the platform runs and
  then the message on the person's phone (`RUNS` in the generator). **The write-your-own
  demo** (`DRAFTS`) mirrors the platform's Add-a-workflow page with its two test cases.
  Everything is in the HTML, so the pages read without JavaScript; `js/main.js` only
  lights the steps in turn and switches tabs. Autoplay pauses off-viewport and never
  runs under `prefers-reduced-motion`.
- The hero headline is locked to two lines on every device (each sentence is a
  non-wrapping block sized to its column; see the comment in `css/style.css`).
- Repo is public (GitHub Pages): never commit secrets or `.idea/` (gitignored).

## Brand/style quick reference

The palette is the logo's. Two accents, one meaning each, everywhere:
**blue = the deputy did it**, **coral = a person decides** (approvals, the person's own
messages, the step that is theirs, the call to action on dark). A workflow step adds two
neutrals: navy for what starts it and plain ink for code, so a step reads as navy
(starts it), neutral (code), blue (an AI model) or coral (a person); a dashed box is a
part the deputy lacks.

Fonts: Bricolage Grotesque (headings), IBM Plex Sans (body, as the platform's own pages),
IBM Plex Mono (labels, commands such as `ok P14`).
Core colours: navy `#04285E`, ink `#0A1F44`, blue `#1C62F8`, coral `#F96A4B`,
paper `#FAF8F3`, night `#06183C` (the dark band).
Body text is left-aligned and ragged; headings are left-aligned.
Tone: plain-spoken, UK English, human-centric - AI assists and a person stays accountable;
avoid hype language that would put off AI-averse SME owners. No em dashes. Honesty is the
brand: never add a claim the company cannot demonstrate today.
