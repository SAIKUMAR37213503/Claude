"""Synthesize the 34-second instrumental score for the Object Talk reel.

One recurring motif (E G A G E | D E C) that changes mood and instrumentation per scene:
  0-4   celesta + woodblock tick-tock, dreamy pad
  4-10  pizzicato strings + light tabla, playful
  10-16 staccato bassoon/plucks, comic "uh-oh"
  16-22 pause, then bansuri variation with a comic slide down at 0:21
  22-30 piano + warm strings in A minor, rising back to C major
  30-34 bansuri/celesta lullaby, final chord fades out by 0:34

Usage: python3 score.py out.wav
"""
import sys
import wave

import numpy as np

SR = 48000
TOTAL = 34.07
rng = np.random.default_rng(7)


def hz(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)


def t_axis(dur):
    return np.arange(int(dur * SR)) / SR


def adsr(n, a=0.01, d=0.1, s=0.7, r=0.1):
    e = np.full(n, s, float)
    A, D, R = int(a * SR), int(d * SR), int(r * SR)
    A = min(A, n); e[:A] = np.linspace(0, 1, A, endpoint=False)
    D = min(D, max(0, n - A)); e[A:A + D] = np.linspace(1, s, D, endpoint=False)
    R = min(R, n); e[n - R:] *= np.linspace(1, 0, R)
    return e


def lowpass(x, cutoff):
    """One-pole low-pass via FFT-free recursion approximated with an exponential kernel."""
    k = np.exp(-2 * np.pi * cutoff / SR)
    n = int(np.ceil(np.log(1e-4) / np.log(k))) if k > 0 else 1
    kern = (1 - k) * k ** np.arange(max(n, 1))
    return np.convolve(x, kern)[:len(x)]


# ---------------------------------------------------------------- instruments
def celesta(f, dur, vel=0.5):
    t = t_axis(dur + 1.2)
    idx = 1.8 * np.exp(-t / 0.15)
    y = np.sin(2 * np.pi * f * t + idx * np.sin(2 * np.pi * 4 * f * t))
    y += 0.25 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t / 0.3)
    return vel * y * np.exp(-t / 0.7) * adsr(len(t), 0.003, 0.05, 1, 0.05)


def pizz(f, dur, vel=0.5):
    """Karplus-Strong plucked string."""
    n = int((dur + 0.6) * SR)
    p = max(2, int(SR / f))
    buf = rng.uniform(-1, 1, p)
    out = np.empty(n)
    i = 0
    while i < n:
        m = min(p, n - i)
        out[i:i + m] = buf[:m]
        buf = 0.994 * 0.5 * (buf + np.roll(buf, -1))
        i += p
    out = lowpass(out, 2600)
    return vel * out * np.exp(-np.arange(n) / SR / 0.35)


def tabla(kind, vel=0.4):
    t = t_axis(0.6)
    if kind == 'ge':  # bass stroke with a little pitch bend
        f = 95 + 35 * (1 - np.exp(-t / 0.08))
        y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.22)
    else:  # 'na' treble ring
        y = (np.sin(2 * np.pi * 540 * t) + 0.5 * np.sin(2 * np.pi * 1290 * t)) * np.exp(-t / 0.09)
        y += 0.5 * rng.uniform(-1, 1, len(t)) * np.exp(-t / 0.006)
    return vel * y


def woodblock(high=True, vel=0.25):
    t = t_axis(0.12)
    f = 1250 if high else 900
    return vel * (np.sin(2 * np.pi * f * t) + 0.4 * np.sin(2 * np.pi * 2.7 * f * t)) * np.exp(-t / 0.018)


def bansuri(freqs, vel=0.45):
    """freqs: per-sample frequency array (allows slides)."""
    n = len(freqs)
    t = np.arange(n) / SR
    vib = 1 + 0.006 * np.sin(2 * np.pi * 5.3 * t) * np.clip((t - 0.15) / 0.3, 0, 1)
    ph = 2 * np.pi * np.cumsum(freqs * vib) / SR
    y = np.sin(ph) + 0.18 * np.sin(2 * ph) + 0.06 * np.sin(3 * ph)
    breath = lowpass(lowpass(rng.uniform(-1, 1, n), 1500), 1500) * 0.1
    return vel * (y + breath) * adsr(n, 0.06, 0.1, 0.85, min(0.12, n / SR / 3))


def bassoon(f, dur, vel=0.4):
    t = t_axis(dur)
    y = sum((1 / k) * np.exp(-((k * f - 520) / 600) ** 2 * 0.5) * np.sin(2 * np.pi * k * f * t) for k in range(1, 14))
    return vel * y * adsr(len(t), 0.02, 0.05, 0.8, 0.05)


def piano(f, dur, vel=0.5):
    t = t_axis(dur + 1.5)
    y = np.zeros_like(t)
    for k in range(1, 9):
        fk = k * f * np.sqrt(1 + 0.0004 * k * k)
        y += (1 / k ** 1.4) * np.sin(2 * np.pi * fk * t) * np.exp(-t * (0.9 + 0.6 * k))
    e = np.ones_like(t); rel = int(0.25 * SR); end = int(dur * SR)
    e[end:end + rel] = np.linspace(1, 0, min(rel, len(t) - end)); e[end + rel:] = 0
    return vel * y * e * adsr(len(t), 0.004, 0.01, 1, 0.01)


def pad(midis, dur, vel=0.12, attack=0.6, release=0.8):
    """Warm string pad: detuned additive saws, slow attack."""
    t = t_axis(dur)
    y = np.zeros_like(t)
    for m in midis:
        for det in (-0.08, 0, 0.07):
            f = hz(m + det)
            for k in range(1, 9):
                y += (1 / k) * np.exp(-k / 3.5) * np.sin(2 * np.pi * k * f * t + rng.uniform(0, 6.28))
    y /= len(midis) * 3
    return vel * y * adsr(len(t), attack, 0.2, 1, release)


# ---------------------------------------------------------------- mixing helpers
L = np.zeros(int(TOTAL * SR) + SR)
R = np.zeros_like(L)


def put(sig, at, pan=0.0, gain=1.0, end=None):
    """Mix a mono signal at time `at` (s); optionally hard-stop with a short fade at `end`."""
    i = int(at * SR)
    if end is not None:
        m = max(0, int((end - at) * SR))
        sig = sig[:m].copy()
        f = min(len(sig), int(0.04 * SR))
        if f:
            sig[-f:] *= np.linspace(1, 0, f)
    j = min(len(L), i + len(sig))
    sig = sig[:j - i] * gain
    L[i:j] += sig * np.sqrt(0.5 * (1 - pan))
    R[i:j] += sig * np.sqrt(0.5 * (1 + pan))


# motif: (semitones above C, beats) - E G A G E | D E C
MOTIF = [(4, .5), (7, .5), (9, 1), (7, 1), (4, 1), (2, 1), (4, 1), (0, 2)]
# the same contour mapped into A minor: C E F E C | B C A
MOTIF_AM = [(3, .5), (7, .5), (8, 1), (7, 1), (3, 1), (2, 1), (3, 1), (0, 2)]


def play_motif(start, beat, base, inst, end, pan=0.0, gain=1.0, staccato=1.0, motif=MOTIF):
    t = start
    for semi, beats in motif:
        if t >= end:
            break
        dur = beats * beat
        inst(base + semi, t, dur * staccato, pan, gain, end)
        t += dur
    return t


def I_celesta(m, t, d, pan, g, end): put(celesta(hz(m), d), t, pan, g, end)
def I_pizz(m, t, d, pan, g, end): put(pizz(hz(m), d), t, pan, g, end)
def I_piano(m, t, d, pan, g, end): put(piano(hz(m), d), t, pan, g, end)
def I_bassoon(m, t, d, pan, g, end): put(bassoon(hz(m), d), t, pan, g, end)
def I_bansuri(m, t, d, pan, g, end): put(bansuri(np.full(int(d * SR), hz(m))), t, pan, g, end)


B = 0.6  # 100 BPM

# ---------------- 0:00-0:04 quiet night intro
put(pad([48, 55, 64], 4.6, 0.10, attack=1.2), 0.0, 0, 1, 4.3)
for k in range(int(4 / B)):
    put(woodblock(k % 2 == 0), k * B + 0.05, 0.35 if k % 2 else -0.35, 0.8)
play_motif(0.3, 0.45, 84, I_celesta, 4.0, pan=-0.1, gain=0.55)

# ---------------- 0:04-0:10 playful pizzicato + tabla
S = 4.0
chords = [(48, [60, 64, 67]), (53, [60, 65, 69]), (55, [59, 62, 67]), (48, [60, 64, 67])]
for bar in range(3):
    root, ch = chords[bar % 4]
    for b in range(4):
        t = S + bar * 4 * B * 0.62 + b * B * 0.62
        if t < 10:
            put(pizz(hz(root if b % 2 == 0 else root + 7), 0.3), t, -0.3, 0.7, 10)
            put(pizz(hz(ch[b % 3]), 0.2), t + B * 0.31, 0.3, 0.35, 10)
for k in range(int(6 / (B * 0.31))):
    t = S + k * B * 0.31
    put(tabla('ge' if k % 4 == 0 else 'na', 0.3 if k % 4 == 0 else 0.16), t, 0.15, 1, 10)
play_motif(S + 0.15, 0.37, 72, I_pizz, 10, pan=0.1, gain=1.3)
play_motif(S + 3.15, 0.37, 79, I_pizz, 10, pan=-0.1, gain=1.0)

# ---------------- 0:10-0:16 comic tension, staccato
S = 10.0
for k, m in enumerate([48, 47, 46, 45, 44, 43, 44, 43]):
    put(bassoon(hz(m - 12), 0.22), S + k * 0.72, -0.2, 0.9, 16)
for k in range(16):
    put(pizz(hz([60, 63, 66][k % 3]), 0.12), S + 0.36 + k * 0.36, 0.35, 0.25, 16)
t = play_motif(S + 0.2, 0.36, 72, I_bassoon, 13.5, pan=0.05, gain=1.0, staccato=0.45)
# "uh-oh": two falling staccato notes
put(bassoon(hz(67), 0.25), 13.9, 0, 0.8); put(bassoon(hz(61), 0.5), 14.3, 0, 0.8)
put(pad([48, 51, 54], 2.0, 0.07), 14.0, 0, 1, 16)

# ---------------- 0:16-0:22 playful pause, then cheeky bansuri, slide down at 0:21
S = 16.0
put(woodblock(True, 0.2), S + 0.6)
put(woodblock(False, 0.2), S + 1.0)
t = S + 1.3
for semi, beats in [(4, .5), (5, .25), (4, .25), (7, .5), (9, 1), (7, .5), (4, .5), (2, .5), (4, .5)]:
    d = beats * 0.5
    put(bansuri(np.full(int(d * SR * 0.95), hz(76 + semi - 4))), t, 0.1, 0.5)
    t += d
# comic slide down from G5 to C5 starting at 0:21
n = int(0.75 * SR)
glide = hz(79) * (hz(72) / hz(79)) ** (np.linspace(0, 1, n) ** 1.6)
put(bansuri(np.concatenate([np.full(int(0.25 * SR), hz(79)), glide])), 20.75, 0.1, 0.6, 22)
for k in range(int(4.5 / 0.3)):
    put(tabla('ge' if k % 4 == 0 else 'na', 0.22 if k % 4 == 0 else 0.11), S + 1.3 + k * 0.3, -0.15, 1, 22)
put(pad([48, 55, 64], 4.6, 0.06), S + 1.3, 0, 1, 22)

# ---------------- 0:22-0:30 emotional turn, A minor -> C major
S = 22.0
prog = [([45, 57, 60, 64], 2.0), ([41, 57, 60, 65], 2.0), ([48, 55, 60, 64], 2.0), ([43, 55, 59, 62], 2.0)]
t = S
for notes, d in prog:
    put(pad(notes[1:], d + 0.6, 0.14, attack=0.5, release=0.6), t, 0, 1, 30.3)
    put(piano(hz(notes[0]), d * 0.9, 0.35), t, -0.25, 1)
    put(piano(hz(notes[0] + 12), d * 0.4, 0.2), t + 1.0, -0.25, 1)
    t += d
play_motif(S + 0.2, 0.62, 69, I_piano, 27.6, pan=0.15, gain=0.6, motif=MOTIF_AM)
# hopeful rise G A B -> C
for k, m in enumerate([67, 69, 71]):
    put(piano(hz(m), 0.6, 0.5), 28.1 + k * 0.6, 0.15, 1)

# ---------------- 0:30-0:34 lullaby resolution
S = 30.0
put(piano(hz(48), 3.5, 0.35), S, -0.25, 1)
put(pad([60, 64, 67, 72], TOTAL - S, 0.13, attack=0.4, release=3.2), S, 0, 1)
play_motif(S + 0.05, 0.42, 72, I_bansuri, 33.2, pan=0.1, gain=0.7)
play_motif(S + 0.05, 0.42, 84, I_celesta, 33.2, pan=-0.2, gain=0.25)
put(celesta(hz(84), 1.0, 0.4), 33.0, -0.2, 0.6)


# ---------------------------------------------------------------- reverb + master
def reverb(x, secs=1.8, mix=0.25):
    n = int(secs * SR)
    ir = rng.standard_normal(n) * np.exp(-np.arange(n) / SR / (secs / 6.9))
    ir = lowpass(ir, 5000); ir /= np.sqrt((ir ** 2).sum())
    size = 1 << int(np.ceil(np.log2(len(x) + n)))
    wet = np.fft.irfft(np.fft.rfft(x, size) * np.fft.rfft(ir, size), size)[:len(x)]
    return x * (1 - mix) + wet * mix * 1.2


L, R = reverb(L), reverb(R)
N = int(TOTAL * SR)
L, R = L[:N], R[:N]
fade = int(1.2 * SR)  # everything gone by 0:34
L[-fade:] *= np.linspace(1, 0, fade) ** 2
R[-fade:] *= np.linspace(1, 0, fade) ** 2
peak = max(np.abs(L).max(), np.abs(R).max())
L, R = L / peak * 0.89, R / peak * 0.89

out = np.stack([L, R], 1)
with wave.open(sys.argv[1] if len(sys.argv) > 1 else 'score.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((out * 32767).astype('<i2').tobytes())
print('wrote', N / SR, 's')
