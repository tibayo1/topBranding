#!/usr/bin/env python3
"""Build draft RCCG/parish pairings without altering either source identity."""
from __future__ import annotations
from pathlib import Path
from copy import deepcopy
from html import escape
import argparse,base64,hashlib,json,zipfile,xml.etree.ElementTree as ET
import fitz
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parents[2]
PREVIOUS=ROOT.parent/'teal-refinement-11'
OUT=ROOT/'exports'
NS='http://www.w3.org/2000/svg'
ET.register_namespace('',NS)
DRAFT='DRAFT — NOT FOR PUBLICATION'
DEFAULT_ASSET=REPO/'brand/assets/rccg-emblem/references/rccg-wayforward-reference.png'
FALLBACK=Path('/tmp/rccg-source-candidates/wayforward-embedded.png')
SOURCE_COMMIT='b053a99345e9178e23db06ac35b9529006684480'
SOURCE_URL=f'https://github.com/RCCG-WayForwardProject/rccg-wayforward/blob/{SOURCE_COMMIT}/public/logo.svg'


def uri(path):
    mime='image/svg+xml' if path.suffix=='.svg' else 'image/png'
    return f'data:{mime};base64,'+base64.b64encode(path.read_bytes()).decode()


def make_pair(direction,mode,asset):
    relative=direction['lockups']['horizontalReverse' if mode=='dark' else 'horizontal']
    source=PREVIOUS/relative
    art=ET.parse(source).getroot()
    # The parish presentation rectangle is changed to the pairing surface only.
    # All parish paths and their transforms remain exactly as in refinement 11.
    for child in list(art):
        if child.tag.rsplit('}',1)[-1] in ('title','desc','rect'):art.remove(child)
    parish=''.join(ET.tostring(child,encoding='unicode') for child in art)
    background='#10494C' if mode=='dark' else '#FFFFFF'
    white_panel='<rect x="24" y="54" width="192" height="192" fill="#FFFFFF"/>' if mode=='dark' else ''
    image=f'<image x="40" y="70" width="160" height="160" preserveAspectRatio="xMidYMid meet" href="{uri(asset)}"/>'
    body=f'<rect width="960" height="300" fill="{background}"/>'+white_panel+image+f'<g transform="translate(230 22)">{parish}</g>'
    title=f'{direction["name"]} with separate RCCG reference emblem / {mode}'
    return (f'<svg xmlns="{NS}" viewBox="0 0 960 300" role="img" aria-label="{escape(title)}">'
            f'<title>{escape(title)} — DRAFT</title><desc>{DRAFT}. Existing reference copy from an RCCG parish website repository, not the original chat-uploaded file. Emblem PNG bytes, full image, colors and proportions are unchanged. Parish path geometry is unchanged. This is an internal pairing test, not a final approved lockup.</desc>'+body+'</svg>\n'),source


def html_source(records,asset):
    columns=[]
    for slug,name in [('shared-rhythm','Shared Rhythm'),('open-praise','Open Praise')]:
        rows=[]
        for mode in ['light','dark']:
            record=next(r for r in records if r['id']==slug and r['mode']==mode)
            rows.append(f'<div class="surface-label">{mode.title()} background</div><img class="pair" src="{uri(ROOT/record["file"])}" alt="{escape(name)} / {mode} / separate RCCG reference emblem">')
        columns.append(f'<article><h2>{name}</h2>'+''.join(rows)+'</article>')
    source_image=uri(asset)
    return '''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>RCCG + Tabernacle of Praise / draft pairing12</title><style>
*{box-sizing:border-box}body{margin:0;background:#eee;color:#163d3e;font-family:Arial,Helvetica,sans-serif}h1,h2,p{margin:0}.sheet{width:1122px;height:794px;background:#f8f7f3;padding:34px 42px 48px;position:relative;overflow:hidden;page-break-after:always}.eyebrow{display:flex;justify-content:space-between;font-size:10px;letter-spacing:1.1px;color:#586765}h1{font-size:33px;line-height:1.1;font-weight:500;letter-spacing:-.5px;margin-top:21px}.sub{font-size:13px;line-height:1.45;color:#62706c;margin-top:10px}.columns{display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-top:28px}h2{font-size:21px;font-weight:500;border-top:1px solid #bac7c0;padding-top:14px;margin-bottom:17px}.surface-label{font-size:10px;color:#65746b;margin-bottom:7px;margin-top:14px}.pair{width:100%;height:auto;display:block;border:1px solid #d9dfd9}.note{font-size:11px;line-height:1.55;color:#596863;margin-top:21px;max-width:970px}.notes{margin-top:30px;display:grid;grid-template-columns:290px 1fr;gap:34px}.emblem{width:236px;height:236px;display:block;background:white;border:1px solid #d7ddd7;padding:0}.notes h2{margin-bottom:12px}.notes p{font-size:13px;line-height:1.65;color:#4a5d57;margin-bottom:15px}.source{font-size:10px!important;line-height:1.5!important;overflow-wrap:anywhere;color:#69756f!important}.detail{margin-top:22px;border-top:1px solid #bcc9bf;padding-top:15px}.detail p{font-size:12px;line-height:1.6;margin-top:10px;color:#52645b}footer{position:absolute;left:42px;right:42px;bottom:20px;border-top:1px solid #bec9bf;padding-top:10px;display:flex;justify-content:space-between;gap:20px;font-size:9px;color:#60706a}footer strong{color:#163d3e}@page{size:297mm 210mm;margin:0}@media print{body{background:white;print-color-adjust:exact;-webkit-print-color-adjust:exact}.sheet{width:297mm;height:210mm}}
</style></head><body><section class="sheet" id="comparison"><header><div class="eyebrow"><span>RCCG TABERNACLE OF PRAISE · ISTANBUL</span><span>PAIRING STUDY 12</span></div><h1>Two parish options, alongside RCCG</h1><p class="sub">A practical draft using an existing emblem reference · teal + sand working parish palette</p></header><div class="columns">'''+''.join(columns)+'''</div><p class="note">The complete emblem stays separate and keeps its original colors. White light surfaces and a padded white panel on teal preserve the full source image. The parish contours, full name and 93% Open Praise optical scale stay unchanged.</p><footer><strong>DRAFT — NOT FOR PUBLICATION</strong><span>Reference copy from a parish repository; original chat-file integrity and production approval remain open.</span><span>1 / 2</span></footer></section><section class="sheet" id="source"><header><div class="eyebrow"><span>REFERENCE FILE + REVIEW NOTES</span><span>PAIRING STUDY 12</span></div><h1>The emblem file is included in the ZIP</h1><p class="sub">Existing PNG preserved byte-for-byte. No redraw, tracing, recoloring, crop or background removal.</p></header><div class="notes"><div><img class="emblem" src="'''+source_image+'''" alt="Full existing 236 pixel RCCG reference PNG, on white"><p class="source" style="margin-top:12px">Native 236×236 PNG reference. Source resolution limits large print use.</p></div><div><h2>What this preview establishes</h2><p>Shared Rhythm's open, angular planes balance the denser circular seal. Open Praise offers a compact alternative; its smaller optical scale helps the two identities stay independent.</p><p>The teal parish ink can sit beside the emblem's full color without borrowing or changing the parent colors. Gold is omitted from these formal pairings.</p><h2 style="margin-top:23px">What remains open</h2><p>This is a sourced reference copy, rather than the exact 1200×1200 image shown in chat. The original upload's checksum is not verified. Final authorized source artwork, ring-letter readability at small sizes, physical print reproduction and final lockup approval remain open.</p><p class="source">Reference source: '''+escape(SOURCE_URL)+'''<br>PNG extracted unchanged from the source SVG's embedded image; reference-source SHA and package hashes are recorded in the manifest.</p></div></div><div class="detail"><p>The ZIP contains the standalone PNG, four self-contained paired SVGs, this review PDF and the comparison PNG. The reference raster remains at its native dimensions; the previews do not create a higher-resolution emblem.</p><p>To rebuild, run source/build.py from the repository with the recorded reference asset and frozen refinement 11 masters available. No image-generation tool or external font is needed.</p></div><footer><strong>DRAFT — NOT FOR PUBLICATION</strong><span>Internal review only. No official source authorization, legal clearance or final brand approval is claimed.</span><span>2 / 2</span></footer></section></body></html>'''


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--asset',type=Path);args=parser.parse_args()
    asset=args.asset or (DEFAULT_ASSET if DEFAULT_ASSET.exists() else FALLBACK)
    if not asset.exists():raise SystemExit('Unchanged source emblem file is required.')
    OUT.mkdir(parents=True,exist_ok=True)
    data=json.loads((PREVIOUS/'exports/artwork.json').read_text())
    records=[]
    for direction in data['directions']:
        for mode in ['light','dark']:
            raw,source=make_pair(direction,mode,asset)
            name=f'{direction["id"]}-{mode}-pairing-DRAFT.svg'
            file=OUT/name;file.write_text(raw)
            records.append({'id':direction['id'],'name':direction['name'],'mode':mode,'file':'exports/'+name,'parishSource':str(source.relative_to(REPO)),'parishSHA256':hashlib.sha256(source.read_bytes()).hexdigest()})
    source=html_source(records,asset);(OUT/'pairing-source.html').write_text(source)
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
        page=browser.new_page(viewport={'width':1200,'height':900},device_scale_factor=2)
        page.set_content(source,wait_until='load')
        broken=page.evaluate('[...document.images].filter(i=>!i.complete||!i.naturalWidth).length');assert not broken
        page.locator('#comparison').screenshot(path=str(OUT/'paired-comparison.png'))
        page.pdf(path=str(OUT/'pairing-review-12.pdf'),prefer_css_page_size=True,print_background=True)
        browser.close()
    with fitz.open(OUT/'pairing-review-12.pdf') as pdf:assert len(pdf)==2
    expected=asset.read_bytes()
    for rec in records:
        root=ET.parse(ROOT/rec['file']).getroot()
        image=next(root.iter('{'+NS+'}image'))
        embedded=base64.b64decode(image.get('href').split(',',1)[1]);assert embedded==expected
    image=Image.open(asset)
    manifest={'status':DRAFT,'finalApproval':False,'emblem':{'sourcePage':SOURCE_URL,'sourceCommit':SOURCE_COMMIT,'file':str(asset.relative_to(REPO)) if asset.is_relative_to(REPO) else str(asset),'sha256':hashlib.sha256(expected).hexdigest(),'dimensions':list(image.size),'bytes':len(expected),'originalChatUploadVerified':False,'productionAssetAuthorized':False,'handling':'Existing PNG extracted from source SVG, embedded unchanged with full image/colors/proportions. No background removal, crop, tracing or regeneration.'},'entries':records,'checks':{'embeddedPNGBytesMatchSource':True,'brokenHTMLImages':broken,'pdfPages':2,'parishGeometry':'All source paths/transforms preserved; only parish presentation rectangle replaced by pairing surface.'}}
    (OUT/'pairing-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    package=OUT/'RCCG-and-Tabernacle-of-Praise-DRAFT.zip'
    readme='RCCG + Tabernacle of Praise — DRAFT REFERENCE PACKAGE\n\nThis PNG is an existing reference copy from an RCCG parish website repository. It is not a regenerated emblem and is not claimed to be the original image uploaded in chat.\n\nSource: '+SOURCE_URL+'\nPNG SHA256: '+hashlib.sha256(expected).hexdigest()+'\nNative size: '+str(image.size)+'\n\nNo publication, official production authorization or final lockup approval is implied. Keep the entire emblem unaltered and separate from the parish identity.\n'
    with zipfile.ZipFile(package,'w',zipfile.ZIP_DEFLATED) as z:
        z.writestr('RCCG-emblem-reference.png',expected)
        z.writestr('README.txt',readme)
        for item in ['README.md','provenance.json']:
            sibling=asset.parent/item
            if sibling.exists():z.write(sibling,'reference-source/'+item)
        for rec in records:z.write(ROOT/rec['file'],Path(rec['file']).name)
        for name in ['paired-comparison.png','pairing-review-12.pdf','pairing-manifest.json']:z.write(OUT/name,name)
    with zipfile.ZipFile(package) as z:
        assert z.testzip() is None
        assert z.read('RCCG-emblem-reference.png')==expected
    print('Built 4 paired SVGs, comparison PNG, 2 page PDF and ZIP; emblem bytes preserved. Asset:',asset)

if __name__=='__main__':main()
