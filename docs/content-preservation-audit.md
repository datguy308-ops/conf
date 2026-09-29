# Content preservation audit — optimization pass

This audit compares the optimized site against two baselines:

1. **The original website.** It was crawled on 2026-09-29. A verbatim copy is in `legacy/original-site/`, and the machine-checked inventory is `tools/inventory.json` (73 items).
2. **The site as it was before this optimization pass.** Every visible text block and image description on every page, in both languages, is in `legacy/pre-optimization-snapshot.json` (824 blocks).

**Status legend**

| Status | Meaning |
|---|---|
| **Verbatim** | The same words appear on the new site. |
| **Rewritten** | Reworded without changing the facts. The original words are still present elsewhere, or the rewrite is listed here. |
| **Reorganized** | The same content on the same page, in a new structure. |
| **Moved** | Now on a different page (the destination is listed). |
| **Historical** | Kept and labelled as coming from the original website. |
| **Flagged** | Kept exactly as published, and listed in `docs/owner-verification-required.md`. |

**How this was verified.** These commands must pass before the site is considered complete, and the Pages workflow runs the first one on every deploy:

- `python3 tools/audit.py` checks four things:
  - every inventory item is at its stated English and Spanish location;
  - all 71 original URLs still resolve;
  - no internal link or anchor is broken;
  - a reverse check extracts every text node, alt/title attribute and meta description/keywords string from the original HTML and requires each one on the new English site. Anything missing must be a documented consolidation or rewrite whose facts are checked as visible text.
- `python3 tools/snapshot.py diff legacy/pre-optimization-snapshot.json` lists every pre-pass text block that no longer appears verbatim. All 74 are explained in [Changes made in this pass](#changes-made-in-this-pass).
- `node tools/qa/qa.js` crawls and tests the site in a browser, including English/Spanish parity of key facts: V9DR072Y, EASA.145.5139, 1998, 2004, 55, both phone numbers, 33166 and A003.

**Result: every meaningful piece of original information is accounted for, and nothing could not be preserved.**

---

## 1. `/` and `/index.htm` — Home

**Original purpose:** welcome page. `/index.htm` was a byte-identical duplicate.

| Important content | Where it is now | Status |
|---|---|---|
| "Welcome" | Home → "Welcome" section heading | Verbatim |
| "Confidence Aviation would like to welcome you to its website." | Home → Welcome | Verbatim |
| "FAA repair station No. V9DR072Y" | Home → Welcome (verbatim line). Also in the hero data panel, top bar, footer, About profile, and Certificates heading and table | Verbatim + repeated |
| "We are an FAA / EASA certified repair station offering overhaul and repair capabilities." | Home → hero lead (first sentence under the headline) | Verbatim · **Flagged** (EASA current status) |
| "We offer a highly skilled staff, and certified technicians with over 55 years of experience." | Home → Welcome | Verbatim · **Flagged** (experience figure dates from 2011 or earlier) |
| "Our goal is customer satisfaction and commitment to quality and reliability." | Home → Welcome | Verbatim |
| "We look forward to doing business with you." | Home → Welcome | Verbatim |
| "Give us a call TODAY at 305-392-6291." | Home → Welcome (tap-to-call link) | Verbatim |
| FAA newsroom press-release feed (third-party jobisite.com widget) | Footer of every page → "Aviation Headlines" → link to the same FAA RSS feed | Moved (the widget script was replaced by a direct link) |
| Commented-out Feedzilla "Aviation Headlines" widget (never visible) | The heading "Aviation Headlines" is kept in the footer | Historical |
| Page title "Confidence Aviation - AVIONICS & INSTRUMENTS - FAA Certified Repair Station" | Rewritten title: "Avionics & Instrument Repair – FAA Repair Station, Miami, FL \| Confidence Aviation". The original wording is visible in the footer tagline on every page: "Avionics & Instruments — FAA Certified Repair Station" | Rewritten (SEO metadata) |
| Meta description "Avionics Shop Miami Florida, OEM Alternative. Boeing, Bendix/King, Honeywell, Sperry, Collins." | Rewritten meta description. Every fact is visible: Miami, Florida; OEM alternative; the five manufacturers (Home → What we repair; Capabilities → Avionics & Instruments) | Rewritten (SEO metadata) |
| Meta keywords | Kept verbatim in `<meta name="keywords">`, including the original "avioncs" spelling | Verbatim |
| Logo (header tiles `ca_01`–`ca_04`) | Replaced at the owner's request by the current brand logo. The original tile files still resolve at their URLs and are archived in `legacy/` | Historical (owner decision, 2026-09-29) |
| Decorative banner tiles `ca_05`–`ca_45` (sky/contrail/globe artwork, no text) | Files still resolve at their original URLs; not displayed | Historical |
| Hidden "Language Option — English / Spanish" block | A working language switcher labelled "Language Option" in the top bar and footer | Rewritten (made functional) |
| Footer "©2003 - 2011 Confidence Aviation, Inc." | Verbatim on About → "Website history". The footer now shows the current notice "© 2003–<year> Confidence Aviation, Inc." | Historical + current notice · **Flagged** (legal name) |
| "Created by wintertek" → http://www.wintertek.com | About → "Website history": "…previous website … was created by wintertek", same link | Moved |
| Navigation: Home, Contact, About Us, Capabilities, Certificates, Shop Tour | Header navigation (same labels) and footer | Verbatim |
| `/index.htm` URL | 301 to `/` in `.htaccess`; `public/index.htm` also forwards via meta refresh for hosts that ignore `.htaccess` | URL preserved by redirect |

## 2. `/about.htm` — About Us / "Our Company"

**Original purpose:** company introduction letter from the two Presidents.

| Important content | Where it is now | Status |
|---|---|---|
| "Our Company" | About → page heading (H1) | Verbatim |
| "Confidence Aviation opened its doors in 1998, and customer satisfaction has always been our number one priority." | About → "A message from our Presidents" | Verbatim |
| "We are FAA & JAA certified, and take pride in providing quality service to all of our customers." | About → "A message from our Presidents". A factual note below the letter says it is reproduced from the original website (©2003 - 2011) and links to the dated certificates | Verbatim · Historical · **Flagged** (JAA wording) |
| "Confidence Aviation is proud to state that our technicians have over 55 years of experience in aviation service." | About → letter (verbatim). Restated in the About → Company profile and the Home → "Why Confidence Aviation" item "Our technicians have over 55 years of experience in aviation service." | Verbatim + restated without strengthening · **Flagged** |
| "Thank you for taking the time to visit us on the web. We encourage you to visit our offices … We look forward to doing business with you in the future." | About → letter | Verbatim |
| "Sincerely, Alex Hernandez, President / Roberto Perera, President" | About → letter signature, and About → Company profile ("Presidents") | Verbatim · **Flagged** (titles) |
| Photo `alex&robert-trans.gif` | About → Company profile (optimized WebP/PNG); the original file still resolves | Verbatim image · **Flagged** (names in alt text come from the file name) |
| Meta description "Avionics repair shop Miami Florida. Providing OEM alternative repairs for Boeing, Bendix/King, Honeywell, Sperry, Collins aircraft instrument panels and valves." | Visible, verbatim, on Capabilities → "Avionics & Instruments". The meta description was rewritten for search | Verbatim (visible) + rewritten metadata · **Flagged** |

## 3. `/capabilities.htm` — "Our Capabilities"

**Original purpose:** list of authorized ratings.

| Important content | Where it is now | Status |
|---|---|---|
| "Our Capabilities" | Capabilities → H1 | Verbatim |
| "Confidence Aviation is authorized the following ratings and limitations:" | Capabilities → "Ratings and limitations", and Home → "What we repair" intro | Verbatim |
| "CLASS RATINGS" | Capabilities → "Class Ratings" heading | Verbatim (case normalized) |
| "Radio Class 1: Communications Equipment (unlimited)" | Capabilities → ratings list (anchor `#communications`). Summary cards on Home and Capabilities: "FAA Radio Class 1 rating (unlimited)" | Verbatim + summarized · **Flagged** ("unlimited" does not appear on the Operations Specifications image) |
| "Radio Class 2: Navigational Equipment (unlimited)" | Same, `#navigation` | Verbatim + summarized · **Flagged** |
| "Radio Class 3: Radar Equipment (unlimited)" | Same, `#radar` | Verbatim + summarized · **Flagged** |
| "Limited Ratings — Many accessories including Pneumatic Valves and Lights." | Capabilities → "Limited Ratings" (`#accessories`); Home card "Limited Ratings: many accessories including pneumatic valves and lights" | Verbatim + summarized |
| "Please call our offices at 1-305-392-6291 for a complete list." | Capabilities → notice (tap-to-call), and Home → below "What we repair" | Verbatim |
| Photo `hugointheshop.png` | Capabilities → beside the ratings | Verbatim image · **Flagged** (name "Hugo" in the alt text comes from the file name) |
| Meta description "…OEM Alternative repair station for Boeing, Bendix/King, Honeywell, Sperry, Collins aircraft instruments and valves." | Facts made visible on Capabilities → "Avionics & Instruments": Scope "Aircraft instruments, instrument panels and valves"; Basis "OEM alternative repair station"; Location "Miami, Florida"; manufacturers listed. The meta description was rewritten | Rewritten metadata; facts visible · **Flagged** (OEM-alternative scope) |
| "AVIONICS & INSTRUMENTS" (page titles) | Home → hero headline, "Avionics & Instruments" eyebrow, capability card; Capabilities lead; footer tagline | Verbatim + reorganized |

## 4. `/certificates.htm` — "Our Certificates"

**Original purpose:** display the three regulatory documents.

| Important content | Where it is now | Status |
|---|---|---|
| "Our Certificates", "Certificate List" | Certificates → H1 and the "Certificate List" table | Verbatim |
| `air_agency_certificate.gif` "Air Agency Certificate" | Certificates → `#air-agency-certificate`: zoomable image, download of the untouched original file, details table and full transcription. Also on Home (certificate card, "Why" item) and in the footer | Verbatim (document + all printed text) · **Flagged** (current status) |
| `easa-cert.jpg` "European Aviation Safety Agency Approval Certificate" | Certificates → `#easa-approval-certificate`, same treatment | Verbatim · **Flagged** (2004 document; current status) |
| `operations_specifications.gif` "Operations Specifications" | Certificates → `#operations-specifications`, same treatment | Verbatim · **Flagged** (2003 amendment) |
| Text printed inside the three documents (numbers, dates, ratings, signatories, conditions, form numbers) | Transcribed verbatim (`tools/documents.py`, unchanged in this pass) in each document's "Full text" and details table. The new "Date on document" column repeats the printed dates | Verbatim |

**Presentation safeguards:**

- Each document shows the date printed on it, and the page states that dates are those printed on each document.
- No document is described as current. The page invites visitors to contact the company for current status.

## 5. `/shop.htm` — "Shop Tour"

**Original purpose:** photo gallery.

| Important content | Where it is now | Status |
|---|---|---|
| "Shop Tour", "IMAGES" | Shop Tour → H1 and the "Images" heading | Verbatim (case normalized) |
| 12 photos with their alt/title captions ("Aviation Workshop Entrance" … "Aviation Workshop Radio Altimeters") | Shop Tour gallery. Each caption is verbatim and visible; each photo has its own anchor and opens in the lightbox. All 12 also appear as thumbnails on Capabilities, 4 on Home, and the entrance photo in Home → Welcome | Verbatim |
| Photo `robertoinshop.png` | Shop Tour → "Visit our offices" | Verbatim image · **Flagged** (name "Roberto" in the alt text comes from the file name) |

## 6. `/contact.htm` — "Contact Info"

**Original purpose:** address, numbers, contact person, directions.

| Important content | Where it is now | Status |
|---|---|---|
| "Contact Info" | Contact → H1 | Verbatim |
| "Confidence Aviation, Inc. 7605 N.W. 50th Street Miami, FL 33166" | Contact card; footer and quote band on every page; Home data panel; About profile; structured data | Verbatim · **Flagged** (confirm current) |
| "Phone: 1-305-392-6291" | Contact card (tap-to-call); top bar, footer and quote band on every page | Verbatim · **Flagged** |
| "Fax: 1-305-392-6292" | Contact card; footer; below the quote form | Verbatim · **Flagged** (in service?) |
| "Email: info@confidenceaviation.com" | Contact card; top bar (desktop), footer and quote band on every page; the quote form addresses this mailbox | Verbatim · **Flagged** |
| "Feel free to contact our Director of Business & Sales Maria Aniag Mikluscar" | Contact card (verbatim); About → Company profile | Verbatim · **Flagged** (still current?) |
| The three "Get directions from … Airport > HERE" links (`mapq.st/mPYIIX`, `mapq.st/o5gaCs`, `mapq.st/oRBGHw`) | Contact → "Directions" (`#directions`): same text, same URLs, with screen-reader context. A Google Maps directions link to the published address was added alongside | Verbatim · **Flagged** (MapQuest short links could not be tested) |
| Photo `reception.gif` | Contact → below Directions | Verbatim image |

## 7. `/robots.txt` and assets

| Item | Where it is now | Status |
|---|---|---|
| `robots.txt` "User-agent: *" | `public/robots.txt`: same, plus `Allow: /` and the sitemap location | Verbatim + extended |
| All 62 original image files and `ca.css` | Still served at their original URLs (checked by `tools/audit.py`) | Preserved |

---

## Changes made in this pass

Each of the 74 pre-pass text blocks that no longer appears verbatim (`tools/snapshot.py diff`) is in one of these groups. None removes information.

| Pre-pass text | What happened | Where the information is now |
|---|---|---|
| Top bar and footer "FAA Repair Station No. V9DR072Y · EASA EASA.145.5139" (all pages) | The top bar now shows the FAA number and "Miami, Florida". The EASA reference moved to the footer with its date: "EASA approval ref. EASA.145.5139 (document dated 2004)". This avoids presenting a 2004 approval as a current credential in the site chrome | Footer (every page); Home data panel and "Why"; About profile; Certificates |
| "Original website created by wintertek" (footer, all pages) | Moved: it credits the previous website, not this one | About → "Website history", same link |
| Home "Repair station data" / ES "Datos de la estación reparadora" | Heading renamed "Repair station at a glance"; the panel now also shows the EASA issue date and a "View certificates" link | Home hero |
| Home contact band "Phone: … Fax: … Email: …" | Replaced by the quote band (phone, email, address) | Fax: footer (every page), Contact, below the quote form |
| Home "Latest press releases from the FAA newsroom:" / "FAA newsroom press releases (RSS feed)" | Moved to the footer, labelled "Aviation Headlines" | Footer (every page) |
| About "Confidence Aviation at a glance" table | Renamed "Company profile" and extended (company name, specialization, ratings, Presidents, Director of Business & Sales). The EASA row now includes the date of issue | About → Company profile |
| Certificates index cards ("Air Agency Certificate No. V9DR072Y" etc.) | Replaced by the "Certificate List" table (document, issuer, number, date on document) | Certificates |
| Certificates notice | One sentence added ("Dates are those printed on each document.") | Certificates |
| Contact form "Send us a message", "Subject", "Message", "Compose email" | Replaced by the "Request a Repair Quote" form (contact, unit and request details; the subject is generated automatically). Still `mailto:`; no backend is claimed | Contact → `#quote` |
| Contact "View 7605 N.W. 50th Street … on a map" (OpenStreetMap; added in an earlier pass, not original content) | Replaced by a Google Maps directions link to the same address | Contact → Directions |
| Shop Tour instruction line | Extended with "Photos of the Confidence Aviation shop and test benches." | Shop Tour lead |
| 404 page phone/email line | Kept, plus quote and call buttons | 404 |

**Wording changes to original facts (all restatements that keep the meaning):**

- "our technicians have over 55 years of experience" → "Over 55 years of experience" (heading). The body text keeps the full sentence. "Combined" and "FAA-certified" were **not** added.
- "opened its doors in 1998" → "In business since 1998" (heading); the body text keeps the original sentence.
- The Radio Class ratings are restated as "FAA Radio Class 1 rating (unlimited)" etc. The verbatim list stays on Capabilities.
- The hero headline "Aircraft Avionics & Instrument Repair" combines the site's own "AVIONICS & INSTRUMENTS" with the meta descriptions' "Avionics repair" and "aircraft instruments". No new capability is implied.

**New copy that makes no factual claim:**

- Section headings, calls to action, form labels, the quote checklist ("Include the manufacturer, model, part number…"), and the notes stating what the form does.
- "Manufacturer names identify the equipment concerned and do not indicate manufacturer authorization." This is a clarification that narrows, not widens, the claim.

## English / Spanish parity

- Both languages are generated by the same functions, so they have the same sections, facts and calls to action. The QA suite (`tools/qa/qa.js`) checks that each English/Spanish page pair has:
  - the same number of sections;
  - the same number of "Request a Repair Quote" links;
  - the same key identifiers and numbers.
- Certificate texts are shown in their original English on the Spanish pages, with a note saying so.
- Regulatory terms are kept in English next to the Spanish (for example "Radio Class 1", "Limited Ratings").
- The Spanish text is a new translation; there was no Spanish on the original site. See `docs/owner-verification-required.md` → Spanish.

## Legacy URLs

All 71 original URLs still work: the 7 page URLs (`/index.htm` by redirect), the 62 images, `ca.css` and `robots.txt`. No URL was changed. The one internal redirect is `/es/index.html` → `/es/`.

## Information that could not be preserved

None.
