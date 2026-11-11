# Project identity asset index

Every project directory contains one 512 × 512 SVG master, two alternative SVG directions, and derivatives exported from the master.

| Project | Master SVG | Banner SVG | Favicon | Apple touch | Open Graph | Asset bundle |
|---|---|---|---|---|---|---|
| LegacyScriptEngine | `logos/legacy-script-engine/icon.svg` | `logos/legacy-script-engine/icon-banner.svg` | `logos/legacy-script-engine/favicon.ico` | `logos/legacy-script-engine/apple-touch-icon.png` | `logos/legacy-script-engine/og-image.png` | `logos/legacy-script-engine/asset-family.zip` |
| lip | `logos/lip/icon.svg` | `logos/lip/icon-banner.svg` | `logos/lip/favicon.ico` | `logos/lip/apple-touch-icon.png` | `logos/lip/og-image.png` | `logos/lip/asset-family.zip` |
| LeviAntiCheat | `logos/levi-anticheat/icon.svg` | `logos/levi-anticheat/icon-banner.svg` | `logos/levi-anticheat/favicon.ico` | `logos/levi-anticheat/apple-touch-icon.png` | `logos/levi-anticheat/og-image.png` | `logos/levi-anticheat/asset-family.zip` |
| LeviOptimize | `logos/levioptimize/icon.svg` | `logos/levioptimize/icon-banner.svg` | `logos/levioptimize/favicon.ico` | `logos/levioptimize/apple-touch-icon.png` | `logos/levioptimize/og-image.png` | `logos/levioptimize/asset-family.zip` |
| MoreDimensions | `logos/moredimensions/icon.svg` | `logos/moredimensions/icon-banner.svg` | `logos/moredimensions/favicon.ico` | `logos/moredimensions/apple-touch-icon.png` | `logos/moredimensions/og-image.png` | `logos/moredimensions/asset-family.zip` |
| bedboo | `logos/bedboo/icon.svg` | `logos/bedboo/icon-banner.svg` | `logos/bedboo/favicon.ico` | `logos/bedboo/apple-touch-icon.png` | `logos/bedboo/og-image.png` | `logos/bedboo/asset-family.zip` |
| LeviMC Mods | `logos/levimc-mods/icon.svg` | `logos/levimc-mods/icon-banner.svg` | `logos/levimc-mods/favicon.ico` | `logos/levimc-mods/apple-touch-icon.png` | `logos/levimc-mods/og-image.png` | `logos/levimc-mods/asset-family.zip` |

## Standard export sizes

- `icon.svg`: 512 × 512, transparent canvas, no project-name text.
- `icon-banner.svg`: 1200 × 240, transparent horizontal lockup; project name uses the LeviLamina leaf-green accent.
- `favicon.ico`: embedded 16, 32, 48, 64, 128, and 256 px images.
- `favicon-16x16.png`, `favicon-32x32.png`, `favicon-48x48.png`, `favicon-64x64.png`, `favicon-128x128.png`, `favicon-256x256.png`: explicit PNG derivatives.
- `apple-touch-icon.png`: 180 × 180.
- `og-image.svg`: editable 1200 × 630 source.
- `og-image.png`: 1200 × 630 raster export for social metadata.
- `variants/*.svg`: additional proposed design directions, each with its own standalone 512 × 512 source.

## Palette and source

The shared palette is sampled from the official [LeviLamina logo SVG](https://github.com/LiteLDev/LeviLamina/blob/main/docs/main/contents/logo.svg): `#294c2d`, `#52784d`, `#7ba46d`, `#90a08c`, and `#b9ccac`. Project-specific metaphors are built using these greens and restrained neutral tones rather than unrelated purple/blue palettes.

The assets are design proposals only; the `/official/` URL does not imply approval by LeviMC maintainers.
