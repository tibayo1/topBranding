#!/usr/bin/env python3
"""Render editable, deterministic paired draft logo motion; no generative service."""
from __future__ import annotations
import base64
from copy import deepcopy
import hashlib
from io import BytesIO
import json
import math
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFont
from scipy.ndimage import label
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
REPO = HERE.parents[3]
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
SCENE = json.loads((HERE / 'scene.json').read_text())
FONT = REPO / 'brand/explorations/identity-development-09/type-study/fonts/instrumentsans/InstrumentSans[wdth,wght].ttf'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def datauri(path):
    return 'data:image/png;base64,' + base64.b64encode(path.read_bytes()).decode()

def tag(name):
    return f'{{{NS}}}{name}'

def scene_svg(direction, fmt):
    root = ET.Element(tag('svg'), {'viewBox': f"0 0 {fmt['width']} {fmt['height']}", 'width': str(fmt['width']), 'height': str(fmt['height']), 'role': 'img'})
    ET.SubElement(root, tag('title')).text = direction['name'] + ' with separate RCCG emblem — DRAFT'
    ET.SubElement(root, tag('desc')).text = 'DRAFT — NOT FOR PUBLICATION. Existing unmodified parish-source RCCG reference, not an approved production master. Parish name below symbol. No Google generation.'
    ET.SubElement(root, tag('rect'), {'width': str(fmt['width']), 'height': str(fmt['height']), 'fill': SCENE['background']})
    pair = ET.SubElement(root, tag('g'), {'data-part': 'pairing', 'transform': f"translate({fmt['x']} {fmt['y']}) scale({fmt['scale']})"})
    source = ET.parse(REPO / direction['source']).getroot()
    for child in source:
        if child.tag not in (tag('title'), tag('desc')):
            pair.append(deepcopy(child))
    for text, x, anchor in [('DRAFT — NOT FOR PUBLICATION', 54 if fmt['width']==1080 else 72, 'start'), (direction['name'], fmt['width']-(54 if fmt['width']==1080 else 72), 'end')]:
        node = ET.SubElement(root, tag('text'), {'x': str(x), 'y': '1014', 'fill': SCENE['parishColor'], 'font-family': 'Arial, sans-serif', 'font-size': '17' if fmt['width']==1080 else '18', 'text-anchor': anchor, 'data-part': 'editorial-footer'})
        node.text = text
    # Preserve exact PNG payload and all parish symbol/name contours.
    sourcepaths = [p.get('d') for p in source.iter(tag('path'))]
    assert [p.get('d') for p in root.iter(tag('path'))] == sourcepaths
    image = next(root.iter(tag('image')))
    href = image.get('href') or image.get('{http://www.w3.org/1999/xlink}href')
    assert base64.b64decode(href.split(',')[1]) == (REPO / SCENE['emblemSource']).read_bytes()
    assert len([p for p in root.iter(tag('path')) if p.get('data-letter')]) == 18
    return root

def motion_svg(root):
    moving = deepcopy(root)
    pair = next(p for p in moving if p.get('data-part') == 'pairing')
    parish = next(p for p in pair if p.tag == tag('g'))
    symbol = next(p for p in parish if p.get('data-part') == 'symbol')
    for node in list(moving):
        if node is not pair: moving.remove(node)
    for node in list(pair):
        if node is not parish: pair.remove(node)
    for node in list(parish):
        if node is not symbol: parish.remove(node)
    for index, node in enumerate(symbol.iter(tag('path'))):
        node.set('data-motion-plane', str(index))
    return ET.tostring(moving, encoding='unicode')

SCRIPT = r'''
const canvas=document.getElementById('stage'),ctx=canvas.getContext('2d');
const images={};
function load(src){return new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>resolve(im);im.onerror=reject;im.src=src})}
const ready=Promise.all(Object.entries(DATA).map(async([key,d])=>{images[key]=await load(d.endImage)}));
function offsetsFor(d,t){
 const values=d.offsets.map((v,i)=>{const u=Math.max(0,Math.min(1,(t-d.delays[i])/d.riseDuration));const c=.75;const eased=1+(c+1)*Math.pow(u-1,3)+c*Math.pow(u-1,2);return t>=6?0:v*(1-eased)});
 if(d.id==='shared-rhythm') values[1]=Math.min(values[1],values[0]+4);
 return values;
}
async function drawFrame(slug,format,t){
 await ready;const key=slug+'/'+format,d=DATA[key];
 if(canvas.width!==d.width||canvas.height!==d.height){canvas.width=d.width;canvas.height=d.height}
 ctx.drawImage(images[key],0,0);
 const offsets=offsetsFor(d,t);
 if(t>=6||offsets.every(v=>Math.abs(v)<1e-8))return;
 const doc=new DOMParser().parseFromString(d.symbolSvg,'image/svg+xml');
 doc.querySelectorAll('[data-motion-plane]').forEach((p,i)=>p.setAttribute('transform',`translate(0 ${offsets[i]})`));
 const raw=new XMLSerializer().serializeToString(doc);
 const moved=await load('data:image/svg+xml;base64,'+btoa(unescape(encodeURIComponent(raw))));
 ctx.fillStyle='#10494C';ctx.fillRect(...d.symbolErase);
 ctx.drawImage(moved,0,0);
}
window.renderFrame=async(slug,format,t)=>{await drawFrame(slug,format,t);return canvas.toDataURL('image/png').split(',')[1]};
window.motionOffsets=(slug,format,t)=>offsetsFor(DATA[slug+'/'+format],t);
let slug='shared-rhythm',format='landscape',playing=false,token=0;
const reduce=document.getElementById('reduce');reduce.checked=matchMedia('(prefers-reduced-motion: reduce)').matches;
async function reset(){playing=false;token++;document.getElementById('play').textContent='Play';document.getElementById('clock').textContent=reduce.checked?'Still preview':'0.0 / 10.0s';await drawFrame(slug,format,reduce.checked?10:0)}
document.getElementById('direction').onchange=async e=>{slug=e.target.value;await reset()};
document.getElementById('format').onchange=async e=>{format=e.target.value;await reset()};reduce.onchange=reset;
document.getElementById('play').onclick=async()=>{
 if(reduce.checked){await reset();return}
 const current=++token;playing=true;const started=performance.now();document.getElementById('play').textContent='Playing';
 async function tick(now){if(!playing||current!==token)return;const t=Math.min(10,(now-started)/1000);await drawFrame(slug,format,t);if(current!==token)return;document.getElementById('clock').textContent=t.toFixed(1)+' / 10.0s';if(t<10)requestAnimationFrame(tick);else{playing=false;document.getElementById('play').textContent='Replay'}}
 requestAnimationFrame(tick);
};
ready.then(reset);
'''

def html_source(data):
    payload = json.dumps(data, ensure_ascii=False).replace('</', '<\\/')
    return '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Tabernacle of Praise — RCCG motion graphics review</title><style>
body{margin:0;background:#eae8e1;color:#10494c;font:16px/1.6 Arial,sans-serif}main{max-width:1120px;margin:28px auto;padding:0 20px 30px}h1{font-size:28px;line-height:1.2;margin:0 0 14px}p{max-width:840px}.controls{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin:18px 0}button,select{font:inherit;padding:7px 12px;border:1px solid #829390;border-radius:4px;background:white;color:#10494c}button:focus-visible,select:focus-visible,input:focus-visible{outline:3px solid #10494c;outline-offset:3px}canvas{display:block;width:100%;height:auto;max-height:75vh;object-fit:contain;background:#10494c}small{display:block;margin-top:14px;max-width:900px}</style></head><body><main>
<h1>A rising response to praise</h1><p>Both parish logo options now move beside the separate, unchanged RCCG emblem. The full name stays below the symbol and remains still. <strong>DRAFT — NOT FOR PUBLICATION.</strong></p>
<div class="controls"><label>Option <select id="direction"><option value="shared-rhythm">Shared Rhythm</option><option value="open-praise">Open Praise</option></select></label><label>Format <select id="format"><option value="landscape">Landscape 1920 × 1080</option><option value="square">Square 1080 × 1080</option></select></label><button id="play" type="button">Play</button><label><input id="reduce" type="checkbox"> Reduce motion</label><span id="clock" aria-live="off">0.0 / 10.0s</span></div>
<canvas id="stage" width="1920" height="1080" aria-label="Paired parish and RCCG logo motion graphic, with stationary full name below"></canvas><small>Silent, controlled vector motion; no AI generation or Google upload. The RCCG reference image and white panel never animate. Final paired artwork is held from 6–10 seconds. The preserved 236 px parish-source emblem reference is not an approved high-resolution production master. Final brand, motion and publication approval remain open.</small>
</main><script>const DATA='''+payload+';'+SCRIPT+'</script></body></html>'

def crop_box(fmt, box):
    x,y,s = fmt['x'],fmt['y'],fmt['scale']
    return (math.floor(x+box[0]*s), math.floor(y+box[1]*s), math.ceil(x+box[2]*s), math.ceil(y+box[3]*s))

def capture(page, slug, format, t):
    encoded = page.evaluate('([s,f,t])=>window.renderFrame(s,f,t)', [slug,format,t])
    return Image.open(BytesIO(base64.b64decode(encoded))).convert('RGB')

def encode(page, direction, format, fmt, end):
    slug=direction['id'];path=OUT/'exports'/f'{slug}-RCCG-motion-{format}-DRAFT.mp4'
    args=['ffmpeg','-y','-hide_banner','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f"{fmt['width']}x{fmt['height']}",'-r',str(SCENE['fps']),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-threads','2','-movflags','+faststart',str(path)]
    proc=subprocess.Popen(args,stdin=subprocess.PIPE)
    parent_box=crop_box(fmt,(139,66,351,278));name_box=crop_box(fmt,(510,312,825,445));symbol_box=crop_box(fmt,(500,35,850,309))
    parent=end.crop(parent_box);name=end.crop(name_box);components=set();exact=True;samples={}
    try:
        for index in range(SCENE['fps']*SCENE['durationSeconds']):
            t=index/SCENE['fps'];frame=capture(page,slug,format,t)
            assert ImageChops.difference(frame.crop(parent_box),parent).getbbox() is None, f'Parent altered: {slug}/{format}@{t}'
            assert ImageChops.difference(frame.crop(name_box),name).getbbox() is None, f'Name altered: {slug}/{format}@{t}'
            if slug=='shared-rhythm':
                # Bright ivory plane ink against teal, excluding parent/name.
                mask=np.asarray(frame.crop(symbol_box).convert('L'))>155
                count=label(mask,structure=np.ones((3,3),dtype=np.uint8))[1]
                assert count==4, f'Plane contact or fragment: {slug}/{format}@{t}: {count}'
                components.add(int(count))
            if t>=6: exact &= ImageChops.difference(frame,end).getbbox() is None
            proc.stdin.write(frame.tobytes())
        proc.stdin.close();assert proc.wait()==0
    except Exception:
        proc.kill();raise
    assert exact
    for t in [0,1.2,2.1,3,4.2,8]:samples[str(t)]=capture(page,slug,format,t)
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]));v=probe['streams'][0]
    assert len(probe['streams'])==1 and v['codec_name']=='h264' and v['pix_fmt']=='yuv420p' and int(v['nb_frames'])==300 and float(probe['format']['duration'])==10
    assert v['width']==fmt['width'] and v['height']==fmt['height']
    return path,samples,{'file':str(path.relative_to(OUT)),'sha256':digest(path),'bytes':path.stat().st_size,'size':[fmt['width'],fmt['height']],'frames':300,'fps':30,'durationSeconds':10,'codec':'h264','pixelFormat':'yuv420p','silent':True,'parentPixelsStaticEveryFrame':True,'namePixelsStaticEveryFrame':True,'all300LosslessFramesChecked':True,'finalLosslessHoldMatchesEndPNG':True,'sharedSymbolComponentsAllFrames':sorted(components) if components else None,'sourceReferencePixelSize':236,'parentDisplaySize':180*fmt['scale'],'parentDisplayNotUpscaled':180*fmt['scale']<=236}

def storyboard(samples):
    labels=['Quiet start','First overlapping response','Shared rise','Tall plane lifts','Gentle settle','Final paired hold']
    board=Image.new('RGB',(1600,900),'#F6F3EC');draw=ImageDraw.Draw(board)
    def text(value,xy,size):draw.text(xy,value,font=ImageFont.truetype(str(FONT),size),fill='#10494C')
    text('Shared Rhythm · A rising response to praise',(40,24),32)
    text('Separate RCCG emblem · full name below · DRAFT — NOT FOR PUBLICATION',(40,73),20)
    for index,((t,image),caption) in enumerate(zip(samples.items(),labels)):
        x=40+(index%3)*520;y=130+(index//3)*350
        board.paste(image.resize((480,270),Image.Resampling.LANCZOS),(x,y))
        text(f'{t}s · {caption}',(x,y+282),18)
    text('The emblem and name stay still. The exact paired composition holds from 6–10 seconds.',(40,852),20)
    board.save(OUT/'previews/shared-rhythm-RCCG-storyboard-DRAFT.png')

def main():
    for folder in ('exports','previews'): (OUT/folder).mkdir(exist_ok=True,parents=True)
    assert digest(REPO/SCENE['emblemSource'])==SCENE['emblemSHA256']
    data={};masters={};sources=[]
    for direction in SCENE['directions']:
        sources.append({'id':direction['id'],'source':direction['source'],'sha256':digest(REPO/direction['source'])})
        for format,fmt in SCENE['formats'].items():
            root=scene_svg(direction,fmt);stem=f"{direction['id']}-RCCG-motion-{format}-end-DRAFT"
            svg=OUT/'exports'/(stem+'.svg');svg.write_text(ET.tostring(root,encoding='unicode'))
            # Browser renders SVG directly; final PNG is the authoritative static scene image.
            masters[direction['id']+'/'+format]=(root,svg)
    with sync_playwright() as pw:
        browser=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
        page=browser.new_page(viewport={'width':1920,'height':1080})
        page.set_content('<canvas id="x"></canvas>')
        for key,(root,svg) in masters.items():
            slug,format=key.split('/');fmt=SCENE['formats'][format];direction=next(x for x in SCENE['directions'] if x['id']==slug)
            raw=base64.b64encode(svg.read_bytes()).decode()
            result=page.evaluate('''async([raw,w,h])=>{const c=document.getElementById('x');c.width=w;c.height=h;const im=new Image();await new Promise((r,j)=>{im.onload=r;im.onerror=j;im.src='data:image/svg+xml;base64,'+raw});c.getContext('2d').drawImage(im,0,0);return c.toDataURL('image/png').split(',')[1]}''',[raw,fmt['width'],fmt['height']])
            png=svg.with_suffix('.png');png.write_bytes(base64.b64decode(result))
            erase=crop_box(fmt,(500,35,850,310));erase=[erase[0],erase[1],erase[2]-erase[0],erase[3]-erase[1]]
            data[key]={**direction,**fmt,'symbolSvg':motion_svg(root),'endImage':datauri(png),'symbolErase':erase}
        html=OUT/'preview.html';html.write_text(html_source(data))
        page.set_content(html.read_text(),wait_until='load');page.evaluate('ready')
        report={'status':SCENE['status'],'method':'Controlled SVG motion graphics; no generative service or upload.','emblem':{'source':SCENE['emblemSource'],'sha256':SCENE['emblemSHA256'],'bytesUnmodified':True,'original1200pxUploadVerified':False},'meaning':SCENE['meaning'],'sources':sources,'videos':[],'notes':['The first two Shared Rhythm rises overlap under a 4-source-unit relative offset constraint to keep the original shoulder interval open.','All checks compare lossless pre-encode RGB frames. H.264/YUV is lossy.','Editorial draft footers are presentation labels outside unchanged parish artwork.','Final artwork holds from 6–10 seconds; no exit or seamless loop is provided.']}
        for direction in SCENE['directions']:
            for format,fmt in SCENE['formats'].items():
                key=direction['id']+'/'+format;end=Image.open(masters[key][1].with_suffix('.png')).convert('RGB')
                path,samples,checks=encode(page,direction,format,fmt,end);report['videos'].append(checks)
                print('Rendered '+str(path.relative_to(OUT)),flush=True)
                if key=='shared-rhythm/landscape':
                    storyboard(samples)
                    subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(path),'-filter_complex','fps=12,scale=768:432:flags=lanczos,split[a][b];[a]palettegen=max_colors=192[p];[b][p]paletteuse=dither=sierra2_4a','-filter_complex_threads','1','-loop','0',str(OUT/'previews/shared-rhythm-RCCG-motion-DRAFT.gif')],check=True)
        browser.close()
    (OUT/'exports/render-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('All four paired motion graphics rendered and checked.',flush=True)

if __name__=='__main__':main()
