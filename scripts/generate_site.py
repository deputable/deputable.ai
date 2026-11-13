import datetime
import json
import os
import re

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
    ("platform.html", "platform", "Platform"),
    ("workflows.html", "workflows", "Workflows"),
    ("personal.html", "personal", "Personal"),
    ("features.html", "features", "Features"),
    ("how-it-works.html", "process", "Getting started"),
    ("trust.html", "trust", "Trust"),
    ("about.html", "about", "About"),
]

SITE_TITLE = "Deputable AI - Agentic workflows for small and mid-sized businesses"
SITE_DESC = ("Deputable runs your routine work as agentic workflows: a deputy and its squad of AI "
             "specialists answer, read, look things up, draft and follow up, fitted to how your business "
             "works. Nothing reaches a customer until a person says ok. Built and run in London.")

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

FONTS_URL = ("https://fonts.googleapis.com/css2?"
             "family=Bricolage+Grotesque:opsz,wght@12..96,400..800"
             "&family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400"
             "&family=IBM+Plex+Mono:wght@400;500;600&display=swap")

# Inline icons (24px grid, stroke follows the text colour).
_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
ICONS = {
    "phone": _SVG + '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>',
    "chat": _SVG + '<path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>',
    "text": _SVG + '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/><path d="M8 8.5h8M8 12h5"/></svg>',
    "page": _SVG + '<rect x="3" y="3" width="18" height="18" rx="2.5"/><path d="M3 9h18M9 21V9"/></svg>',
    "check": _SVG + '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg>',
    "silo": _SVG + '<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 1.66 3.58 3 8 3s8-1.34 8-3V5"/><path d="M4 12c0 1.66 3.58 3 8 3s8-1.34 8-3"/></svg>',
    "pin": _SVG + '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>',
    "lock": _SVG + '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>',
    "clock": _SVG + '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>',
    "user": _SVG + '<path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="8.5" cy="7" r="4"/><path d="m17 11 2 2 4-4"/></svg>',
    "send": _SVG + '<path d="M22 2 11 13"/><path d="M22 2 15 22l-4-9-9-4 20-7z"/></svg>',
    "file": _SVG + '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h6"/></svg>',
    "key": _SVG + '<circle cx="7.5" cy="15.5" r="4.5"/><path d="m10.7 12.3 9.8-9.8M17 6l3 3M14 9l2 2"/></svg>',
    "eye": _SVG + '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>',
    "pen": _SVG + '<path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>',
    "clip": _SVG + '<rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 4V3h6v1M9 13l2 2 4-4"/></svg>',
}


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
<meta name="theme-color" content="#04285E">
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
<link href="{FONTS_URL}" rel="stylesheet">
<link rel="stylesheet" href="{relpath_prefix}css/style.css?v={CSS_VER}">
<script type="application/ld+json">{ORG_JSONLD}</script>{extra_head}{ga}
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<div class="page-shell">
{header(active_id, relpath_prefix)}
<main id="main">
"""


def header(active_id, relpath_prefix=""):
    links = []
    for href, pid, label in NAV_ITEMS:
        if pid == active_id:
            links.append(f'<a class="nav-link active" aria-current="page" href="{relpath_prefix}{href}">{label}</a>')
        else:
            links.append(f'<a class="nav-link" href="{relpath_prefix}{href}">{label}</a>')
    nav_links = "\n        ".join(links)
    home_href = relpath_prefix + "index.html" if relpath_prefix else "index.html"
    return f"""  <header class="site-header">
    <div class="wrap header-inner">
      <a class="logo-link" href="{home_href}">
        <img src="{relpath_prefix}assets/deputable-logo.png?v={ASSET_VER}" alt="Deputable AI - {TAGLINE}" width="231" height="60">
      </a>
      <button class="mobile-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
      <nav class="main-nav" id="site-nav" aria-label="Main">
        {nav_links}
        <a class="btn-nav" href="{relpath_prefix}contact.html">Book a demo</a>
      </nav>
    </div>
  </header>"""


FOOTER_PRODUCT = [
    ("platform.html", "The platform"),
    ("workflows.html", "Workflows"),
    ("platform.html#smart-call-handling", "Smart Call Handling"),
    ("personal.html", "A deputy of your own"),
    ("features.html", "Everything it does"),
    ("how-it-works.html", "Getting started"),
]
FOOTER_COMPANY = [
    ("about.html", "About"),
    ("trust.html", "Trust &amp; Security"),
    ("privacy.html", "Privacy"),
]


def footer(relpath_prefix=""):
    def col(items):
        return "\n          ".join(f'<a href="{relpath_prefix}{href}">{label}</a>' for href, label in items)
    return f"""  <footer class="site-footer">
    <div class="wrap footer-top">
      <div class="footer-brand">
        <img src="{relpath_prefix}assets/deputable-logo.png?v={ASSET_VER}" alt="Deputable AI - {TAGLINE}" width="200" height="52">
        <p>Agentic workflows for small and mid-sized businesses, fitted to how each one works. Built and run from London, with a person in charge of every decision that matters.</p>
      </div>
      <div class="footer-col">
        <div class="footer-col-title">Product</div>
        <div class="footer-nav">
          {col(FOOTER_PRODUCT)}
        </div>
      </div>
      <div class="footer-col">
        <div class="footer-col-title">Company</div>
        <div class="footer-nav">
          {col(FOOTER_COMPANY)}
        </div>
      </div>
      <div class="footer-col">
        <div class="footer-col-title">Contact</div>
        <div class="footer-nav">
          <a href="mailto:hello@deputable.ai">hello@deputable.ai</a>
          <a href="{relpath_prefix}contact.html">Book a demo call</a>
          <span>London, UK</span>
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


def write_redirect(relpath, target, title):
    """A permanent link that forwards somewhere else: noindex, meta
    refresh plus a script, with a plain link as the fallback."""
    full = os.path.join(OUT, relpath)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex">
<meta http-equiv="refresh" content="0; url={target}">
<title>{title}</title>
<script>location.replace("{target}");</script>
</head>
<body>
<p>Taking you there&hellip;
<a href="{target}">Click here if nothing happens.</a></p>
</body>
</html>
""")
    print(f"Generated: {relpath}")


# ------------------------------------------------------------------
# Small building blocks
# ------------------------------------------------------------------
STATUS_LABEL = {"live": "Live", "built": "Built", "next": "Next"}


def status(s):
    """The three honest states. live: running in production and used on
    real calls or messages. built: built and tested, switched on with
    the first clients. next: agreed and drawn, not built."""
    cls = "status" if s == "live" else f"status {s}"
    return f'<span class="{cls}">{STATUS_LABEL[s]}</span>'


def sec_head(kicker, title, sub="", you=False, center=False, level="h2"):
    k_cls = "kicker you" if you else "kicker"
    h_cls = "sec-head center" if center else "sec-head"
    sub_html = f'\n      <p class="sub">{sub}</p>' if sub else ""
    kick = f'<div class="{k_cls}">{kicker}</div>\n      ' if kicker else ""
    return f"""<div class="{h_cls}">
      {kick}<{level}>{title}</{level}>{sub_html}
    </div>"""


def ticks(items, cls=""):
    c = f"ticks {cls}".strip()
    lis = "".join(f"<li>{i}</li>" for i in items)
    return f'<ul class="{c}">{lis}</ul>'


def cta_band(title, sub, label="Book a demo call"):
    return f"""
<section class="cta">
  <div class="wrap cta-inner">
    <div>
      <h2>{title}</h2>
      <p>{sub}</p>
    </div>
    <a class="btn btn-coral" href="contact.html">{label} <span class="arr" aria-hidden="true">&rarr;</span></a>
  </div>
</section>
"""


def page_hero(kicker, title, lede, ctas=""):
    return f"""
<section class="page-hero">
  <div class="wrap">
    <div class="kicker">{kicker}</div>
    <h1>{title}</h1>
    <p class="lede">{lede}</p>{ctas}
  </div>
</section>
"""


def booking_html():
    """One-form booking: the Zoho Bookings calendar embedded directly.
    Its booking form collects everything (name, email, phone, company,
    the process to discuss), so there is no separate enquiry form.
    The portal-embed variant is Zoho's frameable URL; the public page
    sends X-Frame-Options and is used for the new-tab link only."""
    if not ZOHO_BOOKINGS_URL:
        return """
    <div class="booking-fallback">
      <p class="prose">Write to <a href="mailto:hello@deputable.ai">hello@deputable.ai</a> with a line about the business and the process you'd like handled, and we'll ring you back, usually within one working day.</p>
    </div>"""
    embed_src = ZOHO_BOOKINGS_EMBED_URL or ZOHO_BOOKINGS_URL
    return f"""
    <iframe class="booking-embed" src="{embed_src}" title="Book a 45-minute demo call" frameborder="0"></iframe>
    <p class="prose small booking-foot">Prefer a new tab? <a class="link-arrow" href="{ZOHO_BOOKINGS_URL}" target="_blank" rel="noopener">Open the calendar&nbsp;&rarr;</a></p>"""


# ------------------------------------------------------------------
# Who does a step. The platform draws every workflow as a chart whose
# steps are coloured by who does each one (its Workflows pages), and the
# site draws them the same way, so a visitor sees the product's own
# picture of the work:
#   trigger = what starts it       code   = plain code, no AI
#   model   = an AI model reads or drafts
#   person  = one of the client's people decides
#   missing = a part the deputy does not have yet ("Not yet")
# The words under each step are the platform's own wherever it has them
# (the `Flow` declarations and `of_mail_rule` in service/workflows.py).
# ------------------------------------------------------------------
WHO = {"trigger": "Starts it", "code": "Code", "model": "Model", "person": "You", "missing": "Not yet"}


def who_key(kinds=("trigger", "code", "model", "person")):
    words = {"trigger": "Starts it", "code": "Plain code", "model": "An AI model", "person": "A person",
             "missing": "A part it lacks"}
    return '<div class="whokey">' + "".join(
        f'<span><i class="{k}"></i>{words[k]}</span>' for k in kinds) + "</div>"


def chart(steps):
    """A workflow drawn left to right. `steps`: (who, what) or
    (who, what, label) where label replaces the who word."""
    out = []
    for i, step in enumerate(steps):
        who, what = step[0], step[1]
        label = step[2] if len(step) > 2 else WHO[who]
        if i:
            out.append('<span class="arr" aria-hidden="true">&rarr;</span>')
        out.append(f'<div class="node {who}"><span class="who">{label}</span><span class="what">{what}</span></div>')
    return '<div class="chart">' + "".join(out) + "</div>"


def strip(steps):
    """The same steps as a compact strip, for a list of workflows."""
    return '<ol class="strip">' + "".join(
        f'<li class="{who}"><span class="who">{WHO[who]}</span>{what}</li>' for who, what in steps) + "</ol>"


def _msg(kind, body, at="", who="", plain=False):
    cls = f"msg {kind}" + (" plain" if plain else "")
    at_html = f'<span class="at">{at}</span>' if at else ""
    who_html = f'<span class="who"><span>{who}</span>{at_html}</span>' if (who or at) else ""
    return f'<div class="{cls}" data-rv>{who_html}{body}</div>'


# ------------------------------------------------------------------
# The run demo (homepage hero): four workflows, each started a
# different way, shown as the steps the platform runs and then what the
# person sees on their phone. Everything is in the HTML from the start,
# so the page reads without JavaScript; js/main.js only lights the
# steps in turn and switches the tabs.
# ------------------------------------------------------------------
RUNS = [
    {
        "tab": "A call", "name": "Estimate from a call", "via": "A garage",
        "steps": [
            ("trigger", "A registration and a fault arrive, by call or WhatsApp"),
            ("model", "The vehicle identified and the repair named"),
            ("model", "The parts it needs, with live offers"),
            ("code", "Labour, parts and VAT added up and checked against the records"),
            ("person", "Staff approve it before the customer hears a figure"),
        ],
        "phone": [
            _msg("deputy", "Draft estimate <b>P14 v1</b>: BMW 320d, front brakes, <b>&pound;343.68</b>. Reply <code>ok P14</code>, <code>drop P14</code>, or say what to change.", "10:48", "Waiting for you"),
            _msg("you", "ok P14", "10:52", "You"),
        ],
    },
    {
        "tab": "A photo", "name": "A document is read and kept", "via": "Any business",
        "steps": [
            ("trigger", "A photo, PDF or file arrives on WhatsApp"),
            ("model", "Read, and its kind named: an invoice, a receipt, a letter"),
            ("code", "Kept in the record. An invoice waits for your ok, never paid"),
            ("person", "You correct what it was unsure of, then ok it"),
            ("code", "One row in the ledger"),
        ],
        "phone": [
            _msg("deputy", "Supplier invoice: Brightwell Plumbing, <b>&pound;153.00</b>, due 22 October. Kept as <b>S1</b>. Reply <code>ok S1</code> to keep it as a bill.", "09:14", "Waiting for you"),
            _msg("you", "ok S1", "09:15", "You"),
        ],
    },
    {
        "tab": "An email", "name": "Timesheets by email: the month's invoice", "via": "A contractor",
        "steps": [
            ("trigger", "An email from your client arrives, and the sender is confirmed"),
            ("code", "Its screenshots, each read as a timesheet"),
            ("model", "The month's invoice drafted on last month's"),
            ("code", "Days and totals added up. Word file and PDF saved to your Drive"),
            ("person", "You check the figures and send it"),
        ],
        "phone": [
            _msg("deputy", "October's invoice is drafted: 21 days. The PDF is in your Drive and the email is in your drafts, <b>not sent</b>.", "17:31", "Waiting for you"),
            _msg("you", "send", "17:40", "You"),
        ],
    },
    {
        "tab": "A schedule", "name": "Mail that can't wait", "via": "One person",
        "steps": [
            ("trigger", "Every 30 minutes"),
            ("code", "New mail is checked for. Nothing new, nothing runs"),
            ("model", "Only when something changed: can it wait?"),
            ("person", "Told on your phone when there is something to say"),
        ],
        "phone": [
            _msg("deputy", "From the venue, 14:02: they need final numbers for Thursday by 5pm today.", "14:05", "Can't wait"),
            _msg("you", "Draft a reply: 120 of us", "14:07", "You", plain=True),
        ],
    },
]


def run_demo():
    tabs = "".join(
        f'<button type="button" class="demo-tab" role="tab" id="run-tab-{i}" aria-controls="run-panel-{i}" '
        f'aria-selected="{"true" if i == 0 else "false"}" data-demo-tab="{i}">{r["tab"]}</button>'
        for i, r in enumerate(RUNS)
    )
    panels = ""
    for i, r in enumerate(RUNS):
        steps = "".join(
            f'<li class="rstep {who}" data-rv><span class="who">{WHO[who]}</span><span class="what">{what}</span></li>'
            for who, what in r["steps"])
        panels += (
            f'<div class="run-panel{" is-active" if i == 0 else ""}" role="tabpanel" id="run-panel-{i}" '
            f'aria-labelledby="run-tab-{i}" data-demo-panel data-name="{r["name"]}" data-via="{r["via"]}">'
            f'<ol class="run-steps">{steps}</ol>'
            f'<div class="run-phone"><div class="run-phone-label">On your phone</div>{"".join(r["phone"])}</div>'
            "</div>")
    first = RUNS[0]
    return f"""<div class="demo" data-demo="auto">
      <div class="demo-label">It starts with</div>
      <div class="demo-tabs" role="tablist" aria-label="Four workflows, each started a different way">{tabs}</div>
      <div class="runcard">
        <div class="run-head">
          <div>
            <div class="run-kicker">Workflow</div>
            <div class="run-name" data-demo-name>{first["name"]}</div>
          </div>
          <div class="run-via" data-demo-via>{first["via"]}</div>
        </div>
        <div class="run-panels">{panels}</div>
      </div>
      <p class="demo-caption">Real workflows, drawn as the platform draws them. The people and figures are made up.</p>
    </div>"""


# ------------------------------------------------------------------
# The catalogue: workflows that exist today, as the platform lists them
# (one row each: what starts it, the steps, who does each). The id is
# the feature's in the Deputy repo's docs/features.md; the status must
# match that list (see FEATURES below).
# ------------------------------------------------------------------
STARTS = ["A call", "A document", "An email", "A time", "Something happens", "You ask"]

CATALOGUE = [
    ("REC-14", "Estimate from a call or a message", "A call", "live", "Garages", [
        ("trigger", "A registration and a fault arrive"),
        ("model", "The vehicle identified and the repair named"),
        ("model", "The parts it needs, with live offers"),
        ("code", "Totals and VAT added up and checked"),
        ("person", "Staff approve it before the customer hears a figure")]),
    ("REC-15", "Property search on the call", "A call", "live", "Estate agents", [
        ("trigger", "A caller asks what is for sale or to rent"),
        ("code", "The agency's own live listings searched"),
        ("model", "The matches read back, the lead taken"),
        ("person", "Staff ring back")]),
    ("REC-02", "The note after every contact", "A call", "live", "Any business", [
        ("trigger", "A call ends, or a message thread goes quiet"),
        ("code", "Every action taken is listed from the record"),
        ("model", "Summary, open items, promises, the lead"),
        ("code", "Checked complete, then sent to the owner's phone")]),
    ("REC-04", "Call backs owed", "Something happens", "live", "Any business", [
        ("trigger", "A call back is promised"),
        ("code", "Raised as an item due at your next opening"),
        ("person", "Someone makes the call and closes it")]),
    ("REC-03", "The text to your customer", "Something happens", "live", "Any business", [
        ("trigger", "A message is taken"),
        ("code", "Only if the caller said yes to a text"),
        ("code", "One text with what was agreed, never twice")]),
    ("DOC-01", "A document sent in is read and kept", "A document", "built", "Any business", [
        ("trigger", "A photo, PDF or file arrives"),
        ("model", "Read, and its kind named"),
        ("code", "Kept in the record"),
        ("person", "An invoice waits for your ok, never paid")]),
    ("COMP-26", "Meeting follow-ups", "A document", "built", "Any business", [
        ("trigger", "A recording arrives"),
        ("code", "Transcribed, each speaker named"),
        ("model", "Summary, decisions, who owes what by when"),
        ("person", "You approve each follow-up before anyone hears of it")]),
    ("DOC-01b", "Timesheets by email: the month's invoice", "An email", "live", "Contractors", [
        ("trigger", "An email from your client, sender confirmed"),
        ("code", "Its screenshots, each read as a timesheet"),
        ("model", "The month's invoice drafted on last month's"),
        ("person", "You check the figures and send it")]),
    ("COMP-04", "Mail that can't wait", "A time", "live", "One person", [
        ("trigger", "Every 30 minutes"),
        ("code", "New mail checked for. Nothing new, nothing runs"),
        ("model", "Only when something changed: can it wait?"),
        ("person", "Told on your phone when there is something to say")]),
    ("COMP-05", "Diary clashes", "A time", "built", "One person", [
        ("trigger", "Every hour"),
        ("code", "Every calendar read and compared"),
        ("person", "Each new overlap said once, on your phone")]),
    ("COMP-18", "The morning summary", "A time", "built", "One person", [
        ("trigger", "07:30 every day"),
        ("model", "Diaries, mail that needs you, reminders, what waits"),
        ("code", "Emailed once, from your deputy's mailbox")]),
    ("COMP-08", "Reminders", "A time", "live", "One person", [
        ("trigger", "The time you set"),
        ("code", "A text, or a call. No AI model involved")]),
    ("COMP-13", "A call made from a brief", "You ask", "built", "One person", [
        ("trigger", "You ask it to ring someone"),
        ("model", "A brief drafted: who, what to say, what it may agree"),
        ("person", "You approve the brief"),
        ("code", "It rings inside calling hours, with one retry"),
        ("model", "The outcome read against the brief and told to you")]),
    ("COMP-24", "A voice note, heard and answered", "You ask", "built", "Any business", [
        ("trigger", "A voice note arrives on WhatsApp"),
        ("code", "Transcribed"),
        ("model", "Answered as a text would be")]),
    ("COMP-14", "What a call owed, settled", "A call", "built", "One person", [
        ("trigger", "A call ends"),
        ("code", "What was promised is compared with what was done"),
        ("model", "What it can do itself, it does"),
        ("person", "The rest waits on your word")]),
]


def catalogue_html():
    rows = "".join(
        f'<div class="wfrow" data-id="{fid}"><div class="wf-main"><h3>{name}</h3>'
        f'<div class="wf-meta"><span class="starts">{starts}</span><span class="for">{who}</span></div></div>'
        f'{strip(steps)}<div class="wf-status">{status(st)}</div></div>'
        for fid, name, starts, st, who, steps in CATALOGUE)
    return f'<div class="wflist">{rows}</div>'


# ------------------------------------------------------------------
# A workflow from a description: the platform's own Add page, with its
# own wording ("We'd call it", "In your words", "What it lacks", the
# buttons) and its own two test cases (tests/test_workflows.py in the
# Deputy repo). The first is built at once from parts the deputy has;
# the second needs two parts it lacks, which become one request to us.
# ------------------------------------------------------------------
DRAFTS = [
    {
        "tab": "Simple: built at once",
        "words": "When a message is taken, tell Sam and raise a call back for his ok.",
        "name": "Messages to Sam, with a call back",
        "tag": ("ok", "Built from parts it has"),
        "steps": [
            ("trigger", "A message is taken"),
            ("code", "Tells Sam: who rang and what they wanted"),
            ("person", "Raises a call back for someone's ok"),
        ],
        "lacks": [],
        "acts": [("go", "Turn it on")],
        "foot": "Texts to customers go only in the words written here. The model reads and never picks who is told or what is sent.",
    },
    {
        "tab": "Bigger: needs a part it lacks",
        "words": "Every weekday at nine, look up MOT dates at the DVLA, text me, and ring anyone who does not reply.",
        "name": "MOT reminders with the DVLA",
        "tag": ("warn", "Needs Deputable"),
        "steps": [
            ("trigger", "09:00 on weekdays"),
            ("missing", "Look up the MOT date at the DVLA", "Not yet &middot; a tool"),
            ("code", "Tells you: MOT reminders went out"),
            ("missing", "Ring anyone who does not reply", "Not yet &middot; a specialist"),
        ],
        "lacks": ["A tool: look up the MOT date at the DVLA", "A specialist: ring anyone who does not reply"],
        "acts": [("go", "Turn on what it has"), ("warn", "Send the request")],
        "foot": "The parts it has can go on today. The rest becomes one request to Deputable, with your words and the drawing attached.",
    },
]


def draft_demo():
    tabs = "".join(
        f'<button type="button" class="demo-tab" role="tab" id="draft-tab-{i}" aria-controls="draft-panel-{i}" '
        f'aria-selected="{"true" if i == 0 else "false"}" data-demo-tab="{i}">{d["tab"]}</button>'
        for i, d in enumerate(DRAFTS))
    panels = ""
    for i, d in enumerate(DRAFTS):
        tone, tag = d["tag"]
        lacks = ""
        if d["lacks"]:
            lacks = ('<div class="draft-lacks"><div class="draft-k">What it lacks</div><ul>'
                     + "".join(f"<li>{x}</li>" for x in d["lacks"]) + "</ul></div>")
        acts = "".join(f'<span class="draft-btn {t}">{label}</span>' for t, label in d["acts"])
        panels += f"""<div class="draft-panel{" is-active" if i == 0 else ""}" role="tabpanel" id="draft-panel-{i}" aria-labelledby="draft-tab-{i}" data-demo-panel>
          <div class="draft-k">In your words</div>
          <p class="draft-words">{d["words"]}</p>
          <div class="draft-named"><span class="draft-k">We'd call it</span><span class="draft-name">{d["name"]}</span><span class="draft-tag {tone}">{tag}</span></div>
          {chart(d["steps"])}
          {lacks}
          <div class="draft-acts">{acts}</div>
          <p class="draft-foot">{d["foot"]}</p>
        </div>"""
    return f"""<div class="demo draft" data-demo>
      <div class="demo-tabs" role="tablist" aria-label="Two workflows written in words">{tabs}</div>
      <div class="draftcard">
        <div class="draft-bar"><span>Workflows</span><span aria-hidden="true">&middot;</span><span>Add</span><span aria-hidden="true">&middot;</span><span>drawn from your words</span></div>
        <div class="draft-panels">{panels}</div>
      </div>
    </div>"""


# What a business can build for itself today: the platform's closed
# parts catalogue (config/workflow_parts.yaml in the Deputy repo).
PARTS_STARTS = [
    ("At a time", "Every day, on weekdays, or every hour."),
    ("When something happens", "A message is taken, a call ends, a voicemail is left, a document is read, a draft is approved, two diary entries overlap, a send fails."),
    ("When an email arrives", "From a sender you name, with timesheets attached."),
]
PARTS_STEPS = [
    ("code", "Tell one of your people", "In the words you wrote, with the details filled in."),
    ("person", "Raise work for someone's ok", "A call back, a promise, a draft: it waits for a person."),
    ("code", "Text the customer", "Only in the words you wrote, only about the customer it concerns."),
]
# The four kinds of part it will not build from words (`missing:` in the
# same file), and the path a request takes (requisitions.STEPS).
PARTS_MISSING = [
    ("A new tool", "A site, an API or a lookup your deputy has no way into yet."),
    ("A new specialist", "A member of the squad with its own access to one of your systems."),
    ("A new kind of document", "Paperwork it cannot read yet."),
    ("Anything that pays or signs", "Never built from words. Built with you, with a person approving each one."),
]
REQUEST_STEPS = ["You asked", "Deputable is reviewing", "A decision and a price, if any", "Built and tested", "On your deputy"]

# Why the line is drawn there. Each of these is how the platform is
# built, not a promise: see docs/workflows.md ("Invariants held") and
# docs/learning.md ("Invariants this keeps") in the Deputy repo.
PRINCIPLES = [
    ("Your deputy never writes its own code.",
     "A workflow you describe is assembled only from parts that already exist and have been tested. It cannot do something nobody has checked."),
    ("The drawing is the agreement.",
     "It draws exactly what it will do and who does each step. You change the words and it redraws. Turning it on builds what the drawing shows and nothing else."),
    ("A model may read. It may not send.",
     "Every message, and every change to a record, is plain code or a person. A text to a customer goes in the exact words you wrote; the model never picks who is told or what is said."),
    ("Money is never built from words.",
     "Anything that pays, signs or moves money is built with you by people, with an approval on every one."),
    ("New parts are built once, by people.",
     "A tool your deputy lacks is reviewed, built with its tests and signed by one of us before it runs. The next business that needs it gets it from the shelf."),
    ("Every version is kept.",
     "Pause a workflow, remove it, restore it. What it was on any day is in your record."),
]

# The ladder (docs/learning.md, "Five kinds of proposal, on one ladder"):
# the deputy always proposes the lowest rung that does the job.
LADDER = [
    ("you", "A lesson", "A habit in how something is written or done.", "The person it came from"),
    ("you", "A rule", "A line your whole deputy holds, on every call and every job.", "The business owner"),
    ("you", "A skill", "A known sequence of steps over tools it already has, dry-run in front of you first.", "You"),
    ("us", "A new tool", "A way into a system it cannot reach yet.", "Deputable builds and signs"),
    ("us", "A new specialist", "A new member of the squad with its own access.", "Deputable builds and signs"),
]


def ladder_html():
    rungs = "".join(
        f'<li class="rung {side}"><span class="rung-n">0{i}</span><div><h3>{name}</h3><p>{what}</p>'
        f'<span class="rung-by">{by}</span></div></li>'
        for i, (side, name, what, by) in enumerate(LADDER, 1))
    return f"""<ol class="ladder">{rungs}</ol>
    <div class="ladder-key"><span class="you">Rungs 1 to 3: you approve, and it takes effect on the next job</span><span class="us">Rungs 4 and 5: we build, test and sign</span></div>"""


# The shelf: the specialists a squad is assembled from, with what each
# can do and what it works with (src/deputy/members/ in the Deputy
# repo). Plain names here; the platform's own role names stay internal.
SHELF = [
    ("Mail and diary", "Finds and reads mail, drafts replies, sends on a yes. Reads every calendar, blocks time, sends invitations.", "Gmail, Google Calendar, Zoho, calendar feeds"),
    ("Parts and pricing", "Identifies the vehicle, names the repair, finds the parts and live offers, totals it with VAT.", "eBay, your own records"),
    ("Property", "Searches an agency's own live listings and reads the matches back.", "The agency's website"),
    ("Invoicing", "Drafts the month's invoice from timesheets, on last month's as the template.", "Gmail, Google Drive"),
    ("Research", "Searches the web and reads a page in parts.", "Brave Search"),
    ("Journeys", "Public transport in London with real times. Drives in traffic, and when to leave.", "TfL, Google Routes"),
    ("Documents", "Reads photos, PDFs and letters, names what each is, finds them again by name.", "Your deputy's own record"),
    ("Reminders", "A text, or a call, at the time you set.", "Text and phone"),
    ("Lists and facts", "Lists, &ldquo;remember that&rdquo;, and what it is told to forget.", "Your deputy's own record"),
    ("Calls out", "Puts you through to someone, or drafts a brief for a call it makes itself.", "Phone"),
    ("Decks", "Builds slides from an outline you agree, and emails them to you.", "Email"),
]


# Shared by the homepage and About page - keep the two in step.
depute_items = [
    "Drafting estimates, replies and invoices",
    "Reading and sorting the photos and PDFs you send",
    "Writing up every call and every message",
    "Keeping track of every call back you owe",
    "Watching the mail and the diary for what can't wait",
    "Answering the phone out of hours and on a busy line",
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
    "Your data leaves with you if you do",
]

result_metrics = ["Calls answered", "Response time", "Hours saved", "Error rate"]

# Four rules held in the platform's code, each with its own automated
# test (see the Deputy repo's invariants). Do not add a fifth here
# unless a test holds it.
GUARANTEES = [
    ("A named person approves it.", "Anything a customer will see waits at review until one of your people says ok."),
    ("Your ok covers what you read.", "Change anything and it comes back as a new version, to be approved again."),
    ("Every message goes once.", "If we can't tell whether one was delivered, a person decides before it is tried again."),
    ("Outside text can't give orders.", "A caller's words or an email can inform a draft. They can never make your deputy send or change anything."),
]


def guarantees_html():
    rows = "".join(
        f'<div class="guarantee"><div class="n">0{i}</div><div><h3>{t}</h3><p>{b}</p></div></div>'
        for i, (t, b) in enumerate(GUARANTEES, 1)
    )
    return f"""<div class="guarantees">{rows}</div>
        <p class="code-note">{ICONS["check"]}<span>These four are rules in the code, each held by its own automated test. They are not instructions we hope a model follows.</span></p>"""


# ==================================================================
# HOME
# ==================================================================
# The six ways a workflow starts, in the platform's own words (STARTS in
# service/workflows.py).
anatomy_starts = [
    ("A call", "A customer rings your business"),
    ("A document", "A photo, a PDF, a recording"),
    ("An email", "From a sender you name"),
    ("A time", "Every morning, every half hour"),
    ("Something happens", "A message is taken, a draft approved"),
    ("You ask", "By voice, WhatsApp or text"),
]
anatomy_ends = [
    ("person", "A draft, waiting for your ok"),
    ("code", "A message, sent once"),
    ("code", "A record, kept"),
    ("code", "One of your people, told"),
]

kinds = [
    ("Answer", "The phone out of hours and on a busy line, WhatsApp messages, voice notes. In your business's name, from your own facts and rules."),
    ("Write up", "A note after every contact: who it was, what they wanted, what was promised. The text to your customer. The call back you now owe."),
    ("Read", "Photos, PDFs, letters, timesheets, recordings and your inbox. Sorted, the figures pulled out, and what it was unsure of said plainly."),
    ("Look up", "Your own listings and records, parts and live prices, every diary you keep, journeys, the web."),
    ("Draft", "Estimates, invoices, replies and decks, with the arithmetic done in code. Yours to check, change and send."),
    ("Chase and watch", "Reminders, mail that can't wait, diary clashes, meeting follow-ups, a call made for you from a brief you approved."),
]

# Three deputies as they are assembled today: the squad, the workflows
# switched on, and the decision that stays with a person.
fits = [
    ("A garage", ["Parts and pricing"],
     ["The note after every call", "Call backs owed", "An estimate from a call"],
     "The owner approves every estimate. Nobody is quoted on the phone."),
    ("An estate agency", ["Property"],
     ["Listings searched on the call", "A card to staff for every message", "A text listing the properties read out"],
     "Staff ring back every lead."),
    ("A contractor", ["Mail and diary", "Invoicing", "Reminders", "Research"],
     ["The month's invoice from timesheets", "Mail that can't wait", "Diary clashes", "The morning summary"],
     "You check the figures and send it."),
]


def fits_html():
    out = ""
    for name, squad, flows, decides in fits:
        out += (
            f'<div class="fit"><h3>{name}</h3>'
            '<div class="fit-k">Its squad</div><div class="pill-row">'
            + "".join(f'<span class="pill">{s}</span>' for s in squad) + "</div>"
            '<div class="fit-k">Its workflows</div>' + ticks(flows)
            + f'<div class="fit-decides"><span class="fit-k">Stays with a person</span>{decides}</div></div>')
    return out


four_things = [
    ("Its facts", "Your hours, services, people and who may approve what."),
    ("Its rules", "Plain sentences in your own words: &ldquo;never give a price on the phone&rdquo;."),
    ("Its squad", "The specialists your work needs, picked from the shelf or built for you."),
    ("Its workflows", "The pieces of routine work it runs, each one drawn before it is built."),
]

facts_home = [
    ("silo", "Tenant isolation", "A dedicated data silo for every client: its own directory and its own database."),
    ("pin", "UK data residency", "Stored in Oracle Cloud's London region, encrypted at rest. Backups stay in London."),
    ("lock", "Encrypted backups", "Taken hourly and encrypted with a key our servers never hold. Restores are rehearsed."),
    ("eye", "Access on your terms", "You set what Deputable staff can see: none, limited, or full with a reason and an end date."),
    ("clock", "Export and erasure", "Your data exports in full, and one person's data is erased on request."),
    ("pen", "Signed releases", "Production runs only software we have cryptographically signed."),
]

home_body = f"""
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <div class="eyebrow">Agentic workflows for small and mid-sized businesses</div>
      <h1 class="hero-title"><span>Delegate the busywork.</span> <span>Own the <span class="yours">decisions.</span></span></h1>
      <p class="hero-sub">Deputable runs your routine work as workflows: a deputy and its squad of AI specialists that answer, read, look things up, draft and follow up. Fitted to how your business works. Nothing reaches a customer until you say ok.</p>
      <div class="hero-ctas">
        <a class="btn btn-primary" href="contact.html">Book a demo call <span class="arr" aria-hidden="true">&rarr;</span></a>
        <a class="btn btn-secondary" href="workflows.html">See the workflows</a>
      </div>
      <div class="hero-foot">
        <span>Phone, WhatsApp, email and paperwork</span>
        <span class="you">A person approves what customers see</span>
        <span>Built and run in London</span>
      </div>
    </div>
    {run_demo()}
  </div>
</section>

<section class="sec" id="what">
  <div class="wrap">
    {sec_head("What it is", "A deputy, a squad, and the workflows that put them to work.", "One deputy speaks for your business. Behind it sits a squad of specialists, each with its own tools. A piece of routine work is a workflow: something starts it, the squad does the steps, and it stops where a person should decide.")}
    <div class="anatomy">
      <div class="an-col">
        <div class="an-title">It starts with</div>
        {"".join(f'<div class="an-item"><b>{t}</b><span>{b}</span></div>' for t, b in anatomy_starts)}
      </div>
      <div class="an-mid">
        <div class="an-title">The squad does the work</div>
        <div class="an-deputy"><span class="who">Your deputy</span>The only one that talks to people. Answers what is simple, hands on the rest.</div>
        <div class="an-squad">
          {"".join(f'<span class="pill">{name}</span>' for name, _w, _s in SHELF)}
        </div>
        <p class="an-note">Specialists look things up, keep records and draft. None of them can send: every message leaves through one gate, as your deputy, once.</p>
      </div>
      <div class="an-col ends">
        <div class="an-title">It ends with</div>
        {"".join(f'<div class="an-item {who}"><b>{t}</b></div>' for who, t in anatomy_ends)}
      </div>
    </div>
    <div class="credo">
      <span><i class="code"></i>Code where code will do</span>
      <span><i class="model"></i>A model where it is needed</span>
      <span><i class="person"></i>A person where it matters</span>
    </div>
    <div class="sec-foot"><a class="link-arrow" href="platform.html">How the platform is built&nbsp;&rarr;</a></div>
  </div>
</section>

<section class="sec sec-white rule-t rule-b" id="work">
  <div class="wrap">
    {sec_head("What it takes off your desk", "Six kinds of work. Answering the phone is one of them.", "Most of what fills a small business's day is the same few jobs, done again. Each of these runs today.")}
    <div class="g3 kinds">
      {"".join(f'<div class="kind"><span class="kind-n">0{i}</span><h3>{t}</h3><p>{b}</p></div>' for i, (t, b) in enumerate(kinds, 1))}
    </div>
    <div class="sec-foot"><a class="link-arrow" href="workflows.html">Every workflow, and how each one runs&nbsp;&rarr;</a></div>
  </div>
</section>

<section class="sec" id="fit">
  <div class="wrap">
    {sec_head("Tailored", "Built around your business, not the other way round.", "No two deputies are the same. Each is assembled from four things, and any one of them can change without touching the others.")}
    <div class="four">
      {"".join(f'<div class="four-item"><span class="kind-n">0{i}</span><h3>{t}</h3><p>{b}</p></div>' for i, (t, b) in enumerate(four_things, 1))}
    </div>
    <div class="g3 fits">
      {fits_html()}
    </div>
  </div>
</section>

<section class="sec sec-tint rule-t rule-b" id="write">
  <div class="wrap split start wide-right">
    <div>
      <div class="kicker">Your own workflows</div>
      <h2>Write the simple ones yourself. We build the rest.</h2>
      <p class="prose" style="margin-top:18px">Describe what should happen and when, as you would to a member of staff. Your deputy names it, draws how it would run, and builds it from the parts it already has. You turn it on.</p>
      <p class="prose">When a workflow needs a part it lacks, such as a way into a supplier's site, the drawing says so. What it has can go on today; the rest comes to us as one request, with your words attached.</p>
      <p class="prose"><strong>Your deputy never writes its own code.</strong> What you build is made only of tested parts, and anything new is built, tested and signed by a person before it runs.</p>
      <p style="margin-top:20px">{status("built")}</p>
      <div class="sec-foot"><a class="link-arrow" href="workflows.html#write">How writing your own works, and why&nbsp;&rarr;</a></div>
    </div>
    {draft_demo()}
  </div>
</section>

<section class="sec" id="approve">
  <div class="wrap split start">
    <div>
      <div class="kicker you">You stay in charge</div>
      <h2>One word from your phone.</h2>
      <p class="prose" style="margin-top:18px">Every workflow stops where a person should decide. Reply ok to accept a draft, drop to bin it, or just say what to change and it comes back as a new version. From WhatsApp, a text, or your own pages.</p>
      <div class="words">
        <div class="word"><code>ok P14</code><span>accept it</span></div>
        <div class="word"><code>drop P14</code><span>bin it</span></div>
        <div class="word"><code>show P14</code><span>see it again</span></div>
        <div class="word"><code>P14 labour is 2 hours</code><span>change it</span></div>
      </div>
      <p class="prose small" style="margin-top:18px">Some things are not deputable: pricing, hiring, contractual commitments, and any complaint with real consequences. Those stay with your people, always.</p>
    </div>
    <div>
      {guarantees_html()}
    </div>
  </div>
</section>

<section class="sec sec-white rule-t" id="learns">
  <div class="wrap split">
    <div>
      <div class="kicker">It learns how you work</div>
      <h2>The more you use it, the more it works your way.</h2>
      <p class="prose" style="margin-top:18px">Each night your deputy looks back over what you changed. Make the same change to its drafts three times in five and it proposes a lesson. Ask for the same work the same way twice and it proposes a skill.</p>
      <p class="prose">It always proposes the smallest change that does the job, and nothing about how it works changes without your say.</p>
      <p style="margin-top:20px">{status("built")}</p>
      <div class="sec-foot"><a class="link-arrow" href="workflows.html#ladder">The ladder: what you approve, and what we build&nbsp;&rarr;</a></div>
    </div>
    <div class="lesson" aria-label="An example of a proposed lesson">
      <span class="mono-label">Noticed &middot; 3 of your last 5 estimates</span>
      <p class="lesson-q">On warranty jobs you change the labour to the warranty time. Shall I draft it that way from now on?</p>
      <p class="lesson-ev">P9, P11 and P14: labour changed by you after drafting.</p>
      <div class="lesson-acts">
        <span class="lesson-act">Keep the lesson</span>
        <span class="lesson-act">Make it a rule</span>
        <span class="lesson-act quiet">Dismiss</span>
      </div>
    </div>
  </div>
</section>

<section class="sec band-dark">
  <div class="wrap">
    {sec_head("Trust &amp; Security", "Isolated, auditable, and under your control.", "The controls behind every deputy, written for whoever has to sign it off.")}
    <div class="facts">
      {"".join(f'<div class="fact"><div class="fact-ic">{ICONS[ic]}</div><div class="big">{t}</div><p>{b}</p></div>' for ic, t, b in facts_home)}
    </div>
    <div class="sec-foot"><a class="link-arrow" href="trust.html">The twelve security controls&nbsp;&rarr;</a></div>
  </div>
</section>

<section class="sec">
  <div class="wrap split start">
    <div>
      <h2>No logo wall. Not yet.</h2>
      <p class="prose" style="margin-top:18px">We're a new company, and we won't decorate this page with invented numbers or testimonials we don't have. What we do have: deputies running real workflows today, a record you can audit for every job and every draft, and a rule that your data leaves with you if you do.</p>
      <p class="prose">We are taking on our first businesses as founding clients: closer attention and a say in what gets built next, in return for straight feedback. <a class="link-arrow" href="contact.html">Talk to us&nbsp;&rarr;</a></p>
    </div>
    <div class="results-panel">
      <div class="mono-label">Pilot results &middot; published as they complete</div>
      <p>This space is reserved for real measurements. When our first pilots finish, the before-and-after numbers go here, with the client's sign-off, and whether or not they flatter us.</p>
      <div class="pill-row">
        {"".join(f'<span class="pill">{m}</span>' for m in result_metrics)}
      </div>
    </div>
  </div>
</section>
""" + cta_band("See it against your own process.", "Forty-five minutes, one workflow of your choosing, no deck.")

write_page("index.html", SITE_TITLE, SITE_DESC, "home", home_body)

# ==================================================================
# PLATFORM - how a deputy is built, and how one job runs
# ==================================================================
layers = [
    ("The deputy", "The one voice people hear",
     "Only your deputy talks to people: on the phone, on WhatsApp, by text. It answers what is simple itself and hands the rest to its squad."),
    ("The squad", "Specialists, each with its own tools",
     "A specialist looks things up, keeps records and drafts, with its own tools and nobody else's. It cannot send. Every message leaves through one gate, as your deputy, once."),
    ("The workflows", "Known work, drawn as steps",
     "A piece of routine work is a drawn graph: who does each step, what each step is given, and what counts as done. Steps can run side by side."),
    ("The record", "Every job, kept",
     "Each job is one durable row: which tool ran, what it returned, what was drafted, who approved it and when. A job is never silently run again."),
]

automation = [
    ("Follow-ups", "When this happens, do that.",
     "Plain code, with no AI model in the engine. Who gets told is fixed in your configuration and is never chosen by a model.",
     [("trigger", "A message is taken"), ("code", "A card to the owner"), ("code", "A text to the caller, if they said yes")]),
    ("Watches", "On a schedule, a check in plain code.",
     "It costs nothing when nothing has changed. A model runs only when something has, and you hear only when there is something to say.",
     [("trigger", "Every 30 minutes"), ("code", "Anything new?"), ("model", "Can it wait?"), ("person", "You are told")]),
    ("Squad workflows", "Steps for a model, for code, and for a person.",
     "The model reads and drafts. Code does the arithmetic and the sending. A person decides wherever a mistake would reach a customer or a payment.",
     [("trigger", "A call ends"), ("model", "Looked up and drafted"), ("code", "Totals checked"), ("person", "You approve")]),
]

job_run = [
    ("Routed", "A quick, cheap choice first: one specialist, a known workflow, or the squad together when the work spans several."),
    ("Budgeted", "Each job runs to a deadline and a spending cap. If it reaches either, it stops and hands over what it has."),
    ("Checked in code", "No model marks its own work. A figure must trace to a tool's result and a total must be the sum of the records. One more try with the failure spelled out, then it is handed over as partial."),
    ("Reviewed", "Anything a customer will see becomes a draft that waits for one of your named people."),
    ("Traced", "Every step is kept: which tool ran and what it said. &ldquo;Where did that figure come from?&rdquo; always has an answer."),
    ("Drilled", "The squad is drilled like software is tested: scripted jobs graded by code and by a second model, run on every change and against the live models every night."),
]

doors = [
    ("phone", "Phone", "live", "A UK number answered in your business's name. Or keep the number your customers know and forward it when you're busy or closed.", ""),
    ("chat", "WhatsApp", "live", "Customers message the business and get an answer. Your notes, drafts and approvals arrive on your own WhatsApp.", "Meta checks each business before its number goes on WhatsApp. It takes a few days and we handle it."),
    ("text", "Text", "live", "What was agreed on the call, sent to your customer in writing, only if they said yes. STOP is honoured at once.", ""),
    ("page", "Your pages", "built", "Sign in with a code sent to your phone. What waits for you, your workflows, what it has learned, and your usage.", ""),
]

modes_full = [
    ("Out of hours", "live", "Every call answered.",
     "When you close, your deputy picks up: evenings, weekends and bank holidays. It answers from your own business information, takes proper details and promises a call back, which waits for you as an item due at your next opening."),
    ("Busy line", "live", "No caller lost to a busy line.",
     "Your phone provider forwards a call to your deputy when you're engaged or don't pick up, so customers keep the number they know. The note is on your WhatsApp before you've finished the job in hand."),
    ("Put through", "live", "Through to you, when you're there.",
     "In hours, a caller who asks for you hears a short hold line while your mobile rings. A briefed transfer, where you hear who is calling and why and press 1 to take it, is built and in testing."),
]

voice_caps = [
    "Answers from your own hours, services and facts",
    "Follows your standing rules, written in your words",
    "Knows a returning customer: the last call, the notes, what was promised",
    "Greets your staff by name and takes work from them",
    "Starts the workflow the call needs: an estimate, a search, a call back",
    "Asks before texting your customer what was agreed",
    "Puts a caller through to a named person",
    "Says so when it doesn't know, and takes a message",
]

commands = [
    ("ok P14", "Accept the draft, as the version you read."),
    ("drop P14", "Bin it. Add a reason if you like; it is kept."),
    ("show P14", "See it again, and how to answer it."),
    ("P14 labour is 2 hours", "Say what to change. A new version comes back for your ok."),
    ("resend P14", "Try again a send that failed. Only a person can."),
    ("send", "Send your latest email draft as it stands."),
    ("remember that&hellip;", "Keep a fact or a rule. It holds on every job from then on."),
    ("new workflow: when&hellip;", "Describe a workflow. Your deputy draws it for you to turn on."),
]

platform_body = page_hero(
    "The platform",
    "One deputy. A squad behind it. Your workflows on top.",
    "Deputable is an orchestration platform for agentic workflows. Each business gets its own deputy: an orchestrator people talk to, a squad of AI specialists with their own tools, and the workflows that put them to work. Assembled around the business, and run by us as a service.",
    """
    <div class="hero-ctas">
      <a class="btn btn-primary" href="contact.html">Book a demo call <span class="arr" aria-hidden="true">&rarr;</span></a>
      <a class="btn btn-secondary" href="workflows.html">See the workflows</a>
    </div>""") + f"""
<section class="sec" id="built">
  <div class="wrap split start">
    <div>
      {sec_head("How a deputy is built", "Four layers, each doing one job.", "The layers are separate on purpose. The part that talks cannot act on its own, the parts that act cannot send, and all of it leaves a record.")}
    </div>
    <ol class="layers">
      {"".join(f'<li><span class="kind-n">0{i}</span><div><h3>{t}</h3><div class="layer-sub">{s}</div><p>{b}</p></div></li>' for i, (t, s, b) in enumerate(layers, 1))}
    </ol>
  </div>
</section>

<section class="sec sec-white rule-t rule-b" id="squad">
  <div class="wrap">
    {sec_head("The squad", "Specialists on the shelf.", "Your squad is picked from these, and a new one is built when a business needs it. Each works only with its own tools, on your deputy's own record.")}
    <div class="shelf">
      {"".join(f'<div class="shelf-item"><h3>{n}</h3><p>{w}</p><span class="shelf-with">Works with: {s}</span></div>' for n, w, s in SHELF)}
      <a class="shelf-item more" href="workflows.html#more"><h3>The one you need</h3><p>A way into your own system, built with you, tested and signed before it runs.</p><span class="link-arrow">How a new one is built&nbsp;&rarr;</span></a>
    </div>
  </div>
</section>

<section class="sec" id="automation">
  <div class="wrap">
    {sec_head("Three kinds of automation", "Code where code will do. A model where it is needed. A person where it matters.", "Not everything needs an AI model, and what doesn't need one doesn't get one. That keeps the work predictable, and the bill small.")}
    <div class="g3">
      {"".join(f'<div class="card"><div class="for">{k}</div><h3>{t}</h3><p>{b}</p>{strip(steps)}</div>' for k, t, b, steps in automation)}
    </div>
    {who_key()}
  </div>
</section>

<section class="sec sec-tint rule-t rule-b" id="job">
  <div class="wrap split start">
    <div>
      {sec_head("How one job runs", "Six things happen to every job.", "This is the part a demo never shows, and the part that decides whether you can rely on it.")}
    </div>
    <div class="cmd-table">
      {"".join(f'<div class="cmd-row"><code>{t}</code><span>{b}</span></div>' for t, b in job_run)}
    </div>
  </div>
</section>

<section class="sec" id="doors">
  <div class="wrap">
    {sec_head("The doors", "One deputy, every way people reach you.", "The same deputy on every line, working from one record. A customer who rang on Monday and messages on Thursday never has to start again.")}
    <div class="doors">
      {"".join(f'<div class="door"><div class="door-top"><div class="ic">{ICONS[ic]}</div>{status(st)}</div><h3>{t}</h3><p>{b}</p>' + (f'<p class="fine">{fine}</p>' if fine else "") + '</div>' for ic, t, st, b, fine in doors)}
    </div>
  </div>
</section>

<section class="sec sec-white rule-t rule-b" id="smart-call-handling">
  <div class="wrap">
    {sec_head("Smart Call Handling", "The phone, handled. Three ways.", "The phone is one door, and for many small businesses the one where work is lost quietly: after hours, on a busy line, in a voicemail nobody checks. Your deputy covers for your team and backs it up. It takes no one's place.")}
    <div class="g3">
      {"".join(f'<div class="mode"><div class="top"><span class="when">{k}</span>{status(st)}</div><h3>{t}</h3><p>{b}</p></div>' for k, st, t, b in modes_full)}
    </div>
    <div class="split start" style="margin-top:56px">
      <div>
        <h3 style="margin-bottom:18px">What it handles on your line</h3>
        {ticks(voice_caps)}
      </div>
      <div class="panel-stack">
        <div class="panel">
          <h3>Safeguards, not optional extras</h3>
          <p>Callers are told they're speaking with an AI assistant, and that the call is recorded, in the opening sentence. Your deputy doesn't quote a price or commit you to anything on a call. When it lacks the facts it says so and takes a message.</p>
        </div>
        <div class="panel">
          <h3>Inbound-first, by design</h3>
          <p>Your deputy answers the calls your customers make to you. It rings out only when one of your people asks it to, on a brief they have read and approved, one call at a time. No cold calling and no dialling lists, which keeps you square with Ofcom's rules and keeps your number's reputation clean. <a href="https://www.ofcom.org.uk/phones-and-broadband/unwanted-calls-and-messages/refresher-messaging-on-silent-and-abandoned-calls" target="_blank" rel="noopener" class="link-arrow">Ofcom guidance&nbsp;&rarr;</a></p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="sec" id="approve">
  <div class="wrap split start">
    <div>
      <div class="kicker you">Approvals</div>
      <h2>Every workflow stops where a person should decide.</h2>
      <p class="prose" style="margin-top:18px">Every draft has a short name, like P14. You answer it the way you would answer a colleague, from WhatsApp or by text. Or tap Approve, Drop or Change it on your own pages.</p>
      <div style="margin-top:28px">
        {guarantees_html()}
      </div>
    </div>
    <div class="cmd-table">
      {"".join(f'<div class="cmd-row"><code>{c}</code><span>{d}</span></div>' for c, d in commands)}
    </div>
  </div>
</section>
""" + cta_band("See the platform run your own work.", "Forty-five minutes, one workflow of your choosing, no deck.")

write_page(
    "platform.html",
    "The Platform - Agentic Workflow Orchestration for SMEs | Deputable AI",
    "How a deputy is built: an orchestrator, a squad of AI specialists with their own tools, workflows drawn as steps, and a record of every job. Smart Call Handling is one of its doors.",
    "platform", platform_body)

# The old Services page: its links and search results keep working.
write_redirect("services.html", "platform.html", "The platform - Deputable AI")

# ==================================================================
# WORKFLOWS - the catalogue, writing your own, and what we build
# ==================================================================
workflows_body = page_hero(
    "Workflows",
    "Every piece of routine work, as a workflow you can see.",
    "A workflow has a start, steps, and someone who does each step: plain code, an AI model, or one of your people. The ones below exist today. Write the simple ones yourself in a sentence; we build the bigger ones with you.",
    who_key()) + f"""
<section class="sec" id="catalogue">
  <div class="wrap">
    {sec_head("The catalogue", "Workflows that exist today.", "Each row is drawn the way your own Workflows page draws it: what starts it, then each step and who does it. They start in six different ways. A phone call is one.")}
    <div class="starts-row">
      {"".join(f'<span class="starts">{s}</span>' for s in STARTS)}
    </div>
    {catalogue_html()}
  </div>
</section>

<section class="sec sec-tint rule-t rule-b" id="write">
  <div class="wrap">
    <div class="split start wide-right">
      <div>
        <div class="kicker">Write your own</div>
        <h2>The simple ones, you write yourself.</h2>
        <p class="prose" style="margin-top:18px">One box. Describe what should happen and when, as you would to a member of staff, on your Workflows page or by sending <code class="inline">new workflow: when&hellip;</code> on WhatsApp.</p>
        <p class="prose">Your deputy proposes a name and draws the workflow: what starts it, each step, and who does each one. You can't edit the drawing. You edit the words, and it redraws. When it reads right, you turn it on.</p>
        <p style="margin-top:20px">{status("built")}</p>
      </div>
      {draft_demo()}
    </div>
    <div class="parts">
      <div class="parts-col">
        <div class="mono-label">It can start</div>
        {"".join(f'<div class="part"><span class="node trigger mini"><span class="who">Starts it</span></span><div><h3>{t}</h3><p>{b}</p></div></div>' for t, b in PARTS_STARTS)}
      </div>
      <div class="parts-col">
        <div class="mono-label">And then</div>
        {"".join(f'<div class="part"><span class="node {who} mini"><span class="who">{WHO[who]}</span></span><div><h3>{t}</h3><p>{b}</p></div></div>' for who, t, b in PARTS_STEPS)}
      </div>
    </div>
    <p class="prose small parts-note">That list is short on purpose, and it is closed: the drafting model may use only these parts and must name anything else as missing. It grows as parts are built.</p>
  </div>
</section>

<section class="sec" id="more">
  <div class="wrap">
    {sec_head("The bigger ones", "When a workflow needs more, it says so, and asks us.", "A step your deputy has no part for is drawn as a dashed &ldquo;Not yet&rdquo; box. You choose: turn on the parts it has today, send us the rest as one request, or both.")}
    <div class="g4">
      {"".join(f'<div class="card dashed"><h3>{t}</h3><p>{b}</p></div>' for t, b in PARTS_MISSING)}
    </div>
    <div class="reqpath" aria-label="What happens to a request">
      {"".join(f'<div class="req-step"><span class="kind-n">0{i}</span>{s}</div>' for i, s in enumerate(REQUEST_STEPS, 1))}
    </div>
    <p class="prose small" style="margin-top:22px">Your request arrives with your own words and the drawing attached, so nobody has to ask you twice. A person at Deputable decides what it takes, and each decision is written into your record and told to you on your phone.</p>
  </div>
</section>

<section class="sec sec-white rule-t rule-b" id="why">
  <div class="wrap">
    {sec_head("Why the line is drawn there", "Easy where it is safe. Careful where it isn't.", "Plenty of tools let an AI write its own automations. We chose not to, and these are the reasons.", you=True)}
    <div class="g3">
      {"".join(f'<div class="principle"><span class="kind-n">0{i}</span><h3>{t}</h3><p>{b}</p></div>' for i, (t, b) in enumerate(PRINCIPLES, 1))}
    </div>
  </div>
</section>

<section class="sec" id="ladder">
  <div class="wrap">
    {sec_head("The ladder", "It proposes the smallest change that does the job.", "The same idea runs through how a deputy learns. Each night it looks over the day's work and proposes what it noticed, always on the lowest rung that would do. You approve the first three yourself. The last two are ours to build.")}
    {ladder_html()}
    <p style="margin-top:22px">{status("built")}</p>
  </div>
</section>
""" + cta_band("Bring one process. We'll draw it.", "Forty-five minutes, one workflow of your choosing, no deck.")

write_page(
    "workflows.html",
    "Workflows - Write the Simple Ones Yourself, We Build the Rest | Deputable AI",
    "The workflows a deputy runs today, drawn step by step with who does each. Describe a simple one in a sentence and turn it on; anything bigger is built, tested and signed by us.",
    "workflows", workflows_body)

# ==================================================================
# PERSONAL
# ==================================================================
personal_groups = [
    ("Mail", "live", [
        "Find a message in plain words and hear it read",
        "Reply from your own address, after one read-back and a yes",
        "&ldquo;Draft it, don't send it&rdquo;: one draft, kept on the thread",
        "A watch every half hour. You're told only when something can't wait",
        "Several mailboxes side by side",
    ]),
    ("Diary", "live", [
        "Every calendar you keep, in one answer",
        "&ldquo;What's my next meeting with Sam about?&rdquo;",
        "Time blocked on your own diary, after a clash check",
        "A new clash is flagged once, on your phone",
        "Invitations sent on your yes",
    ]),
    ("Knowing things", "live", [
        "Web search, and a page read aloud in parts",
        "Lists, and &ldquo;remember that&rdquo;",
        "Public transport in London with real times",
        "Drives in today's traffic, and when to leave",
        "Photos, PDFs and voice notes read, and found again by name",
    ]),
    ("Doing things", "live", [
        "Reminders by text, or a call, at the time you set",
        "A slide deck built from an outline you agree, and emailed",
        "&ldquo;Call my brother&rdquo;: it rings you back and puts you through",
        "The monthly invoice drafted from your timesheets",
    ]),
    ("Keeping its word", "built", [
        "After a call, what it promised is checked against what it did",
        "What it can do itself gets done. The rest waits on your word",
        "A call made for you, from a brief you approve first",
        "A recording of a meeting becomes follow-ups you approve",
        "A morning summary by email: diary, mail, what's waiting",
    ]),
    ("Your language", "live", [
        "A deputy that speaks your language",
        "Live in English and Hinglish today",
        "Ten more languages drafted, waiting on a native speaker's review",
    ]),
]

personal_body = page_hero(
    "A deputy of your own",
    "For your mail, your diary and the things you'd forget.",
    "Ring it or message it on WhatsApp. It reads your mail to you, keeps your diaries straight, remembers what you tell it and rings people for you. Nothing goes out in your name without your say-so.",
    """
    <div class="hero-ctas">
      <a class="btn btn-primary" href="contact.html">Ask for an invitation <span class="arr" aria-hidden="true">&rarr;</span></a>
    </div>""") + f"""
<section class="sec">
  <div class="wrap">
    {sec_head("What it does", "A second pair of hands, on the phone you already carry.", "No app to learn. You talk to it or write to it, and it answers the same way.")}
    <div class="g3">
      {"".join(f'<div class="card"><div class="top"><h3>{t}</h3>{status(st)}</div>{ticks(items)}</div>' for t, st, items in personal_groups)}
    </div>
  </div>
</section>

<section class="sec sec-white rule-t rule-b">
  <div class="wrap split start">
    <div>
      <div class="kicker you">Yours, privately</div>
      <h2>It asks before it acts.</h2>
      <p class="prose" style="margin-top:18px">An email is read back to you once, with who it goes to and the gist, and sent on your yes. A draft stays a draft until you say send. Anything aimed at someone else waits on your word.</p>
      <p class="prose">You connect your mail and your diary yourself, and disconnect them whenever you like. Your own things never open for a customer or a caller: that is a rule in the code, not a setting.</p>
    </div>
    <div class="panel-stack">
      <div class="panel you">
        <h3>What it will not do</h3>
        <p>Send in your name without a yes. Spend your money. Tell a caller what is in your diary or your inbox.</p>
      </div>
      <div class="panel">
        <h3>By invitation, for now</h3>
        <p>Personal deputies are by invitation while we take on our first people, and for adults only. If you run a business with us, you can have one alongside it. Otherwise, ask on a demo call.</p>
      </div>
    </div>
  </div>
</section>
""" + cta_band("Try one on your own day.", "Forty-five minutes. Bring the task you'd most like off your plate.", "Ask for an invitation")

write_page(
    "personal.html",
    "A Deputy of Your Own - Mail, Diary and Reminders by Voice | Deputable AI",
    "Ring it or message it. Your mail read aloud and replied to on your yes, every diary in one answer, reminders by text or call, lists, journeys and calls made for you.",
    "personal", personal_body)

# ==================================================================
# FEATURES - everything it does, and where each thing stands.
#
# Every row carries the id of its entry in the Deputy platform's master
# feature list (docs/features.md in the deputy repo). The id is not
# shown; it is written into the HTML as data-id so this page can be
# checked against that list. Rows marked CORE-* describe the engine
# itself (the squad, the checks, the record), which that list does not
# number. A row's status must match the list:
#   live  = in production and used on real calls or messages
#   built = built and tested; switched on with the first clients
#   next  = agreed and drawn; not built
# ==================================================================
FEATURES = [
    ("Reaching your deputy", "The same deputy on every line, working from one record.", [
        ("DOOR-01", "A number for your business", "live", "A UK number answered in your business's name. Or keep the number your customers know and forward it when you're busy or closed."),
        ("DOOR-04", "WhatsApp messages", "live", "Customers write to the business and get an answer. Your notes, drafts and approvals arrive on your own WhatsApp. Meta checks each business before its number goes on."),
        ("DOOR-06", "Text messages", "live", "The text after a call, replies by text for people without WhatsApp, STOP and START honoured, delivery receipts."),
        ("DOOR-07", "A team room", "live", "Every note, card and draft mirrored in a private room for your staff, on a phone or a desk."),
        ("DOOR-12", "Your customers' language", "live", "Live in English and Hinglish. Set lines are drafted in ten more languages and wait on a native speaker's review."),
        ("DOOR-05", "WhatsApp calls", "built", "The call button in the chat rings your deputy, on the same record as the phone."),
        ("ACC-13", "Your own pages", "built", "Sign in with a code sent to your phone, then a passkey or Google. What waits for you, recent conversations, your diary and what it knows."),
    ]),
    ("On the call", "Smart Call Handling, one door of several: out of hours, on a busy line, and through to you.", [
        ("REC-01", "Answers in your business's name", "live", "Your greeting, hours, services and facts, and your standing rules in plain language. It says it is an AI assistant in the opening sentence."),
        ("REC-10", "Knows the caller", "live", "A returning customer's last call, the notes, what was promised and whether they agreed to texts, read before it speaks."),
        ("REC-11", "Staff on the line", "live", "One of your people is greeted by name, can ask for texts and can hand work to the deputy."),
        ("REC-05", "Put through to a person", "live", "In hours the caller hears a hold line while your mobile rings. Out of hours or unanswered, a call back is promised."),
        ("REC-09", "Recording, with disclosure", "live", "Calls are recorded by default and the greeting says so. You can turn it off. Kept 30 days unless you choose otherwise."),
        ("REC-06", "Briefed before you pick up", "built", "The caller waits while you hear who is calling and why. Press 1 to take it or 2 to decline."),
    ]),
    ("After the call", "Nothing promised is forgotten.", [
        ("REC-02", "A note after every contact", "live", "Summary, open items, promises, the lead and any call back owed, on your phone as the call ends."),
        ("REC-03", "The text to your customer", "live", "One message with what was agreed, only with the caller's yes, never twice."),
        ("REC-04", "Call backs owed", "live", "A promised call back becomes an item due at your next opening, created by code whatever the note says."),
        ("REC-12", "Follow-ups that run themselves", "live", "When this happens, do that: a card to the owner, a text, a piece of work raised for an ok. Plain code, no AI model in the loop."),
        ("REC-17", "A weekly digest", "next", "Calls taken, call backs kept and estimates drafted, once a week."),
        ("REC-07", "A busy flag", "next", "&ldquo;On a job until three&rdquo; from your phone, and calls in that window take a message."),
    ]),
    ("Approvals", "A person decides what a customer sees.", [
        ("WORK-01", "You approve, it sends", "live", "Nothing customer-facing leaves review without one of your named people approving the version they read."),
        ("WORK-02", "Changes come back as a new version", "live", "Say what to change in your own words. The new version waits for your ok again."),
        ("REC-13", "One-word replies", "live", "ok, drop, show, resend or a change, typed the way a phone types them."),
        ("WORK-03", "Never sent twice", "live", "A message whose delivery we can't confirm is never tried again without a person."),
        ("OPS-17", "Approve on your pages", "built", "Approve, Drop and Change it on what waits for you, the same as the words on WhatsApp."),
    ]),
    ("Workflows", "Known pieces of work, drawn before they are built.", [
        ("REC-14", "Estimates for a garage", "live", "Vehicle, repair, labour and parts, priced at your rate and markup, totals and VAT in code. Parts prices are live from eBay today, with starter labour times; licensed data is next."),
        ("REC-15", "Property search", "live", "An agency's own live listings matched to what the caller asked, and read back."),
        ("DOC-01b", "The monthly invoice", "live", "Timesheet screenshots become the Word file, the PDF and the covering email, drafted for you to check."),
        ("DOC-01", "Documents that start work", "built", "A photo or PDF is read, sorted (invoice, receipt, letter) and its figures pulled out. An invoice is kept as a bill on your ok."),
        ("COMP-26", "Meeting follow-ups", "built", "A recording becomes a summary, the decisions, and who owes what. Each follow-up waits for your ok."),
        ("OPS-22", "A workflow from a description", "built", "Say what should happen when, in your words. Your deputy names it and draws it; you turn it on."),
        ("OPS-21", "Pause, remove, restore", "built", "Every workflow is a row on your page, with its steps, its settings and its runs."),
        ("OPS-23", "Ask us for what's missing", "built", "A part your deputy lacks becomes one request to us, with your words and the drawing attached."),
        ("REC-16", "Bookings", "next", "A slot booked into your diary on the call."),
        ("PORTAL", "Sites with no way in", "next", "Your deputy reads a supplier's site in a browser you signed in to yourself. It looks and never buys."),
    ]),
    ("A deputy of your own", "For one person: mail, diary, reminders and errands.", [
        ("COMP-01", "Mail found and read aloud", "live", "Search in plain words across several mailboxes; one message read in paragraphs."),
        ("COMP-02", "Replies, on your yes", "live", "Sent from your own address after one read-back. Replies stay on their thread."),
        ("COMP-03", "Drafts kept", "live", "&ldquo;Draft it, don't send it&rdquo; keeps one draft on the thread. A change rewrites that draft."),
        ("COMP-04", "The mail watch", "live", "New mail checked every half hour. A text, or a call, only when something can't wait."),
        ("COMP-05", "Diaries across organisations", "live", "Every calendar in one answer, time blocked after a clash check, new clashes flagged once."),
        ("COMP-06", "Search, and pages read aloud", "live", "A web search, and a page reduced to its words and read in parts."),
        ("COMP-07", "Lists and facts", "live", "Shopping and to-do lists, &ldquo;remember that&rdquo;, and &ldquo;forget that&rdquo;."),
        ("COMP-08", "Reminders by text or call", "live", "Set once, fired on time by plain code."),
        ("COMP-09", "Journeys", "live", "Public transport in London with real times; drives in traffic with a leave-by time."),
        ("COMP-10", "A deck by email", "live", "Slides built from an outline you agree on a call, emailed to you."),
        ("COMP-12", "&ldquo;Call my brother&rdquo;", "live", "It rings you back and puts you through to the person you named."),
        ("COMP-19", "Your language", "live", "A deputy in your own language. Hinglish is live."),
        ("COMP-24", "Photos, PDFs and voice notes", "built", "A photo of a letter, a PDF or a voice note is read, kept, and found again by name."),
        ("COMP-14", "What it promised, settled", "built", "After a call, what it said it would do is checked against what it did. The rest waits on your word."),
        ("COMP-13", "Calls made for you", "built", "You approve a brief: who, what to say, what it may and may not agree. Then it rings, inside calling hours, and tells you how it went."),
        ("COMP-18", "The morning summary", "built", "Today's diaries, the mail that needs you, reminders and what waits for your ok, by email."),
        ("COMP-25", "It reads to you", "next", "Long documents read aloud, with your place kept for next time."),
        ("COMP-17", "Chase it for me", "next", "&ldquo;Chase if there's no reply in three days&rdquo; as a standing instruction."),
    ]),
    ("It learns how you work", "What it knows, and how that changes, is yours to see.", [
        ("MEM-01", "A briefing before it speaks", "live", "Reminders, answers owed, items waiting and recent calls, read before the first word."),
        ("MEM-02", "Facts with a source", "live", "What it knows says where it came from and when it expires. &ldquo;Forget that&rdquo; retires it."),
        ("MEM-03", "Notebooks", "live", "Each specialist behind your deputy keeps the lessons you have taught it."),
        ("MEM-06", "Lessons from your corrections", "built", "Make the same change three times in five and it proposes a lesson. You keep it, make it a rule, or dismiss it."),
        ("MEM-07", "Skills from repeated work", "built", "Work you ask for the same way twice is drafted as a skill, dry-run in front of you, and used only once you approve it."),
        ("MEM-08", "Checked every night", "built", "Each approved skill is replayed nightly. Two failures in a row pause it and you are told."),
    ]),
    ("Privacy, access and the record", "The parts a client never sees, and should know are there.", [
        ("ACC-02", "Tenant isolation", "live", "Every client runs in its own data silo: a dedicated directory and a dedicated database, stored in London."),
        ("ACC-06", "Hourly encrypted backups", "live", "Encrypted with a key our servers never hold. Restores are rehearsed."),
        ("ACC-03", "You decide what we can see", "live", "Nothing, a limited view with no call transcripts, or everything, with who, why and until when written down."),
        ("ACC-01", "Roles", "live", "Owner, staff, technician and monitor. What each may ask for and approve is set per business."),
        ("ACC-05", "Export and erasure", "live", "One person's data exported, or erased across the record, the recordings and our telephony supplier's copies."),
        ("ACC-04", "Paperwork as a gate", "live", "A business can't go live without a privacy notice and a dated impact assessment. The software refuses."),
        ("OPS-02", "Signed releases", "live", "Our servers run only software one of us has signed."),
        ("OPS-14", "Every minute you pay for", "built", "A usage page for whoever pays: minutes, messages and finished jobs this month."),
        ("RES-UKEU", "UK and EU processing", "next", "Suppliers and models scoped to the UK and EU, for a client that requires it."),
        ("OPS-12", "A server of your own", "next", "For a client whose data must share no machine with anyone else's."),
    ]),
]


# How the work gets done: the engine, read from the code (squad/loop.py,
# squad/router.py, squad/checks.py, members/_base/tools.py, drills).
FEATURES.append(("How the work gets done", "The engine under every workflow.", [
    ("CORE-squad", "A squad of specialists", "live", "Each specialist works with its own tools and nobody else's. It looks things up, keeps records and drafts; it cannot send."),
    ("CORE-route", "The right hands for each job", "live", "A quick, cheap choice first: one specialist, a known workflow, or the squad together when the work spans several."),
    ("CORE-checks", "Checked in code", "live", "No model marks its own work. A figure must trace to a tool's result; a total must be the sum of the records."),
    ("OPS-09", "A budget for every job", "live", "Each job runs to a deadline and a spending cap, and each deputy to a daily one. At the limit it stops and says so."),
    ("CORE-record", "Every job on the record", "live", "Which tool ran, what it returned, what was drafted and who approved it. A job is never silently run again."),
    ("OPS-13", "No model where none is needed", "live", "Follow-ups and watches are plain code. Sorting a request is a cheap judgment, not a conversation."),
    ("OPS-05", "Drilled every night", "live", "Scripted jobs graded by code and by a second model, run on every change and nightly against the live models."),
    ("MEM-10", "Cheaper with use", "built", "A skill that keeps passing its drill is tried on a smaller model, and offered to you with the saving. It goes back on its own if it slips."),
]))

_FEATURE_ORDER = ["Workflows", "How the work gets done", "Approvals", "It learns how you work",
                  "Reaching your deputy", "On the call", "After the call", "A deputy of your own",
                  "Privacy, access and the record"]
FEATURES.sort(key=lambda g: _FEATURE_ORDER.index(g[0]))


def features_html():
    out = ""
    for title, sub, rows in FEATURES:
        items = "".join(
            f'<div class="frow" data-id="{fid}"><h3>{name}</h3>{status(st)}<p>{desc}</p></div>'
            for fid, name, st, desc in rows
        )
        out += f"""<div class="fgroup">
      <div><h2>{title}</h2><p class="fgroup-sub">{sub}</p></div>
      <div class="frows">{items}</div>
    </div>"""
    return out


_counts = {"live": 0, "built": 0, "next": 0}
for _t, _s, _rows in FEATURES:
    for _r in _rows:
        _counts[_r[2]] += 1

features_body = page_hero(
    "Everything it does",
    "One list. Where each thing really stands.",
    "No roadmap dressed up as a product. Every capability is marked as live, built, or next, and the marks are kept in step with our own engineering list. Workflows first, because that is what the platform is.",
    f"""
    <div class="status-key">
      <div>{status("live")} In production, used on real calls and messages</div>
      <div>{status("built")} Built and tested, switched on with our first clients</div>
      <div>{status("next")} Agreed and drawn, not built yet</div>
    </div>""") + f"""
<section class="sec">
  <div class="wrap">
    {features_html()}
  </div>
</section>
""" + cta_band("Ask us to show you any line of it.", "Forty-five minutes, one workflow of your choosing, no deck.")

write_page(
    "features.html",
    "Features - Everything a Deputy Does, and Where Each Thing Stands | Deputable AI",
    f"The whole list, honestly marked: {_counts['live']} capabilities live in production, {_counts['built']} built and in testing, {_counts['next']} agreed and next.",
    "features", features_body)

# ==================================================================
# HOW IT WORKS
# ==================================================================
# (is the person's step, number, who, title, body, what you get)
process_full = [
    (False, "01", "Together", "A 45-minute call",
     "Bring one process you would like handled. We are direct about what AI does poorly, and will tell you if the answer is a spreadsheet fix rather than a deputy.",
     "A written view on whether to proceed, at no cost."),
    (False, "02", "Together", "Intake",
     "One meeting, recorded with your consent. Who may approve what, your hours and services, your standing rules in your own words, where the notes should land, and what must never happen.",
     "A written summary of what we heard, for you to correct."),
    (False, "03", "Us", "We draw it",
     "Every workflow is a drawing before it is code: what happens on a busy line, after a call, when a customer rings back. You review the drawings, and a change at this stage costs nothing.",
     "Your workflows drawn out, with every approval step marked."),
    (False, "04", "Us", "Set up, and the paperwork",
     "Your deputy's facts and rules, your people, its squad, your number. A privacy notice for your callers and a data protection impact assessment, because your deputy cannot go live without them. The software refuses.",
     "A deputy on a test line, a privacy notice, and a dated assessment."),
    (False, "05", "Us, then you", "Tested on us first",
     "We run every workflow on made-up cases, and ring your deputy as a stranger and as you. The stranger is greeted as your business and told it is an AI assistant, asks for a price and is told you will call back, and the note lands on your phone. Then you try to break it.",
     "The results of the test runs, and what we changed after them."),
    (True, "06", "You", "You say go",
     "You read the facts, the rules and the drawings, and confirm. Until you do, nothing real reaches your deputy. It starts as a trial on your own work: often your existing number forwarded when you're busy or closed, and the first workflow switched on.",
     "A deputy doing real work, and a restore rehearsed from its backup."),
]

discovery = [
    ("01", "Interview employees and map repetitive workflows."),
    ("02", "Measure volumes, labour time, delays and error rates."),
    ("03", "Assess data quality and existing systems."),
    ("04", "Rank opportunities by benefit, complexity and risk."),
    ("05", "Recommend a 60 to 90 day roadmap."),
    ("06", "Build one small, measurable pilot."),
]

process_body = page_hero(
    "Getting started",
    "From a first call to your deputy at work.",
    "Six steps, and you can stop after any of them. We do the set up; your staff give approvals from their phones. Nobody at your business has to learn to prompt an AI.") + f"""
<section class="sec">
  <div class="wrap">
    <div class="process">
      {"".join(f'''<div class="pstep{" you" if you else ""}">
        <div class="num">{n}</div>
        <div>
          <div class="who">{who}</div>
          <h2>{t}</h2>
          <p>{b}</p>
          <div class="get"><strong>You get:</strong> {o}</div>
        </div>
      </div>''' for you, n, who, t, b, o in process_full)}
    </div>
  </div>
</section>

<section class="sec sec-white rule-t rule-b">
  <div class="wrap g2">
    <div class="panel">
      <h3>After go-live</h3>
      <p>We keep reading what the record shows and fix what it turns up. You add the simple workflows yourself, in a sentence; the bigger ones we build with you, each drawn first. Your deputy proposes lessons from the changes you make to its drafts, and you decide which to keep.</p>
    </div>
    <div class="panel">
      <h3>If you leave</h3>
      <p>Your data exports in full and goes with you. Your deputy's facts, rules and workflows are plain files you can read. We would rather earn the next month than hold you to it.</p>
    </div>
  </div>
</section>

<section class="sec" id="readiness">
  <div class="wrap split start">
    <div>
      <div class="kicker">Not sure a deputy is the answer?</div>
      <h2>Start with an AI Readiness Assessment.</h2>
      <p class="prose" style="margin-top:18px">Most businesses don't need convincing that AI could help somewhere. They need to know where, what it would cost, and what it would save. Two weeks, structured so the answer is specific: a costed shortlist, not a strategy document.</p>
      <p class="prose small">A good first project is high-volume, rules-based, easy to review and capable of showing results within several weeks.</p>
    </div>
    <div class="cmd-table">
      {"".join(f'<div class="cmd-row" style="grid-template-columns:44px 1fr"><code>{n}</code><span>{t}</span></div>' for n, t in discovery)}
    </div>
  </div>
</section>
""" + cta_band("It starts with a call.", "Bring one process. We'll tell you straight whether it's worth handing over.")

write_page(
    "how-it-works.html",
    "Getting Started - From a First Call to Your Deputy at Work | Deputable AI",
    "Six steps: a demo call, intake, your workflows drawn, set up and privacy paperwork, test runs, and your go-ahead. Nothing real reaches your deputy until you have confirmed it.",
    "process", process_body)

# ==================================================================
# ABOUT
# ==================================================================
team = [
    ("Rohit Sinha", "Founder", "https://www.linkedin.com/in/rohit-sinha-b6792715/", "Rohit has spent two decades getting change safely into production at Britain's biggest banks - cloud platform delivery, release management and observability at institutions where a bad deployment makes the news - most recently leading AI and Copilot adoption inside a major UK building society. Regulated environments taught him the rules Deputable now runs on: pilots that run alongside the existing process, evidence before reliance, and a named approver on anything that reaches a customer. Deputable exists because he'd watched too many automation programmes fail the same way - by removing people from processes that still needed them."),
    ("Prashant Tiwari", "Founder", "https://www.linkedin.com/in/prashanttiwari247/", "Prashant has spent his career building systems that aren't allowed to fail quietly - low-latency trading engines in an investment bank's front office, IoT fleets, a data platform parsing millions of records a day - and, most recently, AI systems that answer to evaluation gates rather than demos. At Deputable he leads how the work is scoped and built: one workflow at a time, integrated with the systems a client already runs, tested against real calls before it ships, and documented so the client's own team can maintain it afterwards. A co-organiser of PyData London for the last ten years, he started Deputable because the businesses that most need this help are the ones least able to gamble a year and a six-figure budget finding out whether it works."),
]

about_body = f"""
<section class="page-hero">
  <div class="wrap">
    <div class="kicker">About</div>
    <div class="dict-entry">
      <span class="dict-word">deputable</span>
      <span class="dict-ipa">/d&#603;p&#712;ju&#720;t&#601;bl/</span>
      <span class="dict-pos">adjective</span>
      <span class="dict-def">able to be safely deputed; fit to be delegated.</span>
    </div>
    <p class="lede">We started with one question: which parts of a working day can you honestly hand to an AI, and which parts should never leave a person's hands? The company is named after the answer.</p>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    {sec_head("The line", "Some work is deputable. Some never will be.", "A good deputy takes the routine off your desk and brings you the decisions. That's the standard we hold ours to. It reads what came in, looks up what it needs, drafts the estimate, chases the paperwork, and answers the phone at seven in the evening. Then it stops, because the next step belongs to a person.")}
    <div class="depute-grid">
      <div class="depute-col">
        <div class="depute-col-title">Deputable</div>
        {ticks(depute_items)}
      </div>
      <div class="depute-col keep">
        <div class="depute-col-title">Not deputable</div>
        {ticks(keep_items, "you")}
      </div>
    </div>
    <p class="prose depute-close">Our job is to empower and enable people, never to replace them. If a proposal of ours would quietly erase someone's judgment from a process, it's a bad proposal, and we'll tell you so.</p>
    <div class="assure-strip">
      {"".join(f'<a class="assure-item" href="trust.html">{a}</a>' for a in assure_items)}
    </div>
  </div>
</section>

<section class="sec sec-white rule-t rule-b">
  <div class="wrap split start">
    <div>
      <h2>How we work</h2>
      <p class="prose" style="margin-top:18px">Every business runs differently, so a deputy is assembled around yours: your hours, your people, your rules in your own words, the specialists your work needs. We do the intake, draw the workflows with you, handle the privacy paperwork and keep reading what the record shows. Your staff give approvals from their phones.</p>
      <p class="prose">Most of our thinking is shaped by service businesses that live and die by the phone, such as garages, trades, property and logistics, but nothing about the approach is locked to an industry.</p>
    </div>
    <div class="mission-box">
      <div class="label">Our Mission</div>
      <p>Remove the operational friction from growing businesses. When AI manages the repetitive calls, enquiries and system updates, your team responds faster and spends its day on the work that actually creates value.</p>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    {sec_head("Founders", "The people who answer for it.")}
    <div class="g2">
      {"".join(f'''<div class="founder">
        <div class="name">{n}</div>
        <div class="role">{r}</div>
        <p>{b}</p>
        <a class="link-arrow" href="{li}" target="_blank" rel="noopener">LinkedIn&nbsp;&rarr;</a>
      </div>''' for n, r, li, b in team)}
    </div>
  </div>
</section>
""" + cta_band("Meet us on a call.", "Forty-five minutes, one workflow of your choosing, no deck.")

write_page(
    "about.html",
    "About - Why We're Called Deputable | Deputable AI",
    "Deputable: what you can safely hand to an AI, and what should stay with people. The thinking behind the name, and the founders behind the company.",
    "about", about_body)

# ==================================================================
# TRUST
#
# Every answer here is a statement about the platform as it runs. Check
# a change against the Deputy repo (docs/legal/README.md lists what is
# not yet true) before publishing it. The page names no suppliers and
# draws no data-flow map (Prashant 2026-11-13: confusing and concerning,
# and UK or EU processing can be scoped for a client that needs it):
# sub-processors are named per client in the agreement. Do not state
# UK-only processing as a standing feature, and do not claim the AI
# suppliers' no-training terms until the contracts are confirmed.
# ==================================================================
# The controls, as tiles. (icon, group, title, body, held by a test).
# "Held by a test" is set only where the Deputy repo has an automated
# test for it (its CLAUDE.md invariants; tests/test_core_api.py,
# test_workitems.py, test_loop.py, test_dispatch.py, test_deploy.py,
# test_backup_loop.py, test_config.py).
controls = [
    ("silo", "Data", "Tenant isolation",
     "Every client runs in its own data silo: a dedicated directory and a dedicated database. The tenant is resolved at the point of entry, before any AI model runs.", True),
    ("pin", "Data", "UK data residency at rest",
     "Records, documents, recordings and backups are stored in Oracle Cloud's London region, on disks encrypted at rest.", False),
    ("lock", "Data", "Encrypted, rehearsed backups",
     "Hourly backups, encrypted with a key our servers never hold. Restores are rehearsed end to end, not assumed.", True),
    ("clock", "Data", "Retention and erasure",
     "Recordings are kept 30 days and transcripts 90 by default, or to your own schedule. One person's data can be exported or erased on request, including the copies our telephony supplier holds.", False),
    ("user", "AI safety", "Human approval gate",
     "Nothing customer-facing leaves review without a named, authorised person. Approval is bound to the exact version they read.", True),
    ("check", "AI safety", "Prompt-injection containment",
     "Content from outside, such as a caller's words, an email or a web page, is marked untrusted. It can inform a draft. It can never trigger a send or change a record.", True),
    ("send", "AI safety", "A single outbound gate",
     "AI specialists cannot send. Every message leaves through one gate, exactly once, and an unconfirmed delivery is never retried without a person.", True),
    ("file", "AI safety", "Full audit trail",
     "Every job records its inputs, each tool call and its result, the draft, the approver and the time. Any figure can be traced to its source.", False),
    ("key", "Access", "Role-based access control",
     "Owner, staff, technician and monitor roles decide who may ask for what, and who may approve. Your people sign in with a one-time code or a passkey.", False),
    ("eye", "Access", "Supplier access on your terms",
     "You set what Deputable staff can see, per client: none, a limited view with no call transcripts (the default), or full, with the person, reason and end date recorded.", False),
    ("pen", "Assurance", "Signed releases",
     "Production runs only software one of us has cryptographically signed, after it has run on a pre-production twin.", True),
    ("clip", "Assurance", "Privacy by design",
     "No deputy goes live without a published privacy notice and a dated data protection impact assessment. The platform refuses to start it otherwise.", True),
]


def controls_html():
    out = ""
    for ic, group, title, body, tested in controls:
        badge = '<span class="ctl-test">Held by an automated test</span>' if tested else ""
        out += (f'<div class="ctl"><div class="ctl-top"><div class="ctl-ic">{ICONS[ic]}</div>'
                f'<span class="ctl-group">{group}</span></div><h3>{title}</h3><p>{body}</p>{badge}</div>')
    return out


golive = [
    "AI disclosure in the opening sentence of every call",
    "Recording notice, or recording switched off",
    "A named approver for anything customer-facing",
    "A published privacy notice",
    "A dated data protection impact assessment",
    "Opt-outs honoured: STOP stops texts at once",
    "A restore rehearsed from backup",
    "Your list of sub-processors, by name and region",
]

trust = [
    ("Where is our data stored?",
     "In Oracle Cloud's London region, on disks encrypted at rest. Each client has a dedicated directory and a dedicated database, and backups are held in London too."),
    ("Which suppliers process our data?",
     "Your data is stored in the UK. Telephony, speech and the AI models are provided by specialist suppliers, and each one is named, with its processing region, in your data processing agreement before you go live. If you need processing kept within the UK or EU, tell us at the outset and we scope the suppliers and models to that requirement."),
    ("Do you train AI models on our data?",
     "No. We do not train models at all. Your data is used to provide your service and for nothing else. It is never sold and never used for advertising."),
    ("Can the AI send something to a customer on its own?",
     "No. Anything customer-facing waits for a named, authorised person at your business, and their approval is bound to the version they read. Each message is sent exactly once; if delivery cannot be confirmed, a person decides before it is tried again. These are controls in the code, each held by an automated test, not instructions we hope a model follows."),
    ("How do you defend against prompt injection?",
     "Content from outside, such as what a caller says, an email or a web page, is marked as untrusted the moment it arrives. It can inform a draft for a person to read. It cannot trigger a send or change a record, and who a follow-up goes to is fixed in your configuration, never chosen by a model."),
    ("Who at Deputable can access our data?",
     "You decide, per client. None. A limited view, which is the default: the steps your deputy took and the written messages it exchanged with customers, but no call transcripts and nothing it read in your mail or diary. Or full access, with the person, the reason and the end date recorded."),
    ("Are calls recorded, and are callers told?",
     "By default yes, and the greeting says so in its opening sentence, along with the fact that the caller is speaking with an AI assistant. Recording can be switched off. Unless you set your own schedule, recordings are kept for 30 days and notes and transcripts for 90."),
    ("What is your audit trail and recovery position?",
     "Every job records its inputs, each tool call and its result, the draft, the approver and the time, so an error can be traced to its step. Records are backed up hourly, encrypted with a key our servers never hold, and restores are rehearsed. Recordings are held on the server only and are not included in backups."),
    ("Can we export or delete our data?",
     "Yes. Your data exports in full and goes with you if you leave. One person's data can be exported or erased on request across the record, the recordings and the copies our telephony supplier holds. Encrypted backups cannot be edited, so they expire on their own within 90 days."),
]


def _plain(s):
    return re.sub(r"<[^>]+>", "", s).replace("&amp;", "&")


trust_faq_jsonld = json.dumps({
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
        {"@type": "Question", "name": q,
         "acceptedAnswer": {"@type": "Answer", "text": _plain(a)}}
        for q, a in trust
    ],
})

trust_body = page_hero(
    "Trust &amp; Security",
    "Isolated, auditable, and under your control.",
    "How each client's data is isolated, who can access it, and the controls that hold an AI system to account. Written for the person who has to sign it off.",
    """
    <div class="trust-nav">
      <a href="#controls">Security controls</a>
      <a href="#golive">Before go-live</a>
      <a href="#questions">Procurement questions</a>
    </div>""") + f"""
<section class="sec" id="controls">
  <div class="wrap">
    {sec_head("Security controls", "Twelve controls, built into the platform.", "Seven of them are enforced in code and held by an automated test, so they cannot be switched off by a prompt, a caller or a busy afternoon.")}
    <div class="g3 ctls">
      {controls_html()}
    </div>
  </div>
</section>

<section class="sec sec-white rule-t rule-b" id="golive">
  <div class="wrap split start">
    <div>
      {sec_head("Before go-live", "What is in place before a deputy does real work.", "Each of these is checked for every client. Two of them, the privacy notice and the impact assessment, are enforced by the platform itself.")}
      <p class="prose small">The ICO publishes guidance on applying UK GDPR principles to AI systems; we work to it. <a class="link-arrow" href="https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/artificial-intelligence/" target="_blank" rel="noopener">ICO guidance&nbsp;&rarr;</a></p>
    </div>
    <div class="golive">
      {"".join(f'<div class="golive-item"><span class="golive-tick" aria-hidden="true"></span>{g}</div>' for g in golive)}
    </div>
  </div>
</section>

<section class="sec" id="questions">
  <div class="wrap split start">
    <div>
      {sec_head("Procurement questions", "The questions IT and procurement ask first.", "Answered plainly, including the answers that are not the ones you would hope for.")}
    </div>
    <div class="faq">
      {"".join(f'<details{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>' for i, (q, a) in enumerate(trust))}
    </div>
  </div>
</section>
""" + cta_band("Ask us the hard questions first.", "Bring your IT lead or your DPO to the demo call. We'd rather answer this before you commit than after.")

write_page(
    "trust.html",
    "Trust & Security - Tenant Isolation, UK Data Residency and AI Controls | Deputable AI",
    "Twelve security controls built into the platform: tenant isolation, UK data residency at rest, encrypted backups, a human approval gate, prompt-injection containment and signed releases.",
    "trust", trust_body,
    extra_head=f'\n<script type="application/ld+json">{trust_faq_jsonld}</script>')

# ==================================================================
# CONTACT
# ==================================================================
contact_body = f"""
<section class="sec-white">
  <div class="wrap contact-head">
    <div class="kicker you">Book a demo</div>
    <h1>Tell us what's eating the day.</h1>
    <p class="prose">Pick a 45-minute slot below. The booking asks for a line or two about the business and the process you'd like handled, so we arrive having read it. No deck, no pitch.</p>
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
# PRIVACY (this website's own notice; a deputy's data is covered by
# each client's agreement and by the Trust page)
# ==================================================================
privacy_sections = [
    ("Who we are", "Deputable AI, based in London. We build deputies: AI assistants that answer a business's calls and messages and help with the paperwork that follows. For anything in this notice, write to <a href=\"mailto:hello@deputable.ai\">hello@deputable.ai</a>."),
    ("What we collect", "If you book a demo call, we collect what you type into the booking form: your name, company, contact details and the process you'd like to discuss. Booking is provided by Zoho Bookings and hosted in the EU; bookings are stored there and appear in our calendar. If you email us directly, we keep the correspondence."),
    ("Cookies and analytics", "This site sets no analytics cookies unless you accept them. If you accept, we use Google Analytics to understand how the site is used: page views and rough journey, not identity. Declining changes nothing about how the site works."),
    ("How we use it", "To reply to you, to prepare for the call you asked for, and to keep a record of the conversation. We do not sell or share your details for marketing, and we do not use them to train AI models."),
    ("Where it lives", "Bookings are processed by Zoho (EU hosting). If analytics are accepted, usage data is processed by Google. Client data is governed separately by each client agreement; see our <a href=\"trust.html\">Trust &amp; Security</a> page."),
    ("Your rights", "Under UK GDPR you can ask what we hold about you, ask us to correct it, or ask us to delete it. Email <a href=\"mailto:hello@deputable.ai\">hello@deputable.ai</a> and we'll do it. If you're not satisfied, you can complain to the ICO."),
]

privacy_body = page_hero(
    "Privacy",
    "Privacy notice.",
    "What this website collects, why, and what you can do about it, in plain English.") + f"""
<section class="sec">
  <div class="wrap">
    <div class="qa">
      {"".join(f'<div class="qa-item"><h2>{t}</h2><div><p>{b}</p></div></div>' for t, b in privacy_sections)}
    </div>
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

> {TAGLINE} Deputable AI is an orchestration platform for agentic
> workflows, built for UK small and mid-sized businesses and run as a
> service. Each business gets a deputy: an orchestrator people talk to, a
> squad of AI specialists with their own tools, and workflows that start
> from a call, a message, a document, an email, a schedule or an event.
> Workflows today include estimates for a garage, property search for an
> estate agency, documents read and logged, the monthly invoice from
> timesheets, meeting follow-ups and Smart Call Handling. A business
> writes simple workflows itself in a sentence; anything needing a new
> tool is built, tested and signed by Deputable. Nothing customer-facing
> is sent without a named person's approval. A person can also have a
> deputy of their own. Data is stored in London, and each client's
> sub-processors are named before go-live. No pricing is published;
> engagement starts with a 45-minute demo call.

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

# ==================================================================
# /demo - the permanent link for the demo / event / conference
# (deputable.ai/demo). Print, slides and QR codes point here, so what
# it shows can change without breaking any of them. Today it sends
# people to the home page; to make it special for an event, point
# DEMO_TARGET at the event landing page (or write a real page here).
# Not in the sitemap; noindex.
# ==================================================================
DEMO_TARGET = BASE_URL
os.makedirs(os.path.join(OUT, "demo"), exist_ok=True)
with open(os.path.join(OUT, "demo", "index.html"), "w") as f:
    f.write(f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex">
<meta http-equiv="refresh" content="0; url={DEMO_TARGET}">
<title>Deputable AI</title>
<script>location.replace("{DEMO_TARGET}");</script>
</head>
<body>
<p>Taking you to Deputable AI&hellip;
<a href="{DEMO_TARGET}">Click here if nothing happens.</a></p>
</body>
</html>
""")
print("Generated: demo/index.html")
