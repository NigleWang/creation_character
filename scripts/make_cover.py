#!/usr/bin/env python3
"""Xiaohongshu 3:4 cover collage — deterministic Pillow composite, never GenerateImage.

See docs/joint_imgs.md and .cursor/skills/cover-collage/SKILL.md.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

W, H = 1080, 1440
GUTTER = 6
CANVAS_BG = (255, 255, 255)
SCRIM_RGB = (8, 20, 26)
DEFAULT_ACCENT = (255, 214, 51)

FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/Library/Fonts/Arial Unicode.ttf",
]

LAYOUTS = ("grid_2x2", "hero_3", "hero_side")


def die(msg: str, code: int = 2) -> None:
    print(f"make_cover: {msg}", file=sys.stderr)
    raise SystemExit(code)


def find_font_path() -> str:
    for p in FONT_CANDIDATES:
        if Path(p).is_file():
            return p
    die(
        "no Chinese font found. Install wqy-microhei or use PingFang/Hiragino. "
        "Tried: " + ", ".join(FONT_CANDIDATES)
    )
    raise AssertionError


def load_font(size: int) -> ImageFont.FreeTypeFont:
    path = find_font_path()
    last_err: Exception | None = None
    for index in (0, 1, 2):
        try:
            return ImageFont.truetype(path, size=size, index=index)
        except OSError as e:
            last_err = e
            continue
    try:
        return ImageFont.truetype(path, size=size)
    except OSError as e:
        die(f"failed to load font {path}: {e or last_err}")
        raise AssertionError


def open_rgb(path: Path) -> Image.Image:
    if not path.is_file():
        die(f"frame not found: {path}")
    img = Image.open(path)
    img = ImageOps.exif_transpose(img)
    return img.convert("RGB")


def fill_crop(img: Image.Image, size: tuple[int, int], bias: float = 0.4) -> Image.Image:
    """Scale and crop so img exactly covers size. bias<0.5 keeps more of the top."""
    tw, th = size
    sw, sh = img.size
    if sw < 1 or sh < 1 or tw < 1 or th < 1:
        die(f"invalid size src={img.size} target={size}")
    scale = max(tw / sw, th / sh)
    nw, nh = max(1, round(sw * scale)), max(1, round(sh * scale))
    img = img.resize((nw, nh), Image.LANCZOS)
    left = max(0, (nw - tw) // 2)
    top = int((nh - th) * bias)
    top = max(0, min(top, max(0, nh - th)))
    return img.crop((left, top, left + tw, top + th))


def parse_accent(value) -> tuple[int, int, int]:
    if value in (None, "", "auto"):
        return DEFAULT_ACCENT
    if isinstance(value, (list, tuple)) and len(value) == 3:
        return tuple(int(c) for c in value)  # type: ignore[return-value]
    if isinstance(value, str) and "," in value:
        parts = [int(p.strip()) for p in value.split(",")]
        if len(parts) != 3:
            die(f"accent must be R,G,B got {value!r}")
        return parts[0], parts[1], parts[2]
    die(f"bad accent: {value!r}")
    raise AssertionError


def pick_accent(img: Image.Image) -> tuple[int, int, int]:
    small = img.resize((48, 48), Image.BILINEAR)
    best = DEFAULT_ACCENT
    best_score = 0.0
    for r, g, b in small.getdata():
        mx, mn = max(r, g, b), min(r, g, b)
        if mx < 50 or mn > 230:
            continue
        sat = (mx - mn) / mx
        val = mx / 255.0
        score = sat * val
        if score > best_score:
            best_score = score
            best = (int(r), int(g), int(b))
    return best if best_score > 0.15 else DEFAULT_ACCENT


def lighten(rgb: tuple[int, int, int], t: float = 0.55) -> tuple[int, int, int]:
    return tuple(int(c + (255 - c) * t) for c in rgb)  # type: ignore[return-value]


def cells_grid_2x2() -> list[tuple[int, int, int, int]]:
    cw = (W - GUTTER) // 2
    ch = (H - GUTTER) // 2
    return [
        (0, 0, cw, ch),
        (cw + GUTTER, 0, W - cw - GUTTER, ch),
        (0, ch + GUTTER, cw, H - ch - GUTTER),
        (cw + GUTTER, ch + GUTTER, W - cw - GUTTER, H - ch - GUTTER),
    ]


def cells_hero_strip(n_strip: int, strip_h: int = 400) -> list[tuple[int, int, int, int]]:
    n_strip = max(1, n_strip)
    hero_h = H - strip_h - GUTTER
    cells = [(0, 0, W, hero_h)]
    y = hero_h + GUTTER
    cell_w = (W - (n_strip - 1) * GUTTER) // n_strip
    x = 0
    for i in range(n_strip):
        if i < n_strip - 1:
            cells.append((x, y, cell_w, strip_h))
            x += cell_w + GUTTER
        else:
            cells.append((x, y, W - x, strip_h))
    return cells


def cells_hero_side(n_right: int) -> list[tuple[int, int, int, int]]:
    n_right = max(1, n_right)
    hero_w = (W - GUTTER) * 2 // 3
    right_w = W - hero_w - GUTTER
    cells = [(0, 0, hero_w, H)]
    x = hero_w + GUTTER
    cell_h = (H - (n_right - 1) * GUTTER) // n_right
    y = 0
    for i in range(n_right):
        if i < n_right - 1:
            cells.append((x, y, right_w, cell_h))
            y += cell_h + GUTTER
        else:
            cells.append((x, y, right_w, H - y))
    return cells


def layout_cells(layout: str, n_frames: int) -> list[tuple[int, int, int, int]]:
    if layout == "grid_2x2":
        if n_frames < 4:
            die("layout grid_2x2 needs 4 frames")
        return cells_grid_2x2()
    if layout == "hero_3":
        if n_frames < 3:
            die("layout hero_3 needs at least 3 frames")
        n_strip = min(3, n_frames - 1)
        return cells_hero_strip(n_strip)
    if layout == "hero_side":
        if n_frames < 2:
            die("layout hero_side needs at least 2 frames")
        n_right = min(3, n_frames - 1)
        return cells_hero_side(n_right)
    die(f"unknown layout {layout!r}; use {LAYOUTS}")
    raise AssertionError


def default_biases(layout: str, n_cells: int) -> list[float]:
    if layout == "grid_2x2":
        return [0.4] * n_cells
    return [0.28] + [0.32] * (n_cells - 1)


def make_scrim(width: int, height: int, max_alpha: int = 215, power: float = 1.7) -> Image.Image:
    scrim = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    px = scrim.load()
    denom = max(height - 1, 1)
    for i in range(height):
        a = int(((i / denom) ** power) * max_alpha)
        row = (*SCRIM_RGB, a)
        for x in range(width):
            px[x, i] = row
    return scrim


def draw_bold_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    font: ImageFont.FreeTypeFont,
    fill,
    weight: int = 3,
) -> None:
    x, y = xy
    for dx in range(-weight, weight + 1):
        for dy in range(-weight, weight + 1):
            if dx * dx + dy * dy <= weight * weight:
                draw.text((x + dx, y + dy), text, font=font, fill=fill)


def text_size(font: ImageFont.FreeTypeFont, text: str, weight: int = 0) -> tuple[int, int]:
    dummy = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    l, t, r, b = dummy.textbbox((0, 0), text, font=font)
    return (r - l + 2 * weight, b - t + 2 * weight)


def fit_title_font(text: str, max_width: int, start: int = 96) -> ImageFont.FreeTypeFont:
    size = start
    while size >= 40:
        font = load_font(size)
        tw, _ = text_size(font, text, weight=3)
        if tw <= max_width:
            return font
        size -= 4
    return load_font(40)


def decorate(
    canvas: Image.Image,
    *,
    title: str,
    subtitle: str,
    badge: str,
    accent: tuple[int, int, int],
    host: tuple[int, int, int, int],
    scrim_ratio: float,
    max_scrim: int,
) -> Image.Image:
    """Text layer anchored to the host cell's bottom edge, never the wrong strip.

    Default covers skip this entirely (no title / subtitle / badge).
    """
    if not title and not subtitle and not badge:
        return canvas
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    hx, hy, hw, hh = host
    bottom = hy + hh
    if title or subtitle:
        scrim_h = max(120, min(int(hh * scrim_ratio), max_scrim, hh))
        scrim = make_scrim(hw, scrim_h)
        overlay.paste(scrim, (hx, bottom - scrim_h), scrim)
    draw = ImageDraw.Draw(overlay)

    margin = 40
    max_text_w = hw - margin * 2
    pale = lighten(accent, 0.58)

    sub_h = 0
    sub_font = load_font(46)
    if subtitle:
        sub_h = text_size(sub_font, subtitle, weight=1)[1]
    sub_y = bottom - 36 - sub_h

    title_font = fit_title_font(title, max_text_w) if title else load_font(96)
    title_h = text_size(title_font, title, weight=3)[1] if title else 0
    title_y = (sub_y - 14 - title_h) if subtitle else (bottom - 48 - title_h)

    tx = hx + margin
    if title:
        draw_bold_text(draw, (tx, title_y), title, title_font, fill=(255, 255, 255, 255), weight=3)
    if subtitle:
        bar_w = 9
        bar_x = tx
        bar_y = sub_y + 4
        draw.rectangle([bar_x, bar_y, bar_x + bar_w, bar_y + sub_h - 4], fill=(*accent, 255))
        draw_bold_text(
            draw,
            (bar_x + bar_w + 12, sub_y),
            subtitle,
            sub_font,
            fill=(*pale, 255),
            weight=1,
        )

    if badge:
        badge_font = load_font(28)
        bw, bh = text_size(badge_font, badge, weight=1)
        pad_x, pad_y = 16, 8
        box_w, box_h = bw + pad_x * 2, bh + pad_y * 2
        bx = W - 28 - box_w
        by = 28
        box = [bx, by, bx + box_w, by + box_h]
        try:
            draw.rounded_rectangle(box, radius=12, fill=(*accent, 235))
        except Exception:
            draw.rectangle(box, fill=(*accent, 235))
        tw, th = text_size(badge_font, badge)
        draw_bold_text(
            draw,
            (bx + (box_w - tw) // 2, by + (box_h - th) // 2 - 1),
            badge,
            badge_font,
            fill=(20, 20, 20, 255),
            weight=1,
        )

    out = Image.alpha_composite(canvas.convert("RGBA"), overlay)
    return out.convert("RGB")


def parse_biases(raw, n: int, layout: str) -> list[float]:
    if raw in (None, "", []):
        return default_biases(layout, n)
    if isinstance(raw, (int, float)):
        return [float(raw)] * n
    if isinstance(raw, str):
        vals = [float(x.strip()) for x in raw.split(",") if x.strip()]
    elif isinstance(raw, (list, tuple)):
        vals = [float(x) for x in raw]
    else:
        die(f"bad crop_bias: {raw!r}")
        raise AssertionError
    if len(vals) == 1:
        return vals * n
    if len(vals) < n:
        vals = vals + [vals[-1]] * (n - len(vals))
    return vals[:n]


def compose(cfg: dict) -> Image.Image:
    layout = cfg["layout"]
    if layout not in LAYOUTS:
        die(f"layout must be one of {LAYOUTS}")
    frames = [Path(p) for p in cfg["frames"]]
    if not frames:
        die("frames is empty")
    cells = layout_cells(layout, len(frames))
    n = len(cells)
    images = [open_rgb(p) for p in frames[:n]]
    biases = parse_biases(cfg.get("crop_bias"), n, layout)

    canvas = Image.new("RGB", (W, H), CANVAS_BG)
    for img, (x, y, w, h), bias in zip(images, cells, biases):
        canvas.paste(fill_crop(img, (w, h), bias=bias), (x, y))

    title = str(cfg.get("title") or "").strip()
    subtitle = str(cfg.get("subtitle") or "").strip()
    badge = str(cfg.get("badge") or "").strip()
    if not title and not subtitle and not badge:
        return canvas

    accent_raw = cfg.get("accent", "auto")
    if accent_raw in (None, "", "auto"):
        accent = pick_accent(images[0])
    else:
        accent = parse_accent(accent_raw)

    host = (0, 0, W, H) if layout == "grid_2x2" else cells[0]
    scrim_ratio, max_scrim = (0.22, 320) if layout == "grid_2x2" else (0.42, 480)

    return decorate(
        canvas,
        title=title,
        subtitle=subtitle,
        badge=badge,
        accent=accent,
        host=host,
        scrim_ratio=scrim_ratio,
        max_scrim=max_scrim,
    )


def load_config(path: Path | None, args: argparse.Namespace) -> dict:
    cfg: dict = {}
    if path:
        if not path.is_file():
            die(f"config not found: {path}")
        cfg = json.loads(path.read_text(encoding="utf-8"))
    if args.frames:
        cfg["frames"] = args.frames
    if args.layout:
        cfg["layout"] = args.layout
    if args.title is not None:
        cfg["title"] = args.title
    if args.subtitle is not None:
        cfg["subtitle"] = args.subtitle
    if args.badge is not None:
        cfg["badge"] = args.badge
    if args.accent:
        cfg["accent"] = args.accent
    if args.crop_bias:
        cfg["crop_bias"] = args.crop_bias
    if args.out:
        cfg["out"] = args.out
    for key in ("frames", "layout", "out"):
        if not cfg.get(key):
            die(f"missing required field: {key}")
    return cfg


def main() -> None:
    p = argparse.ArgumentParser(description="Compose a 1080x1440 Xiaohongshu cover collage.")
    p.add_argument("--config", type=Path, help="JSON config (fields may be overridden by flags)")
    p.add_argument("--frames", nargs="+", help="Ordered source image paths")
    p.add_argument("--layout", choices=LAYOUTS)
    p.add_argument("--title", default=None)
    p.add_argument("--subtitle", default=None)
    p.add_argument("--badge", default=None)
    p.add_argument("--accent", default=None, help="R,G,B or auto")
    p.add_argument("--crop-bias", dest="crop_bias", default=None, help="one float or comma list")
    p.add_argument("--out", type=Path, help="Output PNG path")
    args = p.parse_args()
    cfg = load_config(args.config, args)
    out = Path(cfg["out"])
    out.parent.mkdir(parents=True, exist_ok=True)
    img = compose(cfg)
    img.save(out, format="PNG", optimize=True)
    print(f"wrote {out} ({img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
    main()
