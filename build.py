"""Build Liam Curran's portfolio hub (one page) into ./docs for GitHub Pages at https://liampcurran.github.io/

Usage: python build.py
Set UPWORK_URL once the Upwork profile is live (the contact button is hidden until then).
"""
import json, shutil
from datetime import date
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).parent
P = ROOT.parent
OUT = ROOT / "docs"
BASE = "https://liampcurran.github.io"
UPWORK_URL = "https://www.upwork.com/freelancers/liampcurran"
GITHUB = "https://github.com/LiamPCurran"
TODAY = date.today().isoformat()

if OUT.exists():
    shutil.rmtree(OUT)
(OUT / "img").mkdir(parents=True)
(OUT / "files").mkdir()
shutil.copy(P / "sites" / "_fonts" / "plus-jakarta-sans-latin-wght-normal.woff2", OUT / "jakarta.woff2")


def cover(src, name, w=800):
    im = Image.open(src).convert("RGB")
    im.resize((w, round(im.height * w / im.width)), Image.LANCZOS).save(OUT / "img" / f"{name}.webp", "WEBP", quality=74, method=6)
    return f"img/{name}.webp"


def pdf(src):
    shutil.copy(src, OUT / "files" / src.name)
    return f"files/{src.name}"


CS = P / "case-studies" / "pdf"
WS = P / "writing-samples" / "pdf"
SC = P / "screenshots" / "covers"

WORK = [
    {"img": cover(SC / "02-tallyloop-cover.png", "rescue"), "tag": "Case study · build, audit, rebuild",
     "title": "A good-looking site Google could barely read",
     "text": "A startup site I designed, wrote and built, first shipped as a JavaScript-only app, then audited and rebuilt as fast, crawlable pages. Google went from receiving 1 word to the full page.",
     "stats": [("36 → 96", "speed score"), ("10.4 s → 1.2 s", "load time")],
     "links": [("Case study (PDF)", pdf(CS / "01-website-rescue-case-study.pdf")), ("SEO audit (PDF)", pdf(CS / "02-seo-audit-tallyloop.pdf")),
               ("Live after", f"{BASE}/tallyloop/"), ("Live before", f"{BASE}/tallyloop/before/")]},
    {"img": cover(SC / "03-kettlepine-cover.png", "store"), "tag": "WooCommerce · speed & SEO",
     "title": "A 12 MB store homepage cut to 465 KB",
     "text": "A WooCommerce store built on a lightweight custom theme, then measured against a typical unoptimized setup on the same host.",
     "stats": [("61 → 97", "speed score"), ("30 s → 2.2 s", "main image on mobile")],
     "links": [("Case study (PDF)", pdf(CS / "03-woocommerce-speed-case-study.pdf")), ("Live store", f"{BASE}/kettlepine-coffee/"),
               ("Before version", f"{BASE}/kettlepine-coffee/before/")]},
    {"img": cover(SC / "01-ashgrove-cover.png", "local"), "tag": "Local service website",
     "title": "An SEO-ready site for a home-service company",
     "text": "Built for calls and quote requests: click-to-call everywhere, instant quote forms, service pages, reviews and local schema.",
     "stats": [("100 / 100", "speed / SEO"), ("1.1 s", "load time")],
     "links": [("Live site", f"{BASE}/ashgrove-heating/"), ("SEO article", f"{BASE}/ashgrove-heating/blog/heat-pump-vs-furnace-ottawa.html")]},
    {"img": cover(SC / "09-automation-cover.png", "automation"), "tag": "Lead automation · n8n",
     "title": "Every quote request logged, sorted and answered",
     "text": "A workflow for the same home-service site: it cleans each lead, flags no-heat and gas/CO calls as urgent, logs it to a lead sheet, alerts the right person and replies to the customer.",
     "stats": [("< 0.5 s", "form to emails"), ("4 / 4", "test leads routed right")],
     "links": [("Case study (PDF)", pdf(CS / "04-lead-automation-demo.pdf"))]},
]
WRITING = [
    ("seo", SC / "7-seo-article-cover.png", "SEO article + content brief", "1,800 words on heat pumps vs furnaces in Ottawa, with the brief behind it.",
     [("Article (PDF)", pdf(WS / "06b-seo-post-heat-pump-vs-furnace.pdf")), ("Brief (PDF)", pdf(WS / "06a-seo-brief-heat-pump-vs-furnace.pdf"))]),
    ("homepage", SC / "5-homepage-rewrite-cover.png", "Homepage & landing page copy", "A before/after homepage rewrite, plus a one-offer campaign landing page.",
     [("Homepage rewrite (PDF)", pdf(WS / "02-homepage-rewrite-before-after.pdf")), ("Landing page (PDF)", pdf(WS / "03-landing-page-tallyloop.pdf"))]),
    ("email", SC / "6-email-flow-cover.png", "Email welcome series & brand story", "Four welcome emails for a coffee brand, plus its About-page story.",
     [("Email flow (PDF)", pdf(WS / "04-email-flow-kettlepine-welcome.pdf")), ("Brand story (PDF)", pdf(WS / "05-brand-story-kettlepine-about.pdf"))]),
    ("products", SC / "8-product-descriptions-cover.png", "Product descriptions", "Short and long descriptions for 8 products, plus a 1,300-word SEO guide.",
     [("Descriptions (PDF)", pdf(WS / "01-product-descriptions.pdf")), ("Coffee guide (PDF)", pdf(WS / "07b-seo-post-coffee-freshness.pdf"))]),
]
SERVICES = [
    ("Fixes & speed", "Broken layouts, plugin conflicts, errors and slow pages on WordPress and WooCommerce. Core Web Vitals passed, not just promised."),
    ("Technical SEO", "Audits where I also implement the fixes: indexing errors, sitemaps, schema, titles and site structure."),
    ("Website rescue", "Sites from quick site builders that look great but load slowly and don't show up on Google, rebuilt to be fast and crawlable."),
    ("Conversion copy", "Homepage, landing page, product and email copy that's specific, believable and written for the reader."),
    ("Monthly care", "Updates, backups, speed and SEO checks month to month, so you have one person to call."),
    ("Simple automations", "Form-to-sheet-to-follow-up flows that make sure no lead or quote request slips through."),
]


def a(label, href):
    ext = ' target="_blank" rel="noopener"' if href.startswith("http") or href.endswith(".pdf") else ""
    return f'<a href="{href}"{ext}>{label}</a>'


work_html = "".join(f'''<article class="work">
<img src="{w['img']}" width="800" height="600" alt="" loading="lazy" decoding="async">
<div class="work-body"><p class="tag">{w['tag']}</p><h3>{w['title']}</h3><p>{w['text']}</p>
<div class="stats">{"".join(f"<div><b>{x}</b><span>{y}</span></div>" for x, y in w['stats'])}</div>
<p class="links">{" ".join(a(l, h) for l, h in w['links'])}</p></div></article>''' for w in WORK)
writing_html = "".join(f'''<article class="wcard"><img src="{cover(src, name, 640)}" width="640" height="480" alt="" loading="lazy" decoding="async">
<div><h3>{t}</h3><p>{d}</p><p class="links">{" ".join(a(l, h) for l, h in links)}</p></div></article>''' for name, src, t, d, links in WRITING)
services_html = "".join(f"<div class='svc'><h3>{t}</h3><p>{d}</p></div>" for t, d in SERVICES)
cta_btn = (f'<a class="btn" href="{UPWORK_URL}" target="_blank" rel="noopener">Message me on Upwork</a>' if UPWORK_URL
           else '<span class="btn btn-muted">Upwork profile link coming soon</span>')

LD = {"@context": "https://schema.org", "@graph": [
    {"@type": "Person", "@id": BASE + "/#liam", "name": "Liam Curran", "url": BASE + "/", "jobTitle": "Website fixes, speed & technical SEO",
     "address": {"@type": "PostalAddress", "addressLocality": "Ottawa", "addressRegion": "ON", "addressCountry": "CA"},
     "sameAs": [GITHUB] + ([UPWORK_URL] if UPWORK_URL else []),
     "knowsAbout": ["WordPress", "WooCommerce", "Technical SEO", "Core Web Vitals", "Schema markup", "Conversion copywriting"]},
    {"@type": "WebSite", "@id": BASE + "/#site", "name": "Liam Curran: Portfolio", "url": BASE + "/", "author": {"@id": BASE + "/#liam"}}]}

html = f'''<!DOCTYPE html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Liam Curran | WordPress & WooCommerce Fixes, Speed & Technical SEO</title>
<meta name="description" content="I find what's wrong with your website, fix it and show you exactly what changed. WordPress and WooCommerce fixes, speed, technical SEO and conversion copy. Based in Ottawa.">
<link rel="canonical" href="{BASE}/">
<meta property="og:type" content="website"><meta property="og:title" content="Liam Curran | Website Fixes, Speed & Technical SEO">
<meta property="og:description" content="Case studies with real before/after measurements: website rescue, WooCommerce speed and local SEO.">
<meta property="og:url" content="{BASE}/"><meta property="og:image" content="{BASE}/img/rescue.webp">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#10233a">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%2310233a'/%3E%3Ctext x='16' y='22' font-family='Arial' font-weight='700' font-size='15' fill='%23ffb37e' text-anchor='middle'%3ELC%3C/text%3E%3C/svg%3E">
<link rel="preload" href="jakarta.woff2" as="font" type="font/woff2" crossorigin>
<style>
@font-face {{ font-family: Jakarta; src: url(jakarta.woff2) format("woff2"); font-weight: 200 800; font-display: optional; }}
:root {{ --ink:#152132; --muted:#55657a; --navy:#10233a; --accent:#b4470c; --accent-2:#ffb37e; --line:#e2e8ef; --tint:#f4f7fa; }}
*,*::before,*::after {{ box-sizing:border-box; }}
html {{ scroll-behavior:smooth; }}
body {{ margin:0; font-family:Jakarta,system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif; color:var(--ink); line-height:1.65; font-size:1.0625rem; background:#fff; }}
img {{ max-width:100%; height:auto; display:block; }}
a {{ color:var(--accent); }}
h1,h2,h3 {{ line-height:1.15; letter-spacing:-.02em; margin:0 0 .5em; color:var(--navy); }}
h1 {{ font-size:clamp(2.2rem,5vw,3.6rem); color:#fff; }}
h2 {{ font-size:clamp(1.7rem,3.2vw,2.4rem); }}
h3 {{ font-size:1.2rem; }}
p {{ margin:0 0 1em; }}
.wrap {{ max-width:1140px; margin:0 auto; padding:0 20px; }}
.skip {{ position:absolute; left:-999px; }} .skip:focus {{ left:8px; top:8px; background:#fff; padding:8px; z-index:9; }}
header.top {{ background:var(--navy); }}
header.top .wrap {{ display:flex; justify-content:space-between; align-items:center; min-height:64px; gap:16px; }}
.brand {{ color:#fff; font-weight:800; text-decoration:none; letter-spacing:-.02em; font-size:1.1rem; }}
nav a {{ color:#d3dde8; text-decoration:none; margin-left:18px; font-weight:600; font-size:.95rem; }}
nav a:hover {{ color:#fff; }}
.hero {{ background:radial-gradient(70% 90% at 85% 10%, #1d4a72 0%, var(--navy) 60%); color:#cfdae6; padding:72px 0 88px; }}
.eyebrow {{ text-transform:uppercase; letter-spacing:.14em; font-size:.8rem; font-weight:800; color:var(--accent-2); margin:0 0 14px; }}
.hero .lede {{ font-size:1.25rem; max-width:36em; }}
.ctas {{ display:flex; gap:12px; flex-wrap:wrap; margin-top:26px; }}
.btn {{ display:inline-flex; align-items:center; padding:13px 22px; border-radius:10px; background:var(--accent); color:#fff !important; font-weight:700; text-decoration:none; border:2px solid var(--accent); }}
.btn:hover {{ background:#933a0a; border-color:#933a0a; }}
.btn.ghost {{ background:transparent; border-color:rgba(255,255,255,.6); }}
.btn.ghost:hover {{ background:#fff; color:var(--navy) !important; }}
.btn-muted {{ background:#e9eef3; border-color:#e9eef3; color:#4a5a6c !important; cursor:default; }}
.facts {{ display:flex; gap:28px; flex-wrap:wrap; margin-top:40px; padding-top:26px; border-top:1px solid rgba(255,255,255,.15); }}
.facts div b {{ display:block; color:#fff; font-size:1.35rem; }}
.facts div span {{ font-size:.9rem; }}
section.block {{ padding:80px 0; }} section.tint {{ background:var(--tint); }}
.sec-head {{ max-width:44em; margin-bottom:36px; }} .sec-head p {{ color:var(--muted); font-size:1.1rem; }}
.work-list {{ display:grid; gap:28px; }}
.work {{ display:grid; grid-template-columns:1fr 1.1fr; gap:32px; align-items:center; background:#fff; border:1px solid var(--line); border-radius:18px; padding:18px; }}
.work img {{ border-radius:12px; border:1px solid var(--line); }}
.tag {{ color:var(--accent); font-weight:800; font-size:.78rem; text-transform:uppercase; letter-spacing:.1em; margin:0 0 6px; }}
.work p {{ color:var(--muted); }}
.stats {{ display:flex; gap:14px; margin:4px 0 16px; flex-wrap:wrap; }}
.stats div {{ background:var(--tint); border-radius:10px; padding:10px 14px; }}
.stats b {{ display:block; color:var(--navy); font-size:1.15rem; }} .stats span {{ font-size:.82rem; color:var(--muted); }}
.links {{ display:flex; gap:8px 16px; flex-wrap:wrap; margin:0; }}
.links a {{ font-weight:700; text-decoration:none; font-size:.95rem; }} .links a:hover {{ text-decoration:underline; }}
@media (max-width:860px) {{ .work {{ grid-template-columns:1fr; gap:16px; }} }}
.svc-grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:18px; }}
.svc {{ background:#fff; border:1px solid var(--line); border-radius:14px; padding:22px; }}
.svc p {{ color:var(--muted); margin:0; font-size:.98rem; }}
@media (max-width:860px) {{ .svc-grid {{ grid-template-columns:1fr 1fr; }} }} @media (max-width:560px) {{ .svc-grid {{ grid-template-columns:1fr; }} }}
.w-grid {{ display:grid; grid-template-columns:repeat(2,1fr); gap:20px; }}
.wcard {{ display:grid; grid-template-columns:200px 1fr; gap:18px; align-items:center; background:#fff; border:1px solid var(--line); border-radius:14px; padding:14px; }}
.wcard img {{ border-radius:8px; }} .wcard p {{ color:var(--muted); font-size:.95rem; margin-bottom:8px; }}
@media (max-width:860px) {{ .w-grid {{ grid-template-columns:1fr; }} }} @media (max-width:480px) {{ .wcard {{ grid-template-columns:1fr; }} }}
.about {{ display:grid; grid-template-columns:1.2fr 1fr; gap:48px; }}
.about ul {{ padding-left:1.1em; color:var(--muted); }} .about li {{ margin-bottom:8px; }}
.process {{ counter-reset:s; list-style:none; padding:0; margin:0; }}
.process li {{ counter-increment:s; position:relative; padding:0 0 18px 48px; }}
.process li::before {{ content:counter(s); position:absolute; left:0; top:0; width:32px; height:32px; border-radius:50%; background:var(--navy); color:#fff; font-weight:800; display:grid; place-items:center; font-size:.9rem; }}
.process b {{ display:block; color:var(--navy); }} .process span {{ color:var(--muted); font-size:.96rem; }}
@media (max-width:860px) {{ .about {{ grid-template-columns:1fr; gap:24px; }} }}
.cta {{ background:var(--navy); color:#cfdae6; padding:72px 0; text-align:center; }}
.cta h2 {{ color:#fff; }} .cta .ctas {{ justify-content:center; }}
footer {{ background:#0a1726; color:#8ea3b8; font-size:.9rem; padding:26px 0; }}
footer a {{ color:#d3dde8; }}
.note {{ font-size:.88rem; color:var(--muted); }}
</style>
<script type="application/ld+json">{json.dumps(LD, ensure_ascii=False, separators=(",", ":"))}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="wrap"><a class="brand" href="./">Liam Curran</a>
<nav aria-label="Main"><a href="#work">Work</a><a href="#services">Services</a><a href="#writing">Writing</a><a href="#about">About</a></nav></div></header>
<main id="main">
<section class="hero"><div class="wrap">
<p class="eyebrow">WordPress · WooCommerce · Technical SEO · Ottawa, Canada</p>
<h1>I find what's wrong with your website, fix it, and show you exactly what changed.</h1>
<p class="lede">Slow pages, broken layouts, sites Google can't read, copy that doesn't convert. I've run my own WooCommerce store since 2019, so I know what those problems cost a small business.</p>
<div class="ctas"><a class="btn" href="#work">See the case studies</a>{cta_btn.replace('class="btn"', 'class="btn ghost"') if UPWORK_URL else ''}</div>
<div class="facts">
<div><b>Since 2019</b><span>running my own WooCommerce store</span></div>
<div><b>95%+</b><span>five-star rating from customers</span></div>
<div><b>Highest</b><span>client retention rate at YellowPages</span></div>
</div></div></section>

<section class="block" id="work"><div class="wrap">
<div class="sec-head"><h2>Case studies</h2><p>Every number below is a real measurement on a live page. The brands are concept projects I built to show the work end to end, and both "before" and "after" versions are online so you can check them yourself.</p></div>
<div class="work-list">{work_html}</div>
</div></section>

<section class="block tint" id="services"><div class="wrap">
<div class="sec-head"><h2>What I can do for you</h2><p>Clear scope and price up front, a full backup before I touch anything, and a short written report of every change.</p></div>
<div class="svc-grid">{services_html}</div>
</div></section>

<section class="block" id="writing"><div class="wrap">
<div class="sec-head"><h2>Writing samples</h2><p>Website, email, product and SEO copy, written for fictional brands and labelled as concept samples.</p></div>
<div class="w-grid">{writing_html}</div>
</div></section>

<section class="block tint" id="about"><div class="wrap about">
<div><h2>About me</h2>
<p>I'm Liam, based in Ottawa. I got into websites the practical way: I built and ran my own e-commerce business, handling the store, SEO, product listings and every customer email myself.</p>
<ul>
<li>Built and ran a WooCommerce store since 2019: 5–20 orders a day, 95%+ five-star rating.</li>
<li>Founded HonestSEO, a system that teaches business owners to handle their own SEO, cutting 10–30 hours of work to 4–10.</li>
<li>Media account consultant at YellowPages: managed the online presence and websites of 80+ small-business clients, ranked #4 of 75 salespeople, and had the highest client retention rate in the company.</li>
</ul>
<p>I use modern tools to work quickly, and I personally check and test every change. You can see my code on <a href="{GITHUB}" target="_blank" rel="noopener">GitHub</a>.</p></div>
<div><h2>How I work</h2>
<ol class="process">
<li><b>Tell me what's wrong</b><span>Send your URL and what's bugging you. I'll tell you what I'd fix first.</span></li>
<li><b>Fixed scope and price</b><span>You know exactly what you're getting before any work starts.</span></li>
<li><b>Backup, then fix</b><span>Changes are made on a backup or staging copy whenever possible.</span></li>
<li><b>Before/after report</b><span>A short list of every change, with the measurements to prove it.</span></li>
</ol></div>
</div></section>

<section class="cta"><div class="wrap">
<h2>Got a slow or broken site?</h2>
<p>Send me the URL and tell me what's bugging you. I'll tell you what I'd fix first.</p>
<div class="ctas">{cta_btn}</div>
</div></section>
</main>
<footer><div class="wrap">© {date.today().year} Liam Curran · Ottawa, Canada · <a href="{GITHUB}" target="_blank" rel="noopener">GitHub</a>
<p class="note" style="color:#8ea3b8;margin:6px 0 0">Ashgrove Heating &amp; Air, Tallyloop and Kettlepine Coffee are fictional concept projects. Their names, reviews and figures are illustrative; every performance measurement is real.</p></div></footer>
</body>
</html>
'''
(OUT / "index.html").write_text(html, encoding="utf-8")
sites = ["", "ashgrove-heating/", "tallyloop/", "kettlepine-coffee/"]
(OUT / "robots.txt").write_text("User-agent: *\nAllow: /\n\n"
                                + "".join(f"Sitemap: {BASE}/{s}sitemap.xml\n" for s in sites), encoding="utf-8")
(OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{BASE}/</loc><lastmod>{TODAY}</lastmod></url></urlset>\n', encoding="utf-8")
(OUT / ".nojekyll").write_text("", encoding="utf-8")
print("built", OUT)
