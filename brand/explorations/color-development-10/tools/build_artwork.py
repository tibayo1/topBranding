#!/usr/bin/env python3
"""Recolor frozen Review 09 paths for draft Review 10; no geometry or type edits.

Run from any directory. Generates editable explicit-background SVGs, their manifest,
and browser-native 16/20/24/32 px proofs. Requires Pillow and Playwright/Chromium.
"""
from __future__ import annotations

import base64
import copy
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent / "identity-development-09"
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)
DRAFT = "DRAFT — NOT FOR PUBLICATION"


def tag(element):
    return element.tag.split("}")[-1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def geometry(svg):
    """Only shape-bearing attributes; fills/metadata are the allowed differences."""
    rows = []
    for element in svg.iter():
        if tag(element) == "path":
            rows.append(["path", element.get("d"), element.get("transform"), element.get("fill-rule")])
        elif tag(element) == "g":
            rows.append(["g", element.get("transform")])
    return rows


def recolor(source, destination, ink, background, title, name_ink=None):
    tree = ET.parse(source)
    svg = tree.getroot()
    before = geometry(svg)
    for element in svg.iter():
        if tag(element) == "title":
            element.text = title + " — " + DRAFT
        elif tag(element) == "desc":
            element.text = (DRAFT + ". Frozen Review 09 contours and transforms. "
                            "Exploratory screen color only; no logo, palette or lettering approval.")
    groups = [child for child in svg if tag(child) == "g"]
    if name_ink is not None:
        assert len(groups) == 2, f"Expected separate symbol/name groups: {source}"
        for group, color in zip(groups, (ink, name_ink)):
            for element in group.iter():
                if tag(element) in {"g", "path"}:
                    element.set("fill", color)
    else:
        for element in svg.iter():
            if tag(element) in {"g", "path"}:
                element.set("fill", ink)
    x, y, width, height = svg.get("viewBox").split()
    rectangle = ET.Element(f"{{{NS}}}rect", {
        "x": x, "y": y, "width": width, "height": height,
        "fill": background, "data-role": "background",
    })
    svg.insert(0, rectangle)
    assert before == geometry(svg), f"Geometry changed: {source}"
    assert not any(tag(e) in {"text", "image", "filter", "mask"} for e in svg.iter())
    destination.parent.mkdir(parents=True, exist_ok=True)
    tree.write(destination, encoding="unicode")
    return len([e for e in svg.iter() if tag(e) == "path"])


def luminance(color):
    values = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    values = [c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4 for c in values]
    return .2126 * values[0] + .7152 * values[1] + .0722 * values[2]


def contrast(a, b):
    high, low = sorted((luminance(a), luminance(b)), reverse=True)
    return round((high + .05) / (low + .05), 3)


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def build():
    palette_source = ROOT / "source/palettes.json"
    palette_data = json.loads(palette_source.read_text())
    master_data = json.loads((SOURCE / "exports/development-artwork.json").read_text())
    palettes = copy.deepcopy(palette_data["palettes"])
    palettes.append({
        "id": "mono", "number": "00", "name": "Monochrome control",
        "family": "Black + White", "mood": "Shape before color",
        "primary": "#000000", "secondary": "#727272", "accent": "#FFFFFF", "neutral": "#FFFFFF",
        "names": {"primary": "Black", "secondary": "Gray", "accent": "White", "neutral": "White"},
        "note": "Control only. Revisit the underlying form without any palette association.",
    })
    manifest = {
        "status": DRAFT, "approval": False,
        "palettes": palettes,
        "directions": [{"id": d["id"], "name": d["name"], "inkBounds": d["inkBounds"]}
                       for d in master_data["directions"]],
        "comparison": master_data["comparison"],
        "geometry": "Every source path d, group transform, path transform and fill rule is unchanged from Review 09.",
        "compact": "16–20 px provisional cuts only. Dark compact art uses neutral ivory/white ink for every palette; larger dark symbols use the accent.",
        "contrastNote": "WCAG relative-luminance ratios describe these actual flat screen pairings. Logo marks are exempt from WCAG text contrast; ordinary body copy still needs an appropriate 4.5:1 pairing. Ratios do not prove symbol or letter recognition.",
        "sources": {}, "entries": [], "contrast": [],
    }
    inputs = {"palettes": palette_source, "review09Manifest": SOURCE / "exports/development-artwork.json"}
    for direction in master_data["directions"]:
        for role in ("primaryFile", "compactFile"):
            inputs[direction["id"] + ":" + role] = SOURCE / direction[role]
        for role in ("horizontal", "stacked"):
            inputs[direction["id"] + ":" + role] = SOURCE / direction["lockups"][role]
    for key, path in inputs.items():
        manifest["sources"][key] = {"path": str(path.relative_to(ROOT.parent.parent.parent)), "sha256": sha(path)}
    path_counts = []
    for palette in palettes:
        primary, accent, neutral = (palette[k] for k in ("primary", "accent", "neutral"))
        manifest["contrast"].append({
            "paletteId": palette["id"],
            "lightSymbolAndName": contrast(primary, neutral),
            "darkSymbolAccent": contrast(accent, primary),
            "darkNameAndCompactNeutral": contrast(neutral, primary),
            "primaryOnSecondarySurface": contrast(primary, palette["secondary"]),
            "secondaryOnNeutral": contrast(palette["secondary"], neutral),
            "accentOnNeutral": contrast(accent, neutral),
            "note": "Accent on light neutral is shown as a limitation, not an approved text pairing.",
        })
        for direction in master_data["directions"]:
            for mode in ("light", "dark"):
                background = neutral if mode == "light" else primary
                symbol_ink = primary if mode == "light" else accent
                name_ink = primary if mode == "light" else neutral
                compact_ink = primary if mode == "light" else neutral
                folder = Path("artwork") / palette["id"] / direction["id"] / mode
                entry = {
                    "paletteId": palette["id"], "directionId": direction["id"], "mode": mode,
                    "colors": {"background": background, "symbol": symbol_ink, "name": name_ink, "compact": compact_ink},
                    "compactInkRole": "primary" if mode == "light" else "neutral",
                }
                for kind in ("symbol", "compact", "horizontal", "stacked"):
                    destination = folder / (kind + ".svg")
                    source = (SOURCE / direction["primaryFile"] if kind == "symbol" else
                              SOURCE / direction["compactFile"] if kind == "compact" else
                              SOURCE / direction["lockups"][kind])
                    ink = compact_ink if kind == "compact" else symbol_ink
                    count = recolor(source, ROOT / destination, ink, background,
                                    f"{direction['name']} / {palette['name']} / {mode} / {kind}",
                                    name_ink if kind in {"horizontal", "stacked"} else None)
                    path_counts.append(count)
                    entry[kind] = str(destination)
                entry["symbolHighContrast"] = entry["symbol"]
                if mode == "dark":
                    destination = folder / "symbol-high-contrast.svg"
                    count = recolor(SOURCE / direction["primaryFile"], ROOT / destination, neutral, background,
                                    f"{direction['name']} / {palette['name']} / dark / neutral-ink primary")
                    path_counts.append(count)
                    entry["symbolHighContrast"] = str(destination)
                entry["highContrastSymbolInkRole"] = "primary" if mode == "light" else "neutral"
                manifest["entries"].append(entry)
    manifest["audit"] = {
        "svgCount": len(path_counts), "geometryComparisonsPassed": len(path_counts),
        "allBackgroundsExplicit": True, "liveText": 0, "rasters": 0, "masks": 0, "filters": 0,
        "sharedRhythmFaces": "One identical ink per four-face symbol; no color-coded bars.",
    }
    save_json(ROOT / "exports/artwork.json", manifest)
    return manifest


def native_proofs(manifest):
    """Render at actual browser pixel sizes, then label nearest-neighbor enlargements."""
    font_file = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    font = ImageFont.truetype(font_file, 18)
    small_font = ImageFont.truetype(font_file, 14)
    heading_font = ImageFont.truetype(font_file, 28)
    width, row_height, top = 1600, 170, 210
    board = Image.new("RGB", (width, top + row_height * 12 + 85), "#F7F7F5")
    draw = ImageDraw.Draw(board)
    draw.text((40, 28), "COLOR 10 / Native small-size proof", fill="#181B20", font=heading_font)
    draw.text((40, 76), DRAFT + " · Actual-size samples + 3× nearest-neighbor details", fill="#51555A", font=font)
    draw.text((40, 110), "32 / 24 px primary: accent on dark. 20 / 16 px compact: ivory on dark for every palette.", fill="#51555A", font=font)
    draw.text((40, 141), "Compact cuts remain provisional; visible gaps do not establish recognition of architecture, praise or the proposed T/P.", fill="#51555A", font=small_font)
    draw.text((340, 180), "SHARED RHYTHM", fill="#181B20", font=font)
    draw.text((960, 180), "OPEN PRAISE", fill="#181B20", font=font)
    raster_count = 0
    records = []
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path="/usr/bin/chromium", args=["--no-sandbox", "--disable-dev-shm-usage"])
        page = browser.new_page()
        page.set_content("<!doctype html><html><body></body></html>")
        for palette_index, palette in enumerate(manifest["palettes"]):
            for mode_index, mode in enumerate(("light", "dark")):
                y = top + (palette_index * 2 + mode_index) * row_height
                draw.text((40, y + 12), palette["name"], fill="#181B20", font=font)
                draw.text((40, y + 40), mode.upper(), fill="#51555A", font=small_font)
                pair = next(c for c in manifest["contrast"] if c["paletteId"] == palette["id"])
                ratio = pair["lightSymbolAndName"] if mode == "light" else pair["darkSymbolAccent"]
                draw.text((40, y + 67), f"Primary mark {ratio:.2f}:1", fill="#51555A", font=small_font)
                if mode == "dark":
                    draw.text((40, y + 92), f"Compact {pair['darkNameAndCompactNeutral']:.2f}:1", fill="#51555A", font=small_font)
                for direction_index, direction in enumerate(manifest["directions"]):
                    entry = next(e for e in manifest["entries"] if e["paletteId"] == palette["id"] and e["directionId"] == direction["id"] and e["mode"] == mode)
                    for size_index, (size, kind) in enumerate(((32, "symbol"), (24, "symbol"), (20, "compact"), (16, "compact"))):
                        x = 340 + direction_index * 620 + size_index * 130
                        svg = (ROOT / entry[kind]).read_bytes()
                        uri = "data:image/svg+xml;base64," + base64.b64encode(svg).decode()
                        png = page.evaluate("""async ({uri,size}) => {
                            const img = new Image(); img.src = uri; await img.decode();
                            const c = document.createElement('canvas'); c.width=size; c.height=size;
                            c.getContext('2d').drawImage(img,0,0,size,size);
                            return c.toDataURL('image/png').split(',')[1];
                        }""", {"uri": uri, "size": size})
                        out = Path("artwork/proofs") / palette["id"] / direction["id"] / f"{mode}-{kind}-{size}.png"
                        (ROOT / out).parent.mkdir(parents=True, exist_ok=True)
                        (ROOT / out).write_bytes(base64.b64decode(png))
                        image = Image.open(ROOT / out).convert("RGB")
                        board.paste(image, (x, y + 8))
                        board.paste(image.resize((size * 3, size * 3), Image.Resampling.NEAREST), (x, y + 50))
                        draw.text((x, y + 148), f"{size} / {'primary' if kind == 'symbol' else 'compact'}", fill="#51555A", font=small_font)
                        records.append({"paletteId": palette["id"], "directionId": direction["id"], "mode": mode, "size": size, "source": entry[kind], "png": str(out)})
                        raster_count += 1
        browser.close()
    draw.text((40, board.height - 52), "Screen rendering only. Inspect at 100% for native size; the enlarged pixels are a diagnostic, not the intended appearance.", fill="#51555A", font=font)
    board.save(ROOT / "artwork/native-small-size-proof.png")
    manifest["proofs"] = {"overview": "artwork/native-small-size-proof.png", "rasterCount": raster_count, "sizes": [32, 24, 20, 16], "entries": records}
    save_json(ROOT / "exports/artwork.json", manifest)


if __name__ == "__main__":
    result = build()
    native_proofs(result)
    print(f"Built {result['audit']['svgCount']} unchanged-geometry SVGs and {result['proofs']['rasterCount']} native PNGs.")
