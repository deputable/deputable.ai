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
    ("business.html", "business", "Business"),
    ("personal.html", "personal", "Personal"),
    ("features.html", "features", "Features"),
    ("how-it-works.html", "process", "How it works"),
    ("trust.html", "trust", "Trust"),
    ("about.html", "about", "About"),
]

SITE_TITLE = "Deputable AI - A deputy for your business: Smart Call Handling, WhatsApp and the paperwork"
SITE_DESC = ("A deputy answers your business's calls and WhatsApp in your name, writes up every one "
             "and drafts the quote or the reply. Nothing reaches a customer until a person says ok. "
             "Built and run in London.")

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
    ("business.html", "A deputy for your business"),
    ("personal.html", "A deputy of your own"),
    ("features.html", "Everything it does"),
    ("how-it-works.html", "How it works"),
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
        <p>A deputy for your business, and one of your own. Built and run from London, with a person in charge of every decision that matters.</p>
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
# The thread demo (homepage hero). Each scenario is a real, built flow
# shown as the messages a person sees on their phone. Messages are in
# the HTML from the start, so the page reads without JavaScript;
# js/main.js only reveals them in turn and switches the tabs.
# Blue = the deputy. Coral = the person's own words and decisions.
# ------------------------------------------------------------------
def _msg(kind, body, at="", who="", plain=False):
    cls = f"msg {kind}" + (" plain" if plain else "")
    at_html = f'<span class="at">{at}</span>' if at else ""
    who_html = f'<span class="who"><span>{who}</span>{at_html}</span>' if (who or at) else ""
    return f'<div class="{cls}">{who_html}{body}</div>'


def _sys(text, you=False):
    return f'<div class="sys{" you" if you else ""}">{text}</div>'


_EST = """<div class="est">
  <div class="est-title">BMW 320d, 2019: front brakes</div>
  <div class="est-row"><span>Discs, pads and wear sensor</span><span class="p">&pound;150.40</span></div>
  <div class="est-row"><span>Labour, 1.6 h</span><span class="p">&pound;136.00</span></div>
  <div class="est-row"><span>VAT</span><span class="p">&pound;57.28</span></div>
  <div class="est-total"><span>Total</span><span class="p">&pound;343.68</span></div>
  <div class="est-note">Parts: eBay, 10:46 today. Labour: starter times.</div>
</div>"""

DEMO_SCENARIOS = [
    {
        "tab": "After a call",
        "name": "Your garage's deputy",
        "via": "On your WhatsApp",
        "msgs": [
            _msg("deputy", "Sam Taylor (07700 900461). BMW 320d, AB12 CDE. Grinding from the front brakes. Wants a price and a slot this week, after 4pm. <b>Call back owed.</b>", "10:47", "Message taken"),
            _msg("deputy", "Draft estimate <b>P14 v1</b> from that call. Reply <code>ok P14</code> to accept it, <code>drop P14</code> to bin it, or tell me what to change." + _EST, "10:48", "Waiting for you"),
            _msg("you", "ok P14", "10:52", "You"),
            _sys("Approved by you &middot; version 1 &middot; 10:52", you=True),
        ],
    },
    {
        "tab": "A photo of a bill",
        "name": "Your deputy",
        "via": "On your WhatsApp",
        "msgs": [
            _msg("you", "Photo &middot; IMG_2041.jpg", "09:12", "You sent"),
            _msg("deputy", "That looks like a <b>supplier invoice</b>: Brightwell Plumbing, INV-2041, <b>&pound;153.00</b>. I was unsure of the due date and read it as 15 October. Kept as <b>S1</b> for your ok.", "09:13", "Read and sorted"),
            _msg("you", "S1 due 22 October", "09:14", "You"),
            _msg("deputy", "<b>S1 v2</b>: due 22 October. Reply <code>ok S1</code> to keep it as a bill.", "09:14", "New version"),
            _msg("you", "ok S1", "09:15", "You"),
            _msg("deputy", "Kept as a bill: Brightwell Plumbing, &pound;153.00, due 22 October. One row in your ledger.", "09:15", "Done"),
        ],
    },
    {
        "tab": "Your own inbox",
        "name": "Your deputy",
        "via": "On your WhatsApp",
        "msgs": [
            _msg("deputy", "From the venue, 14:02: they need final numbers for Thursday by 5pm today.", "14:05", "Mail that can't wait"),
            _msg("you", "Draft a reply: 120 of us, and ask if the car park opens at 8", "14:07", "You", plain=True),
            _msg("deputy", "Draft kept on the thread, everyone in copy:<br><i>&ldquo;Hi Dana, we will be 120 on Thursday. Is the car park open from 8am?&rdquo;</i><br>Say <code>send</code> to send it as it stands.", "14:08", "Draft, not sent"),
            _msg("you", "send", "14:09", "You"),
            _sys("Sent from your own address &middot; once &middot; 14:09", you=True),
        ],
    },
]


def thread_demo():
    tabs = "".join(
        f'<button type="button" class="demo-tab" role="tab" id="demo-tab-{i}" aria-controls="demo-panel-{i}" '
        f'aria-selected="{"true" if i == 0 else "false"}" data-demo-tab="{i}">{s["tab"]}</button>'
        for i, s in enumerate(DEMO_SCENARIOS)
    )
    panels = "".join(
        f'<div class="thread-panel{" is-active" if i == 0 else ""}" role="tabpanel" id="demo-panel-{i}" '
        f'aria-labelledby="demo-tab-{i}" data-demo-panel data-name="{s["name"]}" data-via="{s["via"]}">'
        + "".join(s["msgs"]) + "</div>"
        for i, s in enumerate(DEMO_SCENARIOS)
    )
    first = DEMO_SCENARIOS[0]
    return f"""<div class="demo" data-demo>
      <div class="demo-tabs" role="tablist" aria-label="Three things a deputy does">{tabs}</div>
      <div class="thread">
        <div class="thread-head">
          <div class="thread-avatar"><img src="assets/icon-192.png?v={ASSET_VER}" alt="" width="26" height="26"></div>
          <div>
            <div class="thread-name" data-demo-name>{first["name"]}</div>
            <div class="thread-via" data-demo-via>{first["via"]}</div>
          </div>
        </div>
        <div class="thread-panels">{panels}</div>
      </div>
      <p class="demo-caption">An illustration. The people, the car and the prices are made up.</p>
    </div>"""


# ------------------------------------------------------------------
# What a deputy does, said once and used on several pages.
# ------------------------------------------------------------------
# (for whom, title, status, body)
WORKFLOWS = [
    ("Garages", "Estimates for a garage", "live",
     "The vehicle, the repair, the labour and the parts, totalled with VAT in code and drafted a minute or two after the call for you to check. Parts are priced live from eBay today, with starter labour times; licensed data is next."),
    ("Estate agents", "Property search", "live",
     "A caller asks for a two-bed to rent near the station. Your deputy searches your own live listings, reads the matches back, and takes the lead. If there is nothing in that town it says so and offers the ones nearby."),
    ("Any business", "A photo becomes a bill", "built",
     "Send a supplier invoice or a letter as a photo. It is read, sorted, its figures pulled out and put to you, with what it was unsure of. Your ok writes one row in the ledger."),
    ("Contractors", "The monthly invoice", "live",
     "Timesheet screenshots in, last month's invoice as the template. The Word file, the PDF and the covering email are drafted for you to check. Nothing is sent."),
    ("Any business", "Meeting follow-ups", "built",
     "Send a recording. Back come a summary, the decisions, and who owes what by when. Each follow-up waits for your ok before anyone outside hears from it."),
    ("Any business", "Yours, in your words", "built",
     "&ldquo;When a message is taken, text me and raise a call back.&rdquo; Describe a workflow, your deputy draws it, and you turn it on."),
]


def workflow_cards():
    return "".join(
        f'<div class="card"><div class="top"><span class="for">{who}</span>{status(st)}</div>'
        f'<h3>{title}</h3><p>{body}</p></div>'
        for who, title, st, body in WORKFLOWS
    )


# Shared by the homepage and About page - keep the two in step.
depute_items = [
    "Answering calls out of hours and on a busy line",
    "Taking messages and writing up every call",
    "Keeping track of every call back you owe",
    "Drafting estimates, replies and invoices",
    "Reading and sorting the photos and PDFs you send",
    "Reminders, diaries and the mail that can't wait",
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
doors_home = [
    ("phone", "Phone", "live", "A UK number answered in your business's name. Or keep the number your customers know and forward it when you're busy or closed.", ""),
    ("chat", "WhatsApp", "live", "Customers message the business and get an answer. Your notes, drafts and approvals arrive on your own WhatsApp.", "Meta checks each business before its number goes on WhatsApp. It takes a few days and we handle it."),
    ("text", "Text", "live", "What was agreed on the call, sent to your customer in writing, only if they said yes. STOP is honoured at once.", ""),
    ("page", "Your pages", "built", "Sign in with a code sent to your phone. What waits for you, recent conversations, your workflows and your usage.", ""),
]

callmap = [
    ("Before the first word", "It reads up.", [
        (False, "<b>Who is calling.</b> Your staff are greeted by name. A customer is answered as the business."),
        (False, "<b>What happened last time.</b> The last call, the notes, what was promised."),
        (False, "<b>Your rules.</b> Hours, services and standing rules in your own words: &ldquo;never give a price&rdquo;."),
    ]),
    ("On the call", "It answers as you.", [
        (False, "<b>Says what it is.</b> The greeting names your business, says it is an AI assistant and that the call is recorded."),
        (False, "<b>Answers what it safely can</b> from your own facts, and says so when it can't."),
        (False, "<b>Takes it down properly.</b> Who, the number, what is wrong, what they want."),
        (True, "<b>They ask for a person.</b> It holds the caller and rings your mobile. If you can't take it, a call back is promised."),
    ]),
    ("After the call", "It writes it up.", [
        (False, "<b>A note on your WhatsApp</b> as the call ends: who rang, why, what was promised."),
        (False, "<b>Your customer gets it in writing</b>, by text, only if they said yes."),
        (False, "<b>A promised call back</b> becomes an item that waits until it is done."),
        (True, "<b>Any draft waits for your ok.</b> An estimate, a reply, an invoice. Nothing goes on its own."),
    ]),
]


def callmap_html():
    cols = ""
    for when, title, steps in callmap:
        items = "".join(
            f'<div class="callstep{" you" if you else ""}">{text}</div>' for you, text in steps
        )
        cols += f'<div class="callcol"><div class="when">{when}</div><h3>{title}</h3><div class="callsteps">{items}</div></div>'
    return f"""<div class="callmap">{cols}</div>
    <div class="legend"><span><i></i>Your deputy does it</span><span><i class="you"></i>A person decides</span></div>"""


personal_teaser = [
    "<b>Your inbox, by voice.</b> Found, read aloud, replied to on your yes.",
    "<b>Every diary in one answer</b>, with clashes flagged.",
    "<b>Reminders</b> by text, or a call, at the time you set.",
    "<b>&ldquo;Remember that.&rdquo;</b> Lists and facts, kept and recalled.",
    "<b>Journeys</b> with real times, and when to leave.",
    "<b>&ldquo;Call my brother.&rdquo;</b> It rings you back and puts you through.",
]

facts_home = [
    ("London", "Your deputy's record lives on our server in Oracle Cloud's London region, on disks encrypted at rest."),
    ("Yours alone", "One folder and one database for each business. Nothing is shared with any other client."),
    ("Backed up hourly", "Encrypted with a key our servers never hold. Restores are rehearsed, not assumed."),
    ("You set what we see", "Nothing, a limited view with no call transcripts, or everything, with who, why and until when written down."),
    ("Export or erase", "One person's data or all of it, on request. Take it with you if you leave."),
    ("Signed releases", "Only software one of us has signed reaches the servers."),
]

home_steps = [
    (False, "01", "A 45-minute call", "Bring one process. We'll tell you straight whether a deputy is the answer."),
    (False, "02", "We draw it", "Your hours, people, rules and workflows, drawn and reviewed with you before anything is built."),
    (False, "03", "Test calls", "We ring it as a stranger and as you, until it answers the way you would."),
    (True, "04", "You say go", "No real caller reaches your deputy until you have read it all and confirmed."),
]

home_body = f"""
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <div class="eyebrow">Simplify work &middot; Amplify people</div>
      <h1 class="hero-title"><span>Delegate the busywork.</span> <span>Own the <span class="yours">decisions.</span></span></h1>
      <p class="hero-sub">A deputy answers your business's calls and messages in your name, writes up every one, and drafts the quote or the reply. Nothing reaches a customer until you say ok.</p>
      <div class="hero-ctas">
        <a class="btn btn-primary" href="contact.html">Book a demo call <span class="arr" aria-hidden="true">&rarr;</span></a>
        <a class="btn btn-secondary" href="business.html">See what it does</a>
      </div>
      <div class="hero-foot">
        <span>Phone, WhatsApp and text</span>
        <span class="you">A person approves what customers see</span>
        <span>Built and run in London</span>
      </div>
    </div>
    {thread_demo()}
  </div>
</section>

<section class="sec">
  <div class="wrap">
    {sec_head("One deputy", "Every way your customers reach you.", "The same deputy on every line, working from one record. A customer who rang on Monday and messages on Thursday never has to start again.")}
    <div class="doors">
      {"".join(f'<div class="door"><div class="door-top"><div class="ic">{ICONS[ic]}</div>{status(st)}</div><h3>{t}</h3><p>{b}</p>' + (f'<p class="fine">{fine}</p>' if fine else "") + '</div>' for ic, t, st, b, fine in doors_home)}
    </div>
  </div>
</section>

<section class="sec sec-white rule-t rule-b" id="call">
  <div class="wrap">
    {sec_head("Smart Call Handling", "What happens when the phone rings.", "Your deputy covers for your team and backs it up. It takes no one's place. Where a step belongs to a person, it stops and waits.")}
    {callmap_html()}
    <div class="sec-foot"><a class="link-arrow" href="business.html#smart-call-handling">Smart Call Handling in full&nbsp;&rarr;</a></div>
  </div>
</section>

<section class="sec" id="approve">
  <div class="wrap split start">
    <div>
      <div class="kicker you">You stay in charge</div>
      <h2>One word from your phone.</h2>
      <p class="prose" style="margin-top:18px">Drafts wait for you. Reply ok to accept one, drop to bin it, or just say what to change and it comes back as a new version. From WhatsApp, a text, or your own pages.</p>
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

<section class="sec sec-white rule-t rule-b" id="work">
  <div class="wrap">
    {sec_head("Workflows", "Work it already does.", "Each of these is running or built today, and each carries its true status. More are added with you, one at a time, drawn before they are built.")}
    <div class="g3">
      {workflow_cards()}
    </div>
    <div class="sec-foot"><a class="link-arrow" href="features.html">Everything it does, and where each thing stands&nbsp;&rarr;</a></div>
  </div>
</section>

<section class="sec">
  <div class="wrap split">
    <div>
      <div class="kicker">A deputy of your own</div>
      <h2>And one for you.</h2>
      <p class="prose" style="margin-top:18px">For your mail, your diary and the things you'd forget. Ring it or message it. It drafts and reminds and looks things up, and it never sends anything in your name without your say-so.</p>
      <div class="sec-foot"><a class="link-arrow" href="personal.html">A deputy of your own&nbsp;&rarr;</a></div>
    </div>
    <div class="card">
      {ticks(personal_teaser)}
    </div>
  </div>
</section>

<section class="sec sec-tint rule-t" id="learns">
  <div class="wrap split">
    <div>
      <div class="kicker">It learns how you work</div>
      <h2>The more you use it, the more it works your way.</h2>
      <p class="prose" style="margin-top:18px">Each night your deputy looks back over what you changed. When you make the same change to its drafts three times in five, it proposes a lesson. You keep it, make it a rule, or dismiss it for good.</p>
      <p class="prose">Nothing about how it works changes without your say.</p>
      <p style="margin-top:20px">{status("built")}</p>
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
    {sec_head("Trust &amp; Security", "Your numbers and your data stay yours.", "Plain answers for whoever has to sign this off, including which suppliers handle a call outside the UK.")}
    <div class="facts">
      {"".join(f'<div class="fact"><div class="big">{t}</div><p>{b}</p></div>' for t, b in facts_home)}
    </div>
    <div class="sec-foot"><a class="link-arrow" href="trust.html">The questions IT and procurement ask first&nbsp;&rarr;</a></div>
  </div>
</section>

<section class="sec">
  <div class="wrap split start">
    <div>
      <h2>No logo wall. Not yet.</h2>
      <p class="prose" style="margin-top:18px">We're a new company, and we won't decorate this page with invented numbers or testimonials we don't have. What we do have: deputies answering a live UK number today, a record you can audit for every call and every draft, and a rule that your data leaves with you if you do.</p>
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

<section class="sec sec-white rule-t">
  <div class="wrap">
    {sec_head("How it starts", "Drawn first. Tested on us. Live when you say.")}
    <div class="steps">
      {"".join(f'<div class="step{" you" if you else ""}"><div class="meta">{n}</div><h3>{t}</h3><p>{b}</p></div>' for you, n, t, b in home_steps)}
    </div>
    <div class="sec-foot"><a class="link-arrow" href="how-it-works.html">How it works, step by step&nbsp;&rarr;</a></div>
  </div>
</section>
""" + cta_band("See it against your own process.", "Forty-five minutes, one workflow of your choosing, no deck.")

write_page("index.html", SITE_TITLE, SITE_DESC, "home", home_body)

# ==================================================================
# BUSINESS
# ==================================================================
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
    "Takes the message and captures the lead",
    "Asks before texting your customer what was agreed",
    "Puts a caller through to a named person",
    "Says so when it doesn't know, and takes a message",
]

message_points = [
    "<b>Customers message the business</b> on WhatsApp and get an answer, on the same record as their calls.",
    "<b>Your own WhatsApp</b> carries the notes, the drafts and your approvals.",
    "<b>The text after a call</b> goes once, with the caller's yes.",
    "<b>STOP is honoured at once.</b> START brings texts back.",
    "<b>No WhatsApp?</b> Your people get the same by text.",
]

commands = [
    ("ok P14", "Accept the draft, as the version you read."),
    ("drop P14", "Bin it. Add a reason if you like; it is kept."),
    ("show P14", "See it again, and how to answer it."),
    ("P14 labour is 2 hours", "Say what to change. A new version comes back for your ok."),
    ("resend P14", "Try again a send that failed. Only a person can."),
    ("send", "Send your latest email draft as it stands."),
    ("rate &pound;75 &nbsp; markup 20%", "For a garage: the labour rate and parts markup your estimates use."),
    ("new workflow: when&hellip;", "Describe a workflow. Your deputy draws it for you to turn on."),
]

next_business = [
    "Bookings into your diary, on the call",
    "A weekly digest of calls and call backs kept",
    "&ldquo;On a job until three&rdquo;: a busy flag from your phone",
    "Licensed parts and labour data, through your own access",
]

business_body = page_hero(
    "For your business",
    "Every call answered in your name. Every decision still yours.",
    "Smart Call Handling, WhatsApp and the paperwork that follows a call. Run for you as a service, approved by you from your phone.",
    """
    <div class="hero-ctas">
      <a class="btn btn-primary" href="contact.html">Book a demo call <span class="arr" aria-hidden="true">&rarr;</span></a>
      <a class="btn btn-secondary" href="features.html">Everything it does</a>
    </div>""") + f"""
<section class="sec" id="smart-call-handling">
  <div class="wrap">
    {sec_head("Smart Call Handling", "The phone, handled. Three ways.", "Jobs are won and lost on the phone, and most are lost quietly: after hours, on a busy line, in a voicemail nobody checks. Your deputy covers for your team and backs it up. It takes no one's place.")}
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

<section class="sec sec-white rule-t rule-b" id="messages">
  <div class="wrap split">
    <div>
      <div class="kicker">WhatsApp and text</div>
      <h2>The same deputy, in writing.</h2>
      <p class="prose" style="margin-top:18px">The enquiry that starts as a message is the same enquiry that would have been a phone call, so it is treated the same way: answered from your business information, written up, and put in front of the right person.</p>
      <p class="prose small">Meta checks each business before its own number goes on WhatsApp. It takes a few days and we handle it. Calls from the WhatsApp chat are built and in testing.</p>
    </div>
    <div class="card">
      {ticks(message_points)}
    </div>
  </div>
</section>

<section class="sec" id="note">
  <div class="wrap split">
    <div class="thread" aria-label="An example of a note after a call">
      <div class="thread-head">
        <div class="thread-avatar"><img src="assets/icon-192.png?v={ASSET_VER}" alt="" width="26" height="26"></div>
        <div>
          <div class="thread-name">Your deputy</div>
          <div class="thread-via">Note &middot; call ended 18:42 &middot; 4 min</div>
        </div>
      </div>
      <div class="thread-panels"><div class="thread-panel is-active">
        <div class="msg deputy" style="max-width:100%"><span class="who">Summary</span>Jo Reed rang about a two-bed flat to rent near the station, from January. Three listings read out. Wants a viewing on Saturday morning.</div>
        <div class="msg deputy" style="max-width:100%"><span class="who">Promised</span>A call back tomorrow before noon to fix the viewing.</div>
        <div class="msg deputy" style="max-width:100%"><span class="who">Lead</span>Jo Reed, 07700 900118. Renting, two beds, up to &pound;1,600 a month. Said yes to a text.</div>
        <div class="sys you">Call back owed &middot; due tomorrow 09:00</div>
      </div></div>
    </div>
    <div>
      <div class="kicker">After every contact</div>
      <h2>A note, not a voicemail.</h2>
      <p class="prose" style="margin-top:18px">Every call and every quiet message thread ends with a note on your phone: who it was, what they wanted, what was promised and whether a call back is owed. The note says a thing was done only when the record shows it was.</p>
      <p class="prose">A promised call back becomes an item at your next opening, created by code whatever the note says. It waits until someone has made the call.</p>
      <p class="demo-caption" style="text-align:left">An illustration. The caller and the details are made up.</p>
    </div>
  </div>
</section>

<section class="sec sec-white rule-t rule-b" id="approve">
  <div class="wrap split start">
    <div>
      <div class="kicker you">Approvals</div>
      <h2>Approve with one word.</h2>
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

<section class="sec" id="workflows">
  <div class="wrap">
    {sec_head("Workflows", "The work behind the call.", "A workflow is a known piece of work with its steps drawn out and an approval wherever a mistake would reach a customer or a payment. These exist today.")}
    <div class="g3">
      {workflow_cards()}
    </div>
    <div class="split start" style="margin-top:56px">
      <div class="panel">
        <h3>Built around one process of yours</h3>
        <p>Your estimates, your paperwork and your follow-ups don't run off the shelf, so a workflow only your business needs is drawn with you first, reviewed, and then built. One at a time, each with its approval steps marked before a line of it exists.</p>
        <p>Where a site you rely on has no way in for software, the plan is for your deputy to use it as you do, in a browser you sign in to yourself, reading and never buying.</p>
      </div>
      <div class="card dashed">
        <div class="top"><span class="for">Agreed, not built yet</span>{status("next")}</div>
        {ticks(next_business, "todo")}
      </div>
    </div>
  </div>
</section>

<section class="sec sec-tint rule-t" id="team">
  <div class="wrap">
    {sec_head("Your team", "It knows who is who.", "A customer, a member of staff and the owner are different people to your deputy, and it treats them differently.")}
    <div class="g3">
      <div class="card">
        <h3>Your people</h3>
        <p>Owner, staff, technician. Your people are greeted by name when they ring, can hand work to the deputy, and only the ones you name may approve what reaches a customer.</p>
      </div>
      <div class="card">
        <div class="top"><h3>Your pages</h3>{status("built")}</div>
        <p>Sign in with a code sent to your phone. What waits for you, recent conversations, calls, workflows, and every minute you pay for.</p>
      </div>
      <div class="card">
        <h3>Your rules</h3>
        <p>Write &ldquo;remember that we close at one on Saturdays&rdquo; and it does, on every call from then on. Your standing rules are plain sentences you can read, not settings in a menu.</p>
      </div>
    </div>
  </div>
</section>
""" + cta_band("Hear it answer as your business.", "Forty-five minutes, one workflow of your choosing, no deck.")

write_page(
    "business.html",
    "A Deputy for Your Business - Smart Call Handling, WhatsApp & Workflows | Deputable AI",
    "Calls answered in your business's name out of hours and on a busy line, a note after every one, drafts that wait for your ok, and workflows such as estimates and property search.",
    "business", business_body)

# The old Services page: its links and search results keep working.
write_redirect("services.html", "business.html", "A deputy for your business - Deputable AI")

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
# checked against that list. A row's status must match the list:
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
    ("On the call", "Smart Call Handling: out of hours, on a busy line, and through to you.", [
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
        ("ACC-02", "A folder and a database of your own", "live", "Each business's record is kept apart from every other's, on our server in London."),
        ("ACC-06", "Hourly encrypted backups", "live", "Encrypted with a key our servers never hold. Restores are rehearsed."),
        ("ACC-03", "You decide what we can see", "live", "Nothing, a limited view with no call transcripts, or everything, with who, why and until when written down."),
        ("ACC-01", "Roles", "live", "Owner, staff, technician and monitor. What each may ask for and approve is set per business."),
        ("ACC-05", "Export and erasure", "live", "One person's data exported, or erased across the record, the recordings and our telephony supplier's copies."),
        ("ACC-04", "Paperwork as a gate", "live", "A business can't go live without a privacy notice and a dated impact assessment. The software refuses."),
        ("OPS-02", "Signed releases", "live", "Our servers run only software one of us has signed."),
        ("OPS-14", "Every minute you pay for", "built", "A usage page for whoever pays: minutes, messages and finished jobs this month."),
        ("RES-UKEU", "UK and EU only", "next", "Every part of a call kept inside the UK and EU. Not offered until all of it can be."),
        ("OPS-12", "A server of your own", "next", "For a client whose data must share no machine with anyone else's."),
    ]),
]


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
    "No roadmap dressed up as a product. Every capability is marked as live, built, or next, and the marks are kept in step with our own engineering list.",
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
     "Your deputy's facts and rules, your people, your number. A privacy notice for your callers and a data protection impact assessment, because your deputy cannot go live without them. The software refuses.",
     "A deputy on a test line, a privacy notice, and a dated assessment."),
    (False, "05", "Us, then you", "Test calls",
     "We ring it as a stranger and as you. The stranger is greeted as your business and told it is an AI assistant, asks for a price and is told you will call back, and the note lands on your phone. Then you try to break it.",
     "The notes from the test calls, and what we changed after them."),
    (True, "06", "You", "You say go",
     "You read the facts, the rules and the drawings, and confirm. Until you do, no real caller reaches your deputy. It starts as a trial on your own calls, usually with your existing number forwarded when you're busy or closed.",
     "A deputy answering your calls, and a restore rehearsed from its backup."),
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
    "How it works",
    "From a first call to your deputy answering.",
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
      <p>We keep reading what the calls show and fix what they turn up. New workflows are added one at a time, each drawn first. Your deputy proposes lessons from the changes you make to its drafts, and you decide which to keep.</p>
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
    "How It Works - From a First Call to Your Deputy Answering | Deputable AI",
    "Six steps: a demo call, intake, your workflows drawn, set up and privacy paperwork, test calls, and your go-ahead. Nothing takes a real call until you have confirmed it.",
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
    {sec_head("The line", "Some work is deputable. Some never will be.", "A good deputy takes the routine off your desk and brings you the decisions. That's the standard we hold ours to. It answers the phone at seven in the evening, takes the details down properly, drafts the estimate, chases the paperwork. Then it stops, because the next step belongs to a person.")}
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
      <p class="prose" style="margin-top:18px">Every business runs differently, so a deputy is set up around yours: your hours, your people, your rules in your own words. We do the intake, draw the workflows with you, handle the privacy paperwork and keep reading what the calls show. Your staff give approvals from their phones.</p>
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
# not yet true) before publishing it. Two claims are deliberately NOT
# made yet: a UK-and-EU-only option, and the AI suppliers' no-training
# terms (ours is stated; theirs waits on the confirmed contracts).
# ==================================================================
trust = [
    ("Where does our data live?",
     "On our server in Oracle Cloud's London region, on disks encrypted at rest. Each business has its own folder and its own database, shared with no other client. The backups stay in London too."),
    ("Does any of it leave the UK?",
     "Yes, and you should know exactly where. A phone call has to be carried, heard and understood, and the suppliers who do that for us process it in the United States today: the telephone network, the voice on the call, and the AI models that read and write. Each one is named in your agreement before you go live. A UK and EU only option is being built. We won't offer it until every part of a call can stay inside it."),
    ("Do you train AI models on our data?",
     "No. We don't train models at all. Your data is used to serve you and nobody else. It is never sold and never used for advertising."),
    ("Can it send something to a customer on its own?",
     "No. Anything a customer will see waits for a named person at your business. Your approval covers the version you read, and a change comes back as a new version. Each message goes once; if we can't tell whether it was delivered, a person decides before it is tried again. These are rules in the code, each held by an automated test, not instructions we hope a model follows."),
    ("Could a caller or an email trick it?",
     "Words from outside, such as what a caller says, an email or a web page, are treated as untrusted. They can inform a draft for you to read. They cannot make your deputy send a message or change a record. Who a follow-up goes to is fixed in your configuration and is never chosen by a model."),
    ("Who at Deputable can see our calls and messages?",
     "You choose, per business. Nothing at all. A limited view, which is the default: the steps your deputy took and the written messages it exchanged with customers, but no call transcripts and nothing it read in your mail or diary. Or everything, with the person, the reason and the end date written down."),
    ("Are calls recorded, and do callers know?",
     "By default yes, and the greeting says so in its opening sentence, along with the fact that the caller is speaking with an AI assistant. You can turn recording off. Unless you choose otherwise, recordings are kept for 30 days and notes and transcripts for 90."),
    ("What happens if it gets something wrong?",
     "Every call and every job leaves a record: what was heard, which tools were used, what was drafted, who approved it and when. An error can be traced to its step. Your record is backed up hourly, encrypted with a key our servers never hold, and we rehearse restoring from it. Recordings stay on the server and are not in the backups."),
    ("Can we get our data out, or have it deleted?",
     "Yes. Everything exports in full and goes with you if you leave. One person's data can be exported or erased on request: the record, the recordings and the copies our telephony supplier holds. Encrypted backups can't be edited, so they expire on their own within 90 days."),
]

# The main suppliers, with where each processes data. The complete list
# for one deputy is generated from its configuration (`deputy residency
# <deputy> --markdown` in the platform) and belongs in the client's
# agreement; keep this table in step with the DPA's annex.
suppliers = [
    ("Oracle", "Our servers and backups", "UK (London)"),
    ("Twilio, and Meta for WhatsApp", "Phone calls, texts and WhatsApp", "US"),
    ("Anthropic", "The AI models that read and write", "US"),
    ("OpenAI", "The voice on a call", "US"),
    ("ElevenLabs", "Spoken set lines, and turning speech into text", "US"),
    ("Zoho", "Mail and diary for some deputies, and our staff sign-in", "EU"),
    ("Google", "Journey times, and your account only if you connect it", "US"),
]

deployment_includes = [
    "Callers are told when they're talking to an AI assistant",
    "A route to a person, or a promised call back, on every call",
    "A named person approves anything customer-facing",
    "A record of every call, message, draft and approval",
    "A privacy notice and a dated impact assessment before go-live",
    "Opt-outs honoured: STOP stops texts at once",
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
    "Your data is your own.",
    "Where does it go, and who can act on it? The questions IT and procurement ask us first, answered plainly, including the answers that are not the ones you'd hope for.") + f"""
<section class="sec">
  <div class="wrap">
    <div class="qa">
      {"".join(f'<div class="qa-item"><h2>{q}</h2><div><p>{a}</p></div></div>' for q, a in trust)}
    </div>
  </div>
</section>

<section class="sec sec-white rule-t rule-b" id="suppliers">
  <div class="wrap split start wide-left">
    <div>
      {sec_head("Suppliers", "Which other companies touch our data?", "The main ones, and where each processes it. The complete list for your own deputy, including the smaller services, is generated from its configuration and given to you before you go live.")}
      <div class="table-wrap">
        <table class="plain">
          <thead><tr><th>Supplier</th><th>For</th><th>Where</th></tr></thead>
          <tbody>
            {"".join(f"<tr><td>{s}</td><td>{f}</td><td>{w}</td></tr>" for s, f, w in suppliers)}
          </tbody>
        </table>
      </div>
    </div>
    <div>
      <div class="mono-label" style="display:block;margin-bottom:16px">What every deployment includes</div>
      {ticks(deployment_includes)}
      <p class="prose small" style="margin-top:24px">The ICO publishes guidance on applying UK GDPR principles to AI systems; we work to it. <a class="link-arrow" href="https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/artificial-intelligence/" target="_blank" rel="noopener">ICO guidance&nbsp;&rarr;</a></p>
    </div>
  </div>
</section>
""" + cta_band("Ask us the hard questions first.", "Bring your IT lead or your DPO to the demo call. We'd rather answer this before you commit than after.")

write_page(
    "trust.html",
    "Trust & Security - Your Data Is Your Own | Deputable AI",
    "Where your data lives, what leaves the UK and why, who can see it, and what your deputy can never do on its own. The questions IT and procurement ask first, answered plainly.",
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

> {TAGLINE} Deputable AI builds and runs deputies for UK small and
> mid-sized businesses. A deputy answers a business's phone and WhatsApp
> in its name (Smart Call Handling: out of hours, on a busy line, and
> put through to a person), writes a note after every contact, texts the
> customer what was agreed with their consent, and drafts work such as a
> garage estimate or a monthly invoice for a person to approve with one
> word. Nothing customer-facing is sent without a named person's
> approval. A person can also have a deputy of their own for mail, diary,
> reminders and lists. Data is stored in London; some suppliers process
> calls in the US, and the Trust page says which. No pricing is
> published; engagement starts with a 45-minute demo call.

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
