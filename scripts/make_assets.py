"""Build the icon set and optimised logo from assets/deputable-logo.png.

Run rarely (only when the logo artwork changes):

    python3 scripts/make_assets.py

Needs Pillow (dev-only dependency, never required by generate_site.py):

    python3 -m pip install pillow   # or: uv run --with pillow python3 scripts/make_assets.py

Outputs (all committed):
  assets/favicon.ico        16+32+48 layered, cropped brand mark
  assets/icon-192.png       192x192 PNG
  assets/icon-512.png       512x512 PNG
  assets/apple-touch-icon.png  180x180 on solid #FBFBF9 (iOS flattens alpha to black)
  assets/deputable-logo.png    lockup resized to 448px tall (~2x the 64px header
                               display; the 205KB original stays in git history)
"""
import os

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")
LOGO = os.path.join(ASSETS, "deputable-logo.png")

BG = (251, 251, 249, 255)  # --bg #FBFBF9

logo = Image.open(LOGO).convert("RGBA")
w, h = logo.size
print(f"source logo: {w}x{h}")

# --- brand mark: the rings+arrow occupy the left ~26% of the lockup ---
mark = logo.crop((0, 0, int(w * 0.26), h))
bbox = mark.getbbox()  # trim transparent padding
mark = mark.crop(bbox)
mw, mh = mark.size
side = max(mw, mh)
square = Image.new("RGBA", (side, side), (0, 0, 0, 0))
square.paste(mark, ((side - mw) // 2, (side - mh) // 2), mark)
print(f"mark cropped to {mw}x{mh}, padded to {side}x{side}")

for size, name in [(512, "icon-512.png"), (192, "icon-192.png")]:
    square.resize((size, size), Image.LANCZOS).save(os.path.join(ASSETS, name))
    print(f"wrote assets/{name}")

# iOS flattens transparency to black — give the touch icon a solid ground
touch = Image.new("RGBA", (side, side), BG)
touch.paste(square, (0, 0), square)
touch.resize((180, 180), Image.LANCZOS).convert("RGB").save(
    os.path.join(ASSETS, "apple-touch-icon.png"))
print("wrote assets/apple-touch-icon.png")

square.resize((48, 48), Image.LANCZOS).save(
    os.path.join(ASSETS, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
print("wrote assets/favicon.ico")

# --- shrink the lockup file (200KB -> ~33KB) without touching its
# dimensions: palette-quantise (flat-colour artwork survives this crisply) ---
logo.quantize(colors=256, method=Image.Quantize.FASTOCTREE).save(LOGO, optimize=True)
print(f"wrote assets/deputable-logo.png at {w}x{h} "
      f"({os.path.getsize(LOGO) // 1024}KB)")
