#!/usr/bin/env python3
"""
Helper CLI for ae-motion-replicator skill:
1. inspect-gif: Extract GIF frames, print timing metadata, and build a numbered contact sheet.
2. split: Split a transparent sprite sheet into individual decontaminated RGBA PNGs.
"""

import argparse
import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageSequence
from scipy.ndimage import distance_transform_edt


def cmd_inspect_gif(args):
    os.makedirs(args.out_dir, exist_ok=True)
    im = Image.open(args.gif_path)
    durations = []
    frames = []
    for i, frame in enumerate(ImageSequence.Iterator(im)):
        d = frame.info.get("duration", 0)
        durations.append(d)
        rgba = frame.convert("RGBA")
        frames.append(rgba)
        rgba.save(os.path.join(args.out_dir, f"frame_{i:03d}.png"))

    w, h = im.size
    n = len(frames)
    cols = min(8, n)
    rows = (n + cols - 1) // cols
    sheet = Image.new("RGBA", (cols * w, rows * h), (30, 30, 30, 255))
    draw = ImageDraw.Draw(sheet)

    for i, f in enumerate(frames):
        r, c = divmod(i, cols)
        sheet.paste(f, (c * w, r * h), f)
        draw.rectangle([c * w, r * h, c * w + 64, r * h + 22], fill=(0, 0, 0, 185))
        draw.text((c * w + 6, r * h + 5), f"#{i:02d}", fill=(255, 255, 0, 255))

    sheet_path = os.path.join(args.out_dir, "contact_sheet.png")
    sheet.save(sheet_path)

    print(f"Size: {w}x{h}")
    print(f"Total frames: {n}")
    print(f"Total duration (ms): {sum(durations)}")
    print(f"Unique durations (ms): {sorted(set(durations))}")
    print(f"Durations: {durations}")
    print(f"Contact sheet: {sheet_path}")


def cmd_split(args):
    os.makedirs(args.out_dir, exist_ok=True)
    im = Image.open(args.sheet_path).convert("RGBA")
    arr = np.array(im)
    alpha = arr[:, :, 3]

    col_has_fg = (alpha > args.alpha_thresh).any(axis=0)
    segments = []
    in_seg = False
    start = 0
    for x, val in enumerate(col_has_fg):
        if val and not in_seg:
            in_seg = True
            start = x
        elif not val and in_seg:
            in_seg = False
            if x - start >= args.min_width:
                segments.append((start, x))
    if in_seg and len(col_has_fg) - start >= args.min_width:
        segments.append((start, len(col_has_fg)))

    if not segments:
        print("No foreground segments found.", file=sys.stderr)
        sys.exit(1)

    names = [n.strip() for n in args.names.split(",")] if args.names else []
    pad = args.pad

    for i, (x0, x1) in enumerate(segments):
        sub_a = alpha[:, x0:x1]
        rows = np.where((sub_a > args.alpha_thresh).any(axis=1))[0]
        y0, y1 = int(rows[0]), int(rows[-1]) + 1

        cx0 = max(0, x0 - pad)
        cy0 = max(0, y0 - pad)
        cx1 = min(arr.shape[1], x1 + pad)
        cy1 = min(arr.shape[0], y1 + pad)
        sub = arr[cy0:cy1, cx0:cx1].copy()

        a = sub[:, :, 3]
        a[a <= 10] = 0

        opaque = a >= 235
        if opaque.any():
            _, indices = distance_transform_edt(~opaque, return_indices=True)
            nearest_rgb = sub[indices[0], indices[1], :3]
            edge = (a > 0) & (a < 235)
            sub[edge, :3] = nearest_rgb[edge]

        sub[a == 0, :3] = 0
        sub[:, :, 3] = a

        fname = names[i] if i < len(names) else f"part_{i:02d}"
        if not fname.endswith(".png"):
            fname += ".png"
        out_path = os.path.join(args.out_dir, fname)
        Image.fromarray(sub).save(out_path)
        print(f"Saved {fname}: {sub.shape[1]}x{sub.shape[0]} -> {out_path}")


def main():
    parser = argparse.ArgumentParser(description="AE Motion Replicator sprite & GIF helper")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_gif = sub.add_parser("inspect-gif", help="Inspect GIF and generate contact sheet")
    p_gif.add_argument("gif_path")
    p_gif.add_argument("out_dir")
    p_gif.set_defaults(func=cmd_inspect_gif)

    p_split = sub.add_parser("split", help="Split transparent sprite sheet into clean PNGs")
    p_split.add_argument("sheet_path")
    p_split.add_argument("out_dir")
    p_split.add_argument("--names", default="", help="Comma-separated output names")
    p_split.add_argument("--pad", type=int, default=6)
    p_split.add_argument("--alpha-thresh", type=int, default=5)
    p_split.add_argument("--min-width", type=int, default=10)
    p_split.set_defaults(func=cmd_split)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
