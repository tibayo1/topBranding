"""Resonant Sanctuary: a new editable draft, not a selected church identity."""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parent.parent
ROOT.mkdir(parents=True, exist_ok=True)

# Folded surround seen in plan; the right boundary releases into rising bands.
# Individual seams are actual gaps, not white overlays or color effects.
PATHS = [
    'M48 212 C38 226 44 236 60 236 H170 C204 236 220 218 220 184 V156 '
    'C209 162 193 167 184 175 C177 182 178 188 176 194 '
    'C174 201 170 204 164 204 H72 C60 204 54 208 48 212 Z',
    'M32 92 C24 98 24 106 24 120 V202 C24 216 30 226 40 232 '
    'C34 218 50 204 60 196 V120 C60 108 50 100 42 96 C38 94 34 92 32 92 Z',
    'M24 84 C28 68 42 56 60 56 H152 C172 56 184 68 184 84 V92 '
    'H92 C72 92 56 78 40 78 C34 78 28 80 24 84 Z',
    'M190 86 V62 C190 44 218 36 234 20 V46 C234 64 202 66 190 86 Z',
    'M188 122 V102 C188 84 218 78 246 52 V80 C246 98 202 102 188 122 Z',
    'M192 160 V142 C192 122 222 116 232 104 V128 C232 144 200 144 192 160 Z',
]
geometry = '<g id="symbol" fill="#000000" transform="translate(-7 0)">' + ''.join(f'<path d="{escape(path, quote=True)}"/>' for path in PATHS) + '</g>'
svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="title">'
       '<title id="title">D — Resonant Sanctuary — Tabernacle of Praise — DRAFT</title>'
       '<desc>DRAFT — NOT FOR PUBLICATION. A folded surround defines shared space and opens into a rising rhythm. Abstract association, not literal biblical architecture or approved theology.</desc>'
       + geometry + '</svg>\n')
(ROOT / 'd-resonant-sanctuary-v1.svg').write_text(svg)
print('Built D / Resonant Sanctuary, v1')
