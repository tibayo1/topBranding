#!/usr/bin/env python3
"""Build controlled teal/navy color application comparisons from colored masters.

Run from any directory after ../exports/artwork.json exists. All application
lettering is outlined. Core symbol and name contours are embedded from the
current colored Review 09 masters; the small profile avatar only recolors the
primary symbol in ivory for contrast, without using the compact drawing.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PREVIOUS = ROOT.parent / "identity-development-09"
SPEC = importlib.util.spec_from_file_location("review09_application_utilities", PREVIOUS / "applications/build.py")
U = importlib.util.module_from_spec(SPEC)
sys.dont_write_bytecode = True
SPEC.loader.exec_module(U)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cap(labels, svg, text, p):
    labels.draw(svg, text, 68, 66, 18, fill=p["primary"], track=1.1)


def foot(labels, svg, text, p):
    labels.draw(svg, "DRAFT — NOT FOR PUBLICATION", 68, 852, 16, fill=p["primary"], track=.5)
    labels.draw(svg, text, 1132, 852, 15, fill=p["primary"], align="right")


def entrance(d, p, labels, output):
    svg = U.canvas(1200, 900, f"{p['name']} / {d['name']} — entrance proportion diagram",
                   "Imagined entrance diagram, not an actual church building or a fabrication specification. Same arrangement for both logos and both palettes.")
    U.rect(svg, 0, 0, 1200, 900, "#ffffff")
    cap(labels, svg, "01 / ENTRANCE SIGN · PROPORTION STUDY", p)
    U.rect(svg, 68, 128, 1064, 634, p["neutral"])
    U.rect(svg, 68, 128, 1064, 9, p["accent"])
    U.rect(svg, 105, 242, 258, 520, p["primary"])
    U.rect(svg, 123, 262, 222, 500, p["neutral"])
    U.line(svg, 234, 262, 234, 762, p["primary"], 2)
    U.line(svg, 328, 462, 328, 568, p["primary"], 4)
    U.embed(svg, d["light"]["horizontalPath"], 438, 280, 594, 185)
    labels.draw(svg, "RCCG · ISTANBUL, TÜRKİYE", 454, 516, 17, fill=p["primary"], track=1)
    U.line(svg, 68, 762, 1132, 762, p["primary"], 1.2)
    foot(labels, svg, "Imagined entrance · flat colors, no actual premises", p)
    U.write_svg(output, svg)


def letterhead(d, p, labels, output):
    svg = U.canvas(840, 1188, f"{p['name']} / {d['name']} — A4 correspondence study",
                   "A4 layout using proposed colors. All correspondence and contacts remain explicit placeholders. Warm paper color is a screen simulation, not a stock specification.", physical=True)
    U.rect(svg, 0, 0, 840, 1188, p["neutral"])
    U.embed(svg, d["light"]["horizontalPath"], 76, 66, 432, 134)
    labels.draw(svg, "RCCG TABERNACLE OF PRAISE", 80, 250, 13, fill=p["primary"], track=.5)
    labels.draw(svg, "Istanbul, Türkiye", 80, 276, 16, fill=p["primary"])
    U.line(svg, 80, 320, 760, 320, p["accent"], 2)
    labels.draw(svg, "[CORRESPONDENCE TEXT]", 80, 418, 23, fill=p["primary"])
    for y, stop in [(466, 750), (498, 750), (530, 706), (594, 750), (626, 750), (658, 678)]:
        U.line(svg, 80, y, stop, y, p["primary"], .6)
    U.line(svg, 80, 1048, 760, 1048, p["accent"], 2)
    labels.draw(svg, "[CONTACT DETAILS]", 80, 1082, 14, fill=p["primary"])
    labels.draw(svg, "DRAFT — NOT FOR PUBLICATION", 80, 1132, 12, fill=p["primary"], track=.3)
    U.write_svg(output, svg)


def welcome(d, p, labels, output):
    svg = U.canvas(1080, 1080, f"{p['name']} / {d['name']} — welcome identity study",
                   "Hypothetical square welcome identity post; no date, service schedule, mission, venue or event claim. Large symbol uses flat gold; all supporting copy uses high contrast foregrounds.")
    U.rect(svg, 0, 0, 1080, 1080, p["primary"])
    labels.draw(svg, "03 / WELCOME IDENTITY STUDY", 68, 66, 16, fill=p["neutral"], track=1)
    U.embed(svg, d["dark"]["stackedPath"], 274, 140, 532, 563)
    U.line(svg, 490, 757, 590, 757, p["accent"], 3)
    labels.draw(svg, "Welcome", 540, 865, 82, fill=p["neutral"], align="center", track=-1.2)
    labels.draw(svg, "RCCG · ISTANBUL, TÜRKİYE", 540, 932, 20, fill=p["neutral"], align="center", track=1)
    labels.draw(svg, "DRAFT — NOT FOR PUBLICATION", 540, 1016, 15, fill=p["neutral"], align="center", track=.6)
    U.write_svg(output, svg)


def avatar(parent, path, x, y, size, p, ink_size=None):
    # The nested source has a square primary-colored background; clip the whole
    # embedding to the circle so no square corner can leak outside the crop.
    ident = f"avatar-{x}-{y}-{size}".replace(".", "-")
    defs = U.node("defs", parent=parent)
    clip = U.node("clipPath", {"id": ident}, defs)
    U.node("circle", {"cx": x+size/2, "cy": y+size/2, "r": size/2}, clip)
    group = U.node("g", {"clip-path": f"url(#{ident})"}, parent)
    U.node("circle", {"cx": x+size/2, "cy": y+size/2, "r": size/2, "fill": p["primary"]}, group)
    inset = (size - (ink_size or size*.68))/2
    U.embed(group, path, x+inset, y+inset, size-2*inset, size-2*inset)


def social(d, p, labels, output):
    svg = U.canvas(1200, 900, f"{p['name']} / {d['name']} — avatar and profile study",
                   "Illustrative profile with placeholder handle. Normal avatar uses primary contour. Smaller dark avatars use ivory primary-contour ink for stronger contrast; no compact symbol is enlarged.")
    U.rect(svg, 0, 0, 1200, 900, "#ffffff")
    cap(labels, svg, "04 / AVATAR & PROFILE · PRIMARY CONTOUR", p)
    path = d["dark"]["symbolPath"]
    avatar(svg, path, 95, 230, 330, p, ink_size=246)
    labels.draw(svg, "Large avatar · flat gold", 260, 614, 20, fill=p["primary"], align="center")
    U.rect(svg, 526, 216, 606, 410, p["neutral"])
    avatar(svg, d["dark"]["symbolHighContrastPath"], 566, 258, 84, p, ink_size=62)
    labels.draw(svg, "Tabernacle", 680, 294, 32, fill=p["primary"])
    labels.draw(svg, "of Praise", 680, 335, 32, fill=p["primary"])
    labels.draw(svg, "[CHURCH HANDLE]", 566, 394, 20, fill=p["primary"], track=.4)
    labels.draw(svg, "RCCG Tabernacle of Praise", 566, 454, 23, fill=p["primary"])
    labels.draw(svg, "Istanbul, Türkiye", 566, 495, 21, fill=p["primary"])
    U.line(svg, 566, 532, 1092, 532, p["primary"], .6)
    avatar(svg, d["dark"]["symbolHighContrastPath"], 566, 555, 40, p, ink_size=30)
    labels.draw(svg, "Tabernacle of Praise", 625, 582, 24, fill=p["primary"])
    labels.draw(svg, "Smaller avatar contexts · ivory ink", 829, 673, 18, fill=p["primary"], align="center")
    foot(labels, svg, "Illustrative profile · handle is a placeholder", p)
    U.write_svg(output, svg)


def board(directions, records, p, labels):
    svg = U.canvas(2400, 3920, f"{p['family']} — two-logo application comparison",
                   "Same context placements and copy for Shared Rhythm and Open Praise. Entrance, A4 correspondence, welcome post and avatar/profile studies. All are drafts, not approved templates.")
    U.rect(svg, 0, 0, 2400, 3920, "#ffffff")
    labels.draw(svg, "COLOR APPLICATION STUDIES / 10", 76, 64, 22, fill=p["primary"], track=1.8)
    labels.draw(svg, p["family"], 76, 136, 52, fill=p["primary"], track=-.8)
    labels.draw(svg, directions[0]["name"], 630, 224, 36, fill=p["primary"], align="center")
    labels.draw(svg, directions[1]["name"], 1770, 224, 36, fill=p["primary"], align="center")
    U.line(svg, 1200, 266, 1200, 3790, p["neutral"], 2)
    rows = [("entrance", "01 / ENTRANCE SIGN"), ("letterhead", "02 / A4 CORRESPONDENCE"),
            ("welcome", "03 / WELCOME IDENTITY POST"), ("social", "04 / AVATAR & PROFILE")]
    for i, (key, title) in enumerate(rows):
        y = 276+i*870
        labels.draw(svg, title, 76, y+36, 24, fill=p["primary"], track=.8)
        U.line(svg, 76, y+58, 2324, y+58, p["accent"], 1.5)
        for j, rec in enumerate(records):
            x = 76 if j == 0 else 1252
            if key == "welcome":
                U.embed(svg, HERE / rec[key], x+171, y+100, 740, 740)
            elif key == "letterhead":
                # Keep the A4 ratio and same paper size for both logo directions.
                U.rect(svg, x, y+78, 1072, 804, p["neutral"])
                U.embed(svg, HERE / rec[key], x+278.5, y+96, 515, 728.36)
            else:
                U.embed(svg, HERE / rec[key], x, y+78, 1072, 804)
    labels.draw(svg, "DRAFT — NOT FOR PUBLICATION", 76, 3862, 21, fill=p["primary"], track=1)
    labels.draw(svg, "Palette, artwork and typography remain open", 2324, 3862, 20, fill=p["primary"], align="right")
    output = HERE / f"applications-{p['id']}.svg"
    U.write_svg(output, svg)
    U.render(output, output.with_suffix(".png"), 2400)
    return output


def main():
    metadata_path = ROOT / "exports/artwork.json"
    palettes_path = ROOT / "source/palettes.json"
    data = json.loads(metadata_path.read_text())
    palette_data = json.loads(palettes_path.read_text())
    entries = data["entries"]
    labels = U.OutlinedLabels()
    all_records = []
    boards = []
    for palette_id in ("teal", "navy"):
        p = next(p for p in palette_data["palettes"] if p["id"] == palette_id)
        directions = []
        records = []
        for direction_id, name in (("shared-rhythm", "Shared Rhythm"), ("open-praise", "Open Praise")):
            d = {"id": direction_id, "name": name}
            sources = {}
            for mode in ("light", "dark"):
                entry = next(e for e in entries if e["paletteId"] == palette_id and e["directionId"] == direction_id and e["mode"] == mode)
                d[mode] = {}
                for key in ("symbol", "symbolHighContrast", "horizontal", "stacked"):
                    path = (ROOT / entry[key]).resolve()
                    if not path.is_file():
                        raise FileNotFoundError(path)
                    if ET.parse(path).getroot().findall(f".//{{{U.SVG_NS}}}text"):
                        raise ValueError(f"Master lettering must be outlined: {path}")
                    d[mode][key+"Path"] = path
                    sources[f"{mode}/{key}"] = {"file": str(path.relative_to(ROOT)), "sha256": sha(path)}
            prefix = f"{palette_id}-{direction_id}"
            rec = {"paletteId": palette_id, "directionId": direction_id, "name": name,
                   "entrance": f"{prefix}-entrance-sign.svg", "letterhead": f"{prefix}-a4-letterhead.svg",
                   "welcome": f"{prefix}-welcome-post.svg", "social": f"{prefix}-avatar-profile.svg",
                   "masters": sources}
            entrance(d, p, labels, HERE / rec["entrance"])
            letterhead(d, p, labels, HERE / rec["letterhead"])
            welcome(d, p, labels, HERE / rec["welcome"])
            social(d, p, labels, HERE / rec["social"])
            records.append(rec)
            directions.append(d)
        output = board(directions, records, p, labels)
        boards.append({"paletteId": palette_id, "svg": output.name, "png": output.with_suffix(".png").name})
        all_records.extend(records)
    manifest = {
        "status": "DRAFT — NOT FOR PUBLICATION", "approval": False,
        "metadata": {"file": "../exports/artwork.json", "sha256": sha(metadata_path)},
        "palettes": {"file": "../source/palettes.json", "sha256": sha(palettes_path)},
        "conditions": "Identical layouts, placement boxes and copy for both marks, repeated across teal and navy. Existing Review 09 core contours and lettering are unchanged.",
        "applicationLabelFont": "Instrument Sans 450, width 100; outlined from Review 09's existing licensed font. Core name remains the Review 09 Instrument Sans 470 outline.",
        "smallAvatar": "Profile avatars embed the recorded symbolHighContrast primary contours in ivory rather than soft gold. No contour or source fill is modified, and compact drawings are not enlarged.",
        "copy": "Only church names and Istanbul, Türkiye verified. [CORRESPONDENCE TEXT], [CONTACT DETAILS], [CHURCH HANDLE] are placeholders.",
        "limitations": ["Entrance is an imagined diagram, not actual premises or a fabrication specification.", "Gold is a flat color, not a metallic material.", "Authorized official RCCG PNG is absent; emblem not reconstructed or paired.", "No application, palette or type choice is approved for publication."],
        "applications": all_records, "comparisons": boards,
    }
    (HERE / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print("Built 16 editable applications and two equal-condition palette boards.")


if __name__ == "__main__":
    main()
