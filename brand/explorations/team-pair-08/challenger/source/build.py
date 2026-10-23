#!/usr/bin/env python3
"""Original editable vector interpretation of the selected Folded P rough.

Reference: praise-study-07/exports/praise-comparison.png, original row 2.
The source is raster ideation, not an approved production master. Shapes below
are newly drawn paths; no raster is embedded. All geometry remains exploratory.
"""
from pathlib import Path
import json
ROOT = Path(__file__).resolve().parents[1]
VERSIONS = {
    "v1": [
        "M38 44 97 23 183 51C207 59 219 72 219 91V103C213 94 200 89 178 81Z",
        "M38 49 96 67V126L58 154V233H38Z",
        "M173 96V112C173 124 165 126 154 126H101L62 154 102 168H162C197 168 219 151 219 126C219 110 204 102 181 95Z",
        "M62 160 96 175V233H62Z",
    ],
    "v2": [
        "M36 43 97 21 182 49C207 57 220 71 220 91V101C210 92 199 88 178 81Z",
        "M36 49 94 67V125L57 153V233H36Z",
        "M174 98V113C174 125 166 128 154 128H102L64 153 103 166H163C198 166 220 150 220 126C220 111 205 103 182 96Z",
        "M64 161 94 172V233H64Z",
    ],
    "v3": [
        "M38 43 97 22 181 49C205 57 219 71 219 91V100C209 92 198 87 177 80Z",
        "M38 50 94 68V125L57 153V233H38Z",
        "M174 100V113C174 125 166 128 154 128H102L65 153 103 166H163C198 166 219 150 219 127C219 112 204 104 181 97Z",
        "M65 162 94 173V233H65Z",
    ],
}
def make(paths, title, reverse=False):
    ink = "#ffffff" if reverse else "#000000"
    background = '<rect width="256" height="256" fill="#000000"/>' if reverse else ''
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">\n<title>'+title+' — DRAFT — NOT FOR PUBLICATION</title>\n<desc>Four original path surfaces interpret the Folded P sketch. A broad upper turn and angular inward middle return carry the letter. White channels are open geometry, not painted overlays. No praise stripes or instrument is added.</desc>\n'+background+'\n'+''.join('<path fill="'+ink+'" d="'+d+'"/>' for d in paths)+'\n</svg>\n'
for version,paths in VERSIONS.items():
    (ROOT/f'folded-p-{version}.svg').write_text(make(paths, f'Folded P {version}'))
(ROOT/'primary.svg').write_text(make(VERSIONS['v3'],'Folded P, optical draft'))
(ROOT/'reverse.svg').write_text(make(VERSIONS['v3'],'Folded P, reversed optical draft',True))
(ROOT/'metadata.json').write_text(json.dumps({
 'id':'B','name':'Folded P','status':'DRAFT — NOT FOR PUBLICATION',
 'primary':'primary.svg','reverse':'reverse.svg','viewBox':'0 0 256 256',
 'reference':'../../praise-study-07/exports/praise-comparison.png',
 'referenceLocation':'Original Folded P, middle row, left column',
 'premise':'One folded P offers a letter-led counterpart to Shared Rhythm.',
 'construction':'Four independent black path surfaces; the sloping upper turn, open counter and angular middle return form a P through true gaps. No embedded raster, live text, gradients, strokes or white overlays.',
 'meaning':'P relates directly to Praise. Its returned inner edge suggests a place receiving and holding rather than a decorative musical addition. This is an interpretation, not a literal universal church symbol.',
 'risk':'Folded letterforms can suggest printing, packaging or a creative studio. It is less specifically ecclesiastical than the Shared Rhythm architectural family; no trademark clearance is implied.',
 'changes':['v1 translates the original rough into editable planar paths.','v2 opens the principal sloping channel, shortens the bowl slightly and increases the inset between the two lower planes.','v3 gives the broad counter and sloping channels more breathing room while retaining the middle return and restrained letter width.'],
 'selection':'UNSELECTED. User requested a different second contender and will provide a reference. Folded P roughs preserved as historical source only; do not present as the team challenger.',
 'versions':list(VERSIONS)
},ensure_ascii=False,indent=2)+'\n')
