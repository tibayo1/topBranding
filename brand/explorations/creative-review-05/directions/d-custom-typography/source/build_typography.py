#!/usr/bin/env python3
"""Creative Review 05 / D — bespoke wordmark studies, DRAFT.

The resulting logo artwork combines original letter drawings with licensed
Source Serif 4 or Instrument Sans outlines. No font binary is edited.
Run from any directory with Python 3, fontTools and Pillow/libraqm.
"""
from pathlib import Path
from html import escape
import json
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from PIL import ImageFont

HERE = Path(__file__).resolve().parents[1]
STUDY = HERE.parents[1]
OLD = STUDY.parent / 'strategic-study-04'
STATUS = 'DRAFT — NOT FOR PUBLICATION'


class Face:
    def __init__(self, family, filename, axes):
        self.file = STUDY / 'assets/fonts' / family / filename
        if not self.file.is_file():
            self.file = OLD / 'assets/fonts' / family / filename
        self.font = TTFont(self.file)
        self.gs = self.font.getGlyphSet(location=axes)
        self.cmap = self.font.getBestCmap()
        self.upm = self.font['head'].unitsPerEm
        self.pil = ImageFont.truetype(str(self.file), 1000)
        self.pil.set_variation_by_axes([axes.get(a.axisTag, a.defaultValue) for a in self.font['fvar'].axes])

    def width(self, text):
        return self.pil.getlength(text) * self.upm / 1000

    def glyph(self, c):
        pen = SVGPathPen(self.gs, ntos=lambda v: str(round(v, 2)))
        self.gs[self.cmap[ord(c)]].draw(pen)
        return pen.getCommands()

    def text(self, text, x, y, size=1000, custom=None, kern=None):
        custom, kern = custom or {}, kern or {}
        result, extra = [], 0
        for i, c in enumerate(text):
            if i:
                extra += kern.get(text[i-1:i+1], 0)
            if c == ' ':
                continue
            at = self.width(text[:i+1])-self.width(c)+extra
            d = custom.get(c, self.glyph(c))
            rule = 'evenodd' if c in custom else 'nonzero'
            result.append(f'<path data-letter="{escape(c)}" data-drawn="{str(c in custom).lower()}" fill-rule="{rule}" d="{d}" transform="translate({x+at*size/self.upm:.3f} {y}) scale({size/self.upm:.5f} {-size/self.upm:.5f})"/>')
        return ''.join(result), (self.width(text)+extra)*size/self.upm


serif = Face('sourceserif4', 'SourceSerif4[opsz,wght].ttf', {'wght':550,'opsz':24})
sans = Face('instrumentsans', 'InstrumentSans[wdth,wght].ttf', {'wght':550,'wdth':100})

# D1: counters are drawn first, not icons inserted into inherited letters.
# The P, a and e have an interior floor that rises to the right; the terminal
# of a/r/e repeats that release. Every bowl is still a familiar readable bowl.
OPEN_V1 = {
 'T': 'M25 665H585L590 510H549C536 578 519 615 461 615H364V100C364 63 381 55 454 43V0H151V43C222 55 244 63 244 100V615H149C91 615 74 578 61 510H20Z',
 'P': 'M40 665H303C477 665 567 602 567 477C567 357 473 287 301 287H244V101C244 64 269 56 337 43V0H40V43C104 55 126 65 126 101V564C126 602 103 611 40 622ZM244 616V337H294C400 337 447 393 447 477C447 572 399 616 300 616Z',
 'a': 'M76 393L86 447C140 478 194 489 258 489C368 489 419 438 419 321V95C419 58 431 43 451 43C465 43 477 53 488 67L509 46C485 6 462-13 421-13C364-13 328 14 318 69C273 20 229-14 172-14C91-14 40 29 40 110C40 192 101 234 215 266L314 296V327C314 409 292 444 236 444C197 444 159 424 121 378ZM314 256L237 228C170 205 148 172 148 129C148 82 174 56 215 56C249 56 281 76 314 111Z',
 'e': 'M472 103C428 29 370-14 278-14C138-14 40 79 40 232C40 388 142 489 273 489C390 489 464 410 464 294C464 275 463 258 459 242L153 224C162 119 220 61 310 61C364 61 411 86 449 126ZM153 272L351 293C366 351 349 443 273 443C211 443 161 382 153 272Z',
 'r': 'M36 0V38L103 53V383L29 394V428L188 489L204 478L213 367C242 444 294 489 352 489C386 489 412 475 429 449L405 386C374 397 350 408 326 425C278 408 240 362 213 291V54L295 38V0Z',
}

# A controlled revision increases the rising counter-floor and opens the
# a/e exits. It does not move whole letters off the baseline.
OPEN_V2 = dict(OPEN_V1)
OPEN_V2['P'] = 'M40 665H303C475 665 566 602 566 477C566 356 471 284 301 284H244V101C244 64 269 56 337 43V0H40V43C104 55 126 65 126 101V564C126 602 103 611 40 622ZM244 616V334L304 345C403 364 446 412 446 485C446 573 398 616 300 616Z'
OPEN_V2['e'] = 'M475 112C428 29 370-14 278-14C138-14 40 79 40 232C40 388 142 489 273 489C390 489 465 411 465 295C465 278 464 262 461 248L153 224C162 119 220 61 310 61C365 61 411 87 451 136ZM153 273L351 300C364 360 347 443 273 443C211 443 161 382 153 273Z'
OPEN_V2['a'] = 'M71 394L86 447C140 478 194 489 258 489C368 489 419 438 419 321V95C419 58 431 43 451 43C466 43 479 55 491 72L513 51C488 7 463-13 421-13C364-13 328 14 318 69C273 20 229-14 172-14C91-14 40 29 40 110C40 192 101 234 215 266L314 296V327C314 409 292 444 236 444C196 444 156 422 116 371ZM314 256L237 228C170 205 148 172 148 129C148 82 174 56 215 56C249 56 281 76 314 111Z'
# f now follows the same non-ball, outward terminal rule as r and a.
OPEN_V2['f'] = 'M27 0V38L108 53V421H27V466H108V510C108 670 174 746 281 746C329 746 363 729 382 700L357 643C324 653 306 678 283 700C244 683 220 637 220 550V466H350V421H220V54L309 38V0Z'


def document(name, inner, width, height, desc):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:.2f} {height:.2f}" role="img" aria-labelledby="title desc"><title id="title">D — {escape(name)} — Tabernacle of Praise — DRAFT</title><desc id="desc">{STATUS}. {escape(desc)}</desc><g fill="#000000" fill-rule="evenodd">{inner}</g></svg>\n'


def open_wordmark(version=2, stacked=False):
    custom = OPEN_V2 if version>=2 else OPEN_V1
    # V3 retains V2 lettering exactly. Extra top padding accommodates the
    # inherited b/l ascenders, which exceeded the old canvas by 16 units.
    top_pad = 40 if version>=3 else 0
    kern = {'Ta':-12, 'be':-4, 'er':-3, 'rn':-10, 'na':-9, 'ac':-5, 'cl':-6, 'le':-5, 'Pr':-14, 'ra':-11, 'ai':-3, 'se':-4}
    if stacked:
        first, w1 = serif.text('Tabernacle', 55, 730+top_pad, 1000, custom, kern)
        second, w2 = serif.text('of Praise', 55, 1600+top_pad, 1000, custom, kern)
        # A real common left edge; the shorter line is not expanded to fit.
        return first+second, max(w1,w2)+110, 1680+top_pad
    inner, width = serif.text('Tabernacle of Praise', 55, 730+top_pad, 1000, custom, kern)
    return inner, width+110, 810+top_pad


# D2: one shared baseline stem between a shoulder and the next a. The name
# is deliberately denser than D1. These are trial ligatures, not hidden icons.
def joined_sketch():
    # Instrument Sans UPM is 1000. The a is independently redrawn with a
    # single-storey, open-shouldered contour. Stems bridge n/a and r/a.
    cust = {
      'a':'M423 0H336V63C300 16 254-10 193-10C84-10 26 70 26 244C26 414 91 507 204 507C263 507 305 482 336 438V497H423ZM336 252C336 365 301 424 231 424C158 424 122 359 122 245C122 130 155 73 223 73C296 73 336 140 336 252Z',
      'T':'M20 700H599V610H359V0H260V610H20Z',
      'P':'M70 0V700H332C490 700 565 626 565 489C565 349 483 276 330 276H170V0ZM170 609V368H324C419 368 463 405 463 489C463 571 423 609 328 609Z',
    }
    first,w1=sans.text('Tabernacle',50,740,1000,cust,{'na':-15})
    second,w2=sans.text('of Praise',50,1600,1000,cust,{'ra':-15})
    # These trial joins are literal drawn contact between the real letters.
    na_x = 50+sans.width('Tabern')-15
    ra_x = 50+sans.width('of Pr')-15
    first += f'<path data-ligature="na" d="M{na_x-37} 708Q{na_x+12} 689 {na_x+56} 654L{na_x+56} 720Q{na_x+11} 746 {na_x-37} 740Z"/>'
    second += f'<path data-ligature="ra" d="M{ra_x-45} 1568Q{ra_x+12} 1549 {ra_x+57} 1514L{ra_x+57} 1580Q{ra_x+11} 1606 {ra_x-45} 1600Z"/>'
    return first+second,max(w1,w2)+100,1680


# D3: an original, incised capital alphabet in normalized 100-unit cap-height.
# Wedge ends and chamfered counters form the language throughout the name.
CAPS = {
'T':(69,'M0 100H69V90L42 87V0H28V87L0 90Z'),
'A':(74,'M0 0L30 100H44L75 0H60L51 30H23L14 0ZM26 40H48L37 78Z'),
'B':(64,'M5 0V100H32C51 100 61 91 61 76C61 64 55 56 45 53C58 50 65 41 65 27C65 9 52 0 32 0ZM19 90V58H31C43 58 48 65 48 75C48 86 42 90 31 90ZM19 48V10H31C45 10 51 17 51 28C51 41 44 48 31 48Z'),
'E':(58,'M5 0V100H58V90L19 87V57H50V46H19V13L59 10V0Z'),
'R':(68,'M5 0V100H32C54 100 65 89 65 71C65 56 57 47 44 43L70 0H54L30 41H19V0ZM19 90V51H30C44 51 51 58 51 71C51 84 44 90 31 90Z'),
'N':(75,'M5 0V100H18L62 26V100H73V0H61L16 75V0Z'),
'C':(70,'M67 84L59 76C53 87 46 92 36 92C20 92 13 76 13 50C13 22 21 8 37 8C47 8 56 15 62 27L70 20C62 5 50-3 35-3C11-3-2 17-2 50C-2 83 13 103 36 103C50 103 61 96 67 84Z'),
'L':(58,'M5 100H19V13L58 10V0H5Z'),
'O':(73,'M36 103C61 103 75 83 75 50C75 17 61-3 36-3C11-3-2 17-2 50C-2 83 11 103 36 103ZM36 92C20 92 13 77 13 50C13 23 20 8 36 8C52 8 60 23 60 50C60 77 52 92 36 92Z'),
'F':(57,'M5 0V100H58V90L19 87V56H50V45H19V0Z'),
'P':(65,'M5 0V100H32C54 100 65 89 65 70C65 50 53 40 32 40H19V0ZM19 90V51L32 54C45 57 51 61 51 71C51 84 44 90 31 90Z'),
'I':(27,'M6 100H20V0H6Z'),
'S':(60,'M54 82L45 76C43 87 37 93 28 93C17 93 11 86 11 77C11 64 21 60 33 54C48 47 58 40 58 24C58 7 46-3 28-3C14-3 3 4-1 18L9 25C12 12 19 7 29 7C40 7 46 14 46 23C46 35 37 39 25 45C10 52 0 60 0 76C0 92 12 103 29 103C41 103 50 96 54 82Z'),
}


def caps_line(text,x,y):
    inner=''; pos=x
    for c in text:
        if c==' ': pos+=30;continue
        advance,d=CAPS[c]
        inner+=f'<path data-letter="{c}" data-drawn="true" d="{d}" transform="translate({pos} {y}) scale(1 -1)"/>'
        pos+=advance+9
    return inner,pos-x-9


def build():
    for folder in ('sketches','developed','proofs'):
        (HERE/folder).mkdir(parents=True,exist_ok=True)
    a,w,h=open_wordmark(1,True)
    (HERE/'sketches/D1-open-counter.svg').write_text(document('D1 — Open Counter',f'<g transform="translate(0 40)">{a}</g>',w,h+40,'Original T/P/a/e/r drawings form an inward bowl and rising release within familiar serif word shapes. Remaining letters use licensed Source Serif 4 outlines.'))
    b,w,h=joined_sketch()
    (HERE/'sketches/D2-joined-voices.svg').write_text(document('D2 — Joined Voices',f'<g transform="translate(0 40)">{b}</g>',w,h+40,'Two trial na/ra baseline ligatures join different letter structures through a common movement. Original T/P/a; remaining Instrument Sans outlines. This exploratory join may reduce word recognition.'))
    c,w1=caps_line('TABERNACLE',18,126)
    c2,w2=caps_line('OF PRAISE',18,253)
    (HERE/'sketches/D3-inscribed-response.svg').write_text(document('D3 — Inscribed Response',c+c2,max(w1,w2)+36,278,'Original capital alphabet with tapered incised ends, open spacing, and asymmetric P counter. A monumental response, with the risk of a cultural institution rather than a welcoming parish.'))
    for version in (1,2,3):
        for stacked in (False,True):
            a,w,h=open_wordmark(version,stacked)
            suffix='stacked' if stacked else 'horizontal'
            drawn = 'T/P/a/e/r/f' if version>=2 else 'T/P/a/e/r'
            master=document(f'Open Counter — {suffix} v{version}',a,w,h,f'Original {drawn} letter drawings combined with unchanged licensed Source Serif 4 weight 550 / optical size 24 outlines for b/c/l/n/o/i/s. Repeated enclosed bowls, rising counter floors, and outward-cut terminals are the identity-specific letter grammar. The complete name is read before the association is explained. No extended roof, shifted baseline, or monogram.')
            (HERE/f'developed/open-counter-{suffix}-v{version}.svg').write_text(master)
            if version>=2:
                (HERE/f'developed/open-counter-{suffix}-reverse-v{version}.svg').write_text(master.replace('#000000','#ffffff'))
    # Construction detail juxtaposes complete real glyphs, not symbolic dots.
    construction=''
    for c,x in [('T',70),('P',820),('a',1540),('e',2180),('r',2800),('f',3340)]:
        construction+=f'<path data-letter="{c}" d="{OPEN_V2[c]}" transform="translate({x} 750) scale(1 -1)"/>'
    (HERE/'developed/open-counter-construction.svg').write_text(document('Open Counter — letter construction',construction,3810,840,'The six original edited letter drawings isolated at a common baseline. P/a/e retain enclosed counters and repeat a counter floor rising toward the right. T has normal cap proportions. The r/f terminal replaces a ball with the same outward wedge.'))
    print('Built 3 initial typographic ideas, 3 horizontal/stacked development passes, and construction detail.')


if __name__=='__main__':
    build()
