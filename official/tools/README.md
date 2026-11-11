# SVG asset generator

The generator source lives in `generate-identity-assets.py`. It creates the seven project icon families under `official/logos/`, updates `official/manifest.json`, and writes a light/dark contact sheet at the repository root.

Run from the repository root with Python 3.10+:

```sh
python -m pip install -r official/tools/requirements.txt
python official/tools/generate-identity-assets.py
```

The script uses CairoSVG and Pillow to validate every SVG, rasterize favicon/Apple/OG derivatives, and assemble per-project `asset-family.zip` downloads.
