#!/usr/bin/env python3
"""Build optimised, responsive copies of the original website's images.

Reads the untouched originals from legacy/original-site/ and writes:
  * public/<original filename>        – byte-identical copy (keeps every old image URL alive)
  * public/assets/img/<slug>-<w>.webp  – WebP at the original width and a small thumbnail
  * public/assets/img/<slug>-<w>.jpg|png – fallback for browsers without WebP
  * public/assets/img/logo.png|webp    – the original logo, recomposed from the header tiles

Nothing is upscaled: the originals are small (<=600 px), so the largest output is the
original size. Requires Pillow (pip install pillow).
"""
import json
import re
import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "legacy" / "original-site"
PUB = ROOT / "public"
OUT = PUB / "assets" / "img"

# original filename -> clean slug used by the new site
IMAGES = {
    "air_agency_certificate.gif": "air-agency-certificate",
    "easa-cert.jpg": "easa-approval-certificate",
    "operations_specifications.gif": "operations-specifications",
    "alex&robert-trans.gif": "alex-and-robert",
    "hugointheshop.png": "hugo-in-the-shop",
    "robertoinshop.png": "roberto-in-shop",
    "reception.gif": "reception",
    "shop_entrance-1.jpg": "shop-entrance",
    "shop_dme-transponder_bench-.jpg": "shop-dme-transponder-bench",
    "shop_radar_bench-1.jpg": "shop-radar-bench-1",
    "shop_nav-comm_bench-1.jpg": "shop-nav-comm-bench",
    "shop_radar_bench-2.jpg": "shop-radar-bench-2",
    "shop_dme-transponder&altime.jpg": "shop-dme-altimeter-benches",
    "shop_radar&nav-comm_bench-1.jpg": "shop-radar-nav-comm-bench",
    "shop_altimeter_testset-1.jpg": "shop-altimeter-test-set",
    "shop_equip_hf_antenna_.jpg": "shop-hf-antenna",
    "shop_equip_radar_indicat1.jpg": "shop-radar-indicators",
    "shop_equip_radar_large-1.jpg": "shop-large-radar-system",
    "shop_equip_radio_altimeter2.jpg": "shop-radio-altimeters",
}
THUMB = 320


def has_alpha(im):
    return im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info)


def save_pair(im, slug, width, alpha, manifest):
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    base = OUT / f"{slug}-{im.width}"
    if alpha:
        im = im.convert("RGBA")
        im.save(f"{base}.webp", "WEBP", quality=82, method=6)
        im.save(f"{base}.png", "PNG", optimize=True)
        fallback = "png"
    else:
        im = im.convert("RGB")
        im.save(f"{base}.webp", "WEBP", quality=80, method=6)
        im.save(f"{base}.jpg", "JPEG", quality=82, optimize=True, progressive=True)
        fallback = "jpg"
    manifest.setdefault(slug, {"alpha": alpha, "sizes": []})["sizes"].append(
        {"w": im.width, "h": im.height, "fallback": fallback})


def build_logo():
    """Recompose the logo exactly as it appeared in the original page header."""
    html = (SRC / "index.htm").read_text(encoding="utf-8")
    tiles = re.findall(r'top:(\d+); left:(\d+); width:\d+; height:\d+;"><img name="picture\d*" '
                       r'width="\d+" height="\d+"\s*src="(ca_\d+\.gif)"', html)
    canvas = Image.new("RGB", (761, 190), "white")
    for top, left, name in tiles:
        if int(top) < 95:
            canvas.paste(Image.open(SRC / name).convert("RGB"), (int(left), int(top)))
    logo = canvas.crop((0, 0, 432, 56))
    logo.save(OUT / "logo.png", "PNG", optimize=True)
    logo.save(OUT / "logo.webp", "WEBP", quality=90, method=6)
    # the globe mark alone, used as favicon / touch icon
    mark = canvas.crop((8, 0, 64, 56))
    mark.save(PUB / "apple-touch-icon.png")
    mark.resize((32, 32), Image.LANCZOS).save(PUB / "favicon.png")
    mark.save(PUB / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    # 1. keep every original file (images + stylesheet) at its original URL
    for f in SRC.iterdir():
        if f.suffix.lower() in (".gif", ".jpg", ".png", ".css"):
            shutil.copy2(f, PUB / f.name)
    # 2. responsive, optimised versions
    manifest = {}
    for name, slug in IMAGES.items():
        im = Image.open(SRC / name)
        alpha = has_alpha(im)
        im.load()
        save_pair(im, slug, im.width, alpha, manifest)
        if im.width > THUMB * 1.3:
            save_pair(im, slug, THUMB, alpha, manifest)
        manifest[slug]["original"] = name
    build_logo()
    (ROOT / "src" / "images.json").write_text(json.dumps(manifest, indent=1))
    print(f"{len(manifest)} images processed")


if __name__ == "__main__":
    main()
