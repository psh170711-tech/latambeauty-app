"""Render the 'Clínicas en Seúl' YouTube Short (1080x1920, 30fps).

Inputs : audio/1.wav .. audio/5.wav  (Spanish voiceover from prep_audio.py, one file per scene)
Output : out/seoul_clinicas_short.mp4

Usage  : python3 render.py <workdir>
"""
import math
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
GAP = 0.35  # silence between scenes (s)
TAIL = 1.2  # hold on the last frame (s)

WORK = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
AUDIO = WORK / "audio"
OUT = WORK / "out"
OUT.mkdir(exist_ok=True)

FD = "/usr/share/fonts/opentype/montserrat/"
_fc = {}


def font(weight, size):
    key = (weight, size)
    if key not in _fc:
        _fc[key] = ImageFont.truetype(f"{FD}Montserrat-{weight}.otf", size)
    return _fc[key]


# palette
BG1 = (14, 15, 30)
BG2 = (52, 18, 58)
WHITE = (255, 255, 255)
SOFT = (200, 196, 220)
CORAL = (255, 90, 122)
YELLOW = (255, 212, 59)
RED = (255, 64, 64)
GREEN = (47, 212, 122)
CARD = (34, 30, 56)

# ---------------------------------------------------------------- script
SCENES = [
    ["¿Vienes a Seúl", "para una cirugía?", "Espera.", "Esto nadie te lo dice."],
    ["La zona de las clínicas", "es Gangnam:", "Sinsa, Apgujeong", "y la estación de Gangnam.",
     "Para tratamientos de piel,", "mucha gente va a", "Myeongdong o Cheongdam."],
    ["Pero ojo:", "hay clínicas enormes", "que los coreanos", "llaman «fábricas».",
     "Muchos pacientes por día,", "poco tiempo con el médico."],
    ["Uno:", "que la consulta sea con el cirujano,", "no solo con un coordinador.",
     "Dos:", "nunca pagues el mismo día", "por presión.",
     "Tres:", "busca reseñas con fotos reales,", "no solo en Instagram."],
    ["Comenta CLÍNICA", "y te paso mi checklist en español,", "y cómo verificar si una clínica",
     "está registrada oficialmente", "por el gobierno coreano."],
]


# caption start times (s, relative to each processed clip), set by hand from the
# speech/silence map of audio/N.wav (see prep_audio.py)
CUES = [
    [0.0, 0.72, 2.2, 3.05],
    [0.0, 1.65, 2.4, 4.0, 5.6, 7.35, 8.3],
    [0.0, 1.0, 2.9, 3.9, 4.9, 6.8],
    [0.0, 0.7, 3.5, 5.95, 6.75, 8.68, 9.7, 10.35, 12.7],
    [0.0, 1.12, 3.4, 5.44, 7.5],
]


def dur(p):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout
    return float(out.strip())


# build timeline
timeline = []  # per scene: dict(start, end, chunks=[(text, t0, t1)])
t = 0.25
for i, chunks in enumerate(SCENES, 1):
    wav = AUDIO / f"{i}.wav"
    d = dur(wav)
    cue = CUES[i - 1]
    assert len(cue) == len(chunks)
    spans = [(cue[k], cue[k + 1] if k + 1 < len(cue) else d) for k in range(len(cue))]
    timeline.append({"start": t, "end": t + d, "wav": wav,
                     "chunks": [(c, t + a, t + b) for c, (a, b) in zip(chunks, spans)]})
    t += d + GAP
TOTAL = timeline[-1]["end"] + TAIL
NF = int(TOTAL * FPS)


def chunk_t(si, ci):
    return timeline[si]["chunks"][ci][1]


# ---------------------------------------------------------------- helpers
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease_out(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def ease_back(x):
    x = clamp(x)
    c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2


def prog(now, t0, d=0.35):
    return clamp((now - t0) / d)


def make_bg():
    img = Image.new("RGB", (W, H))
    px = img.load()
    for y in range(H):
        k = y / H
        row = tuple(int(BG1[j] * (1 - k) + BG2[j] * k) for j in range(3))
        for x in range(W):
            px[x, y] = row
    return img


BG = make_bg()


def text_w(d, s, f):
    return d.textlength(s, font=f)


def draw_text_center(img, s, f, y, fill, p=1.0, scale_pop=False, stroke=0, stroke_fill=(0, 0, 0)):
    """Draw centered text with fade + slide (or pop) according to progress p."""
    if p <= 0:
        return
    tmp = Image.new("RGBA", (W, f.size * 2 + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(tmp)
    tw = text_w(d, s, f)
    d.text(((W - tw) / 2, 20), s, font=f, fill=fill + (255,), stroke_width=stroke, stroke_fill=stroke_fill)
    if scale_pop:
        sc = 0.6 + 0.4 * ease_back(p)
        nw, nh = int(tmp.width * sc), int(tmp.height * sc)
        tmp = tmp.resize((max(1, nw), max(1, nh)), Image.LANCZOS)
        x = (W - nw) // 2
        yy = int(y - 20 * sc + (f.size * 2 + 40) * (1 - sc) / 2)
    else:
        x, yy = 0, int(y - 20 + 40 * (1 - ease_out(p)))
    a = tmp.split()[3].point(lambda v: int(v * clamp(p * 1.6)))
    tmp.putalpha(a)
    img.alpha_composite(tmp, (x, yy))


def rrect(d, box, r, fill, outline=None, width=0):
    d.rounded_rectangle(box, r, fill=fill, outline=outline, width=width)


def card_layer(box, r, fill, outline=None, width=0):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    rrect(d, box, r, fill, outline, width)
    return layer, d


def compose(img, layer, p, dy=40):
    if p <= 0:
        return
    a = layer.split()[3].point(lambda v: int(v * clamp(p * 1.5)))
    layer.putalpha(a)
    off = int(dy * (1 - ease_out(p)))
    img.alpha_composite(layer, (0, off))


def pin(d, x, y, s, color):
    d.ellipse((x - s, y - s, x + s, y + s), fill=color)
    d.polygon([(x - s * 0.75, y + s * 0.55), (x + s * 0.75, y + s * 0.55), (x, y + s * 2.1)], fill=color)
    d.ellipse((x - s * 0.4, y - s * 0.4, x + s * 0.4, y + s * 0.4), fill=CARD)


def check(d, x, y, s, color, w=9):
    d.line([(x, y), (x + s * 0.38, y + s * 0.4), (x + s, y - s * 0.45)], fill=color, width=w, joint="curve")


def warn_tri(d, cx, cy, s, color):
    d.polygon([(cx, cy - s), (cx + s * 1.1, cy + s * 0.85), (cx - s * 1.1, cy + s * 0.85)], fill=color)
    d.rectangle((cx - 7, cy - s * 0.45, cx + 7, cy + s * 0.3), fill=BG1)
    d.ellipse((cx - 8, cy + s * 0.45, cx + 8, cy + s * 0.61), fill=BG1)


def person(d, x, y, s, color):
    d.ellipse((x - s * 0.32, y - s, x + s * 0.32, y - s * 0.36), fill=color)
    d.rounded_rectangle((x - s * 0.5, y - s * 0.28, x + s * 0.5, y + s * 0.5), int(s * 0.25), fill=color)


def wrap(d, s, f, maxw):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if text_w(d, trial, f) <= maxw:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
    lines.append(cur)
    return lines


# ---------------------------------------------------------------- scenes
TOP = 250  # keep clear of Shorts top UI


def header(img, now, t0, label, color=CORAL):
    p = prog(now, t0, 0.3)
    f = font("ExtraBold", 40)
    d = ImageDraw.Draw(img)
    tw = text_w(d, label, f)
    layer, ld = card_layer(((W - tw) / 2 - 34, TOP, (W + tw) / 2 + 34, TOP + 76), 38, color + (255,))
    ld.text(((W - tw) / 2, TOP + 15), label, font=f, fill=WHITE)
    compose(img, layer, p, dy=-30)


def scene1(img, now, sc):
    header(img, now, sc["start"], "SEÚL · CIRUGÍA ESTÉTICA")
    draw_text_center(img, "¿Vienes a Seúl", font("Black", 96), 520, WHITE, prog(now, chunk_t(0, 0)))
    draw_text_center(img, "para una cirugía?", font("Black", 96), 640, WHITE, prog(now, chunk_t(0, 1)))
    pe = prog(now, chunk_t(0, 2), 0.4)
    if pe > 0:
        wob = math.sin(now * 18) * 3 * (1 - pe)
        draw_text_center(img, "ESPERA.", font("Black", 190), 820 + wob, YELLOW, pe, scale_pop=True)
    p4 = prog(now, chunk_t(0, 3))
    if p4 > 0:
        draw_text_center(img, "Esto nadie te lo dice.", font("ExtraBold", 66), 1110, WHITE, p4)
        d = ImageDraw.Draw(img)
        lw = 700 * ease_out(prog(now, chunk_t(0, 3) + 0.2, 0.5))
        d.rounded_rectangle(((W - 700) / 2, 1215, (W - 700) / 2 + lw, 1229), 7, fill=CORAL)


def scene2(img, now, sc):
    header(img, now, sc["start"], "¿DÓNDE ESTÁN LAS CLÍNICAS?")
    # card A: cirugía
    pa = prog(now, chunk_t(1, 0), 0.4)
    layer, d = card_layer((70, 380, W - 70, 900), 40, CARD + (255,), CORAL + (255,), 4)
    d.text((120, 420), "CIRUGÍA", font=font("Black", 64), fill=CORAL)
    d.text((120, 500), "Gangnam", font=font("SemiBold", 44), fill=SOFT)
    compose(img, layer, pa)
    rows = [("Sinsa", "Garosu-gil", chunk_t(1, 2)),
            ("Apgujeong", "Rodeo", chunk_t(1, 2) + 0.55),
            ("Estación Gangnam", "", chunk_t(1, 3) + 0.3)]
    for k, (name, sub, t0) in enumerate(rows):
        p = prog(now, t0, 0.35)
        lay, ld = card_layer((0, 0, 1, 1), 0, (0, 0, 0, 0))
        y = 600 + k * 95
        pin(ld, 150, y + 18, 20, CORAL)
        ld.text((200, y), name, font=font("ExtraBold", 54), fill=WHITE)
        if sub:
            nx = 200 + text_w(ld, name, font("ExtraBold", 54)) + 22
            ld.text((nx, y + 14), sub, font=font("Medium", 38), fill=SOFT)
        compose(img, lay, p, dy=0)
    # card B: piel
    pb = prog(now, chunk_t(1, 4), 0.4)
    layer, d = card_layer((70, 950, W - 70, 1290), 40, CARD + (255,), YELLOW + (255,), 4)
    d.text((120, 990), "PIEL / TRATAMIENTOS", font=font("Black", 56), fill=YELLOW)
    compose(img, layer, pb)
    for k, (name, t0) in enumerate([("Myeongdong", chunk_t(1, 6)), ("Cheongdam", chunk_t(1, 6) + 0.6)]):
        p = prog(now, t0, 0.35)
        lay, ld = card_layer((0, 0, 1, 1), 0, (0, 0, 0, 0))
        y = 1090 + k * 95
        pin(ld, 150, y + 18, 20, YELLOW)
        ld.text((200, y), name, font=font("ExtraBold", 54), fill=WHITE)
        compose(img, lay, p, dy=0)


def scene3(img, now, sc):
    p0 = prog(now, sc["start"], 0.3)
    lay, ld = card_layer((0, 0, 1, 1), 0, (0, 0, 0, 0))
    warn_tri(ld, W // 2, 360, 80, RED)
    compose(img, lay, p0, dy=-20)
    draw_text_center(img, "OJO", font("Black", 120), 470, RED, prog(now, chunk_t(2, 0)), scale_pop=True)
    draw_text_center(img, "Clínicas «fábrica»", font("Black", 86), 650, WHITE, prog(now, chunk_t(2, 3)))
    # crowd of patients filling in
    t_crowd = chunk_t(2, 4)
    n_total = 40
    n = int(n_total * ease_out(prog(now, t_crowd, 1.4)))
    if now >= t_crowd:
        d = ImageDraw.Draw(img)
        d.text((90, 815), "Pacientes por día", font=font("ExtraBold", 44), fill=SOFT)
        for i in range(n):
            r, c = divmod(i, 10)
            person(d, 135 + c * 90, 935 + r * 85, 40, CORAL if i % 7 else YELLOW)
    # shrinking doctor-time bar
    t_bar = chunk_t(2, 5)
    pb = prog(now, t_bar, 0.3)
    if pb > 0:
        lay, ld = card_layer((0, 0, 1, 1), 0, (0, 0, 0, 0))
        ld.text((90, 1270), "Tiempo con el médico", font=font("ExtraBold", 44), fill=SOFT)
        ld.rounded_rectangle((90, 1340, W - 90, 1390), 25, fill=CARD)
        frac = 1 - 0.85 * ease_out(prog(now, t_bar + 0.3, 1.2))
        ld.rounded_rectangle((90, 1340, 90 + (W - 180) * frac, 1390), 25, fill=RED)
        compose(img, lay, pb, dy=0)


def scene4(img, now, sc):
    header(img, now, sc["start"], "3 REGLAS ANTES DE ELEGIR")
    tips = [("1", "Consulta con el CIRUJANO,", "no solo con un «coordinador».", chunk_t(3, 0)),
            ("2", "Nunca pagues el mismo día", "por presión.", chunk_t(3, 3)),
            ("3", "Reseñas con fotos reales,", "no solo en Instagram.", chunk_t(3, 6))]
    for k, (num, l1, l2, t0) in enumerate(tips):
        p = prog(now, t0, 0.4)
        if p <= 0:
            continue
        y = 390 + k * 300
        active = (k == 2 or now < tips[k + 1][3]) if k < 2 else True
        oc = GREEN if active else (90, 84, 120)
        lay, ld = card_layer((70, y, W - 70, y + 260), 36, CARD + (255,), oc + (255,), 5 if active else 3)
        ld.ellipse((105, y + 70, 225, y + 190), fill=oc)
        nf = font("Black", 76)
        ld.text((165 - text_w(ld, num, nf) / 2, y + 82), num, font=nf, fill=BG1)
        ld.text((255, y + 58), l1, font=font("ExtraBold", 50), fill=WHITE)
        ld.text((255, y + 135), l2, font=font("SemiBold", 44), fill=SOFT)
        compose(img, lay, p)


def scene5(img, now, sc):
    draw_text_center(img, "Comenta", font("Black", 110), 330, WHITE, prog(now, sc["start"]))
    p = prog(now, chunk_t(4, 0) + 0.2, 0.45)
    if p > 0:
        pulse = 1 + 0.04 * math.sin(max(0, now - chunk_t(4, 0)) * 6)
        f = font("Black", int(140 * pulse))
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        tw = text_w(ld, "CLÍNICA", f)
        ld.rounded_rectangle(((W - tw) / 2 - 50, 490, (W + tw) / 2 + 50, 490 + f.size + 70), 50, fill=CORAL)
        ld.text(((W - tw) / 2, 515), "CLÍNICA", font=f, fill=WHITE)
        compose(img, lay, p, dy=0)
    items = [(["Checklist en español"], chunk_t(4, 1)),
             (["Cómo verificar si una clínica", "está registrada oficialmente", "por el gobierno coreano"],
              chunk_t(4, 2))]
    y = 800
    for lines, t0 in items:
        pi = prog(now, t0, 0.35)
        lay, ld = card_layer((0, 0, 1, 1), 0, (0, 0, 0, 0))
        check(ld, 110, y + 28, 48, GREEN, 11)
        for j, ln in enumerate(lines):
            col = YELLOW if j == 2 else WHITE
            ld.text((185, y + j * 66), ln, font=font("ExtraBold", 50), fill=col)
        compose(img, lay, pi)
        y += 66 * len(lines) + 40
    pf = prog(now, chunk_t(4, 4) + 0.3, 0.5)
    draw_text_center(img, "Información general · No es consejo médico", font("Medium", 32), 1290, SOFT, pf)


RENDER = [scene1, scene2, scene3, scene4, scene5]


def captions(img, now):
    cur = None
    for sc in timeline:
        for c, a, b in sc["chunks"]:
            if a <= now < b + 0.15:
                cur = (c, a)
    if not cur:
        return
    c, a = cur
    p = prog(now, a, 0.12)
    f = font("Black", 62)
    d = ImageDraw.Draw(img)
    lines = wrap(d, c, f, W - 140)
    lh = 78
    y0 = 1470 - (len(lines) - 1) * lh / 2
    for i, ln in enumerate(lines):
        draw_text_center(img, ln, f, y0 + i * lh, WHITE, p, stroke=8, stroke_fill=(10, 8, 20))


def frame(i):
    now = i / FPS
    img = BG.copy().convert("RGBA")
    # active scene = last scene that started
    idx = 0
    for k, sc in enumerate(timeline):
        if now >= sc["start"] - 0.05:
            idx = k
    sc = timeline[idx]
    # crossfade out at scene end
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    RENDER[idx](layer, now, sc)
    nxt = timeline[idx + 1]["start"] if idx + 1 < len(timeline) else 1e9
    fade = clamp((nxt - now) / 0.2)
    if fade < 1:
        layer.putalpha(layer.split()[3].point(lambda v: int(v * fade)))
    img.alpha_composite(layer)
    captions(img, now)
    # progress bar
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W * now / TOTAL, 10), fill=CORAL)
    return img.convert("RGB")


def build_audio():
    inputs, parts = [], []
    for k, sc in enumerate(timeline):
        inputs += ["-i", str(sc["wav"])]
        ms = int(sc["start"] * 1000)
        parts.append(f"[{k}:a]aresample=48000,adelay={ms}|{ms}[a{k}]")
    mix = "".join(f"[a{k}]" for k in range(len(timeline)))
    fc = ";".join(parts) + f";{mix}amix=inputs={len(timeline)}:normalize=0,apad,atrim=0:{TOTAL:.3f},loudnorm=I=-14:TP=-1.5:LRA=11[out]"
    wav = OUT / "voice_mix.wav"
    subprocess.run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", fc, "-map", "[out]",
                    "-ar", "48000", "-ac", "2", str(wav)], check=True)
    return wav


def main():
    if "--still" in sys.argv:
        for ts in [float(x) for x in sys.argv[sys.argv.index("--still") + 1].split(",")]:
            frame(int(ts * FPS)).save(OUT / f"still_{ts:05.1f}.png")
        return
    wav = build_audio()
    out = OUT / "seoul_clinicas_short.mp4"
    ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", str(wav),
                           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                           "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(out)],
                          stdin=subprocess.PIPE)
    for i in range(NF):
        ff.stdin.write(frame(i).tobytes())
    ff.stdin.close()
    ff.wait()
    srt = OUT / "seoul_clinicas_short.srt"
    with open(srt, "w") as fh:
        n = 1
        for sc in timeline:
            for c, a, b in sc["chunks"]:
                ts = lambda x: f"{int(x//3600):02}:{int(x%3600//60):02}:{int(x%60):02},{int(x*1000%1000):03}"
                fh.write(f"{n}\n{ts(a)} --> {ts(b)}\n{c}\n\n")
                n += 1
    print("wrote", out, f"{TOTAL:.1f}s")


if __name__ == "__main__":
    main()
