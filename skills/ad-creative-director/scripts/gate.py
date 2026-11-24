#!/usr/bin/env python3
"""Mechanical quality gate for a finished creative.

    python3 gate.py creative.png --format meta-feed

Checks pixel size against the format, file weight and aspect ratio, then writes a
360px-wide phone preview next to the file (needs Pillow; without it only size checks run).
It does not judge the design. Look at the image and score references/quality-gate.md.
"""
import argparse, struct, sys
from pathlib import Path

FORMATS = {
    "meta-feed": (1080, 1350, 30), "meta-story": (1080, 1920, 30), "square": (1080, 1080, 30),
    "youtube-thumb": (1280, 720, 2), "reel-cover": (1080, 1920, 30), "website-hero": (1920, 900, 1),
    "link-ad": (1200, 628, 30),
}


def dims(p):
    b = p.read_bytes()
    if b[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", b[16:24])
    if b[:2] == b"\xff\xd8":
        i = 2
        while i < len(b):
            if b[i] != 0xFF:
                i += 1; continue
            m = b[i + 1]
            if m in (0xC0, 0xC1, 0xC2):
                h, w = struct.unpack(">HH", b[i + 5:i + 9]); return w, h
            i += 2 + struct.unpack(">H", b[i + 2:i + 4])[0]
    if b[:4] == b"RIFF" and b[8:12] == b"WEBP" and b[12:16] == b"VP8X":
        return int.from_bytes(b[24:27], "little") + 1, int.from_bytes(b[27:30], "little") + 1
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("image"); ap.add_argument("--format", choices=FORMATS, required=True)
    a = ap.parse_args()
    p = Path(a.image)
    W, H, max_mb = FORMATS[a.format]
    d = dims(p)
    problems = []
    if not d:
        sys.exit("Could not read image size (PNG, JPEG or extended WebP expected).")
    w, h = d
    if (w, h) != (W, H):
        if abs(w / h - W / H) > 0.01:
            problems.append(f"Aspect {w}x{h} does not match {a.format} {W}x{H}. It will be cropped.")
        elif w < W:
            problems.append(f"{w}x{h} is below {W}x{H}. Re-export larger.")
        else:
            print(f"  note: {w}x{h} is a clean multiple of {W}x{H}. Fine.")
    mb = p.stat().st_size / 1e6
    if mb > max_mb:
        problems.append(f"{mb:.1f} MB is above the {max_mb} MB limit for {a.format}.")
    try:
        from PIL import Image
        im = Image.open(p).convert("RGB")
        prev = im.resize((360, round(360 * im.height / im.width)), Image.LANCZOS)
        out = p.with_name(p.stem + ".phone-preview.png")
        prev.save(out)
        print(f"  phone preview: {out}  (look at it before delivering)")
    except ImportError:
        print("  Pillow not installed, no phone preview. pip install pillow")
    print(f"GATE {p.name}  {w}x{h}  {mb:.2f} MB  format={a.format}")
    for x in problems:
        print("  FAIL " + x)
    print("PASS mechanical checks. Now score the ten questions." if not problems else f"{len(problems)} problem(s)")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
