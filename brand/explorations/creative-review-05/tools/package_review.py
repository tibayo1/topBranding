#!/usr/bin/env python3
"""Package the draft review; keep final validation outside its own hashed ZIP."""
from pathlib import Path
import hashlib
import json
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
EXPORTS = ROOT / 'exports'
ARCHIVE = EXPORTS / 'creative-review-05-editable.zip'
MANIFEST = EXPORTS / 'package-manifest.json'


def included(path):
    return (path.is_file() and path not in (ARCHIVE, MANIFEST)
            and path.name != 'validation-report.json'
            and '__pycache__' not in path.parts
            and path.suffix not in ('.pyc', '.zip'))


def main():
    required = ['README.md', 'index.html', 'data.js', 'app.js', 'styles.css',
                'exports/tabernacle-creative-review-05.html',
                'exports/tabernacle-creative-review-05.pdf',
                'exports/creative-review-05-overview.png']
    for name in required:
        assert (ROOT / name).is_file(), f'Build the required artifact first: {name}'
    files = sorted(path for path in ROOT.rglob('*') if included(path))
    records = []
    for path in files:
        assert path.stat().st_size < 100_000_000, f'Oversized repository artifact: {path}'
        records.append({'file': path.relative_to(ROOT).as_posix(),
                        'bytes': path.stat().st_size,
                        'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
    MANIFEST.write_text(json.dumps({'status': 'DRAFT — NOT FOR PUBLICATION',
                                   'note': 'Hashes exclude this manifest, ZIP and final validation report.',
                                   'files': records}, ensure_ascii=False, indent=2) + '\n')
    with ZipFile(ARCHIVE, 'w', ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files + [MANIFEST]:
            archive.write(path, 'creative-review-05/' + path.relative_to(ROOT).as_posix())
    with ZipFile(ARCHIVE) as archive:
        assert archive.testzip() is None, 'ZIP CRC error'
        names = archive.namelist()
        assert len(names) == len(set(names)), 'Duplicate ZIP entries'
        assert not any('validation-report.json' in name for name in names)
        for record in records:
            data = archive.read('creative-review-05/' + record['file'])
            assert hashlib.sha256(data).hexdigest() == record['sha256']
    print(f'Packaged and checked {len(files) + 1} entries; {ARCHIVE.stat().st_size:,} bytes.')


if __name__ == '__main__':
    main()
