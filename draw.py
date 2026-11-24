#!/usr/bin/env python3
"""news-23 b110 front-page-dense: draw THE WORLD TODAY, Monday 23 Nov 2026."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

FD = "/usr/share/fonts/truetype/dejavu"
FL = "/usr/share/fonts/truetype/liberation"


def font(path, size):
    return ImageFont.truetype(path, size)


SERIF_B = font(f"{FD}/DejaVuSerif-Bold.ttf", 46)
SERIF_H = font(f"{FD}/DejaVuSerif-Bold.ttf", 21)
SANS_B = font(f"{FL}/LiberationSans-Bold.ttf", 16)
SANS = font(f"{FL}/LiberationSans-Regular.ttf", 13)
SANS_S = font(f"{FL}/LiberationSans-Regular.ttf", 11)
SANS_XS = font(f"{FL}/LiberationSans-Regular.ttf", 10)
SANS_XS_B = font(f"{FL}/LiberationSans-Bold.ttf", 10)
SANS_9 = font(f"{FL}/LiberationSans-Regular.ttf", 9)
SANS_9_B = font(f"{FL}/LiberationSans-Bold.ttf", 9)

BLACK = (17, 17, 17)
RED = (200, 16, 46)
GOLD = (201, 162, 39)
GOLD_D = (176, 138, 20)
NAVY = (11, 42, 74)
TEAL = (14, 124, 123)
GREEN = (20, 107, 52)
CREAM = (255, 248, 231)
GRAY = (85, 85, 85)
LGRAY = (238, 238, 238)
MAPG = (186, 220, 178)
WHITE = (255, 255, 255)

img = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(img)


def text(x, y, s, f, fill, anchor="la"):
    d.text((x, y), s, font=f, fill=fill, anchor=anchor)


def wrap(s, f, maxw):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=f) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def chip(x_right, y, label, fill):
    w_ = int(d.textlength(label, font=SANS_9_B)) + 10
    d.rectangle([x_right - w_, y, x_right, y + 13], fill=fill)
    text(x_right - w_ / 2, y + 1, label, SANS_9_B, WHITE, anchor="ma")


# ---------- masthead ----------
d.rectangle([0, 0, W, 54], fill=BLACK)
text(10, 4, "THE WORLD TODAY", SERIF_B, WHITE)
text(1014, 19, "MONDAY 23 NOVEMBER 2026", SANS_B, GOLD, anchor="ra")

# ---------- kicker ----------
d.rectangle([0, 54, W, 76], fill=RED)
text(512, 58, "AI rout hits Asia  \u00b7  UN chief urges AI rules  \u00b7  "
     "US lead over China at record low  \u00b7  Anthropic IPO $107.3B",
     font(f"{FL}/LiberationSans-Bold.ttf", 17), WHITE, anchor="ma")

# ---------- number strip: 2 rows x 5 cols, pitch 27 ----------
NUMS = [
    ("-3.3%", "KOSPI", RED), ("5.3", "US-CHINA POWER GAP", NAVY),
    ("11,762", "EBOLA CASES, DRC", GREEN), ("10T won", "SEOUL STABILISATION FUND", GOLD_D),
    ("2%", "BILLIONAIRE TAX IN PARIS", BLACK),
    ("$450M", "SKUBAL DEAL", RED), ("165", "RUSSIAN MISSILES/WEEK", NAVY),
    ("12,000", "CLEARED IN MANCHESTER", GREEN), ("264 kg", "EXPLOSIVES SEIZED", GOLD_D),
    ("$107.3B", "ANTHROPIC IPO", BLACK),
]
for i, (val, lab, col) in enumerate(NUMS):
    row, c = divmod(i, 5)
    x = 10 + c * 204
    y = 77 + row * 26
    text(x, y, val, font(f"{FL}/LiberationSans-Bold.ttf", 15), col)
    text(x, y + 16, lab, SANS_9, GRAY)

# ---------- region bar ----------
REGIONS = [("ASIA-PACIFIC 7", TEAL, 172), ("AMERICAS 8", RED, 172),
           ("MIDDLE EAST 6", GOLD_D, 172), ("EUROPE 5", NAVY, 172),
           ("AFRICA 3", GREEN, 168), ("WORLD 2", GRAY, 168)]
x = 0
for name, col, w_ in REGIONS:
    d.rectangle([x, 132, x + w_, 150], fill=col)
    text(x + w_ / 2, 136, name, SANS_XS_B, WHITE, anchor="ma")
    x += w_

# ---------- UTC strip ----------
d.rectangle([0, 150, W, 166], fill=LGRAY)
text(10, 152, "THE DAY IN UTC   ~00:00 Kospi dives   ~06:30 Guterres opens   "
     "~09:00 Power Index   ~12:00 Paris 2% tax   ~15:00 Kyiv missiles",
     SANS_XS, BLACK)
text(1014, 152, "~ APPROX", SANS_XS, GRAY, anchor="ra")

# ---------- hero scenes ----------
HX = [8, 348, 688]          # hero column x
HW = 328                    # hero column width
SC_Y, SC_H = 168, 132       # scene area
LB_Y = 300                  # scene label bar y

# --- scene 1: Kospi skyline + falling chart ---
x0 = HX[0]
d.rectangle([x0, SC_Y, x0 + HW, SC_Y + SC_H], fill=NAVY)
import random
random.seed(23)
for bx in range(x0 + 8, x0 + HW - 10, 26):
    bh = random.randint(38, 88)
    d.rectangle([bx, SC_Y + SC_H - bh, bx + 20, SC_Y + SC_H], fill=(16, 58, 96))
    for wy in range(SC_Y + SC_H - bh + 6, SC_Y + SC_H - 4, 12):
        for wx in (bx + 4, bx + 12):
            if random.random() < 0.7:
                d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 214, 90))
pts = [(x0 + 14, SC_Y + 34), (x0 + 80, SC_Y + 48), (x0 + 150, SC_Y + 44),
       (x0 + 210, SC_Y + 66), (x0 + 270, SC_Y + 82), (x0 + 316, SC_Y + 104)]
d.line(pts, fill=(255, 140, 40), width=3)
for px, py in pts:
    d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=WHITE)
text(x0 + 10, SC_Y + 4, "-3.3%", font(f"{FL}/LiberationSans-Bold.ttf", 34), WHITE)
d.rectangle([x0, LB_Y, x0 + HW, LB_Y + 16], fill=BLACK)
text(x0 + 6, LB_Y + 2, "KOSPI 4,708.54  \u00b7  -161 PTS", SANS_XS_B, WHITE)

# --- scene 2: Guterres ---
x0 = HX[1]
d.rectangle([x0, SC_Y, x0 + HW, SC_Y + SC_H], fill=(20, 83, 45))
text(x0 + 12, SC_Y + 6, "150", font(f"{FL}/LiberationSans-Bold.ttf", 46), GOLD)
for j, ln in enumerate(["DELEGATES", "BACK A RISK", "FRAMEWORK"]):
    text(x0 + 12, SC_Y + 56 + j * 22, ln,
         font(f"{FL}/LiberationSans-Bold.ttf", 20), GOLD)
cx, cy, r = x0 + 262, SC_Y + 62, 44
d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(190, 230, 190))
d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(120, 180, 120), width=2)
d.ellipse([cx - 20, cy - r, cx + 20, cy + r], outline=(120, 180, 120), width=1)
d.line([cx - r, cy, cx + r, cy], fill=(120, 180, 120), width=1)
d.line([cx, cy - r, cx, cy + r], fill=(120, 180, 120), width=1)
d.rectangle([x0, LB_Y, x0 + HW, LB_Y + 16], fill=BLACK)
text(x0 + 6, LB_Y + 2, "UN  \u00b7  BRIDGETOWN", SANS_XS_B, WHITE)

# --- scene 3: Power Index bars ---
x0 = HX[2]
d.rectangle([x0, SC_Y, x0 + HW, SC_Y + SC_H], fill=CREAM)
text(x0 + 8, SC_Y + 6, "NARROWEST SINCE 2018", SANS_XS_B, BLACK)
text(x0 + HW - 8, SC_Y + 6, "GAP 5.3", SANS_XS_B, RED, anchor="ra")
BASE = SC_Y + 122
bars = [("78.9", "US", NAVY, 70), ("73.6", "CHINA", RED, 66), ("40.5", "INDIA", GOLD, 37)]
for k, (val, lab, col, bh) in enumerate(bars):
    bx = x0 + 28 + k * 104
    text(bx + 35, BASE - bh - 20, val, font(f"{FL}/LiberationSans-Bold.ttf", 16), BLACK, anchor="ma")
    d.rectangle([bx, BASE - bh, bx + 70, BASE], fill=col)
    text(bx + 35, BASE - 16, lab, SANS_XS_B, WHITE, anchor="ma")
d.rectangle([x0, LB_Y, x0 + HW, LB_Y + 16], fill=BLACK)
text(x0 + 6, LB_Y + 2, "ASIA POWER INDEX 2026", SANS_XS_B, WHITE)

# ---------- hero headlines / bodies / source+chip ----------
HEROES = [
    ("AI ROUT HITS ASIA",
     "Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. "
     "Samsung -3.1%, SK Hynix -2.5%.", "KOREA EXCHANGE"),
    ("GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
     "UN chief urges global AI safety rules at the Bridgetown summit; "
     "150 back a risk framework.", "UNITED NATIONS"),
    ("US LEAD OVER CHINA AT RECORD LOW",
     "Asia Power Index 2026: US 78.9, China 73.6 \u2014 gap 5.3, narrowest "
     "since 2018. India third at 40.5.", "LOWY INSTITUTE"),
]
for x0, (hl, body, src) in zip(HX, HEROES):
    lines = wrap(hl, SERIF_H, HW - 4)
    for j, ln in enumerate(lines[:2]):
        text(x0, 322 + j * 23, ln, SERIF_H, BLACK)
    blines = wrap(body, SANS, HW - 4)
    for j, ln in enumerate(blines[:2]):
        text(x0, 370 + j * 15, ln, SANS, BLACK)
    text(x0, 402, src, SANS_XS, GRAY)
    chip(x0 + HW, 398, "REPORTED", NAVY)

# ---------- MORE OF THE DAY strip ----------
d.rectangle([0, 414, W, 432], fill=BLACK)
text(10, 418, "MORE OF THE DAY  \u2014  10 STORIES", SANS_XS_B, WHITE)

# ---------- 10 cards: 2 rows x 5 cols ----------
CARDS = [
    ("AMERICAS", RED, "BESSENT: NVIDIA ANSWERS", "Treasury wants answers.", "Reuters", "REPORTED"),
    ("FBI", NAVY, "FBI PROBES NCIC HACK", "NCIC database hacked.", "AP", "REPORTED"),
    ("WHITE HOUSE", TEAL, "TRUMP: IRAN STRIKES MAY RESUME", "May resume in New Year.", "Reuters", "REPORTED"),
    ("MARKETS", GREEN, "US FUTURES JUMP 3%", "Holiday rally lifts 3%.", "Bloomberg", "REPORTED"),
    ("SPORT", GOLD_D, "SKUBAL'S $450M METS DEAL", "Nine-year deal, largest ever.", "AP", "REPORTED"),
    ("SPORT", GOLD_D, "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice.", "ESPN", "REPORTED"),
    ("LEGAL", (120, 60, 140), "STATES SUE SPACEX", "Ten states sue over AI.", "AP", "REPORTED"),
    ("TECH", TEAL, "ANTHROPIC IPO: $107.3B", "Raised $83; closes $97.17.", "WSJ", "REPORTED"),
    ("EUROPE", NAVY, "POLAND: 3 MISSILES CROSSED AIRSPACE", "Kyiv: 3 Kh-101s crossed.", "AP", "CLAIM"),
    ("SPACE", (90, 60, 120), "RUSSIAN NUCLEAR SATELLITE", "May carry a nuke.", "Reuters", "CLAIM"),
]
CARD_F = font(f"{FL}/LiberationSans-Bold.ttf", 12)
CARD_SRC = font(f"{FL}/LiberationSans-Regular.ttf", 10)
for i, (cat, col, hl, body, src, ch) in enumerate(CARDS):
    row, c = divmod(i, 5)
    x = 8 + c * 204
    y = 436 + row * 72
    d.rectangle([x, y, x + 198, y + 68], fill=WHITE, outline=(200, 200, 200))
    d.rectangle([x, y, x + 198, y + 15], fill=col)
    text(x + 5, y + 2, cat, SANS_XS_B, WHITE)
    text(x + 193, y + 2, str(i + 1), SANS_XS_B, WHITE, anchor="ra")
    lines = wrap(hl, CARD_F, 188)
    for j, ln in enumerate(lines[:2]):
        text(x + 5, y + 18 + j * 12, ln, CARD_F, BLACK)
    text(x + 5, y + 47, body, SANS_XS, BLACK)
    text(x + 5, y + 57, src, CARD_SRC, GRAY)
    chip(x + 193, y + 53, ch, RED if ch == "CLAIM" else NAVY)

# ---------- map + ALSO ----------
d.rectangle([0, 580, 404, 598], fill=BLACK)
text(10, 584, "WHERE IT HAPPENED", SANS_XS_B, WHITE)
d.rectangle([412, 580, W, 598], fill=BLACK)
text(420, 584, "ALSO ON MONDAY", SANS_XS_B, WHITE)

# stylised map blobs (Americas / Europe / Africa / Asia / Australia)
d.polygon([(28, 640), (95, 618), (165, 640), (188, 700), (172, 780),
           (140, 858), (95, 878), (45, 838), (18, 748)], fill=MAPG)
d.polygon([(212, 648), (268, 640), (298, 668), (288, 716), (248, 742),
           (214, 712)], fill=MAPG)
d.polygon([(222, 756), (272, 750), (288, 806), (268, 866), (230, 862),
           (210, 808)], fill=MAPG)
d.polygon([(306, 636), (362, 628), (396, 656), (390, 726), (352, 756),
           (310, 716)], fill=MAPG)
d.polygon([(326, 826), (368, 820), (374, 852), (334, 858)], fill=MAPG)

PINS = [(365, 690), (95, 855), (375, 665), (120, 745), (150, 720),
        (265, 690), (105, 770), (45, 790), (85, 810), (105, 835),
        (250, 675), (235, 655), (300, 665)]
for n, (px, py) in enumerate(PINS, 1):
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=WHITE, width=1)
    text(px, py - 5, str(n), SANS_9_B, WHITE, anchor="ma")

text(10, 884, "Pins 1-13:  1 Seoul \u00b7 2 Bridgetown \u00b7 3 Beijing", SANS_9, BLACK)
text(10, 894, "4 Washington \u00b7 5 New York \u00b7 6 Kyiv \u00b7 7 Chicago \u00b7 8 SF", SANS_9, BLACK)
text(10, 904, "9 Denver \u00b7 10 Austin \u00b7 11 Warsaw \u00b7 12 London \u00b7 13 Moscow", SANS_9, BLACK)

ALSO_L = [
    "14. Paris: 100+ back 2% billionaire tax",
    "15. Manchester: 12,000 cleared",
    "16. Zelenskyy: 165 missiles in a week",
    "17. COP31: the day after Antalya pact rejected",
    "18. Israel unity talks resume",
    "19. Gaza: two killed in Israeli strike",
    "20. West Bank settler attacks",
    "21. Iran war: no deal in sight",
    "22. Lebanon seizes 264 kg explosives",
]
ALSO_R = [
    "23. Bahrain: strike hits plant, 2 hurt",
    "24. Benghazi: UN demands probe [CLAIM]",
    "25. Sudan: defences down drones [CLAIM]",
    "26. DRC: fighting traps Ebola teams",
    "27. Bangladesh: Hasina jailed if she returns",
    "28. Seoul minister quits in exam row",
    "29. SK Telecom -7.3% as hype cools",
    "30. China eases margin rules",
    "31. Seoul readies 10T-won fund",
]
for j, s in enumerate(ALSO_L):
    col = RED if "[CLAIM]" in s else BLACK
    text(420, 600 + j * 30, s, font(f"{FL}/LiberationSans-Bold.ttf", 12) if "[CLAIM]" in s else SANS, col)
for j, s in enumerate(ALSO_R):
    col = RED if "[CLAIM]" in s else BLACK
    text(716, 600 + j * 30, s, font(f"{FL}/LiberationSans-Bold.ttf", 12) if "[CLAIM]" in s else SANS, col)

# ---------- DATE CHECK ----------
d.rectangle([8, 914, 1016, 960], outline=RED, width=2)
text(14, 918, "DATE CHECK", font(f"{FL}/LiberationSans-Bold.ttf", 13), RED)
text(1010, 918, "READ 23 NOV 2026, 23:59 UTC \u2014 STORIES DATED 23 NOV ONLY",
     SANS_XS_B, RED, anchor="ra")
text(14, 936, "LEFT OUT \u2014 NOT 23 NOV:  Dems 258 seats (22 Nov)  \u00b7  Sparta II fire (22 Nov)  "
     "\u00b7  El Chapo (22 Nov)  \u00b7  EU\u2013Indonesia (21 Nov)  \u00b7  Nigeria boat (21 Nov)  "
     "\u00b7  ICJ Myanmar (19 Nov)", SANS_XS, BLACK)
text(14, 949, "NOT YET \u2014 Dymer search continues (14 missing)  \u00b7  4 House races uncalled  "
     "\u00b7  COP32 venue not set  \u00b7  WHO evacuating trapped Ebola staff", SANS_XS, BLACK)

# ---------- footer ----------
text(10, 966, "Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 AFP \u00b7 Yonhap \u00b7 BBC \u00b7 WSJ \u00b7 "
     "ESPN \u00b7 Lowy Institute (Asia Power Index 2026).", SANS_XS, GRAY)
text(10, 978, "CHIPS: REPORTED = confirmed by wires \u00b7 CLAIM = one side's claim, not independently "
     "confirmed. ONGOING = still developing.", SANS_XS, GRAY)
text(10, 990, "All times UTC. Figures as reported 23 Nov 2026. Scenes are drawn illustrations, "
     "not photographs.", SANS_XS, GRAY)
text(512, 1006, "THE WORLD TODAY  \u00b7  Monday 23 November 2026  \u00b7  31 stories  \u00b7  6 regions",
     font(f"{FL}/LiberationSans-Bold.ttf", 12), GOLD_D, anchor="ma")

img.save(OUT)
print("saved", OUT, os.path.getsize(OUT), "bytes")
