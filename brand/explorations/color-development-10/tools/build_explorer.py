#!/usr/bin/env python3
"""Build the portable, editable color comparison from the generated SVG manifest."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def clean_svg(path: str) -> str:
    import xml.etree.ElementTree as ET
    node = ET.fromstring((ROOT / path).read_text())
    for element in node.iter():
        element.attrib.pop("id", None)
        element.attrib.pop("aria-labelledby", None)
        element.attrib.pop("width", None) if element is node else None
        element.attrib.pop("height", None) if element is node else None
    node.set("aria-hidden", "true")
    node.set("focusable", "false")
    ET.register_namespace("", "http://www.w3.org/2000/svg")
    return ET.tostring(node, encoding="unicode")


STYLE = r"""
:root{color-scheme:light;--ink:#25292d;--muted:#626769;--paper:#f8f7f3;--rule:#d8dbd7;--white:#fff;--highlight:#10494c}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font-family:Arial,Helvetica,sans-serif;line-height:1.5}button{font:inherit}button:focus-visible,a:focus-visible{outline:3px solid #286e74;outline-offset:4px}button{cursor:pointer}a{color:inherit}main{max-width:1248px;margin:0 auto;padding:40px 24px 64px}header{display:flex;justify-content:space-between;align-items:center;padding-bottom:26px;border-bottom:1px solid var(--rule);gap:20px}.eyebrow{font-size:11px;letter-spacing:.13em;text-transform:uppercase;font-weight:700}.draft{font-size:10px;letter-spacing:.06em;border:1px solid #aeb4af;padding:5px 9px;white-space:nowrap}.intro{display:grid;grid-template-columns:1.2fr 1fr;gap:40px;margin:34px 0 30px;align-items:end}h1{font-size:clamp(32px,4vw,50px);font-weight:500;line-height:1.08;letter-spacing:-.035em;margin:0}h2{font-weight:500;letter-spacing:-.02em;margin:0;font-size:30px}h3{margin:0;font-size:16px;font-weight:600}p{margin:0}.intro p{max-width:480px;color:var(--muted);font-size:14px}.palette-picker{display:grid;grid-template-columns:repeat(5,1fr);gap:10px}.palette-button{border:1px solid var(--rule);padding:14px 13px 12px;text-align:left;background:#fff;color:var(--ink);border-radius:0;position:relative;min-height:112px}.palette-button[aria-pressed=true]{border:2px solid var(--ink);padding:13px 12px 11px}.palette-button strong{font-size:13px;font-weight:600;display:block;margin-top:13px}.palette-button .index{font-size:10px;color:var(--muted);position:absolute;top:14px;right:12px}.mini-swatches{display:flex;gap:3px}.mini-swatches i{width:19px;height:19px;display:block;border:1px solid #00000014}.detail{margin-top:36px}.detail-heading{display:flex;justify-content:space-between;align-items:end;gap:24px;margin-bottom:16px}.detail-heading .mood{font-size:12px;color:var(--muted);margin-top:4px}.toolbar{display:flex;gap:12px;flex-wrap:wrap}.segmented{display:inline-flex;border:1px solid #aeb4af;background:#fff;padding:3px;gap:2px}.segmented button{background:none;border:0;padding:6px 11px;font-size:12px;color:#4b5354}.segmented button[aria-pressed=true]{background:#25292d;color:white}.detail-grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}.concept-card{border:1px solid var(--rule);background:#fff;min-width:0}.concept-title{padding:14px 18px;display:flex;justify-content:space-between;align-items:center;gap:10px;border-bottom:1px solid var(--rule)}.concept-title span{font-size:10px;color:var(--muted);text-transform:uppercase;letter-spacing:.08em}.concept-panes{display:grid;grid-template-columns:1fr 1fr}.mode-single .concept-panes{grid-template-columns:1fr}.logo-pane{min-width:0;position:relative;display:flex;flex-direction:column}.logo-pane+.logo-pane{border-left:1px solid #0000000a}.logo-art{height:190px;display:flex;align-items:center;justify-content:center;padding:18px 10px 4px}.logo-art svg{width:100%;height:100%;max-width:450px;display:block}.surface-label{font-size:9px;text-transform:uppercase;letter-spacing:.09em;padding:12px 14px 0;opacity:.8}.small-proof{border-top:1px solid #00000018;margin:8px 14px 0;padding:11px 0 12px;display:flex;align-items:center;gap:15px}.small-proof>span{font-size:9px;line-height:1.4;max-width:56px;opacity:.8}.native-icon{display:inline-flex;align-items:center;justify-content:center}.native-icon svg{width:100%;height:100%;display:block}.swatch-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:18px 0}.swatch-card{border:1px solid var(--rule);background:#fff;display:flex;gap:12px;padding:12px;align-items:center}.swatch-chip{width:38px;height:48px;flex-shrink:0;border:1px solid #00000014}.swatch-role{font-size:9px;text-transform:uppercase;letter-spacing:.09em;color:var(--muted)}.swatch-name{font-size:12px;margin:2px 0}.hex{font-family:ui-monospace,SFMono-Regular,Consolas,monospace;font-size:12px;user-select:all}.palette-notes{display:grid;grid-template-columns:1fr 1fr;gap:28px;padding:6px 0 28px;font-size:13px;color:var(--muted)}.palette-notes p{max-width:530px}.exploration-note{padding:18px 20px;background:#e9ece7;border-left:3px solid #78877e;font-size:12px;color:#424b45;line-height:1.7}.exploration-note strong{font-weight:600;color:#252d28}.matrix-section{margin-top:50px}.matrix-scroll{overflow:auto;margin-top:22px}.matrix-export{min-width:1160px;background:#f8f7f3;padding:28px 24px 25px}.matrix-head{display:flex;justify-content:space-between;gap:28px;align-items:start;padding-bottom:22px}.matrix-head h2{font-size:32px;line-height:1.14}.matrix-head p{font-size:11px;color:var(--muted);max-width:420px;margin-top:10px}.matrix-brand{font-size:10px;letter-spacing:.06em;text-align:right;line-height:1.7}.matrix-column-head{display:grid;grid-template-columns:185px repeat(4,minmax(0,1fr));gap:10px;font-size:11px;padding:0 0 12px;align-items:end}.matrix-column-head .concept-group{grid-column:span 2;text-align:center;font-weight:600}.matrix-column-head .surfaces{font-size:9px;font-weight:400;color:var(--muted);margin-top:3px;display:flex;justify-content:space-around}.matrix-row{display:grid;grid-template-columns:185px repeat(4,minmax(0,1fr));gap:10px;min-height:191px;border-top:1px solid #cdd1ca;padding:12px 0}.matrix-palette{padding:2px 6px 0 0}.matrix-palette .num{font-size:9px;letter-spacing:.08em;color:var(--muted)}.matrix-palette h3{font-size:15px;line-height:1.2;margin:3px 0 7px}.matrix-mood{font-size:9px;color:var(--muted);line-height:1.5;min-height:29px}.matrix-colors{display:grid;grid-template-columns:repeat(2,1fr);gap:5px 7px;margin-top:9px}.matrix-color{display:flex;align-items:center;gap:4px;min-width:0}.matrix-color i{display:block;width:13px;height:20px;flex-shrink:0;border:1px solid #00000019}.matrix-color span{font-size:7px;line-height:1.3;color:#49514b}.matrix-color code{font-size:8px;color:#25292d;display:block}.matrix-art{display:flex;align-items:center;justify-content:center;min-width:0;padding:5px 1px;align-self:stretch;border:1px solid #0000000a}.matrix-art svg{display:block;width:100%;height:100%;max-height:155px}.matrix-foot{border-top:1px solid #cdd1ca;padding-top:16px;display:flex;gap:30px;justify-content:space-between}.matrix-foot p{max-width:535px;font-size:9px;color:#555c56;line-height:1.6}.matrix-export>.draft{display:inline-block;margin-top:15px;font-size:8px}.closing{margin-top:24px;font-size:12px;color:var(--muted);max-width:840px}.exporting main{max-width:none;padding:0}.exporting .interactive-only{display:none}.exporting .matrix-section{margin:0}.exporting .matrix-scroll{margin:0;overflow:visible}.exporting .matrix-export{width:1200px;min-width:1200px}.exporting .matrix-head h2{font-size:32px}.exporting .matrix-row{min-height:196px}.exporting .matrix-art svg{max-height:160px}@media(max-width:900px){.intro{grid-template-columns:1fr;gap:20px}.palette-picker{grid-template-columns:repeat(3,1fr)}.detail-heading{align-items:start;flex-direction:column}.swatch-grid{grid-template-columns:repeat(2,1fr)}.concept-panes{grid-template-columns:1fr}.logo-pane+.logo-pane{border-left:0}.palette-notes{grid-template-columns:1fr;gap:12px}.logo-art{height:200px}}@media(max-width:600px){main{padding:25px 16px 40px}header{align-items:start;flex-direction:column;gap:12px}.intro{margin-top:26px}.palette-picker{grid-template-columns:repeat(2,1fr);gap:8px}.palette-button{min-height:100px}.detail-grid{grid-template-columns:1fr}.detail-heading h2{font-size:27px}.swatch-card{gap:8px;padding:9px}.swatch-name{font-size:11px}.swatch-chip{width:28px;height:44px}.palette-notes{font-size:12px}.concept-panes{grid-template-columns:1fr 1fr}.logo-art{height:160px;padding:10px 4px 0}.small-proof{gap:10px;margin:6px 10px 0}.surface-label{padding:12px 10px 0}.toolbar{gap:8px}.segmented button{padding:6px 9px}}
"""

SCRIPT = r"""
const palettes = DATA.palettes.filter(p=>p.id!=='mono');
const roles=['primary','secondary','accent','neutral'];
let selected='teal', view='both', ink='color', darkInk='accent';
const $=s=>document.querySelector(s);
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const entry=(paletteId,directionId,mode)=>DATA.entries.find(e=>e.paletteId===paletteId&&e.directionId===directionId&&e.mode===mode);
function swatches(p,mini=false){return roles.map(role=>mini?`<i style="background:${p[role]}"></i>`:`<div class="swatch-card"><div class="swatch-chip" style="background:${p[role]}"></div><div><div class="swatch-role">${role}</div><div class="swatch-name">${esc(p.names[role])}</div><code class="hex">${p[role]}</code></div></div>`).join('');}
function paletteButtons(){ $('#palettePicker').innerHTML=palettes.map(p=>`<button class="palette-button" type="button" data-palette="${p.id}" aria-pressed="${p.id===selected}"><span class="mini-swatches" aria-hidden="true">${swatches(p,true)}</span><span class="index">${p.number}</span><strong>${esc(p.name)}</strong></button>`).join(''); }
function detail(){
 const p=palettes.find(p=>p.id===selected); const pid=ink==='mono'?'mono':selected; const modes=view==='both'?['light','dark']:[view];
 $('#paletteName').textContent=p.family; $('#paletteMood').textContent=p.mood+(ink==='mono'?' · Monochrome control':'');
 $('#detailGrid').classList.toggle('mode-single',view!=='both');
 $('#detailGrid').innerHTML=DATA.directions.map(d=>`<article class="concept-card"><div class="concept-title"><h3>${esc(d.name)}</h3><span>Development 09</span></div><div class="concept-panes">${modes.map(mode=>{ const e=entry(pid,d.id,mode); return `<div class="logo-pane" data-mode="${mode}" style="background:${e.colors.background};color:${e.colors.name}"><div class="surface-label">${mode} background${ink==='mono'?' · monochrome':''}</div><div class="logo-art" aria-label="${esc(d.name)} full-name logo, ${mode} background">${mode==='dark'&&ink==='color'&&darkInk==='ivory'?e.horizontalNeutralSvg:e.horizontalSvg}</div><div class="small-proof"><span>32 px main<br>20 px compact</span><span class="native-icon" style="width:32px;height:32px" aria-label="32 pixel primary symbol">${e.symbolHighContrastSvg}</span><span class="native-icon" style="width:20px;height:20px" aria-label="20 pixel compact symbol">${e.compactSvg}</span></div></div>`;}).join('')}</div></article>`).join('');
 $('#swatches').innerHTML=swatches(p); $('#paletteNote').textContent=p.note; $('#printNote').textContent=p.print;
 document.querySelectorAll('[data-palette]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.palette===selected)));
 document.querySelectorAll('[data-view]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.view===view)));
 document.querySelectorAll('[data-ink]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.ink===ink)));
 document.querySelectorAll('[data-dark-ink]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.darkInk===darkInk)));
 $('#reverseNote').textContent=ink==='color'&&darkInk==='ivory'&&view!=='light'?'Ivory reverse uses each palette’s light neutral for the dark symbol and name. It gives higher contrast than the accent symbol, especially in teal. Geometry and spacing stay unchanged.':'Dark-symbol comparison: Accent keeps the ceremonial color visible; Ivory reverse uses the light neutral for higher contrast. Compact symbols already use neutral on dark.';
 $('#selectionStatus').textContent=`Showing ${p.name}, ${view==='both'?'light and dark backgrounds':view+' background'}, ${ink==='mono'?'monochrome control':'color exploration'}.`;
}
function matrix(){
 $('#matrixRows').innerHTML=palettes.map(p=>`<div class="matrix-row"><div class="matrix-palette"><div class="num">${p.number} / COLOR DIRECTION</div><h3>${esc(p.name)}</h3><p class="matrix-mood">${esc(p.mood)}</p><div class="matrix-colors">${roles.map(role=>`<div class="matrix-color"><i style="background:${p[role]}"></i><span>${role}<code>${p[role]}</code></span></div>`).join('')}</div></div>${DATA.directions.map(d=>['light','dark'].map(mode=>{const e=entry(p.id,d.id,mode);return `<div class="matrix-art" style="background:${e.colors.background}" aria-label="${esc(d.name)}, ${esc(p.name)}, ${mode} background">${e.horizontalSvg}</div>`;}).join('')).join('')}</div>`).join('');
}
document.addEventListener('click',event=>{ const p=event.target.closest('[data-palette]');const v=event.target.closest('[data-view]');const i=event.target.closest('[data-ink]');const k=event.target.closest('[data-dark-ink]'); if(p)selected=p.dataset.palette;if(v)view=v.dataset.view;if(i)ink=i.dataset.ink;if(k)darkInk=k.dataset.darkInk;if(p||v||i||k)detail(); });
if(new URLSearchParams(location.search).has('matrix'))document.documentElement.classList.add('exporting');
paletteButtons();detail();matrix();
"""


def build() -> Path:
    manifest = json.loads((ROOT / "exports/artwork.json").read_text())
    source = json.loads((ROOT / "source/palettes.json").read_text())
    data = {
        "palettes": source["palettes"],
        "directions": manifest["directions"],
        "entries": [],
    }
    for entry in manifest["entries"]:
        item = dict(entry)
        item["horizontalSvg"] = clean_svg(entry["horizontal"])
        item["compactSvg"] = clean_svg(entry["compact"])
        item["symbolHighContrastSvg"] = clean_svg(entry["symbolHighContrast"])
        item["horizontalNeutralSvg"] = item["horizontalSvg"].replace(entry["colors"]["symbol"], entry["colors"]["name"]) if entry["mode"] == "dark" else item["horizontalSvg"]
        data["entries"].append(item)
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><title>Tabernacle of Praise — Color Exploration 10</title><style>{STYLE}</style></head><body><main>
<div class="interactive-only">
<header><div class="eyebrow">Tabernacle of Praise / Color Exploration 10</div><span class="draft">DRAFT — NOT FOR PUBLICATION</span></header>
<div class="intro"><h1>Two marks.<br>Five color directions.</h1><p>Compare Shared Rhythm and Open Praise with the same geometry, lettering and proportions. Color is the next exploration; neither logo, palette nor typography is approved.</p></div>
<nav class="palette-picker" id="palettePicker" aria-label="Choose a color palette"></nav>
<section class="detail" aria-labelledby="paletteName"><div class="detail-heading"><div><h2 id="paletteName"></h2><p class="mood" id="paletteMood"></p></div><div class="toolbar"><div class="segmented" role="group" aria-label="Background comparison"><button data-view="light" type="button" aria-pressed="false">Light</button><button data-view="dark" type="button" aria-pressed="false">Dark</button><button data-view="both" type="button" aria-pressed="true">Both</button></div><div class="segmented" role="group" aria-label="Color or monochrome"><button data-ink="color" type="button" aria-pressed="true">Color</button><button data-ink="mono" type="button" aria-pressed="false">Monochrome</button></div><div class="segmented" role="group" aria-label="Dark symbol ink"><button data-dark-ink="accent" type="button" aria-pressed="true">Accent</button><button data-dark-ink="ivory" type="button" aria-pressed="false">Ivory reverse</button></div></div></div>
<div class="detail-grid" id="detailGrid"></div><p id="reverseNote" style="font-size:11px;color:var(--muted);margin-top:12px"></p><p id="selectionStatus" role="status" aria-live="polite" style="position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)"></p>
<div class="swatch-grid" id="swatches" aria-label="Exact palette colors"></div><div class="palette-notes"><p id="paletteNote"></p><p id="printNote"></p></div></section>
<aside class="exploration-note"><strong>What to judge:</strong> welcome, distinctiveness and lasting everyday use. Each symbol stays one solid ink; color cannot resolve an uncertain silhouette or make Open Praise’s proposed T/P reading automatic. Dark compact cuts use the light neutral for clearer small-size contrast. Gold and copper are flat screen colors. The official RCCG PNG is missing, so an actual emblem pairing is still untested.<br><strong>Next:</strong> shortlist two color families, refine the preferred combinations, then gather team feedback. This is exploration, with no approval inferred.</aside>
</div>
<section class="matrix-section" aria-labelledby="matrixTitle"><div class="interactive-only"><h2 id="matrixTitle">The comparison matrix</h2><p style="font-size:13px;color:var(--muted);margin-top:6px">All five families, with both concepts in the same light and dark conditions. Scroll horizontally on smaller screens.</p></div><div class="matrix-scroll"><div class="matrix-export" id="matrixExport"><div class="matrix-head"><div><div class="eyebrow">Color Exploration / 10</div><h2 style="margin-top:10px">Tabernacle of Praise<br>Five color directions</h2><p>Same drawings, lettering and proportions throughout. Light: primary ink on neutral. Dark: accent symbol and neutral name on primary.</p></div><div class="matrix-brand">TWO DEVELOPING IDENTITIES<br>NO LOGO, PALETTE OR TYPE APPROVAL<br><span class="draft" style="display:inline-block;margin-top:14px">DRAFT — NOT FOR PUBLICATION</span></div></div><div class="matrix-column-head"><div>PALETTE / HEX</div><div class="concept-group">Shared Rhythm<div class="surfaces"><span>Light</span><span>Dark</span></div></div><div class="concept-group">Open Praise<div class="surfaces"><span>Light</span><span>Dark</span></div></div></div><div id="matrixRows"></div><div class="matrix-foot"><p>The symbol remains one ink. Use primary on neutral for everyday text; pale gold and sand are supporting colors, never body copy on ivory. Values are screen explorations, not print or material specifications.</p><p>Shared Rhythm retains its architectural cadence; Open Praise’s proposed T/P reading still needs testing. Color cannot settle recognition. Gold is flat, not metallic. Original RCCG emblem absent: actual pairing untested.</p></div><div class="draft">DRAFT — NOT FOR PUBLICATION · COLOR DEVELOPMENT 10</div></div></div></section>
<p class="closing interactive-only">Working shortlist: deep teal for a contemporary, welcoming balance; navy for a dignified foundation. These are provisional recommendations for comparison. All marks and lettering remain the editable Development 09 drawings.</p>
</main><script>const DATA={payload};\n{SCRIPT}</script></body></html>"""
    output = ROOT / "exports/color-explorer.html"
    output.write_text(page)
    return output


def render(path: Path) -> dict:
    from playwright.sync_api import sync_playwright
    checks = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path="/usr/bin/chromium", args=["--no-sandbox", "--disable-dev-shm-usage"])
        page = browser.new_page(viewport={"width": 1280, "height": 1800}, device_scale_factor=2)
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.set_content(path.read_text(), wait_until="load")
        for palette in ("navy", "forest", "teal", "burgundy", "charcoal"):
            page.locator(f'[data-palette="{palette}"]').click()
            assert page.locator(f'[data-palette="{palette}"]').get_attribute("aria-pressed") == "true"
            assert page.locator("#detailGrid .concept-card").count() == 2
            colors = page.locator("#detailGrid .logo-art svg path").evaluate_all("nodes=>[...new Set(nodes.map(n=>n.getAttribute('fill')||getComputedStyle(n).fill))]")
            checks.append({"palette": palette, "conceptsVisible": 2, "renderedPathFills": colors})
        page.locator('[data-palette="navy"]').focus()
        page.keyboard.press("Enter")
        assert page.locator('[data-palette="navy"]').get_attribute("aria-pressed") == "true"
        checks.append({"keyboardSelection": "Enter on navy palette", "passed": True})
        page.locator('[data-palette="charcoal"]').click()
        for mode, count in (("light", 2), ("dark", 2), ("both", 4)):
            page.locator(f'[data-view="{mode}"]').click()
            assert page.locator("#detailGrid .logo-pane").count() == count
            checks.append({"backgroundMode": mode, "visiblePanes": count})
        page.locator('[data-dark-ink="ivory"]').click()
        neutral_fills = page.locator('#detailGrid .logo-pane[data-mode="dark"] .logo-art svg path').evaluate_all("nodes=>[...new Set(nodes.map(n=>n.getAttribute('fill')||getComputedStyle(n).fill))]")
        assert neutral_fills == ["#F5F0E8"], neutral_fills
        checks.append({"darkSymbolInk": "ivory", "bothLogosRenderedFills": neutral_fills})
        page.locator('[data-dark-ink="accent"]').click()
        page.locator('[data-ink="mono"]').click()
        mono_colors = page.locator("#detailGrid .logo-art svg path").evaluate_all("nodes=>[...new Set(nodes.map(n=>n.getAttribute('fill')||getComputedStyle(n).fill))]")
        assert all(color in {"#000", "#000000", "black", "#fff", "#ffffff", "#FFFFFF", "white", "rgb(0, 0, 0)", "rgb(255, 255, 255)"} for color in mono_colors), mono_colors
        checks.append({"inkMode": "mono", "renderedPathFills": mono_colors})
        page.locator('[data-ink="color"]').click()
        page.locator('[data-palette="teal"]').click()
        page.set_viewport_size({"width": 390, "height": 844})
        assert page.locator("#detailGrid .concept-card").count() == 2
        checks.append({"mobileViewport": [390, 844], "conceptsPresent": 2})
        page.set_viewport_size({"width": 1280, "height": 1800})
        page.evaluate("document.documentElement.classList.add('exporting')")
        assert page.locator(".matrix-row").count() == 5
        assert page.locator(".matrix-art").count() == 20
        page.locator("#matrixExport").screenshot(path=str(ROOT / "exports/palette-comparison.png"))
        assert not errors, errors
        browser.close()
    return {"status": "passed", "checks": checks, "javascriptErrors": errors, "portable": "All SVGs and interaction data embedded; no external network assets.", "render": "Chromium; 1200 CSS-pixel matrix at 2x"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-render", action="store_true")
    args = parser.parse_args()
    output = build()
    print(output.relative_to(ROOT))
    if not args.no_render:
        print(json.dumps(render(output), ensure_ascii=False, indent=2))
