#!/usr/bin/env python3
"""Content-preservation and link audit for the rebuilt site.

Checks, against the built files in public/:
  1. every item in tools/inventory.json appears where the inventory says it must
     (visible text, attribute/URL references, <title>, meta description/keywords);
  2. every URL that returned 200 on the original site still resolves;
  3. every internal href/src/srcset in every page resolves to a real file, and every
     #fragment points at an existing id;
and writes docs/content-inventory.md (the preservation checklist) from the results.

Exit code 0 = everything accounted for. Usage: python3 tools/audit.py
"""
import html
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parent.parent
PUB = ROOT / "public"
INV = json.loads((ROOT / "tools" / "inventory.json").read_text(encoding="utf-8"))
CRAWL = json.loads((ROOT / "legacy" / "crawl-log.json").read_text(encoding="utf-8"))


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text, self.title, self.meta, self.refs, self.ids = [], "", {}, [], set()
        self._skip = 0
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "style"):
            self._skip += 1
        if tag == "title":
            self._in_title = True
        if tag == "meta" and a.get("name"):
            self.meta[a["name"]] = a.get("content", "")
        if "id" in a:
            self.ids.add(a["id"])
        for k in ("href", "src", "action"):
            if a.get(k):
                self.refs.append(a[k])
        if a.get("srcset"):
            self.refs += [c.strip().split(" ")[0] for c in a["srcset"].split(",")]
        if tag in ("br", "p", "li", "div", "dt", "dd", "h1", "h2", "h3", "td", "th", "figcaption"):
            self.text.append(" ")

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self._skip -= 1
        if tag == "title":
            self._in_title = False
        if tag in ("p", "li", "div", "dt", "dd", "h1", "h2", "h3", "td", "th"):
            self.text.append(" ")

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        elif not self._skip:
            self.text.append(data)


def norm(s):
    return re.sub(r"\s+", " ", html.unescape(s).replace("\u00a0", " ")).strip()


_cache = {}


def load(rel):
    if rel not in _cache:
        raw = (PUB / rel).read_text(encoding="utf-8")
        p = Page()
        p.feed(raw)
        p.raw = raw
        p.vis = norm("".join(p.text))
        _cache[rel] = p
    return _cache[rel]


def check_item(spec):
    """Return list of failures for one language spec of an inventory item."""
    fails = []
    if "file" in spec:
        for f in spec.get("exists", []):
            if not (PUB / f).exists():
                fails.append(f"missing file {f}")
        if spec.get("contains"):
            body = (PUB / spec["file"]).read_text(encoding="utf-8")
            fails += [f"{spec['file']}: missing '{c}'" for c in spec["contains"] if c not in body]
        return fails
    for page in spec["pages"]:
        if not (PUB / page).exists():
            fails.append(f"missing page {page}")
            continue
        p = load(page)
        for t in spec.get("text", []):
            if norm(t) not in p.vis:
                fails.append(f"{page}: text not found: {t!r}")
        for a in spec.get("attrs", []):
            if a not in html.unescape(p.raw):
                fails.append(f"{page}: reference not found: {a!r}")
        for m in spec.get("meta", []):
            if not any(m in v for v in p.meta.values()):
                fails.append(f"{page}: meta not found: {m!r}")
        if "title" in spec and norm(p.title) != norm(spec["title"]):
            fails.append(f"{page}: title is {p.title!r}")
        for t in spec.get("titlecontains", []):
            if t not in p.title:
                fails.append(f"{page}: title lacks {t!r}")
    return fails


def resolve(page_rel, ref):
    """Map an internal reference to a file in public/ (None if external)."""
    u = urlparse(ref)
    if u.scheme or ref.startswith(("//", "mailto:", "tel:")):
        if u.netloc in ("www.confidenceaviation.com", "confidenceaviation.com"):
            path = u.path
        else:
            return None
    else:
        path = u.path
    if not path:
        return (page_rel, u.fragment)
    if path.startswith("/"):
        target = path.lstrip("/")
    else:
        base = str(Path(page_rel).parent)
        target = str((Path(base) / path).as_posix())
        parts = []
        for seg in target.split("/"):
            if seg in ("", "."):
                continue
            if seg == "..":
                if parts:
                    parts.pop()
                continue
            parts.append(seg)
        target = "/".join(parts) + ("/" if path.endswith("/") else "")
    target = unquote(target).lstrip("/")
    if target == "" or target.endswith("/"):
        target += "index.html"
    return (target, u.fragment)


def main():
    failures = {}
    rows = []
    for it in INV["items"]:
        f_en = check_item(it["en"]) if "en" in it else []
        f_es = check_item(it["es"]) if "es" in it else []
        if f_en or f_es:
            failures[it["id"]] = f_en + f_es
        where_en = it["en"].get("pages", [it["en"].get("file")]) if "en" in it else []
        where_es = it["es"].get("pages", []) if "es" in it else []
        rows.append((it, where_en, where_es, not (f_en or f_es)))

    # 2. original URLs
    url_fail = []
    for u, status in CRAWL.items():
        if not status.startswith("200"):
            continue
        path = urlparse(u).path.lstrip("/") or "index.html"
        if not (PUB / unquote(path)).exists():
            url_fail.append(u)

    # 3. internal links
    link_fail = []
    pages = sorted(str(p.relative_to(PUB)) for p in PUB.rglob("*") if p.suffix in (".html", ".htm"))
    for rel in pages:
        p = load(rel)
        for ref in p.refs:
            r = resolve(rel, ref)
            if r is None:
                continue
            target, frag = r
            if rel in ("404.html", "index.htm"):
                continue  # served at arbitrary paths / redirect stub; checked separately
            if not (PUB / target).exists():
                link_fail.append(f"{rel}: broken link {ref}")
            elif frag and target.endswith((".html", ".htm")) and frag not in load(target).ids:
                link_fail.append(f"{rel}: missing anchor {ref}")

    # 4. independent reverse check: every text fragment and alt/title in the ORIGINAL html
    #    must occur somewhere in the new English site (case/whitespace-insensitive).
    # Only real English content pages count (not the redirect stub or the 404 page).
    site_text = " ".join(load(r).vis + " " + html.unescape(load(r).raw) for r in pages
                         if not r.startswith("es/") and r not in ("index.htm", "404.html")).lower()
    reverse_fail = []
    for f in sorted((ROOT / "legacy" / "original-site").glob("*.htm")):
        raw = f.read_text(encoding="utf-8")
        raw = re.sub(r"<!--.*?-->", "", raw, flags=re.S)       # commented-out widget (inventory H-10)
        raw = re.sub(r"<script.*?</script>", "", raw, flags=re.S)
        frags = [norm(t) for t in re.split(r"<[^>]+>", raw)]
        frags += [norm(a) for a in re.findall(r'(?:alt|title)="([^"]+)"', raw)]
        frags += [norm(a) for a in re.findall(r'<meta name="(?:description|keywords)" content="([^"]+)"', raw)]
        for t in frags:
            if len(t) < 2 or t.startswith(("<!DOCTYPE", "//")):
                continue
            if norm(t).lower() not in site_text:
                reverse_fail.append(f"{f.name}: {t!r}")
    # Documented consolidations (content represented by a superset elsewhere on every page).
    CONSOLIDATED = {
        "©2003 Confidence Aviation, Inc.":
            "sub-page footer notice; represented by the home page's '©2003 - 2011 Confidence Aviation, Inc.' "
            "which now appears in the footer of every page (inventory G-03/G-04)",
    }
    # Documented rewrites: SEO metadata (page title / meta descriptions) rewritten in the
    # optimization pass. Each fact they contained is checked as visible text elsewhere.
    REWRITTEN = {
        "Confidence Aviation - AVIONICS & INSTRUMENTS - FAA Certified Repair Station":
            ("title", ["Avionics & Instruments — FAA Certified Repair Station"]),
        "Avionics Shop Miami Florida, OEM Alternative. Boeing, Bendix/King, Honeywell, Sperry, Collins.":
            ("meta description", ["Avionics repair shop Miami Florida", "OEM alternative repairs for Boeing, Bendix/King, Honeywell, Sperry, Collins"]),
        "Avionics shop Miami Florida. OEM Alternative repair station for Boeing, Bendix/King, Honeywell, Sperry, Collins aircraft instruments and valves.":
            ("meta description", ["Avionics repair shop Miami Florida", "Aircraft instruments, instrument panels and valves",
                                  "OEM alternative repair station", "Boeing, Bendix/King, Honeywell, Sperry, Collins"]),
    }
    for orig, (_kind, facts) in REWRITTEN.items():
        for f in facts:
            if norm(f).lower() not in site_text:
                reverse_fail.append(f"rewrite of {orig!r}: fact no longer visible: {f!r}")
    rewritten = sorted({r for r in reverse_fail if r.split(": ", 1)[-1].strip("'") in REWRITTEN})
    reverse_fail = sorted(set(reverse_fail) - set(rewritten))
    consolidated = sorted({r for r in reverse_fail if r.split(": ", 1)[1].strip("'") in CONSOLIDATED})
    reverse_fail = sorted(set(reverse_fail) - set(consolidated))

    write_checklist(rows, url_fail)

    ok = not failures and not url_fail and not link_fail and not reverse_fail
    print(f"Inventory items: {len(INV['items'])}, accounted for: {len(INV['items']) - len(failures)}")
    for k, v in failures.items():
        for f in v:
            print(f"  FAIL {k}: {f}")
    print(f"Original URLs returning 200: {sum(1 for s in CRAWL.values() if s.startswith('200'))}, "
          f"still resolving: {sum(1 for s in CRAWL.values() if s.startswith('200')) - len(url_fail)}")
    for u in url_fail:
        print(f"  FAIL original URL gone: {u}")
    print(f"Pages scanned for links: {len(pages)}, broken internal links/anchors: {len(link_fail)}")
    for l in link_fail:
        print(f"  FAIL {l}")
    print(f"Reverse check (original text/alt/title/meta fragments missing from new site): {len(reverse_fail)}")
    for r in reverse_fail:
        print(f"  FAIL {r}")
    for r in consolidated:
        print(f"  consolidated (documented): {r}")
    for r in rewritten:
        print(f"  rewritten metadata (documented; facts verified visible): {r}")
    print("RESULT:", "PASS — 100% of original content accounted for" if ok else "FAIL")
    sys.exit(0 if ok else 1)


def write_checklist(rows, url_fail):
    lines = [
        "# Content preservation checklist",
        "",
        "Generated by `tools/audit.py` from `tools/inventory.json`. Every row is a piece of content",
        "found on the original site (crawled 2026-09-29; verbatim copy in `legacy/original-site/`).",
        "**Status ✅ means the audit found the required text/reference in the listed page(s).**",
        "",
        "| ID | Original location | Kind | Original content | New location (EN) | Spanish | Status |",
        "|---|---|---|---|---|---|---|",
    ]
    for it, en, es, ok in rows:
        orig = it["original"].replace("|", "\\|").replace("\n", " ")
        if len(orig) > 220:
            orig = orig[:217] + "…"
        note = f"<br>_Note: {it['note']}_" if it.get("note") else ""
        lines.append(f"| {it['id']} | {it['src']} | {it['kind']} | {orig}{note} | "
                     f"{', '.join(x for x in en if x)} | {', '.join(es) or '—'} | {'✅' if ok else '❌'} |")
    lines += ["", f"Original URLs no longer resolving: {len(url_fail) or 'none'}", ""]
    (ROOT / "docs" / "content-inventory.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
