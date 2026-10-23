"""Responsive Cover development. Generated material study informed the v4 folds.
Original hypothesis and intermediate vectors remain visible; no reference logo traced.
DRAFT — NOT FOR PUBLICATION.
"""
from pathlib import Path
from html import escape
ROOT=Path(__file__).resolve().parents[1]
VERSIONS={
'v2':[
'M24 208 C36 162 70 148 104 126 C126 112 142 88 152 52 C170 76 190 92 216 102 C180 122 154 150 130 184 C120 198 138 210 166 216 C112 216 66 218 24 208 Z',
'M184 86 C210 88 236 80 256 56 C264 88 282 112 304 130 L244 110 L286 134 C316 148 330 180 336 208 C288 218 242 218 196 216 C226 214 242 208 240 196 C234 170 218 146 196 122 Z'],
'v3':[
'M24 208 C36 162 70 148 104 126 C126 112 142 88 152 52 C158 74 170 90 188 104 C160 124 136 150 116 184 C106 198 128 210 166 216 C112 216 66 218 24 208 Z',
'M184 86 C210 88 236 80 256 56 C264 88 282 112 304 130 L244 110 L286 134 C316 148 330 180 336 208 C288 218 242 218 196 216 C226 214 242 208 240 196 C234 170 218 146 196 122 Z'],
'v4':[
'M152 44 C162 68 178 86 194 96 C170 112 132 130 80 148 L84 136 C108 110 132 76 152 44 Z',
'M80 160 C56 166 32 184 24 216 C68 224 120 224 168 224 C126 222 110 216 116 200 C130 172 148 148 168 132 Z',
'M176 72 C208 78 244 80 256 60 C264 92 286 124 312 142 L196 96 Z',
'M200 114 L286 150 C318 164 332 184 336 216 C294 224 244 224 196 224 C230 222 246 214 240 200 C230 168 216 140 200 114 Z']}
for version,paths in VERSIONS.items():
 geometry='<g id="symbol" fill="#000000">'+''.join(f'<path d="{escape(path,quote=True)}"/>' for path in paths)+'</g>'
 box='0 0 360 256' if version=='v4' else '0 0 360 248'
 (ROOT/f'concepts/01-responsive-cover-{version}.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{box}" role="img"><title>Responsive Cover — {version} — DRAFT</title><desc>DRAFT — NOT FOR PUBLICATION. Coupled textile folds hold a common interior and lift through the same construction. Piece count is compositional, not doctrinal.</desc>{geometry}</svg>\n')
print('Built Responsive Cover v2/v3/v4; initial v1 is retained among sketches.')
