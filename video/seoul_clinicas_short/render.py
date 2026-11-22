"""Render the 'Clínicas en Seúl' YouTube Short (1080x1920, 30fps).

Inputs : audio/1.wav .. audio/5.wav  (Spanish voiceover from prep_audio.py, one file per scene)
         broll/*.jpg|png              (background photos, see broll/CREDITS.md)
         music.py                     (synthesized backing track, rendered on the fly)
Output : out/seoul_clinicas_short.mp4

Usage  : python3 render.py <workdir>
"""
import math
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

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


BROLL = WORK / "broll"
ZOOM = 1.14  # Ken Burns headroom


def _cover(path, blur=0):
    im = Image.open(path).convert("RGB")
    sc = max(W * ZOOM / im.width, H * ZOOM / im.height)
    im = im.resize((int(im.width * sc + 1), int(im.height * sc + 1)), Image.LANCZOS)
    if blur:
        im = im.filter(ImageFilter.GaussianBlur(blur))
    return im


_img_cache = {}


def photo(name, blur=0):
    key = (name, blur)
    if key not in _img_cache:
        _img_cache[key] = _cover(BROLL / name, blur) if name != "_phone" else phone_shot()
    return _img_cache[key]


def kenburns(im, k, mode):
    """k in 0..1 across the shot; mode = (zoom_from, zoom_to, pan_x, pan_y)."""
    z0, z1, px_, py_ = mode
    z = z0 + (z1 - z0) * k
    cw, ch = W * ZOOM / z, H * ZOOM / z
    cw, ch = min(cw, im.width), min(ch, im.height)
    cx = im.width / 2 + px_ * (k - 0.5) * (im.width - cw)
    cy = im.height / 2 + py_ * (k - 0.5) * (im.height - ch)
    box = (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)
    return im.resize((W, H), Image.BILINEAR, box=box)


def _grad_overlay():
    """Darken top and bottom for text legibility."""
    g = Image.new("L", (1, H))
    for y in range(H):
        k = y / H
        top = max(0, 1 - k / 0.35) * 150
        bot = max(0, (k - 0.55) / 0.45) * 215
        g.putpixel((0, y), int(min(235, 70 + top + bot)))
    g = g.resize((W, H))
    ov = Image.new("RGBA", (W, H), (8, 6, 18, 0))
    ov.putalpha(g)
    return ov


GRAD = _grad_overlay()


def phone_shot():
    """Graphic for tip 3: a phone showing photo reviews, over a blurred cafe-ish backdrop."""
    bg = _cover(BROLL / "myeongdong.jpg", blur=28)
    im = bg.convert("RGBA")
    d = ImageDraw.Draw(im)
    ox, oy = (im.width - 620) // 2, (im.height - 1180) // 2 - 60
    d.rounded_rectangle((ox, oy, ox + 620, oy + 1180), 80, fill=(15, 15, 20))
    d.rounded_rectangle((ox + 22, oy + 22, ox + 598, oy + 1158), 62, fill=(245, 243, 248))
    d.rounded_rectangle((ox + 250, oy + 40, ox + 370, oy + 66), 13, fill=(15, 15, 20))
    srcs = ["ai_consulta.png", "ai_fabrica.png", "ai_pago.png", "gangnam_daero.jpg"]
    for k in range(4):
        y = oy + 110 + k * 260
        d.ellipse((ox + 50, y, ox + 110, y + 60), fill=(220, 200, 230))
        d.rounded_rectangle((ox + 125, y + 8, ox + 330, y + 26), 9, fill=(200, 196, 210))
        for st in range(5):
            d.polygon([(ox + 130 + st * 30 + dx, y + 40 + dy) for dx, dy in
                       [(10, 0), (13, 8), (21, 8), (15, 13), (17, 21), (10, 16), (3, 21), (5, 13), (-1, 8), (7, 8)]],
                      fill=YELLOW)
        th = Image.open(BROLL / srcs[k]).convert("RGB")
        th = th.resize((180, int(180 * th.height / th.width))).crop((0, 0, 180, 150))
        th = th.filter(ImageFilter.GaussianBlur(2))
        im.paste(th, (ox + 380, y))
        d.rounded_rectangle((ox + 50, y + 90, ox + 360, y + 106), 8, fill=(215, 212, 225))
        d.rounded_rectangle((ox + 50, y + 120, ox + 300, y + 136), 8, fill=(215, 212, 225))
        d.line((ox + 50, y + 225, ox + 570, y + 225), fill=(225, 222, 232), width=2)
    return im.convert("RGB")


# shot list: (scene, chunk, offset_s, image, kenburns mode)
SHOTS = [
    (0, 0, 0.0, "seoul_night.jpg", (1.0, 1.10, 0.0, 0.6)),
    (0, 2, 0.0, "seoul_night.jpg", (1.18, 1.26, 0.0, 0.4)),          # punch-in on "Espera."
    (1, 0, 0.0, "gangnam_daero.jpg", (1.0, 1.10, 0.0, -0.5)),
    (1, 2, 0.0, "garosugil.jpg", (1.0, 1.12, 0.8, 0.0)),
    (1, 2, 0.8, "apgujeong_rodeo.jpg", (1.05, 1.15, -0.8, 0.0)),
    (1, 3, 0.0, "gangnam_station.jpg", (1.0, 1.10, 0.0, 0.5)),
    (1, 4, 0.0, "myeongdong.jpg", (1.0, 1.12, 0.0, 0.6)),
    (2, 0, 0.0, "ai_fabrica.png", (1.0, 1.14, 0.0, 0.8)),
    (3, 0, 0.0, "ai_consulta.png", (1.0, 1.12, 0.5, 0.0)),
    (3, 3, 0.0, "ai_pago.png", (1.0, 1.12, -0.5, 0.3)),
    (3, 6, 0.0, "_phone", (1.0, 1.10, 0.0, -0.4)),
    (4, 0, 0.0, "seoul_night.jpg|blur", (1.05, 1.12, 0.0, 0.0)),
]
XF = 0.25  # crossfade (s)


def shot_times():
    out = []
    for k, (si, ci, off, name, mode) in enumerate(SHOTS):
        t0 = chunk_t(si, ci) + off - (0.05 if ci == 0 else 0)
        out.append([t0, name, mode])
    for k in range(len(out)):
        out[k].append(out[k + 1][0] if k + 1 < len(out) else TOTAL)
    out[0][0] = 0.0
    return out


SHOT_T = None


def background(now):
    global SHOT_T
    if SHOT_T is None:
        SHOT_T = shot_times()

    def render(sh):
        t0, name, mode, t1 = sh
        nm, blur = (name.split("|")[0], 30) if "|blur" in name else (name, 0)
        k = clamp((now - t0) / max(0.1, t1 - t0 + XF))
        return kenburns(photo(nm, blur), k, mode)

    cur = max(i for i, sh in enumerate(SHOT_T) if sh[0] <= now)
    img = render(SHOT_T[cur])
    if cur > 0 and now - SHOT_T[cur][0] < XF:
        prev = render(SHOT_T[cur - 1])
        hard = SHOT_T[cur][1] == SHOT_T[cur - 1][1]  # same photo -> hard cut (punch-in)
        if not hard:
            img = Image.blend(prev, img, (now - SHOT_T[cur][0]) / XF)
    img = img.convert("RGBA")
    img.alpha_composite(GRAD)
    return img


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
    draw_text_center(img, "¿Vienes a Seúl", font("Black", 96), 520, WHITE, prog(now, chunk_t(0, 0)), stroke=7, stroke_fill=(10, 8, 20))
    draw_text_center(img, "para una cirugía?", font("Black", 96), 640, WHITE, prog(now, chunk_t(0, 1)), stroke=7, stroke_fill=(10, 8, 20))
    pe = prog(now, chunk_t(0, 2), 0.4)
    if pe > 0:
        wob = math.sin(now * 18) * 3 * (1 - pe)
        draw_text_center(img, "ESPERA.", font("Black", 190), 820 + wob, YELLOW, pe, scale_pop=True, stroke=9, stroke_fill=(10, 8, 20))
    p4 = prog(now, chunk_t(0, 3))
    if p4 > 0:
        draw_text_center(img, "Esto nadie te lo dice.", font("ExtraBold", 66), 1110, WHITE, p4, stroke=6, stroke_fill=(10, 8, 20))
        d = ImageDraw.Draw(img)
        lw = 700 * ease_out(prog(now, chunk_t(0, 3) + 0.2, 0.5))
        d.rounded_rectangle(((W - 700) / 2, 1215, (W - 700) / 2 + lw, 1229), 7, fill=CORAL)


def loc_tag(img, now, t0, t1, cat, cat_col, name, sub=""):
    """Big location label for the current shot (fades in at t0, out at t1)."""
    p = prog(now, t0, 0.3) * clamp((t1 - now) / 0.2)
    if p <= 0:
        return
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    fc, fn, fs = font("Black", 44), font("Black", 104), font("SemiBold", 46)
    y = 470
    cw = text_w(d, cat, fc)
    d.rounded_rectangle((90, y, 90 + cw + 56, y + 74), 37, fill=cat_col + (255,))
    d.text((118, y + 13), cat, font=fc, fill=BG1)
    pin(d, 122, y + 150, 26, cat_col)
    d.text((170, y + 100), name, font=fn, fill=WHITE, stroke_width=6, stroke_fill=(10, 8, 20))
    if sub:
        d.text((172, y + 225), sub, font=fs, fill=WHITE, stroke_width=4, stroke_fill=(10, 8, 20))
    compose(img, lay, p, dy=0)


def scene2(img, now, sc):
    header(img, now, sc["start"], "¿DÓNDE ESTÁN LAS CLÍNICAS?")
    c = lambda k: chunk_t(1, k)
    end = sc["end"] + 0.3
    loc_tag(img, now, c(0) + 0.3, c(2), "CIRUGÍA", CORAL, "Gangnam", "La zona de las clínicas")
    loc_tag(img, now, c(2), c(2) + 0.8, "CIRUGÍA", CORAL, "Sinsa", "Garosu-gil")
    loc_tag(img, now, c(2) + 0.8, c(3), "CIRUGÍA", CORAL, "Apgujeong", "Rodeo")
    loc_tag(img, now, c(3), c(4), "CIRUGÍA", CORAL, "Gangnam", "Estación de Gangnam")
    loc_tag(img, now, c(4), c(6), "PIEL", YELLOW, "Tratamientos", "de piel")
    loc_tag(img, now, c(6), end, "PIEL", YELLOW, "Myeongdong", "y Cheongdam")


def scene3(img, now, sc):
    p0 = prog(now, sc["start"], 0.3)
    lay, ld = card_layer((0, 0, 1, 1), 0, (0, 0, 0, 0))
    warn_tri(ld, W // 2, 360, 80, RED)
    compose(img, lay, p0, dy=-20)
    draw_text_center(img, "OJO", font("Black", 130), 465, RED, prog(now, chunk_t(2, 0)), scale_pop=True,
                     stroke=8, stroke_fill=(10, 8, 20))
    draw_text_center(img, "Clínicas «fábrica»", font("Black", 92), 650, WHITE, prog(now, chunk_t(2, 3)),
                     stroke=8, stroke_fill=(10, 8, 20))
    pm = prog(now, chunk_t(2, 4), 0.3)
    if pm > 0:
        lay, ld = card_layer((0, 0, 1, 1), 0, (0, 0, 0, 0))
        f = font("ExtraBold", 48)
        lbl = "MUCHOS PACIENTES POR DÍA"
        tw = text_w(ld, lbl, f)
        ld.rounded_rectangle(((W - tw) / 2 - 36, 830, (W + tw) / 2 + 36, 910), 40, fill=RED + (235,))
        ld.text(((W - tw) / 2, 843), lbl, font=f, fill=WHITE)
        compose(img, lay, pm, dy=20)
    t_bar = chunk_t(2, 5)
    pb = prog(now, t_bar, 0.3)
    if pb > 0:
        lay, ld = card_layer((60, 1150, W - 60, 1330), 34, (14, 12, 28, 215))
        ld.text((100, 1175), "Tiempo con el médico", font=font("ExtraBold", 46), fill=WHITE)
        ld.rounded_rectangle((100, 1250, W - 100, 1300), 25, fill=(60, 56, 84))
        frac = 1 - 0.85 * ease_out(prog(now, t_bar + 0.3, 1.2))
        ld.rounded_rectangle((100, 1250, 100 + (W - 200) * frac, 1300), 25, fill=RED)
        compose(img, lay, pb, dy=0)


def scene4(img, now, sc):
    header(img, now, sc["start"], "3 REGLAS ANTES DE ELEGIR")
    tips = [("1", "Consulta con el CIRUJANO,", "no solo con un «coordinador».", chunk_t(3, 0)),
            ("2", "Nunca pagues el mismo día", "por presión.", chunk_t(3, 3)),
            ("3", "Reseñas con fotos reales,", "no solo en Instagram.", chunk_t(3, 6))]
    for k, (num, l1, l2, t0) in enumerate(tips):
        t1 = tips[k + 1][3] if k < 2 else sc["end"] + 0.4
        p = prog(now, t0, 0.35) * clamp((t1 - now) / 0.2)
        if p <= 0:
            continue
        y = 400
        lay, ld = card_layer((60, y, W - 60, y + 250), 36, (14, 12, 28, 225), GREEN + (255,), 5)
        ld.ellipse((95, y + 65, 215, y + 185), fill=GREEN)
        nf = font("Black", 76)
        ld.text((155 - text_w(ld, num, nf) / 2, y + 77), num, font=nf, fill=BG1)
        ld.text((245, y + 58), l1, font=font("ExtraBold", 50), fill=WHITE)
        ld.text((245, y + 132), l2, font=font("SemiBold", 44), fill=SOFT)
        # 1/2/3 dots
        for j in range(3):
            ld.ellipse((W / 2 - 60 + j * 50, y + 285, W / 2 - 40 + j * 50, y + 305),
                       fill=GREEN if j == k else (255, 255, 255, 120))
        compose(img, lay, p, dy=30)


def scene5(img, now, sc):
    pp = prog(now, sc["start"], 0.3)
    lay, _ = card_layer((50, 290, W - 50, 1340), 48, (14, 12, 28, 170))
    compose(img, lay, pp, dy=0)
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
    draw_text_center(img, "Información general · No es consejo médico", font("Medium", 32), 1260, SOFT, pf)


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
    img = background(now)
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


MUSIC_VOL = 0.25  # backing track level (about 12 dB under the voice in pauses, ~15 dB under speech)


def build_audio():
    """Voice clips on the timeline + synthesized music, ducked under the voice."""
    music = OUT / "music.wav"
    mute = f"{chunk_t(0, 2) - 0.08:.2f}:{chunk_t(0, 3) + 0.05:.2f}"  # drop the beat on "Espera."
    subprocess.run([sys.executable, str(Path(__file__).with_name("music.py")), str(music), f"{TOTAL:.2f}", mute],
                   check=True)
    inputs, parts = [], []
    for k, sc in enumerate(timeline):
        inputs += ["-i", str(sc["wav"])]
        ms = int(sc["start"] * 1000)
        parts.append(f"[{k}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={ms}|{ms}[a{k}]")
    n = len(timeline)
    mix = "".join(f"[a{k}]" for k in range(n))
    fc = (";".join(parts)
          + f";{mix}amix=inputs={n}:normalize=0,apad,atrim=0:{TOTAL:.3f},loudnorm=I=-14:TP=-2:LRA=11,aresample=48000,apad,atrim=0:{TOTAL:.3f},asplit[v1][v2]"
          + f";[{n}:a]aresample=48000,volume={MUSIC_VOL}[m]"
          + ";[m][v2]sidechaincompress=threshold=0.08:ratio=2.5:attack=20:release=350[md]"
          + ";[v1][md]amix=inputs=2:normalize=0,alimiter=limit=0.89:level=false,apad[out]")
    wav = OUT / "mix.wav"
    subprocess.run(["ffmpeg", "-y", "-v", "error", *inputs, "-i", str(music), "-filter_complex", fc,
                    "-map", "[out]", "-ar", "48000", "-ac", "2", "-t", f"{TOTAL:.3f}", str(wav)], check=True)
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
                           "-c:a", "aac", "-b:a", "192k", "-t", f"{NF / FPS:.3f}", "-movflags", "+faststart", str(out)],
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
