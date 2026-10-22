#!/usr/bin/env python3
"""Build the original projected-vector Shared Rhythm motion film."""
from pathlib import Path
from copy import deepcopy
from io import BytesIO
import argparse,base64,hashlib,json,subprocess,shutil
import xml.etree.ElementTree as E
from PIL import Image,ImageChops,ImageDraw,ImageFont
from playwright.sync_api import sync_playwright

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
REPO=HERE.parents[3]
SCENE=json.loads((HERE/'scene.json').read_text())
NS='http://www.w3.org/2000/svg'
E.register_namespace('',NS)
FONT=REPO/'brand/explorations/identity-development-09/type-study/fonts/instrumentsans/InstrumentSans[wdth,wght].ttf'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def uri(p,mime='image/png'):return f'data:{mime};base64,'+base64.b64encode(p.read_bytes()).decode()
def flatten(root,keep):
 for parent in root.iter():
  for child in list(parent):
   part=child.get('data-part')
   if (part=='symbol' and not keep) or (part=='name' and keep):parent.remove(child)
 return root
def html(assets):
 return '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Shared Rhythm — cinematic motion draft</title><style>body{margin:0;background:#e9e6df;color:#10494c;font:16px/1.6 Arial,sans-serif}main{max-width:1280px;margin:28px auto;padding:0 22px}h1{font-size:28px;font-weight:500;line-height:1.2}canvas{display:block;width:100%;height:auto;background:#10494c}.controls{display:flex;gap:20px;align-items:center;margin:20px 0}button{font:inherit;padding:8px 20px;color:#10494c;background:white;border:1px solid #10494c;border-radius:4px}button:focus-visible,input:focus-visible{outline:3px solid #10494c;outline-offset:3px}small{display:block;margin:16px 0 30px;max-width:900px}</style></head><body><main><h1>Shared Rhythm — a rising response to praise</h1><p>DRAFT — NOT FOR PUBLICATION. An original procedural material-and-motion study, with an exact source-artwork closing hold.</p><canvas id="stage" width="1920" height="1080" aria-label="Shared Rhythm gathering, rising and resolving into paired parish and RCCG identity"></canvas><div class="controls"><button type="button" id="play">Play</button><label><input id="reduce" type="checkbox"> Reduce motion</label><span id="time">0.0 / 14.0 s</span></div><small>Silent browser preview. The downloadable film can include a separate original sound study. No AI-generated congregation or generative video service is used. The original RCCG reference and parish lettering are composited intact. Final identity, motion and publication approval remain open.</small></main><script>const ASSETS='''+json.dumps(assets)+''';\n'''+(HERE/'film.js').read_text()+'''</script></body></html>'''
def image_frame(page,t):
 raw=page.evaluate('(t)=>window.renderFrame(t)',t)
 return Image.open(BytesIO(base64.b64decode(raw))).convert('RGB')
def storyboard(frames):
 board=Image.new('RGB',(1600,810),'#F6F3EC');d=ImageDraw.Draw(board)
 def text(v,p,s):d.text(p,v,font=ImageFont.truetype(str(FONT),s),fill='#10494C')
 text('Shared Rhythm — gathering, shared rise, resolve',(36,20),31)
 text('Original procedural motion study · DRAFT — NOT FOR PUBLICATION',(36,67),18)
 captions=['Distinct voices','Gathering in the forecourt','A shared rising response','Folded architectural rhythm','Resolve into the identity','Exact paired closing hold']
 for i,((t,im),cap) in enumerate(zip(frames,captions)):
  x=36+(i%3)*520;y=116+(i//3)*330
  board.paste(im.resize((488,274),Image.Resampling.LANCZOS),(x,y));text(f'{t:.1f}s · {cap}',(x,y+282),17)
 board.save(ROOT/'previews/storyboard-DRAFT.png')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--keyframes-only',action='store_true');args=ap.parse_args()
 for d in ('exports','previews','source/assets'):(ROOT/d).mkdir(parents=True,exist_ok=True)
 src=REPO/SCENE['endSource'];pngsrc=REPO/SCENE['endPNGSource'];outsvg=ROOT/'exports/shared-rhythm-cinematic-end-DRAFT.svg';outpng=outsvg.with_suffix('.png')
 shutil.copyfile(src,outsvg);shutil.copyfile(pngsrc,outpng)
 root=E.parse(src).getroot();overlay=flatten(deepcopy(root),False);symbol=flatten(deepcopy(root),True)
 # Transparent exact-pose separate layers. Keep the emblem/name out of dimensional motion.
 for parent in overlay.iter():
  for child in list(parent):
   if child.tag==f'{{{NS}}}rect' and child.get('fill','').upper()=='#10494C':parent.remove(child)
 for parent in symbol.iter():
  for child in list(parent):
   if child.tag==f'{{{NS}}}image' or child.get('data-part')=='editorial-footer' or child.tag==f'{{{NS}}}rect':parent.remove(child)
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage']);page=browser.new_page(viewport={'width':1920,'height':1080});page.set_content('<canvas id="render"></canvas>')
  assets={'end':uri(outpng)}
  for key,tree in [('overlay',overlay),('symbol',symbol)]:
   svgpath=HERE/'assets'/f'{key}.svg';svgpath.write_text(E.tostring(tree,encoding='unicode'))
   encoded=page.evaluate('''async raw=>{const c=document.getElementById('render');c.width=1920;c.height=1080;const im=new Image();await new Promise((r,j)=>{im.onload=r;im.onerror=j;im.src='data:image/svg+xml;base64,'+raw});c.getContext('2d').drawImage(im,0,0);return c.toDataURL('image/png').split(',')[1]}''',base64.b64encode(svgpath.read_bytes()).decode())
   png=svgpath.with_suffix('.png');png.write_bytes(base64.b64decode(encoded));assets[key]=uri(png)
  preview=ROOT/'preview.html';preview.write_text(html(assets));page.set_content(preview.read_text(),wait_until='load');page.evaluate('assetReady')
  times=[.8,2.8,5,7,9.3,11.5];frames=[]
  for t in times:
   im=image_frame(page,t);im.save(ROOT/'previews'/f'keyframe-{t:04.1f}s-DRAFT.png');frames.append((t,im))
  storyboard(frames);print('Keyframes and storyboard rendered.',flush=True)
  if args.keyframes_only:browser.close();return
  outfile=ROOT/'exports/shared-rhythm-cinematic-1080p-SILENT-DRAFT.mp4'
  proc=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','30','-i','-','-an','-c:v','libx264','-preset','fast','-crf','17','-pix_fmt','yuv420p','-threads','2','-movflags','+faststart',str(outfile)],stdin=subprocess.PIPE)
  reference=Image.open(outpng).convert('RGB');exact=True;energy=[]
  try:
   for i in range(420):
    t=i/30;im=image_frame(page,t);energy.append(max(pair[1] for pair in im.getextrema()));assert energy[-1]>20, f'Unexpected black frame {i}'
    if t>=10.5:exact&=ImageChops.difference(im,reference).getbbox() is None
    proc.stdin.write(im.tobytes())
    if i%90==0:print(f'Rendered frame {i}/420',flush=True)
   proc.stdin.close();assert proc.wait()==0
  except Exception:proc.kill();raise
  assert exact
  browser.close()
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(outfile)]));v=probe['streams'][0]
 assert len(probe['streams'])==1 and v['codec_name']=='h264' and v['pix_fmt']=='yuv420p' and v['nb_frames']=='420' and float(probe['format']['duration'])==14
 subprocess.run(['ffmpeg','-y','-v','error','-i',str(outfile),'-filter_complex','fps=10,scale=768:432:flags=lanczos,split[a][b];[a]palettegen=max_colors=192[p];[b][p]paletteuse=dither=sierra2_4a','-filter_complex_threads','1','-loop','0',str(ROOT/'previews/shared-rhythm-cinematic-DRAFT.gif')],check=True)
 report={'status':SCENE['status'],'method':SCENE['method'],'sourceSVG':str(src.relative_to(REPO)),'sourceSVGSHA256':sha(src),'sourcePNG':str(pngsrc.relative_to(REPO)),'sourcePNGSHA256':sha(pngsrc),'exactEndSVGCopied':outsvg.read_bytes()==src.read_bytes(),'exactEndPNGCopied':outpng.read_bytes()==pngsrc.read_bytes(),'losslessFinalHoldPixelMatch':exact,'exactHoldSeconds':[10.5,14],'video':str(outfile.relative_to(ROOT)),'sha256':sha(outfile),'width':1920,'height':1080,'fps':30,'frames':420,'duration':14,'silent':True,'codec':'h264','pixelFormat':'yuv420p','allFramesNonBlack':min(energy)>20,'notes':['Final hold equality checked before lossy H264 encoding.','Original RCCG reference is only composited intact; it is not transformed into the dimensional scene.','The film uses no human figures, unverified church scenes or external generated video.']}
 (ROOT/'exports/render-checks.json').write_text(json.dumps(report,indent=2)+'\n');print('Finished14-second full-HD silent film.',flush=True)
if __name__=='__main__':main()
