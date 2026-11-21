"""Friday 20 November 2026 — a one-page world news front page.

Everything is drawn from geometry, hand-authored continent outlines and text.
No photographs, no downloads, no network: two runs write byte-identical PNGs.
"""

from PIL import Image, ImageDraw, ImageFont

S = 2  # supersample, then Lanczos downsample for clean edges at 1024 px
W = H = 1024 * S

PAPER = (249, 245, 235)
INK = (22, 24, 28)
RED = (163, 33, 38)
BLUE = (29, 66, 108)
TEAL = (26, 110, 110)
GOLD = (183, 132, 30)
GREY = (108, 110, 112)
SOFT = (235, 229, 214)
NAVY = (18, 32, 58)
SEA = (223, 234, 238)
LAND = (214, 199, 166)
WHITE = (255, 255, 255)

F = "C:/Windows/Fonts/"
SERIF = F + "georgiab.ttf"
SERIF_I = F + "georgiai.ttf"
SANS = F + "arialbd.ttf"
REG = F + "arial.ttf"


def fp(path, px):
    return ImageFont.truetype(path, int(px * S))


def p(x, y):
    return (int(x * S), int(y * S))


def bb(b):
    return tuple(int(v * S) for v in b)


def txt(d, x, y, s, f, col=INK, anchor=None):
    d.text(p(x, y), s, font=f, fill=col, anchor=anchor)


def rect(d, b, fill=None, outline=None, width=1):
    d.rectangle(bb(b), fill=fill, outline=outline, width=max(1, int(width * S)))


def rrect(d, b, r, fill=None, outline=None, width=1):
    d.rounded_rectangle(bb(b), radius=int(r * S), fill=fill, outline=outline,
                        width=max(1, int(width * S)))


def line(d, pts, col, width=1):
    d.line([p(x, y) for x, y in pts], fill=col, width=max(1, int(width * S)), joint="curve")


def poly(d, pts, fill=None, outline=None, width=1):
    d.polygon([p(x, y) for x, y in pts], fill=fill)
    if outline:
        d.line([p(x, y) for x, y in pts] + [p(*pts[0])], fill=outline,
               width=max(1, int(width * S)), joint="curve")


def ell(d, b, fill=None, outline=None, width=1):
    d.ellipse(bb(b), fill=fill, outline=outline, width=max(1, int(width * S)))


def arc(d, b, a0, a1, col, width=1):
    d.arc(bb(b), a0, a1, fill=col, width=max(1, int(width * S)))


def card_icon(d, i, x, y):
    """Small text-free illustrations, sized to fit a 78x42 card thumbnail."""
    rect(d, (x, y, x + 78, y + 42), fill=SOFT)
    if i == 0:  # UK-EU flags
        rect(d, (x + 6, y + 10, x + 34, y + 32), fill=BLUE)
        line(d, [(x + 6, y + 10), (x + 34, y + 32)], WHITE, 1)
        line(d, [(x + 34, y + 10), (x + 6, y + 32)], WHITE, 1)
        rect(d, (x + 40, y + 10, x + 68, y + 32), fill=(24, 48, 112))
        ell(d, (x + 50, y + 17, x + 58, y + 25), fill=GOLD)
    elif i == 1:  # COP31 globe + thermometer
        ell(d, (x + 8, y + 6, x + 38, y + 36), outline=TEAL, width=2)
        line(d, [(x + 8, y + 21), (x + 38, y + 21)], TEAL, 1)
        rect(d, (x + 54, y + 8, x + 59, y + 34), fill=RED)
        ell(d, (x + 51, y + 28, x + 62, y + 39), fill=RED)
    elif i == 2:  # missile over hills
        poly(d, [(x + 4, y + 40), (x + 26, y + 20), (x + 48, y + 40)], fill=GREY)
        line(d, [(x + 56, y + 4), (x + 72, y + 22)], RED, 2)
        ell(d, (x + 69, y + 19, x + 75, y + 25), fill=RED)
    elif i == 3:  # three leaders
        for k, col in enumerate((BLUE, RED, GOLD)):
            cx = x + 16 + k * 20
            ell(d, (cx - 5, y + 10, cx + 5, y + 20), fill=INK)
            rect(d, (cx - 9, y + 20, cx + 9, y + 36), fill=col)
    elif i == 4:  # broken shield
        pts = [(x + 39, y + 3), (x + 64, y + 12), (x + 59, y + 36),
               (x + 39, y + 42), (x + 19, y + 36), (x + 14, y + 12)]
        poly(d, pts, outline=BLUE, width=2)
        line(d, [(x + 26, y + 14), (x + 42, y + 26), (x + 32, y + 34)], RED, 2)
    elif i == 5:  # quake mountains
        poly(d, [(x + 4, y + 40), (x + 28, y + 10), (x + 48, y + 36),
                 (x + 64, y + 14), (x + 76, y + 40)], fill=GREY)
        line(d, [(x + 4, y + 40), (x + 76, y + 40)], RED, 1)
    elif i == 6:  # tanker + oil drop
        poly(d, [(x + 8, y + 26), (x + 60, y + 26), (x + 54, y + 38),
                 (x + 16, y + 38)], fill=NAVY)
        ell(d, (x + 58, y + 4, x + 70, y + 16), fill=RED)
    elif i == 7:  # spacecraft + planet
        ell(d, (x + 42, y + 6, x + 70, y + 34), fill=(150, 142, 130))
        line(d, [(x + 6, y + 34), (x + 38, y + 18)], GOLD, 2)
        poly(d, [(x + 38, y + 18), (x + 30, y + 15), (x + 32, y + 22)], fill=GOLD)
    elif i == 8:  # pill + cells
        rrect(d, (x + 10, y + 14, x + 54, y + 30), 8, fill=WHITE, outline=RED, width=2)
        line(d, [(x + 32, y + 14), (x + 32, y + 30)], RED, 1)
        for k in range(3):
            ell(d, (x + 60 + k * 6, y + 20, x + 64 + k * 6, y + 24), fill=GREY)
    elif i == 9:  # oil rig
        for k in range(4):
            line(d, [(x + 16 + k * 10, y + 40), (x + 30 + k * 4, y + 10)], GREY, 1)
        line(d, [(x + 14, y + 10), (x + 52, y + 10)], INK, 2)
    elif i == 10:  # crowd
        for k in range(7):
            cx = x + 10 + (k % 4) * 18
            cy = y + 18 + (k // 4) * 16
            ell(d, (cx - 4, cy - 5, cx + 1, cy), fill=INK)
            rect(d, (cx - 4, cy, cx + 2, cy + 8), fill=GREY)
    else:  # boat
        poly(d, [(x + 12, y + 26), (x + 60, y + 26), (x + 52, y + 38),
                 (x + 20, y + 38)], fill=(120, 84, 52))
        line(d, [(x + 36, y + 26), (x + 36, y + 6)], GREY, 1)
        line(d, [(x + 36, y + 8), (x + 58, y + 22)], WHITE, 2)


def wrap(d, s, font, maxw, limit=None):
    """Wrap on measured pixel width. maxw is in 1024-space units."""
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if cur and d.textlength(t, font=font) > maxw * S:
            lines.append(cur)
            cur = w
        else:
            cur = t
    if cur:
        lines.append(cur)
    if limit and len(lines) > limit:
        lines = lines[:limit]
        last = lines[-1]
        while last and d.textlength(last + "…", font=font) > maxw * S:
            last = last[:-1]
        lines[-1] = last + "…"
    return lines


# ---------- small illustrations ----------

def draw_river_bridges(d, x, y, w=300, h=122):
    rect(d, (x, y, x + w, y + h), fill=NAVY)
    for i in range(26):
        sx = x + (i * 47) % w
        sy = y + (i * 29) % (h - 30)
        ell(d, (sx, sy, sx + 1.5, sy + 1.5), fill=(180, 195, 220))
    for i in range(11):
        bx = x + i * 30
        ell(d, (bx, y + h - 20, bx + 18, y + h - 2), fill=(32, 52, 82))
    # river
    poly(d, [(x, y + h - 34), (x + w, y + h - 30), (x + w, y + h), (x, y + h)], fill=(38, 76, 112))
    # three bridges, middle one broken
    for i in range(3):
        bx = x + 22 + i * 96
        if i == 1:
            line(d, [(bx, y + h - 26), (bx + 30, y + h - 34)], GOLD, 5)
            line(d, [(bx + 62, y + h - 34), (bx + 92, y + h - 28)], GOLD, 5)
            poly(d, [(bx + 34, y + h - 30), (bx + 46, y + h - 44),
                     (bx + 56, y + h - 26)], fill=RED)
        else:
            line(d, [(bx, y + h - 26), (bx + 92, y + h - 30)], GOLD, 5)
        for k in range(5):
            line(d, [(bx + k * 18, y + h - 28), (bx + k * 18, y + h - 14)], GOLD, 2)
    # incoming missiles
    for i in range(5):
        ax = x + 30 + i * 58
        line(d, [(ax + 44, y + 4), (ax, y + 50 + (i % 2) * 8)], RED, 3)
        ell(d, (ax - 4, y + 46 + (i % 2) * 8, ax + 5, y + 55 + (i % 2) * 8), fill=RED)
    rrect(d, (x + 6, y + 6, x + 118, y + 28), 3, RED)
    txt(d, x + 12, y + 17, "MISSILE BARRAGE", fp(SANS, 13), WHITE)


def draw_cyclone(d, x, y, w=300, h=122):
    rect(d, (x, y, x + w, y + h), fill=(151, 202, 214))
    poly(d, [(x, y + 18), (x + 108, y + 34), (x + 168, y + 74),
             (x + 120, y + h), (x, y + h)], fill=(222, 205, 169))
    line(d, [(x + 108, y + 34), (x + 168, y + 74), (x + 120, y + h)], (150, 132, 100), 2)
    ell(d, (x + 112, y + 50, x + 118, y + 56), fill=RED)
    ell(d, (x + 112, y + 50, x + 118, y + 56), outline=WHITE, width=1)
    txt(d, x + 82, y + 58, "GOPALPUR", fp(SANS, 10), INK)
    for r in (18, 34, 50):
        arc(d, (x + 196 - r, y + 60 - r, x + 196 + r, y + 60 + r), 200, 520, WHITE, 4)
    for r in (14, 28):
        arc(d, (x + 196 - r, y + 60 - r, x + 196 + r, y + 60 + r), 20, 330, WHITE, 3)
    ell(d, (x + 190, y + 54, x + 202, y + 66), fill=WHITE)
    txt(d, x + 158, y + 100, "BAY OF BENGAL", fp(SANS, 11), (40, 82, 100))
    rrect(d, (x + 6, y + 6, x + 148, y + 28), 3, RED)
    txt(d, x + 12, y + 17, "CYCLONE AKVAN", fp(SANS, 13), WHITE)
    rrect(d, (x + 206, y + 90, x + 292, y + 112), 3, WHITE)
    txt(d, x + 212, y + 101, "LANDFALL 8 AM", fp(SANS, 11), RED)


def draw_market(d, x, y, w=300, h=122):
    rect(d, (x, y, x + w, y + h), fill=NAVY)
    for i in range(7):
        gy = y + 16 + i * 15
        line(d, [(x + 6, gy), (x + w - 6, gy)], (38, 56, 84), 1)
    pts = [(x + 10, y + 18), (x + 52, y + 32), (x + 96, y + 26),
           (x + 140, y + 58), (x + 188, y + 48), (x + 244, y + 98)]
    line(d, pts, RED, 4)
    for px, py in pts[::2]:
        ell(d, (px - 3, py - 3, px + 3, py + 3), fill=RED)
    labels = [("TAIEX  -6.2%", x + 178), ("KOSPI  -5.2%", x + 178), ("NIKKEI -5.1%", x + 178)]
    for i, (s, lx) in enumerate(labels):
        txt(d, lx, y + 20 + i * 16, s, fp(SANS, 12), WHITE)
    rrect(d, (x + 6, y + 6, x + 104, y + 26), 3, RED)
    txt(d, x + 12, y + 16, "AI SELL-OFF", fp(SANS, 13), WHITE)


def draw_flags(d, x, y, w=210, h=56):
    rect(d, (x, y, x + w, y + h), fill=SOFT)
    # UK
    rect(d, (x + 8, y + 8, x + 78, y + 46), fill=BLUE)
    line(d, [(x + 8, y + 8), (x + 78, y + 46)], WHITE, 3)
    line(d, [(x + 78, y + 8), (x + 8, y + 46)], WHITE, 3)
    line(d, [(x + 43, y + 8), (x + 43, y + 46)], WHITE, 4)
    line(d, [(x + 8, y + 27), (x + 78, y + 27)], WHITE, 4)
    # EU
    rect(d, (x + 96, y + 8, x + 166, y + 46), fill=(24, 48, 112))
    for i in range(6):
        a = -1.4 + i * 0.47
        cx, cy = x + 131 + 11 * __import__("math").cos(a), y + 27 + 11 * __import__("math").sin(a)
        ell(d, (cx - 2, cy - 2, cx + 2, cy + 2), fill=GOLD)
    line(d, [(x + 168, y + 27), (x + 200, y + 27)], RED, 4)
    poly(d, [(x + 200, y + 27), (x + 192, y + 21), (x + 192, y + 33)], fill=RED)


def draw_globe_thermo(d, x, y, w=210, h=56):
    rect(d, (x, y, x + w, y + h), fill=(214, 234, 226))
    ell(d, (x + 12, y + 6, x + 52, y + 46), outline=TEAL, width=3)
    line(d, [(x + 12, y + 26), (x + 52, y + 26)], TEAL, 2)
    arc(d, (x + 22, y + 6, x + 42, y + 46), 90, 270, TEAL, 2)
    rect(d, (x + 74, y + 12, x + 82, y + 46), fill=RED)
    ell(d, (x + 70, y + 32, x + 86, y + 48), fill=RED)
    rect(d, (x + 98, y + 8, x + 200, y + 32), fill=WHITE, outline=INK, width=1)
    txt(d, x + 103, y + 14, "COP31: NO DEAL", fp(SANS, 12), RED)
    txt(d, x + 100, y + 38, "fossil fuels omitted", fp(REG, 11), INK)


def draw_missile_field(d, x, y, w=210, h=56):
    rect(d, (x, y, x + w, y + h), fill=(216, 226, 206))
    for i in range(6):
        bx = x + 12 + i * 33
        poly(d, [(bx, y + 44), (bx + 8, y + 24), (bx + 16, y + 44)], fill=GREY)
    line(d, [(x + 120, y + 6), (x + 150, y + 30)], RED, 3)
    ell(d, (x + 146, y + 26, x + 154, y + 34), fill=RED)
    rrect(d, (x + 6, y + 4, x + 70, y + 22), 2, RED)
    txt(d, x + 10, y + 11, "KH-101 IN POLAND", fp(SANS, 10), WHITE)


def draw_shield(d, x, y, w=210, h=56):
    rect(d, (x, y, x + w, y + h), fill=SOFT)
    pts = [(x + 40, y + 6), (x + 74, y + 18), (x + 68, y + 46),
           (x + 40, y + 54), (x + 12, y + 46), (x + 6, y + 18)]
    poly(d, pts, outline=BLUE, width=3)
    line(d, [(x + 24, y + 20), (x + 44, y + 34), (x + 30, y + 44), (x + 58, y + 50)], RED, 3)
    txt(d, x + 86, y + 14, "NCIC BREACH", fp(SANS, 12), RED)
    txt(d, x + 86, y + 32, "FBI crime database", fp(REG, 11), INK)


def draw_quake(d, x, y, w=210, h=56):
    rect(d, (x, y, x + w, y + h), fill=(232, 226, 210))
    poly(d, [(x + 6, y + 48), (x + 42, y + 14), (x + 74, y + 42),
             (x + 110, y + 8), (x + 164, y + 48)], fill=GREY)
    poly(d, [(x + 96, y + 25), (x + 110, y + 8), (x + 126, y + 27),
             (x + 110, y + 20)], fill=WHITE)
    trace = [(x + i * 8, y + 52 + (0 if i not in (6, 7, 8) else -10)) for i in range(20)]
    line(d, trace, RED, 2)
    rrect(d, (x + 6, y + 4, x + 78, y + 20), 2, RED)
    txt(d, x + 10, y + 11, "PERU M6.9", fp(SANS, 11), WHITE)


def draw_tanker(d, x, y, w=210, h=56):
    rect(d, (x, y, x + w, y + h), fill=SEA)
    poly(d, [(x + 16, y + 30), (x + 146, y + 30), (x + 130, y + 46),
             (x + 34, y + 46)], fill=NAVY)
    for cx in (x + 56, x + 88, x + 116):
        rect(d, (cx, y + 18, cx + 12, y + 30), fill=GREY)
    ell(d, (x + 132, y + 4, x + 152, y + 24), fill=RED)
    poly(d, [(x + 142, y - 4), (x + 130, y + 16), (x + 154, y + 16)], fill=RED)
    txt(d, x + 160, y + 16, "HORMUZ", fp(SANS, 12), RED)
    txt(d, x + 160, y + 34, "Brent $92.57", fp(REG, 11), INK)


def draw_mercury(d, x, y, w=210, h=56):
    rect(d, (x, y, x + w, y + h), fill=NAVY)
    for i in range(18):
        sx = x + (i * 41) % w
        sy = y + (i * 23) % h
        ell(d, (sx, sy, sx + 1, sy + 1), fill=WHITE)
    ell(d, (x + 108, y + 6, x + 160, y + 52), fill=(150, 142, 130))
    ell(d, (x + 120, y + 14, x + 130, y + 24), fill=(110, 104, 96))
    ell(d, (x + 136, y + 28, x + 143, y + 35), fill=(110, 104, 96))
    line(d, [(x + 10, y + 40), (x + 92, y + 24)], GOLD, 2)
    poly(d, [(x + 92, y + 24), (x + 84, y + 20), (x + 86, y + 28)], fill=GOLD)
    txt(d, x + 8, y + 6, "BEPICOLOMBO", fp(SANS, 11), GOLD)


def draw_pill(d, x, y, w=210, h=56):
    rect(d, (x, y, x + w, y + h), fill=(238, 224, 226))
    rrect(d, (x + 14, y + 14, x + 80, y + 42), 12, fill=WHITE, outline=RED, width=2)
    line(d, [(x + 47, y + 14), (x + 47, y + 42)], RED, 2)
    txt(d, x + 92, y + 10, "60.7%", fp(SANS, 20), RED)
    txt(d, x + 92, y + 36, "tumours shrink", fp(REG, 11), INK)


def draw_oilrig(d, x, y, w=210, h=56):
    rect(d, (x, y, x + w, y + h), fill=(232, 224, 198))
    for i in range(5):
        line(d, [(x + 20 + i * 12, y + 50), (x + 40 + i * 4, y + 12)], GREY, 2)
        line(d, [(x + 32 + i * 10, y + 50), (x + 24 + i * 2, y + 12)], GREY, 2)
    line(d, [(x + 18, y + 12), (x + 70, y + 12)], INK, 3)
    line(d, [(x + 44, y + 12), (x + 44, y + 2)], INK, 2)
    txt(d, x + 86, y + 12, "TURKANA", fp(SANS, 13), RED)
    txt(d, x + 86, y + 32, "first oil Dec 1", fp(REG, 11), INK)


def draw_flags2(d, x, y, w=210, h=56):
    rect(d, (x, y, x + w, y + h), fill=SOFT)
    rect(d, (x + 12, y + 10, x + 52, y + 44), fill=(0, 90, 40))
    rect(d, (x + 52, y + 10, x + 92, y + 44), fill=WHITE)
    rect(d, (x + 92, y + 10, x + 132, y + 44), fill=RED)
    txt(d, x + 18, y + 20, "★", fp(SANS, 16), GOLD)
    txt(d, x + 140, y + 14, "DECLARATION", fp(SANS, 11), RED)
    txt(d, x + 140, y + 32, "toward Peace", fp(REG, 11), INK)


def draw_strike(d, x, y, w=210, h=56):
    rect(d, (x, y, x + w, y + h), fill=(238, 224, 214))
    for i in range(8):
        cx = x + 18 + (i % 4) * 34
        cy = y + 24 + (i // 4) * 22
        ell(d, (cx - 6, cy - 7, cx - 1, cy - 2), fill=INK)
        ell(d, (cx + 1, cy - 7, cx + 6, cy - 2), fill=INK)
        rect(d, (cx - 6, cy, cx + 6, cy + 10), fill=GREY)
    rrect(d, (x + 6, y + 4, x + 62, y + 20), 2, RED)
    txt(d, x + 10, y + 11, "SCIOPERO", fp(SANS, 11), WHITE)


def draw_boat(d, x, y, w=210, h=56):
    rect(d, (x, y, x + w, y + h), fill=SEA)
    poly(d, [(x + 30, y + 34), (x + 120, y + 34), (x + 108, y + 46),
             (x + 42, y + 46)], fill=(120, 84, 52))
    line(d, [(x + 70, y + 34), (x + 70, y + 6)], GREY, 2)
    line(d, [(x + 70, y + 8), (x + 96, y + 26)], WHITE, 4)
    txt(d, x + 128, y + 16, "SENEGAL", fp(SANS, 12), RED)
    txt(d, x + 128, y + 34, "39 dead", fp(REG, 11), INK)


# ---------- world map ----------

CONTINENTS = [
    [(-168, 65), (-160, 71), (-140, 70), (-125, 72), (-110, 68), (-95, 70),
     (-80, 62), (-60, 58), (-55, 50), (-65, 45), (-70, 42), (-75, 35),
     (-81, 25), (-97, 16), (-105, 20), (-115, 30), (-125, 40), (-130, 55),
     (-150, 60), (-168, 65)],
    [(-81, 8), (-75, 12), (-60, 10), (-50, 4), (-35, -6), (-38, -16),
     (-48, -26), (-55, -35), (-65, -55), (-75, -50), (-73, -40), (-72, -20),
     (-80, -4), (-81, 8)],
    [(-17, 15), (0, 20), (10, 33), (25, 32), (35, 30), (43, 12), (51, 12),
     (42, -2), (40, -15), (35, -25), (25, -34), (18, -35), (12, -18),
     (8, 0), (-8, 5), (-17, 15)],
    [(-10, 36), (0, 44), (10, 45), (20, 40), (28, 41), (30, 50), (40, 55),
     (50, 55), (60, 60), (80, 70), (105, 75), (130, 72), (160, 68),
     (180, 65), (170, 55), (140, 45), (130, 35), (122, 25), (110, 20),
     (100, 10), (105, 0), (95, 5), (90, 20), (80, 8), (72, 20), (65, 25),
     (55, 25), (45, 12), (40, 30), (35, 36), (28, 40), (20, 40), (10, 45),
     (0, 44), (-10, 36)],
    [(115, -22), (130, -12), (142, -12), (153, -25), (150, -38),
     (135, -38), (120, -35), (115, -22)],
    [(-52, 60), (-22, 70), (-20, 82), (-50, 82), (-62, 74), (-52, 60)],
]

PINS = [
    (30.5, 50.5, 1), (84.9, 19.3, 2), (121.5, 25.0, 3), (4.35, 50.85, 4),
    (30.7, 36.9, 5), (114.1, 22.5, 6), (22.5, 50.2, 7), (-77.0, 38.9, 8),
    (-75.3, -11.0, 9), (56.5, 26.5, 10), (35.6, 3.1, 11), (-17.4, 14.7, 12),
    (-58.4, -34.6, 13), (12.5, 41.9, 14), (127.0, 37.5, 15), (106.8, -6.2, 16),
    (139.7, 35.7, 17), (34.5, 31.5, 18), (35.8, 33.9, 19), (44.2, 15.3, 20),
    (32.5, 15.5, 21), (-74.0, 40.7, 22), (72.9, 19.1, 23), (32.6, 0.3, 24),
    (90.4, 23.8, 25), (96.0, 21.0, 26), (-115.1, 36.2, 27), (55.3, 25.3, 28),
]


def world_map(d, x, y, w, h):
    rect(d, (x, y, x + w, y + h), fill=SEA)
    mx, my = 6, 12
    iw, ih = w - 2 * mx, h - 2 * my

    def proj(lon, lat):
        return (x + mx + (lon + 180) / 360 * iw,
                y + my + (90 - lat) / 180 * ih)

    for c in CONTINENTS:
        poly(d, [proj(lo, la) for lo, la in c], fill=LAND, outline=(120, 105, 75), width=1)
    for lo, la, n in PINS:
        px, py = proj(lo, la)
        ell(d, (px - 5, py - 5, px + 5, py + 5), fill=RED, outline=WHITE, width=1)
        txt(d, px, py - 0.5, str(n), fp(SANS, 7), WHITE, "mm")
    txt(d, x + 8, y + 5, "WHERE IT HAPPENED", fp(SANS, 11), INK)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # frame and header
    rect(d, (8, 8, 1016, 1016), outline=INK, width=2)
    txt(d, 24, 18, "THE WORLD IN ONE DAY", fp(SANS, 11), RED)
    txt(d, 1000, 18, "ONE PAGE  ·  38 STORIES  ·  7 REGIONS  ·  FRIDAY 20 NOVEMBER 2026",
        fp(SANS, 10), INK, "ra")
    line(d, [(24, 34), (1000, 34)], INK, 1)
    txt(d, 512, 42, "Friday 20 November 2026", fp(SERIF, 63), INK, "mt")
    txt(d, 512, 110,
        "Russian missiles hit Kyiv's bridges · Cyclone Akvan strikes India · "
        "Asia's AI sell-off · UK and EU seal a deal",
        fp(SERIF_I, 16), RED, "mt")
    line(d, [(24, 140), (1000, 140)], RED, 2)

    # the day in numbers
    stats = [("111", "missiles fired at Ukraine", RED),
             ("3", "Kyiv bridges hit", RED),
             ("372,000+", "evacuated before Akvan", TEAL),
             ("-6.2%", "Taiex at Friday's close", BLUE),
             ("2.3%", "Japan CPI, October", GOLD),
             ("118", "Phillips v India", GREY)]
    sx = 24
    for value, label, col in stats:
        w = 158
        txt(d, sx + 6, 148, value, fp(SANS, 24), col)
        txt(d, sx + 6, 174, label, fp(REG, 10), INK)
        line(d, [(sx + w - 8, 146), (sx + w - 8, 184)], GREY, 1)
        sx += w
    line(d, [(24, 190), (1000, 190)], INK, 1)

    # region tabs
    tabs = [("EUROPE 8", RED), ("ASIA-PACIFIC 13", GOLD), ("MIDDLE EAST 3", TEAL),
            ("AFRICA 3", GREY), ("AMERICAS 5", BLUE), ("OCEANIA 2", (120, 90, 140)),
            ("WORLD / SPACE 4", NAVY)]
    tx = 24
    for name, col in tabs:
        width = 139
        rect(d, (tx, 194, tx + width, 210), fill=col)
        txt(d, tx + width / 2, 202, name, fp(SANS, 10), WHITE, "mm")
        tx += width + 1

    # three feature panels
    feats = [(24, 216, draw_river_bridges, "01  KYIV, UKRAINE · WAR",
              "Russian missile barrage kills three, hits Kyiv's bridges",
              "111 missiles and 404 drones in the overnight attack; three bridges")
             , (352, 216, draw_cyclone, "02  ODISHA, INDIA · CYCLONE",
                "Cyclone Akvan makes landfall near Gopalpur",
                "300,000+ moved to shelters; winds near 90 km/h; no major damage")
             , (680, 216, draw_market, "03  TAIPEI · SEOUL · TOKYO · MARKETS",
                "AI sell-off sinks Asia's stock markets",
                "Taiex -6.2%, Kospi -5.2%, Nikkei -5.1%; worst week since 1991")]
    for x, y, artist, kicker, head, body in feats:
        rrect(d, (x, y, x + 320, y + 252), 6, fill=WHITE, outline=INK, width=1)
        artist(d, x + 8, y + 8, 304, 122)
        txt(d, x + 10, y + 138, kicker, fp(SANS, 10), RED)
        hf, bf = fp(SERIF, 17), fp(REG, 10)
        lines = wrap(d, head, hf, 300, 2)
        ty = y + 154
        for ln in lines:
            txt(d, x + 10, ty, ln, hf, INK)
            ty += 20
        for j, ln in enumerate(wrap(d, body, bf, 300, 2)):
            txt(d, x + 10, ty + 2 + j * 12, ln, bf, GREY)

    # story cards, 4 columns x 3 rows
    cards = [
        (draw_flags, "04  BRUSSELS · DIPLOMACY", "UK and EU seal a 'reset' deal", "Food checks, carbon link and 100,000 youth visas each way. (Reuters)"),
        (draw_globe_thermo, "05  ANTALYA · CLIMATE", "COP31 reaches its final day with no deal", "Draft omits fossil fuels; $120bn adaptation finance unresolved. (UN News)"),
        (draw_missile_field, "06  LUBLIN · SECURITY", "Russian missile lands in Poland", "A Kh-101 fell near Nowy Lipowiec; no one hurt, Warsaw says. (BBC)"),
        (draw_flags2, "07  SHENZHEN · DIPLOMACY", "Three leaders issue 'Declaration toward Peace'", "Trump, Xi and Putin pledge dialogue on nuclear risk and UN reform. (BBC)"),
        (draw_shield, "08  WASHINGTON · CYBER", "FBI crime database breached again", "Intrusion hits the NCIC used by police across the United States. (CNN)"),
        (draw_quake, "09  JUNIN · PERU", "Magnitude 6.9 quake shakes the Andes", "Epicentre 34 km north of Junin; no major damage reported. (USGS)"),
        (draw_tanker, "10  HORMUZ · ENERGY", "Tanker attacks keep Brent near $92", "Oil edges up as Iran's tanker attacks continue; Gulf flows recover. (Reuters)"),
        (draw_mercury, "11  MERCURY · SPACE", "BepiColombo reaches Mercury", "Eight-year, 10bn-km trip; second spacecraft ever to orbit the planet. (ESA)"),
        (draw_pill, "12  BARCELONA · HEALTH", "Pancreatic cancer pill shrinks tumours", "Daraxonrasib: tumours shrink or vanish in 60.7% of 61 patients. (Guardian)"),
        (draw_oilrig, "13  TURKANA · KENYA", "Kenya starts drilling its first oil well", "Amosing 1 in South Lokichar; first oil targeted for 1 December. (Nation)"),
        (draw_strike, "14  ROME · LABOUR", "Italy's CGIL holds a 24-hour general strike", "Workers and students march in more than 100 cities over wages. (Reuters)"),
        (draw_boat, "15  DAKAR · MIGRATION", "Migrant boat capsizes off Senegal", "At least 39 dead en route to Spain's Canary Islands; one rescued. (APS)"),
    ]
    cw, ch = 236, 70
    for i, (artist, kicker, head, body) in enumerate(cards):
        col, row = i % 4, i // 4
        x, y = 24 + col * (cw + 4), 476 + row * (ch + 4)
        rect(d, (x, y, x + cw, y + ch), fill=WHITE, outline=(160, 155, 145), width=1)
        card_icon(d, i, x + 4, y + 4)
        kf, hf, bf = fp(SANS, 8), fp(SERIF, 12), fp(REG, 9)
        tx = x + 88
        txt(d, tx, y + 4, kicker, kf, RED)
        ty = y + 15
        for ln in wrap(d, head, hf, 144, 2):
            txt(d, tx, ty, ln, hf, INK)
            ty += 13
        for ln in wrap(d, body, bf, 144, 2):
            txt(d, tx, ty + 1, ln, bf, GREY)
            ty += 11

    # map and 'also on friday'
    world_map(d, 24, 704, 336, 224)
    txt(d, 372, 704, "ALSO ON FRIDAY 20 NOVEMBER — 23 MORE STORIES", fp(SANS, 11), RED)
    also = [
        "16 Kyiv: rail station strike kills 2",
        "17 Estonia: Russia closes Narva link",
        "18 UK: pupils strike over military service",
        "19 China holds loan rates 18th month",
        "20 Gaza: 6 killed despite truce, medics say",
        "21 Lebanon's cabinet wins confidence vote",
        "22 Houthi missile intercepted, Sanaa",
        "23 Japan inflation cools to 2.2%",
        "24 Seoul: push to impeach chief justice",
        "25 Indonesia passes asset-forfeiture bill",
        "26 Uganda enforces Ebola quarantine",
        "27 Bangladesh: 124 held after arson",
        "28 Myanmar rejects World Court ruling",
        "29 Australia: AFL final crowd 100,024",
        "30 Nvidia falls 11% as probe widens",
        "31 Florida storm drops 250 mm of rain",
        "32 Houthi strike on Riyadh rattles oil",
        "33 Hong Kong extradition debate returns",
        "34 Russell fastest in Las Vegas F1 practice",
        "35 Turin: students join strike march",
        "36 Phillips 118 v India in 3rd Test",
        "37 GTA VI: $2.36bn pre-orders record",
        "38 BepiColombo orbit insertion Saturday",
    ]
    af = fp(REG, 9)
    for i, s in enumerate(also):
        col, row = i // 8, i % 8
        txt(d, 372 + col * 213, 722 + row * 24, s, af, INK)

    # date check
    rect(d, (24, 936, 1000, 1008), fill=WHITE, outline=RED, width=2)
    txt(d, 34, 942, "DATE CHECK", fp(SANS, 11), RED)
    df = fp(REG, 9)
    dtxt = ("Left out on purpose, first reported before Friday: the Shenzhen summit itself (19 Nov), "
            "Anthropic's $83 IPO (19 Nov), the ICJ Rohingya ruling and its 19 Nov order on Myanmar. "
            "Every story here happened, or was first reported, on Friday 20 November 2026 in any time "
            "zone. Claims are attributed; forecasts flagged.")
    for j, ln in enumerate(wrap(d, dtxt, df, 950, 3)):
        txt(d, 34, 956 + j * 13, ln, df, INK)
    txt(d, 34, 996,
        "Sources: Reuters, AP, BBC, AFP, Al Jazeera, Guardian, IMD, USGS, ESA, Kyiv Independent, "
        "Nation (Kenya), APS, IMD. Original vector drawings.", fp(REG, 8), GREY)

    out = img.resize((1024, 1024), Image.LANCZOS)
    out.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
