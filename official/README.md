# LeviMC project identity concepts

A standalone review gallery and source collection for proposed project identities. **These concepts are unofficial and are not approved production logos.** The `official/` directory is a URL path for the collection, not an approval claim.

## Preview

- Gallery: open `/official/` on GitHub Pages.
- The gallery includes a global light/dark UI toggle and paired light/dark previews for every SVG concept. Each pair uses the same SVG file to make neutrality failures visible.
- Run locally from the repository root with `python3 -m http.server 8000`, then visit `http://localhost:8000/official/`.

## Projects included

- **LegacyScriptEngine** — predecessor lineage and compatibility with the earlier loader ecosystem.
- **lip** — general-purpose package installation and dependency resolution.
- **LeviAntiCheat** — protection, scanning and detection.
- **LeviOptimize** — computational efficiency and streamlined processing.
- **MoreDimensions** — science-fiction dimensional architecture and spatial transitions.
- **bedboo** — bot identity and API interoperability.
- **LeviMC Mods** — discovery and catalogue browsing.

Each project includes three proposed SVG directions. The first direction is used as `icon.svg`; the other two are preserved under `variants/`.

## Asset family

Every project has a consistent source/export family generated from its `icon.svg` master:

- `icon.svg` — 512 × 512 transparent vector master.
- `icon-banner.svg` — 1200 × 240 transparent icon + project-name lockup.
- `favicon.ico` — multi-resolution 16, 32, 48, 64, 128 and 256 px ICO.
- `favicon-*.png` — the same explicit favicon sizes as individual PNG files.
- `apple-touch-icon.png` — 180 × 180.
- `og-image.svg` and `og-image.png` — editable and raster 1200 × 630 social-card artwork.
- `asset-family.zip` — a per-project package containing all variants and derivatives.

The main SVG remains the source of truth. Raster derivatives should be regenerated rather than edited separately. See [`ASSET-INDEX.md`](ASSET-INDEX.md) for exact paths.

## Visual reference

The shared green family is sampled from the current official [LeviLamina logo SVG](https://github.com/LiteLDev/LeviLamina/blob/main/docs/main/contents/logo.svg): `#294c2d`, `#52784d`, `#7ba46d`, `#90a08c` and `#b9ccac`. The official leaf silhouette informs the shared botanical motif; each project receives a distinct primary metaphor while retaining this family language. The LeviLauncher identity is not redrawn here.

## Regenerate assets

```sh
python -m pip install -r official/tools/requirements.txt
python official/tools/generate-identity-assets.py
```

## License and status

The SVG concepts and gallery code are provided under the repository's MIT License. LeviMC and project names remain the property of their respective owners. This repository is independent and unaffiliated; these are proposals for review, not a claim of official endorsement.
