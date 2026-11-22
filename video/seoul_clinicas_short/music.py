"""Synthesize a royalty-free lo-fi pop backing track (no samples, pure numpy).

Usage: python3 music.py <out.wav> <seconds> [mute_start:mute_end ...]
  e.g. python3 music.py out/music.wav 49 2.4:3.3
Mute windows drop the beat out (with a short fade) for dramatic pauses.
"""
import sys
import wave

import numpy as np

SR = 44100
BPM = 100
BEAT = 60 / BPM
rng = np.random.default_rng(7)


def note(n):
    """MIDI note number -> Hz."""
    return 440.0 * 2 ** ((n - 69) / 12)


def onepole_lp(x, cutoff):
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i, v in enumerate(x):  # fine for short buffers
        acc = (1 - a) * v + a * acc
        y[i] = acc
    return y


def lp_fast(x, cutoff):
    """Vectorised-ish low-pass: repeated moving average (good enough for pads/noise)."""
    k = max(1, int(SR / cutoff / 2))
    ker = np.ones(k) / k
    for _ in range(3):
        x = np.convolve(x, ker, mode="same")
    return x


def env(n, a, d, s, r, sus_len):
    A, D, R = int(a * SR), int(d * SR), int(r * SR)
    S = max(0, sus_len - A - D)
    e = np.concatenate([np.linspace(0, 1, A, False), np.linspace(1, s, D, False),
                        np.full(S, s), np.linspace(s, 0, R)])
    return e[:n] if len(e) >= n else np.pad(e, (0, n - len(e)))


def saw(f, t):
    return 2 * ((t * f) % 1.0) - 1


def tri(f, t):
    return 2 * np.abs(2 * ((t * f) % 1.0) - 1) - 1


def add(buf, start, sig):
    i = int(start * SR)
    if i >= len(buf):
        return
    j = min(len(buf), i + len(sig))
    buf[i:j] += sig[: j - i]


def main():
    out = sys.argv[1]
    total = float(sys.argv[2])
    mutes = [tuple(map(float, m.split(":"))) for m in sys.argv[3:]]
    n = int(total * SR)
    pad = np.zeros(n)
    bass = np.zeros(n)
    pluck = np.zeros(n)
    drums = np.zeros(n)
    kick_env = np.zeros(n)

    # A minor: Am - F - C - G (one bar each)
    chords = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]
    roots = [45, 41, 48, 43]
    bar = 4 * BEAT
    nbars = int(np.ceil(total / bar)) + 1

    for b in range(nbars):
        t0 = b * bar
        ch, root = chords[b % 4], roots[b % 4]
        # pad
        L = int((bar + 0.4) * SR)
        t = np.arange(L) / SR
        sig = sum(saw(note(m) * d, t) for m in ch for d in (0.997, 1.003)) / 6
        sig = lp_fast(sig, 900) * env(L, 0.35, 0.3, 0.8, 0.4, int(bar * SR))
        add(pad, t0, sig * 0.35)
        # bass: beats 1, 2.5, 3
        for off, ln in [(0, 1.2), (1.5, 0.45), (2, 1.6)]:
            L = int(ln * BEAT * SR)
            t = np.arange(L) / SR
            s = np.sin(2 * np.pi * note(root - 12 + 12) * t) + 0.3 * np.sin(4 * np.pi * note(root) * t)
            add(bass, t0 + off * BEAT, s * env(L, 0.01, 0.1, 0.7, 0.08, L) * 0.5)
        # pluck arpeggio in 8ths
        arp = [ch[0] + 12, ch[1] + 12, ch[2] + 12, ch[1] + 24, ch[2] + 12, ch[1] + 12, ch[0] + 24, ch[2] + 12]
        for k, m in enumerate(arp):
            L = int(0.5 * SR)
            t = np.arange(L) / SR
            s = tri(note(m), t) * np.exp(-t * 9)
            add(pluck, t0 + k * BEAT / 2, s * (0.22 if k % 2 == 0 else 0.15))
        # drums
        for beat in range(4):
            tb = t0 + beat * BEAT
            if beat in (0, 2):  # kick
                L = int(0.35 * SR)
                t = np.arange(L) / SR
                f = 50 + 90 * np.exp(-t * 30)
                k_ = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)
                add(drums, tb, k_ * 0.9)
                add(kick_env, tb, np.exp(-np.arange(int(0.3 * SR)) / SR * 10))
            if beat in (1, 3):  # soft clap
                L = int(0.25 * SR)
                t = np.arange(L) / SR
                nz = rng.standard_normal(L)
                nz = nz - lp_fast(nz, 1200)
                add(drums, tb, nz * np.exp(-t * 18) * 0.28)
            for h in (0, 0.5):  # hats
                L = int(0.06 * SR)
                nz = rng.standard_normal(L)
                nz = nz - lp_fast(nz, 6000)
                add(drums, tb + h * BEAT, nz * np.exp(-np.arange(L) / SR * 60) * (0.10 if h else 0.07))

    duck = 1 - 0.45 * np.clip(kick_env, 0, 1)  # sidechain pump on pad
    mix = pad * duck + bass * 0.8 + pluck + drums
    # warm it up a little
    mix = 0.85 * mix + 0.15 * lp_fast(mix, 3000)

    # fades + mute windows
    g = np.ones(n)
    fi, fo = int(0.3 * SR), int(1.5 * SR)
    g[:fi] *= np.linspace(0, 1, fi)
    g[-fo:] *= np.linspace(1, 0, fo)
    for a, b in mutes:
        ia, ib, f = int(a * SR), int(b * SR), int(0.06 * SR)
        g[ia:ib] = 0
        g[max(0, ia - f):ia] *= np.linspace(1, 0, min(f, ia))
        g[ib:ib + f] *= np.linspace(0, 1, len(g[ib:ib + f]))
    mix *= g
    mix = mix / (np.max(np.abs(mix)) + 1e-9) * 0.89

    st = np.stack([mix, mix], axis=1)
    pcm = (st * 32767).astype(np.int16)
    with wave.open(out, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print("wrote", out, f"{total:.1f}s")


if __name__ == "__main__":
    main()
