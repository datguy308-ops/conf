# Confidence Aviation website

Rebuild of https://www.confidenceaviation.com/ — modern design, English + Spanish,
with **every piece of the original site's content preserved** (verified by `tools/audit.py`).

* **`public/`** – the finished static website. To go live, upload its contents (including the
  hidden `.htaccess` file) to the web root of the existing host.
* `docs/owner-verification-required.md` – **facts the company must confirm before launch**.
* `docs/optimization-pass.md` – what the optimization pass changed and why, with QA results.
* `docs/content-preservation-audit.md` – page-by-page proof that no original information was lost.
* `docs/content-inventory.md` – generated checklist of every original content item and its new location.
* `docs/report.md` – report from the original rebuild (URL migration, first-pass decisions).
* `legacy/original-site/` – verbatim snapshot of the original website (source of truth, not deployed).

## Previewing

Pushes to this branch deploy `public/` to GitHub Pages (see `.github/workflows/pages.yml`).
The preview is marked `noindex` so it never competes with the real domain in search results.

Locally: `cd public && python3 -m http.server 8000`, then open http://localhost:8000/.

## Rebuilding

```sh
pip install pillow
python3 tools/images.py   # optimised images from legacy/original-site/
python3 tools/build.py    # pages, sitemap, robots.txt, .htaccess -> public/
python3 tools/audit.py    # content-preservation + link audit (must print PASS)
python3 tools/snapshot.py diff legacy/pre-optimization-snapshot.json   # text changed since the optimization baseline
cd tools/qa && npm install && node qa.js   # browser QA: links, SEO, parity, keyboard, overflow, axe (must print PASS)
```

Page content lives in `tools/build.py` (English and Spanish side by side via `t(en, es)`); certificate
data in `tools/documents.py` (verbatim — do not edit without the source image); styles in
`src/assets/css/site.css`; scripts in `src/assets/js/site.js`; server headers in `src/htaccess`.
