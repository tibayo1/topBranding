#!/usr/bin/env python3
"""Build the draft color shortlist and four-page review from frozen Review 10 art.

Run after build_artwork.py, the browser comparison export and applications/build.py.
The cover HTML embeds the exact SVG artwork and licensed original font. The PDF
embeds the comparison/application PNGs at their original resolution and aspect.
This is a color exploration, not approved identity guidelines or print artwork.
"""
from __future__ import annotations

import base64
from html import escape
import json
from pathlib import Path

import fitz
from PIL import Image
from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "exports"
DRAFT = "DRAFT — NOT FOR PUBLICATION"
FONT = ROOT.parent / "identity-development-09/type-study/fonts/instrumentsans/InstrumentSans[wdth,wght].ttf"


def data_uri(path: Path) -> str:
    mime = "image/svg+xml" if path.suffix == ".svg" else "image/png"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def cover_source(palettes: dict, artwork: dict) -> str:
    by_id = {row["id"]: row for row in palettes["palettes"]}
    entries = {(row["paletteId"], row["directionId"], row["mode"]): row for row in artwork["entries"]}
    concepts = [("shared-rhythm", "Shared Rhythm"), ("open-praise", "Open Praise")]
    descriptions = {
        "teal": ("Contemporary warmth", "A distinctive teal foundation, softened by sand. The most balanced next step for a modern, welcoming parish identity."),
        "navy": ("Quiet dignity", "An elegant, dependable foundation with familiar church and luxury associations. The symbol carries more of the distinctiveness."),
    }
    cards = []
    for number, palette_id in enumerate(("teal", "navy"), 1):
        palette = by_id[palette_id]
        theme, note = descriptions[palette_id]
        concepts_html = []
        for direction_id, name in concepts:
            fields = []
            for mode in ("light", "dark"):
                entry = entries[(palette_id, direction_id, mode)]
                background = entry["colors"]["background"]
                fields.append(
                    f'<div class="logo-field" style="background:{background}">'
                    f'<img src="{data_uri(ROOT / entry["horizontal"])}" alt="{name}, {palette["name"]}, {mode} background">'
                    '</div>'
                )
            concepts_html.append(f'<section class="concept"><h3>{escape(name)}</h3><div class="light-dark">' + ''.join(fields) + '</div></section>')
        swatches = []
        for role in ("primary", "secondary", "accent", "neutral"):
            value = palette[role]
            swatches.append(f'<div class="swatch"><span class="chip" style="background:{value}"></span><b>{role.title()}</b><code>{value}</code></div>')
        ivory_examples = []
        for direction_id, name in concepts:
            entry = entries[(palette_id, direction_id, "dark")]
            ivory_examples.append(f'<span class="ivory-example"><img src="{data_uri(ROOT / entry["compact"])}" alt="{name}, ivory compact symbol on dark"><span>{escape(name)}</span></span>')
        cards.append(
            f'<article class="palette"><div class="palette-heading"><span class="ordinal">0{number}</span>'
            f'<div><h2>{escape(palette["name"])}</h2><p>{escape(theme)}</p></div></div>'
            + ''.join(concepts_html)
            + '<div class="swatches">' + ''.join(swatches) + '</div>'
            + f'<p class="tradeoff">{escape(note)}</p>'
            + f'<div class="ivory-strip" style="background:{palette["primary"]};color:{palette["neutral"]}"><span>Ivory tiny-use alternative</span>' + ''.join(ivory_examples) + '</div></article>'
        )
    font = base64.b64encode(FONT.read_bytes()).decode()
    license_text = FONT.with_name("OFL.txt").read_bytes().decode("utf-8")
    assert "</script" not in license_text.lower()
    font_license = (f'<script type="text/plain" id="embedded-font-license" data-font="Instrument Sans" '
                    f'data-source-font="{escape(FONT.name, quote=True)}">' + license_text + '</script>')
    css = '''
@font-face{font-family:Review;src:url(data:font/ttf;base64,FONTDATA);font-weight:100 900;font-stretch:75% 100%;font-display:block}
*{box-sizing:border-box}html,body{padding:0;margin:0;background:#e8e8e8;color:#20252a;font-family:Review,Arial,sans-serif;font-weight:450}h1,h2,h3,p{margin:0}.sheet{position:relative;width:1122px;height:794px;padding:31px 42px 48px;background:#fbfaf7;overflow:hidden}.eyebrow{display:flex;justify-content:space-between;font-size:10px;letter-spacing:1.1px;font-weight:600;color:#555b5d}h1{font-size:35px;line-height:1.08;letter-spacing:-.7px;font-weight:550;margin-top:18px}.subtitle{font-size:13px;line-height:1.4;color:#5a6060;margin-top:9px}.palette-grid{display:grid;grid-template-columns:1fr 1fr;gap:30px;margin-top:25px}.palette{border-top:1px solid #b7bbba;padding-top:15px}.palette-heading{display:flex;gap:14px;align-items:baseline;height:60px}.ordinal{font-size:12px;letter-spacing:.8px;color:#686f70}h2{font-size:25px;line-height:1.05;font-weight:550;letter-spacing:-.35px}.palette-heading p{font-size:11px;color:#636968;margin-top:6px}.concept{margin-top:9px}h3{font-size:12px;line-height:1.4;font-weight:600;margin-bottom:7px}.light-dark{display:grid;grid-template-columns:1fr 1fr;gap:8px}.logo-field{height:116px;display:flex;align-items:center;justify-content:center}.logo-field img{width:96%;height:99px;object-fit:contain;display:block}.swatches{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:20px}.chip{display:block;height:23px;width:100%;border:1px solid rgba(0,0,0,.1)}.swatch b{font-size:9px;line-height:1.4;display:block;font-weight:500;color:#606866;margin-top:5px}.swatch code{display:block;font-family:Review,Arial,sans-serif;font-size:12px;font-weight:550;letter-spacing:.3px;margin-top:1px}.tradeoff{font-size:11px;line-height:1.5;color:#535c5b;margin-top:16px;max-width:470px}.ivory-strip{margin-top:12px;height:38px;display:flex;align-items:center;justify-content:space-between;gap:10px;padding:0 12px;font-size:9px}.ivory-example{display:flex;align-items:center;gap:7px}.ivory-example img{display:block;width:20px;height:20px}.system-note{position:absolute;left:42px;right:42px;bottom:63px;font-size:10px;line-height:1.4;color:#646b69;max-width:950px}footer{position:absolute;left:42px;right:42px;bottom:20px;border-top:1px solid #c0c4c0;padding-top:10px;display:flex;justify-content:space-between;gap:20px;font-size:9px;line-height:1.4;color:#5c6461}footer strong{font-weight:650;color:#222a28;letter-spacing:.35px}footer span:last-child{white-space:nowrap}@page{size:297mm 210mm;margin:0}@media print{html,body{background:#fbfaf7;print-color-adjust:exact;-webkit-print-color-adjust:exact}.sheet{width:297mm;height:210mm}}
'''.replace("FONTDATA", font)
    return ('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>Tabernacle of Praise · Color 10 shortlist · DRAFT</title>' + font_license + '<style>' + css + '</style><body>'
            '<section class="sheet" id="shortlist"><header><div class="eyebrow"><span>RCCG TABERNACLE OF PRAISE · ISTANBUL</span><span>COLOR DEVELOPMENT 10</span></div>'
            '<h1>Color for both directions</h1><p class="subtitle">Two recommended starting points · Shared Rhythm and Open Praise · all five families compared on the next page</p></header>'
            '<main class="palette-grid">' + ''.join(cards) + '</main>'
            '<p class="system-note">Light: primary symbol and name on neutral. Dark: flat gold symbol and ivory name on primary. Tiny dark versions use ivory; gold remains a larger-size accent.</p>'
            '<footer><strong>' + DRAFT + '</strong><span>Current Review 09 shapes and working lettering. No logo, palette or type system is approved.</span><span>1 / 4</span></footer></section></body></html>')


def image_page(document: fitz.Document, path: Path, number: int) -> dict:
    """Embed the original PNG stream; fit the page to its native aspect ratio."""
    with Image.open(path) as image:
        width, height = image.size
    page_width = 841.89 if width >= height else 595.276
    artwork_height = page_width * height / width
    page = document.new_page(width=page_width, height=artwork_height + 18)
    page.insert_image(fitz.Rect(0, 0, page_width, artwork_height), stream=path.read_bytes())
    page.insert_text((14, artwork_height + 12), "DRAFT - NOT FOR PUBLICATION", fontsize=6.5, color=(.25, .27, .27))
    page.insert_text((page_width - 29, artwork_height + 12), f"{number} / 4", fontsize=6.5, color=(.25, .27, .27))
    return {"page": number, "source": str(path.relative_to(ROOT)), "sourcePixels": [width, height], "pagePoints": [round(page_width, 2), round(artwork_height + 18, 2)], "originalImageEmbedded": True}


def main() -> None:
    palettes = json.loads((ROOT / "source/palettes.json").read_text())
    artwork = json.loads((OUT / "artwork.json").read_text())
    required = [OUT / "palette-comparison.png", ROOT / "applications/applications-teal.png", ROOT / "applications/applications-navy.png"]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    if missing:
        raise SystemExit("Build and freeze comparison/applications first: " + ", ".join(missing))
    source = cover_source(palettes, artwork)
    (OUT / "color-shortlist-source.html").write_text(source, encoding="utf-8")
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path="/usr/bin/chromium", args=["--no-sandbox", "--disable-dev-shm-usage"])
        page = browser.new_page(viewport={"width": 1200, "height": 1000}, device_scale_factor=2)
        page.set_content(source, wait_until="load")
        page.evaluate("document.fonts.ready")
        layout = page.evaluate('''()=>{const s=document.querySelector('.sheet'),b=s.getBoundingClientRect();return {brokenImages:[...document.images].filter(x=>!x.complete||!x.naturalWidth).length,mainBottom:s.querySelector('main').getBoundingClientRect().bottom-b.top,noteTop:s.querySelector('.system-note').getBoundingClientRect().top-b.top,footerTop:s.querySelector('footer').getBoundingClientRect().top-b.top}}''')
        assert layout["brokenImages"] == 0, layout
        assert layout["mainBottom"] < layout["noteTop"] - 4, layout
        page.locator("#shortlist").screenshot(path=str(OUT / "color-shortlist.png"), animations="disabled")
        cover_pdf = page.pdf(prefer_css_page_size=True, print_background=True, display_header_footer=False)
        browser.close()
    document = fitz.open(stream=cover_pdf, filetype="pdf")
    assert len(document) == 1, f"Expected one cover page; got {len(document)}"
    pages = [image_page(document, image, index) for index, image in enumerate(required, 2)]
    document.set_metadata({"title": "Tabernacle of Praise — Color Development 10 — DRAFT", "subject": "Five provisional palettes across Shared Rhythm and Open Praise; no approval or publication", "author": "Tabernacle of Praise — internal identity exploration"})
    document.save(OUT / "color-review-10.pdf", garbage=4, deflate=True)
    assert len(document) == 4
    document.close()
    print(json.dumps({"status": DRAFT, "pdfPages": 4, "coverLayout": layout, "imagePages": pages}, indent=2))


if __name__ == "__main__":
    main()
