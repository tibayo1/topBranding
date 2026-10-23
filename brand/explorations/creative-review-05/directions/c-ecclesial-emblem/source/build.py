from pathlib import Path
import json
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
ROOT=Path(__file__).resolve().parents[1]
STATUS='DRAFT — NOT FOR PUBLICATION'
# All symbol contours below are original manually drawn paths, not raster tracing.
C1='''<path d="M42 66 C48 51 64 47 83 47 H172 C191 47 201 40 205 29 C209 53 195 65 175 65 H122 V195 C122 211 127 218 138 222 H84 C96 215 100 210 100 195 V65 H69 C58 65 50 66 42 72 Z"/>
<path fill-rule="evenodd" d="M137 79 H165 C208 79 226 99 224 128 C222 157 199 172 171 173 C155 174 142 181 131 196 C132 180 139 167 153 157 V103 C153 91 147 84 137 79 Z M174 94 V151 C192 147 203 138 205 124 C207 106 197 95 182 94 Z"/>
<path d="M142 179 V205 C142 215 138 222 130 226 H177 C167 219 164 214 164 202 V171 Z"/>'''
# A broad T and a P whose returning contour is also the eastern edge of an open roundel.
WEST='M123 21 C63 21 18 67 18 127 C18 189 65 236 126 236 C141 236 156 233 169 227 L149 214 C113 222 77 207 56 179 C34 151 34 109 56 79 C72 56 96 43 121 42 C121 34 125 27 132 22 Z'
T='M54 94 C64 76 78 70 99 70 H151 C165 70 174 65 178 55 C180 76 168 87 150 89 H116 V181 C116 197 122 208 134 215 H87 C99 205 101 196 101 181 V102 C101 93 96 89 87 89 C74 89 63 91 54 98 Z'
P='M126 99 C141 99 150 93 162 86 C178 76 195 77 207 90 C221 105 217 126 203 142 C190 156 167 160 152 171 C139 181 141 198 156 207 C173 217 194 208 208 190 C221 174 227 153 227 131 C227 89 199 52 162 40 C155 38 151 32 151 24 C203 35 242 78 242 131 C242 166 224 201 196 222 C175 238 149 234 135 219 C116 199 123 176 141 161 V121 C141 108 135 102 126 99 Z M156 149 C177 141 197 126 197 110 C197 97 185 90 174 96 C160 104 156 118 156 132 Z'
C2=f'<path d="{WEST}"/><path d="{T}"/><path fill-rule="evenodd" d="{P}"/>'
# No initials: upright coupled textile panel; the joining seam opens into an expressive edge.
C3='''<path d="M54 34 H112 V75 L92 95 V171 L112 191 V230 L55 191 C48 186 44 178 44 169 V54 C44 44 47 38 54 34 Z M144 34 H202 C209 38 212 44 212 54 V169 C212 178 208 186 201 191 L144 230 V191 L164 171 V95 L144 75 Z"/>
<path d="M64 34 C78 22 103 20 128 33 C153 20 178 22 192 34 C175 34 157 41 143 54 L128 68 L113 54 C99 41 81 34 64 34 Z"/>
<path d="M112 87 L128 72 L144 87 V165 L128 181 L112 165 Z"/>'''
def svg(name,body,bg=None,view='0 0 256 256'):
 return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view}" role="img"><title>{name} — {STATUS}</title><desc>Original parish identity exploration. Not an official RCCG emblem.</desc>'+ (f'<rect width="100%" height="100%" fill="{bg}"/>' if bg else '')+f'<g fill="currentColor">{body}</g></svg>'
def save(path,data):
 p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(data)
for n,b in [('c1-common-bond',C1),('c2-response-medallion',C2),('c3-coupled-banner',C3)]:save(Path('initials')/(n+'.svg'),svg(n,b))
save(Path('developed/c-developed-v1.svg'),svg('The Joined Roundel — first reconstruction',C2))
# Version 2 follows visual inspection: more generous counters and less decorative T terminal.
# The open enclosing ring is a separate drawn contour. The T and P tails
# overlap it at the base; the three paths are not one continuous ribbon.
WEST2='M132 16 C70 15 18 64 18 128 C18 190 68 240 130 240 C192 240 242 190 242 128 C242 74 203 30 151 18 C151 28 155 35 164 39 C201 53 224 88 224 128 C224 180 182 222 130 222 C78 222 36 180 36 128 C36 79 73 43 120 40 C120 31 125 22 132 16 Z'
T2='M55 94 C65 77 79 71 99 71 H150 C164 71 172 67 178 58 C178 76 166 87 149 89 H115 V180 C115 200 121 215 139 225 L108 230 C101 217 100 201 100 180 V103 C100 93 95 89 87 89 C75 89 64 92 55 98 Z'
P2='M127 101 C141 101 152 94 163 87 C180 77 196 79 208 91 C221 106 217 127 203 142 C190 156 168 160 153 172 C140 182 142 198 157 207 C170 215 185 212 199 203 L201 214 C182 224 157 227 142 216 C124 203 123 187 134 173 C136 168 139 165 141 162 V123 C141 111 136 105 127 101 Z M158 148 C179 140 198 126 198 111 C198 99 187 92 176 98 C162 106 158 119 158 133 Z'
DEV=f'<path d="{WEST2}"/><path d="{T2}"/><path fill-rule="evenodd" d="{P2}"/>'
save(Path('developed/c-developed-v2.svg'),svg('The Joined Roundel',DEV))
# Final optical pass only: remove the angular step where the P stem turns
# into its returning tail. Version 2 remains available for comparison.
P3=P2.replace('C136 168 139 165 141 162 V123', 'C139 167 141 164 141 158 V123')
DEV=f'<path d="{WEST2}"/><path d="{T2}"/><path fill-rule="evenodd" d="{P3}"/>'
save(Path('developed/c-developed-v3.svg'),svg('The Joined Roundel — refined stem-to-tail junction',DEV))
save(Path('developed/c-developed.svg'),svg('The Joined Roundel',DEV))
save(Path('developed/c-developed-reverse.svg'),svg('The Joined Roundel reversed',f'<g fill="white">{DEV}</g>','black'))
# Licensed Noto Serif, outlined review wordmark. Parish name remains complete and readable.
font=TTFont(ROOT.parents[1]/'assets/noto-serif-regular.ttf'); gs=font.getGlyphSet(); cmap=font.getBestCmap(); upm=font['head'].unitsPerEm
hmtx=font['hmtx'].metrics

def textpath(text,size,x,y,tracking=0):
 out=[];cursor=x;scale=size/upm
 for c in text:
  g=cmap[ord(c)];pen=SVGPathPen(gs);gs[g].draw(pen)
  out.append(f'<path transform="translate({cursor:.3f} {y}) scale({scale:.6f} {-scale:.6f})" d="{pen.getCommands()}"/>')
  cursor+=hmtx[g][0]*scale+tracking
 return ''.join(out),cursor-x

a,wa=textpath('Tabernacle',52,298,111,-.15)
b,wb=textpath('of Praise',52,298,170,-.15)
lock=f'<g transform="translate(12 8) scale(.9)">{DEV}</g><g>{a}{b}</g>'
save(Path('developed/c-lockup-horizontal.svg'),svg('The Joined Roundel with parish name',lock,view='0 0 640 256'))
save(Path('developed/c-lockup-horizontal-reverse.svg'),svg('The Joined Roundel with parish name reversed',f'<g fill="white">{lock}</g>','black',view='0 0 640 256'))
# A presentation diagram, not an alternate logo: expose the separate ring
# honestly instead of implying that the final emblem is one ribbon.
construction=''
for x,label,body in [
 (80,'Open enclosure',f'<path d="{WEST2}"/>'),
 (440,'Drawn T + P',f'<path d="{T2}"/><path fill-rule="evenodd" d="{P3}"/>'),
 (800,'Joined at the base',DEV),
]:
 construction+=f'<g transform="translate({x} 32)">{body}</g><text x="{x+128}" y="330" text-anchor="middle" font-family="sans-serif" font-size="17">{label}</text>'
construction+='<text x="570" y="378" text-anchor="middle" font-family="sans-serif" font-size="14">Three drawn contours; the ring remains a separate enclosure.</text><text x="570" y="413" text-anchor="middle" font-family="sans-serif" font-size="12" letter-spacing="2">DRAFT — NOT FOR PUBLICATION</text>'
save(Path('developed/c-construction.svg'),svg('The Joined Roundel — actual construction',construction,'white','0 0 1140 440'))
# Sketch review sheet; labels here are presentation text, symbol sources remain all paths.
labels=['C1 — Common Bond','C2 — Response Medallion','C3 — Coupled Banner']
bodies=[C1,C2,C3]
body=''
for i,(label,b) in enumerate(zip(labels,bodies)):
 x=60+i*380
 body+=f'<g transform="translate({x} 52)">{b}</g><text x="{x+128}" y="350" text-anchor="middle" font-family="sans-serif" font-size="17">{label}</text>'
body+='<text x="570" y="396" text-anchor="middle" font-family="sans-serif" font-size="12" letter-spacing="2">DRAFT — NOT FOR PUBLICATION</text>'
save(Path('c-initial-sketches.svg'),svg('Three distinct emblem investigations',body,'white','0 0 1140 430'))
