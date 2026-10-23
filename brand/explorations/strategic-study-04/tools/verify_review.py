#!/usr/bin/env python3
"""Exercise the delivered strategic study in Chromium, including offline downloads.

Serve the study directory locally, then run this script with its URL (default 8766).
This checks the review interface and artwork transfer, not aesthetic quality,
theological endorsement, trademark clearance, or human small-size recognition.
"""
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import re
import sys
import tempfile
import traceback
import xml.etree.ElementTree as ET

from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]
URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8766'
REPORT = ROOT / 'exports/validation-report.json'
checks = []
evidence = {}


def passed(message):
    checks.append(message)
    print('PASS:', message, flush=True)


def local_name(element):
    return element.tag.rsplit('}', 1)[-1]


def svg_root(art, fragment=False):
    return ET.fromstring('<svg>' + art + '</svg>' if fragment else art)


def geometry(root):
    """Preserve primitive geometry and ancestor transforms/fill rules."""
    result = []
    primitives = {'path', 'rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon', 'use'}
    ignored = {'id', 'fill', 'stroke', 'style', 'class', 'aria-label', 'role'}

    def visit(element, transforms=(), rule='nonzero'):
        transform = element.attrib.get('transform')
        transforms = transforms + ((transform,) if transform else ())
        rule = element.attrib.get('fill-rule', rule)
        tag = local_name(element)
        if tag in primitives:
            attrs = tuple(sorted((key, value) for key, value in element.attrib.items()
                                 if key not in ignored and not key.startswith('data-')
                                 and key not in ('transform', 'fill-rule')))
            result.append((tag, attrs, transforms, rule))
        for child in element:
            visit(child, transforms, rule)

    visit(root)
    return result


def contains_art(root):
    return any(local_name(element) == 'path' for element in root.iter())


def source_path(item):
    reference = item.get('sourceFile') or item.get('source')
    if isinstance(reference, dict):
        reference = reference.get('file') or reference.get('path')
    assert reference, f'Missing sourceFile on {item["id"]}'
    path = (ROOT / reference).resolve()
    assert path.is_relative_to(ROOT), f'Unexpected source path: {reference}'
    assert path.is_file(), reference
    return path


def primary_fragment(item):
    return svg_root(item['mark'], fragment=True)


def collect_data(page):
    page.wait_for_function('window.TOPStudy && window.TOPStudyUI')
    page.evaluate('document.fonts.ready')
    return page.evaluate('window.TOPStudy')


def check_download(page, button, item, kind, temporary):
    try:
        with page.expect_download(timeout=10000) as pending:
            button.click()
    except Exception as error:
        raise AssertionError(f'Download did not complete: {item["id"]}/{kind}. {error}') from error
    download = pending.value
    assert download.suggested_filename.endswith('-DRAFT.svg'), download.suggested_filename
    target = temporary / download.suggested_filename
    download.save_as(target)
    text = target.read_text()
    root = svg_root(text)
    assert contains_art(root), download.suggested_filename
    assert 'DRAFT — NOT FOR PUBLICATION' in text
    assert not any(local_name(element) in ('image', 'foreignObject', 'script') for element in root.iter())
    if kind == 'symbol':
        expected = primary_fragment(item)
    elif kind in ('horizontal', 'stacked'):
        expected = svg_root(item['lockups'][kind])
    else:
        expected = svg_root(item['applications'][kind])
    assert geometry(root) == geometry(expected), f'Download changed geometry: {item["id"]}/{kind}'
    if kind in ('symbol', 'horizontal', 'stacked'):
        assert not any(local_name(element) == 'text' for element in root.iter()), f'Live wordmark type: {item["id"]}/{kind}'
    # Chromium suppresses an automated burst after ten files. Pace distinct
    # user clicks so every offered file is exercised without hitting that limit.
    page.wait_for_timeout(1100)
    return download.suggested_filename


def download_all(page, concepts, temporary):
    downloaded = []
    for item in concepts:
        article = page.locator(f'.concept[data-concept="{item["id"]}"]')
        for kind in ('symbol', 'horizontal', 'stacked'):
            button = article.locator(f'.concept-actions [data-kind="{kind}"]')
            downloaded.append(check_download(page, button, item, kind, temporary))
        article.locator('[data-tab="applications"]').click()
        for kind in ('paper', 'signage'):
            button = article.locator(f'.application-proof [data-kind="{kind}"]')
            downloaded.append(check_download(page, button, item, kind, temporary))
        article.locator('[data-tab="lockups"]').click()
    return downloaded


def run():
    assert (ROOT / 'data.js').exists(), 'Build data.js before validation'
    offline_file = ROOT / 'exports/tabernacle-strategic-explorer.html'
    assert offline_file.exists(), 'Build the standalone offline HTML before validation'
    with tempfile.TemporaryDirectory(prefix='top-strategic-check-') as temporary:
        temporary = Path(temporary)
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(executable_path='/usr/bin/chromium', headless=True,
                args=['--no-sandbox', '--disable-dev-shm-usage'])
            context = browser.new_context(viewport={'width': 1440, 'height': 1000},
                accept_downloads=True, reduced_motion='reduce')
            page = context.new_page()
            errors, remote_requests, failed_requests = [], [], []
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.on('request', lambda request: remote_requests.append(request.url)
                if request.url.startswith(('http://', 'https://')) and not request.url.startswith(URL) else None)
            page.on('requestfailed', lambda request: failed_requests.append(request.url))
            response = page.goto(URL, wait_until='networkidle')
            assert response.ok
            data = collect_data(page)
            concepts, sketches, territories = data['concepts'], data['sketches'], data['territories']
            assert len(territories) == 6 and {t['id'] for t in territories} == set('ABCDEF')
            assert len(sketches) == 12 and Counter(s['territory'] for s in sketches) == {key: 2 for key in 'ABCDEF'}
            assert len(concepts) == 4 and len({str(c['id']) for c in concepts}) == 4
            advancing = [s for s in sketches if s['decision'] == 'shortlisted']
            paused = [s for s in sketches if s['decision'] != 'shortlisted']
            assert len(advancing) == 4 and len(paused) == 8
            assert {str(s['id']) for s in advancing} == {str(c.get('sketchId', c['id'])) for c in concepts}
            assert all(len(s.get('reason', '').strip()) > 35 for s in sketches)
            expect(page.locator('.territory-card')).to_have_count(6)
            expect(page.locator('.sketch-card')).to_have_count(12)
            expect(page.locator('.concept')).to_have_count(4)
            expect(page.locator('.sketch-decision')).to_have_count(12)
            fingerprints = {hashlib.sha256(repr(geometry(primary_fragment(item))).encode()).hexdigest() for item in sketches}
            assert len(fingerprints) == 12, 'Some initial ideas have identical vector geometry'
            evidence['shortlist'] = [{'id': c['id'], 'name': c['name']} for c in concepts]
            passed('Six territories each contain two nonidentical vector studies; four advance and eight show specific set-aside reasons')

            for item in sketches + concepts:
                source = ET.parse(source_path(item)).getroot()
                assert geometry(source) == geometry(primary_fragment(item)), f'Source mismatch: {item["id"]} / {source_path(item).name}'
            for item in concepts:
                assert not any(local_name(e) in ('text', 'image', 'foreignObject', 'filter') for e in primary_fragment(item).iter())
                for kind in ('horizontal', 'stacked'):
                    root = svg_root(item['lockups'][kind])
                    assert contains_art(root)
                    assert not any(local_name(e) in ('text', 'image', 'foreignObject', 'filter') for e in root.iter()), f'Unoutlined lockup: {item["id"]}/{kind}'
                assert item.get('type', {}).get('license'), f'Missing type license disclosure: {item["id"]}'
            assert (ROOT / 'assets/fonts/sourceserif4/OFL.txt').exists()
            assert (ROOT / 'assets/fonts/bricolagegrotesque/OFL.txt').exists()
            assert (ROOT / 'assets/fonts/instrumentsans/OFL.txt').exists()
            evidence['sourceFiles'] = [str(source_path(item).relative_to(ROOT)) for item in sketches + concepts]
            passed('All displayed studies preserve editable source geometry and transforms; shortlisted art and full-name lockups use vector outlines with licensed type disclosed')

            expect(page.locator('.header-status')).to_have_text('DRAFT — NOT FOR PUBLICATION')
            expect(page.locator('.stage-draft')).to_have_count(4)
            assert all('DRAFT — NOT FOR PUBLICATION' in value for value in page.locator('.stage-draft').all_text_contents())
            expect(page.locator('.rccg-placeholder')).to_have_count(4)
            assert all('NOT SUPPLIED' in text for text in page.locator('.rccg-placeholder').all_text_contents())
            assert page.locator('.rccg-placeholder svg, .rccg-placeholder img').count() == 0
            expect(page.locator('.privacy-note')).to_contain_text('nothing is submitted or approved')
            assert page.locator('input[type=color], [data-palette], .palette-choice').count() == 0
            assert all('B — Sanctuary Strings' not in name and 'Praise Ligature' not in name for name in page.locator('.concept-title h3').all_text_contents())
            passed('Draft status and open decisions remain visible; RCCG is reserved with a clearly missing-asset label; no palette stage or mandatory historical finalist is introduced')

            for territory in territories:
                button = page.locator(f'[data-filter="{territory["id"]}"]')
                button.focus()
                page.keyboard.press('Space')
                expect(button).to_have_attribute('aria-pressed', 'true')
                expect(page.locator('.sketch-card')).to_have_count(2)
                expect(page.locator('#sketch-results')).to_contain_text(f'Territory {territory["id"]}')
                for text in page.locator('.sketch-meta').all_text_contents():
                    assert f'Territory {territory["id"]}' in text
            page.locator('[data-filter="all"]').click()
            expect(page.locator('.sketch-card')).to_have_count(12)
            passed('All six territory filters work with keyboard activation and return the correct two studies; all-ideas restores twelve')

            opener = page.locator('[data-inspect-concept]').first
            opener.click()
            expect(page.locator('#art-dialog')).to_be_visible()
            assert page.evaluate('document.querySelector("#art-dialog").contains(document.activeElement)')
            page.locator('#close-dialog').focus()
            page.keyboard.press('Shift+Tab')
            assert page.locator('#dialog-download').evaluate('(el) => el === document.activeElement')
            page.keyboard.press('Tab')
            assert page.locator('#close-dialog').evaluate('(el) => el === document.activeElement')
            for _ in range(8):
                page.keyboard.press('Tab')
                assert page.evaluate('document.querySelector("#art-dialog").contains(document.activeElement)')
            page.keyboard.press('Escape')
            expect(page.locator('#art-dialog')).not_to_be_visible()
            assert opener.evaluate('(el) => el === document.activeElement')
            sketch_opener = page.locator('[data-inspect-sketch]').last
            sketch_opener.click()
            expect(page.locator('#dialog-title')).to_contain_text(sketches[-1]['name'])
            page.locator('#close-dialog').click()
            assert sketch_opener.evaluate('(el) => el === document.activeElement')
            for item in concepts:
                article = page.locator(f'.concept[data-concept="{item["id"]}"]')
                tabs = article.locator('[role=tab]')
                tabs.first.focus()
                page.keyboard.press('ArrowRight')
                expect(tabs.nth(1)).to_have_attribute('aria-selected', 'true')
                expect(article.locator('[role=tabpanel]:visible')).to_have_count(1)
                page.keyboard.press('End')
                expect(tabs.last).to_have_attribute('aria-selected', 'true')
                page.keyboard.press('Home')
                expect(tabs.first).to_have_attribute('aria-selected', 'true')
            passed('Artwork dialogs trap keyboard focus, close with Escape, and restore the opener; all four concept tablists support arrows, Home, and End')

            page.locator('[data-mode="dark"]').click()
            expect(page.locator('.concept-stage[data-dark="true"]')).to_have_count(4)
            expect(page.locator('[data-overview][data-dark="true"]')).to_have_count(4)
            for stage in page.locator('.concept-stage').all():
                assert stage.evaluate('(el) => getComputedStyle(el).backgroundColor') == 'rgb(17, 17, 17)'
                assert stage.locator('.symbol-art > svg').get_attribute('fill') == '#ffffff'
            page.locator('[data-mode="light"]').click()
            expect(page.locator('.concept-stage[data-dark="false"]')).to_have_count(4)
            for stage in page.locator('.concept-stage').all():
                assert stage.locator('.symbol-art > svg').get_attribute('fill') == '#111111'
            for item in concepts:
                article = page.locator(f'.concept[data-concept="{item["id"]}"]')
                article.locator('[data-tab="sizes"]').click()
                boxes = article.locator('.size-art').evaluate_all('(els) => els.map(el => ({label:Number(el.dataset.size),width:el.getBoundingClientRect().width,height:el.getBoundingClientRect().height}))')
                assert [box['label'] for box in boxes] == [64, 32, 24, 16]
                assert all(abs(box['width'] - box['label']) < .1 and abs(box['height'] - box['label']) < .1 for box in boxes), boxes
                widths = article.locator('.name-width-art').evaluate_all('(els) => els.map(el => ({label:Number(el.dataset.nameWidth),width:el.getBoundingClientRect().width}))')
                assert [box['label'] for box in widths] == [320, 240]
                assert all(abs(box['width'] - box['label']) < .1 for box in widths), widths
                if item.get('compact'):
                    expect(article.locator('.compact-note')).to_be_visible()
                    assert 'full' in article.locator('.compact-note').inner_text().lower()
                assert article.locator('.reverse-card:not(.dark) svg').get_attribute('fill') == '#111111'
                assert article.locator('.reverse-card.dark svg').get_attribute('fill') == '#ffffff'
                article.locator('[data-tab="lockups"]').click()
            passed('Every large stage and overview reverses; size proofs use actual 64/32/24/16px boxes and 320/240px full-name widths, with compact/full-wordmark limits disclosed')

            downloaded = download_all(page, concepts, temporary)
            assert len(downloaded) == len(concepts) * 5
            evidence['onlineDownloads'] = downloaded
            passed('All twenty primary-artwork, horizontal, stacked, paper, and signage downloads are valid draft SVGs and retain source geometry')

            first, last = str(concepts[0]['id']), str(concepts[-1]['id'])
            page.locator(f'[data-save="{first}"]').click()
            page.locator(f'#review-choices input[value="{last}"]').check()
            note = 'Validation review: preserve the shared meaning; geometry, type and color remain unapproved.'
            page.locator('#review-notes').fill(note)
            page.wait_for_function('(value) => JSON.parse(localStorage.getItem("top-strategic-study-04-review")).notes === value', arg=note)
            page.locator('[data-mode="dark"]').click()
            page.reload(wait_until='networkidle')
            collect_data(page)
            expect(page.locator('#review-notes')).to_have_value(note)
            expect(page.locator(f'[data-save="{first}"]')).to_have_attribute('aria-pressed', 'true')
            expect(page.locator(f'#review-choices input[value="{last}"]')).to_be_checked()
            expect(page.locator('.concept-stage[data-dark="true"]')).to_have_count(4)
            with page.expect_download() as pending:
                page.locator('#feedback-form button[type="submit"]').click()
            target = temporary / pending.value.suggested_filename
            pending.value.save_as(target)
            feedback = json.loads(target.read_text())
            assert feedback['identityApproved'] is False
            assert {str(item['id']) for item in feedback['selectedForFurtherReview']} == {first, last}
            assert feedback['notes'] == note
            assert 'DRAFT — NOT FOR PUBLICATION' == feedback['status']
            assert 'Color palette' in feedback['decisionsStillOpen']
            page.locator('#clear-feedback').click()
            expect(page.locator('#review-notes')).to_have_value('')
            assert page.locator('#review-choices input:checked').count() == 0
            passed('Review selections, notes and viewing mode survive reload; downloaded JSON records no identity approval and clearing removes local notes')

            for width in (1440, 768, 390, 320):
                page.set_viewport_size({'width': width, 'height': 900})
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), f'Page overflow at {width}px'
                for item in concepts:
                    article = page.locator(f'.concept[data-concept="{item["id"]}"]')
                    for tab in ('lockups', 'construction', 'sizes', 'applications'):
                        article.locator(f'[data-tab="{tab}"]').click()
                        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), f'Page overflow: {width}px / {item["id"]}/{tab}'
                    article.locator('[data-inspect-concept]').click()
                    expect(page.locator('#art-dialog')).to_be_visible()
                    box = page.locator('#art-dialog').bounding_box()
                    assert box['x'] >= -.5 and box['x'] + box['width'] <= width + .5, box
                    assert page.locator('#art-dialog').evaluate('(el) => el.scrollWidth <= el.clientWidth + 1'), f'Dialog internal overflow at {width}px'
                    page.keyboard.press('Escape')
                    article.locator('[data-tab="lockups"]').click()
            passed('All four proof panels and artwork dialogs fit 1440/768/390/320px screens without page or dialog horizontal overflow')

            offline_context = browser.new_context(viewport={'width': 1440, 'height': 1000},
                accept_downloads=True, reduced_motion='reduce')
            offline_requests, offline_errors = [], []
            offline_context.route('**/*', lambda route: (offline_requests.append(route.request.url), route.abort()))
            offline_page = offline_context.new_page()
            offline_page.on('pageerror', lambda error: offline_errors.append(str(error)))
            offline_page.set_content(offline_file.read_text(), wait_until='networkidle')
            offline_data = collect_data(offline_page)
            expect(offline_page.locator('.sketch-card')).to_have_count(12)
            expect(offline_page.locator('.concept')).to_have_count(4)
            offline_page.locator('[data-filter="F"]').click()
            expect(offline_page.locator('.sketch-card')).to_have_count(2)
            offline_page.locator('[data-mode="dark"]').click()
            expect(offline_page.locator('.concept-stage[data-dark="true"]')).to_have_count(4)
            offline_downloads = download_all(offline_page, offline_data['concepts'], temporary)
            assert len(offline_downloads) == 20
            offline_opener = offline_page.locator('[data-inspect-concept]').first
            offline_opener.click()
            expect(offline_page.locator('#art-dialog')).to_be_visible()
            for _ in range(4):
                offline_page.keyboard.press('Tab')
                assert offline_page.evaluate('document.querySelector("#art-dialog").contains(document.activeElement)')
            offline_page.keyboard.press('Escape')
            assert offline_opener.evaluate('(el) => el === document.activeElement')
            offline_page.locator(f'[data-save="{first}"]').click()
            offline_note = 'Offline review note; no direction approved.'
            offline_page.locator('#review-notes').fill(offline_note)
            with offline_page.expect_download() as pending:
                offline_page.locator('#feedback-form button[type="submit"]').click()
            target = temporary / pending.value.suggested_filename
            pending.value.save_as(target)
            offline_feedback = json.loads(target.read_text())
            assert offline_feedback['identityApproved'] is False
            assert offline_feedback['notes'] == offline_note
            assert first in {str(item['id']) for item in offline_feedback['selectedForFurtherReview']}
            assert not offline_errors, offline_errors
            assert not offline_requests, offline_requests
            evidence['offlineDownloads'] = offline_downloads
            passed('Self-contained HTML renders all art with every network route blocked; filters, reversal, dialogs, feedback export and all twenty SVG downloads still work')

            assert not errors, errors
            assert not remote_requests, remote_requests
            assert not failed_requests, failed_requests
            for svg in (ROOT / 'exports').rglob('*.svg'):
                root = ET.parse(svg).getroot()
                assert local_name(root) == 'svg', str(svg)
            evidence['exportSvgCount'] = len(list((ROOT / 'exports').rglob('*.svg')))
            evidence['offlineSha256'] = hashlib.sha256(offline_file.read_bytes()).hexdigest()
            passed('The online study has no JavaScript errors or remote asset requests; every exported SVG parses successfully')
            browser.close()


if __name__ == '__main__':
    status, failure = 'passed', None
    try:
        run()
    except Exception as error:
        status = 'failed'
        failure = f'{type(error).__name__}: {error}'
        traceback.print_exc()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps({
        'study': 'RCCG Tabernacle of Praise — Strategic Identity Study 04',
        'status': status,
        'checkedAtUtc': datetime.now(timezone.utc).isoformat(),
        'browser': 'Chromium / Python Playwright',
        'checksPassed': len(checks),
        'checks': checks,
        'evidence': evidence,
        'failure': failure,
        'limits': 'Behavior, geometry transfer and delivery checks only. Human visual interpretation and small-size recognition remain review questions. No brand approval, theological endorsement or trademark clearance is implied.'
    }, ensure_ascii=False, indent=2) + '\n')
    print(f'Validation report: {REPORT}', flush=True)
    sys.exit(0 if status == 'passed' else 1)
