#!/usr/bin/env python3
"""Package the draft Shared Rhythm cinematic film and editable rebuild sources."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import zipfile


STUDY = Path(__file__).resolve().parents[1]
REPO = STUDY.parents[2]
EXPORTS = STUDY / 'exports'
PACKAGE = EXPORTS / 'SHARED-RHYTHM-CINEMATIC-DRAFT.zip'
STATUS = 'DRAFT — NOT FOR PUBLICATION'
EMBLEM_SHA = '977ee1c5a43c30d2859e31f59705da23a53e8c3e7736d1d1376e021c62703340'


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def start_here() -> str:
    return '''TABERNACLE OF PRAISE — SHARED RHYTHM CINEMATIC FILM
DRAFT — NOT FOR PUBLICATION

WATCH
Open an MP4 in 01-watch directly in a video player or browser.
SOUND includes an optional original synthesized sound-design study.
SILENT is the same visual film without an audio track.
The film is 14 seconds, 1920 x 1080, 30 frames per second.

THE IDEA
Individual strands gather, rise together, and unfold into Shared Rhythm's
four architectural planes: a rising response to praise. This is a design
interpretation of shared worship, not an official mission statement.

THE ENDING
The last 3.5 seconds hold the exact larger-RCCG paired layout from study15.
The parish's complete two-line name stays below its symbol. The RCCG seal
is separate, unmodified and intact. The supplied SVG/PNG is the exact final
composition before lossy video encoding.

THE SOUND STUDY
The score was synthesized for this film from original tones and filtered
noise. It uses no existing music or recording and has no vocals. Technical
checks are supplied. It could not be auditioned by the assistant in this
environment; treat it as an optional draft sound study, not a mastered score.

OTHER FILES
02-endframe contains the editable SVG and PNG closing frame.
03-preview contains a GIF, storyboard and portable browser preview.
04-original-sound contains the original WAV and sound-study notes.
05-editable-rebuild preserves a small repository-like source/dependency tree.
06-records contains rendering, sound and any available visual-review checks.

TO REBUILD
Open a terminal inside 05-editable-rebuild, then run:

python brand/explorations/cinematic-praise-16/source/build_film.py
python brand/explorations/cinematic-praise-16/audio/build_sound.py
python brand/explorations/cinematic-praise-16/source/mux_sound.py

This requires the existing Python/Pillow/NumPy/SciPy, Playwright/Chromium and
ffmpeg environment. It is not a zero-install application. Consult source
and scene parameters for exact installed-tool paths and options. The videos
are ready to watch without rebuilding. The third command adds the new sound
study while preserving the film's video stream without re-encoding it. The
original WAV and silent film are also supplied separately.

SOURCE AND REVIEW STATUS
This is controlled procedural/vector motion with an optional synthesized
score. No Google video generation or upload to a generative service was
performed. The user's privately uploaded reference video is not part of
these deliverables.
The existing RCCG image is a documented 236 x 236 parish-source reference,
not the unavailable 1200 x 1200 original chat upload or a production master.
Its original PNG bytes and provenance are preserved; display scaling adds
no image detail. Final identity, palette, typography, motion, production
asset and publication approval remain open.
'''


def verify_rebuild_tree(archive: zipfile.ZipFile) -> None:
    """Resolve the renderer's actual source paths without rendering the film twice."""
    with tempfile.TemporaryDirectory(prefix='shared-rhythm-rebuild-') as folder:
        archive.extractall(folder)
        mini = Path(folder) / '05-editable-rebuild'
        script = mini / 'brand/explorations/cinematic-praise-16/source/build_film.py'
        spec = importlib.util.spec_from_file_location('shared_rhythm_packaged_renderer', script)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        assert module.REPO == mini
        assert (module.HERE / 'film.js').is_file()
        assert module.FONT.is_file()
        svg = module.REPO / module.SCENE['endSource']
        png = module.REPO / module.SCENE['endPNGSource']
        assert svg.read_bytes() == (EXPORTS / 'shared-rhythm-cinematic-end-DRAFT.svg').read_bytes()
        assert png.read_bytes() == (EXPORTS / 'shared-rhythm-cinematic-end-DRAFT.png').read_bytes()
        assert (mini / 'brand/explorations/cinematic-praise-16/audio/build_sound.py').is_file()
        assert (mini / 'brand/explorations/cinematic-praise-16/source/mux_sound.py').is_file()
        assert sha((mini / 'brand/assets/rccg-emblem/references/rccg-wayforward-reference.png').read_bytes()) == EMBLEM_SHA
        assert '<!doctype html>' in module.html({})


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prepare-only', action='store_true', help='Write the quick-start file before media freeze')
    args = parser.parse_args()
    EXPORTS.mkdir(parents=True, exist_ok=True)
    quickstart = EXPORTS / 'START-HERE.txt'
    quickstart.write_text(start_here(), encoding='utf-8')
    if args.prepare_only:
        print('Prepared START-HERE.txt; waiting for frozen film and sound mux.')
        return

    emblem = REPO / 'brand/assets/rccg-emblem/references/rccg-wayforward-reference.png'
    assert sha(emblem.read_bytes()) == EMBLEM_SHA
    payloads: dict[str, bytes] = {}
    sources: dict[str, str] = {}

    def add(path: Path, destination: str) -> None:
        if not path.is_file():
            raise FileNotFoundError(path)
        if destination in payloads:
            raise ValueError(f'Duplicate archive path: {destination}')
        payloads[destination] = path.read_bytes()
        sources[destination] = path.relative_to(REPO).as_posix()

    add(quickstart, 'START-HERE.txt')
    for sound in ('SOUND', 'SILENT'):
        path = EXPORTS / f'shared-rhythm-cinematic-1080p-{sound}-DRAFT.mp4'
        add(path, '01-watch/' + path.name)
    for extension in ('svg', 'png'):
        path = EXPORTS / f'shared-rhythm-cinematic-end-DRAFT.{extension}'
        add(path, '02-endframe/' + path.name)
    for path in [STUDY / 'preview.html', STUDY / 'previews/storyboard-DRAFT.png',
                 STUDY / 'previews/shared-rhythm-cinematic-DRAFT.gif']:
        add(path, '03-preview/' + path.name)
    for path in [STUDY / 'audio/shared-rhythm-original-sound-study-DRAFT.wav',
                 STUDY / 'audio/sound-notes.md', STUDY / 'audio/build_sound.py',
                 STUDY / 'audio/sound-checks.json']:
        add(path, '04-original-sound/' + path.name)

    rebuild = [p for p in sorted((STUDY / 'source').rglob('*')) if p.is_file() and p.suffix in ('.py', '.json', '.js', '.svg', '.png')]
    rebuild += [p for p in sorted((STUDY / 'audio').iterdir()) if p.suffix in ('.py', '.json', '.md')]
    # The renderer resolves these repository-relative assets from the mini-tree.
    previous = REPO / 'brand/explorations/balanced-emblem-15/exports'
    rebuild += [previous / f'shared-rhythm-RCCG-larger-landscape-DRAFT.{ext}' for ext in ('svg', 'png')]
    rebuild += [p for p in sorted((REPO / 'brand/assets/rccg-emblem/references').iterdir()) if p.is_file()]
    rebuild += [REPO / 'brand/assets/rccg-emblem/README.md']
    font = REPO / 'brand/explorations/identity-development-09/type-study/fonts/instrumentsans'
    rebuild += [font / 'InstrumentSans[wdth,wght].ttf', font / 'OFL.txt']
    for path in rebuild:
        add(path, '05-editable-rebuild/' + path.relative_to(REPO).as_posix())

    for path in [EXPORTS / 'render-checks.json', EXPORTS / 'mux-checks.json', STUDY / 'audio/sound-checks.json']:
        add(path, '06-records/' + path.name)
    review = STUDY / 'reviews'
    if (review / 'visual-review.md').is_file():
        for path in sorted(review.iterdir()):
            if path.is_file() and path.suffix.lower() in ('.md', '.png'):
                add(path, '06-records/reviews/' + path.name)
    entries = [{'file': name, 'bytes': len(raw), 'sha256': sha(raw), 'source': sources[name]}
               for name, raw in sorted(payloads.items())]
    manifest = {
        'status': STATUS,
        'finalApproval': False,
        'method': 'Controlled procedural/vector motion; optional original synthesized sound study.',
        'googleGenerationPerformed': False,
        'externalGenerativeServiceUploadsPerformed': False,
        'privateReferenceVideoIncluded': False,
        'defaultWatch': '01-watch/shared-rhythm-cinematic-1080p-SOUND-DRAFT.mp4',
        'silentAlternative': '01-watch/shared-rhythm-cinematic-1080p-SILENT-DRAFT.mp4',
        'concept': 'Shared Rhythm — a rising response to praise',
        'durationSeconds': 14,
        'fps': 30,
        'size': [1920, 1080],
        'finalExactHoldSeconds': [10.5, 14],
        'namePlacement': 'Complete Tabernacle of Praise name in the exact working two-line arrangement below the symbol.',
        'soundStudy': {'originalSynthesized': True, 'existingMusicUsed': False,
                       'auditionedByAssistant': False, 'masteredScoreClaimed': False},
        'rccg': {'referenceSHA256': EMBLEM_SHA, 'sourceSize': [236, 236],
                 'sourceBytesPreserved': True, 'original1200pxUpload': False, 'productionMaster': False},
        'rebuild': {'folder': '05-editable-rebuild', 'repositoryRelativePathsPreserved': True,
                    'requiresInstalledTools': True},
        'entries': entries,
    }
    payloads['PACKAGE-MANIFEST-DRAFT.json'] = (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode()
    with zipfile.ZipFile(PACKAGE, 'w', zipfile.ZIP_DEFLATED) as archive:
        for name, raw in sorted(payloads.items()):
            info = zipfile.ZipInfo(name, date_time=(2026, 10, 22, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, raw)
    with zipfile.ZipFile(PACKAGE) as archive:
        assert archive.testzip() is None
        assert set(archive.namelist()) == set(payloads)
        for name, raw in payloads.items():
            assert archive.read(name) == raw, name
        assert json.loads(archive.read('PACKAGE-MANIFEST-DRAFT.json'))['entries'] == entries
        for entry in entries:
            assert archive.read(entry['file']) == (REPO / entry['source']).read_bytes(), entry['file']
        verify_rebuild_tree(archive)
    result = {**manifest,
              'package': {'file': PACKAGE.relative_to(STUDY).as_posix(), 'entries': len(payloads),
                          'bytes': PACKAGE.stat().st_size, 'sha256': sha(PACKAGE.read_bytes())},
              'checks': {'zipIntegrity': True, 'allPayloadBytesMatchCurrentSources': True,
                         'soundAndSilentVideosPresent': True, 'referenceBytesMatch': True,
                         'extractedRendererDependenciesResolve': True,
                         'extractedFinalMastersMatchSuppliedEndFiles': True}}
    (EXPORTS / 'package-manifest.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result['package'], indent=2))


if __name__ == '__main__':
    main()
