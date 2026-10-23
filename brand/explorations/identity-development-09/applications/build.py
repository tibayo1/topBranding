#!/usr/bin/env python3
"""Build equal-condition, monochrome application studies from Review 09 masters.

Run after ../exports/development-artwork.json has been built:
    python3 applications/build.py

For layout development only, --provisional reads the preserved Review 08 masters.
The manifest states which masters were used and records their exact hashes.
No symbol or outlined name geometry is redrawn by this application builder.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import io
import json
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from PIL import ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PREVIOUS = ROOT.parent / "team-pair-08"
SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)


def node(tag, attrs=None, parent=None, **extra):
    el = ET.Element(f"{{{SVG_NS}}}{tag}", {k: str(v) for k, v in (attrs or {}).items()})
    for k, v in extra.items():
        el.set(k.replace("_", "-"), str(v))
    if parent is not None:
        parent.append(el)
    return el


def rect(parent, x, y, w, h, fill, stroke=None, sw=1, rx=None):
    attrs = dict(x=x, y=y, width=w, height=h, fill=fill)
    if stroke:
        attrs.update(stroke=stroke, **{"stroke-width": sw})
    if rx is not None:
        attrs["rx"] = rx
    return node("rect", attrs, parent)


def line(parent, x1, y1, x2, y2, fill="#d4d4d4", sw=1):
    return node("path", {"d": f"M{x1} {y1}H{x2}" if y1 == y2 else f"M{x1} {y1}L{x2} {y2}",
                         "stroke": fill, "stroke-width": sw, "fill": "none"}, parent)


def canvas(w, h, title, desc, physical=False):
    svg = node("svg", {"viewBox": f"0 0 {w} {h}", "width": "210mm" if physical else w,
                       "height": "297mm" if physical else h, "role": "img"})
    node("title", parent=svg).text = title
    node("desc", parent=svg).text = desc
    return svg


def write_svg(path, svg):
    ET.indent(svg, space="  ")
    path.write_text('<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(svg, encoding="unicode") + "\n", encoding="utf-8")


class OutlinedLabels:
    """Application copy only. All actual identity lettering comes from masters."""
    def __init__(self):
        paths = [ROOT / "assets/fonts/instrumentsans/InstrumentSans[wdth,wght].ttf",
                 ROOT / "type-study/fonts/instrumentsans/InstrumentSans[wdth,wght].ttf",
                 PREVIOUS / "assets/fonts/instrumentsans/InstrumentSans[wdth,wght].ttf"]
        self.path = next(p for p in paths if p.is_file())
        font = TTFont(self.path)
        self.font = instantiateVariableFont(font, {"wght": 450, "wdth": 100}, inplace=False)
        self.cmap = self.font.getBestCmap()
        self.glyphs = self.font.getGlyphSet()
        self.units = self.font["head"].unitsPerEm
        font_bytes = io.BytesIO()
        self.font.save(font_bytes)
        font_bytes.seek(0)
        self.measure = ImageFont.truetype(font_bytes, size=1000, layout_engine=ImageFont.Layout.RAQM)
        self.outlines = {}

    def width(self, text, size, track=0):
        return self.measure.getlength(text) / 1000 * size + max(0, len(text) - 1) * track

    def draw(self, parent, text, x, y, size, fill="#111111", align="left", track=0):
        if align == "center":
            x -= self.width(text, size, track) / 2
        elif align == "right":
            x -= self.width(text, size, track)
        group = node("g", {"fill": fill, "aria-label": text}, parent)
        for i, ch in enumerate(text):
            if ch == " ":
                continue
            glyph = self.cmap.get(ord(ch))
            if glyph is None:
                raise ValueError(f"Unsupported label character: {ch!r}")
            if glyph not in self.outlines:
                pen = SVGPathPen(self.glyphs)
                self.glyphs[glyph].draw(pen)
                self.outlines[glyph] = pen.getCommands()
            if not self.outlines[glyph]:
                continue
            px = x + self.measure.getlength(text[:i]) / 1000 * size + i * track
            node("path", {"d": self.outlines[glyph],
                          "transform": f"translate({px:.5f} {y:.5f}) scale({size/self.units:.8f} {-size/self.units:.8f})"}, group)
        return group


def embed(parent, source, x, y, w, h):
    """Nest an exact outlined master; fitting changes only its outer viewport."""
    art = copy.deepcopy(ET.parse(source).getroot())
    art.set("x", str(x))
    art.set("y", str(y))
    art.set("width", str(w))
    art.set("height", str(h))
    art.set("preserveAspectRatio", "xMidYMid meet")
    parent.append(art)
    return art


def caption(labels, svg, text, x=68, y=66):
    labels.draw(svg, text, x, y, 18, fill="#555555", track=1.1)


def footer(labels, svg, note, y=852, width=1200):
    labels.draw(svg, "DRAFT — NOT FOR PUBLICATION", 68, y, 16, fill="#444444", track=.5)
    labels.draw(svg, note, width-68, y, 15, fill="#555555", align="right")


def build_signage(direction, labels, output):
    name = direction["name"]
    svg = canvas(1200, 900, f"{name} — illustrative entrance sign study",
                 "Monochrome diagram of an imagined entrance wall. This is not a photograph, actual church premises, fabrication specification or approved sign.")
    rect(svg, 0, 0, 1200, 900, "#ffffff")
    caption(labels, svg, "01 / ENTRANCE SIGN · PROPORTION STUDY")
    # Diagrammatic wall, recess and glazing: no gradients, texture, photographic claims or effects.
    rect(svg, 68, 128, 1064, 634, "#e8e8e8")
    rect(svg, 68, 128, 1064, 44, "#dcdcdc")
    rect(svg, 105, 242, 258, 520, "#c6c6c6")
    rect(svg, 123, 262, 222, 500, "#eeeeee")
    line(svg, 234, 262, 234, 762, "#b5b5b5", 2)
    line(svg, 328, 462, 328, 568, "#777777", 4)
    embed(svg, direction["horizontalPath"], 438, 280, 594, 185)
    labels.draw(svg, "RCCG · ISTANBUL, TÜRKİYE", 454, 516, 17, fill="#555555", track=1)
    line(svg, 68, 762, 1132, 762, "#c9c9c9", 2)
    footer(labels, svg, "Imagined entrance · no actual premises shown")
    write_svg(output, svg)


def build_letterhead(direction, labels, output):
    name = direction["name"]
    svg = canvas(840, 1188, f"{name} — A4 letterhead draft",
                 "Editable A4 letterhead proportion study. The correspondence and contact details are explicit placeholders. No official communication is supplied.", physical=True)
    rect(svg, 0, 0, 840, 1188, "#ffffff")
    embed(svg, direction["horizontalPath"], 76, 66, 432, 134)
    labels.draw(svg, "RCCG TABERNACLE OF PRAISE", 80, 250, 13, fill="#555555", track=.5)
    labels.draw(svg, "Istanbul, Türkiye", 80, 276, 16, fill="#444444")
    line(svg, 80, 320, 760, 320, "#d2d2d2")
    labels.draw(svg, "[CORRESPONDENCE TEXT]", 80, 418, 23, fill="#777777")
    # Lines indicate a flexible writing area without inventing a letter or church statement.
    for y, stop in [(466, 750), (498, 750), (530, 706), (594, 750), (626, 750), (658, 678)]:
        line(svg, 80, y, stop, y, "#e2e2e2", 1.2)
    line(svg, 80, 1048, 760, 1048, "#d2d2d2")
    labels.draw(svg, "[CONTACT DETAILS]", 80, 1082, 14, fill="#666666")
    labels.draw(svg, "DRAFT — NOT FOR PUBLICATION", 80, 1132, 12, fill="#555555", track=.3)
    write_svg(output, svg)


def build_letterhead_context(letterhead, direction, labels, output):
    svg = canvas(1200, 900, f"{direction['name']} — A4 letterhead context",
                 "A flat neutral-gray layout proof of the separate editable A4 letterhead. All contact and correspondence fields are placeholders.")
    rect(svg, 0, 0, 1200, 900, "#f3f3f3")
    caption(labels, svg, "02 / A4 LETTERHEAD · LAYOUT STUDY")
    embed(svg, letterhead, 347.5, 100, 505, 714)
    footer(labels, svg, "A4 · placeholder correspondence and contacts")
    write_svg(output, svg)


def build_welcome(direction, labels, output):
    svg = canvas(1080, 1080, f"{direction['name']} — square welcome identity study",
                 "A hypothetical square welcome post testing the proposed parish logo. No event, date, service schedule, mission or contact claim is supplied.")
    rect(svg, 0, 0, 1080, 1080, "#ffffff")
    labels.draw(svg, "03 / WELCOME IDENTITY STUDY", 68, 66, 16, fill="#555555", track=1)
    embed(svg, direction["stackedPath"], 274, 140, 532, 563)
    labels.draw(svg, "Welcome", 540, 845, 82, align="center", track=-1.2)
    labels.draw(svg, "RCCG · ISTANBUL, TÜRKİYE", 540, 913, 20, fill="#555555", align="center", track=1)
    labels.draw(svg, "DRAFT — NOT FOR PUBLICATION", 540, 1016, 15, fill="#555555", align="center", track=.6)
    write_svg(output, svg)


def avatar(parent, path, x, y, size, ink_size=None):
    node("circle", {"cx": x+size/2, "cy": y+size/2, "r": size/2, "fill": "#ffffff", "stroke": "#d4d4d4", "stroke-width": 1}, parent)
    inset = (size-(ink_size or size*.68))/2
    return embed(parent, path, x+inset, y+inset, size-2*inset, size-2*inset)


def build_social(direction, labels, output):
    svg = canvas(1200, 900, f"{direction['name']} — avatar and profile study",
                 "Illustrative avatar and profile layout using the primary mark. The church handle is explicitly a placeholder. No follower counts, external platform or fabricated profile is shown.")
    rect(svg, 0, 0, 1200, 900, "#ffffff")
    caption(labels, svg, "04 / AVATAR & PROFILE · PRIMARY MARK")
    path = direction["primaryPath"]
    avatar(svg, path, 95, 230, 330, ink_size=246)
    labels.draw(svg, "Avatar crop", 260, 614, 21, fill="#555555", align="center")
    rect(svg, 526, 216, 606, 410, "#f5f5f5")
    avatar(svg, path, 566, 258, 84, ink_size=62)
    labels.draw(svg, "Tabernacle", 680, 294, 32)
    labels.draw(svg, "of Praise", 680, 335, 32)
    labels.draw(svg, "[CHURCH HANDLE]", 566, 394, 20, fill="#666666", track=.4)
    labels.draw(svg, "RCCG Tabernacle of Praise", 566, 454, 23)
    labels.draw(svg, "Istanbul, Türkiye", 566, 495, 21, fill="#555555")
    line(svg, 566, 532, 1092, 532, "#d5d5d5")
    avatar(svg, path, 566, 555, 40, ink_size=30)
    labels.draw(svg, "Tabernacle of Praise", 625, 582, 24)
    labels.draw(svg, "40 px avatar context", 829, 673, 18, fill="#666666", align="center")
    footer(labels, svg, "Illustrative profile · handle is a placeholder")
    write_svg(output, svg)


def render(svg, png, width=None):
    cmd = ["inkscape", str(svg), "--export-type=png", f"--export-filename={png}"]
    if width:
        cmd.append(f"--export-width={width}")
    done = subprocess.run(cmd, capture_output=True, text=True)
    if done.returncode:
        raise RuntimeError(done.stderr or done.stdout)


def build_comparison(directions, records, labels):
    svg = canvas(2400, 3920, "Review 09 — equal-condition application comparison",
                 "Shared Rhythm and Open Praise shown under identical monochrome conditions on an imagined entrance sign, A4 letterhead, welcome post and avatar profile. All are exploratory drafts, with placeholders for unverified information.")
    rect(svg, 0, 0, 2400, 3920, "#ffffff")
    labels.draw(svg, "APPLICATION STUDIES / 09", 76, 64, 22, fill="#666666", track=1.8)
    labels.draw(svg, "Two directions, the same conditions", 76, 136, 52, track=-.8)
    labels.draw(svg, directions[0]["name"], 630, 224, 36, align="center")
    labels.draw(svg, directions[1]["name"], 1770, 224, 36, align="center")
    line(svg, 1200, 266, 1200, 3790, "#e0e0e0")
    rows = [("signage", "01 / ENTRANCE SIGN"), ("letterheadContext", "02 / A4 LETTERHEAD"),
            ("welcome", "03 / WELCOME IDENTITY POST"), ("social", "04 / AVATAR & PROFILE")]
    for i, (key, label) in enumerate(rows):
        y = 276 + i*870
        labels.draw(svg, label, 76, y+36, 24, fill="#555555", track=.8)
        line(svg, 76, y+58, 2324, y+58, "#e0e0e0")
        for j, rec in enumerate(records):
            x = 76 if j == 0 else 1252
            if key == "welcome":
                embed(svg, HERE / rec[key], x+171, y+100, 740, 740)
            else:
                embed(svg, HERE / rec[key], x, y+78, 1072, 804)
    labels.draw(svg, "DRAFT — NOT FOR PUBLICATION", 76, 3862, 21, fill="#555555", track=1)
    labels.draw(svg, "Illustrative contexts · no palette or typography approved", 2324, 3862, 20, fill="#555555", align="right")
    write_svg(HERE / "applications-comparison.svg", svg)
    render(HERE / "applications-comparison.svg", HERE / "applications-comparison.png", 2400)


def read_metadata(provisional):
    path = ROOT / "exports/development-artwork.json"
    if provisional:
        path = PREVIOUS / "exports/review-artwork.json"
        raw = json.loads(path.read_text())
        converted = []
        for i, d in enumerate(raw["directions"]):
            converted.append({"id": "shared-rhythm" if i == 0 else "open-praise", "name": d["name"],
                              "primaryFile": d["primary"], "compactFile": d["primary"], "lockups": d["lockups"]})
        return path, PREVIOUS, converted
    if not path.is_file():
        raise SystemExit("Final Review 09 metadata is not ready. Use --provisional only for layout development.")
    raw = json.loads(path.read_text())
    return path, ROOT, raw["directions"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provisional", action="store_true", help="Layout development only; uses Review 08 masters")
    args = parser.parse_args()
    metadata_path, base, data = read_metadata(args.provisional)
    if len(data) != 2:
        raise SystemExit("The equal-condition studies require exactly two directions.")
    labels = OutlinedLabels()
    records = []
    prepared = []
    for i, source in enumerate(data):
        d = dict(source)
        id_ = d.get("id", "shared-rhythm" if i == 0 else "open-praise")
        # Keep readable filenames stable even if presentation IDs are A/B.
        slug = "shared-rhythm" if "shared" in d["name"].lower() else "open-praise"
        master_files = {"primary": d["primaryFile"], "compact": d.get("compactFile") or d["primaryFile"],
                        "horizontal": d["lockups"]["horizontal"], "stacked": d["lockups"]["stacked"]}
        paths = {key: (base / value).resolve() for key, value in master_files.items()}
        for key, path in paths.items():
            if not path.is_file():
                raise FileNotFoundError(f"{d['name']} {key} master missing: {path}")
            if ET.parse(path).getroot().findall(f".//{{{SVG_NS}}}text"):
                raise ValueError(f"Master has live lettering instead of outlines: {path}")
        d.update({key+"Path": value for key, value in paths.items()})
        rec = {"id": id_, "name": d["name"],
               "signage": f"{slug}-entrance-sign.svg", "letterhead": f"{slug}-a4-letterhead.svg",
               "letterheadContext": f"{slug}-letterhead-context.svg", "welcome": f"{slug}-welcome-post.svg",
               "social": f"{slug}-avatar-profile.svg",
               "masters": {key: {"file": str(path.relative_to(ROOT.parent)), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
                           for key, path in paths.items()}}
        build_signage(d, labels, HERE / rec["signage"])
        build_letterhead(d, labels, HERE / rec["letterhead"])
        build_letterhead_context(HERE / rec["letterhead"], d, labels, HERE / rec["letterheadContext"])
        build_welcome(d, labels, HERE / rec["welcome"])
        build_social(d, labels, HERE / rec["social"])
        for key in ("signage", "letterhead", "letterheadContext", "welcome", "social"):
            render(HERE / rec[key], HERE / rec[key].replace(".svg", ".png"), 1200)
        records.append(rec)
        prepared.append(d)
    build_comparison(prepared, records, labels)
    manifest = {"status": "DRAFT — NOT FOR PUBLICATION", "provisional": args.provisional,
                "metadataFile": str(metadata_path.relative_to(ROOT.parent)),
                "metadataSha256": hashlib.sha256(metadata_path.read_bytes()).hexdigest(),
                "conditions": "Identical monochrome layouts, placement boxes, outlined companion labels and neutral diagram backgrounds for both directions.",
                "copy": "Verified name and Istanbul, Türkiye only; [CORRESPONDENCE TEXT], [CONTACT DETAILS] and [CHURCH HANDLE] are placeholders.",
                "limitation": "Entrance is an imagined proportion diagram. RCCG emblem omitted because the original authorized asset has not been transferred. No application is approved for publication or fabrication.",
                "applicationLabelFont": "Instrument Sans 450, width 100; outlines only. No font binary modified.",
                "directions": records,
                "comparison": "applications-comparison.png"}
    (HERE / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(f"Built {len(records)*4} application masters and comparison board. Provisional: {args.provisional}")


if __name__ == "__main__":
    main()
