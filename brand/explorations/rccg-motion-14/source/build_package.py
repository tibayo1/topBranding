#!/usr/bin/env python3
"""Package the draft RCCG-paired motion graphics and editable rebuild sources."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import zipfile


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
OUT = ROOT / 'exports'
PACKAGE = OUT / 'RCCG-TOP-MOTION-GRAPHICS-DRAFT.zip'
STATUS = 'DRAFT — NOT FOR PUBLICATION'
EMBLEM = REPO / 'brand/assets/rccg-emblem/references/rccg-wayforward-reference.png'
EMBLEM_SHA = '977ee1c5a43c30d2859e31f59705da23a53e8c3e7736d1d1376e021c62703340'
SLUGS = ('shared-rhythm', 'open-praise')
FORMATS = ('landscape', 'square')


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def start_here() -> str:
    return '''TABERNACLE OF PRAISE + RCCG — MOTION GRAPHICS
DRAFT — NOT FOR PUBLICATION

WATCH
Open the MP4 files directly in a browser or video player.
01-landscape-videos has 1920 x 1080 versions for presentations and widescreen.
02-square-videos has 1080 x 1080 versions for a square social-media layout.
Both concepts run for 10 seconds at 30 fps and are silent.

SHARED RHYTHM
The four unequal planes rise together in an overlapping response to praise,
reflecting the description "a rising reaction to praises". Their original
outlines stay rigid and separate. The final paired artwork holds still from
6 to 10 seconds. The complete name remains below the parish symbol.

OPEN PRAISE
The single symbol makes a quieter lift and settle. Its full name stays below.

THE RCCG EMBLEM
The complete RCCG reference remains separate, in its original colors on a
white panel. Its position and appearance remain static throughout the video.
It is the documented 236 x 236 parish-source reference, preserved unchanged;
it is not the unavailable original 1200 x 1200 chat upload or a verified
high-resolution production master. Source and checksum records are included.

OTHER FILES
03-endframes contains SVG and PNG versions of each exact closing layout.
04-motion-preview contains a portable browser player, a GIF and a storyboard.
05-editable-rebuild preserves repository-relative scripts, input artwork,
font/license and reference assets. To rebuild, open a terminal inside that
folder and run:

python brand/explorations/rccg-motion-14/source/build_motion.py

Rebuilding requires the existing Python/Pillow/numpy/scipy/Playwright,
Chromium and ffmpeg environment. It is not a zero-install project. Inspect
the source for current command options and dependencies. The supplied
videos are ready to watch without rebuilding. 06-records documents checks.

These are controlled vector motion graphics. No files were uploaded to
Google and no Google video generation was performed for this package.
Final logo, palette, typography, motion and publication approval remain open.
'''


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prepare-only', action='store_true', help='Write the quick-start file while videos are being rendered')
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'START-HERE.txt').write_text(start_here(), encoding='utf-8')
    if args.prepare_only:
        print('Prepared START-HERE.txt; waiting for frozen motion outputs.')
        return

    assert sha(EMBLEM.read_bytes()) == EMBLEM_SHA
    payloads: dict[str, bytes] = {}
    sources: dict[str, str] = {}

    def add(path: Path, destination: str) -> None:
        if destination in payloads:
            raise ValueError(f'Duplicate archive path: {destination}')
        if not path.is_file():
            raise FileNotFoundError(path)
        payloads[destination] = path.read_bytes()
        sources[destination] = path.relative_to(REPO).as_posix()

    add(OUT / 'START-HERE.txt', 'START-HERE.txt')
    for slug in SLUGS:
        for shape in FORMATS:
            stem = f'{slug}-RCCG-motion-{shape}'
            video = OUT / f'{stem}-DRAFT.mp4'
            add(video, f'0{1 if shape == "landscape" else 2}-{shape}-videos/{video.name}')
            for extension in ('svg', 'png'):
                frame = OUT / f'{stem}-end-DRAFT.{extension}'
                add(frame, f'03-endframes/{frame.name}')

    for path in [ROOT / 'preview.html', ROOT / 'previews/shared-rhythm-RCCG-motion-DRAFT.gif',
                 ROOT / 'previews/shared-rhythm-RCCG-storyboard-DRAFT.png']:
        add(path, '04-motion-preview/' + path.name)

    # Preserve a small repository-like tree so source paths survive extraction.
    rebuild: list[Path] = sorted((ROOT / 'source').glob('*.py'))
    rebuild += sorted((ROOT / 'source').glob('*.json'))
    rebuild += [REPO / f'brand/explorations/stacked-motion-13/pairings/{slug}-stacked-dark-pairing-DRAFT.svg' for slug in SLUGS]
    rebuild += list((REPO / 'brand/assets/rccg-emblem/references').iterdir())
    rebuild += [REPO / 'brand/assets/rccg-emblem/README.md']
    font_root = REPO / 'brand/explorations/identity-development-09/type-study/fonts/instrumentsans'
    rebuild += [font_root / 'InstrumentSans[wdth,wght].ttf', font_root / 'OFL.txt']
    for path in rebuild:
        if path.is_file():
            add(path, '05-editable-rebuild/' + path.relative_to(REPO).as_posix())

    add(OUT / 'render-checks.json', '06-records/render-checks.json')
    review = ROOT / 'reviews'
    if (review / 'visual-review.md').is_file():
        for path in sorted(review.iterdir()):
            if path.suffix.lower() in ('.md', '.png'):
                add(path, '06-records/reviews/' + path.name)
    records = [{'file': name, 'bytes': len(body), 'sha256': sha(body), 'source': sources[name]}
               for name, body in sorted(payloads.items())]
    manifest = {
        'status': STATUS,
        'finalApproval': False,
        'googleGenerationPerformed': False,
        'externalUploadsPerformed': False,
        'defaultWatch': '01-landscape-videos/shared-rhythm-RCCG-motion-landscape-DRAFT.mp4',
        'concepts': ['Shared Rhythm', 'Open Praise'],
        'durationSeconds': 10,
        'fps': 30,
        'silent': True,
        'namePlacement': 'Complete Tabernacle of Praise name below each parish symbol; static throughout.',
        'sharedRhythmMeaning': 'A rising response to praise, preserving the user phrase a rising reaction to praises.',
        'rccg': {'sourceSHA256': EMBLEM_SHA, 'sourceSize': [236, 236],
                 'static': True, 'sourceBytesUnchanged': True,
                 'original1200pxUpload': False, 'productionMaster': False},
        'rebuild': {'folder': '05-editable-rebuild',
                    'script': 'brand/explorations/rccg-motion-14/source/build_motion.py',
                    'relativePathsPreserved': True, 'requiresInstalledTools': True},
        'entries': records,
    }
    payloads['PACKAGE-MANIFEST-DRAFT.json'] = (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode()
    with zipfile.ZipFile(PACKAGE, 'w', zipfile.ZIP_DEFLATED) as archive:
        for name, body in sorted(payloads.items()):
            # Stable archive dates make package hashes reproducible.
            info = zipfile.ZipInfo(name, date_time=(2026, 10, 22, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, body)
    with zipfile.ZipFile(PACKAGE) as archive:
        assert archive.testzip() is None
        assert set(archive.namelist()) == set(payloads)
        for name, body in payloads.items():
            assert archive.read(name) == body, name
        assert json.loads(archive.read('PACKAGE-MANIFEST-DRAFT.json'))['entries'] == records
        for record in records:
            assert archive.read(record['file']) == (REPO / record['source']).read_bytes(), record['file']
    result = {**manifest,
              'package': {'file': PACKAGE.relative_to(ROOT).as_posix(), 'entries': len(payloads),
                          'bytes': PACKAGE.stat().st_size, 'sha256': sha(PACKAGE.read_bytes())},
              'checks': {'zipIntegrity': True, 'allPayloadBytesMatchCurrentSources': True,
                         'fourVideosPresent': True, 'emblemReferenceBytesMatch': True}}
    (OUT / 'package-manifest.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result['package'], indent=2))


if __name__ == '__main__':
    main()
