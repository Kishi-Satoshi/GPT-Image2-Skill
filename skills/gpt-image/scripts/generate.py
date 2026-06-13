#!/usr/bin/env python3
"""Minimal gpt-image-2 generator / editor.

Text -> image:
    python generate.py -p "a cat astronaut" -o out.png

Restyle / edit one or more reference images (-i switches to the edit endpoint, repeatable):
    python generate.py -p "make it a snowy winter evening" -i photo.png -o winter.png
    python generate.py -p "put the dog from image 2 next to the woman in image 1" -i woman.png -i dog.png -o combined.png

Inpaint with a mask (transparent area of the mask is regenerated; requires -i):
    python generate.py -p "replace the sky with an aurora" -i photo.png -m mask.png -o aurora.png

Requirements:
    pip install openai
    OPENAI_API_KEY set in the environment
"""

import argparse
import base64
import os
import sys

try:
    from openai import OpenAI
except ImportError:
    sys.exit('The "openai" package is required. Install it with:  pip install openai')

# Friendly aspect-ratio names -> the literal pixel sizes gpt-image-2 accepts.
SIZE_ALIASES = {
    "square": "1024x1024",
    "portrait": "1024x1536",
    "landscape": "1536x1024",
    "auto": "auto",
}


def suffixed(path, idx):
    root, ext = os.path.splitext(path)
    return f"{root}_{idx}{ext or '.png'}"


def main():
    parser = argparse.ArgumentParser(
        description="Generate or edit images with OpenAI gpt-image-2."
    )
    parser.add_argument("-p", "--prompt", required=True, help="Text prompt.")
    parser.add_argument("-o", "--out", default="output.png",
                        help="Output file path. Default: output.png")
    parser.add_argument("-i", "--image", action="append", default=[],
                        help="Reference image to edit (repeatable). Any -i switches to the edit endpoint.")
    parser.add_argument("-m", "--mask",
                        help="PNG mask for inpainting (transparent = regenerate). Requires -i.")
    parser.add_argument("-s", "--size", default="1024x1024",
                        help="square | portrait | landscape | auto, or an explicit WxH like 1024x1024. Default: 1024x1024")
    parser.add_argument("-q", "--quality", default="high",
                        choices=["low", "medium", "high", "auto"],
                        help="low for cheap drafts, high for final / text-heavy images. Default: high")
    parser.add_argument("-n", "--number", type=int, default=1,
                        help="How many images to generate. Default: 1")
    args = parser.parse_args()

    if not os.environ.get("OPENAI_API_KEY"):
        sys.exit('OPENAI_API_KEY is not set. On Windows:  setx OPENAI_API_KEY "sk-..."  then reopen the terminal.')

    size = SIZE_ALIASES.get(args.size, args.size)
    client = OpenAI()

    open_files = []
    try:
        if args.image:
            # Edit / restyle / inpaint
            images = [open(p, "rb") for p in args.image]
            open_files.extend(images)
            kwargs = dict(model="gpt-image-2", prompt=args.prompt, image=images,
                          size=size, quality=args.quality, n=args.number)
            if args.mask:
                mask_f = open(args.mask, "rb")
                open_files.append(mask_f)
                kwargs["mask"] = mask_f
            result = client.images.edit(**kwargs)
        else:
            # Text -> image
            result = client.images.generate(model="gpt-image-2", prompt=args.prompt,
                                             size=size, quality=args.quality, n=args.number)
    finally:
        for f in open_files:
            f.close()

    # gpt-image models return base64-encoded PNG bytes.
    for idx, item in enumerate(result.data):
        data = base64.b64decode(item.b64_json)
        path = args.out if len(result.data) == 1 else suffixed(args.out, idx)
        with open(path, "wb") as out:
            out.write(data)
        print(f"saved: {path}")


if __name__ == "__main__":
    main()
