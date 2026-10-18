#!/usr/bin/env python3
"""Carved-crossing development. Preserve prior studies; DRAFT — NOT FOR PUBLICATION."""
from pathlib import Path
import json
import xml.etree.ElementTree as ET
ROOT = Path(__file__).resolve().parent
STUDY = ROOT.parent.parent
DRAFT = 'DRAFT — NOT FOR PUBLICATION'
SELECTED = 'M108 26 H80 L30 76 V172 L74 216 L108 182 V122 H76 V86 H108 Z M152 46 L226 88.72 V186 L180 232 H100 L152 180 V122 H190 V86 H152 Z'
IDEA = 'Two folded boundaries form one cruciform shared interior. The interval remains open above and turns outward at a diagonal lower threshold. Contemporary artistic interpretation, not a historic tabernacle plan or a depiction of divine presence.'
def svg(title, d):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" role="img"><title>{title} — {DRAFT}</title><desc>{DRAFT}. {IDEA}</desc><path fill="#000000" d="{d}"/></svg>'
def rel(filename): return str((ROOT / filename).relative_to(STUDY))
(ROOT / 'developed.svg').write_text(svg('Open Crossing', SELECTED))
metadata = {
 'direction':'A','title':'Sacred Space',
 'sketches':[
  {'id':'A1','name':'Open Court','idea':'A canted enclosure surrounds a generous shared interior and leaves diagonal ways through.','approach':'Two turning boundaries; a spatial court rather than a roof illustration.','sourceFile':rel('a1-open-court.svg'),'reason':'The open room is legible, but the split perimeter resembles a generic corporate loop.'},
  {'id':'A2','name':'Resonant Chamber','idea':'Curved boundaries and an inner shelf test an interior that widens toward its opening.','approach':'Asymmetric curved enclosure with a secondary inward edge.','sourceFile':rel('a2-resonant-chamber.svg'),'reason':'The separate inner shelf feels added; the resulting form has too many competing readings.'},
  {'id':'A3','name':'Common Centre','idea':'Three inward-turning boundaries imply one shared centre without drawing individuals.','approach':'Faceted, separated walls organized around a common interval.','sourceFile':rel('a3-common-centre.svg'),'reason':'The gathering is understandable, but the three-part circulation suggests recycling or a business network.'},
  {'id':'A4','name':'Joined Thresholds','idea':'Two folded boundaries give the shared interior a cruciform shape and leave it open to its surroundings.','approach':'Carve the crossing first; let its upper and lower thresholds determine the surrounding silhouettes.','sourceFile':rel('developed-v4.svg'),'reason':'The Christian and spatial readings become visible in one construction. This has a clearer reason to exist than the earlier loops.'}
 ],
 'developed':{
  'name':'Open Crossing','sourceFile':rel('developed.svg'),'chosenSketchId':'A4',
  'idea':'Two folded boundaries make one open, cruciform shared interior.',
  'visible':'Two unequal faceted silhouettes; a vertical crossing with a broad horizontal room; an open upper interval and a diagonal lower threshold.',
  'meaning':'The boundaries suggest a place of gathering, while the shared cruciform interval establishes a visible Christian association. The opening can suggest invitation and response; its relationship to praise is an intended artistic association and is less immediate than the sacred-space reading. The void does not depict God, and this is not a historical tabernacle plan.',
  'construction':[
   '256-unit canvas; exterior x30–226 and y26–232. The main vertical interval is 44 units wide and the horizontal crossing is 36 units deep.',
   'Two closed black filled silhouettes. The interior is actual space between contours, with no white cover shapes, strokes, masks or raster artwork.',
   '45-degree lower threshold edges align the opening with the faceted enclosure; a 30-degree upper-right plane creates measured asymmetry. The selected seventh development removes the small lower step.'
  ],
  'risk':'Its dense faceted boundaries can feel institutional. The lower interval may read as a chevron, and a viewer may see a split geometric badge before recognizing the shared room. Praise is expressed less clearly than Christian gathering.',
  'smallSize':'Rendered and visually checked at true 16, 24, 32 and 64 pixels, in black and reverse. The crossing remains visible at 16 pixels; 24 pixels and above better preserve the diagonal threshold and the distinction between the two boundaries.',
  'longevity':'Flat filled geometry, generous intervals and no effect-dependent detail support enduring reproduction. The cross is familiar; the asymmetrical enclosure must earn recognition through consistent use rather than a claim of unprecedented symbolism.',
  'selectionReason':'The room and Christian association are visible without a long explanation. Compared with the earlier loops, the negative space determines the outer construction. The sixth development widened the upper interval; the seventh removed a lower stub and made the diagonal threshold continuous.',
  'iterations':[rel(f'developed-v{i}.svg') for i in range(1,8)]
 }
}
(ROOT / 'metadata.json').write_text(json.dumps(metadata, indent=2, ensure_ascii=False)+'\n')
# The sheet is a measurement proof; its labels are live text, the symbol masters are paths.
parts=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 650"><title>Open Crossing: refinement and real-size proof — '+DRAFT+'</title><rect width="1200" height="650" fill="white"/><g font-family="sans-serif" fill="#111"><text x="38" y="36" font-size="14">A — SACRED SPACE / OPEN CROSSING</text><text x="38" y="60" font-size="11">'+DRAFT+'</text></g>']
for i,(filename,label) in enumerate([('developed-v4.svg','v4 / initial spatial crossing'),('developed-v6.svg','v6 / 44-unit upper interval'),('developed-v7.svg','v7 / continuous lower threshold')]):
    root=ET.parse(ROOT/filename).getroot()
    d=root.find('{http://www.w3.org/2000/svg}path').get('d')
    parts.append(f'<g transform="translate({38+i*390} 86) scale(1.15)"><path fill="#000" d="{d}"/></g><text x="{38+i*390}" y="410" font-size="13" font-family="sans-serif">{label}</text>')
parts.append('<text x="38" y="460" font-family="sans-serif" font-size="12">ACTUAL PIXEL DIMENSIONS / BLACK</text><rect x="610" y="437" width="552" height="174" fill="#000"/><text x="632" y="460" font-family="sans-serif" font-size="12" fill="white">ACTUAL PIXEL DIMENSIONS / REVERSE</text>')
for side in [0,1]:
    for x,size in [(38,16),(140,24),(254,32),(394,64)]:
        xx=x+side*594
        parts.append(f'<g transform="translate({xx} 487) scale({size/256})"><path fill="{ "#fff" if side else "#000" }" d="{SELECTED}"/></g><text x="{xx}" y="580" font-family="sans-serif" font-size="12" fill="{ "#fff" if side else "#000" }">{size} px</text>')
parts.append('<text x="38" y="635" font-family="sans-serif" font-size="11" fill="#444">The small symbols above are drawn at their stated pixel dimensions. Preferred interpretation size: 24 px and above.</text></svg>')
(ROOT/'refinement-proof.svg').write_text(''.join(parts))
