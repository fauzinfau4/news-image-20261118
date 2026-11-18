"""Render a one-page news poster: six stories from 18 November 2026.

Everything here is drawn with Pillow primitives -- no downloaded assets,
no network access, no timestamps. The same input always produces the
same PNG bytes, because every coordinate, colour and string is fixed.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field

from PIL import Image, ImageDraw, ImageFont

CANVAS_W = 1024
CANVAS_H = 1024

PAPER = (244, 239, 230)
INK = (16, 28, 46)
GOLD = (212, 160, 60)
CARD = (255, 255, 255)
CARD_EDGE = (205, 196, 180)
MUTED = (110, 105, 95)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


@dataclass
class Story:
    """One news item: its label, headline, short summary and palette."""

    tag: str
    headline: str
    summary: str
    accent: tuple
    panel: tuple
    painter: str


@dataclass
class Poster:
    """Holds the canvas plus the typefaces and paints the whole page."""

    stories: list = field(default_factory=list)
    sheet: Image.Image = None
    pen: ImageDraw.ImageDraw = None

    def __post_init__(self):
        self.sheet = Image.new("RGB", (CANVAS_W, CANVAS_H), PAPER)
        self.pen = ImageDraw.Draw(self.sheet)

    # -- type helpers -------------------------------------------------
    def face(self, name, size):
        return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

    def split_lines(self, text, font, width):
        """Greedy word wrap measured with the real font."""
        words = text.split()
        lines, current = [], ""
        for word in words:
            trial = f"{current} {word}".strip()
            if self.pen.textlength(trial, font=font) <= width:
                current = trial
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines

    def block(self, lines, font, x, y, fill, leading):
        for line in lines:
            self.pen.text((x, y), line, font=font, fill=fill)
            y += leading
        return y

    # -- page furniture ----------------------------------------------
    def masthead(self):
        self.pen.rectangle([0, 0, CANVAS_W, 112], fill=INK)
        date_font = self.face("DejaVuSerif-Bold.ttf", 44)
        date = "WEDNESDAY 18 NOVEMBER 2026"
        tw = self.pen.textlength(date, font=date_font)
        self.pen.text(((CANVAS_W - tw) / 2, 16), date, font=date_font, fill=(250, 248, 242))
        sub_font = self.face("DejaVuSans-Bold.ttf", 17)
        sub = "S I X   S T O R I E S   ·   O N E   P A G E"
        sw = self.pen.textlength(sub, font=sub_font)
        self.pen.text(((CANVAS_W - sw) / 2, 72), sub, font=sub_font, fill=GOLD)
        self.pen.rectangle([0, 112, CANVAS_W, 116], fill=(178, 52, 44))

    def footer(self):
        font = self.face("DejaVuSans.ttf", 15)
        note = "Sources: Reuters · AP · AFP · Al Jazeera · US Dept. of Justice  —  18 November 2026"
        nw = self.pen.textlength(note, font=font)
        self.pen.text(((CANVAS_W - nw) / 2, 988), note, font=font, fill=MUTED)

    # -- one story card ----------------------------------------------
    def card(self, story, cx, cy, cw, ch):
        self.pen.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=10,
                                   fill=CARD, outline=CARD_EDGE, width=2)
        self.pen.rectangle([cx, cy + 8, cx + 7, cy + ch - 8], fill=story.accent)
        px, py, pw, ph = cx + 14, cy + 14, 168, ch - 28
        getattr(self, story.painter)(px, py, pw, ph)
        tx = cx + 196
        tw = cw - 196 - 14
        tag_font = self.face("DejaVuSans-Bold.ttf", 14)
        self.pen.text((tx, cy + 16), story.tag, font=tag_font, fill=story.accent)
        head_font = self.face("DejaVuSans-Bold.ttf", 25)
        y = self.block(self.split_lines(story.headline, head_font, tw),
                       head_font, tx, cy + 40, INK, 30)
        body_font = self.face("DejaVuSans.ttf", 15)
        self.block(self.split_lines(story.summary, body_font, tw),
                   body_font, tx, y + 8, (52, 52, 48), 20)

    # -- illustration panels -----------------------------------------
    def paint_chip(self, x, y, w, h):
        self.pen.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=(18, 62, 52))
        cx, cy = x + w // 2, y + h // 2 + 8
        for ex, ey in [(x + 12, y + 22), (x + w - 12, y + 22),
                       (x + 12, y + h - 22), (x + w - 12, y + h - 22),
                       (x + w // 2, y + 12), (x + w // 2, y + h - 12),
                       (x + 12, cy), (x + w - 12, cy)]:
            self.pen.line([ex, ey, cx, cy], fill=(212, 160, 60), width=3)
            self.pen.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], fill=(212, 160, 60))
        self.pen.rectangle([cx - 42, cy - 42, cx + 42, cy + 42], fill=(46, 160, 90))
        self.pen.rectangle([cx - 28, cy - 28, cx + 28, cy + 28], fill=(24, 96, 58))
        self.pen.rectangle([cx - 14, cy - 14, cx + 14, cy + 14], fill=(46, 160, 90))
        self.pen.line([(cx - 22, cy + 16), (cx - 4, cy - 2), (cx + 4, cy + 4),
                       (cx + 24, cy - 22)], fill=(255, 255, 255), width=4)
        self.pen.polygon([(cx + 24, cy - 22), (cx + 24, cy - 10), (cx + 12, cy - 22)],
                         fill=(255, 255, 255))

    def paint_virus(self, x, y, w, h):
        self.pen.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=(247, 226, 224))
        self._bug(x + w // 2, y + 82, 52, (198, 52, 44))
        self._bug(x + 42, y + h - 62, 30, (214, 96, 82))
        self._bug(x + w - 42, y + h - 58, 26, (214, 96, 82))
        self.pen.rounded_rectangle([x + w // 2 - 26, y + h - 46, x + w // 2 + 26, y + h - 12],
                                   radius=6, fill=(255, 255, 255), outline=(198, 52, 44), width=3)
        self.pen.rectangle([x + w // 2 - 4, y + h - 40, x + w // 2 + 4, y + h - 18],
                           fill=(198, 52, 44))
        self.pen.rectangle([x + w // 2 - 12, y + h - 32, x + w // 2 + 12, y + h - 26],
                           fill=(198, 52, 44))

    def _bug(self, cx, cy, r, colour):
        import math
        for k in range(10):
            ang = k * math.pi / 5
            ex, ey = cx + int((r + 12) * math.cos(ang)), cy + int((r + 12) * math.sin(ang))
            self.pen.line([cx, cy, ex, ey], fill=colour, width=4)
            self.pen.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], fill=colour)
        self.pen.ellipse([cx - r, cy - r, cx + r, cy + r], fill=colour)
        self.pen.ellipse([cx - r // 3, cy - r // 3, cx + r // 5, cy + r // 5],
                         fill=(255, 255, 255))

    def paint_crash(self, x, y, w, h):
        self.pen.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=(196, 205, 214))
        self.pen.ellipse([x + w - 52, y + 14, x + w - 16, y + 50], fill=(240, 236, 220))
        self.pen.polygon([(x, y + 150), (x + 60, y + 96), (x + 120, y + 150)],
                         fill=(150, 158, 168))
        self.pen.polygon([(x + 70, y + 150), (x + 130, y + 104), (x + w, y + 150)],
                         fill=(128, 138, 150))
        self.pen.rectangle([x, y + 150, x + w, y + h], fill=(38, 92, 58))
        for tx in range(x + 8, x + w - 8, 18):
            self.pen.polygon([(tx, y + h), (tx + 8, y + h - 26), (tx + 16, y + h)],
                             fill=(26, 66, 42))
        self.pen.polygon([(x + 28, y + 84), (x + 96, y + 118), (x + 92, y + 128),
                          (x + 34, y + 96)], fill=(32, 34, 38))
        self.pen.polygon([(x + 96, y + 118), (x + 132, y + 128), (x + 128, y + 136),
                          (x + 94, y + 128)], fill=(32, 34, 38))
        for sx, sy, sr in [(x + 52, y + 78, 13), (x + 68, y + 62, 16), (x + 88, y + 48, 12)]:
            self.pen.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(96, 96, 96))
        self.pen.polygon([(x + w // 2 - 18, y + h), (x + w // 2, y + h - 42),
                          (x + w // 2 + 18, y + h)], fill=(232, 120, 32))
        self.pen.polygon([(x + w // 2 - 9, y + h), (x + w // 2, y + h - 22),
                          (x + w // 2 + 9, y + h)], fill=(245, 196, 66))

    def paint_parliament(self, x, y, w, h):
        self.pen.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=(214, 230, 244))
        self.pen.ellipse([x + 16, y + 16, x + 48, y + 48], fill=(245, 214, 130))
        self.pen.rectangle([x + w - 26, y + 26, x + w - 23, y + 96], fill=(60, 60, 60))
        self.pen.polygon([(x + w - 26, y + 26), (x + w - 62, y + 36), (x + w - 26, y + 46)],
                         fill=(255, 255, 255))
        self.pen.rectangle([x + w - 62, y + 36, x + w - 26, y + 41], fill=(38, 84, 160))
        self.pen.rectangle([x + w - 62, y + 41, x + w - 26, y + 46], fill=(255, 255, 255))
        bx, bw = x + 22, w - 44
        self.pen.ellipse([x + w // 2 - 20, y + 62, x + w // 2 + 20, y + 100], fill=(214, 186, 138))
        self.pen.polygon([(bx, y + 108), (x + w // 2, y + 84), (bx + bw, y + 108)],
                         fill=(198, 170, 122))
        self.pen.rectangle([bx, y + 108, bx + bw, y + 196], fill=(232, 220, 196))
        for i in range(4):
            colx = bx + 12 + i * ((bw - 24) // 3)
            self.pen.rectangle([colx, y + 118, colx + 12, y + 186], fill=(196, 180, 146))
        self.pen.rectangle([bx - 6, y + 196, bx + bw + 6, y + 206], fill=(160, 140, 104))
        self.pen.rectangle([bx - 6, y + 206, bx + bw + 6, y + 214], fill=(120, 100, 70))
        self.pen.rounded_rectangle([x + 16, y + h - 26, x + 64, y + h - 2], radius=4,
                                   fill=(38, 84, 160))
        self.pen.line([(x + 26, y + h - 14), (x + 36, y + h - 22), (x + 52, y + h - 8)],
                      fill=(255, 255, 255), width=4)

    def paint_dossier(self, x, y, w, h):
        self.pen.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=(20, 34, 58))
        for dx, dy in [(x + 14, y + 16), (x + w - 20, y + 20), (x + 18, y + h - 22)]:
            self.pen.ellipse([dx, dy, dx + 6, dy + 6], fill=(200, 210, 220))
        self.pen.rectangle([x + 34, y + 26, x + w - 34, y + 158], fill=(238, 236, 228))
        for i, ly in enumerate(range(y + 44, y + 120, 14)):
            self.pen.rectangle([x + 46, ly, x + w - 46, ly + 5], fill=(150, 148, 140))
        self.pen.rectangle([x + 46, y + 128, x + w - 84, y + 138], fill=(178, 52, 44))
        self.pen.ellipse([x + w - 78, y + 122, x + w - 46, y + 154],
                         outline=(178, 52, 44), width=3)
        self.pen.ellipse([x + 78, y + 128, x + 130, y + 180],
                         outline=(212, 160, 60), width=6)
        self.pen.line([(x + 122, y + 172), (x + 148, y + 200)], fill=(212, 160, 60), width=7)
        for fx, flag in [(x + 22, "us"), (x + w - 62, "uk")]:
            self.pen.rectangle([fx, y + h - 34, fx + 40, y + h - 12],
                               outline=(255, 255, 255), width=2)
            if flag == "us":
                for s in range(4):
                    self.pen.rectangle([fx, y + h - 34 + s * 5, fx + 40, y + h - 32 + s * 5],
                                       fill=(178, 52, 44) if s % 2 == 0 else (255, 255, 255))
                self.pen.rectangle([fx, y + h - 34, fx + 16, y + h - 24], fill=(38, 84, 160))
            else:
                self.pen.rectangle([fx, y + h - 34, fx + 40, y + h - 12], fill=(38, 84, 160))
                self.pen.line([(fx, y + h - 34), (fx + 40, y + h - 12)], fill=(255, 255, 255), width=3)
                self.pen.line([(fx + 40, y + h - 34), (fx, y + h - 12)], fill=(255, 255, 255), width=3)

    def paint_courtroom(self, x, y, w, h):
        self.pen.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=(226, 226, 222))
        self.pen.polygon([(x + 14, y + 78), (x + w // 2, y + 34), (x + w - 14, y + 78)],
                         fill=(168, 168, 160))
        self.pen.ellipse([x + w // 2 - 9, y + 52, x + w // 2 + 9, y + 70], fill=(212, 160, 60))
        self.pen.rectangle([x + 22, y + 78, x + w - 22, y + 190], fill=(250, 250, 246))
        for i in range(3):
            colx = x + 34 + i * 44
            self.pen.rectangle([colx, y + 90, colx + 16, y + 178], fill=(150, 150, 146))
        self.pen.rectangle([x + 16, y + 190, x + w - 16, y + 200], fill=(120, 118, 112))
        self.pen.rectangle([x + 16, y + 200, x + w - 16, y + 208], fill=(96, 94, 90))
        self.pen.rectangle([x + 30, y + 214, x + 96, y + 228], fill=(122, 82, 46))
        self.pen.rectangle([x + 96, y + 220, x + 150, y + 228], fill=(92, 60, 32))
        self.pen.rectangle([x + w - 62, y + 214, x + w - 22, y + 228], fill=(122, 82, 46))

    # -- assemble ------------------------------------------------------
    def compose(self):
        self.masthead()
        left, top = 20, 126
        cw = (CANVAS_W - 2 * left - 16) // 2
        ch = 271
        for idx, story in enumerate(self.stories):
            row, col = divmod(idx, 2)
            self.card(story, left + col * (cw + 16), top + row * (ch + 16), cw, ch)
        self.footer()
        return self.sheet


def build_poster():
    items = [
        Story("TECHNOLOGY · UNITED STATES",
              "NVIDIA'S RECORD QUARTER, WITHOUT HUANG",
              "Revenue more than doubled to $115.8bn, profit hit $65.3bn, "
              "and $130bn is guided next. Huang said he would return if asked "
              "\u2014 the board says no. CFO Colette Kress leads for now.",
              (24, 110, 78), (18, 62, 52), "paint_chip"),
        Story("HEALTH · AMERICAS",
              "AMERICA LOSES ITS MEASLES-FREE LABEL",
              "After 26 years, PAHO says measles is spreading in the US "
              "without a break. Over 5,400 cases in 2026 \u2014 the worst in "
              "30+ years. Mexico and Bolivia lost the status too.",
              (178, 52, 44), (247, 226, 224), "paint_virus"),
        Story("DISASTER · RUSSIA",
              "19 DEAD AS ARMY PLANE CRASHES IN SIBERIA",
              "An An-12 transport came down near Kemerovo, killing all 19 "
              "aboard. The ministry blames a suspected technical fault. "
              "Some reports put the toll at 17.",
              (90, 96, 104), (196, 205, 214), "paint_crash"),
        Story("POLITICS · ISRAEL",
              "EISENKOT ALLY TAKES THE KNESSET CHAIR",
              "Matan Kahana beat Likud's Ofir Katz 66\u201352 to become "
              "speaker, ousting Amir Ohana. The win hands Eisenkot's bloc "
              "control of parliament's agenda.",
              (38, 84, 160), (214, 230, 244), "paint_parliament"),
        Story("ESPIONAGE · BRITAIN / USA",
              "SPY-SUSPECT OFFICER NOW IN US HANDS",
              "Lt Col Brandon Tyner, 41, was arrested near Gloucester on "
              "10 Nov on suspicion of spying for Russia. Britain has now "
              "passed him to US military custody.",
              (30, 58, 110), (20, 34, 58), "paint_dossier"),
        Story("COURTS · UNITED STATES",
              "27\u00bd YEARS FOR TRUMP MURDER PLOT",
              "Asif Merchant, 48, was jailed in Brooklyn for 330 months over "
              "an Iran-linked murder-for-hire scheme aimed at Donald Trump. "
              "Prosecutors had asked for life.",
              (122, 82, 46), (226, 226, 222), "paint_courtroom"),
    ]
    return Poster(stories=items).compose()


def save_poster(path):
    build_poster().save(path, format="PNG", optimize=True)


if __name__ == "__main__":
    import sys
    save_poster(sys.argv[1] if len(sys.argv) > 1 else "entry.png")
