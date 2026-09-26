#!/usr/bin/env python3
"""Deterministic wallpaper geometry. Does not redraw the subject.

crop    — cut a screen region out of a device photo before generation.
compose — key the flat field off a subject cutout and paste it onto a
          background at a given scale and position. Never upscales.
place   — pad a master onto a wider or taller canvas at native pixels.

See .cursor/skills/wallpaper/SKILL.md.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageOps

def die(msg: str, code: int = 2) -> None:
    print(f"make_wallpaper: {msg}", file=sys.stderr)
    raise SystemExit(code)


def open_image(path: Path) -> Image.Image:
    if not path.is_file():
        die(f"image not found: {path}")
    img = Image.open(path)
    return ImageOps.exif_transpose(img)


def open_rgb(path: Path) -> Image.Image:
    return open_image(path).convert("RGB")


def parse_box(text: str) -> tuple[int, int, int, int]:
    parts = [p.strip() for p in text.split(",")]
    if len(parts) != 4:
        die("box must be left,top,right,bottom")
    try:
        box = tuple(int(p) for p in parts)
    except ValueError:
        die("box values must be integers")
    left, top, right, bottom = box
    if right <= left or bottom <= top:
        die(f"empty crop box: {box}")
    return left, top, right, bottom


def parse_aspect(text: str) -> tuple[float, float]:
    parts = text.split(":")
    if len(parts) != 2:
        die(f"aspect must be W:H, got {text!r}")
    try:
        w, h = float(parts[0]), float(parts[1])
    except ValueError:
        die(f"aspect must be W:H, got {text!r}")
    if w <= 0 or h <= 0:
        die(f"invalid aspect: {text}")
    return w, h


def parse_color(text: str) -> tuple[int, int, int]:
    parts = [p.strip() for p in text.split(",")]
    if len(parts) != 3:
        die("color must be R,G,B")
    try:
        rgb = tuple(int(p) for p in parts)
    except ValueError:
        die("color values must be integers")
    if any(c < 0 or c > 255 for c in rgb):
        die(f"color out of range: {rgb}")
    return rgb  # type: ignore[return-value]


def save(img: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, format="PNG")
    print(f"{path} {img.size[0]}x{img.size[1]}")


def cmd_crop(src: Path, box: tuple[int, int, int, int], out: Path) -> None:
    img = open_rgb(src)
    w, h = img.size
    left, top, right, bottom = box
    if left < 0 or top < 0 or right > w or bottom > h:
        die(f"box {box} outside image {w}x{h}")
    save(img.crop(box), out)


def corner_color(img: Image.Image) -> tuple[int, int, int]:
    """Color of the flat blank field. Warns when the four corners disagree."""
    w, h = img.size
    samples: list[tuple[int, int, int]] = []
    for x0, y0 in ((0, 0), (w - 8, 0), (0, h - 8), (w - 8, h - 8)):
        x0 = min(max(0, x0), w - 1)
        y0 = min(max(0, y0), h - 1)
        x1 = min(w, x0 + 8)
        y1 = min(h, y0 + 8)
        samples.extend(img.crop((x0, y0, x1, y1)).getdata())
    samples.sort(key=lambda p: p[0] + p[1] + p[2])
    mid = samples[len(samples) // 2]
    spread = max(max(c) - min(c) for c in zip(*samples))
    if spread > 18:
        print(
            f"make_wallpaper: corners differ by {spread}; blank field is not flat",
            file=sys.stderr,
        )
    return mid


def canvas_size(sw: int, sh: int, aspect: tuple[float, float]) -> tuple[int, int]:
    """Smallest canvas that contains the source and matches the aspect. Never shrinks."""
    aw, ah = aspect
    target = aw / ah
    if (sw / sh) <= target:
        width = max(sw, round(sh * target))
        height = sh
    else:
        width = sw
        height = max(sh, round(sw / target))
    if width < sw or height < sh:
        die(f"canvas {width}x{height} smaller than source {sw}x{sh}")
    return width, height


def fraction(name: str, value: float) -> float:
    if not 0.0 <= value <= 1.0:
        die(f"{name} must be between 0 and 1")
    return value


def has_cutout_alpha(img: Image.Image) -> bool:
    if img.mode != "RGBA":
        return False
    alpha = img.getchannel("A")
    lo, _hi = alpha.getextrema()
    if lo > 250:
        return False
    hist = alpha.histogram()
    clear = sum(hist[:250])
    return clear > img.size[0] * img.size[1] * 0.01


def key_out_field(img: Image.Image, tol: int) -> Image.Image:
    """Remove a flat key color that touches the image edges. Leave the subject."""
    if tol < 0 or tol > 255:
        die("key-tol must be between 0 and 255")
    rgb = img.convert("RGB")
    w, h = rgb.size
    key = corner_color(rgb)
    src = rgb.tobytes()
    n = w * h
    seen = bytearray(n)

    def is_close(i: int) -> bool:
        o = i * 3
        return max(
            abs(src[o] - key[0]),
            abs(src[o + 1] - key[1]),
            abs(src[o + 2] - key[2]),
        ) <= tol

    stack: list[int] = []
    for x in range(w):
        for y in (0, h - 1):
            i = y * w + x
            if is_close(i):
                stack.append(i)
    for y in range(1, h - 1):
        for x in (0, w - 1):
            i = y * w + x
            if is_close(i):
                stack.append(i)

    removed = 0
    while stack:
        i = stack.pop()
        if seen[i] or not is_close(i):
            continue
        seen[i] = 1
        removed += 1
        x = i % w
        y = i // w
        if x > 0:
            stack.append(i - 1)
        if x + 1 < w:
            stack.append(i + 1)
        if y > 0:
            stack.append(i - w)
        if y + 1 < h:
            stack.append(i + w)

    if removed < n * 0.01:
        die(
            "flat field not found. Regenerate the subject on one flat key color "
            "that touches all four edges."
        )

    alpha = bytearray(b"\xff" * n)
    for i, flagged in enumerate(seen):
        if flagged:
            alpha[i] = 0
    for i in range(n):
        if alpha[i] == 0:
            continue
        x = i % w
        y = i // w
        neighbor = False
        if x > 0 and seen[i - 1]:
            neighbor = True
        elif x + 1 < w and seen[i + 1]:
            neighbor = True
        elif y > 0 and seen[i - w]:
            neighbor = True
        elif y + 1 < h and seen[i + w]:
            neighbor = True
        if not neighbor or not is_close(i):
            continue
        o = i * 3
        dist = max(
            abs(src[o] - key[0]),
            abs(src[o + 1] - key[1]),
            abs(src[o + 2] - key[2]),
        )
        alpha[i] = min(255, int(255 * dist / max(tol, 1)))

    out = rgb.convert("RGBA")
    out.putalpha(Image.frombytes("L", (w, h), bytes(alpha)))
    opaque = sum(1 for a in alpha if a > 16)
    if opaque < n * 0.05:
        die(
            "key color removed almost the entire subject. "
            "Use a key color that is not present in the clothing, then pass it "
            "by regenerating on that flat field."
        )
    print(f"make_wallpaper: keyed {key[0]},{key[1]},{key[2]} tol={tol}")
    return out


def opaque_bbox(img: Image.Image) -> tuple[int, int, int, int]:
    mask = img.getchannel("A").point(lambda p: 255 if p > 16 else 0)
    box = mask.getbbox()
    if box is None:
        die("subject has no opaque pixels")
    return box


def fit_box(
    bw: int,
    bh: int,
    sw: int,
    sh: int,
    scale: float,
    cx: float,
    cy: float,
    safe_top: float,
    safe_bottom: float,
) -> tuple[int, int, int, int, bool]:
    """Return left, top, width, height, and whether scale was clamped to native pixels."""
    margin_x = round(bw * 0.02)
    avail_w = max(1, bw - 2 * margin_x)
    avail_h = max(1, bh - round(safe_top * bh) - round(safe_bottom * bh))
    target_w = max(1, round(bw * scale))
    clamped = False
    if target_w > sw:
        target_w = sw
        clamped = True
    target_h = max(1, round(sh * target_w / sw))
    if target_h > avail_h:
        target_h = avail_h
        target_w = max(1, round(sw * target_h / sh))
        clamped = True
    if target_w > avail_w:
        target_w = avail_w
        target_h = max(1, round(sh * target_w / sw))
        clamped = True
    left = round(cx * bw - target_w / 2)
    top = round(cy * bh - target_h / 2)
    min_left = margin_x
    max_left = max(min_left, bw - margin_x - target_w)
    min_top = round(safe_top * bh)
    max_top = max(min_top, bh - round(safe_bottom * bh) - target_h)
    left = min(max(left, min_left), max_left)
    top = min(max(top, min_top), max_top)
    return left, top, target_w, target_h, clamped


def prepare_subject(img: Image.Image, tol: int) -> Image.Image:
    rgba = img if has_cutout_alpha(img) else key_out_field(img, tol)
    return rgba.crop(opaque_bbox(rgba))


def paste_layer(
    canvas: Image.Image,
    layer: Image.Image,
    scale: float,
    cx: float,
    cy: float,
    safe_top: float,
    safe_bottom: float,
    label: str,
) -> None:
    bw, bh = canvas.size
    sw, sh = layer.size
    left, top, tw, th, clamped = fit_box(
        bw, bh, sw, sh, scale, cx, cy, safe_top, safe_bottom
    )
    resized = layer.resize((tw, th), Image.Resampling.LANCZOS) if (tw, th) != (sw, sh) else layer
    canvas.paste(resized, (left, top), resized)
    note = " adjusted" if clamped else ""
    print(
        f"make_wallpaper: {label} {tw}x{th} at {left},{top} "
        f"on {bw}x{bh} scale={tw / bw:.3f}{note}"
    )


def cmd_compose(
    subject: Path,
    background: Path,
    out: Path,
    scale: float,
    cx: float,
    cy: float,
    safe_top: float,
    safe_bottom: float,
    tol: int,
    prop: Path | None,
    prop_scale: float,
    prop_x: float,
    prop_y: float,
) -> None:
    """Paste the cutout onto the background. Position is the subject center."""
    fraction("scale", scale)
    fraction("x", cx)
    fraction("y", cy)
    fraction("safe-top", safe_top)
    fraction("safe-bottom", safe_bottom)
    if safe_top + safe_bottom >= 1:
        die("safe-top and safe-bottom leave no room for the subject")
    bg = open_rgb(background).convert("RGBA")
    sub = prepare_subject(open_image(subject), tol)
    if prop is not None:
        fraction("prop-scale", prop_scale)
        fraction("prop-x", prop_x)
        fraction("prop-y", prop_y)
        layer = prepare_subject(open_image(prop), tol)
        paste_layer(bg, layer, prop_scale, prop_x, prop_y, 0.0, 0.02, "prop")
    paste_layer(bg, sub, scale, cx, cy, safe_top, safe_bottom, "subject")
    save(bg.convert("RGB"), out)


def cmd_place(
    src: Path,
    out: Path,
    aspect: tuple[float, float],
    top_ratio: float,
    color: tuple[int, int, int] | None,
) -> None:
    """Paste the master at 1:1 onto a blank canvas. No scale, no crop."""
    if not 0.0 <= top_ratio <= 1.0:
        die("top-ratio must be between 0 and 1")
    img = open_rgb(src)
    sw, sh = img.size
    tw, th = canvas_size(sw, sh, aspect)
    fill = color if color is not None else corner_color(img)
    canvas = Image.new("RGB", (tw, th), fill)
    x = (tw - sw) // 2
    y = round((th - sh) * top_ratio)
    canvas.paste(img, (x, y))
    save(canvas, out)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Pad or crop wallpaper files. Does not generate images.")
    sub = p.add_subparsers(dest="cmd", required=True)

    crop = sub.add_parser("crop", help="Cut a rectangle out of a device photo")
    crop.add_argument("--src", type=Path, required=True)
    crop.add_argument("--box", required=True, help="left,top,right,bottom in source pixels")
    crop.add_argument("--out", type=Path, required=True)

    compose = sub.add_parser(
        "compose",
        help="Paste a cutout onto a background. Never upscales the subject.",
    )
    compose.add_argument("--subject", type=Path, required=True)
    compose.add_argument("--background", type=Path, required=True)
    compose.add_argument("--out", type=Path, required=True)
    compose.add_argument("--scale", type=float, default=0.82, help="Subject width / background width")
    compose.add_argument("--x", type=float, default=0.50, help="Subject center, 0–1 across")
    compose.add_argument("--y", type=float, default=0.61, help="Subject center, 0–1 down")
    compose.add_argument("--safe-top", type=float, default=0.24)
    compose.add_argument("--safe-bottom", type=float, default=0.08)
    compose.add_argument("--key-tol", type=int, default=40, help="Key-color distance removed from the edges")
    compose.add_argument("--prop", type=Path, default=None, help="Optional detached object cutout")
    compose.add_argument("--prop-scale", type=float, default=0.18)
    compose.add_argument("--prop-x", type=float, default=0.18)
    compose.add_argument("--prop-y", type=float, default=0.88)

    place = sub.add_parser("place", help="Pad onto an aspect at native resolution. Never scales.")
    place.add_argument("--src", type=Path, required=True)
    place.add_argument("--out", type=Path, required=True)
    place.add_argument("--aspect", required=True, help="9:19.5, 4:3, or 16:9")
    place.add_argument("--top-ratio", type=float, default=0.70, help="Share of extra pixels placed above the master")
    place.add_argument("--color", default=None, help="R,G,B blank fill. Default: sampled corners")
    return p


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    if args.cmd == "crop":
        cmd_crop(args.src, parse_box(args.box), args.out)
    elif args.cmd == "compose":
        cmd_compose(
            args.subject,
            args.background,
            args.out,
            args.scale,
            args.x,
            args.y,
            args.safe_top,
            args.safe_bottom,
            args.key_tol,
            args.prop,
            args.prop_scale,
            args.prop_x,
            args.prop_y,
        )
    elif args.cmd == "place":
        color = parse_color(args.color) if args.color else None
        cmd_place(args.src, args.out, parse_aspect(args.aspect), args.top_ratio, color)
    else:
        die(f"unknown command {args.cmd}")


if __name__ == "__main__":
    main()
