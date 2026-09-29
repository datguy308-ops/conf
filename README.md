# Confidence Aviation website

Rebuild of https://www.confidenceaviation.com/ — modern design, English + Spanish,
with **every piece of the original site's content preserved** (verified by `tools/audit.py`).

* **`public/`** – the finished static website. To go live, upload its contents (including the
  hidden `.htaccess` file) to the web root of the existing host.
* `docs/report.md` – final report: pages, URL migration, content mapping, SEO, performance,
  accessibility, and **items the owner should verify**.
* `docs/content-inventory.md` – checklist of every piece of original content and where it now lives.
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
```

Page content lives in `tools/build.py`; styles in `src/assets/css/site.css`; scripts in `src/assets/js/site.js`.
