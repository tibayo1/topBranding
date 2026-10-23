"""Editable, exploratory geometry. DRAFT — NOT FOR PUBLICATION.

Run from any directory with python3. Does not modify the installed skills.
"""
from pathlib import Path
import html

ROOT = Path(__file__).resolve().parent.parent
ROOT.mkdir(parents=True, exist_ok=True)

STUDIES = {
    'a-folded-sanctuary-v1': (
        'A — Folded Sanctuary',
        '<path d="M24 40 L96 88 V176 L24 228 Z"/>'
        '<path d="M50 52 L212 28 V100 L198 106 Z"/>'
        '<path d="M172 124 L240 88 V228 L172 202 Z"/>'
        '<path d="M32 232 L100 184 L228 232 Z"/>',
    ),
    'b-sanctuary-strings-v1': (
        'B — Sanctuary Strings',
        '<path fill-rule="evenodd" d="'
        'M24 20 C70 16 88 72 130 124 C158 158 200 166 214 196 '
        'L232 232 H44 V104 C44 78 38 68 24 64 Z '
        'M50 46 C68 100 54 196 76 224 H60 Z '
        'M72 64 C100 140 84 196 116 224 H88 Z '
        'M96 84 C120 146 196 178 166 214 C158 224 148 228 132 228 '
        'C110 204 108 150 96 84 Z"/>',
    ),
    'c-praise-ligature-v1': (
        'C — Praise Ligature',
        '<path d="M20 40 H236 C232 52 220 60 204 60 H158 '
        'C138 60 126 78 126 100 V228 H80 C92 220 94 210 94 192 '
        'V72 H72 C48 72 32 76 28 92 C28 68 24 52 20 40 Z"/>'
        '<path d="M138 76 H166 C208 76 230 98 230 124 '
        'C230 154 206 164 182 172 C158 180 140 194 140 210 '
        'C140 218 146 224 154 228 H138 Z '
        'M154 90 V174 C166 158 190 154 190 124 '
        'C190 104 178 90 154 90 Z" fill-rule="evenodd"/>',
    ),
}

# Optical pass: open the fold seams, thicken the harp baseline, and separate T/P.
# Preserve v1 above so the geometry can be compared rather than overwritten.
STUDIES.update({
    'a-folded-sanctuary-v2': (
        'A — Folded Sanctuary',
        '<path d="M20 36 L92 84 V168 L20 216 Z"/>'
        '<path d="M46 48 L208 24 V96 L194 102 Z"/>'
        '<path d="M168 132 L236 92.74 V224 L168 198 Z"/>'
        '<path d="M36 228 L100 188 L216 228 Z"/>',
    ),
    'b-sanctuary-strings-v2': (
        'B — Sanctuary Strings',
        '<path fill-rule="evenodd" d="'
        'M24 20 C70 16 88 72 130 124 C158 158 200 166 214 196 '
        'L232 232 H44 V104 C44 78 38 68 24 64 Z '
        'M50 44 C70 98 56 188 80 216 H58 Z '
        'M76 66 C102 136 92 188 120 216 H94 Z '
        'M104 96 C126 142 184 174 162 202 C156 212 150 216 134 216 '
        'C116 194 112 144 104 96 Z"/>',
    ),
    'c-praise-ligature-v2': (
        'C — Praise Ligature',
        '<path d="M20 34 H236 C232 46 220 54 204 54 H158 '
        'C138 54 126 72 126 94 V222 H80 C92 214 94 204 94 186 '
        'V66 H72 C48 66 32 70 28 86 C28 62 24 46 20 34 Z"/>'
        '<path d="M144 70 H168 C210 70 232 92 232 118 '
        'C232 148 208 158 184 166 C160 174 146 188 146 204 '
        'C146 212 152 218 160 222 H144 Z '
        'M160 86 V168 C176 152 194 148 194 118 '
        'C194 100 182 86 160 86 Z" fill-rule="evenodd"/>',
    ),
})

for key, (title, geometry) in list(STUDIES.items()):
    if not key.endswith('-v2'):
        continue
    geometry = geometry.replace('M36 228 L100 188', 'M36 228 L100 191.05')
    geometry = geometry.replace('M50 44 C70 98 56 188 80 216 H58 Z',
                                'M58 52 C78 106 62 188 84 216 H58 Z')
    STUDIES[key.replace('-v2', '-v3')] = (title, geometry)

for name, (title, geometry) in STUDIES.items():
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" '
        'width="256" height="256" role="img" aria-labelledby="title">'
        f'<title id="title">{html.escape(title)} — Tabernacle of Praise — DRAFT</title>'
        '<desc>DRAFT — NOT FOR PUBLICATION. Exploratory symbol; no approved branding decision.</desc>'
        f'<g id="symbol" fill="#000000">{geometry}</g></svg>\n'
    )
    path = ROOT / f'{name}.svg'
    if path.exists() and path.read_text() != svg:
        raise SystemExit(f'Preserving earlier iteration: {path}')
    path.write_text(svg)
    print(path.name)
