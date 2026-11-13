# LeviMC Icon Study

An unofficial design review repository for website icons and project/application identities. **Nothing here is approved production branding unless the relevant maintainers explicitly accept it.**

## One shared, responsive gallery

Run a static server from the repository root:

```sh
python3 -m http.server 8000
```

Open `http://localhost:8000/`. The same interface contains three category tabs:

- **Website / UI** — 15 website placements, original current PixelIcon SVGs copied unchanged from `LiteLDev/levimc.org/kit/assets/icons/`, and 45 candidate icons. Candidate SVGs can be previewed in **Multicolour outline** or **Multicolour filled** styles.
- **Project / app logos** — seven project identities, three selectable concepts each. The current repository logo remains visible while you select a proposed mark. After selecting a concept, preview its icon SVG, banner SVG, multi-resolution favicon, Apple touch icon and OG image.
- **Official references** — the original LeviLamina SVG and LeviLauncher leaf asset displayed on white and OLED-black surfaces.

The `/official/` route redirects into the project/app logo category of the same gallery. It does not maintain a second UI implementation.

## Theme and comparison behaviour

The global theme switch changes the website background between pure white and OLED black. It does not recolour SVG artwork. The current website icons are the exact original 16 × 16 pixel-art source SVGs; proposed website icons have both multi-colour and filled variants.

For project logos, each card always shows the existing project artwork from its source repository. A proposed logo is shown only after you select one of the unranked concept tabs. No concept is marked recommended or alternative.

## Project asset families

Every project has three logo directions. Each direction has its own complete derivative family:

- `icon.svg` — 512 × 512 transparent vector master (standard root export path; the other two equal choices are in `variants/`).
- `icon-banner.svg` — 1200 × 240 transparent icon and name lockup. The accent line sits below the subtitle, not through the text.
- `favicon.ico` — multi-resolution ICO containing 16, 32, 48, 64, 128 and 256 px images.
- `favicon-*.png` — explicit PNG favicon sizes.
- `apple-touch-icon.png` — 180 × 180 PNG.
- `og-image.svg` and `og-image.png` — editable source and 1200 × 630 export. OG artwork uses neutral backgrounds and project-specific graphic accents; it does not use a generic green circle.
- `asset-family.zip` — complete per-project exports, including selected concept variants.

There is no local `icon.png` asset.

## Brand and colour direction

The LeviLamina reference is copied unchanged to `official/references/levilamina-logo.svg`. Its green leaf remains a secondary family motif. Project marks use distinct palettes: heritage greens for LegacyScriptEngine; teal/navy for lip; navy/blue/coral for LeviAntiCheat; navy/cyan/violet/amber for LeviOptimize; indigo/violet/cyan for MoreDimensions; blue/teal for bedboo; and indigo/amber for LeviMC Mods.

## Regenerate assets

Install dependencies and run both generators from the repository root:

```sh
python -m pip install -r official/tools/requirements.txt
python official/tools/generate-identity-assets.py
python official/tools/generate-website-icon-styles.py
```

The first script generates the project icon variants, banners, ICO/PNG derivatives, Apple touch icons, OG images, manifest and per-project ZIPs. The second generates the multicolour outline and multicolour filled styles for the website icon candidate icons.

## GitHub Pages

The workflow in `.github/workflows/pages.yml` stages the static website and deploys it with GitHub Pages. Set **Settings → Pages → Build and deployment → Source** to **GitHub Actions**. The workflow uses `actions/checkout@v6`, `actions/configure-pages@v5`, `actions/upload-pages-artifact@v4` and `actions/deploy-pages@v4`.

## Full repository ZIP workflow

The companion ZIP is a full repository working-tree snapshot based on the existing project files and this update. It intentionally excludes `.git/` so you can copy your existing Git metadata into it:

1. Extract the ZIP into a new folder.
2. Copy the complete `.git` directory from your existing `Levi-icon` clone into the extracted folder, beside `README.md` and `index.html`.
3. Open a terminal in that folder and run:

```sh
git status --short
git add -A
git commit -m "Refine icon comparisons and project logo concepts"
git push origin HEAD
```

No individual files need to be copied into the old working tree.

## Status and ownership

This repository is an independent, unofficial proposal. LeviMC, LeviLamina, LeviLauncher and project names/logos remain the property of their respective owners. The official reference marks are included or linked only for comparison, without modification or implied endorsement. The proposal website and authored concepts are provided under the repository MIT License.

## Preview sheets

Static review sheets for the generated assets are available under [`previews/`](previews/): website icon styles, project logo directions, and banner examples. The interactive gallery remains the primary comparison interface.
