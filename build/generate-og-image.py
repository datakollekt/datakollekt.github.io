#!/usr/bin/env python3
"""Generate the 1200x630 social preview card (og-image.png).

Brand-matched to the site: dark ground, cyan accent, wordmark, hero tagline.
Requires Pillow (`pip install Pillow`) and macOS system fonts (adjust FONT_DIR
on other platforms).

Usage:  python build/generate-og-image.py [output.png]   # default: og-image.png
"""
import sys
from PIL import Image, ImageDraw, ImageFont

OUT = sys.argv[1] if len(sys.argv) > 1 else "og-image.png"

W, H = 1200, 630
BG    = (10, 12, 16)     # #0a0c10  site background
CYAN  = (34, 211, 238)   # #22d3ee  accent
WHITE = (233, 236, 240)
DIM   = (120, 130, 140)
GRID  = (26, 30, 36)

FONT_DIR = "/System/Library/Fonts/Supplemental/"
bold = lambda s: ImageFont.truetype(FONT_DIR + "Arial Bold.ttf", s)
mono = lambda s: ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", s)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# subtle dot grid
for y in range(40, H, 26):
    for x in range(40, W, 26):
        d.point((x, y), fill=GRID)

PAD = 80

# wordmark: cyan diamond + DataKollekt AB
cx, cy, r = PAD + 12, PAD + 12, 13
d.polygon([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)], fill=CYAN)
d.text((PAD + 38, PAD - 3), "DataKollekt", font=bold(30), fill=WHITE)
wm_w = d.textlength("DataKollekt", font=bold(30))
d.text((PAD + 38 + wm_w + 8, PAD + 4), "AB", font=mono(18), fill=DIM)

# headline (cyan on "run in production", matching the hero)
hf, lh, y = bold(72), 84, 232
d.text((PAD, y), "Data platforms and", font=hf, fill=WHITE); y += lh
seg = "AI agents that "
d.text((PAD, y), seg, font=hf, fill=WHITE)
d.text((PAD + d.textlength(seg, font=hf), y), "run in", font=hf, fill=CYAN); y += lh
d.text((PAD, y), "production.", font=hf, fill=CYAN)

# accent divider + footer meta
d.rectangle([PAD, 508, PAD + 54, 512], fill=CYAN)
d.text((PAD, 536), "POOYA SHAHRYARI", font=mono(22), fill=WHITE)
d.text((PAD, 570), "STOCKHOLM, SWEDEN   ·   DATA & AI-AGENT ENGINEERING", font=mono(18), fill=DIM)
url = "datakollekt.se"
d.text((W - PAD - d.textlength(url, font=mono(22)), 570), url, font=mono(22), fill=CYAN)

img.save(OUT, "PNG")
print("saved", OUT, img.size)
