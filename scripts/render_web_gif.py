#!/usr/bin/env python3
"""
Deterministic frame-by-frame HTML/GSAP -> GIF/MP4 renderer using Playwright + ffmpeg.
The target HTML should expose `window.__seek(timeInSeconds)` (e.g., `tl.seek(t)`).
"""

import argparse
import os
import shutil
import subprocess
import tempfile
from playwright.sync_api import sync_playwright


def main():
    parser = argparse.ArgumentParser(description="Render HTML/GSAP animation to GIF via Playwright + ffmpeg")
    parser.add_argument("html_path", help="Path to local HTML file")
    parser.add_argument("out_path", help="Output .gif or .mp4 path")
    parser.add_argument("--duration", type=float, required=True, help="Total duration in seconds")
    parser.add_argument("--fps", type=int, default=25, help="Frames per second (default: 25)")
    parser.add_argument("--width", type=int, default=480, help="Viewport width (default: 480)")
    parser.add_argument("--height", type=int, default=480, help="Viewport height (default: 480)")
    parser.add_argument("--transparent", action="store_true", help="Capture transparent background (PNG alpha)")
    args = parser.parse_args()

    html_abs = os.path.abspath(args.html_path)
    out_abs = os.path.abspath(args.out_path)
    os.makedirs(os.path.dirname(out_abs) or ".", exist_ok=True)

    total_frames = max(1, int(round(args.duration * args.fps)))
    tmp_dir = tempfile.mkdtemp(prefix="web_motion_frames_")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": args.width, "height": args.height})
            page.goto(f"file://{html_abs}", wait_until="networkidle")

            for i in range(total_frames):
                t = i / args.fps
                page.evaluate(f"if (window.__seek) window.__seek({t:.6f});")
                page.wait_for_timeout(15)
                frame_file = os.path.join(tmp_dir, f"frame_{i:04d}.png")
                page.screenshot(path=frame_file, omit_background=args.transparent)

            browser.close()

        pattern = os.path.join(tmp_dir, "frame_%04d.png")
        if out_abs.lower().endswith(".gif"):
            vf = (
                f"fps={args.fps},split[s0][s1];"
                f"[s0]palettegen=max_colors=128:reserve_transparent={'1' if args.transparent else '0'}[p];"
                f"[s1][p]paletteuse=dither=bayer:bayer_scale=3"
            )
            cmd = ["ffmpeg", "-y", "-framerate", str(args.fps), "-i", pattern, "-vf", vf, out_abs]
        else:
            cmd = [
                "ffmpeg", "-y", "-framerate", str(args.fps), "-i", pattern,
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", out_abs
            ]

        subprocess.run(cmd, check=True)
        print(f"Rendered {total_frames} frames ({args.duration}s @ {args.fps}fps) -> {out_abs}")
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
