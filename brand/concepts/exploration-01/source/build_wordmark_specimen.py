"""Common comparison lettering only; no typeface decision is approved."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

out = Path(__file__).resolve().parent.parent
font_path = '/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf'
font = TTFont(font_path)
glyphs, cmap = font.getGlyphSet(), font.getBestCmap()
scale = 58 / font['head'].unitsPerEm
fragments = []
for line, baseline in [('Tabernacle', 108), ('of Praise', 184)]:
    x = 300
    for char in line:
        name = cmap[ord(char)]
        pen = SVGPathPen(glyphs)
        glyphs[name].draw(TransformPen(pen, (scale, 0, 0, -scale, x, baseline)))
        if pen.getCommands():
            fragments.append(f'<path d="{pen.getCommands()}"/>')
        x += (font['hmtx'][name][0] * scale) - 0.35

for name in ('a-folded-sanctuary', 'b-sanctuary-strings', 'c-praise-ligature'):
    raw = (out / f'{name}-v3.svg').read_text()
    symbol = raw[raw.index('<g id="symbol"'):raw.index('</g>') + 4]
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 650 256" width="650" height="256">'
           '<title>Tabernacle of Praise — DRAFT comparison lockup</title>'
           '<desc>DRAFT — NOT FOR PUBLICATION. Noto Sans Regular, SIL OFL, common comparison specimen only; '
           'font, typography, spacing and lockup not approved.</desc>'
           f'{symbol}<g id="wordmark-specimen" fill="#000000">{"".join(fragments)}</g></svg>\n')
    (out / f'{name}-comparison-lockup.svg').write_text(svg)
