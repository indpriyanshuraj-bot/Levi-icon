# V2 project identity concepts

This directory stores SVG masters, alternative directions and exported assets for seven LeviMC project identity concepts. Its `/official/` route is only a convenient collection path; **it does not mean the designs have been approved as official LeviMC branding**.

The gallery is shared with the repository root. Open `/official/` to jump directly to the V2 tab; all styling, theme switching, search and preview code is in the repository root.

## Project asset families

Each `logos/<project>/` directory includes:

- `icon.svg` — 512 × 512 transparent vector master.
- `variants/*.svg` — two independent alternative directions.
- `icon-banner.svg` — 1200 × 240 transparent lockup.
- `favicon.ico` — multi-resolution ICO (16, 32, 48, 64, 128, 256 px).
- `favicon-*.png` — explicit PNG sizes.
- `apple-touch-icon.png` — 180 × 180 PNG.
- `og-image.svg` and `og-image.png` — editable source and 1200 × 630 export.
- `asset-family.zip` — complete per-project export bundle.

The website's project cards provide tabs to preview and download each format. No `icon.png` is generated.

## Colour and family system

The current LeviLamina SVG is kept unchanged at `references/levilamina-logo.svg`. Its green leaf motif is a secondary family cue. Each V2 symbol has its own colour system: teal/navy for lip; navy/blue/coral for LeviAntiCheat; navy/cyan/violet for LeviOptimize; indigo/violet/cyan for MoreDimensions; blue/teal for bedboo; indigo/amber for LeviMC Mods; and the original botanical green family for LegacyScriptEngine.

## Regeneration

From repository root:

```sh
python -m pip install -r official/tools/requirements.txt
python official/tools/generate-identity-assets.py
python official/tools/retheme-projects.py
```

Always run the retheme/export pass after the source generator. It restores the project-specific palettes and updates all raster derivatives and project ZIP bundles.

The concepts remain unofficial and require maintainer review before any project adopts them.
