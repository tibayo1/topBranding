#!/usr/bin/env python3
"""Focused open-contour counter refinements. Preserves the previous outer silhouette."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json,subprocess,os,hashlib
import xml.etree.ElementTree as ET
from fontTools.pens.boundsPen import BoundsPen
from fontTools.svgLib.path import parse_path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parents[3]
R=ROOT/'renders';V=ROOT/'versions'
TEAL='#10494C';IVORY='#F6F3EC';DRAFT='DRAFT — NOT FOR PUBLICATION'
VERSIONS={
'v0-review-09':'M28 28H140C205 28 228 65 228 96C228 142 197 163 133 177V101H147C167 101 179 111 179 126L184 126C191 116 194 107 194 99V85C194 73 188 68 177 68H62C57 68 53 67 49 66C53 83 62 95 75 95H90V169C90 193 102 207 133 223H110C45 223 28 190 28 142Z',
'v1-aligned-crossbar':'M28 28H140C205 28 228 65 228 96C228 142 197 163 133 177V98H147C167 98 179 109 179 124L184 124C191 114 194 106 194 98V85C194 73 188 68 177 68H62C57 68 53 67 49 66C53 84 62 98 75 98H90V169C90 193 102 207 133 223H110C45 223 28 190 28 142Z',
'v2-centered-wider-stem':'M28 28H140C205 28 228 65 228 96C228 142 197 163 135 177V98H148C168 98 179 109 179 124L184 124C191 114 194 106 194 98V85C194 73 188 68 177 68H62C57 68 53 67 49 66C53 84 62 98 75 98H88V169C88 193 101 207 133 223H110C45 223 28 190 28 142Z',
'v3-aligned-compact':'M28 28H140C205 28 228 65 228 96C228 142 197 163 134 177V100H146C165 100 175 110 180 121H188C192 114 194 107 194 98V86C194 74 188 69 177 69H62C57 69 53 68 49 67C54 86 63 100 76 100H88V168C88 193 101 207 133 223H110C45 223 28 190 28 142Z'
}
VERSIONS['v0-review-09-compact']='M28 28H140C205 28 228 65 228 96C228 142 197 163 134 177V103H146C165 103 175 110 180 121H188C192 114 194 107 194 98V86C194 74 188 69 177 69H62C57 69 53 68 49 67C54 84 63 95 76 95H88V168C88 193 101 207 133 223H110C45 223 28 190 28 142Z'
SELECTED='v1-aligned-crossbar';COMPACT='v3-aligned-compact'
LABELS={'v0-review-09':'Review 09 baseline','v1-aligned-crossbar':'Aligned crossbar','v2-centered-wider-stem':'Aligned + wider stem','v3-aligned-compact':'Tiny-use candidate','v0-review-09-compact':'Review 09 tiny-use baseline'}
NOTES={'v0-review-09':['Crossbar underside left 95/right 101.','A six-unit step across the stem.'],'v1-aligned-crossbar':['Both lower edges meet at 98.','Same stem width and outer silhouette.'],'v2-centered-wider-stem':['Stem widened from 43 to 47.','More open, but less compact character.']}
def svg(path,label,mode=None):
 ink=TEAL if mode=='light' else IVORY if mode=='dark' else '#000000'
 bg=IVORY if mode=='light' else TEAL if mode=='dark' else None
 rect=f'<rect width="256" height="256" fill="{bg}"/>' if bg else ''
 return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256"><title>Open Praise / {label} — {DRAFT}</title><desc>One original contour holding an open negative T. No mask or background-colored overlay. Recognition remains subject to review.</desc>{rect}<path fill="{ink}" d="{path}"/></svg>\n'
def render(job):
 src,out,size=job
 env=os.environ.copy();env['XDG_CONFIG_HOME']='/tmp/top-branding-inkscape-config';env['XDG_CACHE_HOME']='/tmp/top-branding-inkscape-cache'
 subprocess.run(['inkscape',str(src),'--export-type=png',f'--export-filename={out}',f'--export-width={size}',f'--export-height={size}'],check=True,capture_output=True,env=env)
def board():
 fontfile=REPO/'brand/explorations/creative-review-05/assets/noto-sans-regular.ttf'
 f=ImageFont.truetype(str(fontfile),25);s=ImageFont.truetype(str(fontfile),19);tiny=ImageFont.truetype(str(fontfile),16)
 out=Image.new('RGB',(1600,1320),'#fbfaf7');d=ImageDraw.Draw(out)
 d.text((35,24),'OPEN PRAISE / TEAL REFINEMENT 11',font=f,fill=TEAL)
 d.text((35,63),DRAFT+' · Focused counter study; full letter recognition is not assumed.',font=s,fill=TEAL)
 for col,name in enumerate(list(VERSIONS)[:3]):
  x=35+col*530
  d.text((x,112),LABELS[name],font=f,fill=TEAL)
  for row,mode in enumerate(['light','dark']):
   y=160+row*390
   im=Image.open(R/f'{name}-{mode}-512.png').convert('RGB').resize((360,360),Image.Resampling.LANCZOS)
   out.paste(im,(x+58,y))
  for j,line in enumerate(NOTES[name]):d.text((x,958+j*30),line,font=s,fill=TEAL)
  for j,size in enumerate([24,32,48,64]):
   xx=x+j*125
   d.text((xx,1050),f'{size}px',font=tiny,fill=TEAL)
   for row,mode in enumerate(['light','dark']):
    yy=1083+row*92
    bg=IVORY if mode=='light' else TEAL
    d.rectangle((xx,yy,xx+93,yy+77),fill=bg)
    im=Image.open(R/f'{name}-{mode}-{size}.png').convert('RGB');out.paste(im,(xx+(94-size)//2,yy+(78-size)//2))
 d.text((35,1290),'The outer P body is preserved. Compare the actual-size samples; aligned edges do not prove T recognition.',font=tiny,fill=TEAL)
 out.save(R/'counter-comparison.png')

def compact_board():
 fontfile=REPO/'brand/explorations/creative-review-05/assets/noto-sans-regular.ttf'
 f=ImageFont.truetype(str(fontfile),23);s=ImageFont.truetype(str(fontfile),17)
 out=Image.new('RGB',(1120,600),'#fbfaf7');d=ImageDraw.Draw(out)
 d.text((30,18),'OPEN PRAISE / 16–20 px COMPACT CANDIDATE',font=f,fill=TEAL)
 d.text((30,56),DRAFT+' · Native at left, 5x nearest-neighbor detail at right.',font=s,fill=TEAL)
 for col,name in enumerate(['v0-review-09-compact',COMPACT]):
  x=30+col*555
  d.text((x,103),LABELS[name],font=f,fill=TEAL)
  for row,mode in enumerate(['light','dark']):
   y=154+row*174;bg=IVORY if mode=='light' else TEAL;ink=TEAL if mode=='light' else IVORY
   d.rectangle((x,y,x+505,y+152),fill=bg)
   for j,size in enumerate([16,20]):
    xx=x+25+j*240
    im=Image.open(R/f'{name}-{mode}-{size}.png').convert('RGB')
    out.paste(im,(xx,y+38))
    out.paste(im.resize((size*5,size*5),Image.Resampling.NEAREST),(xx+55,y+20))
    d.text((xx,y+125),f'{size} px',font=s,fill=ink)
 d.text((30,535),'Candidate aligns the crossbar undersides while keeping the broad stem. Silhouette remains clearer than letter detail.',font=s,fill=TEAL)
 d.text((30,564),'Large avatars use the primary. This is a provisional tiny-use drawing, not a final minimum-size standard.',font=s,fill=TEAL)
 out.save(R/'compact-comparison.png')

def structural_checks():
 records=[];ns='{http://www.w3.org/2000/svg}'
 for file in [*ROOT.glob('*.svg'),*V.glob('*.svg')]:
  root=ET.parse(file).getroot();paths=list(root.iter(ns+'path'))
  assert len(paths)==1,file
  assert not any(root.iter(ns+'text')) and not any(root.iter(ns+'image')) and not any(root.iter(ns+'mask')),file
  path=paths[0].get('d');assert path.count('M')==1 and path.endswith('Z'),file
  pen=BoundsPen(None);parse_path(path,pen)
  assert pen.bounds==(28.0,28.0,228.0,223.0),(file,pen.bounds)
  records.append({'file':str(file.relative_to(ROOT)),'singleClosedContour':True,'bounds':list(pen.bounds),'noLiveTypeOrRaster':True})
 return {'svgAudit':records,'nativeRenders':[16,20,24,32,48,64],'largeRender':512,'renderer':'Inkscape','claim':'Structural checks and inspected renders do not establish letter recognition, production minimums or approval.'}

def main():
 R.mkdir(exist_ok=True);V.mkdir(exist_ok=True)
 jobs=[]
 for name,path in VERSIONS.items():
  (V/(name+'.svg')).write_text(svg(path,LABELS[name]))
  for mode in ['light','dark']:
   source=V/f'{name}-{mode}.svg';source.write_text(svg(path,LABELS[name],mode))
   sizes=[16,20,24,32,48,64,512] if 'compact' in name else [24,32,48,64,512]
   for size in sizes:jobs.append((source,R/f'{name}-{mode}-{size}.png',size))
 with ThreadPoolExecutor(max_workers=3) as ex:list(ex.map(render,jobs))
 for role,key in [('primary',SELECTED),('compact',COMPACT)]:
  (ROOT/f'{role}.svg').write_text(svg(VERSIONS[key],LABELS[key]))
  for mode in ['light','dark']:(ROOT/f'{role}-{mode}.svg').write_text(svg(VERSIONS[key],LABELS[key],mode))
 board()
 compact_board()
 metadata={'id':'open-praise','name':'Open Praise','status':DRAFT,'approval':False,'viewBox':'0 0 256 256','primaryFile':'primary.svg','compactFile':'compact.svg','sourceFile':'source/build.py','primaryVersion':SELECTED,'compactVersion':COMPACT,'baseline':'../../identity-development-09/open-praise/primary.svg','changes':['The left and right undersides of the negative crossbar are aligned at 98 instead of 95/101.','Same 43-unit primary stem width; original outer P silhouette and lower exit preserved.','Right counter terminal lifts two units with the leveled crossbar to keep the transition compact.'],'compact':'Provisional 16–20 px cut aligns the two lower crossbar edges at 100 while retaining a 46-unit stem and simpler terminal. Primary remains for normal avatars and display.','risk':'Negative T remains inferential; P may dominate. Studio, publisher or institutional associations remain possible. Shape and rendering tests do not establish audience recognition or legal originality.','meaning':'T and P refer to Tabernacle and Praise through one open figure-ground contour. No additional worship symbol is claimed.','palette':{'primary':TEAL,'neutral':IVORY,'secondary':'#D9CBB4','accent':'#B69255','status':'User-selected working direction, not final production colors.'},'versions':[{'id':key,'file':'versions/'+key+'.svg','name':LABELS[key]} for key in VERSIONS],'proofs':['renders/counter-comparison.png','renders/compact-comparison.png'],'sourceHash':hashlib.sha256((ROOT/'primary.svg').read_bytes()).hexdigest(),'checks':structural_checks(),'visualInspection':'Viewed actual large and native teal/ivory comparisons. Independent editor prefers aligned crossbar as a modest cohesion improvement; wider stem rejected as less compact. Compact 16/20 proof viewed separately; independent editor found no visible downside and agreed to freeze both aligned cuts. Recognition is not established.'}
 (ROOT/'metadata.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n')
 print('Rendered counter comparison with baseline, two primary tests and one compact candidate.')
if __name__=='__main__':main()
