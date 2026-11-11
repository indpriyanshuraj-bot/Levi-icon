# LeviMC Icon Study

An unofficial review repository for website icon replacements (V1) and project identity concepts (V2). **Nothing here is approved production branding unless the relevant LeviMC maintainers explicitly accept it.**

## One shared gallery

Run a local static server from the repository root:

```sh
python3 -m http.server 8000
```

Open `http://localhost:8000/`. The same page contains three tabs:

- **V1 · Website** — the existing 15 website placements, the original source PixelIcon SVG for each current icon (copied unchanged, including its original colours), and all 45 proposed coloured SVG candidates.
- **V2 · Projects** — seven project identities, three logo directions per project, and tabs for the icon, banner, favicon, Apple touch icon and Open Graph image.
- **Official comparison** — the exact current LeviLamina SVG and the current LeviLauncher leaf asset, shown on white and OLED-black surfaces.

`/official/` redirects into the V2 tab of the same page. Both routes use one stylesheet, one script, one search/theme system and the same card components; there is no duplicate gallery implementation.

## Theme and preview behaviour

The gallery has a global **White / OLED black** switch. It changes the website surface only. Each SVG is the same file in both modes. The V1 current-icon previews use the exact original 16 × 16 pixel-art SVGs from `LiteLDev/levimc.org/kit/assets/icons/`; the source files are preserved unchanged and shown on a neutral white tile for fidelity. Proposed V1 options and official-logo references are also tested against white and OLED-black surfaces.

The V2 project cards let you select one of the three concept directions, then preview:

- `icon.svg` — 512 × 512 transparent vector master.
- `icon-banner.svg` — 1200 × 240 transparent name lockup.
- `favicon.ico` — 16, 32, 48, 64, 128 and 256 px embedded images.
- `apple-touch-icon.png` — 180 × 180.
- `og-image.png` — 1200 × 630; editable source is `og-image.svg`.

Each project also has explicit PNG favicon derivatives and `asset-family.zip`. **There is no `icon.png` asset.**

## Visual direction

The shared leaf motif and LeviLamina green reference are derived from the current official SVG at `official/references/levilamina-logo.svg` (copied unchanged from the official source). V2 geometry has separate project colour systems so projects do not all become green variations:

- LegacyScriptEngine — heritage greens.
- lip — deep blue, teal and amber dependency accents.
- LeviAntiCheat — navy, detection blue and coral alert accents.
- LeviOptimize — technical navy, electric cyan and violet telemetry accents.
- MoreDimensions — indigo, dimensional violet and cyan.
- bedboo — blue, teal and warm connector accents.
- LeviMC Mods — indigo, amber and green catalogue accents.

The original LeviLamina leaf motif remains green as a secondary family cue. Project-specific colour belongs to the surrounding symbol, not to the copied reference logo.

## Regenerate V2 artwork

Install the listed Python dependencies, then run the generator and the palette/export pass:

```sh
python -m pip install -r official/tools/requirements.txt
python official/tools/generate-identity-assets.py
python official/tools/retheme-projects.py
```

The second script reapplies project-specific palettes, adds the additional detail to lip, LeviAntiCheat and LeviOptimize, and regenerates favicons, Apple touch icons, OG PNGs and per-project asset bundles. Do not run only the first script if you need the checked V2 colour treatment.

## GitHub Pages

The workflow in `.github/workflows/pages.yml` stages the static site without `.git` or workflow files, then deploys it with GitHub Pages. Set **Settings → Pages → Build and deployment → Source** to **GitHub Actions**.

The workflow uses `actions/checkout@v6`, `actions/configure-pages@v5`, `actions/upload-pages-artifact@v4` and `actions/deploy-pages@v4`, matching the current GitHub Pages workflow guidance checked for this revision.

## Repository ZIP and commit workflow

The accompanying `Levi-icon-full-repository.zip` is a full working-tree snapshot based on the current `main` repository state plus this update. It intentionally excludes `.git/` so it can remain a clean, portable archive.

1. Extract the ZIP into a new folder.
2. Copy the `.git` directory from your existing `Levi-icon` clone into the extracted folder.
3. From that folder, run:

```sh
git status --short
git add -A
git commit -m "Unify icon gallery and refine project identity previews"
git push origin HEAD
```

No files need to be copied individually from the ZIP into your existing clone. The `.git` directory supplies the repository history and remote; the extracted working tree supplies the complete updated files.

## Status and ownership

This repository is an independent, unofficial proposal. LeviMC, LeviLamina, LeviLauncher and project names/logos remain the property of their respective owners. The official reference marks are included or linked only for comparison, without modification or implied endorsement. The proposal website and authored concept assets are provided under the repository MIT License.
