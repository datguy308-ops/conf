# Optimization pass — change log

**Goal:** make Confidence Aviation read as a serious, credible aviation repair business that an operator or MRO would contact about a component, **without inventing any fact and without losing any information.**

The companion documents are:

- `docs/content-preservation-audit.md`: where every piece of original content is now.
- `docs/owner-verification-required.md`: facts the company must confirm.

## What was already good and was kept

- **Pages and addresses:** static HTML with no framework, and every original URL.
- **Bilingual structure:** English/Spanish pages with hreflang.
- **Content audit:** the original-site content inventory and audit.
- **Certificates:** document images, transcriptions, and links to the original files.
- **Gallery:** the keyboard-accessible lightbox.
- **Search basics:** sitemap, robots.txt, canonical URLs, the 404 page and the `/index.htm` redirect.
- **Speed, print and fallbacks:** image pipeline, print styles, and the site working without JavaScript.
- **Brand:** the brand colours and transparent logo chosen by the owner.

## Changes by page

### All pages (layout)

| Change | Why |
|---|---|
| **"Request a Quote" button in the header**, inside the menu on phones. Every page links to `contact.htm#quote`. | Makes the main conversion path obvious from any page (§5, §8, §9). |
| **Top bar:** FAA repair station number, "Miami, Florida", phone, email and language. The EASA number moved out of the top bar. | It answers "who, where, how to reach them" immediately. The 2004 EASA approval is no longer presented as a current credential in the site chrome; it appears with its date on Home, About, Certificates and in the footer. |
| **Footer:** business name and tagline, FAA number, EASA reference with its date, contact details, a directions link, pages, links to the three documents, the FAA headlines link and the language option. The copyright now reads "© 2003–<year> Confidence Aviation, Inc.". | A useful, uncluttered footer (§27). Outdated items were not deleted: the old "©2003 - 2011" notice and the wintertek credit are on About → "Website history" (§28). |
| **End-of-page "Request a Repair Quote" band** on Home, About, Capabilities and Shop Tour: what to include, the button, a phone button and the address. | A consistent next step (§9). One call-to-action label is used throughout (§8). |
| **Inline SVG icon set** (radio, navigation, radar, valve, gauge, document, globe, calendar, wrench, test bench, pin, phone, mail). Single-weight line icons, no icon font. | Professional iconography without a dependency (§12). |
| **Spanish header label for Shop Tour shortened to "Taller".** The page title, breadcrumbs and footer keep "Recorrido del taller". | The Spanish header now fits on one line at 1280 px. |

### Home

| Change | Why |
|---|---|
| **Hero headline "Aircraft Avionics & Instrument Repair".** The lead is the original sentence "We are an FAA / EASA certified repair station offering overhaul and repair capabilities." A second line summarizes the FAA ratings. | Answers "what does this company do" in the first seconds, using the site's own terms: "AVIONICS & INSTRUMENTS", "Avionics repair", "aircraft instruments" (§5). |
| **Call-to-action buttons:** "Request a Repair Quote" (primary) and "View Capabilities" (secondary), with phone and email below. | As specified (§5). |
| **"Repair station at a glance" panel:** certificate number, class ratings, limited ratings, EASA reference **with its issue date**, the year opened, the address, and a link to the certificates. | Concrete trust signals, dated honestly (§15, §17). |
| **"What we repair":** five cards built only from documented categories (Radio Class 1/2/3, Limited Ratings – accessories, Avionics & Instruments – OEM alternative). Each links to its anchor on Capabilities. | Visitors no longer have to hunt through paragraphs to find what is repaired (§7). |
| **"Why Confidence Aviation":** six factual items: FAA certificate, EASA reference, since 1998, over 55 years of experience, documented test equipment, and the Miami location with directions. Each links to its evidence. | Trust built on documented facts, not slogans (§6). Generic statements were not added. |
| **"Inside our shop":** four real shop photos with their original captions. | Real facility imagery used prominently (§13). |
| **Certificate cards now show the date printed on each document**, plus the note "Contact us for current certification status". | So historical documents don't look current (§15). |
| **The original Welcome text is kept in full** (verbatim), in its own section. | Preservation. It was moved lower so the first screen serves B2B visitors. |

### About

| Change | Why |
|---|---|
| **New factual lead:** "Confidence Aviation, Inc. is an avionics and instrument repair station in Miami, Florida — FAA repair station No. V9DR072Y, in business since 1998." | Answers who, what, where and since when (§14). |
| **"Company profile" table:** company, year opened, specialization, FAA number, ratings, EASA reference with date, experience, the Presidents, and the Director of Business & Sales, with links to the evidence. | Makes the About page useful rather than just a letter. |
| **The Presidents' letter is kept verbatim** under "A message from our Presidents". A factual note says it is reproduced from the original website (©2003 - 2011) and points to the dated certificates. | Preserves the "FAA & JAA" wording without presenting it as a current certification claim, and without rewriting regulatory history (§16). |
| **"Website history" section:** the previous site's copyright notice and the wintertek credit. | Retained as historical information (§28). |

### Capabilities

| Change | Why |
|---|---|
| Capability cards at the top act as an in-page index. | Fast scanning (§7). |
| **Ratings list with icons and anchors** (`#communications`, `#navigation`, `#radar`, `#accessories`, `#avionics-instruments`). | Deep links from Home. |
| The **"Avionics & Instruments" section keeps the original sentence verbatim** and adds a small table (Scope / Basis / Location). The table makes visible the one fact that was only in metadata: "aircraft instruments and valves". | No information is narrowed or lost (§34). |
| **Manufacturer clarification:** "Manufacturer names identify the equipment concerned and do not indicate manufacturer authorization." | Prevents an implied OEM relationship (§2). |
| All 12 shop photos are shown as test-bench thumbnails linking to the Shop Tour. | Evidence next to the claim. |
| End band headed "Is your unit covered? Request a Repair Quote". | The natural next step for this page (§9). |

### Certificates

| Change | Why |
|---|---|
| The **"Certificate List" is now a table** of document, issuer, number/reference and **date on document**. On phones it becomes stacked cards. | Status and dates understandable at a glance (§15). |
| Each document shows the date printed on it above its details. The links are "View full size" and "Download original file". | Clear document access. |
| End section "Questions about our certification? → Contact Confidence Aviation". | The call to action requested for certificate pages (§9). |
| **No change to any certificate number, rating, date or transcription.** The data was moved unchanged into `tools/documents.py`. | §15. |

### Shop Tour

| Change | Why |
|---|---|
| The lead states "Photos of the Confidence Aviation shop and test benches". | Context without implying date or location details the source does not give (§13). |
| The first two images load eagerly; the rest load as the visitor scrolls. | LCP (§24). |
| "Visit our offices" now links to the directions section, plus the quote band. | Next step. |

### Contact

| Change | Why |
|---|---|
| **"Request a Repair Quote" form** (`#quote`) in three groups: your details; unit details (manufacturer, model, part number, serial numbers, quantity, aircraft type/registration); request (work requested, AOG checkbox, reported fault/details). | Tells visitors exactly what a repair station needs to quote (§10). |
| **Accessible validation:** inline field errors, an error summary that takes focus with links to each field, `aria-invalid`, labelled required fields. | §23. |
| **Honest wording:** "Sending this form opens your own email program … Nothing is sent until you send that email. You can attach photos, work orders or other documents there." The email body is pre-filled with labelled lines, and the subject includes the manufacturer, part number and "AOG" when ticked. | No fake backend and no storage or security claims (§10, §29). |
| The contact card keeps the address, phone, fax, email and Director of Business & Sales verbatim. **Directions:** the three original MapQuest links (verbatim) plus a Google Maps directions link to the published address. | Contact details easy to find; legacy links kept but flagged (§17, §32). |

## SEO

- **Titles and meta descriptions:** rewritten for search intent (avionics and instrument repair, FAA repair station, Miami, the ratings), with no keyword stuffing. The original title and descriptions are recorded, and each fact in them is checked as visible text on the site (`tools/audit.py`).
- **Structured data:** now a single `@graph` per page:
  - **LocalBusiness** (name, URL, logo, image, factual description, founding date 1998, phone, fax, email, FAA Air Agency Certificate number as `identifier`, postal address);
  - **WebSite**;
  - **WebPage** (with `inLanguage` and `about`);
  - **BreadcrumbList** on subpages.

  No ratings, reviews, hours, coordinates, awards or social profiles were added, because none are documented.
- **Heading hierarchy:** one H1 per page and no skipped levels. On Capabilities, the heading for the card index is visually hidden.
- **One URL strategy:** `https://www.confidenceaviation.com` everywhere: canonicals, hreflang, sitemap, Open Graph and JSON-LD (297 references, no variants). The https/www redirects in `.htaccess` stay commented out until the host is confirmed, to avoid redirect loops (§31).
- **Internal links:** deep links from Home cards and "Why" items to their evidence (capability anchors, certificate anchors, About profile, Contact directions).

## Accessibility

- Checked by **axe-core on 13 pages at desktop and mobile widths: 0 violations** (WCAG 2.0/2.1/2.2 A and AA + best practice). Automated testing does not prove compliance; this is a strong baseline, not a legal claim.
- **Keyboard (tested):**
  - the skip link is the first tab stop;
  - the mobile menu opens with Enter and closes with Escape, returning focus;
  - the lightbox opens with Enter, → moves between images, Escape closes it, and focus returns to the thumbnail;
  - the form's error summary takes focus.
- Visible focus rings; touch targets of at least 44 px for buttons and form controls; `prefers-reduced-motion` turns off transitions and the card lift.
- Icons are `aria-hidden`; every link has a text label.

## Performance

Lighthouse (mobile emulation) after the pass:

| Page | Performance | Accessibility | Best Practices | SEO | LCP | CLS | Transfer |
|---|---|---|---|---|---|---|---|
| Home | 100 | 100 | 100 | 100 | 1.5 s | 0 | 105 KB |
| Capabilities | 100 | 100 | 100 | 100 | 1.5 s | 0 | 106 KB |
| Certificates | 100 | 100 | 100 | 100 | 1.6 s | 0 | 125 KB |
| Shop Tour | 100 | 100 | 100 | 100 | 1.9 s | 0 | 224 KB |
| Contact | 100 | 100 | 100 | 100 | 1.5 s | 0 | 98 KB |
| Home (ES) | 100 | 100 | 100 | 100 | 1.5 s | 0 | 106 KB |

Shop Tour loads its first two images eagerly; the rest load as the visitor scrolls.

- No frameworks, fonts or third-party scripts.
- One CSS file and one deferred JS file, both cache-busted by content hash.
- Icons are an inline sprite, so there are no extra requests for them.

## Security / technical quality

- New headers in `.htaccess`:
  - a **Content-Security-Policy**: only this site's own scripts and styles, the one inline script pinned by hash, forms may only send to `mailto:`, no framing by other sites, no plugins;
  - **Permissions-Policy**.

  HSTS is included but commented out until HTTPS is confirmed on both hosts.
- All `style=""` attributes were removed, so the policy does not have to allow inline styles.
- `tools/build.py` refuses to build if the inline script and its CSP hash drift apart.
- The QA server sends the production CSP; the site produces **no console errors** under it.
- External links that open new tabs use `rel="noopener"`, and the form builds its text with `textContent` (no HTML injection).

## Tooling added

| Tool | What it does |
|---|---|
| `tools/documents.py` | The verbatim certificate data, separated so page rewrites cannot touch it. |
| `tools/snapshot.py` | Save and diff the visible text blocks of the built site (baseline: `legacy/pre-optimization-snapshot.json`). |
| `tools/qa/qa.js` | The final QA crawl (see below). |
| `tools/audit.py` | Now counts only real content pages (not the redirect stub or the 404 page) toward preservation, and verifies that the facts in rewritten metadata are visible. |

`tools/qa/qa.js` checks:

- links, assets and anchors;
- canonical URLs, hreflang reciprocity, JSON-LD, sitemap and robots;
- titles, descriptions and headings;
- console errors under the production CSP;
- the 404 page and the legacy `/index.htm`;
- banned marketing phrases and placeholder text;
- English/Spanish parity of sections, calls to action and key facts;
- the mobile menu, keyboard use of the lightbox, and form validation in both languages;
- horizontal overflow on 13 pages at 9 widths;
- axe-core.

## Final QA results

| Check | Result |
|---|---|
| `python3 tools/audit.py` | **PASS**: 73/73 inventory items, 71/71 original URLs, 0 broken links, 0 missing original fragments |
| `node tools/qa/qa.js` | **PASS**: all sections above |

## Competitive-quality review

Compared with the conventions of serious avionics repair station, MRO and aerospace component shop websites (none copied):

| Area | Before | After |
|---|---|---|
| What they do | A welcome paragraph | Explicit headline, ratings on the first screen, a category grid |
| Proof | Documents on a sub-page | Certificate number, ratings and dated approvals on the first screen, each linked to its document |
| Next step | Phone number in the text | A consistent quote CTA on every page, and a structured quote form with the fields a repair station needs |
| Findability | Five nav links | Deep links from summaries to evidence, anchors, breadcrumbs |
| Remaining gaps | — | These need owner input: a downloadable capabilities list (R6), current certificate copies (R10), operating hours (B6), and a real form backend with a privacy policy (F1, F4). With those, the site would match the strongest sites in this niche. |

## Intentionally left unchanged

- Every original sentence (preserved verbatim; see the audit), including customer-satisfaction wording that is weak as marketing (§6: not used in "Why", but kept in Welcome and in the letter).
- The certificate transcriptions and details.
- The page URLs and file names of all original assets.
- The meta keywords (search engines ignore them; kept verbatim for preservation).
- The MapQuest links (kept and flagged; they could not be tested).
- The Spanish translation approach (flagged for native review).
