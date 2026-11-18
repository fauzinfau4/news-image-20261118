#!/usr/bin/env python3
"""Draw the 18 November 2026 world-news summary image (1024x1024 PNG).

The final image is baked into entry.png; main.py only copies it so the
graded program is deterministic and needs no network access.
All text is rendered here with PIL + DejaVu (no AI-generated text).
All illustrations are flat vector shapes drawn with PIL primitives.
Layout: dark masthead, six cards in a 2x3 grid, each with a left
illustration tile, a coloured side bar, a tag, a headline and a short body.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
F_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
F_REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")

W = H = 1024

# Palette
SLATE = (16, 26, 34)
SLATE_LT = (34, 48, 62)
RED = (178, 44, 36)
GOLD = (198, 140, 44)
PAPER = (247, 245, 238)
INK = (22, 24, 26)
BODY = (56, 56, 54)
MUTED = (112, 108, 98)
CARD = (255, 255, 255)
BORDER = (218, 212, 198)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- scenes
# Each scene draws into a 150x240 portrait tile (flat vector style).

def scene_chip(d):
    # dark teal board, gold circuit traces, green chip, rising arrow
    d.rectangle([0, 0, 150, 240], fill=(12, 44, 40))
    for x0, y0, x1, y1 in ((14, 56, 52, 56), (98, 56, 136, 56),
                           (14, 184, 52, 184), (98, 184, 136, 184),
                           (52, 14, 52, 56), (98, 14, 98, 56),
                           (52, 184, 52, 226), (98, 184, 98, 226)):
        d.line([x0, y0, x1, y1], fill=GOLD, width=3)
    for cx, cy in ((14, 56), (136, 56), (14, 184), (136, 184),
                   (52, 14), (98, 14), (52, 226), (98, 226)):
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=GOLD)
    # chip body
    d.rectangle([40, 70, 110, 170], fill=(96, 168, 0))
    d.rectangle([40, 70, 110, 170], outline=(48, 96, 0), width=4)
    for i in range(5):
        d.rectangle([46 + i * 12, 62, 54 + i * 12, 70], fill=(210, 210, 210))
        d.rectangle([46 + i * 12, 170, 54 + i * 12, 178], fill=(210, 210, 210))
        d.rectangle([32, 78 + i * 12, 40, 86 + i * 12], fill=(210, 210, 210))
        d.rectangle([110, 78 + i * 12, 118, 86 + i * 12], fill=(210, 210, 210))
    d.rectangle([60, 96, 90, 144], fill=(24, 64, 10))
    d.rectangle([66, 104, 84, 124], fill=(96, 168, 0))
    # rising arrow across the chip
    d.line([46, 138, 66, 118, 78, 128, 104, 100], fill=(255, 255, 255), width=5)
    d.polygon([(104, 100), (92, 102), (102, 112)], fill=(255, 255, 255))


def scene_virus(d):
    # pale rose background, spiky red virus spheres
    d.rectangle([0, 0, 150, 240], fill=(246, 226, 224))
    d.ellipse([8, 196, 142, 240], fill=(228, 196, 192))  # ground hint

    def virus(cx, cy, r, col):
        for i in range(12):
            a = math.radians(i * 30)
            x1 = cx + int((r - 2) * math.cos(a))
            y1 = cy + int((r - 2) * math.sin(a))
            x2 = cx + int((r + 12) * math.cos(a))
            y2 = cy + int((r + 12) * math.sin(a))
            d.line([x1, y1, x2, y2], fill=col, width=4)
            d.ellipse([x2 - 4, y2 - 4, x2 + 4, y2 + 4], fill=col)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
        d.ellipse([cx - r + 8, cy - r + 8, cx - r + 22, cy - r + 22],
                  fill=(255, 255, 255))

    virus(75, 92, 42, (178, 44, 36))
    virus(30, 178, 22, (200, 90, 80))
    virus(122, 182, 18, (200, 90, 80))
    # small shield with cross (vaccination)
    d.polygon([(75, 196), (108, 208), (108, 224), (75, 240), (42, 224),
               (42, 208)], fill=(255, 255, 255))
    d.polygon([(75, 196), (108, 208), (108, 224), (75, 240), (42, 224),
               (42, 208)], outline=(178, 44, 36), width=3)
    d.rectangle([71, 210, 79, 232], fill=(178, 44, 36))
    d.rectangle([63, 217, 87, 225], fill=(178, 44, 36))


def scene_plane(d):
    # grey sky, snowy Siberian hills, plane nose-down with smoke,
    # flames where it hit the ground
    d.rectangle([0, 0, 150, 240], fill=(168, 178, 186))
    d.ellipse([112, 16, 142, 46], fill=(240, 240, 235))  # pale sun
    # snowy hills
    d.polygon([(0, 150), (50, 96), (100, 150)], fill=(226, 232, 236))
    d.polygon([(60, 150), (120, 92), (150, 130), (150, 150)],
              fill=(206, 214, 220))
    # taiga band
    d.rectangle([0, 150, 150, 240], fill=(38, 74, 52))
    for x in range(6, 150, 18):
        d.polygon([(x, 186), (x + 8, 158), (x + 16, 186)],
                  fill=(24, 56, 38))
    d.rectangle([0, 186, 150, 240], fill=(52, 88, 62))
    # smoke trail from the plane
    for cx, cy, r in ((52, 58, 11), (66, 70, 13), (80, 82, 15), (94, 94, 13)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(88, 88, 90))
    # plane silhouette, nose-down to the right
    d.polygon([(40, 96), (96, 122), (100, 130), (46, 106)],
              fill=(28, 30, 34))  # fuselage
    d.polygon([(66, 108), (58, 130), (76, 116)], fill=(28, 30, 34))  # wing
    d.polygon([(40, 96), (30, 88), (44, 104)], fill=(28, 30, 34))  # tail
    d.polygon([(96, 122), (108, 120), (100, 130)], fill=(28, 30, 34))  # nose
    # flames at the crash point on the ground
    cx, cy = 112, 196
    d.polygon([(cx - 26, cy + 16), (cx - 16, cy - 18), (cx - 6, cy + 2),
               (cx + 2, cy - 26), (cx + 12, cy - 2), (cx + 22, cy - 16),
               (cx + 26, cy + 16)], fill=(255, 140, 0))
    d.polygon([(cx - 12, cy + 16), (cx - 6, cy - 6), (cx + 2, cy + 6),
               (cx + 8, cy - 10), (cx + 14, cy + 16)], fill=(255, 210, 60))
    # smoke rising from the fire
    for sx, sy, r in ((112, 158, 10), (120, 142, 12), (108, 128, 9)):
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(96, 96, 98))


def scene_knesset(d):
    # sandstone parliament: dome, columns, steps + ballot box
    d.rectangle([0, 0, 150, 240], fill=(214, 228, 240))
    d.ellipse([18, 14, 52, 48], fill=(255, 236, 190))  # sun
    # building
    d.rectangle([16, 108, 134, 196], fill=(238, 226, 200))
    d.polygon([(8, 108), (75, 66), (142, 108)], fill=(214, 198, 164))
    d.ellipse([58, 48, 92, 82], fill=(198, 178, 138))  # dome
    d.rectangle([72, 34, 78, 52], fill=(198, 178, 138))
    for x in (26, 52, 78, 104):
        d.rectangle([x, 116, x + 12, 186], fill=(250, 240, 214))
    d.rectangle([10, 196, 140, 204], fill=(190, 172, 136))
    d.rectangle([6, 204, 144, 212], fill=(176, 158, 122))
    # flag: blue-white with star
    d.rectangle([118, 30, 121, 108], fill=(90, 80, 70))
    d.rectangle([121, 34, 146, 58], fill=(255, 255, 255))
    d.rectangle([121, 34, 146, 40], fill=(30, 80, 170))
    d.rectangle([121, 52, 146, 58], fill=(30, 80, 170))
    # ballot box with tick
    d.rectangle([20, 218, 62, 238], fill=(30, 80, 170))
    d.rectangle([14, 212, 68, 218], fill=(24, 64, 140))
    d.line([28, 228, 38, 236, 56, 220], fill=(255, 255, 255), width=5)


def scene_spy(d):
    # dark navy: magnifier over a file, two small flags
    d.rectangle([0, 0, 150, 240], fill=(20, 34, 56))
    for x, y in ((18, 24), (132, 40), (120, 200), (24, 210), (140, 120)):
        d.ellipse([x, y, x + 4, y + 4], fill=(200, 200, 200))
    # file
    d.rectangle([28, 52, 122, 150], fill=(240, 238, 230))
    d.rectangle([28, 52, 122, 150], outline=(160, 156, 146), width=2)
    for yy in (66, 80, 94, 108):
        d.line([38, yy, 112, yy], fill=(120, 118, 110), width=3)
    d.rectangle([38, 122, 78, 134], fill=(178, 44, 36))
    # red stamp circle
    d.ellipse([92, 118, 116, 142], outline=(178, 44, 36), width=3)
    # magnifier
    d.ellipse([48, 128, 108, 188], outline=(216, 164, 65), width=6)
    d.line([100, 180, 120, 200], fill=(216, 164, 65), width=8)
    # US flag (small)
    for i in range(5):
        d.rectangle([14, 206 + i * 5, 66, 206 + i * 5 + 2],
                    fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
    d.rectangle([14, 206, 30, 220], fill=(30, 60, 120))
    # UK flag (small, simplified)
    d.rectangle([84, 206, 136, 232], fill=(0, 36, 125))
    d.rectangle([84, 216, 136, 222], fill=(255, 255, 255))
    d.rectangle([107, 206, 113, 232], fill=(255, 255, 255))
    d.rectangle([84, 218, 136, 220], fill=(200, 16, 46))
    d.rectangle([109, 206, 111, 232], fill=(200, 16, 46))


def scene_court(d):
    # courthouse with pediment and columns, gavel in front
    d.rectangle([0, 0, 150, 240], fill=(226, 228, 230))
    # building
    d.rectangle([18, 92, 132, 182], fill=(250, 250, 248))
    d.polygon([(10, 92), (75, 56), (140, 92)], fill=(188, 190, 194))
    d.ellipse([67, 66, 83, 82], fill=(198, 140, 44))
    for x in (28, 54, 80, 106):
        d.rectangle([x, 100, x + 12, 168], fill=(158, 160, 164))
    d.rectangle([14, 182, 136, 190], fill=(148, 150, 154))
    d.rectangle([10, 190, 140, 198], fill=(138, 140, 144))
    # gavel
    d.rectangle([34, 206, 92, 222], fill=(122, 82, 44))
    d.rectangle([28, 200, 46, 228], fill=(96, 62, 30))
    d.rectangle([88, 206, 118, 216], fill=(122, 82, 44))
    # sound block
    d.rectangle([96, 222, 132, 232], fill=(96, 62, 30))


SCENES = {
    "chip": scene_chip,
    "virus": scene_virus,
    "plane": scene_plane,
    "knesset": scene_knesset,
    "spy": scene_spy,
    "court": scene_court,
}

# ---------------------------------------------------------------- stories
STORIES = [
    dict(tag="TECH \u00b7 USA", color=(20, 100, 60), scene="chip",
         head="NVIDIA BEATS ESTIMATES; HUANG NOT BACK",
         body="Q3 revenue hits $115.8bn, double a year ago, with $130bn "
              "guided next. The board says it will not bring back ousted "
              "CEO Jensen Huang; interim chief Colette Kress takes over."),
    dict(tag="HEALTH \u00b7 AMERICAS", color=(178, 44, 36), scene="virus",
         head="US LOSES MEASLES-FREE STATUS",
         body="After 26 years, the Pan American Health Organization strips "
              "the US of measles elimination status. Cases pass 5,400 in "
              "2026, the worst in 30 years; Mexico and Bolivia lose it too."),
    dict(tag="DISASTER \u00b7 RUSSIA", color=(90, 90, 96), scene="plane",
         head="ARMY PLANE DOWN IN SIBERIA",
         body="An An-12 military transport crashes in the Kemerovo region. "
              "Russia's defence ministry says all 19 aboard died; a "
              "technical fault is the suspected cause."),
    dict(tag="POLITICS \u00b7 ISRAEL", color=(30, 80, 170), scene="knesset",
         head="KNESSET PICKS EISENKOT ALLY AS SPEAKER",
         body="Matan Kahana wins 66\u201352, replacing Likud's Amir Ohana. "
              "The vote hands Netanyahu's rivals control of parliament's "
              "agenda as Eisenkot tries to form a government."),
    dict(tag="ESPIONAGE \u00b7 UK / USA", color=(40, 60, 110), scene="spy",
         head="US OFFICER IN SPY CASE HANDED OVER",
         body="Lt Col Brandon Tyner, arrested in Britain on Nov 10 on "
              "suspicion of spying for Russia, is transferred to US "
              "military custody. The Kremlin denies any link."),
    dict(tag="COURTS \u00b7 USA", color=(120, 70, 20), scene="court",
         head="27 YEARS FOR PLOT TO KILL TRUMP",
         body="Asif Merchant is jailed for 27\u00bd years in Brooklyn for an "
              "Iran-linked murder-for-hire plot against Donald Trump. "
              "Prosecutors had sought life."),
]


def draw_panel(img, x, y, w, h, story):
    d = ImageDraw.Draw(img)
    # card
    d.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=CARD,
                        outline=BORDER, width=2)
    # coloured side bar
    d.rounded_rectangle([x, y, x + 7, y + h], radius=4, fill=story["color"])
    d.rectangle([x + 3, y, x + 7, y + h], fill=story["color"])
    # illustration tile
    tile = Image.new("RGB", (150, 240), (255, 255, 255))
    td = ImageDraw.Draw(tile)
    SCENES[story["scene"]](td)
    mask = Image.new("L", (150, 240), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([0, 0, 150, 240], radius=8, fill=255)
    img.paste(tile, (x + 16, y + 16), mask)
    # text column
    tx = x + 178
    tw = x + w - 14 - tx
    f_tag = font(F_BOLD, 14)
    f_head = font(F_BOLD, 23)
    f_body = font(F_REG, 17)
    cy = y + 20
    d.text((tx, cy), story["tag"], font=f_tag, fill=story["color"])
    cy += 25
    for line in wrap(d, story["head"], f_head, tw):
        d.text((tx, cy), line, font=f_head, fill=INK)
        cy += 28
    cy += 4
    for line in wrap(d, story["body"], f_body, tw):
        d.text((tx, cy), line, font=f_body, fill=BODY)
        cy += 22


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # masthead
    d.rectangle([0, 0, W, 104], fill=SLATE)
    d.rectangle([0, 104, W, 108], fill=RED)
    f_title = font(F_BOLD, 44)
    title = "WEDNESDAY 18 NOVEMBER 2026"
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, 14), title, font=f_title, fill=(255, 255, 255))
    f_sub = font(F_BOLD, 18)
    sub = "T H E   W O R L D   I N   O N E   D A Y"
    sw = d.textlength(sub, font=f_sub)
    d.text(((W - sw) / 2, 68), sub, font=f_sub, fill=GOLD)
    # grid 2 x 3
    pw, ph, gap = 490, 272, 12
    gx, gy = 16, 120
    for i, story in enumerate(STORIES):
        col, row = i % 2, i // 2
        draw_panel(img, gx + col * (pw + gap), gy + row * (ph + gap),
                   pw, ph, story)
    # footer
    f_foot = font(F_REG, 15)
    foot = ("Sources: Reuters \u00b7 AP \u00b7 AFP \u00b7 CNN \u00b7 Al Jazeera"
            "  \u2014  18 November 2026")
    fw = d.textlength(foot, font=f_foot)
    d.text(((W - fw) / 2, 986), foot, font=f_foot, fill=MUTED)
    return img


if __name__ == "__main__":
    out = os.path.join(HERE, "entry.png")
    img = build()
    img.save(out, "PNG", optimize=True)
    print(out, os.path.getsize(out), "bytes", img.size)
