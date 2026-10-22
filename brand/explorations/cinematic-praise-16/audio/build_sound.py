#!/usr/bin/env python3
"""Synthesize an original, optional 14-second sound study; no sampled recordings."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess

import numpy as np
from scipy import signal
from scipy.io import wavfile

HERE = Path(__file__).resolve().parent
RATE = 48_000
SECONDS = 14
COUNT = RATE * SECONDS
RNG = np.random.default_rng(226104)


def envelope(length, attack=.1, release=1.0):
    """Half-cosine attack/release with zero endpoint slopes."""
    n = int(round(length * RATE))
    a = min(n, int(round(attack * RATE)))
    r = min(n-a, int(round(release * RATE)))
    env = np.ones(n)
    if a:
        env[:a] = .5 - .5 * np.cos(np.linspace(0, np.pi, a))
    if r:
        env[-r:] = .5 + .5 * np.cos(np.linspace(0, np.pi, r))
    return env


def place(mix, mono, at, gain=1, pan=0):
    start = int(round(at * RATE))
    n = min(len(mono), len(mix)-start)
    assert start >= 0 and n >= 0
    angle = (np.clip(pan, -1, 1) + 1) * np.pi / 4
    mix[start:start+n, 0] += mono[:n] * gain * np.cos(angle)
    mix[start:start+n, 1] += mono[:n] * gain * np.sin(angle)


def pad(frequency, seconds, attack=.9, release=2.2):
    t = np.arange(int(round(seconds * RATE))) / RATE
    wave = np.zeros_like(t)
    # Gently beating fundamentals and low overtones give a warm body.
    for ratio, amount in [(1, .76), (2, .12), (3, .035), (4, .009)]:
        phase = RNG.uniform(-np.pi, np.pi)
        wave += amount * np.sin(2*np.pi*frequency*ratio*t + phase)
    wave += .1*np.sin(2*np.pi*frequency*1.0006*t)
    wave += .1*np.sin(2*np.pi*frequency*.9994*t)
    wave *= 1 + .018*np.sin(2*np.pi*.31*t)
    return wave * envelope(seconds, attack, release)


def felt_glass(frequency, seconds=3.5, velocity=1):
    t = np.arange(int(round(seconds * RATE))) / RATE
    wave = np.zeros_like(t)
    for ratio, amount, decay in [(1, .94, 1.25), (2.001, .115, .7), (3.983, .026, .35), (5.01, .009, .22)]:
        wave += amount * np.exp(-t/decay) * np.sin(2*np.pi*frequency*ratio*t)
    # A very soft filtered mallet transient; this is synthesized noise.
    transient = RNG.normal(size=len(t))
    transient = signal.sosfilt(signal.butter(2, 1600, fs=RATE, output='sos'), transient)
    wave += .012 * transient * np.exp(-t/.028)
    return velocity * wave * envelope(seconds, .014, .8)


def air(seconds, low, high):
    n = int(round(seconds*RATE))
    noise = RNG.normal(size=n)
    filtered = signal.sosfilt(signal.butter(2, [low, high], btype='bandpass', fs=RATE, output='sos'), noise)
    return filtered / (np.std(filtered) + 1e-12)


def diffusion(mix):
    # Short diffuse room, with gentle cross-channel reflections, not a long hall.
    delays = [.047, .073, .113, .173, .233, .317, .421, .563, .719, .887, 1.109, 1.401]
    amounts = [.061, .055, .049, .043, .038, .033, .029, .024, .019, .014, .010, .007]
    room = np.zeros_like(mix)
    softened = signal.sosfilt(signal.butter(2, 4200, fs=RATE, output='sos'), mix, axis=0)
    for index, (delay, amount) in enumerate(zip(delays, amounts)):
        offset = int(round(delay*RATE))
        source = softened[:, ::-1] if index % 2 else softened
        room[offset:] += amount * source[:-offset]
    return mix + room


def main():
    HERE.mkdir(exist_ok=True, parents=True)
    mix = np.zeros((COUNT, 2), dtype=np.float64)
    # Frequencies form an open D major/add9 color, without an existing melody.
    d2, a2, d3, a3, d4, fs4, a4, e5, d5, fs5 = 73.4162, 110, 146.8324, 220, 293.6648, 369.9944, 440, 659.2551, 587.3295, 739.9888
    for frequency, at, length, gain, pan in [
        (d2, .12, 7.2, .016, -.1), (d3, .16, 6.5, .050, .05),
        (a2, .34, 6.0, .015, .12), (a3, 1.1, 5.1, .017, -.15),
    ]:
        place(mix, pad(frequency, length, 1.2, 2.1), at, gain, pan)
    place(mix, air(5.6, 240, 1300)*envelope(5.6, 1.7, 2.3), .15, .0014, -.35)
    place(mix, air(5.6, 280, 1600)*envelope(5.6, 1.9, 2.0), .25, .0014, .35)

    # Four distinct voices enter from left to right, then coexist.
    voices = [
        {'at': 2.4, 'frequency': d4, 'pan': -.6, 'velocity': .112, 'note': 'D4'},
        {'at': 3.05, 'frequency': fs4, 'pan': -.2, 'velocity': .104, 'note': 'F#4'},
        {'at': 3.7, 'frequency': a4, 'pan': .2, 'velocity': .095, 'note': 'A4'},
        {'at': 4.35, 'frequency': e5, 'pan': .6, 'velocity': .071, 'note': 'E5'},
    ]
    for event in voices:
        place(mix, felt_glass(event['frequency']), event['at'], event['velocity'], event['pan'])

    # Harmonic bloom supports the shared architectural rise.
    for frequency, gain, pan in [(d3, .037, -.2), (a3, .029, .25), (d4, .023, -.35), (fs4, .014, .35), (e5/2, .012, .1)]:
        place(mix, pad(frequency, 5.2, 1.25, 2.1), 4.9, gain, pan)
    rise = [
        {'at': 5.28, 'frequency': d4, 'pan': -.42, 'velocity': .060, 'note': 'D4'},
        {'at': 5.94, 'frequency': a4, 'pan': -.1, 'velocity': .070, 'note': 'A4'},
        {'at': 6.60, 'frequency': d5, 'pan': .16, 'velocity': .072, 'note': 'D5'},
        {'at': 7.28, 'frequency': fs5, 'pan': .42, 'velocity': .061, 'note': 'F#5'},
    ]
    for event in rise:
        place(mix, felt_glass(event['frequency'], 3.1), event['at'], event['velocity'], event['pan'])
    for at, low, high, gain, pan in [(5.05, 300, 800, .0028, -.35), (5.65, 600, 1350, .0025, .1), (6.25, 950, 2100, .0021, .3)]:
        place(mix, air(2.8, low, high)*envelope(2.8, 1.0, 1.45), at, gain, pan)

    # An open, warm resolution; no impact boom or borrowed recording.
    for frequency, gain, pan in [(d3, .052, -.12), (a3, .032, .17), (d4, .033, -.28), (fs4, .020, .28), (e5/2, .014, .05)]:
        place(mix, pad(frequency, 4.6, .22, 3.4), 9.15, gain, pan)
    place(mix, felt_glass(d5, 4.2), 9.18, .085, .04)
    place(mix, felt_glass(a4, 3.8), 9.23, .039, -.24)
    place(mix, felt_glass(e5, 3.5), 9.29, .022, .24)

    mix = diffusion(mix)
    mix = signal.sosfilt(signal.butter(2, 35, btype='highpass', fs=RATE, output='sos'), mix, axis=0)
    # Final whole-piece fades remove residual filter/reverb tails cleanly.
    mix *= envelope(SECONDS, .12, 1.1)[:, None]
    peak = float(np.max(np.abs(mix)))
    mix *= (10**(-6.8/20)) / peak
    # Deterministic TPDF dither for 16-bit delivery. The outermost samples are silent.
    dither = (RNG.random(mix.shape)-RNG.random(mix.shape)) / 65536
    dither *= envelope(SECONDS, .12, 1.1)[:, None]
    pcm = np.rint(np.clip(mix+dither, -1, 1)*32767).astype(np.int16)
    pcm[:32] = 0
    pcm[-32:] = 0
    target = HERE / 'shared-rhythm-original-sound-study-DRAFT.wav'
    wavfile.write(target, RATE, pcm)
    rate, decoded = wavfile.read(target)
    float_pcm = decoded.astype(np.float64)/32768
    upsampled = signal.resample_poly(float_pcm, 4, 1, axis=0)
    rms = np.sqrt(np.mean(float_pcm**2, axis=0))
    assert rate == RATE and decoded.shape == (COUNT, 2)
    assert np.isfinite(mix).all() and not (np.abs(decoded) >= 32767).any()
    assert not decoded[:32].any() and not decoded[-32:].any()
    assert np.max(np.abs(upsampled)) < .5
    report = {
        'status': 'DRAFT — NOT FOR PUBLICATION',
        'optionalSoundStudy': True, 'durationSeconds': SECONDS, 'sampleRate': RATE,
        'channels': 2, 'pcmBitDepth': 16, 'samplesPerChannel': COUNT,
        'method': 'Original deterministic additive/modal synthesis and filtered noise. No sampled recordings, existing melody, vocals or external audio assets.',
        'auditioned': False,
        'auditionLimitation': 'Audio input/playback audition is unavailable in this execution context. Technical checks do not constitute subjective mix or mastering approval.',
        'sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
        'bytes': target.stat().st_size,
        'peakDBFS': round(float(20*np.log10(np.max(np.abs(float_pcm)))), 3),
        'oversampled4xTruePeakApproxDBFS': round(float(20*np.log10(np.max(np.abs(upsampled)))), 3),
        'channelRMSDBFS': [round(float(20*np.log10(value)), 3) for value in rms],
        'channelDCOffset': [float(value) for value in float_pcm.mean(axis=0)],
        'firstAndLast32SamplesSilent': True, 'finiteSignal': True, 'noFullScaleClips': True,
        'entryVoices': voices, 'riseVoices': rise,
        'sync': {'quietOpening': [0, 2.4], 'fourEnteringVoices': [2.4, 4.35], 'sharedRise': [5, 8.5], 'harmonicResolution': 9.18, 'tailAcrossFinalHold': [10.5, 14]},
    }
    analysis = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', str(target), '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True, check=True)
    summary = analysis.stderr[analysis.stderr.rfind('Summary:'):].split('\n[out#', 1)[0].strip()
    report['ffmpegLoudnessSummary'] = summary
    report['integratedLoudnessLUFS'] = float(re.search(r'I:\s+(-?[\d.]+) LUFS', summary).group(1))
    report['loudnessRangeLU'] = float(re.search(r'LRA:\s+(-?[\d.]+) LU', summary).group(1))
    (HERE / 'sound-checks.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({key: report[key] for key in ['durationSeconds', 'sampleRate', 'channels', 'bytes', 'peakDBFS', 'oversampled4xTruePeakApproxDBFS', 'channelRMSDBFS', 'sha256']}))


if __name__ == '__main__':
    main()
