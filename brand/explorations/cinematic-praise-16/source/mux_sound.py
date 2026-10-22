#!/usr/bin/env python3
"""Add the optional original sound study without re-encoding the film image."""
from pathlib import Path
import hashlib
import json
import subprocess

STUDY = Path(__file__).resolve().parent.parent


def probe(path):
    return json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_format', '-show_streams', '-of', 'json', str(path)]))


def main():
    silent = STUDY / 'exports/shared-rhythm-cinematic-1080p-SILENT-DRAFT.mp4'
    wav = STUDY / 'audio/shared-rhythm-original-sound-study-DRAFT.wav'
    output = STUDY / 'exports/shared-rhythm-cinematic-1080p-SOUND-DRAFT.mp4'
    subprocess.run(['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error', '-i', str(silent), '-i', str(wav), '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-t', '14', '-movflags', '+faststart', str(output)], check=True)
    before, after = probe(silent), probe(output)
    video = next(s for s in after['streams'] if s['codec_type'] == 'video')
    sound = next(s for s in after['streams'] if s['codec_type'] == 'audio')
    assert len(before['streams']) == 1 and len(after['streams']) == 2
    assert video['width'] == 1920 and video['height'] == 1080 and video['nb_frames'] == '420'
    assert video['r_frame_rate'] == '30/1' and video['codec_name'] == 'h264'
    assert abs(float(after['format']['duration'])-14) < .05
    assert sound['codec_name'] == 'aac' and sound['sample_rate'] == '48000' and sound['channels'] == 2
    def packet_hashes(path):
        data = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_packets', '-show_data_hash', 'sha256', '-show_entries', 'packet=data_hash', '-of', 'json', str(path)]))
        return [p['data_hash'] for p in data['packets']]
    assert packet_hashes(silent) == packet_hashes(output)
    sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    report = {'status': 'DRAFT — NOT FOR PUBLICATION', 'durationSeconds': 14, 'frames': 420, 'size': [1920,1080], 'fps': 30, 'videoPacketsByteIdenticalToSilentVersion': True, 'audio': 'Optional original synthesized sound study; not auditioned by the assistant.', 'silentSHA256': sha(silent), 'WAV_SHA256': sha(wav), 'soundMP4_SHA256': sha(output), 'publicationApproval': False}
    (STUDY / 'exports/mux-checks.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print('Created optional sound MP4; all420video packet hashes match the silent film.')


if __name__ == '__main__':
    main()
