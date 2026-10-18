from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import subprocess
P=Path(__file__).resolve().parent
F='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
DRAFT='DRAFT — NOT FOR PUBLICATION'
paths={
'new-B14-passing-fold':('Passing Fold','M 25 101 C 68 72 108 79 142 106 C 178 134 194 167 232 171 L 220 207 C 184 211 157 171 139 151 C 109 120 66 126 25 151 Z M 83 139 C 63 149 56 167 66 184 C 83 211 132 219 190 209 L 208 188 C 160 190 116 176 83 139 Z M 151 104 C 181 83 187 39 232 37 V 78 C 205 82 193 115 172 132 Z'),
'new-B15-gathering-passage':('Gathering Passage','M 24 104 C 65 78 106 81 140 108 C 175 135 191 168 232 173 L 221 207 C 183 207 157 172 138 152 C 107 122 65 129 24 152 Z M 82 141 C 63 154 60 170 70 185 C 88 211 133 215 189 204 L 204 184 C 158 188 115 175 82 141 Z M 151 104 C 180 85 185 41 230 38 V 78 C 204 84 191 114 170 131 Z'),
'new-B16-gathered-response':('Gathered Response','M 24 100 C 65 76 105 78 140 105 C 176 132 191 163 232 168 L 222 202 C 183 204 157 170 137 150 C 106 122 65 127 24 150 Z M 82 140 C 63 152 59 167 70 182 C 89 207 136 212 189 202 L 203 184 C 157 187 115 173 82 140 Z M 150 102 C 178 83 186 40 231 37 V 76 C 204 82 192 112 169 129 Z')
}
def svg(name,d,fill='#000000'):
 return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" role="img" aria-labelledby="title"><title id="title">B / {name} — {DRAFT}</title><desc>Original direction B. A broad sheltering fold passes over a returning surface; the return continues upward beyond the crossing. The opening is made by the same gesture.</desc><path fill="{fill}" d="{d}"/></svg>\n'
board=Image.new('RGB',(1500,700),'white');dr=ImageDraw.Draw(board)
font=ImageFont.truetype(F,20);small=ImageFont.truetype(F,14);dr.text((24,20),DRAFT,font=small,fill='black')
for i,(stem,(name,d)) in enumerate(paths.items()):
 (P/(stem+'.svg')).write_text(svg(name,d));subprocess.run(['inkscape',str(P/(stem+'.svg')),'--export-type=png',f'--export-filename={P/(stem+".png")}','--export-width=440'],check=True,capture_output=True)
 im=Image.open(P/(stem+'.png')).convert('RGBA');board.paste(im,(i*500+30,90),im);dr.text((i*500+35,590),name,font=font,fill='black')
board.save(P/'passing-fold-review.png')
