import os

# Output to the repo root (this script lives in scripts/)
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PAGES = [
    ("index.html", "home", "Home"),
    ("services.html", "services", "What We Do"),
    ("how-it-works.html", "process", "How It Works"),
    ("about.html", "about", "About"),
    ("trust.html", "trust", "Trust & Security"),
    ("contact.html", "contact", "Contact"),
]

NAV_ITEMS = [
    ("services.html", "services", "What We Do"),
    ("how-it-works.html", "process", "How It Works"),
    ("about.html", "about", "About"),
    ("trust.html", "trust", "Trust & Security"),
    ("contact.html", "contact", "Contact"),
]

SITE_TITLE = "Deputable AI — Human Centric AI Solutions for UK SMEs"
SITE_DESC = "Deputable AI builds practical AI automation for small and medium businesses across the UK — telephone agents, workflow automation, internal knowledge assistants and governance built in from day one."


def head(title, desc, active_id, relpath_prefix=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="{relpath_prefix}assets/deputable-logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{relpath_prefix}css/style.css">
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
        <img src="{relpath_prefix}assets/deputable-logo.png" alt="Deputable AI">
      </a>
      <button class="mobile-toggle" aria-label="Toggle menu">Menu</button>
      <nav class="main-nav">
        {nav_links}
        <a class="btn-nav" href="{relpath_prefix}contact.html">Request a Demo</a>
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
        <img src="{relpath_prefix}assets/deputable-logo.png" alt="Deputable AI">
        <p>Human centric AI solutions for small and medium businesses in the United Kingdom.</p>
      </div>
      <div class="footer-cols">
        <div class="footer-nav">
          {links}
        </div>
        <div class="footer-contact">
          <div>hello@deputable.ai</div>
          <div>London, UK</div>
        </div>
      </div>
    </div>
    <div class="footer-bottom">
      <div class="wrap footer-bottom-inner">
        <span>&copy; 2026 Deputable AI Ltd</span>
        <span>Registered in England &amp; Wales</span>
      </div>
    </div>
  </footer>"""


def tail(relpath_prefix=""):
    return f"""</main>
{footer(relpath_prefix)}
</div>
<script src="{relpath_prefix}js/main.js"></script>
</body>
</html>
"""


def write_page(filename, title, desc, active_id, body):
    html = head(title, desc, active_id) + body + tail()
    with open(os.path.join(OUT, filename), "w") as f:
        f.write(html)


# ==================================================================
# HOME
# ==================================================================
start_points = [
    ("01", "Quotes, invoices and order paperwork that someone retypes by hand"),
    ("02", "Inbox and enquiry triage that delays a first response by days"),
    ("03", "Reporting assembled from spreadsheets every Monday morning"),
    ("04", "Knowledge locked in the head of one long-serving colleague"),
]

principles = [
    ("A Person Stays Accountable", "Anything that touches a customer, a payment or a record is reviewed or approved by a named person. The system proposes; your team decides."),
    ("Your Data Is Not Our Training Set", "Client data is used to serve that client only. It is never used to train models, and we tell you exactly which third-party services process it."),
    ("Built to Be Handed Over", "We document what we build and train your staff to run it. If you end the relationship, the workflow keeps working."),
]

services_home = [
    ("#00B4FF", "AI Readiness Assessment", "Two weeks mapping where AI would genuinely save time, and where it would not. You get a costed shortlist, not a strategy document."),
    ("#16BFA0", "Workflow Automation", "Document handling, triage, data entry and reporting, connected to the systems you already run."),
    ("#0E2A4A", "Assistants on Your Own Knowledge", "Internal and customer-facing assistants grounded in your documents, with citations and clear limits on what they answer."),
]

home_steps = [
    ("01", "Week 0", "Demo Call", "You bring a process. We walk through how it would run and whether it is worth doing."),
    ("02", "Weeks 1–2", "Assessment", "We map the work as it happens today and cost the options."),
    ("03", "Weeks 3–6", "Build", "One workflow, deployed to a small group first, with approval steps in place."),
    ("04", "Weeks 7–8", "Handover", "Documentation, training, and a review of what it saved."),
]

home_body = f"""
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <div class="eyebrow">Human Centric AI &middot; United Kingdom</div>
      <h1>AI Solutions for Small and Medium Businesses Across the UK.</h1>
      <p class="hero-sub">We build AI that works alongside your team rather than around it. Practical automation, deployed carefully, with a person accountable at every step.</p>
      <div class="hero-ctas">
        <a class="btn btn-primary" href="contact.html">Request a Demo</a>
        <a class="btn btn-secondary" href="services.html">See What We Do</a>
      </div>
    </div>
    <div class="hero-panel">
      <div class="hero-panel-title">Where We Start</div>
      <div>
        {"".join(f'<div class="start-point"><span class="n">{n}</span><span class="t">{t}</span></div>' for n, t in start_points)}
      </div>
    </div>
  </div>
</section>

<section class="bg-navy">
  <div class="wrap principles-grid">
    <h2>What &ldquo;Human Centric&rdquo; Means Here</h2>
    <div>
      {"".join(f'<div class="principle-item"><div class="principle-title">{t}</div><div class="principle-body">{b}</div></div>' for t, b in principles)}
    </div>
  </div>
</section>

<section>
  <div class="wrap section-pad">
    <div class="section-head-row">
      <h2>What We Do</h2>
      <a href="services.html" style="font-size:15px;font-weight:600;color:#0090D6">All Services &rarr;</a>
    </div>
    <div class="grid-3">
      {"".join(f'<div class="card"><div class="accent" style="background:{a}"></div><h3>{t}</h3><p>{b}</p></div>' for a, t, b in services_home)}
    </div>
  </div>
</section>

<section class="border-t bg-white">
  <div class="wrap section-pad">
    <h2 style="margin-bottom:44px">How It Works</h2>
    <div class="steps-grid">
      {"".join(f'<div class="step-item"><div class="meta">{n} &middot; {w}</div><h3>{t}</h3><p>{b}</p></div>' for n, w, t, b in home_steps)}
    </div>
  </div>
</section>

<section class="border-t">
  <div class="wrap split">
    <div>
      <h2>Built for the Way UK SMEs Actually Operate</h2>
      <p>Small teams, mixed systems, no spare capacity for a year-long programme. We scope work in weeks, integrate with the tools you already pay for, and hand over documentation your team can maintain.</p>
      <p>Data stays in the UK or EU. We are equally comfortable working with enterprise IT functions and public sector procurement.</p>
    </div>
    <div class="placeholder-img">
      <span>team photo / workshop shot<span class="sub">drop image here</span></span>
    </div>
  </div>
</section>

<section class="bg-navy">
  <div class="wrap cta-band">
    <div>
      <h2>See It Against Your Own Process</h2>
      <p>A 30-minute demo using a workflow you choose.</p>
    </div>
    <a class="btn btn-teal" href="contact.html">Request a Demo</a>
  </div>
</section>
"""

write_page("index.html", SITE_TITLE, SITE_DESC, "home", home_body)

print("Generated: index.html")

# ==================================================================
# SERVICES
# ==================================================================
voice_caps = [
    "Answer frequently asked questions",
    "Identify the caller and reason for calling",
    "Book, change, or cancel appointments",
    "Check availability, order status, or delivery information",
    "Qualify sales enquiries and capture lead details",
    "Take messages and create follow-up tasks",
    "Route urgent or complex calls to the correct employee",
    "Send confirmations by SMS or email",
    "Update the CRM automatically",
    "Produce call transcripts, summaries, and sentiment indicators",
    "Support several languages",
    "Handle calls outside normal business hours",
]

channels = [
    "Website chat and lead capture", "WhatsApp customer service", "SMS enquiries and reminders",
    "Email classification and response drafting", "Facebook or Instagram enquiries", "Customer self-service portals",
]

knowledge_qs = [
    "What is our refund process?",
    "Which products meet this customer’s requirements?",
    "Summarise this contract.",
    "How do I complete this compliance procedure?",
    "Show me the latest pricing and approved proposal wording.",
]

departments = [
    ("Sales", "Lead qualification, proposal drafting, CRM updates and follow-ups"),
    ("Customer Service", "Voice agents, chat, ticket summaries and suggested responses"),
    ("Finance", "Invoice extraction, reconciliation support and payment reminders"),
    ("Operations", "Scheduling, job allocation, stock alerts and report generation"),
    ("HR", "Onboarding, policy assistants, training and routine employee enquiries"),
    ("Marketing", "Content drafts, campaign personalisation and enquiry attribution"),
    ("Management", "Automated reports, business dashboards and forecasting support"),
    ("Compliance", "Document checks, audit trails, retention controls and policy monitoring"),
]

bespoke = [
    "Staff operations portals", "Customer booking systems", "Quote and proposal generators",
    "Field-service applications", "Document-processing platforms", "Management dashboards",
    "Secure approval workflows", "Industry-specific case-management systems",
]

discovery = [
    ("01", "Interview employees and map repetitive workflows."),
    ("02", "Measure volumes, labour time, delays and error rates."),
    ("03", "Assess data quality and existing systems."),
    ("04", "Rank opportunities by benefit, complexity and risk."),
    ("05", "Recommend a 60–90 day roadmap."),
    ("06", "Build one small, measurable pilot."),
]

support = [
    "Process and requirements discovery", "Solution design and integration", "Knowledge-base preparation",
    "Testing with real business scenarios", "Employee training and adoption", "Performance monitoring",
    "Conversation and workflow improvement", "Security updates and incident response",
    "Monthly business-impact reporting", "Human support and service-level agreements",
    "Backup procedures when the AI or another system is unavailable",
]

measures = [
    "Calls resolved", "Appointments booked", "Response time", "Employee hours saved",
    "Conversion rate", "Transfer rate", "Error rate", "Customer satisfaction",
]

governance = [
    "A documented lawful basis for processing personal information",
    "Data minimisation and defined retention periods",
    "A data-protection impact assessment where appropriate",
    "Supplier and data-location review",
    "Role-based access and audit logs",
    "Testing for inaccurate or harmful responses",
    "Clear AI disclosure",
    "Human escalation and override",
    "A process for challenging significant automated decisions",
    "Written incident and complaint procedures",
    "An employee AI-use policy",
    "Controls preventing client data from being used for model training without authority",
]

packages = [
    ("#00B4FF", "AI Receptionist", "Telephone answering, appointment booking, FAQ support and call summaries."),
    ("#16BFA0", "Customer Service Automation", "Voice, website chat, email and ticketing integration."),
    ("#0E2A4A", "AI Workflow Pilot", "One end-to-end internal process automated within a fixed scope."),
    ("#00B4FF", "Internal Knowledge Assistant", "Secure search and answers across approved company information."),
    ("#16BFA0", "AI Operations Suite", "Several connected agents and workflows across departments."),
    ("#0E2A4A", "Managed AI Service", "Monitoring, improvements, support, reporting and governance for a monthly fee."),
]

services_body = f"""
<section class="border-b bg-white">
  <div class="wrap page-hero">
    <div class="eyebrow">What We Do</div>
    <h1 style="max-width:24em">We identify repetitive work, automate it safely, connect existing business systems, and provide ongoing human support.</h1>
    <p class="lede">An AI operations partner for UK small and mid-sized businesses &mdash; not merely a chatbot developer.</p>
  </div>
</section>

<section class="bg-white border-b">
  <div class="wrap section-pad">
    <h2>Business-Process Automation</h2>
    <p style="font-size:17.5px;line-height:1.6;color:#43535F;margin:16px 0 32px;max-width:46em">Three things agents do from day one: bring in leads, answer the phone, and run the internal applications your team already depends on &mdash; stock, fleet, inventory, scheduling and job paperwork. Pick one to watch it run.</p>

    <div data-flow-demo>
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
        <div class="flow-note">Employees remain responsible for financial commitments, recruitment decisions, contract approval, complaints with serious consequences, and other high-impact decisions.</div>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap split start">
    <div>
      <h2 style="font-size:30px">AI Telephone and Customer-Service Agents</h2>
      <p style="margin-bottom:26px">An AI receptionist can answer calls 24/7 using a natural voice and the client&rsquo;s business information.</p>
      <div class="check-list">
        {"".join(f'<div class="check-item"><span class="tick">&#10003;</span><span>{c}</span></div>' for c in voice_caps)}
      </div>
    </div>
    <div class="panel-stack">
      <div class="panel">
        <h3>Safeguards, Not Optional Extras</h3>
        <p>Clear disclosure that the customer is speaking with an AI, an easy route to a person, recording and privacy notices, confidence thresholds, and emergency escalation.</p>
      </div>
      <div class="panel">
        <h3>We Start With Inbound Calls</h3>
        <p>Outbound sales calling brings additional consent, privacy and telecommunication considerations. Ofcom specifically requires organisations to prevent automated systems from producing silent or abandoned calls, and can take enforcement action for persistent misuse. <a href="https://www.ofcom.org.uk/phones-and-broadband/unwanted-calls-and-messages/refresher-messaging-on-silent-and-abandoned-calls" target="_blank" rel="noopener" style="color:#0090D6;font-weight:500">Ofcom Guidance &rarr;</a></p>
      </div>
      <div class="panel">
        <h3 style="margin-bottom:8px">Website, WhatsApp and Messaging Agents</h3>
        <p style="margin-bottom:16px">A conversation can begin on the website, continue by telephone, and finish with an appointment confirmation without the customer repeating their information.</p>
        <div class="pill-row">
          {"".join(f'<span class="pill">{c}</span>' for c in channels)}
        </div>
      </div>
    </div>
  </div>
</section>

<section class="bg-white border-t border-b">
  <div class="wrap" style="padding:84px 32px;display:grid;grid-template-columns:0.9fr 1.1fr;gap:60px;align-items:start">
    <div>
      <h2 style="font-size:30px">Internal Knowledge Assistants</h2>
      <p style="margin:14px 0 18px">Many SMEs have information scattered across documents, emails, shared drives and employee knowledge. We provide a secure internal assistant that answers questions about it.</p>
      <p style="font-size:15.5px;color:#52626D">The assistant quotes or links to its source, respects employee permissions, and says when it cannot find a reliable answer.</p>
    </div>
    <div style="display:grid;gap:12px">
      {"".join(f'<div class="quote-box">&ldquo;{q}&rdquo;</div>' for q in knowledge_qs)}
    </div>
  </div>
</section>

<section>
  <div class="wrap section-pad">
    <h2 style="font-size:34px;margin-bottom:14px">Department-Specific Solutions</h2>
    <p style="font-size:17px;line-height:1.6;color:#43535F;margin-bottom:36px;max-width:44em">Focused packages rather than vague &ldquo;AI transformation&rdquo;.</p>
    <div class="dept-table">
      {"".join(f'<div class="dept-row"><div class="dept-area">{a}</div><div class="dept-solutions">{s}</div></div>' for a, s in departments)}
    </div>
  </div>
</section>

<section class="bg-white border-t">
  <div class="wrap" style="padding:84px 32px;display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:start">
    <div>
      <h2 style="font-size:30px">Bespoke Applications</h2>
      <p style="margin:14px 0 24px">Some clients need a small application instead of another disconnected AI tool. The best approach is usually to extend or connect existing software before replacing it.</p>
      <div class="pill-row">
        {"".join(f'<span class="pill pill-lg">{b}</span>' for b in bespoke)}
      </div>
    </div>
    <div>
      <h2 style="font-size:30px">AI Readiness and Consulting</h2>
      <p style="margin:14px 0 24px">Many SMEs will not know where to begin, so discovery is structured.</p>
      <div class="numbered-list">
        {"".join(f'<div class="numbered-item"><span class="n">{n}</span><span class="t">{t}</span></div>' for n, t in discovery)}
      </div>
      <p style="font-size:15px;line-height:1.6;color:#52626D;margin-top:20px">A good first project is high-volume, rules-based, easy to review and capable of showing results within several weeks.</p>
    </div>
  </div>
</section>

<section class="bg-navy">
  <div class="wrap" style="padding:84px 32px;display:grid;grid-template-columns:0.9fr 1.1fr;gap:60px;align-items:start">
    <div>
      <h2 style="font-size:30px;color:#fff">Implementation and Ongoing Support</h2>
      <p style="margin:14px 0 24px;color:#C3D0DC">Our service covers more than initial development.</p>
      <div style="border-top:1px solid #24456B;padding-top:20px">
        <div style="font-family:'IBM Plex Mono',monospace;font-size:11px;letter-spacing:0.12em;text-transform:uppercase;color:#7FDBC8;margin-bottom:14px">What We Measure</div>
        <div class="pill-row">
          {"".join(f'<span class="pill pill-dark">{m}</span>' for m in measures)}
        </div>
      </div>
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px 28px">
      <div class="check-list check-list-tight" style="grid-column:1/-1;display:grid;grid-template-columns:1fr 1fr;gap:0 28px">
        {"".join(f'<div class="check-item" style="color:#E4EBF1"><span class="tick">&#10003;</span><span>{s}</span></div>' for s in support)}
      </div>
    </div>
  </div>
</section>

<section class="bg-white border-b">
  <div class="wrap section-pad">
    <h2 style="font-size:34px;margin-bottom:14px">Governance and UK Compliance</h2>
    <p style="font-size:17px;line-height:1.6;color:#43535F;margin-bottom:40px;max-width:46em">Responsible AI is part of the product rather than an optional consultancy extra. Every deployment includes the following.</p>
    <div class="gov-grid">
      {"".join(f'<div class="check-item"><span class="tick">&#10003;</span><span>{g}</span></div>' for g in governance)}
    </div>
    <div class="gov-panels">
      <div class="gov-note">
        <p>The ICO provides an AI risk toolkit and guidance on applying UK GDPR principles to AI systems. UK rules also require safeguards around significant solely automated decisions, including information, the ability to challenge a decision and access to human intervention.</p>
        <div style="display:flex;gap:20px;flex-wrap:wrap;margin-top:16px">
          <a href="https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/artificial-intelligence/" target="_blank" rel="noopener" style="font-size:14.5px;font-weight:500;color:#0090D6">ICO AI and Data-Protection Guidance &rarr;</a>
          <a href="https://www.gov.uk/guidance/data-use-and-access-act-2025-data-protection-and-privacy-changes?hl=en-GB" target="_blank" rel="noopener" style="font-size:14.5px;font-weight:500;color:#0090D6">UK Government Guidance &rarr;</a>
        </div>
      </div>
      <div class="gov-stat">
        <div class="num">17%</div>
        <p>of AI-using businesses had any AI policy or guidance, and just 5% had a formal written policy. <a href="https://www.gov.uk/government/statistics/uk-business-data-survey-2026/uk-business-data-survey-2026" target="_blank" rel="noopener" style="color:#0090D6;font-weight:500">UK Business Data Survey 2026 &rarr;</a></p>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap" style="padding:84px 32px 96px">
    <h2 style="font-size:34px;margin-bottom:14px">Commercial Packages</h2>
    <p style="font-size:17px;line-height:1.6;color:#43535F;margin-bottom:36px;max-width:46em">A one-off discovery and implementation charge, combined with monthly platform, usage, monitoring and support fees.</p>
    <div class="grid-3">
      {"".join(f'<div class="card"><div class="accent" style="background:{a}"></div><h3>{n}</h3><p>{b}</p></div>' for a, n, b in packages)}
    </div>
    <div class="pkg-actions">
      <a class="btn btn-primary" href="contact.html">Request a Demo</a>
    </div>
  </div>
</section>
"""

write_page("services.html", "What We Do — Deputable AI", "Business-process automation, AI telephone agents, internal knowledge assistants, bespoke applications and UK AI governance for SMEs.", "services", services_body)
print("Generated: services.html")

# ==================================================================
# HOW IT WORKS
# ==================================================================
process_full = [
    ("01", "Week 0", "Demo Call", "A 30-minute conversation about one process you would like handled. We are direct about what AI does poorly, and will tell you if the answer is a spreadsheet fix rather than a model.", "A written view on whether to proceed, at no cost."),
    ("02", "Weeks 1–2", "Assessment", "We observe the work as it is actually done, not as the process document describes it. Volumes, exceptions, handoffs and the cost of each error are recorded.", "Costed shortlist of workflows ranked by payback, plus a risk note."),
    ("03", "Weeks 3–6", "Build and Pilot", "One workflow at a time. It runs alongside the existing process first, so you can compare outputs before anyone relies on it. Approval steps sit wherever a mistake would reach a customer.", "A working workflow in your environment, plus pilot results."),
    ("04", "Weeks 7–8", "Handover and Review", "Your team is trained to operate and adjust what we built. We measure time saved against the assessment estimate and share the numbers whether or not they flatter us.", "Documentation, trained staff, and a measured before-and-after."),
]

process_body = f"""
<section class="border-b bg-white">
  <div class="wrap page-hero">
    <div class="eyebrow">How It Works</div>
    <h1 style="max-width:22em">Eight Weeks From First Call to Something Running in Production.</h1>
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
        <div class="process-output"><strong style="font-weight:600">You get:</strong> {o}</div>
      </div>
    </div>''' for n, w, t, b, o in process_full)}
  </div>
</section>
"""

write_page("how-it-works.html", "How It Works — Deputable AI", "An eight-week path from a demo call to a working AI workflow in production, with a decision point at every stage.", "process", process_body)
print("Generated: how-it-works.html")

# ==================================================================
# ABOUT
# ==================================================================
capabilities = [
    "Generating, qualifying and following up with sales leads",
    "Answering business calls and handling customer enquiries",
    "Booking appointments and routing requests to the right team",
    "Supporting stock, inventory and fleet-management processes",
    "Connecting AI agents with existing CRM and internal applications",
    "Automating routine administrative and operational workflows",
    "Providing employees with fast access to relevant business information",
]

sector_groups = [
    ("Trades & Installation", ["Construction", "Electricians", "Plumbing & Heating", "Roofing & Glazing", "HVAC & Refrigeration", "Lift Installation & Maintenance", "Water Treatment & Softeners", "Security & Fire Systems"]),
    ("Property & Facilities", ["Estate Agents", "Lettings & Property Management", "Facilities & Maintenance", "Cleaning Services", "Landscaping & Grounds", "Pest Control", "Surveying & Inspection", "Waste & Recycling"]),
    ("Product & Logistics", ["Manufacturing & Fabrication", "Wholesale & Distribution", "Trade Suppliers & Merchants", "Equipment Hire", "Removals & Logistics", "Vehicle Repair & MOT"]),
    ("Clinics & Professional Services", ["Dental Practices", "Chiropractic Clinics", "Physiotherapy", "Health & Fitness", "Healthcare Practices", "Veterinary Practices", "Accountancy & Bookkeeping", "Legal Services", "Recruitment Agencies", "Insurance Brokers", "Training Providers", "Hospitality & Events"]),
]

team = [
    ("Rohit Sinha", "Founder", "https://www.linkedin.com/in/rohit-sinha-b6792715/", "Rohit has spent his career getting change into production safely at large organisations — release and change management, cutover and deployment, service transition and major incident response across enterprise infrastructure and cloud programmes. That work is the reason Deputable pilots every workflow alongside the existing process and puts a named approver on anything that reaches a customer."),
    ("Prashant Tiwari", "Founder", "https://www.linkedin.com/in/prashanttiwari247/", "Prashant leads how the work is scoped and built, from the first process-mapping session through to handover. He focuses on keeping engagements small enough to finish: one workflow at a time, integrated with the systems a client already runs, documented so their own team can maintain it afterwards."),
]

about_body = f"""
<section class="border-b bg-white">
  <div class="wrap page-hero">
    <div class="eyebrow">About Us</div>
    <h1 style="max-width:24em">We Help UK Businesses Work Smarter With Practical, Intelligent AI Solutions.</h1>
    <p class="lede" style="font-size:18.5px;max-width:46em">Our company was founded with a clear purpose: to make advanced AI accessible and valuable to small and medium-sized businesses. We create tailored AI agents that support everyday operations, reduce repetitive work and give business owners and their teams more time to focus on customers, growth and important decisions.</p>
  </div>
</section>

<section>
  <div class="wrap" style="padding:80px 32px;display:grid;grid-template-columns:0.85fr 1.15fr;gap:60px;align-items:start">
    <div>
      <h2 style="font-size:32px;margin-bottom:16px">What We Do</h2>
      <p style="font-size:17px;line-height:1.65;color:#43535F">Every business operates differently, so we do not offer a one-size-fits-all product. We take the time to understand each organisation&rsquo;s processes, challenges and existing systems before designing a solution around its needs.</p>
    </div>
    <div>
      <div style="font-family:'IBM Plex Mono',monospace;font-size:11px;letter-spacing:0.12em;text-transform:uppercase;color:#8A968F;margin-bottom:6px">Our Capabilities Include</div>
      <div class="check-list check-list-lined">
        {"".join(f'<div class="check-item"><span class="tick" style="font-size:14px">&#10003;</span><span style="font-size:16.5px">{c}</span></div>' for c in capabilities)}
      </div>
    </div>
  </div>
</section>

<section class="bg-white border-t border-b">
  <div class="wrap section-pad">
    <h2 style="font-size:32px;margin-bottom:16px">Who We Support</h2>
    <p style="font-size:17px;line-height:1.65;color:#43535F;margin-bottom:30px;max-width:50em">We work with small and medium-sized businesses across the UK, without limiting our services to a single industry. Our solutions can support construction companies, electricians, plumbers, estate agents, lift installation and maintenance providers, water-treatment businesses and many other service-led organisations.</p>
    <div class="grid-2">
      {"".join(f'''<div class="sector-card">
        <div class="sector-card-head"><span class="name">{name}</span><span class="count">{len(items):02d}</span></div>
        <div class="sector-items">
          {"".join(f'<span class="sector-pill">{s}</span>' for s in items)}
        </div>
      </div>''' for name, items in sector_groups)}
    </div>
  </div>
</section>

<section>
  <div class="wrap" style="padding:80px 32px;display:grid;grid-template-columns:1fr 1fr;gap:60px;align-items:start">
    <div>
      <h2 style="font-size:32px;margin-bottom:16px">Our Approach</h2>
      <p style="font-size:17px;line-height:1.65;color:#43535F;margin-bottom:16px">We combine agentic AI, workflow automation and system integration to create solutions that can understand requests, take appropriate actions and collaborate with employees. Our technology is designed to complement your team&mdash;not replace the expertise, relationships and judgement that make your business successful.</p>
      <p style="font-size:17px;line-height:1.65;color:#43535F">From the first consultation through implementation and ongoing improvement, we focus on delivering technology that is secure, dependable and straightforward to use.</p>
    </div>
    <div class="mission-box">
      <div class="label">Our Mission</div>
      <p>Our mission is to remove operational friction from growing businesses. By allowing AI to manage repetitive calls, enquiries, administrative tasks and system updates, we help teams respond faster, operate more efficiently and concentrate on the work that creates the greatest value.</p>
    </div>
  </div>
</section>

<section class="bg-white border-t">
  <div class="wrap" style="padding:72px 32px 88px">
    <h2 style="font-size:30px;margin-bottom:32px">Founders</h2>
    <div class="grid-2" style="gap:40px">
      {"".join(f'''<div class="founder">
        <div class="founder-portrait"><span>portrait</span></div>
        <div>
          <div class="name">{n}</div>
          <div class="role">{r}</div>
          <p>{b}</p>
          <a class="li-link" href="{li}" target="_blank" rel="noopener">LinkedIn &rarr;</a>
        </div>
      </div>''' for n, r, li, b in team)}
    </div>
  </div>
</section>
"""

write_page("about.html", "About — Deputable AI", "Deputable AI is a UK-based AI operations partner for small and medium businesses, founded by Rohit Sinha and Prashant Tiwari.", "about", about_body)
print("Generated: about.html")

# ==================================================================
# TRUST
# ==================================================================
trust = [
    ("Where Is Our Data Processed?", "In the UK or EU by default. Where a workflow requires a model hosted elsewhere, we say so in writing before deployment and you decide whether to proceed."),
    ("Do You Train Models on Our Data?", "No. Client data is used to serve that client only. We contract with providers on terms that exclude training on submitted data, and we can show you those terms."),
    ("Who Can the System Act on Behalf Of?", "Nothing that touches a customer, a payment or a record of account is sent without a named person approving it, unless you explicitly ask for an unattended step and accept that in writing."),
    ("What Happens if the Model Gets It Wrong?", "Every workflow logs its inputs, outputs and decisions so an error can be traced and reversed. Pilots run alongside the existing process precisely so failures surface before anyone depends on the output."),
    ("What if We End the Engagement?", "You keep the workflow, the documentation and the accounts it runs on. We do not hold your integrations hostage, and there is no proprietary layer you have to keep paying us for."),
    ("Subprocessors and Compliance", "We maintain a current list of subprocessors and data flows for each client, and work to UK GDPR requirements. Certifications and DPA terms are shared on request."),
]

trust_body = f"""
<section class="border-b bg-white">
  <div class="wrap page-hero">
    <div class="eyebrow">Trust &amp; Security</div>
    <h1 style="max-width:22em">Where Your Data Goes, and Who Can Act on It.</h1>
    <p class="lede">The questions procurement and IT ask us first, answered plainly.</p>
  </div>
</section>
<section>
  <div class="trust-list">
    {"".join(f'<div class="trust-item"><h2>{q}</h2><p>{a}</p></div>' for q, a in trust)}
  </div>
</section>
"""

write_page("trust.html", "Trust & Security — Deputable AI", "How Deputable AI handles data location, model training, human accountability and UK GDPR compliance.", "trust", trust_body)
print("Generated: trust.html")

# ==================================================================
# CONTACT
# ==================================================================
contact_body = """
<section class="bg-white" style="min-height:70vh">
  <div class="wrap contact-grid">
    <div class="contact-info">
      <div class="eyebrow">Request a Demo</div>
      <h1>Bring a Workflow. We&rsquo;ll Show You What It Looks Like Handled.</h1>
      <p>Thirty minutes, no deck. Tell us the process that wastes the most time and we will walk through how it would run.</p>
      <div class="contact-details">
        <div>hello@deputable.ai</div>
        <div>London, United Kingdom</div>
      </div>
    </div>
    <div class="contact-panel">
      <!-- Demo-request form is a Zoho Forms embed; submissions are stored in
           Zoho Forms and emailed to the team. Edit the form at forms.zoho.eu. -->
      <iframe class="contact-form-embed" aria-label="Demo Request" frameborder="0"
        src="https://forms.zohopublic.eu/prashantdepu1/form/DemoRequest/formperma/NZOvPlQ0DNGZdgDLAsVXU9CWqtnsvX2yJ9xcpn_Qs24"></iframe>
    </div>
  </div>
</section>
"""

write_page("contact.html", "Contact — Deputable AI", "Request a 30-minute demo with Deputable AI. Bring a workflow and see how it would be handled.", "contact", contact_body)
print("Generated: contact.html")
