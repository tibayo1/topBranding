#!/usr/bin/env python3
"""Make tiny licensed UI-glyph subsets; no new brand typography is proposed."""
from pathlib import Path
from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[1]
for source, target, name, points in (
    ('NotoSansSymbols-Regular.ttf', 'ui-arrows.ttf', 'Study UI Arrows', [0x2192, 0x2197]),
    ('NotoSansSymbols2-Regular.ttf', 'ui-symbols.ttf', 'Study UI Symbols', [0x2605, 0x2606, 0x2713]),
):
    font = TTFont(Path('/usr/share/fonts/truetype/noto') / source)
    options = subset.Options()
    options.name_IDs = [0, 1, 2, 3, 4, 5, 6, 13, 14]
    worker = subset.Subsetter(options=options)
    worker.populate(unicodes=points)
    worker.subset(font)
    for record in font['name'].names:
        replacement = {1: name, 2: 'Regular', 4: name + ' Regular', 6: name.replace(' ', '') + '-Regular', 16: name, 17: 'Regular'}.get(record.nameID)
        if replacement:
            record.string = replacement.encode(record.getEncoding(), errors='replace')
    font.save(ROOT / 'assets' / target)
    print('Built', target)
