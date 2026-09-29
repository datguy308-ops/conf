#!/usr/bin/env python3
"""Generate the Confidence Aviation website into public/.

Content rule: every sentence taken from the original site is reproduced verbatim
(see tools/inventory.json and docs/content-inventory.md). Only headings, labels
and navigation text are new. Run tools/images.py first, then this script,
then tools/audit.py to prove nothing from the original site is missing.

Usage:  python3 tools/build.py
"""
import hashlib
import html
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUB = ROOT / "public"
SRC = ROOT / "src"
SITE = "https://www.confidenceaviation.com"
IMG = json.loads((SRC / "images.json").read_text())

PHONE, PHONE_TEL = "1-305-392-6291", "tel:+13053926291"
FAX = "1-305-392-6292"
EMAIL = "info@confidenceaviation.com"
FAA_RSS = "https://www.faa.gov/newsroom/press_releases/rss"
OSM = "https://www.openstreetmap.org/search?query=7605%20NW%2050th%20Street%2C%20Miami%2C%20FL%2033166"

# Original <meta name="keywords">, verbatim. index.htm and about.htm used the first
# spelling ("avioncs"), the other pages the second.
KEYWORDS_A = ("FAA, certified, repair, station, OEM, boeing, avionics, avionics repair, L3, avioncs, Bendix, "
              "Honeywell, King, Sperry, ameri-cam, DME, aviation, auto pilot, transponder, T-CAS, aircraft "
              "antennas, weather radar, altimeter repair, collins")
KEYWORDS_B = KEYWORDS_A.replace("L3, avioncs", "L3, avionics")

PAGES = ["home", "about", "capabilities", "certificates", "shop", "contact"]
FILES = {"home": "index.html", "about": "about.htm", "capabilities": "capabilities.htm",
         "certificates": "certificates.htm", "shop": "shop.htm", "contact": "contact.htm"}


def url(lang, page):
    prefix = "/es/" if lang == "es" else "/"
    return prefix if page == "home" else prefix + FILES[page]


def e(s):
    return html.escape(s, quote=True)


# ---------------------------------------------------------------- images
def picture(slug, alt, *, sizes="100vw", lazy=True, cls="", priority=False, max_w=None):
    info = IMG[slug]
    variants = sorted(info["sizes"], key=lambda s: s["w"])
    if max_w:
        variants = [v for v in variants if v["w"] <= max_w] or variants[:1]
    big = variants[-1]
    fb = big["fallback"]
    webp = ", ".join(f"/assets/img/{slug}-{v['w']}.webp {v['w']}w" for v in variants)
    fall = ", ".join(f"/assets/img/{slug}-{v['w']}.{fb} {v['w']}w" for v in variants)
    attrs = f' loading="lazy" decoding="async"' if lazy else ' decoding="async"'
    if priority:
        attrs += ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    return (f'<picture><source type="image/webp" srcset="{webp}" sizes="{sizes}">'
            f'<img src="/assets/img/{slug}-{big["w"]}.{fb}" srcset="{fall}" sizes="{sizes}" '
            f'width="{big["w"]}" height="{big["h"]}" alt="{e(alt)}"{c}{attrs}></picture>')


def full_src(slug):
    info = IMG[slug]
    big = max(info["sizes"], key=lambda s: s["w"])
    return f"/assets/img/{slug}-{big['w']}.{big['fallback']}"


# ---------------------------------------------------------------- shared data
SHOP = [  # (anchor/slug, original caption (alt/title on old site), Spanish caption, EN alt, ES alt)
    ("shop-entrance", "Aviation Workshop Entrance", "Taller de aviación: entrada",
     "View from the shop entrance of workbenches lined with electronic test equipment",
     "Vista desde la entrada del taller de bancos de trabajo con equipos electrónicos de prueba"),
    ("shop-dme-transponder-bench", "Aviation Workshop DME Transponder Bench", "Taller de aviación: banco de DME y transpondedor",
     "Workbench with oscilloscopes and test instruments at the DME transponder bench",
     "Banco de trabajo con osciloscopios e instrumentos de prueba en el banco de DME y transpondedor"),
    ("shop-radar-bench-1", "Aviation Workshop Radar Bench 1", "Taller de aviación: banco de radar 1",
     "Radar test bench with instruments, a unit on the bench and an open manual",
     "Banco de prueba de radar con instrumentos, una unidad en el banco y un manual abierto"),
    ("shop-nav-comm-bench", "Aviation Workshop NAV/COMM Bench", "Taller de aviación: banco NAV/COMM",
     "NAV/COMM bench with racks of test instruments and an open manual",
     "Banco NAV/COMM con estantes de instrumentos de prueba y un manual abierto"),
    ("shop-radar-bench-2", "Aviation Workshop Radar Bench 2", "Taller de aviación: banco de radar 2",
     "Radar bench with components and tools laid out on the work surface",
     "Banco de radar con componentes y herramientas sobre la superficie de trabajo"),
    ("shop-dme-altimeter-benches", "Aviation Workshop DME & Altimeter Benches", "Taller de aviación: bancos de DME y altímetro",
     "Row of benches with test equipment and a test rack",
     "Fila de bancos con equipos de prueba y un bastidor de pruebas"),
    ("shop-radar-nav-comm-bench", "Aviation Workshop Radar & NAV Comm Bench 2", "Taller de aviación: banco de radar y NAV/COMM 2",
     "Radar and NAV/COMM bench with test instruments",
     "Banco de radar y NAV/COMM con instrumentos de prueba"),
    ("shop-altimeter-test-set", "Aviation Workshop Altimeter Test Set", "Taller de aviación: equipo de prueba de altímetros",
     "Altimeter test set rack with meters, switches and a connection panel",
     "Bastidor del equipo de prueba de altímetros con medidores, interruptores y panel de conexiones"),
    ("shop-hf-antenna", "Aviation Workshop HF Antenna", "Taller de aviación: antena HF",
     "HF antenna equipment and avionics units on a bench",
     "Equipo de antena HF y unidades de aviónica sobre un banco"),
    ("shop-radar-indicators", "Aviation Workshop Radar Indicators", "Taller de aviación: indicadores de radar",
     "Several radar indicator display units stacked on a bench",
     "Varias unidades indicadoras de radar apiladas sobre un banco"),
    ("shop-large-radar-system", "Aviation Workshop Large Radar System", "Taller de aviación: sistema de radar grande",
     "Large radar system with its antenna dish on a bench",
     "Sistema de radar grande con su antena parabólica sobre un banco"),
    ("shop-radio-altimeters", "Aviation Workshop Radio Altimeters", "Taller de aviación: radioaltímetros",
     "Radio altimeter units stacked on a bench",
     "Unidades de radioaltímetro apiladas sobre un banco"),
]

DOCS = [  # (anchor/slug, original title, original file, Spanish subtitle, short id)
    ("air-agency-certificate", "Air Agency Certificate", "air_agency_certificate.gif",
     "Certificado de Agencia Aérea (FAA)", "No. V9DR072Y"),
    ("easa-approval-certificate", "European Aviation Safety Agency Approval Certificate", "easa-cert.jpg",
     "Certificado de aprobación de la Agencia Europea de Seguridad Aérea", "EASA.145.5139"),
    ("operations-specifications", "Operations Specifications", "operations_specifications.gif",
     "Especificaciones de operación (FAA)", "A003"),
]

UI = {
    "en": {
        "nav": {"home": "Home", "about": "About Us", "capabilities": "Capabilities",
                "certificates": "Certificates", "shop": "Shop Tour", "contact": "Contact"},
        "skip": "Skip to main content", "menu": "Menu", "main_nav": "Main navigation",
        "lang_label": "Language Option", "brand_alt": "Confidence Aviation, Inc.",
        "home_link": "Confidence Aviation, Inc. — home",
        "tag": "Avionics & Instruments — FAA Certified Repair Station",
        "phone": "Phone", "fax": "Fax", "email": "Email",
        "f_contact": "Contact", "f_pages": "Pages", "f_lang": "Language Option",
        "credit": 'Original website created by <a href="http://www.wintertek.com" rel="noopener" target="_blank">wintertek</a>',
        "breadcrumb": "Breadcrumb", "repair_no": "FAA Repair Station No.",
        "og_locale": "en_US", "quick": "Quick contact and language",
    },
    "es": {
        "nav": {"home": "Inicio", "about": "Nosotros", "capabilities": "Capacidades",
                "certificates": "Certificados", "shop": "Recorrido del taller", "contact": "Contacto"},
        "skip": "Saltar al contenido principal", "menu": "Menú", "main_nav": "Navegación principal",
        "lang_label": "Idioma", "brand_alt": "Confidence Aviation, Inc.",
        "home_link": "Confidence Aviation, Inc. — inicio",
        "tag": "Aviónica e instrumentos — Estación reparadora certificada por la FAA",
        "phone": "Teléfono", "fax": "Fax", "email": "Correo electrónico",
        "f_contact": "Contacto", "f_pages": "Páginas", "f_lang": "Idioma",
        "credit": 'Sitio web original creado por <a href="http://www.wintertek.com" rel="noopener" target="_blank">wintertek</a>',
        "breadcrumb": "Ruta de navegación", "repair_no": "Estación reparadora FAA No.",
        "og_locale": "es_ES", "quick": "Contacto rápido e idioma",
    },
}


# ---------------------------------------------------------------- layout
def lang_switch(lang, page, label=True):
    en_cur = ' aria-current="true"' if lang == "en" else ""
    es_cur = ' aria-current="true"' if lang == "es" else ""
    lab = f'<span class="lang__label">{UI[lang]["lang_label"]}:</span> ' if label else ""
    es_text = 'Español<span class="visually-hidden"> (Spanish)</span>' if lang == "en" else "Español"
    return (f'<span class="lang">{lab}<a href="{url("en", page)}" hreflang="en" lang="en"{en_cur}>English</a>'
            f'<span aria-hidden="true">/</span><a href="{url("es", page)}" hreflang="es" lang="es"{es_cur}>{es_text}</a></span>')


def layout(lang, page, *, title, desc, body, crumbs=None, keywords=KEYWORDS_B, jsonld=None, og_image=None, noindex=False):
    u = UI[lang]
    canonical = SITE + url(lang, page)
    cur = ' aria-current="page"'
    nav = "".join(
        f'<li><a href="{url(lang, p)}"{cur if p == page else ""}>{u["nav"][p]}</a></li>'
        for p in PAGES)
    og_img = SITE + (og_image or "/assets/img/banner-1200.jpg")
    ld = [LOCAL_BUSINESS(lang)] if page == "home" and not noindex else []
    if crumbs:
        ld.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + h}
            for i, (n, h) in enumerate([(u["nav"]["home"], url(lang, "home"))] + crumbs)]})
    if jsonld:
        ld.extend(jsonld)
    ld_html = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    crumb_html = ""
    if crumbs:
        items = [f'<li><a href="{url(lang, "home")}">{u["nav"]["home"]}</a></li>']
        items += [f'<li><a href="{h}" aria-current="page">{e(n)}</a></li>' for n, h in crumbs]
        crumb_html = f'<nav class="breadcrumb" aria-label="{u["breadcrumb"]}"><ol>{"".join(items)}</ol></nav>'
    body = body.replace("{{CRUMBS}}", crumb_html)
    alt_locale = "es_ES" if lang == "en" else "en_US"
    if noindex:
        index_tags = '<meta name="robots" content="noindex">'
    else:
        index_tags = (f'<link rel="canonical" href="{canonical}">\n'
                      f'<link rel="alternate" hreflang="en" href="{SITE + url("en", page)}">\n'
                      f'<link rel="alternate" hreflang="es" href="{SITE + url("es", page)}">\n'
                      f'<link rel="alternate" hreflang="x-default" href="{SITE + url("en", page)}">')
    footer_lang = (f'<a href="{url("en", page)}" hreflang="en" lang="en">English</a> / '
                   f'<a href="{url("es", page)}" hreflang="es" lang="es">Spanish (Español)</a>') if lang == "en" else (
                   f'<a href="{url("en", page)}" hreflang="en" lang="en">English</a> / '
                   f'<a href="{url("es", page)}" hreflang="es" lang="es">Español</a>')
    return f"""<!doctype html>
<html lang="{lang}" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="keywords" content="{e(keywords)}">
{index_tags}
<meta property="og:type" content="website">
<meta property="og:site_name" content="Confidence Aviation, Inc.">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_img}">
<meta property="og:locale" content="{u['og_locale']}">
<meta property="og:locale:alternate" content="{alt_locale}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#03204a">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/favicon.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="stylesheet" href="/assets/css/site.css?v={ASSET_V['css']}">
<script>document.documentElement.className="js"</script>
<script src="/assets/js/site.js?v={ASSET_V['js']}" defer></script>
{ld_html}
</head>
<body>
<a class="skip-link" href="#main">{u['skip']}</a>
<aside class="topbar" aria-label="{u['quick']}">
  <div class="wrap topbar__inner">
    <p class="topbar__ids"><span>{u['repair_no']} <span class="mono">V9DR072Y</span></span><span>EASA <span class="mono">EASA.145.5139</span></span></p>
    <div class="topbar__contact">
      <a href="{PHONE_TEL}">{PHONE}</a>
      <a href="mailto:{EMAIL}">{EMAIL}</a>
      {lang_switch(lang, page)}
    </div>
  </div>
</aside>
<header class="site-header">
  <div class="wrap site-header__inner">
    <a class="brand" href="{url(lang, 'home')}" aria-label="{u['home_link']}">
      <picture><source type="image/webp" srcset="/assets/img/logo-400.webp 1x, /assets/img/logo-800.webp 2x"><img src="/assets/img/logo-400.png" srcset="/assets/img/logo-800.png 2x" width="400" height="59" alt="{u['brand_alt']}"></picture>
    </a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav"><span class="nav-toggle__bars" aria-hidden="true"></span>{u['menu']}</button>
    <nav class="site-nav" id="site-nav" aria-label="{u['main_nav']}"><ul>{nav}</ul></nav>
  </div>
</header>
<main id="main" tabindex="-1">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <p class="footer-name">Confidence Aviation, Inc.</p>
        <p>{u['tag']}</p>
        <p>{u['repair_no']} <span class="mono">V9DR072Y</span><br>EASA <span class="mono">EASA.145.5139</span></p>
      </div>
      <div>
        <h2>{u['f_contact']}</h2>
        <address>Confidence Aviation, Inc.<br>7605 N.W. 50th Street<br>Miami, FL 33166</address>
        <ul>
          <li>{u['phone']}: <a href="{PHONE_TEL}">{PHONE}</a></li>
          <li>{u['fax']}: {FAX}</li>
          <li>{u['email']}: <a href="mailto:{EMAIL}">{EMAIL}</a></li>
        </ul>
      </div>
      <div>
        <h2>{u['f_pages']}</h2>
        <ul>{"".join(f'<li><a href="{url(lang, p)}">{u["nav"][p]}</a></li>' for p in PAGES)}</ul>
      </div>
      <div>
        <h2>{u['f_lang']}</h2>
        <p>{footer_lang}</p>
      </div>
    </div>
    <div class="footer-bottom">
      <p>©2003 - 2011 Confidence Aviation, Inc.</p>
      <p>{u['credit']}</p>
    </div>
  </div>
</footer>
</body>
</html>
"""


def LOCAL_BUSINESS(lang):
    return {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "@id": SITE + "/#organization",
        "name": "Confidence Aviation, Inc.",
        "url": SITE + url(lang, "home"),
        "logo": SITE + "/assets/img/logo-800.png",
        "image": SITE + "/assets/img/banner-1200.jpg",
        "description": ("FAA / EASA certified repair station offering overhaul and repair capabilities. "
                        "FAA repair station No. V9DR072Y.") if lang == "en" else (
                        "Estación reparadora certificada por la FAA / EASA. Estación reparadora FAA No. V9DR072Y."),
        "foundingDate": "1998",
        "telephone": "+1-305-392-6291",
        "faxNumber": "+1-305-392-6292",
        "email": EMAIL,
        "address": {"@type": "PostalAddress", "streetAddress": "7605 N.W. 50th Street",
                    "addressLocality": "Miami", "addressRegion": "FL", "postalCode": "33166",
                    "addressCountry": "US"},
        "inLanguage": lang,
    }


def page_head(eyebrow, h1, lead=""):
    lead_html = f'<p class="lead">{lead}</p>' if lead else ""
    return f"""<div class="page-head"><div class="wrap">{{{{CRUMBS}}}}<span class="eyebrow">{eyebrow}</span><h1>{h1}</h1>{lead_html}</div></div>"""


def ratings_list(lang):
    if lang == "en":
        rows = [("Radio Class 1:", "Communications Equipment", "(unlimited)"),
                ("Radio Class 2:", "Navigational Equipment", "(unlimited)"),
                ("Radio Class 3:", "Radar Equipment", "(unlimited)")]
        return '<ul class="ratings">' + "".join(
            f'<li><span class="r-class">{c}</span> <span class="r-scope">{s}</span> <span class="r-limit">{l}</span></li>'
            for c, s, l in rows) + "</ul>"
    rows = [("Radio Class 1:", "Equipos de comunicaciones", "Communications Equipment"),
            ("Radio Class 2:", "Equipos de navegación", "Navigational Equipment"),
            ("Radio Class 3:", "Equipos de radar", "Radar Equipment")]
    return '<ul class="ratings">' + "".join(
        f'<li><span class="r-class" lang="en">{c}</span> <span class="r-scope">{s} <span lang="en">({en})</span></span> '
        f'<span class="r-limit">(ilimitada / <span lang="en">unlimited</span>)</span></li>'
        for c, s, en in rows) + "</ul>"


def gallery(lang, items, group, *, compact=False, link_to=None, with_ids=False):
    out = []
    for i, (slug, cap_en, cap_es, alt_en, alt_es) in enumerate(items):
        cap = cap_en if lang == "en" else cap_es
        alt = alt_en if lang == "en" else alt_es
        sizes = "(max-width: 560px) 100vw, (max-width: 1100px) 33vw, 280px"
        above_fold = with_ids and i < 4  # first gallery row on the Shop Tour page is the LCP area
        pic = picture(slug, alt, sizes=sizes, lazy=not above_fold, priority=with_ids and i == 0)
        href = link_to + "#" + slug if link_to else full_src(slug)
        lb = "" if link_to else f' data-lightbox="{group}" data-caption="{e(cap)}"'
        idattr = f' id="{slug}"' if with_ids else ""
        en_cap = f' <span class="visually-hidden" lang="en">({cap_en})</span>' if lang == "es" and not compact else ""
        out.append(f'<li{idattr}><figure><a href="{href}"{lb}>{pic}</a><figcaption>{e(cap)}{en_cap}</figcaption></figure></li>')
    return f'<ul class="gallery{" gallery--compact" if compact else ""}">{"".join(out)}</ul>'


def doc_thumb(slug, alt):
    return picture(slug, alt, sizes="(max-width: 760px) 90vw, 320px", max_w=320)


# ---------------------------------------------------------------- certificate transcriptions (verbatim, as printed)
TRANSCRIPT = {
"air-agency-certificate": """
<p class="centered">UNITED STATES OF AMERICA<br>DEPARTMENT OF TRANSPORTATION<br>FEDERAL AVIATION ADMINISTRATION</p>
<p class="centered"><strong>Air Agency Certificate</strong><br>Number <strong>V9DR072Y</strong></p>
<p>This certificate is issued to <strong>CONFIDENCE AVIATION INC.</strong> whose business address is 7605 N.W. 50TH STREET, MIAMI, FLORIDA 33166 upon finding that its organization complies in all respects with the requirements of the Federal Aviation Regulations relating to the establishment of an Air Agency, and is empowered to operate an approved REPAIR STATION with the following ratings:</p>
<p class="centered"><strong>RADIO (June 13, 2000)</strong><br><strong>LIMITED ACCESSORY (Nov 18, 1999)</strong></p>
<p>This certificate, unless canceled, suspended, or revoked, shall continue in effect INDEFINITELY.</p>
<p>Date issued: DECEMBER 15, 1998</p>
<p>By direction of the Administrator: MICHAEL C. THOMAS, MANAGER, SO-MIAMI FSDO-19</p>
<p>This Certificate is not Transferable, and any major change in the basic facilities, or in the location thereof, shall be immediately reported to the appropriate regional office of the Federal Aviation Administration.</p>
<p>Any alteration of this certificate is punishable by a fine of not exceeding $1,000, or imprisonment not exceeding 3 years, or both.</p>
<p>FAA Form 8000-4 (1-67) &nbsp; SUPERCEDES FAA FORM 395.</p>
""",
"easa-approval-certificate": """
<p class="centered">European Aviation Safety Agency</p>
<p class="centered"><strong>APPROVAL CERTIFICATE</strong><br>REFERENCE EASA.145.5139</p>
<p>Taking into account the provisions of Article 9(2) of Regulation (EC) No 1592/2002<sup><a href="#easa-legibility">*</a></sup> of the European Parliament and of the Council and the bilateral agreements currently in force between European Union Member States and the Government of the United States of America, the European Aviation Safety Agency (EASA) hereby certifies:</p>
<p class="centered"><strong>CONFIDENCE AVIATION INC.</strong><br>FAA Repair Station Number: V9DR072Y<br>7605 N.W. 50th Street<br>Miami, Florida 33166<br>USA</p>
<p>as a Part-145 maintenance organization approved to maintain the products listed in the FAA Air Agency Certificate and associated Operations Specifications and to issue related certificates of release to service using the above reference, subject to the following conditions:</p>
<ol>
<li>The scope of the approval is limited to that specified on the FAR Part 145 repair station Air Agency Certificate, and the associated Operations Specifications for work carried out in the USA (Unless otherwise agreed in a particular case by EASA).</li>
<li>This approval requires continued compliance with FAR Part 145 and the differences as specified in the Maintenance Implementation Procedures, including the use of the FAA Form 8130-3 for release/return to service of components up to and including powerplants.</li>
<li>Certificates of return to service must quote the EASA Part 145 approval reference number quoted above and the FAR Part 145 Air Agency Certificate number.</li>
<li>Subject to compliance with the foregoing conditions, this approval shall remain valid for an unlimited duration until the approval is surrendered, superseded, suspended or revoked.</li>
</ol>
<p>Date of issue: 19th October 2004<br>Signed — For EASA</p>
<p>EASA Form 3 &nbsp; Page 1 of 1</p>
<p class="note" id="easa-legibility">* The regulation number is partly illegible in the scanned document; see the document image.</p>
""",
"operations-specifications": """
<p>U.S. Department of Transportation — Federal Aviation Administration<br><strong>Operations Specifications</strong></p>
<p><strong>A003. Ratings and Limitations</strong> — HQ Control: 12/16/98 &nbsp; HQ Revision: 00c</p>
<p>The Certificate Holder is authorized the following Ratings and/or Limitations:</p>
<p><strong>Class Ratings</strong></p>
<ul><li>Radio Class 1: Communications Equipment</li><li>Radio Class 2: Navigational Equipment</li><li>Radio Class 3: Radar Equipment</li></ul>
<div class="table-wrap"><table><caption>Limited Ratings</caption>
<thead><tr><th scope="col">Rating</th><th scope="col">Manufacturer</th><th scope="col">Make / Model</th><th scope="col">Limitations</th></tr></thead>
<tbody><tr><td>Accessories</td><td>From the Approved Capabilities List</td><td>Current Revision</td><td>N/A</td></tr></tbody></table></div>
<div class="table-wrap"><table><caption>Limited Ratings - Specialized Services</caption>
<thead><tr><th scope="col">Rating</th><th scope="col">Specifications</th><th scope="col">Limitations</th></tr></thead>
<tbody><tr><td>None Authorized</td><td>N/A</td><td>N/A</td></tr></tbody></table></div>
<ol>
<li>Issued by the Federal Aviation Administration.</li>
<li>These Operations Specifications are approved by direction of the Administrator.<br>Schmidt, Gordon, Principal Avionics Inspector, SO19</li>
<li>Date Approval is effective: 1/22/03 &nbsp; Amendment Number: 2</li>
<li>I hereby accept and receive the Operations Specifications in this paragraph.<br>Hernandez, Alexis R., General Manager &nbsp; Date: 1/22/03</li>
</ol>
<p>Print Date: 1/28/2003 &nbsp; A003-1 &nbsp; Confidence Aviation, Inc. &nbsp; Certificate No.: V9DR072Y</p>
""",
}

SPEC = {  # key facts printed on each document; values verbatim, labels translated per language
"air-agency-certificate": [
    ("Issued by", "Emitido por", "United States of America, Department of Transportation, Federal Aviation Administration"),
    ("Certificate number", "Número de certificado", '<span class="mono">V9DR072Y</span>'),
    ("Issued to", "Emitido a", "CONFIDENCE AVIATION INC."),
    ("Business address", "Dirección comercial", "7605 N.W. 50th Street, Miami, Florida 33166"),
    ("Approved as", "Aprobado como", "REPAIR STATION"),
    ("Ratings", "Habilitaciones", "RADIO (June 13, 2000)<br>LIMITED ACCESSORY (Nov 18, 1999)"),
    ("Date issued", "Fecha de emisión", "DECEMBER 15, 1998"),
    ("Duration (as printed)", "Vigencia (según el documento)", "Unless canceled, suspended, or revoked, shall continue in effect INDEFINITELY"),
    ("Signed", "Firmado", "MICHAEL C. THOMAS, MANAGER, SO-MIAMI FSDO-19 (by direction of the Administrator)"),
    ("Form", "Formulario", "FAA Form 8000-4 (1-67), SUPERCEDES FAA FORM 395"),
],
"easa-approval-certificate": [
    ("Issued by", "Emitido por", "European Aviation Safety Agency (EASA)"),
    ("Reference", "Referencia", '<span class="mono">EASA.145.5139</span>'),
    ("Certifies", "Certifica a", "CONFIDENCE AVIATION INC."),
    ("FAA Repair Station Number", "Número de estación reparadora FAA", '<span class="mono">V9DR072Y</span>'),
    ("Address", "Dirección", "7605 N.W. 50th Street, Miami, Florida 33166, USA"),
    ("Approved as", "Aprobado como", "Part-145 maintenance organization"),
    ("Date of issue", "Fecha de emisión", "19th October 2004"),
    ("Duration (as printed)", "Vigencia (según el documento)", "Valid for an unlimited duration until the approval is surrendered, superseded, suspended or revoked, subject to the conditions listed"),
    ("Form", "Formulario", "EASA Form 3"),
],
"operations-specifications": [
    ("Issued by", "Emitido por", "U.S. Department of Transportation, Federal Aviation Administration"),
    ("Paragraph", "Párrafo", "A003. Ratings and Limitations"),
    ("HQ Control / HQ Revision", "HQ Control / HQ Revision", "12/16/98 / 00c"),
    ("Certificate No.", "Certificado No.", '<span class="mono">V9DR072Y</span>'),
    ("Class Ratings", "Habilitaciones de clase", "Radio Class 1: Communications Equipment<br>Radio Class 2: Navigational Equipment<br>Radio Class 3: Radar Equipment"),
    ("Limited Ratings", "Habilitaciones limitadas", "Accessories — From the Approved Capabilities List — Current Revision — Limitations: N/A"),
    ("Specialized Services", "Servicios especializados", "None Authorized"),
    ("Date approval is effective", "Fecha de vigencia de la aprobación", "1/22/03 (Amendment Number: 2)"),
    ("Approved by", "Aprobado por", "Schmidt, Gordon, Principal Avionics Inspector, SO19"),
    ("Accepted by", "Aceptado por", "Hernandez, Alexis R., General Manager (1/22/03)"),
    ("Print date / page", "Fecha de impresión / página", "1/28/2003 / A003-1"),
],
}


# ---------------------------------------------------------------- pages: English
BANNER = ('<picture><source type="image/webp" srcset="/assets/img/banner-800.webp 800w, /assets/img/banner-1200.webp 1200w, '
          '/assets/img/banner-2000.webp 2000w" sizes="100vw"><img src="/assets/img/banner-1200.jpg" '
          'srcset="/assets/img/banner-800.jpg 800w, /assets/img/banner-1200.jpg 1200w, /assets/img/banner-2000.jpg 2000w" '
          'sizes="100vw" width="2000" height="667" alt="Confidence Aviation, Inc." fetchpriority="high" decoding="async"></picture>')


def en_home():
    body = f"""
<section class="hero on-dark" aria-labelledby="hero-title">
  <h1 class="hero__banner" id="hero-title">{BANNER}</h1>
  <div class="wrap hero__grid">
    <div>
      <span class="eyebrow">Avionics &amp; Instruments · FAA Certified Repair Station</span>
      <p class="cert-line">FAA repair station No. V9DR072Y</p>
      <p class="lead">We are an FAA / EASA certified repair station offering overhaul and repair capabilities.</p>
      <div class="actions">
        <a class="btn btn--primary" href="{PHONE_TEL}">Call {PHONE}</a>
        <a class="btn btn--outline" href="/capabilities.htm">Our Capabilities</a>
      </div>
    </div>
    <aside class="dataplate" aria-labelledby="dp-title">
      <p class="dataplate__title" id="dp-title">Repair station data</p>
      <dl>
        <dt>FAA Air Agency Certificate</dt><dd><span class="mono">V9DR072Y</span></dd>
        <dt>EASA approval</dt><dd><span class="mono">EASA.145.5139</span></dd>
        <dt>Class ratings</dt><dd>Radio Class 1, 2 &amp; 3</dd>
        <dt>Limited ratings</dt><dd>Accessories</dd>
        <dt>Opened</dt><dd>1998</dd>
        <dt>Location</dt><dd>7605 N.W. 50th Street, Miami, FL 33166</dd>
      </dl>
    </aside>
  </div>
</section>

<section class="section" aria-labelledby="welcome-title">
  <div class="wrap split">
    <div class="prose welcome">
      <h2 id="welcome-title">Welcome</h2>
      <p>Confidence Aviation would like to welcome you to its website.</p>
      <p>We offer a highly skilled staff, and certified technicians with over 55 years of experience.</p>
      <p>Our goal is customer satisfaction and commitment to quality and reliability.</p>
      <p>We look forward to doing business with you.</p>
      <p class="call">Give us a call TODAY at <a href="{PHONE_TEL}">305-392-6291</a>.</p>
      <p><a class="more" href="/about.htm">About Us</a></p>
    </div>
    <figure class="photo">
      <a href="/shop.htm#shop-entrance">{picture("shop-entrance", "View from the shop entrance of workbenches lined with electronic test equipment", sizes="(max-width: 860px) 100vw, 420px")}</a>
      <figcaption>Aviation Workshop Entrance</figcaption>
    </figure>
  </div>
</section>

<section class="section section--alt" aria-labelledby="cap-title">
  <div class="wrap">
    <div class="section__head">
      <div><span class="eyebrow">Avionics &amp; Instruments</span><h2 id="cap-title">Capabilities</h2></div>
      <a class="more" href="/capabilities.htm">All capabilities</a>
    </div>
    <p>Confidence Aviation is authorized the following ratings and limitations:</p>
    <h3>Class Ratings</h3>
    {ratings_list("en")}
    <h3>Limited Ratings</h3>
    <p>Many accessories including Pneumatic Valves and Lights.</p>
  </div>
</section>

<section class="section" aria-labelledby="cert-title">
  <div class="wrap">
    <div class="section__head">
      <div><span class="eyebrow">FAA · EASA</span><h2 id="cert-title">Certificates</h2></div>
      <a class="more" href="/certificates.htm">View all certificates</a>
    </div>
    <div class="grid-3">
      {"".join(f'''<a class="card card--link" href="/certificates.htm#{slug}"><div class="card__media card__media--doc">{doc_thumb(slug, title)}</div><h3>{title}</h3><p class="mono">{short}</p></a>''' for slug, title, _f, _es, short in DOCS)}
    </div>
  </div>
</section>

<section class="section section--alt" aria-labelledby="shop-title">
  <div class="wrap">
    <div class="section__head">
      <div><span class="eyebrow">Shop Tour</span><h2 id="shop-title">Inside our shop</h2></div>
      <a class="more" href="/shop.htm">See the full shop tour</a>
    </div>
    {gallery("en", [s for s in SHOP if s[0] in ("shop-dme-transponder-bench", "shop-radar-bench-1", "shop-altimeter-test-set", "shop-radar-indicators")], "home", compact=True)}
  </div>
</section>

<section class="section section--dark on-dark" aria-labelledby="contact-title">
  <div class="wrap grid-2">
    <div>
      <h2 id="contact-title">Contact Info</h2>
      <address class="address-block">Confidence Aviation, Inc.<br>7605 N.W. 50th Street<br>Miami, FL 33166</address>
      <p>Phone: <a href="{PHONE_TEL}">{PHONE}</a><br>Fax: {FAX}<br>Email: <a href="mailto:{EMAIL}">{EMAIL}</a></p>
      <div class="actions"><a class="btn btn--primary" href="/contact.htm">Contact &amp; directions</a></div>
    </div>
    <div>
      <h2>Aviation Headlines</h2>
      <p>Latest press releases from the FAA newsroom:</p>
      <p><a href="{FAA_RSS}" rel="noopener">FAA newsroom press releases (RSS feed)</a></p>
    </div>
  </div>
</section>
"""
    return layout("en", "home",
                  title="Confidence Aviation - AVIONICS & INSTRUMENTS - FAA Certified Repair Station",
                  desc="Avionics Shop Miami Florida, OEM Alternative. Boeing, Bendix/King, Honeywell, Sperry, Collins.",
                  keywords=KEYWORDS_A, body=body)


def en_about():
    body = page_head("About Us", "Our Company") + f"""
<section class="section">
  <div class="wrap split">
    <div class="prose">
      <p>Confidence Aviation opened its doors in 1998, and customer satisfaction has always been our number one priority. We are FAA &amp; JAA certified, and take pride in providing quality service to all of our customers.</p>
      <p>Confidence Aviation is proud to state that our technicians have over 55 years of experience in aviation service.</p>
      <p>Thank you for taking the time to visit us on the web. We encourage you to visit our offices and see for yourself just how confident we are that we can fulfill all your aviation repair needs. We look forward to doing business with you in the future.</p>
      <div class="signature">
        <p>Sincerely,</p>
        <p class="names">Alex Hernandez, President</p>
        <p class="names" style="margin-top:0">Roberto Perera, President</p>
      </div>
    </div>
    <figure class="photo">
      {picture("alex-and-robert", "Alex Hernandez and Roberto Perera shaking hands", sizes="289px", lazy=False)}
    </figure>
  </div>
</section>
<section class="section section--alt" aria-labelledby="glance">
  <div class="wrap">
    <h2 id="glance">Confidence Aviation at a glance</h2>
    <dl class="spec">
      <dt>Opened</dt><dd>1998</dd>
      <dt>FAA repair station No.</dt><dd><span class="mono">V9DR072Y</span> — <a href="/certificates.htm#air-agency-certificate">Air Agency Certificate</a></dd>
      <dt>EASA approval</dt><dd><span class="mono">EASA.145.5139</span> — <a href="/certificates.htm#easa-approval-certificate">European Aviation Safety Agency Approval Certificate</a></dd>
      <dt>Ratings</dt><dd>Radio Class 1, 2 &amp; 3; Limited Ratings — <a href="/capabilities.htm">Our Capabilities</a></dd>
      <dt>Experience</dt><dd>Technicians with over 55 years of experience in aviation service</dd>
      <dt>Offices</dt><dd><address>Confidence Aviation, Inc., 7605 N.W. 50th Street, Miami, FL 33166</address></dd>
    </dl>
    <div class="actions"><a class="btn btn--primary" href="/contact.htm">Contact Info</a><a class="btn btn--outline" href="/shop.htm">Shop Tour</a></div>
  </div>
</section>
"""
    return layout("en", "about", crumbs=[("About Us", "/about.htm")],
                  title="About Us – Our Company | Confidence Aviation, Inc., Miami, FL",
                  desc="Avionics repair shop Miami Florida. Providing OEM alternative repairs for Boeing, Bendix/King, Honeywell, Sperry, Collins aircraft instrument panels and valves.",
                  keywords=KEYWORDS_A, body=body)


def en_capabilities():
    links = "".join(f'<li><a href="/shop.htm#{s}">{cap}</a></li>' for s, cap, *_ in SHOP)
    body = page_head("Capabilities", "Our Capabilities", "Avionics &amp; Instruments — FAA Certified Repair Station") + f"""
<section class="section" aria-labelledby="ratings">
  <div class="wrap split">
    <div>
      <h2 id="ratings">Ratings and limitations</h2>
      <p>Confidence Aviation is authorized the following ratings and limitations:</p>
      <h3>Class Ratings</h3>
      {ratings_list("en")}
      <h3>Limited Ratings</h3>
      <p>Many accessories including Pneumatic Valves and Lights.</p>
      <div class="notice"><p>Please call our offices at <a href="{PHONE_TEL}">1-305-392-6291</a> for a complete list.</p></div>
    </div>
    <div>
      <figure class="photo">{picture("hugo-in-the-shop", "Hugo at a test bench in the shop", sizes="232px")}</figure>
      <div class="card" style="margin-top:1.25rem">
        <h3>Where these ratings are documented</h3>
        <p>The class ratings and limited ratings are listed in the FAA <a href="/certificates.htm#operations-specifications">Operations Specifications (A003. Ratings and Limitations)</a> and the <a href="/certificates.htm#air-agency-certificate">Air Agency Certificate</a>, No. <span class="mono">V9DR072Y</span>.</p>
      </div>
    </div>
  </div>
</section>
<section class="section section--alt" aria-labelledby="avionics">
  <div class="wrap">
    <h2 id="avionics">Avionics &amp; Instruments</h2>
    <p class="prose">Avionics repair shop Miami Florida. Providing OEM alternative repairs for Boeing, Bendix/King, Honeywell, Sperry, Collins aircraft instrument panels and valves.</p>
    <ul class="tag-list" aria-label="Manufacturers">
      <li>Boeing</li><li>Bendix/King</li><li>Honeywell</li><li>Sperry</li><li>Collins</li>
    </ul>
  </div>
</section>
<section class="section" aria-labelledby="benches">
  <div class="wrap">
    <div class="section__head"><h2 id="benches">Test benches and equipment in our shop</h2><a class="more" href="/shop.htm">Shop Tour</a></div>
    <ul class="link-list">{links}</ul>
  </div>
</section>
"""
    return layout("en", "capabilities", crumbs=[("Capabilities", "/capabilities.htm")],
                  title="Our Capabilities – Radio Class 1, 2 & 3 Ratings | Confidence Aviation",
                  desc="Avionics shop Miami Florida. OEM Alternative repair station for Boeing, Bendix/King, Honeywell, Sperry, Collins aircraft instruments and valves.",
                  body=body)


def doc_sections(lang):
    out = []
    for slug, title, orig, es_title, short in DOCS:
        spec = "".join(f"<dt>{en if lang == 'en' else es}</dt><dd>{v}</dd>" for en, es, v in SPEC[slug])
        size_kb = round((ROOT / "legacy" / "original-site" / orig).stat().st_size / 1024)
        ext = orig.rsplit(".", 1)[1].upper()
        if lang == "en":
            h = f"<h2>{title}</h2>"
            links = (f'<li><a href="{full_src(slug)}" data-lightbox="docs" data-caption="{e(title)}">View full size</a></li>'
                     f'<li><a href="/{e(orig)}">Original file ({ext}, {size_kb} KB)</a></li>')
            summ, note = "Full text of the document", ""
        else:
            h = f'<h2><span lang="en">{title}</span></h2><p class="note">{es_title}</p>'
            links = (f'<li><a href="{full_src(slug)}" data-lightbox="docs" data-caption="{e(title)}">Ver en tamaño completo</a></li>'
                     f'<li><a href="/{e(orig)}">Archivo original ({ext}, {size_kb} KB)</a></li>')
            summ = "Texto completo del documento (en inglés, tal como fue emitido)"
            note = ""
        thumb_alt = f"{title} — scanned document" if lang == "en" else f"{title} — documento escaneado"
        out.append(f"""
<article class="doc" id="{slug}" aria-labelledby="{slug}-h">
  <div class="doc__image">
    <a href="{full_src(slug)}" data-lightbox="docs" data-caption="{e(title)}">{doc_thumb(slug, thumb_alt)}</a>
    <ul class="doc__links">{links}</ul>
  </div>
  <div>
    <div id="{slug}-h">{h}</div>
    <dl class="spec">{spec}</dl>
    <details><summary>{summ}</summary><div class="transcript" lang="en">{TRANSCRIPT[slug]}</div></details>{note}
  </div>
</article>""")
    return "".join(out)


def doc_index(lang):
    return '<ul class="doc-index">' + "".join(
        f'<li><a href="#{slug}">{picture(slug, "", sizes="52px", max_w=320)}<span><span lang="en">{title}</span><small>{short}</small></span></a></li>'
        for slug, title, _o, _es, short in DOCS) + "</ul>"


def en_certificates():
    body = page_head("Certificates", "Our Certificates", "FAA repair station No. V9DR072Y") + f"""
<section class="section" aria-labelledby="list">
  <div class="wrap">
    <h2 id="list">Certificate List</h2>
    {doc_index("en")}
    <div class="notice" style="margin-top:1.5rem"><p>The document images below are the certificates as displayed on our previous website. Text transcriptions are provided for accessibility and search; the document images are the authoritative record. For the current status of any certificate, contact us at <a href="mailto:{EMAIL}">{EMAIL}</a>.</p></div>
    {doc_sections("en")}
  </div>
</section>
"""
    return layout("en", "certificates", crumbs=[("Certificates", "/certificates.htm")],
                  title="Our Certificates – FAA Air Agency Certificate V9DR072Y & EASA.145.5139 | Confidence Aviation",
                  desc="Confidence Aviation certificates: FAA Air Agency Certificate No. V9DR072Y, European Aviation Safety Agency Approval Certificate EASA.145.5139 and FAA Operations Specifications.",
                  body=body, og_image="/assets/img/air-agency-certificate-545.jpg")


def en_shop():
    body = page_head("Shop Tour", "Shop Tour", "Select an image to enlarge it. Use the arrow keys to move between images.") + f"""
<section class="section" aria-labelledby="images">
  <div class="wrap">
    <h2 id="images">Images</h2>
    {gallery("en", SHOP, "shop", with_ids=True)}
  </div>
</section>
<section class="section section--alt">
  <div class="wrap split split--reverse">
    <figure class="photo">{picture("roberto-in-shop", "Roberto at a rack of test equipment in the shop", sizes="(max-width: 860px) 100vw, 407px")}</figure>
    <div class="prose">
      <h2>Visit our offices</h2>
      <address class="address-block">Confidence Aviation, Inc.<br>7605 N.W. 50th Street<br>Miami, FL 33166</address>
      <p>Phone: <a href="{PHONE_TEL}">{PHONE}</a></p>
      <div class="actions"><a class="btn btn--primary" href="/contact.htm">Contact Info</a></div>
    </div>
  </div>
</section>
"""
    return layout("en", "shop", crumbs=[("Shop Tour", "/shop.htm")],
                  title="Shop Tour – Avionics Test Benches | Confidence Aviation, Miami, FL",
                  desc="Photos of the Confidence Aviation shop in Miami, Florida: DME transponder, radar, NAV/COMM and altimeter benches, altimeter test set, HF antenna, radar indicators and radio altimeters.",
                  body=body)


def contact_form(lang):
    L = {"en": {"h": "Send us a message", "intro": f"Submitting this form opens your email app with the message addressed to {EMAIL}.",
                "name": "Name", "company": "Company", "email": "Email", "phone": "Phone", "subject": "Subject",
                "message": "Message", "req": "required", "send": "Compose email",
                "hint_msg": "For example part numbers, units and the work required."},
         "es": {"h": "Envíenos un mensaje", "intro": f"Al enviar este formulario se abrirá su aplicación de correo con el mensaje dirigido a {EMAIL}.",
                "name": "Nombre", "company": "Empresa", "email": "Correo electrónico", "phone": "Teléfono", "subject": "Asunto",
                "message": "Mensaje", "req": "obligatorio", "send": "Redactar correo",
                "hint_msg": "Por ejemplo, números de parte, unidades y el trabajo requerido."}}[lang]
    r = f' <span class="hint" style="display:inline">({L["req"]})</span>'
    return f"""
<form id="contact-form" action="mailto:{EMAIL}" method="post" enctype="text/plain" novalidate>
  <h2>{L['h']}</h2>
  <p class="note">{L['intro']}</p>
  <div class="field"><label for="f-name">{L['name']}{r}</label><input id="f-name" name="name" autocomplete="name" required></div>
  <div class="field"><label for="f-company">{L['company']}</label><input id="f-company" name="company" autocomplete="organization"></div>
  <div class="field"><label for="f-email">{L['email']}{r}</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
  <div class="field"><label for="f-phone">{L['phone']}</label><input id="f-phone" name="phone" type="tel" autocomplete="tel"></div>
  <div class="field"><label for="f-subject">{L['subject']}{r}</label><input id="f-subject" name="subject" required></div>
  <div class="field"><label for="f-message">{L['message']}{r}<span class="hint" id="f-message-hint">{L['hint_msg']}</span></label><textarea id="f-message" name="message" aria-describedby="f-message-hint" required></textarea></div>
  <button class="btn btn--primary" type="submit">{L['send']}</button>
  <p class="form-status" role="status" aria-live="polite"></p>
</form>"""


def en_contact():
    body = page_head("Contact", "Contact Info") + f"""
<section class="section">
  <div class="wrap split">
    <div>
      <address class="address-block">Confidence Aviation, Inc.<br>7605 N.W. 50th Street<br>Miami, FL 33166</address>
      <ul class="contact-list" style="margin-top:1.25rem">
        <li><span class="k">Phone</span><span class="v"><a href="{PHONE_TEL}">{PHONE}</a></span></li>
        <li><span class="k">Fax</span><span class="v">{FAX}</span></li>
        <li><span class="k">Email</span><span class="v"><a href="mailto:{EMAIL}">{EMAIL}</a></span></li>
      </ul>
      <p>Feel free to contact our Director of Business &amp; Sales<br><strong>Maria Aniag Mikluscar</strong></p>
      <h2>Directions</h2>
      <ul class="link-list" style="columns:1">
        <li>Get directions from Miami International (MIA) Airport &gt; <a href="http://mapq.st/mPYIIX" rel="noopener" target="_blank">HERE<span class="visually-hidden"> – directions from MIA (MapQuest, opens in a new tab)</span></a></li>
        <li>Get directions from Fort Lauderdale International (FLL) Airport &gt; <a href="http://mapq.st/o5gaCs" rel="noopener" target="_blank">HERE<span class="visually-hidden"> – directions from FLL (MapQuest, opens in a new tab)</span></a></li>
        <li>Get directions from Fort Lauderdale Executive (FXE) Airport &gt; <a href="http://mapq.st/oRBGHw" rel="noopener" target="_blank">HERE<span class="visually-hidden"> – directions from FXE (MapQuest, opens in a new tab)</span></a></li>
        <li><a href="{OSM}" rel="noopener">View 7605 N.W. 50th Street, Miami, FL 33166 on a map</a></li>
      </ul>
      <figure class="photo" style="max-width:280px;margin-top:2rem">{picture("reception", "Reception desk", sizes="248px")}</figure>
    </div>
    <div class="card">{contact_form("en")}</div>
  </div>
</section>
"""
    return layout("en", "contact", crumbs=[("Contact", "/contact.htm")],
                  title="Contact Info – 7605 N.W. 50th Street, Miami, FL 33166 | Confidence Aviation",
                  desc="Contact Confidence Aviation, Inc., 7605 N.W. 50th Street, Miami, FL 33166. Phone 1-305-392-6291, fax 1-305-392-6292, info@confidenceaviation.com. Directions from MIA, FLL and FXE airports.",
                  body=body)


# ---------------------------------------------------------------- pages: Spanish
def es_home():
    body = f"""
<section class="hero on-dark" aria-labelledby="hero-title">
  <h1 class="hero__banner" id="hero-title">{BANNER}</h1>
  <div class="wrap hero__grid">
    <div>
      <span class="eyebrow">Aviónica e instrumentos · Estación reparadora certificada por la FAA</span>
      <p class="cert-line">Estación reparadora FAA No. V9DR072Y</p>
      <p class="lead">Somos una estación reparadora certificada por la FAA / EASA que ofrece capacidades de reparación general (overhaul) y reparación.</p>
      <div class="actions">
        <a class="btn btn--primary" href="{PHONE_TEL}">Llamar al {PHONE}</a>
        <a class="btn btn--outline" href="/es/capabilities.htm">Nuestras capacidades</a>
      </div>
    </div>
    <aside class="dataplate" aria-labelledby="dp-title">
      <p class="dataplate__title" id="dp-title">Datos de la estación reparadora</p>
      <dl>
        <dt>Certificado de Agencia Aérea FAA</dt><dd><span class="mono">V9DR072Y</span></dd>
        <dt>Aprobación EASA</dt><dd><span class="mono">EASA.145.5139</span></dd>
        <dt>Habilitaciones de clase</dt><dd>Radio Class 1, 2 y 3</dd>
        <dt>Habilitaciones limitadas</dt><dd>Accesorios</dd>
        <dt>Apertura</dt><dd>1998</dd>
        <dt>Ubicación</dt><dd>7605 N.W. 50th Street, Miami, FL 33166</dd>
      </dl>
    </aside>
  </div>
</section>

<section class="section" aria-labelledby="welcome-title">
  <div class="wrap split">
    <div class="prose welcome">
      <h2 id="welcome-title">Bienvenidos</h2>
      <p>Confidence Aviation le da la bienvenida a su sitio web.</p>
      <p>Contamos con un personal altamente calificado y técnicos certificados con más de 55 años de experiencia.</p>
      <p>Nuestra meta es la satisfacción del cliente y el compromiso con la calidad y la confiabilidad.</p>
      <p>Esperamos hacer negocios con usted.</p>
      <p class="call">Llámenos HOY al <a href="{PHONE_TEL}">305-392-6291</a>.</p>
      <p><a class="more" href="/es/about.htm">Nosotros</a></p>
    </div>
    <figure class="photo">
      <a href="/es/shop.htm#shop-entrance">{picture("shop-entrance", "Vista desde la entrada del taller de bancos de trabajo con equipos electrónicos de prueba", sizes="(max-width: 860px) 100vw, 420px")}</a>
      <figcaption>Taller de aviación: entrada</figcaption>
    </figure>
  </div>
</section>

<section class="section section--alt" aria-labelledby="cap-title">
  <div class="wrap">
    <div class="section__head">
      <div><span class="eyebrow">Aviónica e instrumentos</span><h2 id="cap-title">Capacidades</h2></div>
      <a class="more" href="/es/capabilities.htm">Todas las capacidades</a>
    </div>
    <p>Confidence Aviation está autorizada para las siguientes habilitaciones y limitaciones:</p>
    <h3>Habilitaciones de clase (<span lang="en">Class Ratings</span>)</h3>
    {ratings_list("es")}
    <h3>Habilitaciones limitadas (<span lang="en">Limited Ratings</span>)</h3>
    <p>Muchos accesorios, incluidas válvulas neumáticas y luces.</p>
  </div>
</section>

<section class="section" aria-labelledby="cert-title">
  <div class="wrap">
    <div class="section__head">
      <div><span class="eyebrow">FAA · EASA</span><h2 id="cert-title">Certificados</h2></div>
      <a class="more" href="/es/certificates.htm">Ver todos los certificados</a>
    </div>
    <div class="grid-3">
      {"".join(f'''<a class="card card--link" href="/es/certificates.htm#{slug}"><div class="card__media card__media--doc">{doc_thumb(slug, title)}</div><h3 lang="en">{title}</h3><p>{es}</p><p class="mono">{short}</p></a>''' for slug, title, _f, es, short in DOCS)}
    </div>
  </div>
</section>

<section class="section section--alt" aria-labelledby="shop-title">
  <div class="wrap">
    <div class="section__head">
      <div><span class="eyebrow">Recorrido del taller</span><h2 id="shop-title">Nuestro taller</h2></div>
      <a class="more" href="/es/shop.htm">Ver el recorrido completo</a>
    </div>
    {gallery("es", [s for s in SHOP if s[0] in ("shop-dme-transponder-bench", "shop-radar-bench-1", "shop-altimeter-test-set", "shop-radar-indicators")], "home", compact=True)}
  </div>
</section>

<section class="section section--dark on-dark" aria-labelledby="contact-title">
  <div class="wrap grid-2">
    <div>
      <h2 id="contact-title">Información de contacto</h2>
      <address class="address-block">Confidence Aviation, Inc.<br>7605 N.W. 50th Street<br>Miami, FL 33166</address>
      <p>Teléfono: <a href="{PHONE_TEL}">{PHONE}</a><br>Fax: {FAX}<br>Correo electrónico: <a href="mailto:{EMAIL}">{EMAIL}</a></p>
      <div class="actions"><a class="btn btn--primary" href="/es/contact.htm">Contacto y cómo llegar</a></div>
    </div>
    <div>
      <h2>Noticias de aviación</h2>
      <p>Últimos comunicados de prensa de la FAA:</p>
      <p><a href="{FAA_RSS}" rel="noopener" hreflang="en">Comunicados de prensa de la FAA (fuente RSS, en inglés)</a></p>
    </div>
  </div>
</section>
"""
    return layout("es", "home",
                  title="Confidence Aviation - Aviónica e instrumentos - Estación reparadora certificada por la FAA",
                  desc="Taller de aviónica en Miami, Florida. Alternativa al OEM. Boeing, Bendix/King, Honeywell, Sperry, Collins.",
                  keywords=KEYWORDS_A, body=body)


def es_about():
    body = page_head("Nosotros", "Nuestra empresa") + f"""
<section class="section">
  <div class="wrap split">
    <div class="prose">
      <p>Confidence Aviation abrió sus puertas en 1998 y la satisfacción del cliente siempre ha sido nuestra prioridad número uno. Estamos certificados por la FAA y JAA, y nos enorgullece brindar un servicio de calidad a todos nuestros clientes.</p>
      <p>Confidence Aviation se enorgullece de afirmar que nuestros técnicos tienen más de 55 años de experiencia en servicios de aviación.</p>
      <p>Gracias por tomarse el tiempo de visitarnos en la web. Le invitamos a visitar nuestras oficinas y comprobar por sí mismo cuán seguros estamos de poder satisfacer todas sus necesidades de reparación aeronáutica. Esperamos hacer negocios con usted en el futuro.</p>
      <div class="signature">
        <p>Atentamente,</p>
        <p class="names">Alex Hernandez, Presidente</p>
        <p class="names" style="margin-top:0">Roberto Perera, Presidente</p>
      </div>
    </div>
    <figure class="photo">
      {picture("alex-and-robert", "Alex Hernandez y Roberto Perera estrechándose la mano", sizes="289px", lazy=False)}
    </figure>
  </div>
</section>
<section class="section section--alt" aria-labelledby="glance">
  <div class="wrap">
    <h2 id="glance">Confidence Aviation en resumen</h2>
    <dl class="spec">
      <dt>Apertura</dt><dd>1998</dd>
      <dt>Estación reparadora FAA No.</dt><dd><span class="mono">V9DR072Y</span> — <a href="/es/certificates.htm#air-agency-certificate"><span lang="en">Air Agency Certificate</span></a></dd>
      <dt>Aprobación EASA</dt><dd><span class="mono">EASA.145.5139</span> — <a href="/es/certificates.htm#easa-approval-certificate">Certificado de aprobación de la EASA</a></dd>
      <dt>Habilitaciones</dt><dd>Radio Class 1, 2 y 3; habilitaciones limitadas — <a href="/es/capabilities.htm">Nuestras capacidades</a></dd>
      <dt>Experiencia</dt><dd>Técnicos con más de 55 años de experiencia en servicios de aviación</dd>
      <dt>Oficinas</dt><dd><address>Confidence Aviation, Inc., 7605 N.W. 50th Street, Miami, FL 33166</address></dd>
    </dl>
    <div class="actions"><a class="btn btn--primary" href="/es/contact.htm">Información de contacto</a><a class="btn btn--outline" href="/es/shop.htm">Recorrido del taller</a></div>
  </div>
</section>
"""
    return layout("es", "about", crumbs=[("Nosotros", "/es/about.htm")],
                  title="Nosotros – Nuestra empresa | Confidence Aviation, Inc., Miami, FL",
                  desc="Taller de reparación de aviónica en Miami, Florida. Reparaciones como alternativa al OEM para paneles de instrumentos y válvulas de aeronaves Boeing, Bendix/King, Honeywell, Sperry, Collins.",
                  keywords=KEYWORDS_A, body=body)


def es_capabilities():
    links = "".join(f'<li><a href="/es/shop.htm#{s}">{cap_es}</a></li>' for s, _c, cap_es, *_ in SHOP)
    body = page_head("Capacidades", "Nuestras capacidades", "Aviónica e instrumentos — Estación reparadora certificada por la FAA") + f"""
<section class="section" aria-labelledby="ratings">
  <div class="wrap split">
    <div>
      <h2 id="ratings">Habilitaciones y limitaciones</h2>
      <p>Confidence Aviation está autorizada para las siguientes habilitaciones y limitaciones:</p>
      <h3>Habilitaciones de clase (<span lang="en">Class Ratings</span>)</h3>
      {ratings_list("es")}
      <h3>Habilitaciones limitadas (<span lang="en">Limited Ratings</span>)</h3>
      <p>Muchos accesorios, incluidas válvulas neumáticas y luces.</p>
      <div class="notice"><p>Llame a nuestras oficinas al <a href="{PHONE_TEL}">1-305-392-6291</a> para obtener una lista completa.</p></div>
    </div>
    <div>
      <figure class="photo">{picture("hugo-in-the-shop", "Hugo en un banco de pruebas del taller", sizes="232px")}</figure>
      <div class="card" style="margin-top:1.25rem">
        <h3>Dónde constan estas habilitaciones</h3>
        <p>Las habilitaciones de clase y las habilitaciones limitadas figuran en las <a href="/es/certificates.htm#operations-specifications"><span lang="en">Operations Specifications</span> (A003. <span lang="en">Ratings and Limitations</span>)</a> de la FAA y en el <a href="/es/certificates.htm#air-agency-certificate"><span lang="en">Air Agency Certificate</span></a> No. <span class="mono">V9DR072Y</span>.</p>
      </div>
    </div>
  </div>
</section>
<section class="section section--alt" aria-labelledby="avionics">
  <div class="wrap">
    <h2 id="avionics">Aviónica e instrumentos</h2>
    <p class="prose">Taller de reparación de aviónica en Miami, Florida. Reparaciones como alternativa al OEM para paneles de instrumentos y válvulas de aeronaves Boeing, Bendix/King, Honeywell, Sperry, Collins.</p>
    <ul class="tag-list" aria-label="Fabricantes">
      <li>Boeing</li><li>Bendix/King</li><li>Honeywell</li><li>Sperry</li><li>Collins</li>
    </ul>
  </div>
</section>
<section class="section" aria-labelledby="benches">
  <div class="wrap">
    <div class="section__head"><h2 id="benches">Bancos y equipos de prueba de nuestro taller</h2><a class="more" href="/es/shop.htm">Recorrido del taller</a></div>
    <ul class="link-list">{links}</ul>
  </div>
</section>
"""
    return layout("es", "capabilities", crumbs=[("Capacidades", "/es/capabilities.htm")],
                  title="Nuestras capacidades – Habilitaciones Radio Class 1, 2 y 3 | Confidence Aviation",
                  desc="Taller de aviónica en Miami, Florida. Estación reparadora alternativa al OEM para instrumentos y válvulas de aeronaves Boeing, Bendix/King, Honeywell, Sperry, Collins.",
                  body=body)


def es_certificates():
    body = page_head("Certificados", "Nuestros certificados", "Estación reparadora FAA No. V9DR072Y") + f"""
<section class="section" aria-labelledby="list">
  <div class="wrap">
    <h2 id="list">Lista de certificados</h2>
    {doc_index("es")}
    <div class="notice" style="margin-top:1.5rem"><p>Las imágenes siguientes son los certificados tal como se mostraban en nuestro sitio web anterior. Los documentos originales están en inglés; sus datos y su texto completo se reproducen tal como fueron emitidos. Las imágenes de los documentos son el registro oficial. Para conocer el estado actual de cualquier certificado, escríbanos a <a href="mailto:{EMAIL}">{EMAIL}</a>.</p></div>
    {doc_sections("es")}
  </div>
</section>
"""
    return layout("es", "certificates", crumbs=[("Certificados", "/es/certificates.htm")],
                  title="Nuestros certificados – FAA V9DR072Y y EASA.145.5139 | Confidence Aviation",
                  desc="Certificados de Confidence Aviation: Air Agency Certificate de la FAA No. V9DR072Y, certificado de aprobación de la EASA EASA.145.5139 y Operations Specifications de la FAA.",
                  body=body, og_image="/assets/img/air-agency-certificate-545.jpg")


def es_shop():
    body = page_head("Recorrido del taller", "Recorrido del taller", "Seleccione una imagen para ampliarla. Use las teclas de flecha para pasar de una imagen a otra.") + f"""
<section class="section" aria-labelledby="images">
  <div class="wrap">
    <h2 id="images">Imágenes</h2>
    {gallery("es", SHOP, "shop", with_ids=True)}
  </div>
</section>
<section class="section section--alt">
  <div class="wrap split split--reverse">
    <figure class="photo">{picture("roberto-in-shop", "Roberto junto a un bastidor de equipos de prueba en el taller", sizes="(max-width: 860px) 100vw, 407px")}</figure>
    <div class="prose">
      <h2>Visite nuestras oficinas</h2>
      <address class="address-block">Confidence Aviation, Inc.<br>7605 N.W. 50th Street<br>Miami, FL 33166</address>
      <p>Teléfono: <a href="{PHONE_TEL}">{PHONE}</a></p>
      <div class="actions"><a class="btn btn--primary" href="/es/contact.htm">Información de contacto</a></div>
    </div>
  </div>
</section>
"""
    return layout("es", "shop", crumbs=[("Recorrido del taller", "/es/shop.htm")],
                  title="Recorrido del taller – Bancos de prueba de aviónica | Confidence Aviation, Miami, FL",
                  desc="Fotos del taller de Confidence Aviation en Miami, Florida: bancos de DME y transpondedor, radar, NAV/COMM y altímetro, equipo de prueba de altímetros, antena HF, indicadores de radar y radioaltímetros.",
                  body=body)


def es_contact():
    body = page_head("Contacto", "Información de contacto") + f"""
<section class="section">
  <div class="wrap split">
    <div>
      <address class="address-block">Confidence Aviation, Inc.<br>7605 N.W. 50th Street<br>Miami, FL 33166</address>
      <ul class="contact-list" style="margin-top:1.25rem">
        <li><span class="k">Teléfono</span><span class="v"><a href="{PHONE_TEL}">{PHONE}</a></span></li>
        <li><span class="k">Fax</span><span class="v">{FAX}</span></li>
        <li><span class="k">Correo</span><span class="v"><a href="mailto:{EMAIL}">{EMAIL}</a></span></li>
      </ul>
      <p>No dude en contactar a <strong>Maria Aniag Mikluscar</strong>, a cargo de la Dirección de Negocios y Ventas (<span lang="en">Director of Business &amp; Sales</span>).</p>
      <h2>Cómo llegar</h2>
      <ul class="link-list" style="columns:1">
        <li>Cómo llegar desde el Aeropuerto Internacional de Miami (MIA) &gt; <a href="http://mapq.st/mPYIIX" rel="noopener" target="_blank">AQUÍ<span class="visually-hidden"> – indicaciones desde MIA (MapQuest, se abre en una pestaña nueva)</span></a></li>
        <li>Cómo llegar desde el Aeropuerto Internacional de Fort Lauderdale (FLL) &gt; <a href="http://mapq.st/o5gaCs" rel="noopener" target="_blank">AQUÍ<span class="visually-hidden"> – indicaciones desde FLL (MapQuest, se abre en una pestaña nueva)</span></a></li>
        <li>Cómo llegar desde el Aeropuerto Ejecutivo de Fort Lauderdale (FXE) &gt; <a href="http://mapq.st/oRBGHw" rel="noopener" target="_blank">AQUÍ<span class="visually-hidden"> – indicaciones desde FXE (MapQuest, se abre en una pestaña nueva)</span></a></li>
        <li><a href="{OSM}" rel="noopener">Ver 7605 N.W. 50th Street, Miami, FL 33166 en un mapa</a></li>
      </ul>
      <figure class="photo" style="max-width:280px;margin-top:2rem">{picture("reception", "Recepción", sizes="248px")}</figure>
    </div>
    <div class="card">{contact_form("es")}</div>
  </div>
</section>
"""
    return layout("es", "contact", crumbs=[("Contacto", "/es/contact.htm")],
                  title="Información de contacto – 7605 N.W. 50th Street, Miami, FL 33166 | Confidence Aviation",
                  desc="Contacte a Confidence Aviation, Inc., 7605 N.W. 50th Street, Miami, FL 33166. Teléfono 1-305-392-6291, fax 1-305-392-6292, info@confidenceaviation.com. Cómo llegar desde los aeropuertos MIA, FLL y FXE.",
                  body=body)


# ---------------------------------------------------------------- special files
def not_found():
    body = f"""
<section class="section">
  <div class="wrap prose">
    <p class="error-code">404</p>
    <h1>Page not found</h1>
    <p>The page you requested does not exist or has moved. Every page from our previous website is still available at its original address:</p>
    <ul>{"".join(f'<li><a href="{url("en", p)}">{UI["en"]["nav"][p]}</a></li>' for p in PAGES)}</ul>
    <div lang="es">
      <h2>Página no encontrada</h2>
      <p>La página solicitada no existe o se ha movido.</p>
      <ul>{"".join(f'<li><a href="{url("es", p)}">{UI["es"]["nav"][p]}</a></li>' for p in PAGES)}</ul>
    </div>
    <p>Phone / Teléfono: <a href="{PHONE_TEL}">{PHONE}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>
  </div>
</section>"""
    out = layout("en", "home", title="Page not found | Confidence Aviation", desc="Page not found.", body=body, noindex=True)
    return out.replace(' aria-current="page"', "")  # no nav item is current on the 404 page


def relativize(page_html, depth):
    """Make site-internal links relative so the site works at any base path
    (domain root, GitHub Pages project URL, local web server). Absolute
    https:// URLs (canonical, hreflang, Open Graph, JSON-LD) are untouched."""
    import re
    prefix = "../" * depth
    out = re.sub(r'((?:href|src|srcset|action)=")/(?!/)', lambda m: m.group(1) + prefix, page_html)
    out = re.sub(r'(srcset="[^"]*)', lambda m: m.group(1).replace(", /assets", ", " + prefix + "assets"), out)
    return out.replace('href=""', 'href="./"')


def redirect_stub(target):
    """Static fallback for hosts that ignore .htaccess: the old URL keeps working."""
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>Confidence Aviation - AVIONICS &amp; INSTRUMENTS - FAA Certified Repair Station</title>
<link rel="canonical" href="{SITE}/">
<meta name="robots" content="noindex, follow">
<meta http-equiv="refresh" content="0; url={target}">
</head><body><p>This page has moved to <a href="{target}">{SITE}/</a>.</p></body></html>
"""


def sitemap():
    rows = []
    for p in PAGES:
        for lang in ("en", "es"):
            alts = "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{SITE}{url(l, p)}"/>' for l in ("en", "es"))
            alts += f'<xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{url("en", p)}"/>'
            rows.append(f"  <url><loc>{SITE}{url(lang, p)}</loc>{alts}</url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
            + "\n".join(rows) + "\n</urlset>\n")


ROBOTS = f"""User-agent: *
Allow: /

Sitemap: {SITE}/sitemap.xml
"""


def main():
    global ASSET_V
    (PUB / "assets" / "css").mkdir(parents=True, exist_ok=True)
    (PUB / "assets" / "js").mkdir(parents=True, exist_ok=True)
    (PUB / "es").mkdir(exist_ok=True)
    ASSET_V = {}
    for kind, name in (("css", "site.css"), ("js", "site.js")):
        data = (SRC / "assets" / kind / name).read_bytes()
        (PUB / "assets" / kind / name).write_bytes(data)
        ASSET_V[kind] = hashlib.sha256(data).hexdigest()[:10]

    pages = {
        "index.html": en_home(), "about.htm": en_about(), "capabilities.htm": en_capabilities(),
        "certificates.htm": en_certificates(), "shop.htm": en_shop(), "contact.htm": en_contact(),
        "es/index.html": es_home(), "es/about.htm": es_about(), "es/capabilities.htm": es_capabilities(),
        "es/certificates.htm": es_certificates(), "es/shop.htm": es_shop(), "es/contact.htm": es_contact(),
        "404.html": not_found(),
        "index.htm": redirect_stub("./"),
        "sitemap.xml": sitemap(),
        "robots.txt": ROBOTS,
        "site.webmanifest": json.dumps({
            "name": "Confidence Aviation, Inc.", "short_name": "Confidence Aviation",
            "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
                      {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"}],
            "theme_color": "#03204a", "background_color": "#ffffff", "display": "browser"}, indent=1),
    }
    for name, content in pages.items():
        if name.endswith((".html", ".htm")) and name not in ("404.html", "index.htm"):
            content = relativize(content, name.count("/"))
        (PUB / name).write_text(content, encoding="utf-8")
    shutil.copy2(SRC / "htaccess", PUB / ".htaccess")
    print(f"built {len(pages)} files into {PUB.relative_to(ROOT)}/")


ASSET_V = {"css": "", "js": ""}

if __name__ == "__main__":
    main()
