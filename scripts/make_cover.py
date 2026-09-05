#!/usr/bin/env python3
"""Build a 3:4 Xiaohongshu cover from four pose-series frames."""

import os
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1440
GUTTER = 6
FONT_PATH = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"

SERIES = "/workspace/outputs/approved/series/20260905_teo_paddleboard_series"
FRAMES = [
    f"{SERIES}/08_sit_hug_knee.png",
    f"{SERIES}/05_hands_hair_wet.png",
    f"{SERIES}/04_sit_legs_water.png",
    f"{SERIES}/01_sit_board_lean_back.png",
]
OUT = f"{SERIES}/cover_a_grid.png"
OUT_HERO = f"{SERIES}/cover_b_hero.png"

TITLE = "被太阳晒化的一下午"
SUBTITLE = "Teo · 滴水湖桨板日记"
BADGE = "8图"


def fill_crop(img, size, bias=0.4):
    """Scale and crop so img exactly covers size; bias<0.5 keeps more of the top."""
    tw, th = size
    sw, sh = img.size
    scale = max(tw / sw, th / sh)
    nw, nh = round(sw * scale), round(sh * scale)
    img = img.resize((nw, nh), Image.LANCZOS)
    left = (nw - tw) // 2
    top = int((nh - th) * bias)
    return img.crop((left, top, left + tw, top + th))


def bold_text(draw, xy, text, font, fill, weight=3):
    """Fake bold: WenQuanYi ships no bold face."""
    x, y = xy
    for dx in range(-weight, weight + 1):
        for dy in range(-weight, weight + 1):
            if dx * dx + dy * dy <= weight * weight:
                draw.text((x + dx, y + dy), text, font=font, fill=fill)


def paste(canvas, path, origin, size, bias=0.4):
    with Image.open(path) as src:
        canvas.paste(fill_crop(src.convert("RGB"), size, bias), origin)


def decorate(canvas, bottom=H, scrim_h=460):
    """Shared scrim, title block, and count badge, anchored to `bottom`."""
    scrim = Image.new("RGBA", (W, scrim_h), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(scrim)
    for i in range(scrim_h):
        alpha = int(215 * (i / scrim_h) ** 1.7)
        sdraw.line([(0, i), (W, i)], fill=(8, 20, 26, alpha))
    canvas.paste(scrim, (0, bottom - scrim_h), scrim)

    draw = ImageDraw.Draw(canvas)
    title_font = ImageFont.truetype(FONT_PATH, 96, index=0)
    sub_font = ImageFont.truetype(FONT_PATH, 46, index=0)
    badge_font = ImageFont.truetype(FONT_PATH, 42, index=0)

    margin = 64
    title_h = draw.textbbox((0, 0), TITLE, font=title_font)[3]
    sub_h = draw.textbbox((0, 0), SUBTITLE, font=sub_font)[3]
    sub_y = bottom - margin - sub_h - 10
    title_y = sub_y - title_h - 46

    bold_text(draw, (margin, title_y), TITLE, title_font, "white", weight=3)

    # Yellow bar echoes the paddleboard deck colour.
    bar_y = sub_y + 8
    draw.rectangle([margin, bar_y, margin + 9, bar_y + sub_h + 6], fill=(255, 214, 51))
    draw.text((margin + 28, sub_y), SUBTITLE, font=sub_font, fill=(255, 235, 160))

    # Count badge drives the "see all" tap.
    bx0, by0 = W - 190, 44
    bw, bh = 130, 74
    draw.rounded_rectangle([bx0, by0, bx0 + bw, by0 + bh], radius=37, fill=(255, 214, 51))
    bbox = draw.textbbox((0, 0), BADGE, font=badge_font)
    draw.text(
        (bx0 + (bw - bbox[2]) / 2, by0 + (bh - bbox[3]) / 2 - 4),
        BADGE,
        font=badge_font,
        fill=(20, 32, 40),
    )


def grid_cover():
    """A — even 2x2 grid, reads as a set at thumbnail size."""
    canvas = Image.new("RGB", (W, H), "white")
    cell_w = (W - GUTTER) // 2
    cell_h = (H - GUTTER) // 2
    origins = [
        (0, 0),
        (cell_w + GUTTER, 0),
        (0, cell_h + GUTTER),
        (cell_w + GUTTER, cell_h + GUTTER),
    ]
    for path, origin in zip(FRAMES, origins):
        paste(canvas, path, origin, (cell_w, cell_h))
    decorate(canvas)
    canvas.save(OUT, "PNG", optimize=True)
    print(f"saved {OUT} {canvas.size}")


def hero_cover():
    """B — one large hero over a three-up strip, stronger single focal point."""
    canvas = Image.new("RGB", (W, H), "white")
    strip_h = 400
    hero_h = H - strip_h - GUTTER
    paste(canvas, FRAMES[1], (0, 0), (W, hero_h), bias=0.28)

    thumb_w = (W - GUTTER * 2) // 3
    for i, path in enumerate([FRAMES[0], FRAMES[2], FRAMES[3]]):
        x = i * (thumb_w + GUTTER)
        paste(canvas, path, (x, hero_h + GUTTER), (thumb_w, strip_h), bias=0.32)

    decorate(canvas, bottom=hero_h, scrim_h=430)
    canvas.save(OUT_HERO, "PNG", optimize=True)
    print(f"saved {OUT_HERO} {canvas.size}")


def main():
    for path in FRAMES:
        if not os.path.exists(path):
            sys.exit(f"missing frame: {path}")
    grid_cover()
    hero_cover()


if __name__ == "__main__":
    main()
