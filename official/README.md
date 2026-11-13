# Project and application logo concepts

This directory stores SVG masters, proposed logo directions and their complete asset exports for seven LeviMC-related projects. The name `/official/` is a convenient collection path and **does not mean the designs are approved official branding**.

Open `/official/` in a browser to redirect to the Project / app logos category in the shared root gallery. The root website owns the navigation, search, theme control and preview UI.

Each project has three selectable directions. The project card keeps its current repository logo visible, then lets you select a proposed design. Each selected design has its own icon, banner, favicon, Apple touch icon and Open Graph image. No variant is tagged recommended or alternative.

## Asset structure

Each project folder includes three equal SVG directions. The first uses the standard root `icon.svg` path for export compatibility; the other two live under `variants/`. The gallery does not rank them. Banner lockups place the only accent rule below the subtitle, never through the lettering. Open Graph images use neutral backgrounds and project-specific accents, not a default green circle.

There is no local `icon.png` asset. The current project logos in the comparison are read from their original public repository URLs; the source link is shown alongside each one.

## Regenerate

From the repository root:

```sh
python -m pip install -r official/tools/requirements.txt
python official/tools/generate-identity-assets.py
```

The generator creates all project assets, per-variant exports, manifest metadata and project ZIP bundles.
