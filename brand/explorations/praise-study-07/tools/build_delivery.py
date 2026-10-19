#!/usr/bin/env python3
"""Fit the existing, unchanged comparison PNG onto one printable A4 page.

Run from any directory. This packages the artwork; it never edits the image.
"""
from pathlib import Path
import base64
import hashlib
import struct

import fitz
from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "exports/praise-comparison.png"
OUTPUT = ROOT / "exports/praise-comparison.pdf"


def main():
    raw = SOURCE.read_bytes()
    if raw[:8] != b"\x89PNG\r\n\x1a\n" or raw[12:16] != b"IHDR":
        raise ValueError("Expected the existing comparison board as a PNG.")
    width, height = struct.unpack(">II", raw[16:24])
    if min(width, height) < 500:
        raise ValueError("The comparison board is too small for print review.")
    landscape = width >= height
    page_width, page_height = (297, 210) if landscape else (210, 297)
    orientation = "landscape" if landscape else "portrait"
    data = base64.b64encode(raw).decode("ascii")
    html = f'''<!doctype html>
<html lang="en"><meta charset="utf-8">
<title>Tabernacle of Praise — praise sketch comparison</title>
<style>
@page {{ size: A4 {orientation}; margin: 0; }}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; background: white; color: #111; }}
body {{ font: 10px Arial, sans-serif; }}
section {{ width: {page_width}mm; height: {page_height}mm; padding: 10mm;
  display: flex; flex-direction: column; }}
header {{ height: 8mm; flex-shrink: 0; }}
.art {{ flex: 1; min-height: 0; width: 100%; }}
img {{ display: block; width: 100%; height: 100%; object-fit: contain; }}
footer {{ height: 12mm; flex-shrink: 0; display: flex; flex-direction: column;
  justify-content: flex-end; gap: 1.2mm; font-size: 9px; }}
</style>
<section>
<header>Tabernacle of Praise / Praise integration study 07</header>
<div class="art"><img src="data:image/png;base64,{data}"
  alt="Before and after sketch comparison testing integrated praise symbolism"></div>
<footer><strong>DRAFT — NOT FOR PUBLICATION</strong>
<span>Exploratory comparison; no logo or typography approved.</span></footer>
</section></html>'''
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path="/usr/bin/chromium",
            args=["--no-sandbox", "--disable-dev-shm-usage"],
        )
        page = browser.new_page()
        page.set_content(html, wait_until="load")
        image = page.locator("img").evaluate("""e => ({
            loaded: e.complete,
            width: e.naturalWidth,
            height: e.naturalHeight,
            boxWidth: e.getBoundingClientRect().width,
            boxHeight: e.getBoundingClientRect().height
        })""")
        assert image["loaded"] and (image["width"], image["height"]) == (width, height)
        assert image["boxWidth"] > 500 and image["boxHeight"] > 500
        page.pdf(path=str(OUTPUT), print_background=True, prefer_css_page_size=True)
        browser.close()
    with fitz.open(OUTPUT) as doc:
        assert len(doc) == 1, f"Expected one page, received {len(doc)}."
        pdf_page = doc[0]
        images = pdf_page.get_images(full=True)
        assert any(item[2:4] == (width, height) for item in images), "Source image missing."
        covered = max(
            rect.width * rect.height / (pdf_page.rect.width * pdf_page.rect.height)
            for item in images for rect in pdf_page.get_image_rects(item[0])
        )
        assert covered > 0.45, "Artwork occupies too little of the review page."
        text = pdf_page.get_text()
        assert "DRAFT" in text and "no logo or typography approved" in text
    assert SOURCE.read_bytes() == raw, "The source PNG must remain unchanged."
    print(f"Created {OUTPUT.relative_to(ROOT)}: one A4 {orientation} page; "
          f"unchanged {width} × {height} artwork; {covered:.0%} page coverage.")
    print(f"Source SHA-256: {hashlib.sha256(raw).hexdigest()}")


if __name__ == "__main__":
    main()
