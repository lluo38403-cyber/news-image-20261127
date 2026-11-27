"""Draw the news-image-20261127 entry: a one-page newspaper front page.

Deterministic, no network. Output: 1024x1024 PNG, under 1 MiB.
Stories are as reported on 27 November 2026 (Qatar Tribune world page,
NDTV, The Economic Times): explosions on three tankers in the Strait of
Hormuz; Russian strikes kill 5 in Ukraine and cut power; a Thanksgiving
storm cancels ~400 US flights and leaves 724,000 without power; UK net
migration falls to a near 30-year low; Kim Jong Un orders North Korea's
nuclear programme expanded; all hostages freed after a 16-hour
supermarket siege in Colombia.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (250, 248, 242)
INK = (18, 22, 32)
NAVY = (16, 42, 92)
RED = (178, 34, 34)
TEAL = (0, 110, 105)
GOLD = (176, 124, 0)
GREY = (90, 92, 100)
LINE = (200, 196, 188)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= width:
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

# Header band
d.rectangle([0, 0, W, 168], fill=NAVY)
d.text((48, 26), "FRIDAY  27  NOVEMBER  2026", font=font(SANS_B, 44), fill=(255, 255, 255))
d.text((48, 88), "THE WORLD IN ONE DAY  —  SIX STORIES THAT DEFINED THE DAY",
       font=font(SANS_B, 24), fill=(200, 214, 235))
d.rectangle([0, 168, W, 176], fill=RED)

# Sub-line
d.text((48, 196), "World news  •  Friday 27 November 2026",
       font=font(SANS_B, 26), fill=INK)
d.text((48, 232), "Gulf  •  Ukraine  •  US storm  •  UK migration  •  North Korea  •  Colombia",
       font=font(SANS, 22), fill=GREY)

stories = [
    ("MIDDLE EAST  •  STRAIT OF HORMUZ", RED, "EXPLOSIONS HIT THREE TANKERS",
     "Iran reports explosions on three tankers in the Strait of Hormuz as Gulf tensions rise."),
    ("EUROPE  •  UKRAINE", TEAL, "RUSSIAN STRIKES KILL 5; POWER OUT",
     "Russian strikes kill five in Ukraine and knock out power; Zelensky warns a new mass strike is coming."),
    ("UNITED STATES", NAVY, "THANKSGIVING STORM CUTS POWER TO 724,000",
     "A storm disrupts Thanksgiving on the US East Coast: about 400 flights cancelled, 724,000 homes dark."),
    ("UNITED KINGDOM", GOLD, "UK NET MIGRATION AT 30-YEAR LOW",
     "Net migration falls to 77,000, the lowest since 1997 outside the pandemic, after tougher rules."),
    ("ASIA  •  NORTH KOREA", RED, "KIM ORDERS NUCLEAR PROGRAMME EXPANDED",
     "North Korea's Kim Jong Un calls for an expansion of the country's nuclear programme."),
    ("LATIN AMERICA  •  COLOMBIA", TEAL, "ALL HOSTAGES FREED AFTER 16-HOUR SIEGE",
     "All hostages are freed after a 16-hour supermarket siege in Colombia."),
]

x0, y0 = 48, 288
cw, ch, gap = 464, 208, 0
gx, gy = 32, 16
for i, (tag, color, head, body) in enumerate(stories):
    col, row = i % 2, i // 2
    x = x0 + col * (cw + gx)
    y = y0 + row * (ch + gy)
    d.rectangle([x, y, x + cw, y + ch], outline=LINE, width=2, fill=(255, 255, 255))
    d.rectangle([x, y, x + cw, y + 8], fill=color)
    d.text((x + 20, y + 22), tag, font=font(SANS_B, 20), fill=color)
    lines = wrap(d, head, font(SANS_B, 26), cw - 40)
    yy = y + 52
    for ln in lines[:3]:
        d.text((x + 20, yy), ln, font=font(SANS_B, 26), fill=INK)
        yy += 31
    blines = wrap(d, body, font(SANS, 19), cw - 40)
    for ln in blines[:3]:
        d.text((x + 20, yy + 4), ln, font=font(SANS, 19), fill=(52, 56, 68))
        yy += 24

# Footer
d.rectangle([0, 984, W, H], fill=NAVY)
d.text((48, 995), "27 NOVEMBER 2026  •  HORMUZ  •  UKRAINE  •  US STORM  •  KIM  •  COLOMBIA",
       font=font(SANS_B, 20), fill=(255, 255, 255))

img.save("/home/hatch/workspace/makefun/news-image-20261127-entry/entry.png")
print("saved")
