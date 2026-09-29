#!/usr/bin/env python3
"""Build optimised, responsive copies of the original website's images.

Reads the untouched originals from legacy/original-site/ and writes:
  * public/<original filename>        – byte-identical copy (keeps every old image URL alive)
  * public/assets/img/<slug>-<w>.webp  – WebP at the original width and a small thumbnail
  * public/assets/img/<slug>-<w>.jpg|png – fallback for browsers without WebP
  * public/assets/img/logo-*, banner-*  – current brand logo and banner (src/brand/)
  * public/favicon.*, icon-*.png, apple-touch-icon.png – icons from the logo's globe mark

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


def build_brand():
    """Current brand assets supplied by the owner (src/brand/): transparent logo for the
    header, globe mark for icons, sky banner for the home page hero and social sharing.
    The original 2003 logo remains available at its original tile URLs (ca_01-ca_04.gif)."""
    brand = ROOT / "src" / "brand"
    logo = Image.open(brand / "logo.png").convert("RGBA")
    visible = logo.getchannel("A").point(lambda a: 255 if a > 40 else 0)
    l, t, r, b = visible.getbbox()                          # trim the (near-)transparent margin
    logo = logo.crop((max(l - 4, 0), max(t - 4, 0), r + 4, b + 4))
    for w in (400, 800):
        im = logo.resize((w, round(logo.height * w / logo.width)), Image.LANCZOS)
        im.save(OUT / f"logo-{w}.png", "PNG", optimize=True)
        im.save(OUT / f"logo-{w}.webp", "WEBP", quality=90, method=6)
    print("logo size at 400w:", round(logo.height * 400 / logo.width))

    src = Image.open(brand / "logo.png").convert("RGBA")
    globe = src.crop((27, 83, 145, 201))                  # the globe mark only
    for size, name in ((32, "favicon.png"), (192, "icon-192.png"), (512, "icon-512.png")):
        globe.resize((size, size), Image.LANCZOS).save(PUB / name)
    globe.resize((48, 48), Image.LANCZOS).save(PUB / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    touch = Image.new("RGBA", (180, 180), (255, 255, 255, 255))   # iOS needs an opaque icon
    touch.alpha_composite(globe.resize((150, 150), Image.LANCZOS), (15, 15))
    touch.convert("RGB").save(PUB / "apple-touch-icon.png")

    banner = Image.open(brand / "banner.webp").convert("RGB")
    for w in (800, 1200, 2000):
        im = banner.resize((w, round(banner.height * w / banner.width)), Image.LANCZOS)
        im.save(OUT / f"banner-{w}.webp", "WEBP", quality=80, method=6)
        im.save(OUT / f"banner-{w}.jpg", "JPEG", quality=82, optimize=True, progressive=True)


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
    build_brand()
    (ROOT / "src" / "images.json").write_text(json.dumps(manifest, indent=1))
    print(f"{len(manifest)} images processed")


if __name__ == "__main__":
    main()
