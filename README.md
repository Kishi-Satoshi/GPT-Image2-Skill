# GPT Image 2 — Claude Code plugin

A lightweight Claude Code plugin that generates and edits images with OpenAI's
`gpt-image-2` model. Text-to-image, reference-image editing/restyling, and
mask-based inpainting, via one small bundled CLI script. No prompt gallery, no
heavy assets — just the generator.

## Install

```bash
claude plugin marketplace add Kishi-Satoshi/GPT-Image2-Skill
claude plugin install gpt-image@kishi-skills
```

Restart Claude Code afterwards.

## Requirements

- `OPENAI_API_KEY` set in the environment (your own OpenAI key; usage is billed by OpenAI).
- Python with the `openai` package: `pip install openai`.

## Use it directly (without Claude Code)

The bundled script works standalone too:

```bash
# text -> image
python skills/gpt-image/scripts/generate.py -p "a cat astronaut" -o cat.png

# edit / restyle a reference image (-i is repeatable)
python skills/gpt-image/scripts/generate.py -p "make it a snowy winter evening" -i photo.png -o winter.png

# inpaint (transparent area of the mask is regenerated)
python skills/gpt-image/scripts/generate.py -p "replace the sky with an aurora" -i photo.png -m mask.png -o aurora.png
```

Options: `-s square|portrait|landscape|auto` (or `WxH`), `-q low|medium|high|auto`, `-n <count>`.

## License

MIT
