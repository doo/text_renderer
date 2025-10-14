#!/usr/bin/env python3
"""
Simple font viewer script to categorize fonts as robust, fragile, extreme, or blacklist.

Usage: python sort_fonts.py

Controls:
- 'r': Mark font as robust
- 'f': Mark font as fragile
- 'e': Mark font as extreme
- 'b': Add font to blacklist
- 'n': Next image (skip current)
- 'q': Quit
"""

from pathlib import Path

import cv2

WORK_DIR = Path(__file__).absolute().parent / 'tlr'
OUT_DIR = WORK_DIR / "output"
FONT_LIST_DIR = WORK_DIR / "font_list"
FONT_DIR = WORK_DIR / "font"
FONT_BLACKLIST = FONT_LIST_DIR / "font_blacklist.txt"
FONT_LIST = FONT_LIST_DIR / "font_list.txt"


def get_font_blacklist():
    if not FONT_BLACKLIST.exists():
        return []

    with open(FONT_BLACKLIST, 'r') as f:
        return [line.strip() for line in f if line.strip()]


def get_font_list():
    src_file = FONT_LIST_DIR / "fragile_and_robust_fonts.txt"
    assert src_file.exists()

    with open(src_file, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]


def main():
    FONT_LIST_DIR.mkdir(exist_ok=True)
    robust_file = FONT_LIST_DIR / "robust_fonts.txt"
    fragile_file = FONT_LIST_DIR / "fragile_fonts.txt"
    extreme_file = FONT_LIST_DIR / "extreme_fonts.txt"

    font_names = get_font_list()
    assert len(font_names) > 0

    print(
        "Controls: 'r'=robust, 'f'=fragile, 'e'=extreme, 'b'=blacklist, 'n'=next, 'q'=quit"
    )

    for i, font_name in enumerate(font_names):
        font_path = Path(font_name)
        font_dir = OUT_DIR / f"font_{i}_{font_path.stem}"

        # Find the image file
        images_dir = font_dir / "images"
        if not images_dir.exists():
            print(f"No images directory in {font_dir}")
            continue

        image_files = list(images_dir.glob("*.jpg"))
        if not image_files:
            print(f"No images found in {images_dir}")
            continue

        image_path = image_files[0]  # Take the first image

        # Load and display image
        img = cv2.imread(str(image_path))
        if img is None:
            print(f"Could not load image: {image_path}")
            continue

        cv2.imshow(f'{i}/{len(font_names)}', img)

        while True:
            key = cv2.waitKey(0) & 0xFF

            if key == ord('r'):
                # Mark as robust
                with open(robust_file, 'a') as f:
                    f.write(f"{font_name}\n")
                print(f"✓ Marked {font_name} as ROBUST")
                break

            elif key == ord('f'):
                # Mark as fragile
                with open(fragile_file, 'a') as f:
                    f.write(f"{font_name}\n")
                print(f"✓ Marked {font_name} as FRAGILE")
                break

            elif key == ord('e'):
                # Mark as extreme
                with open(extreme_file, 'a') as f:
                    f.write(f"{font_name}\n")
                print(f"✓ Marked {font_name} as EXTREME")
                break

            elif key == ord('b'):
                # Add to blacklist
                with open(FONT_BLACKLIST, 'a') as f:
                    f.write(f"{font_name}\n")
                print(f"🚫 Added {font_name} to BLACKLIST")
                break

            # elif key == ord('n'):
            if key == ord('n'):
                # Skip this font
                print(f"⏭ Skipped {font_name}")
                break

            elif key == ord('q'):
                # Quit
                print("Quitting...")
                cv2.destroyAllWindows()
                return

        cv2.destroyAllWindows()

    print("\n✅ Finished reviewing all fonts!")
    print(f"Results saved in:")
    print(f"  - Robust fonts: {robust_file}")
    print(f"  - Fragile fonts: {fragile_file}")
    print(f"  - Extreme fonts: {extreme_file}")
    print(f"  - Blacklisted fonts: {FONT_BLACKLIST}")


if __name__ == "__main__":
    main()
