#!/usr/bin/env python3
"""Draw the front page for 27 November 2026 world news.

Writes entry.png (1024x1024) next to this file. Pure Pillow, no network:
the six stories are baked into STORIES below, so the output is fully
deterministic -- run it twice and the bytes match.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

PAPER = (246, 241, 231)
INK = (26, 26, 26)
NAVY = (22, 50, 79)
RED = (176, 42, 48)
GREY = (96, 96, 96)
CARD = (255, 253, 247)
LINE = (200, 192, 175)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# (kicker, headline, one-line summary)
STORIES = [
    ("STRAIT OF HORMUZ",
     "EXPLOSIONS HIT THREE TANKERS",
     "Iran reports blasts aboard three tankers in the Strait of Hormuz; "
     "crews safe, cause under investigation."),
    ("UKRAINE",
     "RUSSIAN STRIKES KILL 5; POWER OUT",
     "Russian strikes kill five and knock out power across Ukraine "
     "as winter sets in."),
    ("UNITED STATES",
     "THANKSGIVING STORM CUTS POWER TO 724,000",
     "A Thanksgiving storm lashes the US East Coast, leaving 724,000 "
     "homes without power."),
    ("UNITED KINGDOM",
     "UK NET MIGRATION AT 30-YEAR LOW",
     "Net migration falls to 77,000, the lowest in thirty years."),
    ("NORTH KOREA",
     "KIM ORDERS NUCLEAR PROGRAMME EXPANDED",
     "Kim Jong Un orders the nuclear programme expanded as tensions rise."),
    ("COLOMBIA",
     "ALL HOSTAGES FREED AFTER 16-HOUR SIEGE",
     "Every hostage walks free after a 16-hour siege at a supermarket."),
]


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_tanker(draw, x, y, scale=1.0):
    """A minimal tanker silhouette: hull, bridge block, two wave arcs."""
    hull = [(x, y), (x + 150 * scale, y), (x + 138 * scale, y + 22 * scale),
            (x + 12 * scale, y + 22 * scale)]
    draw.polygon(hull, fill=NAVY)
    draw.rectangle([x + 108 * scale, y - 26 * scale,
                    x + 138 * scale, y], fill=NAVY)
    draw.rectangle([x + 30 * scale, y - 12 * scale,
                    x + 96 * scale, y], fill=RED)
    for i, wx in enumerate((x, x + 52 * scale, x + 104 * scale)):
        draw.arc([wx, y + 30 * scale, wx + 48 * scale, y + 44 * scale],
                 180, 360, fill=NAVY, width=3)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead -------------------------------------------------------
    d.rectangle([0, 0, W, 124], fill=NAVY)
    d.text((34, 22), "THE WORLD", font=font(SERIF, 62), fill=(250, 247, 240))
    d.text((34, 92), "ONE DAY  •  SIX STORIES",
           font=font(SANS_BOLD, 17), fill=(214, 196, 160))
    d.text((W - 34, 30), "FRIDAY", font=font(SANS_BOLD, 26),
           fill=(250, 247, 240), anchor="ra")
    d.text((W - 34, 62), "27 NOVEMBER 2026", font=font(SANS_BOLD, 26),
           fill=(250, 247, 240), anchor="ra")
    d.rectangle([0, 124, W, 130], fill=RED)

    # --- lead story -----------------------------------------------------
    lx, ly, lw, lh = 34, 146, W - 68, 208
    d.rectangle([lx, ly, lx + lw, ly + lh], fill=CARD, outline=LINE, width=2)
    d.text((lx + 22, ly + 16), STORIES[0][0], font=font(SANS_BOLD, 18), fill=RED)
    head = wrap(d, STORIES[0][1], font(SERIF, 40), lw - 44)
    y = ly + 44
    for line in head[:2]:
        d.text((lx + 22, y), line, font=font(SERIF, 40), fill=INK)
        y += 48
    summary = wrap(d, STORIES[0][2], font(SANS, 21), 560)
    y = ly + 148
    for line in summary[:2]:
        d.text((lx + 22, y), line, font=font(SANS, 21), fill=(64, 64, 64))
        y += 28
    draw_tanker(d, lx + lw - 210, ly + 118, scale=1.0)

    # --- middle grid: stories 2-5 --------------------------------------
    gx, gy = 34, 372
    gw, gh, gut = 469, 160, 18
    for i, (kicker, headline, summary) in enumerate(STORIES[1:5]):
        cx = gx + (i % 2) * (gw + gut)
        cy = gy + (i // 2) * (gh + gut)
        d.rectangle([cx, cy, cx + gw, cy + gh], fill=CARD, outline=LINE, width=2)
        d.text((cx + 18, cy + 12), kicker, font=font(SANS_BOLD, 16), fill=RED)
        lines = wrap(d, headline, font(SERIF, 25), gw - 36)
        y = cy + 38
        for line in lines[:2]:
            d.text((cx + 18, y), line, font=font(SERIF, 25), fill=INK)
            y += 31
        s_lines = wrap(d, summary, font(SANS, 17), gw - 36)
        for line in s_lines[:2]:
            d.text((cx + 18, y), line, font=font(SANS, 17), fill=(64, 64, 64))
            y += 22
        assert y <= cy + gh - 6, f"story {i + 2} overflows its card"

    # --- last story, full width -----------------------------------------
    bx, by, bw, bh = 34, 724, W - 68, 150
    d.rectangle([bx, by, bx + bw, by + bh], fill=CARD, outline=LINE, width=2)
    d.text((bx + 22, by + 14), STORIES[5][0], font=font(SANS_BOLD, 18), fill=RED)
    d.text((bx + 22, by + 42), STORIES[5][1], font=font(SERIF, 34), fill=INK)
    d.text((bx + 22, by + 96), STORIES[5][2], font=font(SANS, 21),
           fill=(64, 64, 64))

    # --- footer ---------------------------------------------------------
    d.line([34, 906, W - 34, 906], fill=LINE, width=2)
    d.text((34, 922), "Compiled from wire reports filed 27 November 2026",
           font=font(SANS, 18), fill=GREY)
    d.text((W - 34, 922), "make.fun", font=font(SANS_BOLD, 18),
           fill=GREY, anchor="ra")
    recap = ("Tanker blasts in Hormuz  •  Strikes on Ukraine  •  "
             "Storm blackout in the US  •  UK migration low  •  "
             "Pyongyang expands nuclear drive  •  Colombia siege ends")
    y = 952
    for line in wrap(d, recap, font(SERIF_REG, 15), W - 68)[:2]:
        d.text((34, y), line, font=font(SERIF_REG, 15), fill=GREY)
        y += 21

    img.save(OUT, "PNG")
    print(f"wrote {OUT}: {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main()
