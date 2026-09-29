#!/usr/bin/env python3
"""Snapshot / compare the visible text blocks of the built site.

  python3 tools/snapshot.py save  legacy/pre-optimization-snapshot.json
  python3 tools/snapshot.py diff  legacy/pre-optimization-snapshot.json

A "block" is the normalised text of one block-level element (p, li, h1-h4, dt, dd,
figcaption, th, td, summary, label, caption, address) plus every img alt text.
`diff` lists, per page, every block that existed in the snapshot but no longer
appears verbatim anywhere on the same-language site, so each can be checked
and documented.
"""
import html
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUB = ROOT / "public"
BLOCK = {"p", "li", "h1", "h2", "h3", "h4", "dt", "dd", "figcaption", "th", "td", "summary", "label",
         "caption", "address", "button", "legend", "option"}


class Blocks(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.blocks, self.skip = [], [], 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "style", "svg"):
            self.skip += 1
        if tag in BLOCK:
            self.stack.append([])
        if tag == "img" and a.get("alt"):
            self.blocks.append("[img] " + a["alt"])
        if tag == "br" and self.stack:
            self.stack[-1].append(" ")

    def handle_endtag(self, tag):
        if tag in ("script", "style", "svg"):
            self.skip -= 1
        if tag in BLOCK and self.stack:
            t = norm("".join(self.stack.pop()))
            if t:
                self.blocks.append(t)
                if self.stack:
                    self.stack[-1].append(" " + t + " ")

    def handle_data(self, d):
        if not self.skip and self.stack:
            self.stack[-1].append(d)


def norm(s):
    return re.sub(r"\s+", " ", html.unescape(s).replace(" ", " ")).strip()


def collect():
    out = {}
    for p in sorted(PUB.rglob("*.htm*")):
        rel = str(p.relative_to(PUB))
        if rel == "index.htm":
            continue
        b = Blocks()
        b.feed(p.read_text(encoding="utf-8"))
        out[rel] = list(dict.fromkeys(b.blocks))
    return out


def main():
    cmd, path = sys.argv[1], ROOT / sys.argv[2]
    if cmd == "save":
        path.write_text(json.dumps(collect(), indent=1, ensure_ascii=False), encoding="utf-8")
        print("saved", path)
        return
    old, new = json.loads(path.read_text(encoding="utf-8")), collect()
    corpus = {"en": "", "es": ""}
    for rel, blocks in new.items():
        corpus["es" if rel.startswith("es/") else "en"] += "\n".join(blocks).lower() + "\n"
        # attribute text (e.g. captions in data-caption, meta) also counts
        corpus["es" if rel.startswith("es/") else "en"] += html.unescape((PUB / rel).read_text(encoding="utf-8")).lower()
    for rel, blocks in old.items():
        lang = "es" if rel.startswith("es/") else "en"
        gone = [b for b in blocks if b.lower().removeprefix("[img] ") not in corpus[lang]]
        if gone:
            print(f"\n## {rel} — {len(gone)} block(s) no longer present verbatim")
            for g in gone:
                print(f"- {g}")


if __name__ == "__main__":
    main()
