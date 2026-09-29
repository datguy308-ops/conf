# Original website snapshot

Verbatim copy of every file publicly reachable on https://www.confidenceaviation.com/
as crawled on 2026-09-29 (server `Last-Modified: Fri, 02 Sep 2022`).

* `original-site/` – the HTML pages, stylesheet and every image exactly as served.
  `/` and `/index.htm` returned byte-identical files, so only `index.htm` is stored.
* `crawl-log.json` – every URL requested during the crawl and its HTTP status.
  (`/sitemap.xml`, `/confidence.css` and the `*.src` rollover-script names returned 404
  on the original server and are excluded.)

This snapshot is the source of truth for `docs/content-inventory.md` and for
`tools/inventory.json`, which `tools/audit.py` checks the rebuilt site against.
It is **not** deployed.
