# LeviMC Icon Refresh Proposal

An unofficial design and implementation reference for icon improvements across the LeviMC website and related projects. **Nothing in this repository is approved production branding unless the relevant maintainers explicitly accept it.**

## Preview

- Main website icon comparison: repository root / GitHub Pages home.
- Project identity concepts and asset exports: [`/official/`](official/).
- Run locally from the repository root with `python3 -m http.server 8000`, then open `http://localhost:8000/` or `http://localhost:8000/official/`.

## Project identity collection

The `/official/` gallery covers LegacyScriptEngine, lip, LeviAntiCheat, LeviOptimize, MoreDimensions, bedboo, and LeviMC Mods. Each project has three SVG concepts: one preferred master and two alternatives. A global light/dark gallery toggle is included, and every concept is rendered side-by-side against both surfaces using the same SVG source.

Each project folder contains:

- `icon.svg` — 512 × 512 transparent SVG master.
- `icon-banner.svg` — transparent horizontal name lockup; project name uses the LeviLamina leaf-green accent.
- `favicon.ico` — multi-resolution 16, 32, 48, 64, 128, and 256 px icon.
- `favicon-*.png` — explicit PNG favicon sizes.
- `apple-touch-icon.png` — 180 × 180.
- `og-image.svg` and `og-image.png` — editable source and 1200 × 630 social image.
- `variants/*.svg` — two alternative logo directions.
- `asset-family.zip` — complete per-project export bundle.

See [`official/ASSET-INDEX.md`](official/ASSET-INDEX.md) for exact paths and sizes.

## Brand reference

The palette and botanical language are based on the current official [LeviLamina logo SVG](https://github.com/LiteLDev/LeviLamina/blob/main/docs/main/contents/logo.svg). Core colours are `#294c2d`, `#52784d`, `#7ba46d`, `#90a08c`, and `#b9ccac`. The LeviLauncher identity remains a separate reference and is not redrawn in this collection.

## Regenerate the project assets

```sh
python -m pip install -r official/tools/requirements.txt
python official/tools/generate-identity-assets.py
```

## GitHub Pages

The workflow in `.github/workflows/pages.yml` deploys the repository root (including `/official/`) through GitHub Actions. Set **Settings → Pages → Build and deployment → Source** to **GitHub Actions**.

## License and status

The concepts and gallery code are provided under the repository's MIT License. LeviMC and project names remain the property of their respective owners. This is an independent proposal and does not imply endorsement.
