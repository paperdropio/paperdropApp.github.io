#!/usr/bin/env python3
"""Generate the service, location and 404 pages.

GitHub Pages has no include mechanism, so the nav, footer and head are
duplicated into every page. Edit the content or chrome here, run
`python3 scripts/build_pages.py`, and commit the regenerated HTML.
The home page (index.html) is hand-written and not touched by this script.
"""
import json, html, os, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://paperdrop.io"
CONTACT = "https://beredo.io/start/6f3ce085954fdb059ed47274797a8f5e78dbb2ca63724382291001de504575f4"
ORG_ID = SITE + "/#organization"

def esc(s): return html.escape(s, quote=True)

def head(title, desc, path, ld, og_title=None):
    url = SITE + path
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}" />
<meta name="author" content="Paperdrop" />
<meta name="robots" content="index, follow, max-image-preview:large" />
<link rel="canonical" href="{url}" />
<link rel="icon" type="image/png" href="/assets/mark.png" />
<link rel="apple-touch-icon" sizes="180x180" href="/assets/apple-touch-icon.png" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="Paperdrop" />
<meta property="og:url" content="{url}" />
<meta property="og:title" content="{esc(og_title or title)}" />
<meta property="og:description" content="{esc(desc)}" />
<meta property="og:image" content="{SITE}/assets/og.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:locale" content="en_CA" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{esc(og_title or title)}" />
<meta name="twitter:description" content="{esc(desc)}" />
<meta name="twitter:image" content="{SITE}/assets/og.png" />
<meta name="theme-color" content="#f2f2f3" />
<script type="application/ld+json">
{json.dumps(ld, indent=2, ensure_ascii=False)}
</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;700&family=Barlow+Condensed:wght@400;600&display=swap">
<link rel="stylesheet" href="/assets/industry.css">
<link rel="stylesheet" href="/assets/site.css">
</head>
<body>
'''

NAV = f'''
<nav id="top" class="nav" style="position:sticky;top:0;z-index:20;background:var(--color-bg);border-bottom:1px solid var(--color-divider);padding-inline:max(24px, calc((100% - 1160px) / 2 + 24px))">
  <a class="nav-brand" href="/" aria-label="Paperdrop — home" style="display:flex;align-items:center;gap:10px;letter-spacing:0.05em;text-transform:uppercase;font-size:26px">
    <img src="/assets/mark-68.png" alt="" width="34" height="34" style="display:block;object-fit:contain" />
    <span><span style="color:var(--color-accent)">Paper</span><span style="color:var(--color-accent-2-700)">drop</span></span>
  </a>
  <a href="/#services">Services</a>
  <a href="/#ai">AI capability</a>
  <a href="/#method">Method</a>
  <a href="/#about">About</a>
  <a href="/#beredo">Beredo</a>
  <a href="/#careers">Careers</a>
  <a class="btn btn-primary" href="{CONTACT}" target="_blank" rel="noopener" style="color:var(--color-bg)">Contact us</a>
</nav>

<div class="wrap">
'''

FOOTER_LINKS = [
    ("/digital-transformation/", "Digital transformation"),
    ("/process-automation/", "Process automation"),
    ("/consulting-training/", "Consulting &amp; training"),
    ("/toronto/", "Toronto"),
    ("/pune/", "Pune"),
    ("/#faq", "FAQ"),
    ("/#beredo", "Beredo"),
    ("/#careers", "Careers"),
]

def footer():
    links = "\n    ".join(f'<a href="{h}">{t}</a>' for h, t in FOOTER_LINKS)
    return f'''
  <div class="footer-links">
    {links}
  </div>
  <footer class="footer">
    <span>© 2026 Paperdrop. Toronto · Pune.</span>
    <span><a href="mailto:hello@paperdrop.io">hello@paperdrop.io</a></span>
  </footer>

</div>

</body>
</html>
'''

def contact_block(no):
    return f'''
  <section id="contact" class="section">
    <span class="kicker">{no} · Contact</span>
    <hr class="rule" />
    <div class="two-col" style="padding-top:20px;border-top:2px solid var(--color-accent-2)">
      <div>
        <h2 class="h-section"><a href="{CONTACT}" target="_blank" rel="noopener" style="color:inherit">Describe the process</a></h2>
        <p class="body">Tell us about the workflow that costs you the most time, through the contact form. We will reply with what we would look at first, and whether a review is worth your money.</p>
        <a class="btn btn-primary" href="{CONTACT}" target="_blank" rel="noopener" style="margin-top:24px;color:var(--color-bg)">Contact us</a>
      </div>
      <div style="display:grid;gap:0">
        <div class="spec-row"><span>Contact</span><a href="{CONTACT}" target="_blank" rel="noopener">Contact form on Beredo</a></div>
        <div class="spec-row"><span>Toronto</span><a href="tel:+14374496106">+1 437 449 6106</a></div>
        <div class="spec-row"><span>Pune</span><a href="tel:+917276197537">+91 7276 197 537</a></div>
        <div class="spec-row"><span>Email</span><a href="mailto:hello@paperdrop.io">hello@paperdrop.io</a></div>
      </div>
    </div>
  </section>
'''

def steps_html(steps):
    out = []
    for i, (t, p) in enumerate(steps, 1):
        cls = "tile tile-lead" if i == 1 else "tile"
        out.append(f'''      <div class="{cls}">
        <span class="step-no">{i:02d}</span>
        <h3 class="h-step">{t}</h3>
        <p class="muted">{p}</p>
      </div>''')
    return "\n".join(out)

def rows_html(rows):
    return "\n".join(f'        <div class="spec-row"><span>{k}</span><span>{v}</span></div>' for k, v in rows)

def paras(ps, cls="body"):
    return "\n".join(f'        <p class="{cls}">{p}</p>' for p in ps)

# --------------------------------------------------------------------------
# Service pages
# --------------------------------------------------------------------------

SERVICES = {
  "digital-transformation": dict(
    name="Digital transformation",
    title="Digital transformation for paper-based businesses | Paperdrop",
    desc="Paperdrop replaces paper forms, shared inboxes and spreadsheets with systems of record. Process and document audit, systems selection and integration, migration off paper and PDFs. Toronto and Pune.",
    h1=("Off paper.", "Onto a system of record."),
    lede="Digital transformation is not a new app on top of the old process. It is deciding what each document is for, keeping the ones that matter, and giving them one home that the whole business can trust.",
    problem_h="The problem we are usually called about",
    problem=[
      "A form gets filled in by hand, scanned, emailed to a shared inbox and typed into a spreadsheet by somebody whose real job is something else. The spreadsheet is copied. Two versions drift. Nobody is sure which one the auditor saw.",
      "The cost rarely shows on the ledger as a line item. It shows as late month-ends, a hire that only exists to re-key, a compliance finding, and a manager who cannot answer a simple question about volume without asking three people.",
      "We work with owner-led firms, operations teams and internal IT who know this is happening and want it fixed without a multi-year programme or a platform they will never fully use.",
    ],
    steps=[
      ("Inventory", "We list every document, form, spreadsheet and inbox in the process and record who creates it, who reads it, and what decision it feeds. Most firms are surprised by how many exist."),
      ("Decide", "For each one: keep, merge, or retire. What each document is actually for, agreed in writing with the people who use it. The ones nobody reads are retired here, not migrated."),
      ("Select and integrate", "Where a system of record is needed we help you choose it, favouring software you already license. We integrate rather than replace wherever the existing tool is sound."),
      ("Migrate", "Historic paper and PDFs are brought across with a documented mapping, so a record from before the change is as findable as one from after. The old route is closed only when the new one has run cleanly."),
    ],
    receive=[
      ("Audit", "A document and process inventory, with the decision recorded for each item"),
      ("Selection", "A written recommendation and the reasoning behind it, usable with any vendor"),
      ("Integration", "Working connections between the systems you keep, with source and configuration"),
      ("Migration", "Historic records moved, mapped and verified against the originals"),
      ("Runbook", "How the new process runs day to day, and what to do when it does not"),
    ],
    related_h="Where this leads",
    related="Once documents have one home, the repetitive work between them becomes visible and can be handed to software. That is <a href=\"/process-automation/\">process automation</a>, and most transformation engagements are followed by one.",
  ),
  "process-automation": dict(
    name="Process automation",
    title="Process automation with an audit trail | Paperdrop",
    desc="Paperdrop automates the repetitive middle of a workflow: intake, routing, approval chasing and re-keying. Exceptions go to a named person, every step is logged. Toronto and Pune.",
    h1=("The repetitive middle,", "handed to software."),
    lede="Between the moment a request arrives and the moment somebody acts on it sits a chain of intake, routing, chasing and re-keying that no one chose as a career. We automate that chain and leave a log on every step a machine takes.",
    problem_h="What the middle of a workflow costs",
    problem=[
      "An application comes in by email. Someone checks it is complete, files it, creates a record, notifies the approver, chases the approver, records the decision and tells the applicant. Seven steps, one of which needed a human judgement.",
      "When volume rises the chain stretches. Requests sit in inboxes, approvals are chased twice, and the one exception that mattered is handled the same way as the routine ninety-nine, which is to say late.",
      "The fix is not to remove people from the decision. It is to remove them from the plumbing around it, and to make sure the plumbing tells them the moment something does not fit.",
    ],
    steps=[
      ("Map the flow as it runs", "Not the flow on the org chart. We sit with the operators and document each hand-off, wait and workaround, and mark which steps involve a real judgement."),
      ("Route and chase", "Intake, validation, routing to the right approver and reminders are handled by software. The approver sees a queue, not an inbox, and the requester sees a status, not silence."),
      ("Extract and re-key", "Documents are read and the fields your system needs are filled in. Where a language model does the reading it runs behind a confidence threshold, and anything below it queues for a person."),
      ("Escalate exceptions", "Whatever the automation does not recognise goes to a named person with the context attached. Nothing is silently dropped, and every outcome, human or machine, is logged and reversible."),
    ],
    receive=[
      ("Workflow", "Routing, approvals and reminders running in the software you already open each morning"),
      ("Intake", "Document intake and extraction, with the confidence threshold and review queue set by you"),
      ("Exceptions", "Escalation rules, alerts and the log that shows who decided what and when"),
      ("Review mode", "Every automation ships watching first, so you see what it would have done before it does it"),
      ("Source and runbook", "The code, the configuration and the operating manual, handed to your team"),
    ],
    related_h="Where the AI sits",
    related="Language models appear in exactly one place in this work: reading documents, classifying requests and drafting routine replies, each behind a lever a human can pull. Read how we bound a model step on the <a href=\"/#ai\">AI capability</a> section, or see it running in <a href=\"/#beredo\">Beredo</a>.",
  ),
  "consulting-training": dict(
    name="Consulting & training",
    title="Automation consulting, due diligence and operator training | Paperdrop",
    desc="Paperdrop advises on systems and automation, reviews what has already been built, and trains operators and administrators so the system keeps running after we leave. Runbooks, handover and source included.",
    h1=("Advice you can act on.", "Training that sticks."),
    lede="Consulting and training exist so the system keeps running after we leave. We review what you have, tell you plainly what we would do, and teach the people who will operate it.",
    problem_h="When advice is the right first step",
    problem=[
      "A vendor has proposed a platform and you want a second opinion before signing. A previous automation project stalled and nobody is sure whether to rescue it or start again. An internal team built something useful that only its author understands.",
      "In each case the wrong move is to start building. The right one is a short, honest technical review with a written recommendation you can take to anyone, including another firm.",
      "Training is the other half. Automation that only the consultants can operate is a dependency, not a capability. We would rather hand over a runbook and a trained administrator than a support contract.",
    ],
    steps=[
      ("Technical due diligence", "We read the code, the architecture and the vendor proposal, and write down what is sound, what is fragile, and what it would cost to change. Plain language, no slides."),
      ("Recommendation", "A written recommendation with the assumptions it rests on and what we would not do. You own it, and you can act on it with or without us."),
      ("Operator and admin training", "Hands-on sessions for the people who run the process daily and the people who administer the system, on your own data and your own screens."),
      ("Handover", "Source code, configuration, runbooks and a recorded walkthrough. Ongoing support is a separate agreement if you want one, never a dependency we design in."),
    ],
    receive=[
      ("Review", "A technical due diligence report on the system, proposal or codebase in question"),
      ("Recommendation", "What we would do, what it rests on, and what we would leave alone"),
      ("Training", "Operator and administrator sessions, with the materials left with you"),
      ("Runbook", "Day-to-day operation, exception handling and recovery, written for your team"),
      ("Source", "Everything we build or touch is handed over with its history"),
    ],
    related_h="How we use this ourselves",
    related="The same discipline shapes our own practice. A very small team carries each engagement from review to handover, with language models doing the drafting, scaffolding and documentation that used to need a separate role each. Read more <a href=\"/#about\">about how we work</a>.",
  ),
}

def service_page(slug, s):
    path = f"/{slug}/"
    ld = {
      "@context": "https://schema.org",
      "@type": "Service",
      "@id": SITE + path + "#service",
      "name": s["name"].replace("&", "and"),
      "serviceType": s["name"].replace("&", "and"),
      "description": s["desc"],
      "url": SITE + path,
      "provider": {"@id": ORG_ID, "@type": "ProfessionalService", "name": "Paperdrop", "url": SITE + "/"},
      "areaServed": ["CA", "US", "IN"],
      "audience": {"@type": "BusinessAudience", "name": "Small and midsize businesses"},
    }
    others = [(f"/{k}/", v["name"]) for k, v in SERVICES.items() if k != slug]
    other_links = " · ".join(f'<a href="{h}">{esc(n)}</a>' for h, n in others)
    h1a, h1b = s["h1"]
    body = f'''
  <section class="hero">
    <p class="crumbs"><a href="/">Paperdrop</a> / <a href="/#services">Services</a> / {esc(s["name"])}</p>
    <h1 class="h-display">{h1a}<br>{h1b}</h1>
    <p class="lede">{s["lede"]}</p>
    <div style="display:flex;flex-wrap:wrap;gap:12px;margin-top:32px">
      <a class="btn btn-primary" href="{CONTACT}" target="_blank" rel="noopener" style="color:var(--color-bg)">Contact us</a>
      <a class="btn btn-secondary" href="/#method">How we work</a>
    </div>
  </section>

  <section class="section">
    <span class="kicker">01 · The problem</span>
    <hr class="rule" />
    <div class="two-col">
      <h2 class="h-section">{s["problem_h"]}</h2>
      <div>
{paras(s["problem"])}
      </div>
    </div>
  </section>

  <section class="section">
    <span class="kicker">02 · What we do</span>
    <hr class="rule" />
    <div class="grid-cards">
{steps_html(s["steps"])}
    </div>
  </section>

  <section class="section">
    <span class="kicker">03 · What you receive</span>
    <hr class="rule" />
    <div class="two-col">
      <div>
        <h2 class="h-section">Handed over, not held</h2>
        <p class="body">Every engagement starts with a short review and a written, fixed-price scope. What you receive at the end is listed here, and it is yours to run without us.</p>
      </div>
      <div style="display:grid;gap:0">
{rows_html(s["receive"])}
      </div>
    </div>
  </section>

  <section class="section">
    <span class="kicker">04 · Related</span>
    <hr class="rule" />
    <div class="two-col">
      <h2 class="h-section">{s["related_h"]}</h2>
      <div>
        <p class="body">{s["related"]}</p>
        <p class="muted">Other services: {other_links}. Offices in <a href="/toronto/">Toronto</a> and <a href="/pune/">Pune</a>.</p>
      </div>
    </div>
  </section>
{contact_block("05")}'''
    return head(s["title"], s["desc"], path, ld, og_title=f'{s["name"]} | Paperdrop') + NAV + body + footer()

# --------------------------------------------------------------------------
# Location pages
# --------------------------------------------------------------------------

LOCATIONS = {
  "toronto": dict(
    city="Toronto", region="ON", region_name="Ontario", country="CA", country_name="Canada",
    tel_display="+1 437 449 6106", tel="+1-437-449-6106", tel_href="tel:+14374496106",
    tz="Eastern Time", tz_iana="America/Toronto",
    title="Process automation and AI consultancy in Toronto | Paperdrop",
    desc="Paperdrop is a software consultancy in Toronto for small and midsize businesses still running on paper, forms and manual re-keying. Digital transformation, process automation and auditable AI, with a delivery team in Pune.",
    h1=("Toronto.", "Paper in, automation out."),
    lede="Our Toronto office is where most engagements start: the process review, the scoping conversation, and the training sessions with the people who will run the system. Delivery is shared with our Pune team, so work continues across the day.",
    who_h="Who we work with here",
    who=[
      "Owner-led firms and operations teams across the Greater Toronto Area whose processes still run on forms, email attachments and spreadsheets: brokerages and advisory firms collecting client documents, professional services practices onboarding clients, and businesses with an approvals chain that lives in somebody's inbox.",
      "Canadian data residency comes up in nearly every conversation. Where documents must not leave the country, or the network, we run open models on your own hardware and integrate with the Canadian regions of the platforms you already license.",
      "We meet in person for the review and for training. Everything else runs remotely, with a named person in Toronto responsible for the engagement from first meeting to handover.",
    ],
    rows=[
      ("Phone", '<a href="tel:+14374496106">+1 437 449 6106</a>'),
      ("Email", '<a href="mailto:hello@paperdrop.io">hello@paperdrop.io</a>'),
      ("Hours", "Monday to Friday, Eastern Time. Delivery continues in Pune outside these hours."),
      ("Meetings", "In person across the Greater Toronto Area, or by video"),
      ("Serving", "Toronto, Ontario and clients across Canada and the United States"),
    ],
    other=("pune", "Pune"),
  ),
  "pune": dict(
    city="Pune", region="MH", region_name="Maharashtra", country="IN", country_name="India",
    tel_display="+91 7276 197 537", tel="+91-7276197537", tel_href="tel:+917276197537",
    tz="India Standard Time", tz_iana="Asia/Kolkata",
    title="Process automation and AI consultancy in Pune | Paperdrop",
    desc="Paperdrop's Pune office delivers digital transformation, process automation and auditable AI for small and midsize businesses in India and for our North American clients. Overlapping hours with Toronto.",
    h1=("Pune.", "Built here, run anywhere."),
    lede="Pune is where much of our building happens, and where we work with Indian businesses directly. The same small team, the same review-then-build method, and hours that overlap with both India and North America.",
    who_h="Who we work with here",
    who=[
      "Small and midsize businesses in Pune and across Maharashtra whose approvals, intake and record-keeping still move as paper, scans and WhatsApp forwards: manufacturers and their purchasing desks, professional practices, educational institutions and growing service firms.",
      "For our Toronto clients the Pune team is the reason work progresses overnight in North America. A review conducted in Toronto in the afternoon is being built against in Pune the same evening, with a shared log so nothing is lost in the hand-off.",
      "Where documents must stay in India, or on your own premises, we run open models locally and integrate with the Indian regions of the cloud platforms you already use.",
    ],
    rows=[
      ("Phone", '<a href="tel:+917276197537">+91 7276 197 537</a>'),
      ("Email", '<a href="mailto:hello@paperdrop.io">hello@paperdrop.io</a>'),
      ("Hours", "Monday to Friday, India Standard Time, with overlap into the North American morning."),
      ("Meetings", "In person in Pune, or by video"),
      ("Serving", "Pune, Maharashtra, clients across India, and delivery for North American engagements"),
    ],
    other=("toronto", "Toronto"),
  ),
}

def location_page(slug, L):
    path = f"/{slug}/"
    ld = {
      "@context": "https://schema.org",
      "@type": "ProfessionalService",
      "@id": SITE + path + "#office",
      "name": f'Paperdrop {L["city"]}',
      "url": SITE + path,
      "image": SITE + "/assets/og.png",
      "logo": SITE + "/assets/mark.png",
      "telephone": L["tel"],
      "email": "hello@paperdrop.io",
      "description": L["desc"],
      "parentOrganization": {"@id": ORG_ID, "@type": "ProfessionalService", "name": "Paperdrop", "url": SITE + "/"},
      "address": {"@type": "PostalAddress", "addressLocality": L["city"], "addressRegion": L["region"], "addressCountry": L["country"]},
      "areaServed": {"@type": "AdministrativeArea", "name": f'{L["city"]}, {L["region_name"]}'},
      "knowsAbout": ["Digital transformation", "Business process automation", "Document automation", "AI integration"],
    }
    other_slug, other_name = L["other"]
    h1a, h1b = L["h1"]
    body = f'''
  <section class="hero">
    <p class="crumbs"><a href="/">Paperdrop</a> / Offices / {L["city"]}</p>
    <h1 class="h-display">{h1a}<br>{h1b}</h1>
    <p class="lede">{L["lede"]}</p>
    <div style="display:flex;flex-wrap:wrap;gap:12px;margin-top:32px">
      <a class="btn btn-primary" href="{CONTACT}" target="_blank" rel="noopener" style="color:var(--color-bg)">Contact us</a>
      <a class="btn btn-secondary" href="{L["tel_href"]}">Call {L["tel_display"]}</a>
    </div>
  </section>

  <section class="section">
    <span class="kicker">01 · The office</span>
    <hr class="rule" />
    <div class="two-col">
      <div>
        <h2 class="h-section">Working with us from {L["city"]}</h2>
        <p class="body">One team across two offices. Whichever one you start with, the people you meet in the review are the people who build the thing, and the same log follows the work between {L["city"]} and {other_name}.</p>
      </div>
      <div style="display:grid;gap:0">
{rows_html(L["rows"])}
      </div>
    </div>
  </section>

  <section class="section">
    <span class="kicker">02 · Clients</span>
    <hr class="rule" />
    <div class="two-col">
      <h2 class="h-section">{L["who_h"]}</h2>
      <div>
{paras(L["who"])}
      </div>
    </div>
  </section>

  <section class="section">
    <span class="kicker">03 · Services</span>
    <hr class="rule" />
    <div class="grid-cards">
      <div class="tile tile-lead">
        <h3 class="h-card"><a class="card-link" href="/digital-transformation/">Digital transformation</a></h3>
        <p class="muted">Paper forms, shared inboxes and spreadsheets replaced with systems of record.</p>
      </div>
      <div class="tile">
        <h3 class="h-card"><a class="card-link" href="/process-automation/">Process automation</a></h3>
        <p class="muted">Intake, routing, approval chasing and re-keying handed to software, exceptions to a named person.</p>
      </div>
      <div class="tile">
        <h3 class="h-card"><a class="card-link" href="/consulting-training/">Consulting &amp; training</a></h3>
        <p class="muted">Technical due diligence, operator training, runbooks and handover.</p>
      </div>
    </div>
    <p class="muted" style="margin-top:32px">Also from our <a href="/{other_slug}/">{other_name}</a> office. Read <a href="/#method">how we work</a> and the <a href="/#faq">frequently asked questions</a>.</p>
  </section>
{contact_block("04")}'''
    return head(L["title"], L["desc"], path, ld, og_title=f'Paperdrop {L["city"]}') + NAV + body + footer()

# --------------------------------------------------------------------------
# 404
# --------------------------------------------------------------------------

def not_found_page():
    ld = {"@context": "https://schema.org", "@type": "WebPage", "name": "Page not found", "url": SITE + "/404.html", "isPartOf": {"@id": SITE + "/#website"}}
    body = f'''
  <section class="hero">
    <p class="crumbs"><a href="/">Paperdrop</a> / 404</p>
    <h1 class="h-display">That page<br>has moved on.</h1>
    <p class="lede">The address you followed does not exist on this site any more. The pages below are the ones people usually want.</p>
    <div style="display:flex;flex-wrap:wrap;gap:12px;margin-top:32px">
      <a class="btn btn-primary" href="/" style="color:var(--color-bg)">Home</a>
      <a class="btn btn-secondary" href="/#services">Services</a>
      <a class="btn btn-secondary" href="/#contact">Contact</a>
    </div>
  </section>

  <section class="section">
    <span class="kicker">Pages</span>
    <hr class="rule" />
    <div class="grid-cards">
      <div class="tile tile-lead"><h3 class="h-card"><a class="card-link" href="/digital-transformation/">Digital transformation</a></h3></div>
      <div class="tile"><h3 class="h-card"><a class="card-link" href="/process-automation/">Process automation</a></h3></div>
      <div class="tile"><h3 class="h-card"><a class="card-link" href="/consulting-training/">Consulting &amp; training</a></h3></div>
      <div class="tile"><h3 class="h-card"><a class="card-link" href="/toronto/">Toronto</a></h3></div>
      <div class="tile"><h3 class="h-card"><a class="card-link" href="/pune/">Pune</a></h3></div>
      <div class="tile"><h3 class="h-card"><a class="card-link" href="/#beredo">Beredo</a></h3></div>
    </div>
  </section>
'''
    page = head("Page not found | Paperdrop", "This page does not exist on paperdrop.io. Find our services, offices and contact details.", "/404.html", ld) + NAV + body + footer()
    return page.replace('<meta name="robots" content="index, follow, max-image-preview:large" />', '<meta name="robots" content="noindex, follow" />')

# --------------------------------------------------------------------------

def write(rel, content):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print(f"wrote {rel} ({len(content.encode())} bytes)")

if __name__ == "__main__":
    for slug, s in SERVICES.items():
        write(f"{slug}/index.html", service_page(slug, s))
    for slug, L in LOCATIONS.items():
        write(f"{slug}/index.html", location_page(slug, L))
    write("404.html", not_found_page())
