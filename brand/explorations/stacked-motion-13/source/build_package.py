#!/usr/bin/env python3
"""Package the name-below logos, motion studies and manual Google handoff."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET
import zipfile


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'exports'
PACKAGE = OUT / 'UPDATED-LOGOS-AND-GOOGLE-ANIMATION-DRAFT.zip'
SLUGS = [('shared-rhythm', 'Shared-Rhythm'), ('open-praise', 'Open-Praise')]
DRAFT = 'DRAFT — NOT FOR PUBLICATION'


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def prompts() -> dict[str, str]:
    source = (ROOT / 'animation/google-animation-prompts.md').read_text()
    result = {}
    for slug, title in [('shared-rhythm', 'Shared Rhythm'), ('open-praise', 'Open Praise')]:
        pattern = rf'## {re.escape(title)} — full-name prompt\s+~~~text\n(.*?)\n~~~'
        match = re.search(pattern, source, re.S)
        if not match:
            raise ValueError(f'Missing full-name prompt for {title}')
        result[slug] = match.group(1).strip() + '\n'
        (OUT / f'{slug}-google-prompt.txt').write_text(result[slug])
    return result


def quick_start() -> str:
    return '''TABERNACLE OF PRAISE — NAME-BELOW LOGOS + ANIMATION KIT
DRAFT — NOT FOR PUBLICATION

1. Watch the controlled motion studies in 03-motion-previews. Both names stay
   below the symbol. Shared Rhythm expresses a rising response to praise:
   its four unequal planes lift in succession, settle, and hold the exact logo.

2. Choose Shared-Rhythm or Open-Praise in 01-upload-to-google. Start with
   full-logo-end-landscape-DRAFT.png (1920 x 1080). Square files are supplied
   for tools that accept that shape.

3. In your Google video tool, choose image-to-video if available, upload that
   PNG and paste the matching text from 02-copy-paste-prompts. Aim for 8 seconds
   with the final 2 seconds still. The draft is silent.

4. If your tool offers start AND end frames, use the matching start and end
   PNGs. With only one image slot, use the finished end PNG: the prompt asks
   for a gentle lift-and-return. Available controls have not been verified here.

5. Compare the result with the end PNG before sharing for review. Check the
   exact symbol, complete spelling, name placement and still final hold.

For exact lettering, use 05-optional-symbol-only-and-name-overlays: animate the
symbol-only PNG, then place the matching transparent name-overlay PNG over the
video at full-frame size. Both images must use the same canvas dimensions.
Replace the last 2 seconds with the exact full-logo end PNG if needed.

The supplied MP4/GIF previews are controlled vector motion studies. They are
not Google-generated videos; no files have been uploaded to Google for you.

Keep the RCCG emblem outside generative animation. Folder 04 contains static
reference pairings only. If needed, add that emblem separately and unchanged
after generation. The current 236 x 236 emblem is a documented parish-source
reference, not the verified original chat upload or an approved print master.

The palette is a working teal/ivory direction. Final logo, motion, typography,
production artwork and publication approval remain open.
'''


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prepare-only', action='store_true', help='Write prompt and quick-start files without packaging unfinished motion outputs')
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    prompt_text = prompts()
    start = quick_start()
    (OUT / 'START-HERE.txt').write_text(start)
    if args.prepare_only:
        print('Prepared START-HERE.txt and two copy-and-paste prompt files.')
        return

    inputs = json.loads((ROOT / 'animation-inputs/manifest.json').read_text())
    by_slug = {row['id']: row for row in inputs['directions']}
    motion = ROOT / 'animation'
    videos = sorted(motion.glob('*.mp4'))
    gifs = sorted(motion.glob('*.gif'))
    if len(videos) < 2 or not gifs:
        raise SystemExit('Wait for both final MP4 motion studies and the Shared Rhythm GIF before packaging.')
    for slug, _ in SLUGS:
        if not any(slug in video.name for video in videos):
            raise SystemExit(f'No final motion video for {slug}')

    payloads: dict[str, bytes] = {}
    sources: dict[str, str] = {}

    def add(path: Path, destination: str) -> None:
        if destination in payloads:
            raise ValueError(f'Duplicate ZIP path: {destination}')
        if not path.is_file():
            raise FileNotFoundError(path)
        payloads[destination] = path.read_bytes()
        sources[destination] = path.relative_to(ROOT).as_posix()

    payloads['START-HERE.txt'] = start.encode()
    for slug, folder in SLUGS:
        direction = by_slug[slug]
        for format_ in ('landscape', 'square'):
            files = direction['formats'][format_]['files']
            for kind in ('full-logo-end', 'full-logo-start'):
                svg_root = ET.parse(ROOT / files[kind]['svg']).getroot()
                assert not list(svg_root.iter('{http://www.w3.org/2000/svg}image')), 'Google input must contain parish paths only'
                assert ''.join(path.get('data-letter', '') for path in svg_root.iter('{http://www.w3.org/2000/svg}path')) == 'TabernacleofPraise'
                add(ROOT / files[kind]['png'], f'01-upload-to-google/{folder}/{kind}-{format_}-DRAFT.png')
                add(ROOT / files[kind]['svg'], f'editable/{folder}/{kind}-{format_}-DRAFT.svg')
            for kind in ('symbol-only-end', 'symbol-only-start', 'name-overlay'):
                add(ROOT / files[kind]['png'], f'05-optional-symbol-only-and-name-overlays/{folder}/{kind}-{format_}-DRAFT.png')
                add(ROOT / files[kind]['svg'], f'editable/{folder}/{kind}-{format_}-DRAFT.svg')
        destination = f'02-copy-paste-prompts/{folder}-google-prompt.txt'
        payloads[destination] = prompt_text[slug].encode()
        sources[destination] = f'exports/{slug}-google-prompt.txt'

    add(ROOT / 'animation/google-animation-prompts.md', '02-copy-paste-prompts/Full-handoff-and-fallbacks-DRAFT.md')
    add(ROOT / 'animation/storyboard.json', 'editable/storyboard-DRAFT.json')
    add(ROOT / 'animation/motion-checks.json', 'editable/motion-checks-DRAFT.json')
    add(ROOT / 'animation-inputs/manifest.json', 'editable/animation-inputs-manifest-DRAFT.json')
    for file in sorted(motion.iterdir()):
        if file.suffix.lower() in ('.mp4', '.gif', '.png', '.html'):
            add(file, '03-motion-previews/' + file.name)
    pairings = ROOT / 'pairings'
    for file in sorted(pairings.iterdir()):
        if file.suffix.lower() in ('.svg', '.png', '.pdf'):
            add(file, '04-static-RCCG-pairings/' + file.name)
    add(pairings / 'README.md', '04-static-RCCG-pairings/README-DRAFT.md')
    add(pairings / 'manifest.json', '04-static-RCCG-pairings/manifest-DRAFT.json')

    records = [{'file': path, 'bytes': len(body), 'sha256': sha(body), **({'source': sources[path]} if path in sources else {})}
               for path, body in sorted(payloads.items())]
    manifest = {'status': DRAFT, 'finalApproval': False,
                'manualGoogleHandoff': True, 'googleGenerationPerformed': False,
                'layout': 'Full name below each parish symbol; static typography.',
                'sharedRhythmMeaning': 'A rising response to praise, reflecting the user phrase a rising reaction to praises.',
                'defaultUpload': '01-upload-to-google/Shared-Rhythm/full-logo-end-landscape-DRAFT.png',
                'rccg': 'Static reference pairings only; excluded from every Google upload image.',
                'entries': records}
    manifest_bytes = (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode()
    payloads['PACKAGE-MANIFEST-DRAFT.json'] = manifest_bytes
    with zipfile.ZipFile(PACKAGE, 'w', zipfile.ZIP_DEFLATED) as archive:
        for name, body in sorted(payloads.items()):
            archive.writestr(name, body)
    with zipfile.ZipFile(PACKAGE) as archive:
        assert archive.testzip() is None
        assert len(archive.namelist()) == len(payloads)
        for name, body in payloads.items():
            assert archive.read(name) == body, name
        assert not any('rccg' in name.lower() for name in archive.namelist() if name.startswith('01-upload-to-google/'))
    result = {**manifest, 'package': {'file': PACKAGE.relative_to(ROOT).as_posix(), 'entries': len(payloads),
                                    'bytes': PACKAGE.stat().st_size, 'sha256': sha(PACKAGE.read_bytes())},
              'checks': {'zipIntegrity': True, 'allEntryBytesMatchSources': True,
                         'bothMotionVideosPresent': True, 'googleUploadImagesExcludeRCCG': True}}
    (OUT / 'package-manifest.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result['package'], indent=2))


if __name__ == '__main__':
    main()
