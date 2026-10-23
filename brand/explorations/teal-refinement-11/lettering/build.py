#!/usr/bin/env python3
"""Polish spacing and name arrangements without modifying licensed glyphs."""
from pathlib import Path
from html import escape
import hashlib
import json
import shutil
import subprocess
import re
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.svgLib.path import parse_path
from PIL import ImageFont

HERE = Path(__file__).resolve().parent
STUDY09 = HERE.parents[1] / 'identity-development-09'
FONT = STUDY09 / 'type-study/fonts/instrumentsans/InstrumentSans[wdth,wght].ttf'
LICENSE = FONT.parent / 'OFL.txt'
NS = 'http://www.w3.org/2000/svg'
DRAFT = 'DRAFT — NOT FOR PUBLICATION'
BASELINE = {'Ta':-.012,'er':-.003,'rn':.004,'cl':.005,
            'Pr':-.010,'ra':-.004,'ai':-.003,'is':.003}
REFINED = {'Ta':-.010,'er':-.003,'rn':.008,'ac':-.002,'cl':.007,
           'Pr':-.008,'ra':-.003,'ai':-.002,'is':.004}


def svg(body, box, title):
    return (f'<svg xmlns="{NS}" viewBox="{box}" role="img" aria-label="{escape(title)}">'
            f'<title>{escape(title)} — DRAFT</title><desc>{DRAFT}. Original Instrument Sans 470 '
            'glyph contours; shaped and optically spaced. No font binary, glyph shape, '
            'type family or final brand approval is changed.</desc>'+body+'</svg>\n')


def ink(body):
    pen = BoundsPen(None)
    for path in re.findall(r'<path\b[^>]*\bd="([^"]+)"',body):
        parse_path(path,pen)
    return pen.bounds


class Lettering:
    def __init__(self,corrections):
        self.corrections=corrections
        self.font=TTFont(FONT)
        self.glyphs=self.font.getGlyphSet(location={'wdth':100,'wght':470})
        self.cmap=self.font.getBestCmap()
        self.units=self.font['head'].unitsPerEm
        self.shaper=ImageFont.truetype(str(FONT),1000,layout_engine=ImageFont.Layout.RAQM)
        self.shaper.set_variation_by_axes([100,470])

    def length(self,text):
        return self.shaper.getlength(text,features=['-liga','-clig'])

    def draw(self,text,x,baseline,size=100):
        pieces=[];positions=[];adjustment=0
        for i,char in enumerate(text):
            if i:
                adjustment+=self.corrections.get(text[i-1:i+1],0)
            advance=(self.length(text[:i+1])-self.length(char))/1000
            advance+=i*.002+adjustment
            left=x+advance*size
            positions.append({'character':char,'x':round(left,7),'baseline':baseline,'size':size})
            if char==' ':continue
            pen=SVGPathPen(self.glyphs)
            self.glyphs[self.cmap[ord(char)]].draw(TransformPen(pen,
                (size/self.units,0,0,-size/self.units,left,baseline)))
            pieces.append(f'<path data-letter="{escape(char)}" d="{pen.getCommands()}"/>')
        return ''.join(pieces),positions


def build_wordmark(face,kind,pitch=110):
    lines=['Tabernacle of Praise'] if kind=='single-line' else ['Tabernacle','of Praise']
    raw=[]
    for i,line in enumerate(lines):
        body,_=face.draw(line,0,100+i*pitch)
        raw.append((line,ink(body)))
    width=max(b[2]-b[0] for _,b in raw)
    first_top=raw[0][1][1]
    bodies=[];positions=[]
    for i,(line,b) in enumerate(raw):
        x=12-b[0]
        if kind=='centered':x+=(width-(b[2]-b[0]))/2
        body,pos=face.draw(line,x,100+i*pitch+12-first_top)
        bodies.append(body);positions.append({'text':line,'positions':pos})
    body='<g fill="#000000">'+''.join(bodies)+'</g>'
    b=ink(body);box=f'0 0 {width+24:.7f} {b[3]+12:.7f}'
    return body,box,positions,b


def caption(text,x,y,size=18,color='#10494C',weight='400'):
    return f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}">{escape(text)}</text>'


def fit(body,b,x,y,w,h):
    a,c,d,e=b;s=min(w/(d-a),h/(e-c))
    return f'<g transform="translate({x+(w-(d-a)*s)/2-a*s:.7f} {y+(h-(e-c)*s)/2-c*s:.7f}) scale({s:.9f})">{body}</g>'


def main():
    HERE.joinpath('versions').mkdir(exist_ok=True)
    baseline_file=STUDY09/'type-study/specimens/01-open-titlecase-two-line.svg'
    shutil.copyfile(baseline_file,HERE/'versions/v0-review-09-two-line.svg')
    face=Lettering(REFINED)
    outputs={};variants={}
    for kind,file in [('left','wordmark.svg'),('centered','wordmark-centered.svg'),('single-line','wordmark-single-line.svg')]:
        body,box,positions,b=build_wordmark(face,kind)
        (HERE/file).write_text(svg(body,box,'Tabernacle of Praise / '+kind))
        outputs[kind]={'file':file,'viewBox':box,'inkBounds':list(b),'linePositions':positions}
        variants[kind]=(body,b)
    baseline_face=Lettering(BASELINE)
    before,_,_,before_bounds=build_wordmark(baseline_face,'left',pitch=117)
    trial,trial_box,_,_=build_wordmark(face,'left',pitch=107)
    (HERE/'versions/v1-tight-leading-trial.svg').write_text(svg(trial,trial_box,'Tighter line trial, not selected'))
    after,after_bounds=variants['left']
    board='<rect width="1600" height="1180" fill="#F6F3EC"/>'
    board+=caption('Tabernacle of Praise / lettering refinement',50,60,30,weight='600')
    board+=caption('Same family, weight and glyph contours. The refinement is spacing and arrangement.',50,95,17)
    board+=caption('09 baseline',50,153,20,weight='600')
    board+=caption('11 working refinement',840,153,20,weight='600')
    board+=fit(before.replace('#000000','#10494C'),before_bounds,50,185,690,260)
    board+=fit(after.replace('#000000','#10494C'),after_bounds,840,185,690,260)
    board+=caption('117-unit baseline pitch; original pair adjustments.',50,487,17)
    board+=caption('110-unit pitch; more space at rn / cl, slight Ta / Pr easing.',840,487,17)
    board+='<path d="M50 530H1550" stroke="#D9CBB4"/>'
    board+=caption('Single-line arrangement / new functional companion',50,585,23,weight='600')
    body,b=variants['single-line']
    board+=fit(body.replace('#000000','#10494C'),b,70,630,1460,130)
    board+=caption('Full name stays on one baseline for wide headers and signs; no words are reduced.',50,805,17)
    board+=caption('Two-line name at a normal small-use width',50,870,18,weight='600')
    board+=fit(after.replace('#000000','#10494C'),after_bounds,50,900,240,95)
    board+=fit(after.replace('#000000','#F6F3EC'),after_bounds,520,900,240,95)
    # A plain dark field is included before the reversed name, not a mask.
    marker=fit(after.replace('#000000','#F6F3EC'),after_bounds,520,900,240,95)
    board=board.replace(marker,'<rect x="490" y="881" width="310" height="137" fill="#10494C"/>'+marker)
    board+=caption('240 px width / primary on neutral',50,1045,15)
    board+=caption('240 px width / neutral on primary',490,1045,15)
    board+=caption(DRAFT,50,1128,16,weight='600')
    board+=caption('Font-based optical refinement. No custom-drawn glyphs, modified font binaries or final type approval.',50,1155,15)
    (HERE/'lettering-refinement.svg').write_text(svg(board,'0 0 1600 1180','Lettering before and after'))
    subprocess.run(['inkscape',str(HERE/'lettering-refinement.svg'),'--export-type=png',f'--export-filename={HERE/"lettering-refinement.png"}','--export-width=1600'],check=True,capture_output=True)
    metadata={'status':DRAFT,'approval':False,'family':'Instrument Sans','axes':{'wdth':100,'wght':470},
              'fontFile':'../../identity-development-09/type-study/fonts/instrumentsans/InstrumentSans[wdth,wght].ttf',
              'licenseFile':'../../identity-development-09/type-study/fonts/instrumentsans/OFL.txt',
              'fontSHA256':hashlib.sha256(FONT.read_bytes()).hexdigest(),'licenseSHA256':hashlib.sha256(LICENSE.read_bytes()).hexdigest(),
              'glyphContours':'Original unmodified font glyphs; positions are shaped and optically adjusted. Not bespoke type design.',
              'trackingEm':.002,'baselineCorrectionsEm':BASELINE,'workingCorrectionsEm':REFINED,
              'changes':['Baseline pitch reduced from 117 to 110 at size 100, bringing the two lines into a more coherent name unit.',
                         'Ta and Pr eased 0.2 units at size 100; rn opened 0.4 units and cl 0.2 units to retain separate-letter rhythm.',
                         'ac tightened 0.2 units; ra/ai/is moved 0.1 units for adjacent-space balance.',
                         'No word is reduced in size or weight. The full single-line arrangement preserves normal wordspace and all 18 letter contours.'],
              'notSelected':'107-unit pitch trial feels more compressed; preserved rather than adopted.',
              'files':outputs,'proof':'lettering-refinement.png','smallUse':'240 px two-line width shown as a screen proof, not a production minimum. Tiny full-name use still needs larger placements than symbol-only icons.'}
    (HERE/'metadata.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n')
    print('Built 3 reusable full-name masters, preserved baseline/trial and comparison PNG.')


if __name__=='__main__':main()
