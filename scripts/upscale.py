#!/usr/bin/env python3
"""Batch 4x upscale with Real-ESRGAN's anime model.

Uses the conda Python that has torch and spandrel (system python3 does not):

  python scripts/upscale.py data/iPhone/IMG_1810.PNG
  python scripts/upscale.py data/iPhone
  python scripts/upscale.py data/iPhone --out outputs/upscaled
  python scripts/upscale.py data/iPhone/IMG_1810.PNG --is-replace

A file is written to <its folder>/upscaled_4x/. A directory's images are
written to <that folder>/upscaled_4x/. Pass --out to choose the folder.
Pass --is-replace to overwrite each source image instead.
"""
from __future__ import annotations

import argparse
import sys
import time
import urllib.request
from pathlib import Path

WEIGHTS_URL = (
    "https://github.com/xinntao/Real-ESRGAN/releases/download/"
    "v0.2.5.0/realesr-animevideov3.pth"
)
WEIGHTS_NAME = "realesr-animevideov3.pth"
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}


def die(msg: str, code: int = 2) -> None:
    print(f"upscale: {msg}", file=sys.stderr)
    raise SystemExit(code)


def weights_path() -> Path:
    return Path.home() / ".cache" / "realesrgan" / WEIGHTS_NAME


def ensure_weights() -> Path:
    path = weights_path()
    if path.is_file() and path.stat().st_size > 1_000_000:
        return path
    path.parent.mkdir(parents=True, exist_ok=True)
    print(f"downloading {WEIGHTS_NAME} …", flush=True)
    try:
        urllib.request.urlretrieve(WEIGHTS_URL, path)
    except Exception as exc:
        if path.exists():
            path.unlink()
        die(f"could not download weights: {exc}")
    return path


def pick_device(torch):
    if torch.cuda.is_available():
        return torch.device("cuda")
    mps = getattr(torch.backends, "mps", None)
    if mps is not None and mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


def load_model(torch, weights: Path):
    try:
        from spandrel import ModelLoader
    except ImportError:
        die("spandrel is not installed. Run: python -m pip install spandrel")
    device = pick_device(torch)
    model = ModelLoader().load_from_file(weights).eval().to(device)
    if model.scale != 4:
        die(f"expected a 4x model, got scale {model.scale}")
    return model, device


def collect(src: Path) -> list[Path]:
    if src.is_file():
        if src.suffix.lower() not in IMAGE_EXTS:
            die(f"not an image: {src}")
        return [src]
    if not src.is_dir():
        die(f"not found: {src}")
    files = [
        p
        for p in sorted(src.iterdir())
        if p.is_file() and p.suffix.lower() in IMAGE_EXTS
    ]
    if not files:
        die(f"no images in {src}")
    return files


def default_out(src: Path) -> Path:
    parent = src.parent if src.is_file() else src
    return parent / "upscaled_4x"


def to_tensor(torch, im):
    im = im.convert("RGB")
    width, height = im.size
    buf = bytearray(im.tobytes())
    tensor = torch.frombuffer(buf, dtype=torch.uint8).reshape(height, width, 3)
    return tensor.permute(2, 0, 1).unsqueeze(0).to(dtype=torch.float32).div(255)


def save_image(image, dest: Path, *, is_replace: bool) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    suffix = dest.suffix.lower()
    if not is_replace or suffix == ".png":
        image.save(dest, format="PNG", optimize=True)
        return
    if suffix in {".jpg", ".jpeg"}:
        image.save(dest, format="JPEG", quality=95, subsampling=0)
        return
    if suffix == ".webp":
        image.save(dest, format="WEBP", quality=95)
        return
    image.save(dest, format="BMP")


def upscale_one(torch, model, device, src: Path, dest: Path, *, is_replace: bool) -> None:
    from PIL import Image

    image = Image.open(src)
    tensor = to_tensor(torch, image).to(device)
    started = time.perf_counter()
    with torch.inference_mode():
        out = model(tensor)
    array = (
        out.squeeze(0)
        .clamp(0, 1)
        .mul(255)
        .byte()
        .permute(1, 2, 0)
        .cpu()
        .numpy()
    )
    # Pixels are already in memory, so overwriting src is safe.
    save_image(Image.fromarray(array), dest, is_replace=is_replace)
    elapsed = time.perf_counter() - started
    size_mb = dest.stat().st_size / (1024 * 1024)
    print(
        f"{src.name} {image.size[0]}x{image.size[1]} -> "
        f"{array.shape[1]}x{array.shape[0]}  {size_mb:.1f} MB  {elapsed:.1f}s",
        flush=True,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="放大一张图，或一个目录里的全部图片（动漫超分，4 倍）。"
    )
    parser.add_argument("input", type=Path, help="图片路径，或图片所在目录")
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="输出目录（默认：图片旁边或该目录下的 upscaled_4x/）",
    )
    parser.add_argument(
        "--is-replace",
        dest="is_replace",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="替换原始文件（默认不替换，写到 upscaled_4x/）",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        import torch
    except ImportError:
        die("torch is not installed. Use the conda Python: python scripts/upscale.py")

    if args.is_replace and args.out is not None:
        die("--is-replace 会覆盖原图，不要同时传 --out")

    src = args.input.expanduser().resolve()
    files = collect(src)
    out_dir = None if args.is_replace else (
        args.out.expanduser().resolve() if args.out else default_out(src)
    )
    weights = ensure_weights()
    torch.set_num_threads(8)
    model, device = load_model(torch, weights)
    where = "replace source" if args.is_replace else str(out_dir)
    print(f"device={device}  out={where}  images={len(files)}", flush=True)
    for path in files:
        dest = path if args.is_replace else out_dir / f"{path.stem}_4x.png"
        upscale_one(torch, model, device, path, dest, is_replace=args.is_replace)


if __name__ == "__main__":
    main()
