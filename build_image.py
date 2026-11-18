#!/usr/bin/env python3
"""Build the 1024x1024 front-page image for make.fun bounty
'Sum up 18 November's world news in one image' (news-image-20261118).
Headlines verified 2026-11-18 ~12:20 UTC from oneturn.news, horizonapp.link,
tehworldnews.com, nexuseuropa.eu and make.fun submissions. Run: python3 build_image.py
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (250, 248, 240)
INK = (18, 18, 18)
RED = (178, 34, 34)
NAVY = (16, 42, 90)
TEAL = (0, 110, 110)
GOLD = (176, 132, 0)
GREY = (90, 90, 90)
LIGHT = (232, 228, 218)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def font(p, s):
    return ImageFont.truetype(p, s)

def wrap(draw, text, f, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=f) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)
d.rectangle([0, 0, W, 10], fill=RED)
# Masthead
d.text((512, 58), "THE WORLD TODAY", font=font(SERIF_B, 62), fill=INK, anchor="ma")
d.text((512, 122), "WEDNESDAY  •  18 NOVEMBER 2026  •  ONE DAY, ONE PAGE", font=font(SANS_B, 20), fill=GREY, anchor="ma")
d.line([36, 152, 988, 152], fill=INK, width=3)
d.line([36, 158, 988, 158], fill=INK, width=1)

# Lead story
y = 178
d.rectangle([36, y, 988, y + 218], fill=(255, 255, 255), outline=NAVY, width=3)
d.rectangle([36, y, 988, y + 44], fill=NAVY)
d.text((56, y + 22), "LEAD  •  THE GULF", font=font(SANS_B, 22), fill=(255, 255, 255), anchor="lm")
d.text((56, y + 82), "GULF ON EDGE", font=font(SERIF_B, 58), fill=RED, anchor="la")
lines = wrap(d, "US strikes a missile site on Iran's Qeshm Island — Iran fires drones at US bases in Bahrain and Kuwait.", font(SANS, 27), 920)
yy = y + 148
for ln in lines:
    d.text((56, yy), ln, font=font(SANS, 27), fill=INK, anchor="la")
    yy += 34

# Two-column stories
stories = [
    ("UKRAINE", RED, "Kerch Bridge partly collapses after a second day of Ukrainian drone and missile strikes on the link to Crimea."),
    ("SUMMIT", NAVY, "Trump, Xi and Putin to meet in Shenzhen tomorrow — the first trilateral summit — as APEC opens in China."),
    ("USA", TEAL, "Democrat Mary Peltola wins Alaska's Senate seat; Democrats reach 56 seats in the US Senate."),
    ("HEALTH", RED, "Ebola in DR Congo more than doubles: 11,000+ cases, 5,400 deaths. Three in four infected children under 5 die."),
    ("DISASTER", NAVY, "Russian military plane crashes in Siberia, killing all 19 on board. Category 5 Cyclone Xavier hits the Cook Islands."),
    ("AT HOME & MARKETS", GOLD, "US loses measles-free status after 26 years. Cold threatens Gaza's tent camps. Nvidia revenue $115.8bn; Dow falls ~850."),
]
x0, x1 = 36, 522
col_w = 466
y = 424
for i, (kicker, color, body) in enumerate(stories):
    x = x0 if i % 2 == 0 else x1
    if i % 2 == 0 and i > 0:
        y += 178
    d.rectangle([x, y, x + col_w, y + 162], fill=(255, 255, 255), outline=(200, 196, 186), width=2)
    d.rectangle([x, y, x + 8, y + 162], fill=color)
    d.text((x + 24, y + 16), kicker, font=font(SANS_B, 21), fill=color, anchor="la")
    ls = wrap(d, body, font(SANS, 23), col_w - 48)
    yy = y + 48
    for ln in ls[:4]:
        d.text((x + 24, yy), ln, font=font(SANS, 23), fill=INK, anchor="la")
        yy += 29

# Footer
d.line([36, 972, 988, 972], fill=INK, width=2)
d.text((512, 992), "7 stories, 5 continents  •  Sources: wire & news roundups, 18 Nov 2026", font=font(SANS, 19), fill=GREY, anchor="ma")
img.save("/home/hatch/workspace/makefun-news-18nov/entry.png", "PNG", optimize=True)
print("saved entry.png", img.size)
