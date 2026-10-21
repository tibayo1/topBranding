#!/usr/bin/env python3
"""Render a silent, deterministic vector motion study from the exact draft marks.

This is a controlled motion reference, not a Google-generated video. Only symbol
paths translate. Every frame retains the supplied outlined full name below it.
"""
from __future__ import annotations

import base64
from io import BytesIO
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import xml.etree.ElementTree as ET

from PIL import Image, ImageChops, ImageDraw, ImageFont
import numpy as np
from scipy.ndimage import label
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
INPUTS = ROOT / 'animation-inputs'
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
SIZE, FPS, SECONDS = 1080, 30, 8
FONT = ROOT.parent / 'identity-development-09/type-study/fonts/instrumentsans/InstrumentSans[wdth,wght].ttf'


def uri(path):
    return 'data:image/png;base64,' + base64.b64encode(path.read_bytes()).decode()


def source_data(slug):
    folder = INPUTS / slug / 'square'
    end = folder / 'full-logo-end-DRAFT.svg'
    root = ET.parse(end).getroot()
    # Keep the outer placement and original symbol geometry. The name comes
    # directly from the authoritative end PNG, so its pixels never animate.
    for node in list(root):
        if node.tag.rsplit('}', 1)[-1] in ('title', 'desc', 'rect'):
            root.remove(node)
    for parent in root.iter():
        for child in list(parent):
            if child.get('data-part') == 'name':
                parent.remove(child)
    mark = next(node for node in root.iter() if node.get('data-part') == 'symbol')
    paths = list(mark.iter(f'{{{NS}}}path'))
    for index, path in enumerate(paths):
        path.set('data-motion-plane', str(index))
    return {
        'id': slug,
        'name': 'Shared Rhythm' if slug == 'shared-rhythm' else 'Open Praise',
        'symbolSvg': ET.tostring(root, encoding='unicode'),
        'startImage': uri(folder / 'full-logo-start-DRAFT.png'),
        'endImage': uri(folder / 'full-logo-end-DRAFT.png'),
        'offsets': [22, 26, 30, 24] if slug == 'shared-rhythm' else [18],
        'delays': [.8, 1.25, 1.7, 2.15] if slug == 'shared-rhythm' else [.8],
        'duration': 2.4 if slug == 'shared-rhythm' else 3.0,
        'namePixelTop': 660,
        'source': str(end.relative_to(ROOT)),
        'sourceSHA256': hashlib.sha256(end.read_bytes()).hexdigest(),
        'endPNG': str((folder/'full-logo-end-DRAFT.png').relative_to(ROOT)),
    }


SCRIPT = r'''
const canvas=document.getElementById('stage'),ctx=canvas.getContext('2d');
let selected='shared-rhythm',playing=false,startClock=0,elapsed=0;
const images={};
function image(src){return new Promise((resolve,reject)=>{let im=new Image();im.onload=()=>resolve(im);im.onerror=reject;im.src=src})}
const ready=Promise.all(Object.values(DATA).map(async d=>{images[d.id]={start:await image(d.startImage),end:await image(d.endImage)}}));
function easeOutBack(u){const c=.75;return 1+(c+1)*Math.pow(u-1,3)+c*Math.pow(u-1,2)}
function offsetsFor(d,t){
 const values=d.offsets.map((offset,i)=>{let u=Math.max(0,Math.min(1,(t-d.delays[i])/d.duration));return t>=6?0:offset*(1-easeOutBack(u))});
 // The original shoulder must not touch plane1 as the responses overlap.
 // Keep all contours intact; coordinate their translations rather than
 // redrawing, scaling or hiding the projecting shoulder.
 if(d.id==='shared-rhythm')values[1]=Math.min(values[1],values[0]+4);
 return values;
}
async function drawFrame(slug,t){
 await ready;const d=DATA[slug];t=Math.max(0,Math.min(8,t));
 if(t<=.8){ctx.drawImage(images[slug].start,0,0);return}
 const offsets=offsetsFor(d,t);
 if(t>=6||offsets.every(v=>Math.abs(v)<1e-8)){ctx.drawImage(images[slug].end,0,0);return}
 const doc=new DOMParser().parseFromString(d.symbolSvg,'image/svg+xml');
 doc.querySelectorAll('[data-motion-plane]').forEach((path,i)=>path.setAttribute('transform',`translate(0 ${offsets[i]})`));
 const raw=new XMLSerializer().serializeToString(doc);
 const moved=await image('data:image/svg+xml;base64,'+btoa(unescape(encodeURIComponent(raw))));
 ctx.drawImage(images[slug].end,0,0);
 // Erase only the symbol region. The name pixels are untouched and static.
 ctx.fillStyle='#F6F3EC';ctx.fillRect(0,0,1080,d.namePixelTop);
 ctx.drawImage(moved,0,0);
}
window.renderFrame=async(slug,t)=>{await drawFrame(slug,t);return canvas.toDataURL('image/png').split(',')[1]};
window.motionOffsets=(slug,t)=>offsetsFor(DATA[slug],t);
async function tick(clock){if(!playing)return;elapsed=Math.min(8,(clock-startClock)/1000);await drawFrame(selected,elapsed);document.getElementById('clock').textContent=elapsed.toFixed(1)+' / 8.0s';if(elapsed<8&&playing)requestAnimationFrame(tick);else{playing=false;document.getElementById('play').textContent='Replay'}}
document.getElementById('play').onclick=()=>{playing=false;elapsed=0;startClock=performance.now();playing=true;document.getElementById('play').textContent='Playing';requestAnimationFrame(tick)};
document.getElementById('direction').onchange=async e=>{playing=false;selected=e.target.value;elapsed=0;document.getElementById('play').textContent='Play';document.getElementById('clock').textContent='0.0 / 8.0s';await drawFrame(selected,0)};
ready.then(()=>drawFrame(selected,0));
'''


def html_source(data):
    payload = json.dumps(data, ensure_ascii=False).replace('</', '<\\/')
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>Tabernacle of Praise — draft motion study</title><style>'
            'body{margin:0;background:#e9e8e2;color:#10494c;font-family:Arial,sans-serif}'
            'main{max-width:760px;margin:28px auto;padding:0 20px 30px}h1{font-size:25px;margin:0 0 10px}'
            'p{font-size:14px;line-height:1.6}canvas{width:100%;height:auto;display:block;background:#F6F3EC}'
            '.controls{display:flex;gap:12px;align-items:center;margin:16px 0}button,select{font:inherit;padding:8px 12px}'
            'button:focus-visible,select:focus-visible{outline:3px solid #10494c;outline-offset:3px}'
            'small{display:block;margin-top:14px;line-height:1.5}</style></head><body><main>'
            '<h1>A rising response to praise</h1><p>DRAFT — NOT FOR PUBLICATION. '
            'The four planes rise in response, then settle into Shared Rhythm. The complete name stays below, still and readable.</p>'
            '<div class="controls"><label>Option <select id="direction"><option value="shared-rhythm">Shared Rhythm</option>'
            '<option value="open-praise">Open Praise</option></select></label><button id="play" type="button">Play</button>'
            '<span id="clock" aria-live="off">0.0 / 8.0s</span></div><canvas id="stage" width="1080" height="1080" '
            'aria-label="Draft exact-vector logo animation with static name below"></canvas>'
            '<small>Controlled vector motion reference, made from the supplied SVG paths. This is not a Google-generated video. '
            'Silent; static camera; no RCCG emblem in the moving artwork. Geometry is held exactly for the final two seconds.</small>'
            '</main><script>const DATA='+payload+';'+SCRIPT+'</script></body></html>')


def frame(page, slug, seconds):
    data = page.evaluate('([slug,t])=>window.renderFrame(slug,t)', [slug, seconds])
    return Image.open(BytesIO(base64.b64decode(data))).convert('RGB')


def encode(page, slug, end):
    output = HERE / f'{slug}-rising-response-1080-DRAFT.mp4'
    command = ['ffmpeg','-y','-hide_banner','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24',
               '-s','1080x1080','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','18',
               '-pix_fmt','yuv420p','-movflags','+faststart','-threads','2',str(output)]
    encoder = subprocess.Popen(command, stdin=subprocess.PIPE)
    name_reference = end.crop((0,660,SIZE,SIZE))
    exact_final = True
    components = set()
    samples = {}
    try:
        for index in range(FPS*SECONDS):
            t = index/FPS
            image = frame(page, slug, t)
            assert ImageChops.difference(image.crop((0,660,SIZE,SIZE)), name_reference).getbbox() is None, f'Name changed at {t}'
            if slug=='shared-rhythm':
                # Only the reserved symbol region, not the static name.
                # A half-coverage luminance threshold ignores faint AA fringe.
                mask=np.asarray(image.crop((0,0,SIZE,660)).convert('L'))<155
                count=label(mask,structure=np.ones((3,3),dtype=np.uint8))[1]
                assert count==4,f'Planes touch or fragment at {t}: {count} components'
                components.add(int(count))
            if t>=6:
                exact_final &= ImageChops.difference(image, end).getbbox() is None
            encoder.stdin.write(image.tobytes())
        encoder.stdin.close()
        assert encoder.wait()==0
    except Exception:
        encoder.kill()
        raise
    assert exact_final
    for t in [0,1.2,2.1,3.0,4.2,6.5]:
        samples[str(t)] = frame(page,slug,t)
    probe = json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(output)]))
    video = next(row for row in probe['streams'] if row['codec_type']=='video')
    assert video['codec_name']=='h264' and video['pix_fmt']=='yuv420p'
    assert video['width']==SIZE and video['height']==SIZE and int(video['nb_frames'])==FPS*SECONDS
    assert abs(float(probe['format']['duration'])-SECONDS)<.05
    assert not any(row['codec_type']=='audio' for row in probe['streams'])
    return output, samples, {'durationSeconds':SECONDS,'frames':FPS*SECONDS,'fps':FPS,'size':[SIZE,SIZE],
                            'codec':'h264','pixelFormat':'yuv420p','silent':True,'namePixelsStatic':True,
                            'sharedPlaneComponentsAllFrames':sorted(components) if components else None,
                            'sharedGapMethod':'All 240 native pre-encode frames: 8-neighbor components in the symbol region, grayscale < 155. This supports separation only.' if components else None,
                            'losslessFinalFramesMatchRootPNG':exact_final,'encodedVideoNote':'H.264/YUV is lossy; exact equality is verified before encoding.'}


def contact_sheet(samples):
    board = Image.new('RGB',(1200,960),'#F6F3EC')
    draw = ImageDraw.Draw(board)
    def text(value,xy,size=18):
        draw.text(xy,value,font=ImageFont.truetype(str(FONT),size),fill='#10494C')
    text('Shared Rhythm — a rising response to praise',(30,25),28)
    text('DRAFT — NOT FOR PUBLICATION / controlled vector motion study',(30,65),17)
    captions = ['Quiet lower start','First planes responding','Shared rise','Tall inner face lifts','Gentle settling','Exact final identity']
    for index,((time,image),caption) in enumerate(zip(samples.items(),captions)):
        x=30+(index%3)*390;y=110+(index//3)*400
        board.paste(image.resize((360,360),Image.Resampling.LANCZOS),(x,y))
        text(f'{time}s · {caption}',(x,y+365),16)
    text('Four original planes; name remains still below; final master held through 6–8 seconds.',(30,927),17)
    path=HERE/'shared-rhythm-motion-contact-sheet.png';board.save(path);return path


def main():
    data={slug:source_data(slug) for slug in ['shared-rhythm','open-praise']}
    html=HERE/'motion-preview-DRAFT.html';html.write_text(html_source(data))
    report={'status':'DRAFT — NOT FOR PUBLICATION','method':'Deterministic SVG motion reference, not Google-generated.',
            'meaning':'A rising response to praise: four planes respond in sequence, then settle around their shared open space.',
            'timing':{'quietStart':[0,.8],'riseStarts':[.8,1.25,1.7,2.15],'allMotionSettledBy':6,'exactHold':[6,8]},
            'overlapCorrection':'The first two responses overlap: plane 2 stays within 4 source units below plane 1, preserving the projecting shoulder interval. Nominal delays are coordinated by this gap constraint; contours remain unchanged.',
            'sources':[{k:row[k] for k in ['id','source','sourceSHA256','endPNG']} for row in data.values()], 'videos':[]}
    with sync_playwright() as playwright:
        browser=playwright.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
        page=browser.new_page(viewport={'width':1200,'height':1200})
        page.set_content(html.read_text(),wait_until='load')
        page.evaluate('ready')
        for slug in ['shared-rhythm','open-praise']:
            end=Image.open(ROOT/data[slug]['endPNG']).convert('RGB')
            path,samples,checks=encode(page,slug,end)
            checks['file']=path.name;checks['sha256']=hashlib.sha256(path.read_bytes()).hexdigest();report['videos'].append(checks)
            if slug=='shared-rhythm':
                contact_sheet(samples)
                gif=HERE/'shared-rhythm-rising-response-540-DRAFT.gif'
                subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(path),'-filter_complex',
                                'fps=12,scale=540:540:flags=lanczos,split[a][b];[a]palettegen=max_colors=128[p];[b][p]paletteuse=dither=sierra2_4a',
                                '-filter_complex_threads','1','-loop','0',str(gif)],check=True)
        browser.close()
    (HERE/'motion-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('Rendered two 8-second silent 1080-square motion studies, Shared GIF/contact sheet, exact source-final holds and static names verified.')


if __name__=='__main__':
    main()
