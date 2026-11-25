#!/usr/bin/env python3
"""THE MARKET BELL — News Image 20261125, Akun 12.
Tuesday 25 November 2026 rung in like a trading day: old gold and
bottle green on cream. The page leads with the markets (Nvidia's
Monday, the PCE report that had not landed, the Hormuz claim priced
as a claim) and still carries the whole day — 37 dated stories.
Two layouts are rendered and duelled; the winner becomes entry.png.
PIL draws locally; the submitted main.py is copy-only stdlib.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/home/hatch/workspace/tools/bedah-19nov/news-image/fonts/"
W = H = 1024
MX = 26

CREAM = (244, 238, 222)
CREAM_D = (235, 226, 198)
INK = (30, 32, 26)
MUTE = (102, 96, 78)
GOLD = (146, 110, 38)
GOLD_L = (196, 160, 84)
GREEN = (26, 62, 44)
GREEN_L = (44, 92, 62)
RED = (158, 44, 32)
SKY = (206, 214, 210)
SEA = (70, 102, 96)
SAND = (216, 200, 156)
WHITE = (250, 248, 238)


def F(size, bold=False, disp=False, italic=False):
    if disp:
        name = "PlayfairDisplay-Black.ttf"
    elif italic:
        name = "PlayfairDisplay-Italic.ttf"
    elif bold:
        name = "Archivo-Bold.ttf"
    else:
        name = "Archivo.ttf"
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def T(d, xy, s, font, fill=INK, anchor=None):
    d.text(xy, s, font=font, fill=fill, anchor=anchor)


def wrap(d, s, font, maxw):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- pool
# num, region tag, headline, deck, source, tag, chip
CARDS = {
    36: ("36 · WORLD — NVIDIA", "Nvidia's $1 trillion Monday",
         "Monday close: Nvidia shares +31.5%, nearly $1 trillion of "
         "market value clawed back as Jensen Huang returned as CEO, "
         "+$34 billion in a day (Forbes).", "Forbes via wires",
         "REPORTED", "+31.5% MONDAY CLOSE"),
    33: ("33 · WORLD — WASHINGTON", "PCE inflation report due today",
         "The US PCE report is due Tuesday 25 November; markets "
         "watch for the Fed's next signal. No figure had landed "
         "when this page closed.", "scheduled",
         "SCHEDULED", "PCE DUE TODAY"),
    2: ("2 · MIDDLE EAST — STRAIT OF HORMUZ", "Iran says 3 tankers hit by mines",
        "The IRGC Navy claims three oil tankers were hit by naval "
        "mines in the Strait of Hormuz; shipping concerns rise.", "Iranian claim via wires",
        "CLAIMED", "3 TANKERS HIT — IRAN SAYS"),
    1: ("1 · EUROPE — POLAND", "NATO sends early-warning jets to Poland",
        "AWACS to Poland after Russian missiles landed there "
        "during an attack on Ukraine; Merz vows complete support.", "wire reports", "REPORTED",
        "AWACS TO POLAND"),
    3: ("3 · MIDDLE EAST — IRAQ", "Baghdad orders Kurdish oilfields seized",
        "Baghdad's PM orders federal units to seize Kurdish "
        "oilfields and border crossings.", "Starlit / wires", "REPORTED", "OILFIELDS ORDER"),
    6: ("6 · WORLD — UKRAINE", "700,000 Russian dead, new count finds",
        "New analysis counts 700,000+ Russian soldiers killed "
        "in the nearly five-year war on Ukraine.", "RFE/RL",
        "REPORTED", "700,000+ KILLED"),
    4: ("4 · MIDDLE EAST — GAZA", "Drone strikes kill Hamas security chief",
        "Strikes killed 7 in Gaza: a Hamas security chief, "
        "three policemen and three siblings, one a child.", "Al Jazeera", "REPORTED",
        "7 KILLED IN STRIKES"),
    10: ("10 · ASIA — CHINA", "Xiamen Airlines orders 50 Boeing jets",
         "Xiamen Airlines, a China Southern unit, agreed to "
         "acquire 50 Boeing 737-8 jets.", "wire reports", "REPORTED",
         "50 JETS ORDERED"),
    11: ("11 · EUROPE — MADRID", "Madrid rout PSV 5-1 in comeback",
         "Madrid came from behind: 5-1 over PSV, a Bellingham "
         "stunner and an Mbappé brace.",
         "wire reports", "REPORTED", "MADRID 5-1 PSV"),
    13: ("13 · OCEANIA — AUSTRALIA", "12 coral species brought back",
         "Great Barrier Reef genetic analysis resurrects 12 "
         "Acropora coral species; reef diversity wider than known.",
         "science wires", "REPORTED", "12 SPECIES BACK"),
    37: ("37 · AMERICAS — USA", "Storms target Thanksgiving travel",
         "Storm weather on both US coasts threatens Thanksgiving "
         "travel for millions.", "wire reports",
         "REPORTED", "STORMS BOTH COASTS"),
    26: ("26 · ASIA-PACIFIC — SOLOMONS", "Solomons eye Australia treaty switch",
         "Solomon Islands plans to replace its China defence "
         "treaty with an Australia treaty, according to reports.",
         "wire reports", "REPORTED", "TREATY SWITCH"),
    5: ("5 · EUROPE — BRUSSELS", "EU unveils new Russia sanctions",
        "The EU announced new restrictive measures against "
        "Russia amid the war in Ukraine.",
        "wire roundups", "REPORTED", "NEW EU SANCTIONS"),
}
LEADS = [36, 33, 2]
GRID = [1, 3, 6, 4, 10, 11, 13, 37, 26, 5]

BRIEFS = [
    (7, "First 5 Lynx KF41 IFVs enter Ukrainian service"),
    (8, "Colombia car bomb injures at least 23"),
    (9, "Gunmen hold dozens in a Cartagena supermarket"),
    (12, "England level T20 series, chasing 185"),
    (14, "Fiji declares disaster in El Niño dry spell"),
    (15, "Iran pharmacies run dry in medicine shortage"),
    (16, "Iran braces for winter gas shortages"),
    (17, "Britain sanctions the Houthis' top leaders"),
    (18, "Senegal AFCON title restored by CAS ruling"),
    (19, "Rebels pull back in DR Congo after clashes"),
    (20, "Nigerian emir suspended after allegation"),
    (21, "Sudan RSF commander defects"),
    (22, "Cameroon separatist in Norway court"),
    (23, "Punjab: BJP and Akali Dal reunite as allies"),
    (24, "Bangladesh opens Guangzhou investment office"),
    (25, "Indonesia's vice-president resigns"),
    (27, "North Korea touts China ties in Pyongyang"),
    (28, "Denmark court upholds ghetto evictions law"),
    (29, "Sarkozy headed for Libya-case trial"),
    (30, "Black Sea clash at the UN"),
    (31, "Shortwave school for Afghan girls"),
    (32, "Dimorphos casts its shadow on Didymos"),
    (34, "US targets 7 firms over chip diversion"),
    (35, "Moscow buys inflatable decoys from China"),
]

TICKER = [
    ("NVDA +31.5%", "MONDAY CLOSE"),
    ("$1 TRILLION", "VALUE CLAWED BACK"),
    ("PCE", "DUE TODAY — NO FIGURE YET"),
    ("3 TANKERS", "HORMUZ — IRAN SAYS"),
    ("700,000+", "RUSSIAN DEAD — NEW COUNT"),
    ("50 JETS", "XIAMEN ORDERS BOEING"),
    ("5–1", "MADRID OVER PSV"),
    ("12", "CORAL SPECIES BACK"),
]
REGIONS = [("EUROPE", 8), ("MIDDLE EAST", 6), ("WORLD", 6), ("AFRICA", 5),
           ("AMERICAS", 4), ("ASIA", 2), ("SOUTH ASIA", 2),
           ("ASIA-PACIFIC", 2), ("OCEANIA", 2)]
TIMELINE = [
    ("MON CLOSE", "Nvidia +31.5% — Monday close, Forbes"),
    ("EARLY", "NATO AWACS plan for Poland reported"),
    ("MORNING", "Iran says 3 tankers mined at Hormuz"),
    ("MIDDAY", "Baghdad oilfield order reaches Kurdistan"),
    ("TODAY", "US PCE report due — no figure yet"),
    ("TONIGHT", "Storms target Thanksgiving travel"),
]
DATECHECK = [
    "GTA VI launch hype — a game date, not today's news",
    "COP31 talks — earlier this month, not Tuesday",
    "Liverpool 4–0 — a weekend score, not 25 November",
    "Mercury stories filed 23 Nov — two days old, excluded",
    "Black Friday sales — Friday's story, not Tuesday's",
]


# ---------------------------------------------------------------- scenes
def _sky(d, x, y, w, h, top, bot):
    steps = 20
    for i in range(steps):
        t = i / steps
        c = tuple(int(top[k] + (bot[k] - top[k]) * t) for k in range(3))
        d.rectangle([x, y + h * i // steps, x + w, y + h * (i + 1) // steps + 1], fill=c)


def sc_chip_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 48, 36))
    cw, ch = w * 0.30, h * 0.50
    cx, cy = x + w * 0.08, y + (h - ch) / 2
    d.rectangle([cx, cy, cx + cw, cy + ch], fill=(40, 76, 52), outline=GOLD_L, width=2)
    for i in range(4):
        px = cx + cw * (0.16 + i * 0.22)
        d.line([px, cy - 7, px, cy], fill=GOLD_L, width=3)
        d.line([px, cy + ch, px, cy + ch + 7], fill=GOLD_L, width=3)
    pts = [(0.46, 0.80), (0.58, 0.64), (0.70, 0.70), (0.82, 0.40), (0.94, 0.18)]
    d.line([(x + px * w, y + py * h) for px, py in pts], fill=(240, 170, 90), width=3)
    for px, py in pts:
        d.ellipse([x + px * w - 3, y + py * h - 3, x + px * w + 3, y + py * h + 3], fill=(250, 220, 160))
    T(d, (x + w * 0.94, y + h * 0.10), "+31.5%", F(15, True), (250, 220, 160), anchor="ra")


def sc_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 234, 214))
    for i in range(4):
        gy = y + h * (0.2 + i * 0.2)
        d.line([x + 8, gy, x + w - 8, gy], fill=(206, 196, 168), width=1)
    pts = [(0.08, 0.60), (0.26, 0.54), (0.44, 0.58), (0.60, 0.46), (0.74, 0.50)]
    d.line([(x + px * w, y + py * h) for px, py in pts], fill=GREEN, width=3)
    ex, ey = x + w * 0.90, y + h * 0.38
    d.ellipse([ex - 13, ey - 13, ex + 13, ey + 13], outline=RED, width=3)
    T(d, (ex, ey - 1), "?", F(17, True), RED, anchor="mm")
    d.line([x + w * 0.74, y + h * 0.50, ex - 8, ey + 6], fill=RED, width=2)


def sc_tanker(d, x, y, w, h):
    _sky(d, x, y, w, h, (168, 178, 168), (128, 148, 138))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=SEA)
    for sx in (0.16, 0.52, 0.84):
        bx, by = x + w * sx, y + h * 0.60
        d.polygon([(bx - 16, by), (bx + 16, by), (bx + 9, by + 9), (bx - 9, by + 9)], fill=INK)
        d.rectangle([bx - 11, by - 7, bx + 11, by], fill=(122, 32, 24))
    mx, my = x + w * 0.34, y + h * 0.80
    d.polygon([(mx, my - 12), (mx + 4, my - 2), (mx + 11, my + 2), (mx + 4, my + 5),
               (mx, my + 12), (mx - 4, my + 5), (mx - 11, my + 2), (mx - 4, my - 2)], fill=INK)


def sc_awacs(d, x, y, w, h):
    _sky(d, x, y, w, h, (176, 190, 188), (228, 230, 216))
    cy = y + h * 0.52
    d.ellipse([x + w * 0.34, cy - h * 0.30, x + w * 0.66, cy + h * 0.26], outline=GREEN, width=3)
    d.ellipse([x + w * 0.42, cy - h * 0.18, x + w * 0.58, cy + h * 0.14], outline=GREEN_L, width=2)
    d.polygon([(x + w * 0.20, cy), (x + w * 0.62, cy - h * 0.05), (x + w * 0.78, cy),
               (x + w * 0.62, cy + h * 0.05)], fill=INK)
    d.polygon([(x + w * 0.22, cy - h * 0.02), (x + w * 0.13, cy - h * 0.18),
               (x + w * 0.26, cy - h * 0.14)], fill=GOLD)
    d.rectangle([x + w * 0.45, cy - h * 0.14, x + w * 0.53, cy - h * 0.07], fill=INK)


def sc_oilfield(d, x, y, w, h):
    _sky(d, x, y, w, h, (228, 208, 164), (242, 230, 192))
    d.rectangle([x, y + h * 0.78, x + w, y + h], fill=SAND)
    for fx in (0.24, 0.62):
        bx, by = x + w * fx, y + h * 0.78
        d.line([bx - 20, by, bx, by - h * 0.52], fill=INK, width=3)
        d.line([bx + 20, by, bx, by - h * 0.52], fill=INK, width=3)
        d.line([bx - 15, by - h * 0.18, bx + 15, by - h * 0.18], fill=INK, width=2)
        d.line([bx, by - h * 0.52, bx + 26, by - h * 0.40], fill=INK, width=3)
        d.polygon([(bx + 26, by - h * 0.40), (bx + 34, by - h * 0.30), (bx + 22, by - h * 0.30)], fill=RED)
    d.ellipse([x + w * 0.86, y + h * 0.10, x + w * 0.97, y + h * 0.28], fill=GOLD_L)


def sc_field(d, x, y, w, h):
    import random
    _sky(d, x, y, w, h, (78, 78, 84), (130, 118, 104))
    d.rectangle([x, y + h * 0.60, x + w, y + h], fill=(98, 88, 66))
    rng = random.Random(12)
    for _ in range(46):
        cx = x + rng.uniform(0.03, 0.97) * w
        cy = y + rng.uniform(0.64, 0.94) * h
        s = rng.uniform(3, 6)
        d.line([cx - s, cy, cx + s, cy], fill=CREAM, width=2)
        d.line([cx, cy - s, cx, cy + s], fill=CREAM, width=2)


def sc_drone(d, x, y, w, h):
    _sky(d, x, y, w, h, (98, 94, 96), (170, 150, 128))
    base = y + h * 0.86
    for i, bh in enumerate((0.30, 0.44, 0.24, 0.52, 0.36, 0.28)):
        bx = x + w * (0.04 + i * 0.155)
        d.rectangle([bx, base - h * bh, bx + w * 0.11, base], fill=(54, 50, 48))
        d.rectangle([bx + 3, base - h * bh + 4, bx + 7, base - h * bh + 8], fill=GOLD_L)
    d.rectangle([x, base, x + w, y + h], fill=(72, 62, 52))
    qx, qy = x + w * 0.60, y + h * 0.20
    d.rectangle([qx - 16, qy - 3, qx + 16, qy + 3], fill=INK)
    for dx in (-20, 20):
        d.ellipse([qx + dx - 6, qy - 8, qx + dx + 6, qy - 3], outline=INK, width=2)


def sc_jet(d, x, y, w, h):
    _sky(d, x, y, w, h, (162, 184, 198), (230, 232, 222))
    cy = y + h * 0.46
    d.polygon([(x + w * 0.10, cy), (x + w * 0.78, cy - h * 0.05), (x + w * 0.92, cy),
               (x + w * 0.78, cy + h * 0.07), (x + w * 0.16, cy + h * 0.05)], fill=(238, 238, 240), outline=INK)
    d.polygon([(x + w * 0.14, cy - h * 0.02), (x + w * 0.06, cy - h * 0.20),
               (x + w * 0.20, cy - h * 0.17)], fill=GREEN)
    d.polygon([(x + w * 0.44, cy + h * 0.03), (x + w * 0.34, cy + h * 0.20),
               (x + w * 0.52, cy + h * 0.16)], fill=(202, 206, 208), outline=INK)
    for i in range(9):
        wx = x + w * (0.30 + i * 0.055)
        d.ellipse([wx, cy - h * 0.015, wx + 5, cy + h * 0.02], fill=(90, 120, 150))


def sc_stadium(d, x, y, w, h):
    _sky(d, x, y, w, h, (46, 54, 74), (86, 98, 110))
    d.rectangle([x, y + h * 0.58, x + w, y + h], fill=(80, 98, 58))
    d.ellipse([x + w * 0.30, y + h * 0.62, x + w * 0.70, y + h * 0.94], outline=CREAM, width=2)
    d.line([x + w * 0.5, y + h * 0.60, x + w * 0.5, y + h * 0.96], fill=CREAM, width=1)
    for fx in (0.10, 0.90):
        px = x + w * fx
        d.line([px, y + h * 0.52, px, y + h * 0.16], fill=INK, width=3)
        d.ellipse([px - 9, y + h * 0.08, px + 9, y + h * 0.17], fill=(250, 240, 200))
    T(d, (x + w * 0.5, y + h * 0.30), "5–1", F(26, True), CREAM, anchor="mm")


def sc_coral(d, x, y, w, h):
    import math
    d.rectangle([x, y, x + w, y + h], fill=(54, 98, 110))
    d.rectangle([x, y + h * 0.80, x + w, y + h], fill=(198, 184, 140))

    def branch(bx, by, ang, ln, wd, col, depth):
        ex, ey = bx + ln * math.cos(ang), by - ln * math.sin(ang)
        d.line([bx, by, ex, ey], fill=col, width=max(1, wd))
        if depth <= 0 or ln < 5:
            d.ellipse([ex - 2, ey - 2, ex + 2, ey + 2], fill=(240, 170, 150))
            return
        branch(ex, ey, ang + 0.42, ln * 0.72, wd - 1, col, depth - 1)
        branch(ex, ey, ang - 0.38, ln * 0.72, wd - 1, col, depth - 1)

    branch(x + w * 0.30, y + h * 0.86, 1.35, h * 0.30, 5, (226, 120, 96), 4)
    branch(x + w * 0.62, y + h * 0.88, 1.65, h * 0.36, 5, (240, 160, 110), 4)
    branch(x + w * 0.84, y + h * 0.84, 1.45, h * 0.24, 4, (226, 120, 96), 3)


def sc_storm(d, x, y, w, h):
    _sky(d, x, y, w, h, (88, 96, 104), (142, 150, 150))
    d.rectangle([x, y + h * 0.68, x + w, y + h], fill=(72, 94, 100))
    for i in range(3):
        wy = y + h * (0.74 + i * 0.09)
        d.arc([x + w * (0.06 + i * 0.22), wy, x + w * (0.30 + i * 0.22), wy + h * 0.08], 180, 360, fill=CREAM, width=2)
    cx, cy = x + w * 0.72, y + h * 0.30
    for r in (26, 17, 9):
        d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=CREAM, width=3)
    for lx in (0.16, 0.34):
        px = x + w * lx
        d.line([px, y + h * 0.06, px - 5, y + h * 0.20], fill=GOLD_L, width=2)
        d.line([px - 5, y + h * 0.20, px + 3, y + h * 0.20], fill=GOLD_L, width=2)
        d.line([px + 3, y + h * 0.20, px - 3, y + h * 0.34], fill=GOLD_L, width=2)


def sc_islands(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(88, 130, 138))
    d.ellipse([x + w * 0.10, y + h * 0.30, x + w * 0.46, y + h * 0.62], fill=SAND, outline=INK)
    d.ellipse([x + w * 0.56, y + h * 0.44, x + w * 0.90, y + h * 0.72], fill=SAND, outline=INK)
    for px, py in ((0.26, 0.40), (0.72, 0.54)):
        bx, by = x + w * px, y + h * py
        d.line([bx, by + 8, bx, by - 8], fill=(70, 84, 50), width=3)
        d.polygon([(bx, by - 8), (bx - 9, by - 2), (bx + 9, by - 2)], fill=(70, 84, 50))
    sx, sy = x + w * 0.50, y + h * 0.20
    d.rectangle([sx - 16, sy - 10, sx + 16, sy + 10], fill=(242, 236, 216), outline=INK)
    d.line([sx - 16, sy - 10, sx + 16, sy + 10], fill=RED, width=1)
    d.line([sx + 16, sy - 10, sx - 16, sy + 10], fill=RED, width=1)


def sc_dome(d, x, y, w, h):
    import math
    _sky(d, x, y, w, h, (174, 186, 196), (226, 228, 214))
    cx, base = x + w / 2, y + h * 0.88
    d.pieslice([cx - w * 0.30, base - h * 0.72, cx + w * 0.30, base + h * 0.20], 180, 360, fill=(198, 200, 200), outline=INK, width=2)
    d.rectangle([cx - w * 0.34, base, cx + w * 0.34, base + 3], fill=INK)
    for i in range(6):
        a = math.pi * (0.12 + i * 0.15)
        sx = cx + w * 0.21 * math.cos(a)
        sy = base - h * 0.40 * math.sin(a)
        d.ellipse([sx - 4, sy - 4, sx + 4, sy + 4], fill=GOLD_L, outline=INK)


SCENES = {36: sc_chip_chart, 33: sc_chart, 2: sc_tanker, 1: sc_awacs,
          3: sc_oilfield, 6: sc_field, 4: sc_drone, 10: sc_jet,
          11: sc_stadium, 13: sc_coral, 37: sc_storm, 26: sc_islands,
          5: sc_dome}

MAP = [
    "..........####..........######..####........................................",
    "......##########......##############......##..####..........................",
    ".....###########.....################....##########.........................",
    "......########......#################...############..##....................",
    ".......######........###############.....##########.........................",
    "........####..........#############........######......#....................",
    ".........##............###########..........####............................",
    ".........##.............########............###..........##.................",
    "........###..............######.............##..........####................",
    "........####..............####.........................######...............",
    "........#####..............###........................########..............",
    ".........####...............#........................#########..............",
    ".........###........................................##########.......##.....",
    ".........##..........................................########.......####....",
    "..........#...........................................######.........##.....",
    ".......................................................####...................",
    ".......................................................##..........##.........",
    "..................................................................####........",
    "...................................................................##.........",
]


def draw_map(d, x, y, w, h, pins):
    rows, cols = len(MAP), len(MAP[0])
    cw, ch = w / cols, h / rows
    for r, row in enumerate(MAP):
        for c, cell in enumerate(row):
            if cell == "#":
                cx, cy = x + c * cw, y + r * ch
                d.ellipse([cx, cy, cx + cw * 0.72, cy + ch * 0.72], fill=(168, 150, 104))
    for num, fx, fy in pins:
        cx, cy = x + fx * w, y + fy * h
        d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=GREEN, outline=CREAM, width=2)
        T(d, (cx, cy - 1), str(num), F(9, True), CREAM, anchor="mm")


PINS = [(36, 0.075, 0.22), (33, 0.10, 0.24), (2, 0.565, 0.30), (1, 0.485, 0.16),
        (3, 0.575, 0.27), (6, 0.53, 0.15), (4, 0.565, 0.26), (10, 0.76, 0.28),
        (11, 0.465, 0.20), (13, 0.885, 0.78), (37, 0.11, 0.20),
        (26, 0.90, 0.62), (5, 0.475, 0.14)]


# ---------------------------------------------------------------- cards
def draw_card(d, num, x, y, w, h, lead=False):
    region, head, deck, source, tag, chip = CARDS[num]
    d.rectangle([x, y, x + w, y + h], fill=WHITE, outline=INK, width=1)
    d.rectangle([x, y, x + w, y + 15], fill=GREEN if lead else INK)
    T(d, (x + 5, y + 3), region, F(8, True), CREAM)
    T(d, (x + w - 5, y + 3), tag, F(8, True), (240, 210, 140), anchor="ra")
    scene_h = int(h * (0.40 if lead else 0.34))
    SCENES[num](d, x + 3, y + 18, w - 6, scene_h)
    ty = y + 22 + scene_h
    hf = F(19, disp=True) if lead else F(12, True)
    for line in wrap(d, head, hf, w - 12):
        if ty + 14 > y + h - 18:
            break
        T(d, (x + 6, ty), line, hf, INK)
        ty += (23 if lead else 15)
    df = F(11) if lead else F(9)
    for line in wrap(d, deck, df, w - 12):
        if ty + (13 if lead else 11) > y + h - 18:
            break
        T(d, (x + 6, ty), line, df, (54, 52, 44))
        ty += (14 if lead else 11)
    d.rectangle([x, y + h - 16, x + w, y + h], fill=CREAM_D, outline=INK)
    T(d, (x + 5, y + h - 12), chip, F(8, True), GREEN)
    T(d, (x + w - 5, y + h - 12), source, F(7), MUTE, anchor="ra")


def draw_wide_lead(d, num, x, y, w, h):
    region, head, deck, source, tag, chip = CARDS[num]
    d.rectangle([x, y, x + w, y + h], fill=WHITE, outline=INK, width=1)
    d.rectangle([x, y, x + w, y + 15], fill=GREEN)
    T(d, (x + 5, y + 3), region, F(8, True), CREAM)
    T(d, (x + w - 5, y + 3), tag, F(8, True), (240, 210, 140), anchor="ra")
    sw = int(w * 0.44)
    SCENES[num](d, x + 3, y + 18, sw - 6, h - 36)
    tx = x + sw + 8
    ty = y + 26
    hf = F(23, disp=True)
    for line in wrap(d, head, hf, w - sw - 20):
        T(d, (tx, ty), line, hf, INK)
        ty += 27
    ty += 2
    for line in wrap(d, deck, F(12), w - sw - 20):
        if ty + 15 > y + h - 20:
            break
        T(d, (tx, ty), line, F(12), (54, 52, 44))
        ty += 16
    d.rectangle([x + sw, y + h - 16, x + w, y + h], fill=CREAM_D, outline=INK)
    T(d, (x + sw + 5, y + h - 12), chip, F(8, True), GREEN)
    T(d, (x + w - 5, y + h - 12), source, F(7), MUTE, anchor="ra")


def bell(d, cx, cy, s, col):
    d.pieslice([cx - s, cy - s, cx + s, cy + s], 180, 360, fill=col)
    d.polygon([(cx - s, cy), (cx + s, cy), (cx + s * 1.15, cy + s * 0.55),
               (cx - s * 1.15, cy + s * 0.55)], fill=col)
    d.ellipse([cx - s * 0.22, cy + s * 0.55, cx + s * 0.22, cy + s * 0.95], fill=col)
    d.rectangle([cx - 2, cy - s - 4, cx + 2, cy - s + 2], fill=col)


def ticker_band(d, y):
    d.rectangle([MX, y, W - MX, y + 42], fill=GREEN)
    cw = (W - 2 * MX) / 8
    for i, (big, lab) in enumerate(TICKER):
        x = MX + i * cw
        if i:
            d.line([x, y + 5, x, y + 37], fill=GREEN_L, width=1)
        T(d, (x + cw / 2, y + 5), big, F(14, True), (246, 214, 140), anchor="ma")
        for j, line in enumerate(wrap(d, lab, F(7, True), cw - 6)):
            T(d, (x + cw / 2, y + 25 + j * 8), line, F(7, True), CREAM, anchor="ma")
    return y + 48


def ticker_line(d, y):
    d.rectangle([MX, y, W - MX, y + 20], fill=GOLD_L)
    items = "  ◆  ".join(f"{b} {l}" for b, l in TICKER)
    T(d, (W / 2, y + 4), items, F(10, True), (40, 34, 16), anchor="ma")
    return y + 26


def region_strip(d, y):
    x = MX
    T(d, (x, y + 2), "REGIONS:", F(10, True), INK)
    x += d.textlength("REGIONS: ", font=F(10, True))
    fills = [(44, 92, 62), (146, 110, 38), (26, 62, 44), (176, 141, 62),
             (84, 110, 116), (122, 32, 24), (104, 88, 120), (70, 120, 130),
             (150, 120, 70)]
    for i, (name, n) in enumerate(REGIONS):
        label = f"{name} {n}"
        tw = d.textlength(label, font=F(9, True)) + 12
        d.rectangle([x, y, x + tw, y + 16], fill=fills[i % len(fills)])
        T(d, (x + 6, y + 3), label, F(9, True), CREAM)
        x += tw + 5
    return y + 22


def briefs_block(d, y, h):
    d.rectangle([MX, y, W - MX, y + 17], fill=INK)
    T(d, (MX + 6, y + 3), "ALSO RUNG TODAY — 24 MORE DATED STORIES, NUMBERED AS REPORTED",
      F(10, True), CREAM)
    cols = 4
    cw = (W - 2 * MX) / cols
    rows = (len(BRIEFS) + cols - 1) // cols
    rh = (h - 22) / rows
    for idx, (num, text) in enumerate(BRIEFS):
        cx = MX + (idx // rows) * cw
        cy = y + 21 + (idx % rows) * rh
        T(d, (cx + 2, cy), f"{num}. {text}", F(9), INK)
    return y + h


def bottom_row(d, y, h, order):
    widths = {"map": 0.44, "time": 0.28, "date": 0.28}
    x = MX
    total = W - 2 * MX
    for i, kind in enumerate(order):
        w = total * widths[kind] - (6 if i < 2 else 0)
        if kind == "map":
            d.rectangle([x, y, x + w, y + 15], fill=INK)
            T(d, (x + 5, y + 3), "THE DAY ON THE MAP — PINS ARE CARD NUMBERS", F(9, True), CREAM)
            draw_map(d, x + 4, y + 19, w - 8, h - 36, PINS)
            T(d, (x + 5, y + h - 13),
              "36 NVIDIA · 33 WASHINGTON · 2 HORMUZ · 1 POLAND · 3 IRAQ · 6 UKRAINE",
              F(7, True), MUTE)
            T(d, (x + 5, y + h - 5),
              "4 GAZA · 5 BRUSSELS · 10 CHINA · 11 MADRID · 13 GBR REEF · 37 US · 26 SOLOMONS",
              F(7, True), MUTE)
        elif kind == "time":
            d.rectangle([x, y, x + w, y + 15], fill=GREEN)
            T(d, (x + 5, y + 3), "THE DAY, BELL TO BELL", F(9, True), CREAM)
            ty = y + 21
            for when, what in TIMELINE:
                T(d, (x + 5, ty), when, F(8, True), GREEN)
                for line in wrap(d, what, F(9), w - 66):
                    T(d, (x + 64, ty), line, F(9), INK)
                    ty += 11
                ty += 4
        else:
            d.rectangle([x, y, x + w, y + 15], fill=INK)
            T(d, (x + 5, y + 3), "DATE CHECK — NOT TODAY", F(9, True), CREAM)
            ty = y + 21
            for item in DATECHECK:
                T(d, (x + 5, ty), "×", F(10, True), RED)
                for line in wrap(d, item, F(9), w - 22):
                    T(d, (x + 17, ty), line, F(9), INK)
                    ty += 11
                ty += 3
        x += w + 6
    return y + h


def footer(d):
    T(d, (MX, 1002),
      "Sources: Forbes via wires · RFE/RL · Al Jazeera · DW · Starlit Daily · wire roundups. Claims are labelled as claims.",
      F(8), MUTE)
    T(d, (W - MX, 1002), "Original drawings, drawn for this page.", F(8), MUTE, anchor="ra")
    T(d, (W / 2, 1013), "THE MARKET BELL · TUESDAY 25 NOVEMBER 2026 · RUNG ONCE, AT THE CLOSE",
      F(8, True), INK, anchor="ma")


# ---------------------------------------------------------------- layouts
def layout_a():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    T(d, (MX, 8), "ONE DAY · 37 DATED STORIES · 13 FULL-SCENE CARDS · 9 REGIONS",
      F(11, True), INK)
    T(d, (W - MX, 8), "EVERY FIGURE FROM TODAY'S WIRES", F(11, True), GREEN, anchor="ra")
    d.line([MX, 28, W - MX, 28], fill=GOLD, width=2)
    bell(d, MX + 26, 62, 13, GOLD)
    bell(d, W - MX - 26, 62, 13, GOLD)
    T(d, (W / 2, 34), "THE MARKET BELL", F(54, disp=True), INK, anchor="ma")
    T(d, (W / 2, 98), "TUESDAY 25 NOVEMBER 2026", F(15, True), GREEN, anchor="ma")
    d.line([MX, 118, W - MX, 118], fill=GOLD, width=2)
    y = ticker_band(d, 124)
    y = region_strip(d, y + 2)
    y += 6
    draw_wide_lead(d, 36, MX, y, W - 2 * MX, 140)
    y += 146
    hw = (W - 2 * MX - 8) / 2
    draw_card(d, 33, MX, y, hw, 140, lead=True)
    draw_card(d, 2, MX + hw + 8, y, hw, 140, lead=True)
    y += 146
    cw = (W - 2 * MX - 4 * 6) / 5
    for r in range(2):
        for c in range(5):
            draw_card(d, GRID[r * 5 + c], MX + c * (cw + 6), y, cw, 142)
        y += 148
    y = briefs_block(d, y + 2, 88)
    bottom_row(d, y + 6, 990 - (y + 6), ["map", "time", "date"])
    footer(d)
    return img


def layout_b():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    T(d, (MX, 8), "ONE DAY — ONE PAGE — EVERY STORY DATED AND SOURCED", F(11, True), INK)
    T(d, (W - MX, 8), "37 STORIES — 9 REGIONS", F(11, True), GREEN, anchor="ra")
    d.rectangle([MX, 28, W - MX, 98], fill=GREEN)
    bell(d, MX + 30, 58, 12, GOLD_L)
    T(d, (MX + 52, 40), "THE MARKET BELL", F(38, disp=True), CREAM)
    T(d, (MX + 54, 82), "OLD GOLD & BOTTLE GREEN — THE DAY, PRICED HONESTLY", F(9, True), (220, 200, 150))
    d.rectangle([W - MX - 218, 36, W - MX - 8, 90], fill=GOLD)
    T(d, (W - MX - 113, 42), "TUESDAY", F(17, True), CREAM, anchor="ma")
    T(d, (W - MX - 113, 64), "25 NOVEMBER 2026", F(17, True), CREAM, anchor="ma")
    y = ticker_line(d, 104)
    y = region_strip(d, y + 2)
    y += 6
    lw = (W - 2 * MX - 2 * 8) / 3
    for i, num in enumerate(LEADS):
        draw_card(d, num, MX + i * (lw + 8), y, lw, 232, lead=True)
    y += 238
    cw = (W - 2 * MX - 4 * 6) / 5
    for r in range(2):
        for c in range(5):
            draw_card(d, GRID[r * 5 + c], MX + c * (cw + 6), y, cw, 168)
        y += 174
    y = briefs_block(d, y + 2, 100)
    bottom_row(d, y + 6, 990 - (y + 6), ["date", "map", "time"])
    footer(d)
    return img


def render(variant):
    return layout_a() if variant == "A" else layout_b()


if __name__ == "__main__":
    variant = sys.argv[1] if len(sys.argv) > 1 else "A"
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, f"entry_{variant.lower()}.png")
    render(variant).save(out, optimize=True)
    print("saved", out)
