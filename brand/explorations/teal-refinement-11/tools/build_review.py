#!/usr/bin/env python3
"""Build a concise draft review from the current teal refinement artwork.

Run only after exports/artwork.json has been assembled from frozen 11 sources.
The three application diagrams retain actual outlined master contours. The HTML
embeds every preview and the original font/license; no network is required.
"""
from __future__ import annotations

import base64
import copy
import hashlib
from html import escape
import importlib.util
import json
from pathlib import Path
import xml.etree.ElementTree as ET

import fitz
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'exports'
APPS = ROOT / 'applications'
PREVIOUS = ROOT.parent / 'identity-development-09'
FONT = PREVIOUS / 'type-study/fonts/instrumentsans/InstrumentSans[wdth,wght].ttf'
NS = 'http://www.w3.org/2000/svg'
DRAFT = 'DRAFT — NOT FOR PUBLICATION'
ET.register_namespace('', NS)


def helper_module():
    spec = importlib.util.spec_from_file_location('review09_diagram_helpers', PREVIOUS / 'applications/build.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def uri(path):
    mime = 'image/svg+xml' if path.suffix == '.svg' else 'image/png'
    return f'data:{mime};base64,' + base64.b64encode(path.read_bytes()).decode()


def colored_svg(path, ink, background=None):
    """Change ink only; leave master path data and transforms untouched."""
    art = ET.parse(path).getroot()
    for child in list(art):
        if child.tag.rsplit('}', 1)[-1] in ('title', 'desc', 'rect'):
            art.remove(child)
    for item in art.iter():
        if item.tag.rsplit('}', 1)[-1] in ('path', 'polygon', 'polyline'):
            item.set('fill', ink)
    if background:
        a, b, w, h = art.get('viewBox').split()
        art.insert(0, ET.Element(f'{{{NS}}}rect', {'x':a, 'y':b, 'width':w, 'height':h, 'fill':background}))
    return art


def preview_uri(path, ink, background=None):
    return 'data:image/svg+xml;base64,' + base64.b64encode(ET.tostring(colored_svg(path, ink, background))).decode()


def embed(parent, art, x, y, w, h):
    nested = copy.deepcopy(art)
    nested.set('x', str(x)); nested.set('y', str(y))
    nested.set('width', str(w)); nested.set('height', str(h))
    nested.set('preserveAspectRatio', 'xMidYMid meet')
    parent.append(nested)


def applications(data, palette):
    h = helper_module()
    labels = h.OutlinedLabels()
    APPS.mkdir(exist_ok=True)
    records = []
    teal, ivory, sand, gold = (palette[k] for k in ('primary', 'neutral', 'secondary', 'accent'))
    for d in data['directions']:
        slug = d['id']; name = d['name']
        primary = ROOT / d['primaryFile']
        single = ROOT / d['lockups']['singleLine']
        horizontal = ROOT / d['lockups']['horizontal']
        rec = {'id':slug, 'name':name, 'sources':{}}
        for key, source in [('primary', primary), ('singleLine', single), ('horizontal', horizontal)]:
            rec['sources'][key] = {'file':source.relative_to(ROOT).as_posix(), 'sha256':hashlib.sha256(source.read_bytes()).hexdigest()}
        # A header proportion study, not a complete website or fabricated parish page.
        svg = h.canvas(1000, 210, f'{name} / single-line header study', DRAFT + '. Imagined header proportion study using the current full-name master.')
        h.rect(svg, 0, 0, 1000, 210, ivory)
        h.line(svg, 0, 16, 1000, 16, gold, 3)
        embed(svg, colored_svg(single, teal), 34, 34, 760, 120)
        h.line(svg, 34, 165, 966, 165, sand, 1)
        labels.draw(svg, 'SINGLE-LINE HEADER / FULL NAME', 34, 193, 14, fill=teal, track=.6)
        labels.draw(svg, 'DRAFT', 966, 193, 14, fill=teal, align='right', track=.6)
        target = APPS / f'{slug}-header.svg'; h.write_svg(target, svg); rec['header'] = target.relative_to(ROOT).as_posix()
        # The entrance stays a clearly labeled diagram with no actual building claim.
        svg = h.canvas(1000, 480, f'{name} / entrance proportion study', DRAFT + '. Imagined entrance, not actual church premises or fabrication artwork.')
        h.rect(svg, 0, 0, 1000, 480, ivory)
        h.rect(svg, 35, 54, 930, 355, ivory, stroke=sand, sw=1)
        h.line(svg, 35, 55, 965, 55, gold, 4)
        h.rect(svg, 72, 100, 210, 309, teal)
        h.rect(svg, 86, 114, 182, 295, ivory)
        h.line(svg, 177, 114, 177, 409, sand, 1)
        h.line(svg, 247, 245, 247, 308, teal, 2)
        embed(svg, colored_svg(horizontal, teal), 343, 121, 561, 210)
        labels.draw(svg, 'RCCG · ISTANBUL, TÜRKİYE', 364, 346, 14, fill=teal, track=.7)
        labels.draw(svg, 'IMAGINED ENTRANCE / PROPORTION STUDY', 35, 451, 14, fill=teal, track=.5)
        labels.draw(svg, 'DRAFT', 965, 451, 14, fill=teal, align='right', track=.6)
        target = APPS / f'{slug}-entrance.svg'; h.write_svg(target, svg); rec['entrance'] = target.relative_to(ROOT).as_posix()
        # Normal avatar uses primary geometry, never an enlarged compact cut.
        svg = h.canvas(1000, 260, f'{name} / primary avatar study', DRAFT + '. Primary symbol in a circular profile context; church handle is an explicit placeholder.')
        h.rect(svg, 0, 0, 1000, 260, ivory)
        h.node('circle', {'cx':137, 'cy':119, 'r':94, 'fill':teal}, svg)
        embed(svg, colored_svg(primary, ivory), 67, 49, 140, 140)
        embed(svg, colored_svg(horizontal, teal), 282, 27, 623, 164)
        labels.draw(svg, '[CHURCH HANDLE]', 304, 217, 17, fill=teal, track=.3)
        labels.draw(svg, 'PRIMARY SYMBOL', 137, 242, 13, fill=teal, align='center', track=.6)
        target = APPS / f'{slug}-avatar.svg'; h.write_svg(target, svg); rec['avatar'] = target.relative_to(ROOT).as_posix()
        records.append(rec)
    manifest = {'status':DRAFT, 'approval':False, 'conditions':'Both directions use identical header, entrance and primary-avatar proportion diagrams. Exact master paths retained, with working teal/ivory ink only.', 'limitations':'Imagined diagrams, not actual premises or an official website/profile. No RCCG emblem is present. [CHURCH HANDLE] is a placeholder.', 'directions':records}
    (APPS / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n')
    return records


def header(title, subtitle, number):
    return (f'<header><div class="eyebrow"><span>RCCG TABERNACLE OF PRAISE · ISTANBUL</span><span>TEAL REFINEMENT 11 / 0{number}</span></div>'
            f'<h1>{escape(title)}</h1><p class="subtitle">{escape(subtitle)}</p></header>')


def footer(number):
    return f'<footer><strong>{DRAFT}</strong><span>Working palette selected. Final logo and brand system remain open.</span><span>{number} / 3</span></footer>'


def review_source(data, palette, contexts):
    teal, ivory, sand, gold = (palette[k] for k in ('primary', 'neutral', 'secondary', 'accent'))
    meanings = {
        'shared-rhythm':('Gathering space + collective rhythm', 'Four unequal folded faces hold an open shared space. Their changing heights suggest people responding together in praise.', 'The favored main shape is preserved. The name has closer line spacing and a new single-line arrangement.', 'The architectural reading remains abstract; the complete parish name supplies clear context.'),
        'open-praise':('Tabernacle + Praise through negative space', 'A P-like outer contour holds an open T-shaped interior, bringing the two initials into one compact gesture.', 'The inner crossbar now meets the stem at one level; the outer silhouette is preserved.', 'The T is still a reading to test. Color and geometric alignment do not guarantee recognition.'),
    }
    columns=[]
    for idx,d in enumerate(data['directions'],1):
        idea,meaning,change,risk=meanings[d['id']]
        columns.append(f'<article class="option"><div class="option-heading"><span>0{idx}</span><div><h2>{escape(d["name"])}</h2><p>{escape(idea)}</p></div></div>'
                       f'<div class="hero light"><img src="{preview_uri(ROOT/d["lockups"]["stacked"],teal,ivory)}" alt="{d["name"]}, complete parish name"></div>'
                       f'<div class="reverse"><img src="{preview_uri(ROOT/d["lockups"]["horizontal"],ivory,teal)}" alt="{d["name"]}, ivory reverse"></div>'
                       f'<p class="meaning">{escape(meaning)}</p><p class="change"><b>Refined:</b> {escape(change)}</p><p class="risk">{escape(risk)}</p></article>')
    swatches=''.join(f'<div><i style="background:{palette[key]}"></i><span>{key.title()}</span><code>{palette[key]}</code></div>' for key in ('primary','secondary','accent','neutral'))
    page1='<section class="sheet" id="overview">'+header('Two directions, in one working palette','Shared Rhythm and Open Praise · teal + sand · complete-name arrangements',1)+'<main class="options">'+''.join(columns)+'</main><div class="palette-strip">'+swatches+'</div><p class="palette-note">Preferred dark treatment: ivory mark and name on teal. Soft gold stays a restrained layout accent.</p>'+footer(1)+'</section>'
    appcols=[]
    for rec in contexts:
        appcols.append(f'<article class="context"><h2>{escape(rec["name"])}</h2><div class="context-block"><h3>01 / Single-line header</h3><img class="header-context" src="{uri(ROOT/rec["header"])}" alt="{rec["name"]} header"></div><div class="context-block"><h3>02 / Entrance proportion</h3><img class="sign-context" src="{uri(ROOT/rec["entrance"])}" alt="{rec["name"]} imagined entrance"></div><div class="context-block"><h3>03 / Primary avatar</h3><img class="avatar-context" src="{uri(ROOT/rec["avatar"])}" alt="{rec["name"]} primary avatar"></div></article>')
    page2='<section class="sheet" id="applications">'+header('A clearer name across everyday uses','The new single-line arrangement joins the stacked and two-line horizontal versions.',2)+'<main class="context-grid">'+''.join(appcols)+'</main><p class="context-note">Identical illustrative conditions for both options. Entrance is imagined; the profile handle is a placeholder. Primary symbol geometry is used for these normal-size avatars.</p>'+footer(2)+'</section>'
    open_board=ROOT/'open-praise/renders/counter-comparison.png'
    type_board=ROOT/'lettering/lettering-refinement.png'
    page3='<section class="sheet" id="refinements">'+header('Small changes, with a practical purpose','Preserved comparisons make this refinement pass reviewable.',3)+'<main class="refinement-grid"><article><h2>Open Praise / counter</h2><img class="diagnostic" src="'+uri(open_board)+'" alt="Open Praise counter comparisons"><p>The baseline and trials remain available. The chosen contour is tested against the former crossbar; the outer P and open lower exit remain intact. T/P recognition still needs audience feedback.</p></article><article><h2>Full-name lettering</h2><img class="diagnostic" src="'+uri(type_board)+'" alt="Full-name spacing and arrangement comparisons"><p>Instrument Sans title case remains the working companion. Optical spacing and line leading are adjusted; all words retain equal size and weight. The single-line name is a new practical arrangement.</p></article></main><div class="next-grid"><article><h3>Actual-size proof supplied</h3><p>Use the separate A4 vector sheet at 100% / actual size, then check its 50 mm ruler. Physical printing and material performance have not been verified here.</p></article><article><h3>RCCG pairing remains open</h3><p>The original supplied emblem PNG is still absent. No emblem is recreated and no actual two-logo pairing is claimed.</p></article><article><h3>Two options remain in development</h3><p>Team feedback comes later. These drafts record the working direction; they do not establish final identity or production standards.</p></article></div><p class="diagnostic-note">Diagnostic boards are scaled to fit this review. Native screen renders and the separate calibrated print sheet provide the appropriate size checks.</p>'+footer(3)+'</section>'
    font=base64.b64encode(FONT.read_bytes()).decode()
    license_text=FONT.with_name('OFL.txt').read_text()
    assert '</script' not in license_text.lower()
    font_license='<script type="text/plain" id="embedded-font-license" data-font="Instrument Sans" data-source-font="'+escape(FONT.name,quote=True)+'">'+license_text+'</script>'
    css='''
@font-face{font-family:Review;src:url(data:font/ttf;base64,FONTDATA);font-weight:100 900;font-stretch:75% 100%;font-display:block}
*{box-sizing:border-box}html,body{margin:0;padding:0;background:#e4e6e2;color:TEAL;font-family:Review,Arial,sans-serif;font-weight:450}h1,h2,h3,p{margin:0}.sheet{position:relative;width:1122px;height:794px;padding:29px 42px 46px;background:IVORY;overflow:hidden;page-break-after:always}.sheet:last-child{page-break-after:auto}.eyebrow{display:flex;justify-content:space-between;font-size:10px;letter-spacing:1px;color:#56645f;font-weight:550}h1{font-size:34px;font-weight:550;line-height:1.1;letter-spacing:-.7px;margin-top:20px}.subtitle{font-size:13px;line-height:1.4;color:#5a6761;margin-top:9px}.options{display:grid;grid-template-columns:1fr 1fr;gap:32px;margin-top:23px}.option{border-top:1px solid SAND;padding-top:13px}.option-heading{display:flex;gap:13px;align-items:baseline}.option-heading>span{font-size:11px;color:#727c74}.option-heading h2{font-size:23px;font-weight:550;line-height:1.1}.option-heading p{font-size:11px;color:#657069;margin-top:4px}.hero{margin-top:14px;height:226px;display:flex;align-items:center;justify-content:center}.hero img{height:100%;max-width:100%;display:block}.reverse{height:103px;background:TEAL;display:flex;justify-content:center;align-items:center;margin-top:11px}.reverse img{height:100%;width:89%;display:block}.meaning{font-size:12px;line-height:1.5;margin-top:13px;max-width:485px}.change{font-size:11px;line-height:1.45;margin-top:8px;color:#5a665e}.change b{font-weight:600}.risk{font-size:10px;line-height:1.5;margin-top:7px;color:#647168}.palette-strip{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:17px}.palette-strip>div{display:grid;grid-template-columns:35px 1fr;column-gap:9px;align-items:center}.palette-strip i{height:28px;grid-row:span 2;border:1px solid #23382d22}.palette-strip span{font-size:9px;color:#66716a}.palette-strip code{font-family:Review,Arial,sans-serif;font-size:10px;letter-spacing:.3px}.palette-note{font-size:10px;margin-top:10px;color:#5d6c62}.context-grid{display:grid;grid-template-columns:1fr 1fr;gap:32px;margin-top:23px}.context h2{font-size:19px;font-weight:550;border-top:1px solid SAND;padding-top:13px;margin-bottom:14px}.context h3{font-size:10px;text-transform:uppercase;letter-spacing:.65px;font-weight:500;color:#647168;margin:5px 0}.context-block img{width:100%;object-fit:contain;display:block}.header-context{height:95px}.sign-context{height:231px}.avatar-context{height:119px}.context-note{font-size:10px;color:#647168;line-height:1.45;max-width:960px;margin-top:16px}.refinement-grid{display:grid;grid-template-columns:1fr 1fr;gap:32px;margin-top:24px}.refinement-grid h2{font-size:19px;font-weight:550;border-top:1px solid SAND;padding-top:13px}.diagnostic{width:100%;height:315px;object-fit:contain;display:block;margin-top:12px;background:#fff}.refinement-grid p{font-size:11px;color:#5c6a60;line-height:1.55;margin-top:12px}.next-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:23px;margin-top:25px;padding-top:17px;border-top:1px solid SAND}.next-grid h3{font-size:12px;font-weight:600}.next-grid p{font-size:10px;line-height:1.55;color:#647168;margin-top:7px}.diagnostic-note{font-size:9px;color:#68746b;margin-top:16px}footer{position:absolute;left:42px;right:42px;bottom:20px;display:flex;justify-content:space-between;gap:20px;border-top:1px solid #b8c4ba;padding-top:10px;font-size:9px;color:#647168}footer strong{font-weight:650;color:TEAL;letter-spacing:.3px}footer span:last-child{white-space:nowrap}@page{size:297mm 210mm;margin:0}@media print{html,body{background:IVORY;print-color-adjust:exact;-webkit-print-color-adjust:exact}.sheet{width:297mm;height:210mm}}
'''.replace('FONTDATA',font).replace('TEAL',teal).replace('IVORY',ivory).replace('SAND',sand)
    return '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Tabernacle of Praise / Teal Refinement 11 / DRAFT</title>'+font_license+'<style>'+css+'</style><body>'+page1+page2+page3+'</body></html>'


def main():
    OUT.mkdir(exist_ok=True)
    data=json.loads((OUT/'artwork.json').read_text())
    palette=data.get('workingPalette') or json.loads((ROOT/'source/working-palette.json').read_text())
    contexts=applications(data,palette)
    source=review_source(data,palette,contexts)
    (OUT/'review-source.html').write_text(source)
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
        page=browser.new_page(viewport={'width':1200,'height':1000},device_scale_factor=2)
        page.set_content(source,wait_until='load');page.evaluate('document.fonts.ready')
        result=page.evaluate('''()=>({brokenImages:[...document.images].filter(x=>!x.complete||!x.naturalWidth).length,sheets:[...document.querySelectorAll('.sheet')].map(s=>{const f=s.querySelector('footer').getBoundingClientRect(),r=s.getBoundingClientRect();return{id:s.id,lastContentBottom:Math.max(...[...s.children].filter(x=>x.tagName!=='FOOTER').map(x=>x.getBoundingClientRect().bottom))-r.top,footerTop:f.top-r.top}})})''')
        assert result['brokenImages']==0,result
        assert all(s['lastContentBottom']<s['footerTop']-6 for s in result['sheets']),result
        page.locator('#overview').screenshot(path=str(OUT/'two-options-teal.png'),animations='disabled')
        for ident in ('applications','refinements'):
            page.locator('#'+ident).screenshot(path='/tmp/teal11-review-'+ident+'.png',animations='disabled')
        page.pdf(path=str(OUT/'two-option-review-11.pdf'),prefer_css_page_size=True,print_background=True,display_header_footer=False)
        browser.close()
    with fitz.open(OUT/'two-option-review-11.pdf') as doc:
        assert len(doc)==3,len(doc)
        assert all('DRAFT' in page.get_text() for page in doc)
    result.update(status=DRAFT,pdfPages=3,metadataSHA256=hashlib.sha256((OUT/'artwork.json').read_bytes()).hexdigest(),limitations='Draft review only. No physical print result, RCCG pairing, audience recognition or final approval is claimed.')
    (OUT/'review-checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
