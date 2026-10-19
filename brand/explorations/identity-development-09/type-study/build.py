#!/usr/bin/env python3
"""Build provisional outlined companion lettering; retain original font binaries.

No glyph is redrawn or distorted. Pillow/libraqm supplies normal kerning, with
small documented pair adjustments added before each following glyph. The three
specimens are alternatives for review, not an approved typography system.
"""
from pathlib import Path
from html import escape
import hashlib
import json
import re
import shutil
import subprocess
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.svgLib.path import parse_path
from PIL import ImageFont

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
STUDY04 = REPO / 'brand/explorations/strategic-study-04'
PAIR08 = REPO / 'brand/explorations/team-pair-08'
DRAFT = 'DRAFT — NOT FOR PUBLICATION'

STYLES = [
    dict(id='01-open-titlecase', name='Open title case', family='Instrument Sans',
         folder='instrumentsans', file='InstrumentSans[wdth,wght].ttf',
         axes={'wdth':100, 'wght':470}, tracking=0.002,
         corrections={'Ta':-0.012,'er':-0.003,'rn':0.004,'cl':0.005,
                      'Pr':-0.010,'ra':-0.004,'ai':-0.003,'is':0.003},
         lines=['Tabernacle','of Praise'],
         voice='Clear, open and welcoming. Keeps the familiar word shapes.'),
    dict(id='02-measured-capitals', name='Measured capitals', family='Instrument Sans',
         folder='instrumentsans', file='InstrumentSans[wdth,wght].ttf',
         axes={'wdth':100, 'wght':500}, tracking=0.085,
         corrections={'TA':-0.018,'AB':-0.005,'RA':-0.012,'AC':-0.006,
                      'CL':-0.004,'PR':-0.006,'AI':-0.010},
         lines=['TABERNACLE','OF PRAISE'],
         voice='Composed, compact and ceremonial. More formal than title case.'),
    dict(id='03-warm-serif', name='Warm serif', family='Source Serif 4',
         folder='sourceserif4', file='SourceSerif4[opsz,wght].ttf',
         axes={'opsz':24, 'wght':500}, tracking=0.002,
         corrections={'Ta':-0.005,'rn':0.003,'cl':0.002,
                      'Pr':-0.005,'ra':-0.003,'ai':-0.002},
         lines=['Tabernacle','of Praise'],
         voice='Warm and literary, with a quieter institutional association.'),
]


def svg(inner, viewbox, title, description=''):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}" role="img" '
            f'aria-label="{escape(title, quote=True)}"><title>{escape(title)}</title>'
            f'<desc>{DRAFT}. {escape(description)}</desc>{inner}</svg>\n')


class Lettering:
    def __init__(self, settings):
        self.settings = settings
        self.path = ROOT / 'fonts' / settings['folder'] / settings['file']
        self.font = TTFont(self.path)
        self.glyphs = self.font.getGlyphSet(location=settings['axes'])
        self.cmap = self.font.getBestCmap()
        self.units = self.font['head'].unitsPerEm
        self.shaper = ImageFont.truetype(str(self.path), 1000,
                                         layout_engine=ImageFont.Layout.RAQM)
        self.shaper.set_variation_by_axes([settings['axes'][a.axisTag]
                                          for a in self.font['fvar'].axes])

    def length(self, text):
        return self.shaper.getlength(text, features=['-liga','-clig'])

    def draw(self, text, x, baseline, size=100):
        pieces, positions = [], []
        adjustment = 0
        for i, char in enumerate(text):
            if i:
                adjustment += self.settings['corrections'].get(text[i-1:i+1], 0)
            advance = (self.length(text[:i+1])-self.length(char))/1000
            advance += i*self.settings['tracking']+adjustment
            left = x+advance*size
            positions.append({'character':char,'x':round(left,5),
                              'baseline':baseline, 'size':size})
            if char != ' ':
                pen = SVGPathPen(self.glyphs)
                self.glyphs[self.cmap[ord(char)]].draw(TransformPen(pen,
                    (size/self.units,0,0,-size/self.units,left,baseline)))
                pieces.append(f'<path data-letter="{escape(char, quote=True)}" d="{pen.getCommands()}"/>')
        return '<g fill="#000000">'+''.join(pieces)+'</g>', positions

    def width(self, text, size=100):
        correction = sum(self.settings['corrections'].get(text[i-1:i+1],0)
                         for i in range(1,len(text)))
        return (self.length(text)/1000+(len(text)-1)*self.settings['tracking']+correction)*size


def read_art(path):
    raw = path.read_text()
    box = re.search(r'viewBox="([^"]+)"', raw)[1]
    inner = re.sub(r'<(?:title|desc)\b[^>]*>.*?</(?:title|desc)>', '', raw, flags=re.S)
    inner = re.sub(r'^.*?<svg\b[^>]*>|</svg>\s*$', '', inner, flags=re.S)
    inner = re.sub(r'\s(?:id|aria-labelledby)="[^"]*"','',inner)
    return inner.replace('currentColor','#000000'), box


def ink_box(mark):
    pen = BoundsPen(None)
    for d in re.findall(r'<path\b[^>]*\bd="([^"]+)"', mark):
        parse_path(d, pen)
    assert pen.bounds
    x0,y0,x1,y1=pen.bounds
    return (x0,y0,x1-x0,y1-y0)


def fit(mark, box, x, y, w, h):
    a,b,sw,sh = box
    scale=min(w/sw,h/sh)
    tx=x+(w-sw*scale)/2-a*scale
    ty=y+(h-sh*scale)/2-b*scale
    return f'<g transform="translate({tx:.6f} {ty:.6f}) scale({scale:.9f})">{mark}</g>'


def caption(text,x,y,size=18,fill='#444444',weight='400'):
    return (f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" '
            f'font-size="{size}" font-weight="{weight}" fill="{fill}">{escape(text)}</text>')


def main():
    ROOT.joinpath('specimens').mkdir(exist_ok=True)
    ROOT.joinpath('lockup-tests').mkdir(exist_ok=True)
    for family in ['instrumentsans','sourceserif4']:
        source = STUDY04 / 'assets/fonts' / family
        target = ROOT / 'fonts' / family
        target.mkdir(parents=True, exist_ok=True)
        for file in source.iterdir():
            shutil.copyfile(file, target/file.name)
            assert (target/file.name).read_bytes()==file.read_bytes()
    symbols=[]
    for folder,name in [('shared-rhythm','Shared Rhythm'),('second-direction','Open Praise')]:
        mark,_=read_art(PAIR08/folder/'primary.svg')
        symbols.append((folder,name,mark,ink_box(mark)))
    records=[]
    board='<rect width="1480" height="1500" fill="#ffffff"/>'
    board+=caption('Tabernacle of Praise',64,64,32,'#111111','600')
    board+=caption('COMPANION LETTERING • THREE PROVISIONAL APPROACHES',64,103,15)
    board+=caption('Shared Rhythm',64,163,22,'#111111','600')
    board+=caption('Open Praise',790,163,22,'#111111','600')
    for row, style in enumerate(STYLES):
        face=Lettering(style)
        y=195+row*390
        full=' '.join(style['lines'])
        horizontal,pos=face.draw(full,8,100)
        hwidth=face.width(full)+16
        horizontal_file=f"specimens/{style['id']}-single-line.svg"
        (ROOT/horizontal_file).write_text(svg(horizontal, f'0 0 {hwidth:.5f} 126',
             f"{style['name']} / full-name single line",f"{style['family']}, original glyph contours; shaped and optically spaced. No font or identity approved."))
        twoline=''
        line_positions=[]
        widths=[face.width(line) for line in style['lines']]
        twidth=max(widths)+16
        for line,baseline in zip(style['lines'],[100,217]):
            out,positions=face.draw(line,8,baseline)
            twoline+=out
            line_positions.append({'text':line,'positions':positions})
        two_file=f"specimens/{style['id']}-two-line.svg"
        (ROOT/two_file).write_text(svg(twoline, f'0 0 {twidth:.5f} 243',
             f"{style['name']} / full-name two lines",f"{style['family']}, original glyph contours; shaped and optically spaced. Both lines use equal size and weight; 'of' stays readable."))
        ti=ink_box(twoline)
        testfiles={}
        for col,(folder,name,mark,mbox) in enumerate(symbols):
            # Native font outline sizes are not distorted. All names occupy a
            # common 330-unit-wide region; symbols share 126-unit ink height.
            test=fit(mark,mbox,28,49,146,148)
            test+=fit(twoline,ti,224,43,352,167)
            file=f"lockup-tests/{folder}-{style['id']}.svg"
            (ROOT/file).write_text(svg(test,'0 0 620 256',
                 f"{name} / {style['name']} / temporary lockup",
                 'Unchanged Review 08 symbol and font-based companion lettering. No third logo proposed.'))
            testfiles[folder]=file
            x=64+col*726
            board+=f'<line x1="{x}" y1="{y}" x2="{x+626}" y2="{y}" stroke="#dddddd"/>'
            board+=caption(f"0{row+1}   {style['name']}",x,y+36,20,'#111111','600')
            board+=f'<svg x="{x}" y="{y+56}" width="626" height="258" viewBox="0 0 620 256">{test}</svg>'
            board+=caption(f"{style['family']} • weight {style['axes']['wght']}",x,y+337,15)
            board+=caption(['Readable, welcoming title case.','Measured capitals; stronger formal tone.','Warmer serif; more literary character.'][row],x,y+362,15)
        records.append({**style,'singleLineFile':horizontal_file,'twoLineFile':two_file,
                        'singleLineViewBox':f'0 0 {hwidth:.5f} 126',
                        'twoLineViewBox':f'0 0 {twidth:.5f} 243',
                        'singleLinePositions':pos,'linePositions':line_positions,
                        'twoLineInkBounds':list(ti),'lockupTests':testfiles,
                        'fontFile':f"fonts/{style['folder']}/{style['file']}",
                        'licenseFile':f"fonts/{style['folder']}/OFL.txt",
                        'fontSHA256':hashlib.sha256(face.path.read_bytes()).hexdigest()})
    board+=caption(DRAFT,64,1450,15,'#111111','600')
    board+=caption('Font-based lettering studies. No glyph redraw, font binary modification or typography approval.',64,1477,15)
    (ROOT/'typographic-comparison.svg').write_text(svg(board,'0 0 1480 1500',
            'Three companion-lettering approaches for both proposed logos',
            'Matching symbol ink scale and name area. Type is original licensed glyph contours, with measured pair-spacing adjustments.'))
    metadata={'status':DRAFT,'fontsUnmodified':True,'letteringClassification':'Licensed, shaped font outlines with optical spacing; not bespoke type design.',
              'recommendations':{
                 'shared-rhythm':{'style':'01-open-titlecase','provisional':True,
                    'reason':'The familiar lowercase shapes soften the unequal folded architecture and preserve the clean, readable full-name feel of the previous praise study.'},
                 'open-praise':{'style':'01-open-titlecase','alternative':'02-measured-capitals','provisional':True,
                    'reason':'Title case is the stronger working default for welcome and immediate name recognition. Capitals offer a compact, formal alternative but risk making the TP emblem feel civic or institutional.'}},
              'specimens':records,
              'comparisonNote':'Both columns use the unchanged Review 08 master art. Symbols are fitted to the same ink field; full-name wordmarks share a common width area without nonuniform scaling. These are layout comparisons, not size standards.'}
    (ROOT/'metadata.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n')
    subprocess.run(['inkscape',str(ROOT/'typographic-comparison.svg'),
                    '--export-type=png',f'--export-filename={ROOT/"typographic-comparison.png"}',
                    '--export-width=1480'],check=True,capture_output=True)
    print('Built 6 outlined wordmark specimens, 6 paired comparisons and one preview board.')


if __name__=='__main__':
    main()
