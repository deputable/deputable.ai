import datetime
import json
import os

# Output to the repo root (this script lives in scripts/)
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ------------------------------------------------------------------
# Site-wide constants. The placeholder values below degrade
# gracefully: an unset GA id emits no analytics at all, and an unset
# bookings URL makes the contact flow skip straight to confirmation.
# ------------------------------------------------------------------
BASE_URL = "https://deputable.ai/"
ASSET_VER = "2"                     # bump to cache-bust icons/logo
GA_MEASUREMENT_ID = "G-XXXXXXXXXX"  # FOUNDER TO-DO: create GA4 property, paste id
ZOHO_BOOKINGS_URL = "https://deputableai.zohobookings.eu/264805000000037050"  # Demo Call, 45 min
ZOHO_BOOKINGS_EMBED_URL = "https://deputableai.zohobookings.eu/portal-embed#/264805000000037050"
TAGLINE = "Simplify Work. Amplify People."

GA_IS_SET = not GA_MEASUREMENT_ID.endswith("XXXXXXXXXX")


def _content_ver(relpath):
    """Short content hash for cache-busting css/js URLs: every deploy
    that changes the file busts caches automatically, so GitHub Pages'
    10-minute asset cache can never serve fresh HTML with stale JS."""
    import hashlib
    with open(os.path.join(OUT, relpath), "rb") as fh:
        return hashlib.md5(fh.read()).hexdigest()[:8]


CSS_VER = _content_ver("css/style.css")
JS_VER = _content_ver("js/main.js")

NAV_ITEMS = [
    ("services.html", "services", "Services"),
    ("how-it-works.html", "process", "How It Works"),
    ("about.html", "about", "About"),
    ("trust.html", "trust", "Trust & Security"),
    ("contact.html", "contact", "Contact"),
]

SITE_TITLE = "Deputable AI - Smart Call Handling & AI Operations for UK Businesses"
SITE_DESC = "AI that answers your phone out of hours, catches overflow calls, and runs routine workflows - with a person in charge of every decision that matters. Built in London."

ORG_JSONLD = json.dumps({
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "Deputable AI",
    "url": BASE_URL,
    "logo": BASE_URL + "assets/deputable-logo.png",
    "email": "hello@deputable.ai",
    "slogan": TAGLINE,
    "address": {"@type": "PostalAddress", "addressLocality": "London", "addressCountry": "GB"},
    "founder": [
        {"@type": "Person", "name": "Rohit Sinha", "sameAs": "https://www.linkedin.com/in/rohit-sinha-b6792715/"},
        {"@type": "Person", "name": "Prashant Tiwari", "sameAs": "https://www.linkedin.com/in/prashanttiwari247/"},
    ],
})

# Consent Mode v2, default-denied: no analytics cookie is set until the
# visitor accepts the banner (PECR/ICO-compliant path for GA4).
GA_SNIPPET = """<script>
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('consent', 'default', {'analytics_storage':'denied','ad_storage':'denied','ad_user_data':'denied','ad_personalization':'denied'});
gtag('js', new Date());
gtag('config', '__GA_ID__');
</script>
<script async src="https://www.googletagmanager.com/gtag/js?id=__GA_ID__"></script>"""


def head(title, desc, active_id, filename, relpath_prefix="", extra_head=""):
    canonical = BASE_URL if filename == "index.html" else BASE_URL + filename
    ga = GA_SNIPPET.replace("__GA_ID__", GA_MEASUREMENT_ID) if GA_IS_SET else ""
    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Deputable AI">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{BASE_URL}assets/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Deputable AI - Delegate the busywork. Own the decisions.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{BASE_URL}assets/og-image.png">
<link rel="icon" href="{relpath_prefix}assets/favicon.ico?v={ASSET_VER}" sizes="32x32">
<link rel="icon" type="image/png" href="{relpath_prefix}assets/icon-192.png?v={ASSET_VER}" sizes="192x192">
<link rel="apple-touch-icon" href="{relpath_prefix}assets/apple-touch-icon.png?v={ASSET_VER}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{relpath_prefix}css/style.css?v={CSS_VER}">
<script type="application/ld+json">{ORG_JSONLD}</script>{extra_head}{ga}
</head>
<body>
<div class="page-shell">
{header(active_id, relpath_prefix)}
<main>
"""


def header(active_id, relpath_prefix=""):
    links = []
    for href, pid, label in NAV_ITEMS:
        cls = "nav-link active" if pid == active_id else "nav-link"
        links.append(f'<a class="{cls}" href="{relpath_prefix}{href}">{label}</a>')
    nav_links = "\n        ".join(links)
    home_href = relpath_prefix + "index.html" if relpath_prefix else "index.html"
    return f"""  <header class="site-header">
    <div class="wrap header-inner">
      <a class="logo-link" href="{home_href}">
        <img src="{relpath_prefix}assets/deputable-logo.png?v={ASSET_VER}" alt="Deputable AI - {TAGLINE}">
      </a>
      <button class="mobile-toggle" aria-label="Toggle menu">Menu</button>
      <nav class="main-nav">
        {nav_links}
        <a class="btn-nav" href="{relpath_prefix}contact.html">Book a Demo</a>
      </nav>
    </div>
  </header>"""


def footer(relpath_prefix=""):
    links = "\n          ".join(
        f'<a href="{relpath_prefix}{href}">{label}</a>' for href, pid, label in NAV_ITEMS
    )
    return f"""  <footer class="site-footer">
    <div class="wrap footer-top">
      <div class="footer-brand">
        <img src="{relpath_prefix}assets/deputable-logo.png?v={ASSET_VER}" alt="Deputable AI">
        <p class="footer-tagline">{TAGLINE}</p>
        <p>Human-centric AI for small and mid-sized businesses, from our London HQ.</p>
      </div>
      <div class="footer-col">
        <div class="footer-col-title">Explore</div>
        <div class="footer-nav">
          {links}
        </div>
      </div>
      <div class="footer-col">
        <div class="footer-col-title">Contact</div>
        <div class="footer-contact">
          <a href="mailto:hello@deputable.ai">hello@deputable.ai</a>
          <div>London, UK</div>
        </div>
      </div>
    </div>
    <div class="footer-bottom">
      <div class="wrap footer-bottom-inner">
        <span>&copy; 2026 Deputable AI &middot; London</span>
        <a href="{relpath_prefix}privacy.html">Privacy</a>
      </div>
    </div>
  </footer>"""


def consent_banner():
    if not GA_IS_SET:
        return ""
    return """
<div class="consent-bar hidden" data-consent-bar>
  <p>We use one optional analytics cookie to understand how the site is used. Nothing is set unless you accept.</p>
  <div class="consent-actions">
    <button type="button" class="btn btn-primary" data-consent-accept>Accept</button>
    <button type="button" class="btn btn-secondary" data-consent-decline>Decline</button>
  </div>
</div>"""


def tail(relpath_prefix=""):
    return f"""</main>
{footer(relpath_prefix)}
</div>{consent_banner()}
<script src="{relpath_prefix}js/main.js?v={JS_VER}"></script>
</body>
</html>
"""


WRITTEN = []  # (filename, title, desc) for sitemap.xml + llms.txt


def write_page(filename, title, desc, active_id, body, extra_head="", in_sitemap=True):
    html = head(title, desc, active_id, filename, extra_head=extra_head) + body + tail()
    with open(os.path.join(OUT, filename), "w") as f:
        f.write(html)
    if in_sitemap:
        WRITTEN.append((filename, title, desc))
    print(f"Generated: {filename}")


def cta_band(title, sub, label="Book a Demo Call"):
    return f"""
<section class="bg-navy">
  <div class="wrap cta-band">
    <div>
      <h2>{title}</h2>
      <p>{sub}</p>
    </div>
    <a class="btn btn-teal" href="contact.html">{label}</a>
  </div>
</section>
"""


def flow_demo_html():
    """The animated workflow diagram. Tab/lane/step labels live in
    js/main.js (FLOW_MODES); human-approval steps are objects with
    human:true and render amber."""
    return """
    <div data-flow-demo id="flow">
      <div class="flow-tabs" data-flow-tabs></div>
      <div class="flow-panel">
        <div class="flow-row">
          <div class="flow-start">
            <div class="flow-box entry">
              <div class="label">Entry</div>
              <div class="val" data-flow-entry></div>
            </div>
            <div class="flow-connector"></div>
            <div class="flow-box route">
              <div class="label">Auto-route</div>
              <div class="val" data-flow-route></div>
            </div>
          </div>
          <div class="flow-lanes" data-flow-lanes></div>
        </div>
        <div class="flow-legend" data-flow-legend></div>
        <div class="flow-key"><span class="key-dot"></span>Amber steps wait for a person - nothing passes them on its own.</div>
        <div class="flow-note">Some things are not deputable: pricing, hiring, contractual commitments, and any complaint with real consequences. Those stay with your people, always.</div>
      </div>
    </div>"""


def booking_html():
    """One-form booking: the Zoho Bookings calendar embedded directly.
    Its booking form collects everything (name, email, phone, company,
    the process to discuss), so there is no separate enquiry form.
    The portal-embed variant is Zoho's frameable URL; the public page
    sends X-Frame-Options and is used for the new-tab link only."""
    if not ZOHO_BOOKINGS_URL:
        return """
    <div class="booking-fallback">
      <p class="prose">Write to <a href="mailto:hello@deputable.ai">hello@deputable.ai</a> with a line about the business and the process you'd like handled, and we'll ring you back - usually within one working day.</p>
    </div>"""
    embed_src = ZOHO_BOOKINGS_EMBED_URL or ZOHO_BOOKINGS_URL
    return f"""
    <iframe class="booking-embed" src="{embed_src}" title="Book a 45-minute demo call" frameborder="0"></iframe>
    <p class="prose small booking-foot">Prefer a new tab? <a class="link-arrow" href="{ZOHO_BOOKINGS_URL}" target="_blank" rel="noopener">Open the calendar &rarr;</a></p>"""


# ==================================================================
# HOME
# ==================================================================
modes_home = [
    ("Out of hours", "Every call answered.",
     "When the office closes, the AI picks up - evenings, weekends and bank holidays. It answers the routine questions, takes proper details, and books callbacks so the morning starts with a list, not a voicemail backlog."),
    ("Office hours · overflow", "No caller lost to a busy line.",
     "When everyone is already on a call, the AI takes the next one. It captures who's calling and why, answers what it safely can, and queues the rest for the right person - so a busy hour doesn't cost you a customer."),
    ("Live, during the call", "Your team, two steps ahead.",
     "While one of your people takes the call, the AI works alongside them - surfacing the caller's history, the job details and the next free slot as the conversation happens. The customer just notices they're talking to someone who already knows."),
]

services_home = [
    ("#00B4FF", "website-chat", "Website Chat", "The same engine that answers your phone, on your website. Enquiries answered, details captured, callbacks arranged - one system, one conversation history."),
    ("#16BFA0", "workflow-automation", "Workflow Automation", "Built bespoke around one process of yours - route planning, stock reordering, job paperwork - connected to the systems you already run, with an approval step wherever a mistake would reach a customer."),
    ("#0E2A4A", "readiness", "AI Readiness Assessment", "Two weeks mapping where AI would genuinely save time, and where it would not. You get a costed shortlist, not a strategy document."),
]

# Shared by the homepage and About page - keep the two in step.
depute_items = [
    "Out-of-hours and overflow call answering",
    "Appointment booking and diary management",
    "Customer detail capture and callbacks",
    "Data entry across your systems",
    "Follow-up drafts and routine reports",
    "Routine paperwork and reminders",
]

keep_items = [
    "Pricing and quote negotiations",
    "Managing human resources",
    "Escalated complaints and disputes",
    "Contractual commitments",
    "Decisions that carry your reputation",
]

assure_items = [
    "A named person stays accountable",
    "Your data is never our training set",
    "Built to be handed over, not held hostage",
]

result_metrics = ["Calls answered", "Response time", "Hours saved", "Error rate"]

home_steps = [
    ("01", "Week 0", "Demo Call", "You bring a process. We walk through how it would run and whether it is worth doing."),
    ("02", "Weeks 1–2", "Assessment", "We map the work as it happens today and cost the options."),
    ("03", "Weeks 3–6", "Build", "One workflow, deployed to a small group first, with approval steps in place."),
    ("04", "Weeks 7–8", "Handover", "Documentation, training, and a review of what it saved."),
    ("05", "Ongoing", "Support (optional)", "Monitoring, tuning and a monthly report, priced separately. Or run it yourself - it's yours either way."),
]

home_body = f"""
<section class="hero">
  <div class="wrap hero-center">
    <div class="eyebrow">Simplify work &middot; Amplify people</div>
    <h1 class="hero-title"><span>Delegate the busywork.</span> <span>Own the decisions.</span></h1>
    <p class="hero-sub">We build AI that takes on the work you'd hand to a trusted deputy - answering the phone after hours, picking up overflow calls while your team is busy, running the routine steps of scheduling, stock and paperwork. Turn-key, fitted to the systems you already run, with a person in charge of everything that matters.</p>
    <div class="hero-ctas">
      <a class="btn btn-primary" href="contact.html">Book a Demo Call</a>
      <a class="btn btn-secondary" href="how-it-works.html">See How It Works</a>
    </div>
  </div>
</section>

<section class="bg-white border-b">
  <div class="wrap section-pad section-center">
    <div class="eyebrow">Smart Call Handling</div>
    <h2>The phone, handled. Three ways.</h2>
    <p class="prose section-sub">One system, fitted to how your day actually runs - not a machine that takes your team's place, but one that covers for it and backs it up.</p>
    <div class="grid-3">
      {"".join(f'<div class="mode-card"><div class="mode-kicker">{k}</div><h3>{t}</h3><p>{b}</p></div>' for k, t, b in modes_home)}
    </div>
    <div class="section-foot"><a class="link-arrow" href="services.html#smart-call-handling">Smart Call Handling in full &rarr;</a></div>
  </div>
</section>

<section>
  <div class="wrap section-pad section-center">
    <h2>More than the phone.</h2>
    <p class="prose section-sub">An AI operations partner for UK small and mid-sized businesses - three more ways we take on the busywork.</p>
    <div class="grid-3">
      {"".join(f'<div class="card"><div class="accent" style="background:{a}"></div><h3>{t}</h3><p>{b}</p><a class="link-arrow card-link" href="services.html#{anchor}">Learn more &rarr;</a></div>' for a, anchor, t, b in services_home)}
    </div>
    <div class="section-foot"><a class="link-arrow" href="services.html">All services &rarr;</a></div>
  </div>
</section>

<section class="bg-white border-t border-b">
  <div class="wrap section-pad section-center">
    <h2>Watch a job run end to end.</h2>
    <p class="prose section-sub">Every flow below has a step only a person can pass - it's marked. That's not a limitation we apologise for; it's the design.</p>
    {flow_demo_html()}
    <p class="prose flow-after">Follow-ups go only to customers you already serve, by email or a callback they asked for. We don't do cold outbound calling - and nothing here sends without a person's say-so.</p>
  </div>
</section>

<section>
  <div class="wrap section-pad section-center">
    <h2>What you can depute. What stays yours.</h2>
    <div class="depute-grid">
      <div class="depute-col">
        <div class="depute-col-title">Depute it</div>
        {"".join(f'<div class="depute-item"><span class="tick">&#10003;</span><span>{d}</span></div>' for d in depute_items)}
      </div>
      <div class="depute-col keep">
        <div class="depute-col-title">Keep it</div>
        {"".join(f'<div class="depute-item"><span class="dot">&#9679;</span><span>{k}</span></div>' for k in keep_items)}
      </div>
    </div>
    <p class="prose depute-close">That line - what's deputable and what isn't - is the whole company. It's why we're called what we're called. <a class="link-arrow" href="about.html">Why &ldquo;Deputable&rdquo; &rarr;</a></p>
    <div class="assure-strip">
      {"".join(f'<a class="assure-item" href="trust.html">{a}</a>' for a in assure_items)}
    </div>
  </div>
</section>

<section class="bg-white border-t">
  <div class="wrap split start">
    <div>
      <h2>No logo wall. Not yet.</h2>
      <p>We're a new company, and we won't decorate this page with invented numbers or testimonials we don't have. What we do have: a working product answering a live UK number, a build process you can audit at every stage, and a rule that you keep everything we make - the workflow, the documentation, the accounts it runs on.</p>
    </div>
    <div class="results-panel">
      <div class="mono-label">Pilot results - published as they complete</div>
      <p>This space is reserved for real measurements. When our first pilots finish, the before-and-after numbers go here - with the client's sign-off, and whether or not they flatter us.</p>
      <div class="pill-row">
        {"".join(f'<span class="pill">{m}</span>' for m in result_metrics)}
      </div>
    </div>
  </div>
</section>

<section class="border-t">
  <div class="wrap section-pad section-center">
    <h2 class="mb-lg">How It Works</h2>
    <div class="steps-grid">
      {"".join(f'<div class="step-item"><div class="meta">{n} &middot; {w}</div><h3>{t}</h3><p>{b}</p></div>' for n, w, t, b in home_steps)}
    </div>
  </div>
</section>
""" + cta_band("See it against your own process.", "Forty-five minutes, one workflow of your choosing, no deck.")

write_page("index.html", SITE_TITLE, SITE_DESC, "home", home_body)

# ==================================================================
# SERVICES
# ==================================================================
modes_full = [
    ("Out of hours", "Every call answered.",
     "When the office closes, the AI picks up - evenings, weekends and bank holidays. It answers the routine questions from your own business information, takes proper details with the caller's number confirmed digit by digit, and books callbacks so the morning starts with a list, not a voicemail backlog."),
    ("Office hours · overflow", "No caller lost to a busy line.",
     "When everyone is already on a call, the AI takes the next one instead of letting it ring out. It captures who's calling and why, answers what it safely can, and queues the rest for the right person - a busy hour stops costing you customers."),
    ("Live, during the call", "Your team, two steps ahead.",
     "While one of your people takes the call, the AI works for them, not instead of them - surfacing the caller's history, the job details and the next free slot as the conversation happens, so your operator can focus on the customer rather than the lookup."),
]

voice_caps = [
    "Answer frequently asked questions from your own business information",
    "Identify the caller and the reason for calling",
    "Book, change or cancel appointments",
    "Take messages and organise callbacks",
    "Qualify enquiries and capture lead details",
    "Route urgent or complex calls to the right person",
    "Send confirmations by email",
    "Log transcripts and summaries in your CRM",
]

workflow_pills = [
    "Route planning", "Inventory & stock reordering", "Job scheduling & dispatch",
    "Quotes & job paperwork", "Reporting",
]

discovery = [
    ("01", "Interview employees and map repetitive workflows."),
    ("02", "Measure volumes, labour time, delays and error rates."),
    ("03", "Assess data quality and existing systems."),
    ("04", "Rank opportunities by benefit, complexity and risk."),
    ("05", "Recommend a 60–90 day roadmap."),
    ("06", "Build one small, measurable pilot."),
]

services_body = f"""
<section class="border-b bg-white">
  <div class="wrap page-hero">
    <div class="eyebrow">Services</div>
    <h1 class="hw-narrow">An AI operations partner for UK small and mid-sized businesses.</h1>
    <p class="lede">Four services. Each one is on this page because we can deliver it today - nothing here is a roadmap.</p>
  </div>
</section>

<section id="smart-call-handling" class="bg-white border-b">
  <div class="wrap section-pad section-center">
    <div class="eyebrow">Flagship</div>
    <h2>Smart Call Handling</h2>
    <p class="prose section-sub">Your phone is where jobs are won and lost, and most small businesses lose them silently - after hours, on busy lines, in voicemail nobody checks. Smart Call Handling covers all three, without pretending to be a person and without taking anyone's place.</p>
    <div class="grid-3 mb-lg">
      {"".join(f'<div class="mode-card"><div class="mode-kicker">{k}</div><h3>{t}</h3><p>{b}</p></div>' for k, t, b in modes_full)}
    </div>
    <div class="split start no-pad">
      <div>
        <h3 class="list-title">What it handles on your line</h3>
        <div class="check-list">
          {"".join(f'<div class="check-item"><span class="tick">&#10003;</span><span>{c}</span></div>' for c in voice_caps)}
        </div>
      </div>
      <div class="panel-stack">
        <div class="panel">
          <h3>Safeguards, not optional extras</h3>
          <p>Callers are told they're speaking with an AI. There is always an easy route to a person. Recording and privacy notices are in place, and anything the system isn't confident about gets escalated, not improvised.</p>
        </div>
        <div class="panel">
          <h3>Inbound-first, by design</h3>
          <p>We answer the calls your customers make to you, and make only the follow-ups they've asked for - never cold outbound. It keeps us square with Ofcom's rules on automated calling, and keeps your number's reputation clean. <a href="https://www.ofcom.org.uk/phones-and-broadband/unwanted-calls-and-messages/refresher-messaging-on-silent-and-abandoned-calls" target="_blank" rel="noopener" class="link-arrow">Ofcom guidance &rarr;</a></p>
        </div>
      </div>
    </div>
  </div>
</section>

<section id="website-chat">
  <div class="wrap section-pad-sm">
    <h2 class="h2-md">Website Chat - the same engine, on your site.</h2>
    <p class="prose">The enquiry that starts in a chat box is the same enquiry that would have been a phone call, so we treat it the same way: answered from your business information, details captured, a callback arranged where it matters. One engine, one conversation history, no customer repeating themselves.</p>
  </div>
</section>

<section id="workflow-automation" class="bg-white border-t border-b">
  <div class="wrap section-pad-sm">
    <h2 class="h2-md">Workflow Automation - built around one process of yours.</h2>
    <p class="prose">No off-the-shelf packages, because your route planning, stock control and job paperwork don't run off the shelf either. We solve one core problem at a time, build the solution into the systems you already run - no new process for your team to adopt - and put an approval step wherever a mistake would reach a customer or a payment. When it's done, it's yours: keep us on a support contract if you want to, or take the handover and run it yourself.</p>
    <p class="prose">Where a workflow needs it, that includes an assistant grounded in your own documents - one that cites its source and says when it doesn't know.</p>
    <div class="pill-row">
      {"".join(f'<span class="pill pill-lg">{p}</span>' for p in workflow_pills)}
    </div>
    <div class="section-foot"><a class="link-arrow" href="index.html#flow">Watch a job run end to end &rarr;</a></div>
  </div>
</section>

<section id="readiness">
  <div class="wrap section-pad-sm">
    <div class="split start no-pad">
      <div>
        <h2 class="h2-md">AI Readiness Assessment - two weeks to a costed shortlist.</h2>
        <p class="prose">Most businesses don't need convincing that AI could help somewhere; they need to know where, what it would cost, and what it would save. Discovery is structured so the answer is specific.</p>
        <p class="prose small">A good first project is high-volume, rules-based, easy to review and capable of showing results within several weeks.</p>
      </div>
      <div class="numbered-list">
        {"".join(f'<div class="numbered-item"><span class="n">{n}</span><span class="t">{t}</span></div>' for n, t in discovery)}
      </div>
    </div>
  </div>
</section>

""" + cta_band("See it against your own process.", "Forty-five minutes, one workflow of your choosing, no deck.")

write_page(
    "services.html",
    "Services - Smart Call Handling, Website Chat & Workflow Automation | Deputable AI",
    "Three modes of Smart Call Handling, website chat on the same engine, bespoke workflow automation and a two-week AI readiness assessment. Nothing on this page is a roadmap.",
    "services", services_body)

# ==================================================================
# HOW IT WORKS
# ==================================================================
process_full = [
    ("01", "Week 0", "Demo Call", "A 45-minute conversation about one process you would like handled. We are direct about what AI does poorly, and will tell you if the answer is a spreadsheet fix rather than a model.", "A written view on whether to proceed, at no cost."),
    ("02", "Weeks 1–2", "Assessment", "We observe the work as it is actually done, not as the process document describes it. Volumes, exceptions, handoffs and the cost of each error are recorded.", "Costed shortlist of workflows ranked by payback, plus a risk note."),
    ("03", "Weeks 3–6", "Build and Pilot", "One workflow at a time. It runs alongside the existing process first, so you can compare outputs before anyone relies on it. Approval steps sit wherever a mistake would reach a customer.", "A working workflow in your environment, plus pilot results."),
    ("04", "Weeks 7–8", "Handover and Review", "Your team is trained to operate and adjust what we built. We measure time saved against the assessment estimate and share the numbers whether or not they flatter us.", "Documentation, trained staff, and a measured before-and-after."),
    ("05", "After week 8", "Ongoing Support (optional)", "If you want us to stay, we monitor the workflow, tune it as your business changes, and send a monthly report of what it handled and what it escalated. Priced separately, cancelled whenever you like - because the handover in week 8 was real, not a hostage arrangement.", "A support agreement with response times, monthly reporting, and the freedom to leave."),
]

process_body = f"""
<section class="border-b bg-white">
  <div class="wrap page-hero">
    <div class="eyebrow">How It Works</div>
    <h1 class="hw-narrow">Eight Weeks From First Call to Something Running in Production.</h1>
    <p class="lede">Every stage ends with a decision point. You can stop after any of them and keep what has been delivered.</p>
  </div>
</section>
<section>
  <div class="process-list">
    {"".join(f'''<div class="process-item">
      <div>
        <div class="n">{n}</div>
        <div class="when">{w}</div>
      </div>
      <div class="process-body">
        <h2>{t}</h2>
        <p>{b}</p>
        <div class="process-output"><strong>You get:</strong> {o}</div>
      </div>
    </div>''' for n, w, t, b, o in process_full)}
  </div>
</section>
""" + cta_band("Week 0 starts with a call.", "Bring one process. We'll tell you straight whether it's worth automating.")

write_page(
    "how-it-works.html",
    "How It Works - Eight Weeks to Production | Deputable AI",
    "Five steps: demo call, assessment, build and pilot, handover, optional ongoing support. A decision point at every stage - and you keep everything we deliver.",
    "process", process_body)

# ==================================================================
# ABOUT
# ==================================================================
team = [
    ("Rohit Sinha", "Founder", "https://www.linkedin.com/in/rohit-sinha-b6792715/", "Rohit has spent two decades getting change safely into production at Britain's biggest banks - cloud platform delivery, release management and observability at institutions where a bad deployment makes the news - most recently leading AI and Copilot adoption inside a major UK building society. Regulated environments taught him the rules Deputable now runs on: pilots that run alongside the existing process, evidence before reliance, and a named approver on anything that reaches a customer. Deputable exists because he'd watched too many automation programmes fail the same way - by removing people from processes that still needed them."),
    ("Prashant Tiwari", "Founder", "https://www.linkedin.com/in/prashanttiwari247/", "Prashant has spent his career building systems that aren't allowed to fail quietly - low-latency trading engines in an investment bank's front office, IoT fleets, a data platform parsing millions of records a day - and, most recently, AI systems that answer to evaluation gates rather than demos. At Deputable he leads how the work is scoped and built: one workflow at a time, integrated with the systems a client already runs, tested against real calls before it ships, and documented so the client's own team can maintain it afterwards. A co-organiser of PyData London for the last ten years, he started Deputable because the businesses that most need this help are the ones least able to gamble a year and a six-figure budget finding out whether it works."),
]

about_body = f"""
<section class="border-b bg-white">
  <div class="wrap page-hero">
    <div class="eyebrow">About</div>
    <div class="dict-entry">
      <span class="dict-word">deputable</span>
      <span class="dict-ipa">/d&#603;p&#712;ju&#720;t&#601;bl/</span>
      <span class="dict-pos">adjective</span>
      <span class="dict-def">able to be safely deputed; fit to be delegated.</span>
    </div>
    <p class="lede">We started with one question: which parts of a working day can you honestly hand to an AI - and which parts should never leave a person's hands? The company is named after the answer.</p>
  </div>
</section>

<section>
  <div class="wrap section-pad section-center">
    <h2>Some work is deputable. Some never will be.</h2>
    <p class="prose section-sub">A good deputy takes the routine off your desk and brings you the decisions. That's the standard we hold our AI to. It answers the phone at seven in the evening, takes the details down properly, checks the diary, chases the paperwork - and then it stops, because the next step belongs to a person.</p>
    <div class="depute-grid">
      <div class="depute-col">
        <div class="depute-col-title">Deputable</div>
        {"".join(f'<div class="depute-item"><span class="tick">&#10003;</span><span>{d}</span></div>' for d in depute_items)}
      </div>
      <div class="depute-col keep">
        <div class="depute-col-title">Not deputable</div>
        {"".join(f'<div class="depute-item"><span class="dot">&#9679;</span><span>{k}</span></div>' for k in keep_items)}
      </div>
    </div>
    <p class="prose depute-close">Our job is to empower and enable people - never to replace them. If a proposal of ours would quietly erase someone's judgment from a process, it's a bad proposal, and we'll tell you so.</p>
  </div>
</section>

<section class="bg-white border-t border-b">
  <div class="wrap split start">
    <div>
      <h2 class="h2-md">How we work</h2>
      <p class="prose">Every business operates differently, so we don't sell a one-size-fits-all product. We take the time to understand your processes, your systems and your day before building anything - then we deliver one working solution at a time, fitted to the tools you already run, documented so your own team can maintain it.</p>
      <p class="prose">Most of our thinking is shaped by service businesses that live and die by the phone - trades, clinics, property, logistics - but nothing about the approach is locked to an industry.</p>
    </div>
    <div class="mission-box">
      <div class="label">Our Mission</div>
      <p>Remove the operational friction from growing businesses. When AI manages the repetitive calls, enquiries and system updates, your team responds faster and spends its day on the work that actually creates value.</p>
    </div>
  </div>
</section>

<section>
  <div class="wrap section-pad-sm section-center">
    <h2 class="h2-md mb-lg">Founders</h2>
    <div class="grid-2 founder-grid">
      {"".join(f'''<div class="founder">
        <div class="name">{n}</div>
        <div class="role">{r}</div>
        <p>{b}</p>
        <a class="li-link" href="{li}" target="_blank" rel="noopener">LinkedIn &rarr;</a>
      </div>''' for n, r, li, b in team)}
    </div>
  </div>
</section>
"""

write_page(
    "about.html",
    "About - Why We're Called Deputable | Deputable AI",
    "Deputable: what you can safely hand to an AI, and what should stay with people. The thinking behind the name, and the founders behind the company.",
    "about", about_body)

# ==================================================================
# TRUST
# ==================================================================
trust = [
    ("Where is our data processed?", "In the UK or EU by default. Where a workflow requires a model hosted elsewhere, we say so in writing before deployment and you decide whether to proceed."),
    ("Do you train models on our data?", "No. Client data is used to serve that client only. We contract with providers on terms that exclude training on submitted data, and we can show you those terms."),
    ("Who can the system act on behalf of?", "Nothing that touches a customer, a payment or a record of account is sent without a named person approving it, unless you explicitly ask for an unattended step and accept that in writing."),
    ("What happens if the model gets it wrong?", "Every workflow logs its inputs, outputs and decisions so an error can be traced and reversed. Pilots run alongside the existing process precisely so failures surface before anyone depends on the output."),
    ("What if we end the engagement?", "You keep the workflow, the documentation and the accounts it runs on. We do not hold your integrations hostage, and there is no proprietary layer you have to keep paying us for."),
    ("Which other companies touch our data?", "The third-party services we use to run your workflow - for example the telephony provider and the model provider. We keep a current, named list of them for every client, with where each one processes data, and we work to UK GDPR throughout. Our data-processing terms are shared on request."),
]

deployment_includes = [
    "Callers and users are told when they're talking to an AI",
    "An easy route to a human, always",
    "A named person approves anything customer-facing",
    "Logs of every input, output and action",
    "A documented UK GDPR lawful basis and retention period",
    "A contractual bar on training models with your data",
]

trust_faq_jsonld = json.dumps({
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
        {"@type": "Question", "name": q,
         "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in trust
    ],
})

trust_body = f"""
<section class="border-b bg-white">
  <div class="wrap page-hero">
    <div class="eyebrow">Trust &amp; Security</div>
    <h1 class="hw-narrow">Your data is your own.</h1>
    <p class="lede">Where does it go, and who can act on it? The questions IT and procurement ask us first - answered plainly.</p>
  </div>
</section>
<section>
  <div class="trust-list">
    {"".join(f'<div class="trust-item"><h2>{q}</h2><p>{a}</p></div>' for q, a in trust)}
    <div class="trust-includes">
      <div class="mono-label">What every deployment includes</div>
      <div class="check-list check-list-lined">
        {"".join(f'<div class="check-item"><span class="tick">&#10003;</span><span>{d}</span></div>' for d in deployment_includes)}
      </div>
      <p class="prose small ico-note">The ICO publishes guidance on applying UK GDPR principles to AI systems; we work to it. <a class="link-arrow" href="https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/artificial-intelligence/" target="_blank" rel="noopener">ICO AI and data-protection guidance &rarr;</a></p>
    </div>
  </div>
</section>
""" + cta_band("Ask us the hard questions first.", "Bring your IT lead or your DPO to the demo call - we'd rather answer this before you commit than after.")

write_page(
    "trust.html",
    "Trust & Security - Your Data Is Your Own | Deputable AI",
    "Where your data is processed, who can act on it, and what happens when the model gets it wrong - the questions IT and procurement ask first, answered plainly.",
    "trust", trust_body,
    extra_head=f'\n<script type="application/ld+json">{trust_faq_jsonld}</script>')

# ==================================================================
# CONTACT
# ==================================================================
contact_body = f"""
<section class="bg-white contact-min">
  <div class="wrap contact-head">
    <div class="eyebrow">Book a Demo</div>
    <h1>Tell us what's eating the day.</h1>
    <p class="prose">Pick a 45-minute slot below. The booking asks for a line or two about the business and the process you'd like handled - so we arrive having read it. No deck, no pitch.</p>
  </div>
  <div class="wrap booking-wrap">
    {booking_html()}
  </div>
</section>
"""

write_page(
    "contact.html",
    "Book a Demo Call | Deputable AI",
    "Pick a 45-minute slot and tell us the process that wastes the most time. No deck, no pitch - we arrive having read what you wrote.",
    "contact", contact_body)

# ==================================================================
# PRIVACY
# ==================================================================
privacy_sections = [
    ("Who we are", "Deputable AI, based in London. We build AI call handling and workflow automation for businesses. For anything in this notice, write to <a href=\"mailto:hello@deputable.ai\">hello@deputable.ai</a>."),
    ("What we collect", "If you book a demo call, we collect what you type into the booking form - your name, company, contact details and the process you'd like to discuss. Booking is provided by Zoho Bookings and hosted in the EU; bookings are stored there and appear in our calendar. If you email us directly, we keep the correspondence."),
    ("Cookies and analytics", "This site sets no analytics cookies unless you accept them. If you accept, we use Google Analytics to understand how the site is used - page views and rough journey, not identity. Declining changes nothing about how the site works."),
    ("How we use it", "To reply to you, to prepare for the call you asked for, and to keep a record of the conversation. We do not sell or share your details for marketing, and we do not use them to train AI models."),
    ("Where it lives", "Bookings are processed by Zoho (EU hosting). If analytics are accepted, usage data is processed by Google. Client project data is governed separately by each client agreement - see our <a href=\"trust.html\">Trust &amp; Security</a> page."),
    ("Your rights", "Under UK GDPR you can ask what we hold about you, ask us to correct it, or ask us to delete it. Email <a href=\"mailto:hello@deputable.ai\">hello@deputable.ai</a> and we'll do it. If you're not satisfied, you can complain to the ICO."),
]

privacy_body = f"""
<section class="border-b bg-white">
  <div class="wrap page-hero">
    <div class="eyebrow">Privacy</div>
    <h1 class="hw-narrow">Privacy Notice.</h1>
    <p class="lede">What this website collects, why, and what you can do about it - in plain English.</p>
  </div>
</section>
<section>
  <div class="trust-list">
    {"".join(f'<div class="trust-item"><h2>{t}</h2><p>{b}</p></div>' for t, b in privacy_sections)}
  </div>
</section>
"""

write_page(
    "privacy.html",
    "Privacy Notice | Deputable AI",
    "What the deputable.ai website collects, why, and your rights under UK GDPR - in plain English.",
    "privacy", privacy_body)

# ==================================================================
# SITEMAP + LLMS.TXT (regenerated every run - cannot drift from pages)
# ==================================================================
today = datetime.date.today().isoformat()
urls = "\n".join(
    f"  <url><loc>{BASE_URL if fn == 'index.html' else BASE_URL + fn}</loc><lastmod>{today}</lastmod></url>"
    for fn, _, _ in WRITTEN
)
with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
    f.write(f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>
""")
print("Generated: sitemap.xml")

llms_pages = "\n".join(
    f"- [{title}]({BASE_URL if fn == 'index.html' else BASE_URL + fn}): {desc}"
    for fn, title, desc in WRITTEN
)
with open(os.path.join(OUT, "llms.txt"), "w") as f:
    f.write(f"""# Deputable AI

> {TAGLINE} Deputable AI builds Smart Call Handling and workflow automation
> for UK small and mid-sized businesses: AI that answers the phone out of
> hours, catches overflow calls during the day, briefs operators live
> during a call, and runs routine workflows (route planning, stock,
> job paperwork) integrated with a client's existing systems. A person
> stays accountable for every decision that matters. Solutions are
> delivered turn-key and handed over - clients own what we build, with
> ongoing support available as an optional service contract. No pricing
> is published; engagement starts with a 45-minute demo call.

## Pages
{llms_pages}
""")
print("Generated: llms.txt")

# ==================================================================
# /book - the permanent shareable booking link (deputable.ai/book).
# Everything printed or spoken points here (QR codes, cards, email
# signatures), so the target can change without breaking any of it.
# Not in the sitemap; noindex. Falls back to the contact page while
# no booking URL is configured.
# ==================================================================
book_target = ZOHO_BOOKINGS_URL or (BASE_URL + "contact.html")
os.makedirs(os.path.join(OUT, "book"), exist_ok=True)
with open(os.path.join(OUT, "book", "index.html"), "w") as f:
    f.write(f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex">
<meta http-equiv="refresh" content="0; url={book_target}">
<title>Book a demo call - Deputable AI</title>
<script>location.replace("{book_target}");</script>
</head>
<body>
<p>Taking you to the booking calendar&hellip;
<a href="{book_target}">Click here if nothing happens.</a></p>
</body>
</html>
""")
print("Generated: book/index.html")
