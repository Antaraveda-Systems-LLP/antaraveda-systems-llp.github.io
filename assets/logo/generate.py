#!/usr/bin/env python3
"""Regenerate every Antaraveda logo asset from the masters in src/.

Run from anywhere:  python3 assets/logo/generate.py
Requires Pillow.
"""
import os
from PIL import Image

OUT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(OUT, "src")

# The three lockup masters are pixel-aligned: artwork occupies (88, 80)-(864, 401)
# on a 1360x480 canvas, and the light/dark pair maps 1:1 by colour.
ART = (88, 80, 864, 401)          # 776 x 321
PAD = 88                          # matches the master's left/top clear space

LIGHT = {"ink": (26, 25, 22), "muted": (140, 138, 132),
         "rule": (212, 210, 204), "red": (216, 43, 43), "bg": (248, 247, 244)}
# Authored, not derived — taken from antaraveda-lockup-dark.png, which uses a
# warmer red and a dimmer rule than a naive inversion would produce.
DARK = {"ink": (240, 238, 232), "muted": (92, 90, 86),
        "rule": (42, 41, 38), "red": (232, 69, 60), "bg": (17, 17, 16)}

INVERSE = {LIGHT[k]: DARK[k] for k in ("ink", "muted", "rule", "red")}


def to_inverse(src):
    """Recolour light artwork to the dark palette, preserving alpha anti-aliasing.

    Recolouring the transparent master beats keying the dark master: the latter
    has its anti-aliasing blended into the background and would fringe.
    """
    out = Image.new("RGBA", src.size, (0, 0, 0, 0))
    sp, op = src.load(), out.load()
    for y in range(src.height):
        for x in range(src.width):
            r, g, b, a = sp[x, y]
            if not a:
                continue
            key = min(INVERSE, key=lambda c: (c[0]-r)**2 + (c[1]-g)**2 + (c[2]-b)**2)
            op[x, y] = INVERSE[key] + (a,)
    return out


def key_background(img, bg, tolerance=12):
    """Lift a flat background to alpha and trim to the artwork."""
    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sp, op = img.load(), out.load()
    for y in range(img.height):
        for x in range(img.width):
            p = sp[x, y]
            if max(abs(p[i] - bg[i]) for i in range(3)) > tolerance:
                op[x, y] = p + (255,)
    return out.crop(out.getbbox())


# Strokes go sub-pixel below ~64px and wash out. Pulling alpha up by a gamma
# curve keeps the circle and the A readable at icon sizes.
GAMMA = {16: 0.42, 32: 0.55, 48: 0.68, 64: 0.80}


def boost(img, g):
    alpha = img.getchannel("A").point(lambda v: min(255, round(255 * (v / 255) ** g)))
    out = img.copy()
    out.putalpha(alpha)
    return out


def emit(img, w, path, square=False):
    h = w if square else max(1, round(img.height * w / img.width))
    r = img.resize((w, h), Image.LANCZOS)
    if square and w in GAMMA:
        r = boost(r, GAMMA[w])
    r.save(path, optimize=True)


def main():
    transparent = Image.open(f"{SRC}/antaraveda-lockup-transparent.png").convert("RGBA")

    lockup = transparent.crop(ART)                       # 776 x 321, tight
    lockup_inv = to_inverse(lockup)

    # Boxed variants keep the master's clear space and even up the surplus canvas
    # on the right, which the originals leave asymmetric.
    box = (ART[0] - PAD, 0, ART[2] + PAD, 480)           # 952 x 480
    boxed_light = Image.open(f"{SRC}/antaraveda-lockup-light.png").convert("RGB").crop(box)
    boxed_dark = Image.open(f"{SRC}/antaraveda-lockup-dark.png").convert("RGB").crop(box)

    # No standalone mark was supplied with the lockups, so icons keep the bolder
    # purpose-built mark; the hairline one is illegible below ~128px.
    bold = key_background(
        Image.open(f"{SRC}/antaraveda-mark-bold.png").convert("RGB"), LIGHT["bg"])
    bold_inv = to_inverse(bold)

    for w in (240, 480, 776):
        emit(lockup,     w, f"{OUT}/antaraveda-logo-{w}.png")
        emit(lockup_inv, w, f"{OUT}/antaraveda-logo-inverse-{w}.png")
    for w in (480, 952):
        emit(boxed_light, w, f"{OUT}/antaraveda-logo-boxed-light-{w}.png")
        emit(boxed_dark,  w, f"{OUT}/antaraveda-logo-boxed-dark-{w}.png")

    # 16/48/180 are omitted deliberately: favicon.ico and apple-touch-icon already
    # cover those sizes. 32 and 64 stay because they carry the alpha boost, which a
    # hand-resize of the 512 would lose.
    for s in (32, 64, 256, 512):
        emit(bold, s, f"{OUT}/antaraveda-mark-{s}.png", square=True)
    for s in (256, 512):
        emit(bold_inv, s, f"{OUT}/antaraveda-mark-inverse-{s}.png", square=True)

    frames = []
    for s in (16, 32, 48, 64, 128, 256):
        r = bold.resize((s, s), Image.LANCZOS)
        frames.append(boost(r, GAMMA[s]) if s in GAMMA else r)
    frames[-1].save(f"{OUT}/favicon.ico",
                    sizes=[(f.width, f.height) for f in frames],
                    append_images=frames[:-1])

    # iOS and Android discard alpha and apply their own mask, so these are opaque
    # and carry their clear space inside the square.
    def padded(size, pad):
        canvas = Image.new("RGBA", (size, size), LIGHT["bg"] + (255,))
        n = round(size * (1 - 2 * pad))
        art = bold.resize((n, n), Image.LANCZOS)
        canvas.paste(art, ((size - n) // 2,) * 2, art)
        return canvas.convert("RGB")

    padded(180, 0.14).save(f"{OUT}/apple-touch-icon.png", optimize=True)
    padded(192, 0.14).save(f"{OUT}/icon-192.png", optimize=True)
    padded(512, 0.20).save(f"{OUT}/icon-maskable-512.png", optimize=True)

    print(f"lockup {lockup.size}  boxed {boxed_light.size}  mark {bold.size}")
    print(f"-> {len([f for f in os.listdir(OUT) if f.endswith(('.png', '.ico'))])} files")


if __name__ == "__main__":
    main()
