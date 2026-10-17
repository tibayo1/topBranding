#!/usr/bin/env python3
"""Bundle the study and referenced concept sources with repository-relative paths."""
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
target = ROOT / 'exports/color-study-02-editable.zip'
prefix = Path('Tabernacle-of-Praise-Color-Study-02')
files = [path for folder in (ROOT, REPO / 'brand/concepts/exploration-03')
         for path in sorted(folder.rglob('*'))
         if path.is_file() and path != target and '__pycache__' not in path.parts]
files += [REPO / 'brand/concepts/exploration-01' / name for name in
          ('b-sanctuary-strings-v3.svg', 'c-praise-ligature-v3.svg')]
with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as archive:
    archive.writestr(str(prefix / 'README.md'), """# Tabernacle of Praise — editable draft study

DRAFT — NOT FOR PUBLICATION. No logo, palette, or typography is approved.

Open [the offline explorer](brand/explorations/color-study-02/exports/tabernacle-color-explorer.html)
in a browser. It includes all scripts and fonts and needs no installation.

[Study notes](brand/explorations/color-study-02/README.md) contain exact HEX values,
application links, editing instructions, and validation limits.
[Logo meanings and the new D concept](brand/concepts/exploration-03/README.md)
include the visual breakdown, construction source, and tradeoffs.

Folders preserve repository-relative paths so the source builders and links work.
Only the B/C symbol sources needed for the breakdown are included from exploration 01.
""")
    for path in sorted(files):
        name = prefix / path.relative_to(REPO)
        if path == ROOT / 'README.md':
            text = path.read_text()
            text = '\n'.join(line for line in text.splitlines() if not line.startswith('- [Complete editable study ZIP]')) + '\n'
            archive.writestr(str(name), text)
        else:
            archive.write(path, arcname=name)
with zipfile.ZipFile(target) as archive:
    assert archive.testzip() is None
    assert len(archive.namelist()) == len(set(archive.namelist()))
    print(f'Packaged and verified {len(archive.namelist())} files: {target.name}')
