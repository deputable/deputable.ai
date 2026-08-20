"""Generate favicons and the social share image from assets/deputable-logo.png.

Run after changing the logo:  python3 scripts/generate_icons.py

Outputs (all in assets/):
  favicon.ico          16/32/48 multi-size, browser tab
  favicon-32.png       32x32 PNG fallback
  apple-touch-icon.png 180x180, iOS home screen
  og-image.png         1200x630 link preview / thumbnail
"""

import os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")
LOGO = os.path.join(ASSETS, "deputable-logo.png")

BG = (251, 251, 249, 255)  # brand background #FBFBF9

# The logo lockup is [mark][gap][wordmark]; the gap sits at x=350..382.
MARK_SPLIT_X = 366


def square(img, size, pad_ratio):
    """Fit img into a size x size canvas on the brand background."""
    box = int(size * (1 - 2 * pad_ratio))
    fitted = img.copy()
    fitted.thumbnail((box, box), Image.LANCZOS)
    canvas = Image.new("RGBA", (size, size), BG)
    canvas.alpha_composite(
        fitted, ((size - fitted.width) // 2, (size - fitted.height) // 2)
    )
    return canvas


def main():
    logo = Image.open(LOGO).convert("RGBA")
    mark = logo.crop((0, 0, MARK_SPLIT_X, logo.height)).crop(
        logo.crop((0, 0, MARK_SPLIT_X, logo.height)).getbbox()
    )

    icon = square(mark, 512, 0.08)
    icon.convert("RGB").save(
        os.path.join(ASSETS, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)]
    )
    icon.resize((32, 32), Image.LANCZOS).save(os.path.join(ASSETS, "favicon-32.png"))
    icon.resize((180, 180), Image.LANCZOS).save(
        os.path.join(ASSETS, "apple-touch-icon.png")
    )

    # Social thumbnail: full lockup centred on the brand background.
    og = Image.new("RGBA", (1200, 630), BG)
    full = logo.crop(logo.getbbox())
    full.thumbnail((900, 400), Image.LANCZOS)
    og.alpha_composite(full, ((1200 - full.width) // 2, (630 - full.height) // 2))
    og.convert("RGB").save(os.path.join(ASSETS, "og-image.png"), optimize=True)

    print("wrote favicon.ico, favicon-32.png, apple-touch-icon.png, og-image.png")


if __name__ == "__main__":
    main()
