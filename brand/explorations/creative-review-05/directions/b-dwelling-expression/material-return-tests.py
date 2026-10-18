from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import subprocess
P=Path(__file__).resolve().parent
DRAFT='DRAFT — NOT FOR PUBLICATION'; F='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
shapes={
'new-B11-held-response':('Held Response','M 20 48 C 52 48 74 87 106 91 C 121 93 136 85 149 75 L 132 107 C 112 126 92 127 69 113 C 49 101 34 96 20 96 Z M 28 167 C 61 163 78 134 94 108 C 109 82 124 64 147 64 C 174 64 188 94 207 119 C 220 135 230 143 241 140 V 179 C 217 182 199 172 183 155 C 162 187 135 202 105 194 C 71 185 58 176 28 185 Z M 84 162 C 105 176 134 176 157 150 C 145 132 137 121 125 123 C 111 126 101 149 84 162 Z'),
'new-B12-opening-interval':('Opening Interval','M 23 43 C 57 45 83 87 114 87 C 127 87 138 83 149 74 L 132 107 C 109 126 88 124 65 109 C 46 96 34 91 23 92 Z M 30 173 C 61 167 77 131 96 104 C 111 82 129 62 151 65 C 179 68 192 101 211 126 C 221 139 230 146 240 144 V 183 C 217 188 198 178 181 161 C 158 194 133 205 108 196 C 92 191 79 181 64 177 C 48 175 39 182 30 183 Z M 83 166 C 103 183 129 183 155 153 C 144 135 136 123 124 124 C 108 126 100 149 83 166 Z'),
'new-B13-common-turn':('Common Turn','M 24 48 C 56 48 77 89 109 93 C 123 95 137 88 150 78 L 130 112 C 110 131 88 129 65 114 C 46 102 34 96 24 96 Z M 32 173 C 65 168 80 138 97 111 C 114 85 132 66 153 70 C 176 74 188 99 204 122 C 217 140 228 150 240 146 V 182 C 218 187 199 176 184 161 C 163 190 139 202 112 196 C 83 190 63 179 32 190 Z M 84 165 C 107 177 132 177 159 151 C 147 134 139 123 127 125 C 113 127 103 151 84 165 Z'),
}
def svg(name,d,fill='#000000'):
 return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" role="img" aria-labelledby="title"><title id="title">B / {name} — {DRAFT}</title><desc>Two broad counter-moving surfaces shelter one shared interval and open in collective response. Original exploratory construction.</desc><path fill="{fill}" fill-rule="evenodd" d="{d}"/></svg>\n'
board=Image.new('RGB',(1500,700),'white');draw=ImageDraw.Draw(board)
font=ImageFont.truetype(F,20);small=ImageFont.truetype(F,14);draw.text((24,20),DRAFT,font=small,fill='black')
for i,(stem,(name,d)) in enumerate(shapes.items()):
 (P/(stem+'.svg')).write_text(svg(name,d))
 subprocess.run(['inkscape',str(P/(stem+'.svg')),'--export-type=png',f'--export-filename={P/(stem+".png")}','--export-width=440'],check=True,capture_output=True)
 im=Image.open(P/(stem+'.png')).convert('RGBA');board.paste(im,(i*500+30,90),im)
 draw.text((i*500+35,590),name,font=font,fill='black')
board.save(P/'integral-return-review.png')
