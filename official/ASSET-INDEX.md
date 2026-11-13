# Project identity asset index

Seven projects have three selectable logo concepts each. Every concept has its own full set of exports. The root `icon.svg` path is the standard export path; the other two directions are in the `variants/` folder. The gallery presents every direction equally.

| Project | Primary icon master | Current logo comparison |
|---|---|---|
| LegacyScriptEngine | `logos/legacy-script-engine/icon.svg` | `LiteLDev/LegacyScriptEngine` docs logo |
| lip | `logos/lip/icon.svg` | `LiteLDev/lip` docs logo |
| LeviAntiCheat | `logos/levi-anticheat/icon.svg` | `LiteLDev/LeviAntiCheat` docs logo |
| LeviOptimize | `logos/levioptimize/icon.svg` | `LiteLDev/LeviOptimize` docs logo |
| MoreDimensions | `logos/moredimensions/icon.svg` | `LiteLDev/MoreDimensions` docs logo |
| bedboo | `logos/bedboo/icon.svg` | `LiteLDev/bedboo` docs logo |
| LeviMC Mods | `logos/levimc-mods/icon.svg` | `LiteLDev/levimc.org` mods catalogue icon |

## Per-direction exports

For each direction, the manifest records exact paths for:

- `icon.svg` — 512 × 512 transparent vector master.
- `icon-banner.svg` — 1200 × 240 transparent icon/name lockup; the accent line is below the subtitle.
- `favicon.ico` — 16, 32, 48, 64, 128 and 256 px embedded sizes.
- `favicon-16x16.png` through `favicon-256x256.png` — explicit PNG sizes.
- `apple-touch-icon.png` — 180 × 180.
- `og-image.svg` and `og-image.png` — editable SVG and 1200 × 630 PNG, neutral background, project-specific graphic accents, no circular green background.

Each project's `asset-family.zip` contains the asset exports for all three directions. No local `icon.png` is created.

## Reference provenance

`references/levilamina-logo.svg` is an unchanged copy of the current official `LiteLDev/LeviLamina/docs/main/contents/logo.svg`. The gallery displays the current LeviLauncher leaf asset directly from its official source URL. Website UI icon comparisons use unchanged SVG files from `LiteLDev/levimc.org/kit/assets/icons/`.

All proposed project artwork remains unofficial and requires maintainer review.
