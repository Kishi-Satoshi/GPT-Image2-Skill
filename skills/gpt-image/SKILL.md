---
name: gpt-image
description: "Use this skill when the user asks to generate, create, draw, render, or edit an image with gpt-image-2, GPT Image 2, or ChatGPT image generation. Covers text-to-image, restyling or editing one or more reference images, and mask-based inpainting. Run the bundled scripts/generate.py from the terminal to call OpenAI's gpt-image-2 model; do not write new image-generation code."
---

# gpt-image

Generate or edit images with OpenAI's `gpt-image-2` model by running the bundled script. Do not reimplement the API call.

## Requirements

- `OPENAI_API_KEY` must be set in the environment.
- The `openai` Python package must be installed: `pip install openai`.

## How to run

Text to image:

```bash
python scripts/generate.py -p "a photorealistic convenience store at 10pm" -o out.png
```

Restyle or edit one or more reference images (each `-i` switches to the edit endpoint and is repeatable):

```bash
python scripts/generate.py -p "make it a snowy winter evening" -i photo.png -o winter.png
python scripts/generate.py -p "put the dog from image 2 next to the woman in image 1" -i woman.png -i dog.png -o combined.png
```

Mask-based inpaint (the transparent area of the mask is regenerated; requires `-i`):

```bash
python scripts/generate.py -p "replace the sky with an aurora" -i photo.png -m mask.png -o aurora.png
```

## Options

- `-s, --size`: `square` (1024x1024), `portrait` (1024x1536), `landscape` (1536x1024), `auto`, or an explicit pixel size like `1024x1024`. Default is `1024x1024`.
- `-q, --quality`: `low`, `medium`, `high`, or `auto`. Use `low` for cheap drafts, `high` for final or text-heavy images. Default is `high`.
- `-n, --number`: how many images to generate. When greater than 1, output files get `_0`, `_1`, ... suffixes.

## Prompting tips

- State the intended use (poster, UI mock, photo) and put any text that must appear in the image inside straight quotes.
- Be concrete about subject, materials, composition, and medium. For in-image text, dense diagrams, or small labels, use `--quality high`.

## After running

Report the saved file path(s) to the user.
