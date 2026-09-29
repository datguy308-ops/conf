# Confidence Aviation website

Rebuild of https://www.confidenceaviation.com/ — **work in progress**.

* `public/` — the deployable static site (upload its contents, including `.htaccess`, to the web root).
* `legacy/original-site/` — verbatim snapshot of the original website (source of truth, not deployed).
* `tools/inventory.json` — every piece of original content and where it lives in the new site.
* `tools/images.py` → `tools/build.py` — regenerate images and pages (`pip install pillow`, Python 3.11+).

All original URLs (`about.htm`, `capabilities.htm`, `certificates.htm`, `shop.htm`,
`contact.htm`, every original image) are kept; `/index.htm` 301-redirects to `/`.
Spanish pages live under `/es/`.
