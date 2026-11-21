"""Tighten voiceover pacing for Shorts.

Reads  <workdir>/audio_raw/{1,2,3,4a,4b,4c,5}.wav
Writes <workdir>/audio/{1..5}.wav  (long pauses shortened, 4a+4b+4c joined)
"""
import subprocess
import sys
from pathlib import Path

MAX_PAUSE = 0.42   # pauses longer than this get cut down to it
EDGE = 0.08        # silence kept at clip start/end
JOIN_GAP = 0.30    # gap between tip clips 4a/4b/4c

WORK = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
RAW, OUT = WORK / "audio_raw", WORK / "audio"
OUT.mkdir(exist_ok=True)


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                 "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout)


def silences(p):
    r = subprocess.run(["ffmpeg", "-i", str(p), "-af", "silencedetect=n=-35dB:d=0.12", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    s, out = None, []
    for line in r.splitlines():
        if "silence_start" in line:
            s = float(line.split("silence_start:")[1].split()[0])
        elif "silence_end" in line and s is not None:
            out.append((s, float(line.split("silence_end:")[1].split()[0])))
            s = None
    return out


def keep_ranges(p):
    d = dur(p)
    cuts = []
    for s, e in silences(p):
        if s <= 0.01:
            cuts.append((0, max(0, e - EDGE)))
        elif e >= d - 0.01:
            cuts.append((s + EDGE, d))
        elif e - s > MAX_PAUSE:
            mid = (s + e) / 2
            cuts.append((mid - (e - s) / 2 + MAX_PAUSE / 2, mid + (e - s) / 2 - MAX_PAUSE / 2))
    keep, t = [], 0.0
    for a, b in sorted(cuts):
        if a > t:
            keep.append((t, a))
        t = max(t, b)
    if t < d:
        keep.append((t, d))
    return keep


def tighten(src, dst):
    ks = keep_ranges(src)
    parts = [f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS[p{i}]" for i, (a, b) in enumerate(ks)]
    fc = ";".join(parts) + ";" + "".join(f"[p{i}]" for i in range(len(ks))) + f"concat=n={len(ks)}:v=0:a=1[o]"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-filter_complex", fc, "-map", "[o]", str(dst)],
                   check=True)


tmp = WORK / "tmp_audio"
tmp.mkdir(exist_ok=True)
for name in ["1", "2", "3", "5"]:
    tighten(RAW / f"{name}.wav", OUT / f"{name}.wav")
for name in ["4a", "4b", "4c"]:
    tighten(RAW / f"{name}.wav", tmp / f"{name}.wav")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(tmp / "4a.wav"), "-i", str(tmp / "4b.wav"),
                "-i", str(tmp / "4c.wav"), "-filter_complex",
                f"[0:a]apad=pad_dur={JOIN_GAP}[a];[1:a]apad=pad_dur={JOIN_GAP}[b];[a][b][2:a]concat=n=3:v=0:a=1[o]",
                "-map", "[o]", str(OUT / "4.wav")], check=True)
for f in sorted(OUT.glob("*.wav")):
    print(f.name, round(dur(f), 2))
