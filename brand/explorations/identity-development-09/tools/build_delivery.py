#!/usr/bin/env python3
"""Build a six-page draft development review from the editable Review 09 masters.

Run from any directory after tools/build_lockups.py and applications/build.py.
The HTML contains its font and all artwork, so the saved source is self-contained.
It is a review document, not approved identity guidelines or publication artwork.
"""
from __future__ import annotations

import base64
from html import escape
import json
from pathlib import Path
import xml.etree.ElementTree as ET

from playwright.sync_api import sync_playwright
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "exports"
DRAFT = "DRAFT — NOT FOR PUBLICATION"
SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)


def uri(path: str | Path) -> str:
    file = ROOT / path
    mime = "image/svg+xml" if file.suffix == ".svg" else "image/png"
    return f"data:{mime};base64," + base64.b64encode(file.read_bytes()).decode()


def artwork(path: str | Path, css: str = "", label: str = "") -> str:
    return f'<img class="{css}" src="{uri(path)}" alt="{escape(label or str(path), quote=True)}">'


def equal_ink_symbol(row: dict) -> str:
    """Change only the outer viewport; both symbols display at 150 px ink height."""
    svg = ET.parse(ROOT / row["primaryFile"]).getroot()
    x0, y0, x1, y1 = row["inkBounds"]
    svg.set("viewBox", f"{x0} {y0} {x1-x0} {y1-y0}")
    svg.set("width", str((x1-x0)/(y1-y0)*150))
    svg.set("height", "150")
    svg.set("class", "equal-symbol")
    return ET.tostring(svg, encoding="unicode")


def header(title: str, subtitle: str, number: int) -> str:
    return (f'<header><div class="eyebrow"><span>RCCG TABERNACLE OF PRAISE · ISTANBUL</span>'
            f'<span>DEVELOPMENT 09 / {number:02d}</span></div>'
            f'<h1>{escape(title)}</h1><p class="subtitle">{escape(subtitle)}</p></header>')


def footer(number: int) -> str:
    return (f'<footer><span>{DRAFT}</span>'
            '<span>Both directions remain in development. No logo, palette or type system is final.</span>'
            f'<span>{number} / 6</span></footer>')


def overview(data: dict) -> str:
    notes = {
        "shared-rhythm": (
            "Gathering space + collective rhythm",
            "Four unequal folded faces hold a shared open space. Their changing heights suggest people responding together in praise.",
            "The liked primary form is preserved. The name has more breathing room, and a separate tiny-use drawing opens the intervals."
        ),
        "open-praise": (
            "Tabernacle + Praise through negative space",
            "A P-like outer contour holds an open T-shaped interior. The two letters connect the parish name through one compact gesture.",
            "A shorter, blunter inner terminal replaces the pointed hook. The open interior is adjusted; the T remains a reading to test."
        ),
    }
    cards = []
    for i, row in enumerate(data["directions"], 1):
        theme, meaning, changes = notes[row["id"]]
        cards.append(f'''<article class="concept-card">
<div class="concept-head"><h2>{i:02d} / {escape(row['name'])}</h2><p>{escape(theme)}</p></div>
<div class="equal-field">{equal_ink_symbol(row)}</div>
<div class="name-field">{artwork(row['lockups']['wordmark'], 'wordmark', 'Tabernacle of Praise outlined name')}</div>
<div class="reverse-field">{artwork(row['lockups']['horizontalReverse'], 'reverse-lockup', row['name'] + ' reversed full-name arrangement')}</div>
<p class="meaning">{escape(meaning)}</p><p class="changes"><b>Developed:</b> {escape(changes)}</p>
</article>''')
    note = ('Top symbols share the same actual ink height. Practical lockups below use the same name scale; '
            'the denser Open Praise symbol is 7% smaller for visual balance. Working lettering: Instrument Sans, title case.')
    return (f'<section class="sheet" id="overview">'
            + header("Two directions, developed further", "Monochrome studies · complete parish name · light and dark", 1)
            + '<main class="overview-grid">' + ''.join(cards) + '</main>'
            + f'<p class="page-note">{escape(note)}</p>' + footer(1) + '</section>')


def proof_page(kind: str, number: int) -> str:
    if kind == "shared-rhythm":
        title, subtitle = "Shared Rhythm", "Preserving the form you liked; opening its tiny-use intervals"
        source = "shared-rhythm/renders/primary-and-compact.png"
        paragraphs = [
            ("What it expresses", "A sanctuary is suggested by four folded faces around an open forecourt. Their uneven rise and fall brings praise into the same arrangement, without adding a separate music icon."),
            ("What changed", "The main symbol is unchanged from Review 08. A dedicated 16–20 px candidate narrows the faces and opens the intervals while retaining the small fold shoulder."),
            ("Where to be careful", "The primary feels more coherent at normal sizes. The compact cut looks more disconnected when enlarged and should stay a tiny-use experiment. At 16 px, the result is still an abstract rhythm."),
            ("Meaning still to test", "Architecture, a cultural venue or property branding are possible associations. Praise is an abstract cadence; the full name and church context remain important."),
        ]
    else:
        title, subtitle = "Open Praise", "A calmer interior within the same compact outer silhouette"
        source = "open-praise/renders/outline-comparison.png"
        paragraphs = [
            ("What it expresses", "The outer P and proposed negative T refer to Praise and Tabernacle. The open exit offers a sense of welcome. It is a name-based figure-ground idea, rather than a literal church building or instrument."),
            ("What changed", "The main outline is the balanced-counter trial shown second in this proof. Its inner hook ends earlier with a blunt terminal, and the negative stem is slightly wider. The level-terminal trial was not taken forward."),
            ("Small-use candidate", "The compact drawing further widens the negative stem and shortens the tip. At 16–20 px, the silhouette is clearer than the full letter reading. Normal applications retain the primary."),
            ("Meaning still to test", "The T is inferential and the P may dominate. A publisher, creative studio or luxury identity is another possible association. This refinement does not establish universal letter recognition."),
        ]
    notes = ''.join(f'<div><h3>{escape(head)}</h3><p>{escape(body)}</p></div>' for head, body in paragraphs)
    return (f'<section class="sheet" id="{kind}">' + header(title, subtitle, number)
            + f'<main class="proof-layout"><div class="proof-image">{artwork(source, "proof-board", title + " optical comparison")}</div>'
            + '<aside class="notes">' + notes
            + '<p class="small-note">This proof board is scaled to fit the page. Use the separate native PNGs for 1:1 pixel checks. Minimum-size rules remain provisional.</p></aside></main>'
            + footer(number) + '</section>')


def typography_page() -> str:
    return (f'<section class="sheet" id="typography">'
            + header("Lettering changes the voice", "Three provisional approaches, applied to both directions", 4)
            + '<main class="type-layout"><div class="type-image">'
            + artwork("type-study/typographic-comparison.svg", "type-board", "Three lettering approaches compared across both symbols")
            + '</div><aside class="notes">'
            + '<div><h3>01 / Open title case — working choice</h3><p>Readable word shapes and a welcoming tone. Instrument Sans at weight 470 is used in the new development lockups and application studies.</p></div>'
            + '<div><h3>02 / Measured capitals</h3><p>A more formal, composed voice. The wide setting brings confidence, but can make the parish feel less personal and require more width at small sizes.</p></div>'
            + '<div><h3>03 / Warm serif</h3><p>Source Serif 4 adds warmth and a literary character. It can also move the identity toward a traditional institution or publisher.</p></div>'
            + '<p class="small-note">This board deliberately uses the unchanged Review 08 symbols to isolate the lettering comparison. Current refined symbols appear on the other pages.</p>'
            + '<p class="small-note">Font-based, outlined and optically spaced; these are original font glyphs, not a claim of custom-drawn type. The type decision remains open.</p>'
            + '</aside></main>' + footer(4) + '</section>')


def application_page(data: dict, number: int, contexts: list[tuple[str, str]], title: str) -> str:
    cells = []
    for suffix, label in contexts:
        for row in data["directions"]:
            path = f'applications/{row["id"]}-{suffix}.svg'
            cells.append(f'<article class="application-card"><h3>{escape(row["name"])} <span>· {escape(label)}</span></h3>'
                         + artwork(path, "application-image", row["name"] + " " + label) + '</article>')
    note = ('The entrance is an imagined proportion study. Correspondence, contact details and social handle are placeholders. '
            'The original RCCG emblem PNG is absent, so no actual two-emblem pairing is shown.')
    return (f'<section class="sheet" id="applications-{number}">'
            + header(title, "The same quiet layouts and monochrome conditions for both concepts", number)
            + '<main class="applications-grid">' + ''.join(cells) + '</main>'
            + f'<p class="page-note">{escape(note)}</p>' + footer(number) + '</section>')


def main() -> None:
    data = json.loads((OUT / "development-artwork.json").read_text())
    manifest = json.loads((ROOT / "applications/manifest.json").read_text())
    if manifest["provisional"]:
        raise SystemExit("Rebuild applications from final Review 09 masters before rendering delivery.")
    font = base64.b64encode((ROOT / "type-study/fonts/instrumentsans/InstrumentSans[wdth,wght].ttf").read_bytes()).decode()
    css = '''
@font-face{font-family:Review;src:url(data:font/ttf;base64,FONTDATA);font-weight:100 900;font-stretch:75% 100%;font-display:block}
*{box-sizing:border-box}html,body{margin:0;padding:0;background:#e8e8e8;color:#111;font-family:Review,Arial,sans-serif;font-weight:450}p,h1,h2,h3{margin:0}b{font-weight:650}img{display:block;object-fit:contain}.sheet{position:relative;overflow:hidden;background:#fff;width:1122px;height:794px;margin:0 auto 24px;padding:32px 42px 46px;break-after:page;page-break-after:always}.sheet:last-child{break-after:auto;page-break-after:auto}
.eyebrow{display:flex;justify-content:space-between;font-size:10px;font-weight:600;letter-spacing:1.15px}.eyebrow span:last-child{white-space:nowrap}h1{font-size:32px;line-height:1.12;letter-spacing:-.6px;font-weight:550;margin-top:18px}.subtitle{font-size:13px;line-height:1.4;color:#555;margin-top:7px}footer{position:absolute;left:42px;right:42px;bottom:19px;border-top:1px solid #ccc;padding-top:11px;display:flex;justify-content:space-between;gap:14px;font-size:9px;line-height:1.4;color:#555}footer span:first-child{font-weight:650;color:#111;letter-spacing:.4px;white-space:nowrap}footer span:last-child{white-space:nowrap}.page-note{position:absolute;left:42px;right:42px;bottom:66px;font-size:10px;line-height:1.45;color:#555}
.overview-grid{display:grid;grid-template-columns:1fr 1fr;gap:42px;margin-top:24px}.concept-head{border-top:1px solid #bbb;padding-top:12px}.concept-head h2{font-size:23px;line-height:1.15;font-weight:550}.concept-head p{font-size:11px;color:#555;margin-top:5px}.equal-field{height:176px;display:flex;align-items:center;justify-content:center}.equal-symbol{height:150px;flex:none;display:block}.name-field{height:108px;display:flex;align-items:center;justify-content:center}.wordmark{width:300px;height:108px}.reverse-field{height:118px;background:#000;display:flex;align-items:center;justify-content:center}.reverse-lockup{height:112px;width:375px}.meaning{font-size:12px;line-height:1.45;margin-top:12px}.changes{font-size:11px;line-height:1.45;color:#555;margin-top:7px}
.proof-layout{display:grid;grid-template-columns:660px 1fr;gap:30px;margin-top:23px;align-items:start}.proof-image{height:568px;display:flex;align-items:flex-start;justify-content:center}.proof-board{width:660px;height:568px;object-position:top center}.notes{padding-top:1px}.notes>div{border-top:1px solid #d5d5d5;padding-top:12px;margin-bottom:18px}.notes h3{font-size:12px;line-height:1.35;font-weight:600}.notes p{font-size:12px;line-height:1.5;margin-top:7px;color:#444}.notes .small-note{font-size:10px;line-height:1.5;color:#666;margin-top:14px}.type-layout{display:grid;grid-template-columns:600px 1fr;gap:42px;margin-top:19px}.type-image{height:580px;display:flex;justify-content:center}.type-board{width:572px;height:580px}.type-layout .notes{padding-top:13px}.type-layout .notes>div{margin-bottom:24px}.type-layout .notes p{font-size:13px}
.applications-grid{display:grid;grid-template-columns:1fr 1fr;grid-template-rows:257px 257px;gap:17px 26px;margin-top:23px}.application-card{min-width:0;overflow:hidden}.application-card h3{font-size:13px;line-height:1.3;font-weight:600;border-top:1px solid #ccc;padding-top:8px}.application-card h3 span{font-weight:450;color:#555}.application-image{width:100%;height:227px;margin-top:3px}
@page{size:A4 landscape;margin:0}@media print{html,body{background:#fff;print-color-adjust:exact;-webkit-print-color-adjust:exact}.sheet{margin:0;width:297mm;height:210mm}}
'''.replace("FONTDATA", font)
    body = (overview(data) + proof_page("shared-rhythm", 2) + proof_page("open-praise", 3)
            + typography_page()
            + application_page(data, 5, [("entrance-sign", "Entrance sign"), ("letterhead-context", "A4 letterhead")], "An identity at the door and on paper")
            + application_page(data, 6, [("welcome-post", "Welcome post"), ("avatar-profile", "Avatar and profile")], "A clear presence on social media"))
    source = ('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
              '<title>Tabernacle of Praise · Development 09 · DRAFT</title><style>' + css + '</style><body>' + body + '</body></html>')
    (OUT / "review-source.html").write_text(source, encoding="utf-8")
    names = [
        ("overview", "two-directions-development.png"),
        ("shared-rhythm", "shared-rhythm-development.png"),
        ("open-praise", "open-praise-development.png"),
        ("typography", "lettering-development.png"),
        ("applications-5", "signage-and-stationery.png"),
        ("applications-6", "social-applications.png"),
    ]
    reports = []
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path="/usr/bin/chromium", args=["--no-sandbox", "--disable-dev-shm-usage"])
        page = browser.new_page(viewport={"width": 1200, "height": 1200}, device_scale_factor=2)
        page.set_content(source, wait_until="load")
        page.evaluate("document.fonts.ready")
        for anchor, filename in names:
            page.locator("#" + anchor).screenshot(path=str(OUT / filename), animations="disabled")
            reports.append(page.evaluate('''id=>{const s=document.getElementById(id),b=s.getBoundingClientRect();return {page:id,brokenImages:[...s.querySelectorAll('img')].filter(x=>!x.complete||!x.naturalWidth).length,bodyBottom:s.querySelector('main').getBoundingClientRect().bottom-b.top,footerTop:s.querySelector('footer').getBoundingClientRect().top-b.top}}''', anchor))
        page.pdf(path=str(OUT / "development-review-09.pdf"), prefer_css_page_size=True, print_background=True, display_header_footer=False)
        browser.close()
    pdf = PdfReader(OUT / "development-review-09.pdf")
    assert len(pdf.pages) == 6, f"Expected six pages, found {len(pdf.pages)}"
    for report in reports:
        assert report["brokenImages"] == 0, report
        assert report["bodyBottom"] < report["footerTop"] - 4, report
    print(json.dumps({"pdfPages": len(pdf.pages), "layout": reports}, indent=2))


if __name__ == "__main__":
    main()
