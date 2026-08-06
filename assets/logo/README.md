# Antaraveda Systems — Logo Assets

Everything here is derived from the original lockup PNGs in [`src/`](src/) by
[`generate.py`](generate.py). Derived files have transparent backgrounds unless the
name says `boxed` or they are platform icons.

## Which file do I use?

| Need | File |
|---|---|
| Website header, letterhead, slide deck | `antaraveda-logo-480.png` (or 240 / 776) |
| Same, on a dark background | `antaraveda-logo-inverse-480.png` |
| Somewhere transparency breaks (email signature, Word, print) | `antaraveda-logo-boxed-light-480.png` |
| Same, dark card | `antaraveda-logo-boxed-dark-480.png` |
| Avatar, app icon, social profile, stamp | `antaraveda-mark-256.png` |
| Same, on a dark background | `antaraveda-mark-inverse-256.png` |
| Browser tab | `favicon.ico` (multi-res 16→256) |
| iOS home screen | `apple-touch-icon.png` (180px) |
| Android / PWA | `icon-192.png`, `icon-maskable-512.png` |

**Lockup** — mark + wordmark + tagline. Trimmed tight to the artwork, 776 × 321 native,
aspect ratio 2.417:1. Widths 240, 480, 776.

**Boxed lockup** — opaque, keeping the master's 88px clear space, 952 × 480 native.
Widths 480, 952.

**Mark** — the circled *A*, square. Sizes 32, 64, 256, 512 (inverse: 256, 512).

The mark comes from `src/antaraveda-mark-bold.png`, which has heavier strokes and a
larger dot than the one inside the lockup — the lockup's hairline version is illegible
below ~128px, and the three lockup masters contain no standalone mark.

The 32 and 64 have an alpha-gamma boost baked in so the strokes survive rasterisation.
They are therefore **not** plain downscales of the 512 — regenerate with the script
rather than resizing by hand, or they will come out washed out.

## Colours

| Role | Light | Dark |
|---|---|---|
| Ink | `#1A1916` | `#F0EEE8` |
| Muted (tagline) | `#8C8A84` | `#5C5A56` |
| Rule (divider) | `#D4D2CC` | `#2A2926` |
| Red (the dot) | `#D82B2B` | `#E8453C` |
| Background | `#F8F7F4` | `#111110` |

The dark column is **authored, not inverted** — it comes from
`src/antaraveda-lockup-dark.png`, which uses a warmer red and a much dimmer rule than a
naive inversion produces. The `-inverse-` files reproduce it exactly: composited on
`#111110` they are pixel-identical to the dark master.

Note the light column matches the CSS custom properties in `index.html`, but the site's
dark `#security` section still uses `#D82B2B` rather than the dark-palette `#E8453C`.

## Usage

- **Clear space** — keep free space of at least the circle's radius on all sides. The
  non-`boxed` files are trimmed tight, so add this in layout.
- **Minimum sizes** — lockup 160px wide; mark 16px (via `favicon.ico`).
- **On dark** — use the `-inverse-` variants. Do not invert the standard files; the red
  is a different value in each palette.
- **Don't** re-colour, stretch, rotate, add effects, or rebuild the lockup by placing
  the mark next to typed text — the spacing is part of the artwork.

## Masters

| File | Notes |
|---|---|
| `src/antaraveda-lockup-transparent.png` | 1360 × 480 RGBA. **The one everything derives from.** |
| `src/antaraveda-lockup-light.png` | 1360 × 480 RGB on `#F8F7F4`. Source for boxed light. |
| `src/antaraveda-lockup-dark.png` | 1360 × 480 RGB on `#111110`. Reference for the dark palette. |
| `src/antaraveda-mark-bold.png` | 328 × 328. Small-size mark; source for all icons. |

All three lockups are pixel-aligned — artwork sits at `(88, 80)–(864, 401)` in every
one. The canvas is much wider than the artwork, leaving ~496px of surplus on the right;
the derived files trim it.

## Regenerating

```sh
pip install Pillow
python3 assets/logo/generate.py
```

Sizes are kept deliberately few. If you need one that isn't here, add it to the size
tuple in `generate.py` and re-run rather than resizing an existing PNG by hand.

## Known gap

**No vector source.** Everything derives from raster masters, so the lockup cannot
exceed 776px wide, nor the mark 328px, without softening. Adequate for web; not for
print or signage. If you still have the file these PNGs were exported from, an SVG or
PDF export would remove the ceiling permanently.
