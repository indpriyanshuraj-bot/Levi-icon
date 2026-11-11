# V2 project identity asset index

All seven projects have a main SVG, two alternative SVG concepts and a complete set of derivatives. The preferred project SVG is always `icon.svg`; no raster `icon.png` is generated.

| Project | Main SVG | Banner | Favicon | Apple touch | Open Graph | Asset ZIP |
|---|---|---|---|---|---|---|
| LegacyScriptEngine | `logos/legacy-script-engine/icon.svg` | `icon-banner.svg` | `favicon.ico` | `apple-touch-icon.png` | `og-image.png` | `asset-family.zip` |
| lip | `logos/lip/icon.svg` | `icon-banner.svg` | `favicon.ico` | `apple-touch-icon.png` | `og-image.png` | `asset-family.zip` |
| LeviAntiCheat | `logos/levi-anticheat/icon.svg` | `icon-banner.svg` | `favicon.ico` | `apple-touch-icon.png` | `og-image.png` | `asset-family.zip` |
| LeviOptimize | `logos/levioptimize/icon.svg` | `icon-banner.svg` | `favicon.ico` | `apple-touch-icon.png` | `og-image.png` | `asset-family.zip` |
| MoreDimensions | `logos/moredimensions/icon.svg` | `icon-banner.svg` | `favicon.ico` | `apple-touch-icon.png` | `og-image.png` | `asset-family.zip` |
| bedboo | `logos/bedboo/icon.svg` | `icon-banner.svg` | `favicon.ico` | `apple-touch-icon.png` | `og-image.png` | `asset-family.zip` |
| LeviMC Mods | `logos/levimc-mods/icon.svg` | `icon-banner.svg` | `favicon.ico` | `apple-touch-icon.png` | `og-image.png` | `asset-family.zip` |

Each path in the table is relative to that project's `logos/<slug>/` directory where the table gives only a filename.

## Asset requirements

- `icon.svg`: 512 × 512 viewBox, transparent canvas, editable vector shapes, no embedded raster.
- `icon-banner.svg`: 1200 × 240 transparent lockup.
- `favicon.ico`: embedded sizes 16, 32, 48, 64, 128 and 256 px.
- `favicon-16x16.png`, `favicon-32x32.png`, `favicon-48x48.png`, `favicon-64x64.png`, `favicon-128x128.png`, `favicon-256x256.png`: explicit PNG sizes.
- `apple-touch-icon.png`: 180 × 180.
- `og-image.svg`: editable 1200 × 630 vector source.
- `og-image.png`: 1200 × 630 social-sharing image.
- `variants/*.svg`: two independently authored alternatives, each with a 512 × 512 viewBox.
- `asset-family.zip`: includes all SVGs and derivatives for that one project.

## Colour approach

The LeviLamina leaf itself retains the original botanical green. The rest of each symbol uses a project-specific palette: navy/teal for lip, navy/blue/coral for LeviAntiCheat, navy/cyan/violet for LeviOptimize, indigo/violet/cyan for MoreDimensions, blue/teal for bedboo, and indigo/amber for LeviMC Mods. LegacyScriptEngine stays in the heritage-green family.

## Reference provenance

`references/levilamina-logo.svg` is an unchanged copy of `LiteLDev/LeviLamina/docs/main/contents/logo.svg`. The gallery also displays the current LeviLauncher leaf PNG directly from its official source URL for an exact comparison. V1's current-icon previews use unchanged copies of the source SVGs in `LiteLDev/levimc.org/kit/assets/icons/`. Neither official mark is recoloured or redrawn.

All project artwork remains an unofficial proposal pending maintainer review.
