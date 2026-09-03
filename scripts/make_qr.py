"""Build the print QR code for the permanent booking link.

The QR encodes https://deputable.ai/book (NEVER the Zoho URL directly:
/book is the redirect we control, so printed material survives any
change of booking provider).

Run (dev-only deps, not needed by generate_site.py):

    uv run --with segno --with pillow python3 scripts/make_qr.py

Verify it still scans after any change (logo overlay eats error budget):

    uv run --with opencv-python-headless python3 -c "
    import cv2; print(cv2.QRCodeDetector().detectAndDecode(cv2.imread('assets/book-qr.png'))[0])"

Outputs (committed; also served from the site so they can be linked):
  assets/book-qr.svg  vector master, plain navy - use for print layouts
  assets/book-qr.png  2048px with the brand mark centred - ready to drop
                      into cards/flyers as-is
"""
import io
import os

import segno
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")

URL = "https://deputable.ai/book"
NAVY = "#0E2A4A"
SIZE = 2048

qr = segno.make(URL, error="h")  # H = 30% error budget, room for the logo

qr.save(os.path.join(ASSETS, "book-qr.svg"), kind="svg", dark=NAVY,
        light="#FFFFFF", border=4)
print("wrote assets/book-qr.svg")

# PNG at print resolution with the brand mark on a white tile in the
# centre (~18% of width - well inside the 30% error budget).
buf = io.BytesIO()
qr.save(buf, kind="png", dark=NAVY, light="#FFFFFF", border=4, scale=10)
buf.seek(0)
img = Image.open(buf).convert("RGBA").resize((SIZE, SIZE), Image.NEAREST)

mark = Image.open(os.path.join(ASSETS, "icon-512.png")).convert("RGBA")
tile_side = int(SIZE * 0.18)
mark_side = int(tile_side * 0.82)
tile = Image.new("RGBA", (tile_side, tile_side), (255, 255, 255, 255))
mark = mark.resize((mark_side, mark_side), Image.LANCZOS)
tile.paste(mark, ((tile_side - mark_side) // 2, (tile_side - mark_side) // 2), mark)
img.paste(tile, ((SIZE - tile_side) // 2, (SIZE - tile_side) // 2))

img.convert("RGB").save(os.path.join(ASSETS, "book-qr.png"), optimize=True)
print(f"wrote assets/book-qr.png ({SIZE}x{SIZE})")
