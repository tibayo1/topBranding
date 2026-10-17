#!/usr/bin/env python3
"""Bundle this editable study, excluding its own archive and Python caches."""
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
target = ROOT / 'exports/color-study-02-editable.zip'
with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as archive:
    for path in sorted(ROOT.rglob('*')):
        if path.is_file() and path != target and '__pycache__' not in path.parts:
            archive.write(path, arcname=Path('Tabernacle-of-Praise-Color-Study-02') / path.relative_to(ROOT))
with zipfile.ZipFile(target) as archive:
    assert archive.testzip() is None
    assert len(archive.namelist()) == len(set(archive.namelist()))
    print(f'Packaged and verified {len(archive.namelist())} files: {target.name}')
