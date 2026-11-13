# LeviMC icon review

A comparison tool for the icons on [levimc.org](https://levimc.org): what each placement uses today, what is proposed
instead, and at the sizes it actually renders at.

Open the site: **https://indpriyanshuraj-bot.github.io/Levi-icon**

## How it works

The whole app is four files and no build step:

| File | Role |
|---|---|
| `data.json` | every placement, its current icon, its options and colours |
| `app.js` | reads `data.json` and renders the rail, the stage and the decision sheet |
| `styles.css` | the layout — landscape first, no page scroll |
| `assets/website/*.svg` | the website icon set |
| `assets/levi/*.svg`, `assets/miracle/*.svg` | the two logo sets, empty and ready |

The current icons are **not stored here**. They are hotlinked from the `LiteLDev/levimc.org` repository
(`kit/assets/icons/`) through jsDelivr, with a `raw.githubusercontent.com` fallback, so the comparison always shows
what is live in the source rather than a copy that can drift.

Each SVG carries its own two-tone artwork: a three-stop gradient stroke, one accent colour on a detail, and a soft
offset shadow. `data.json` decides which file each placement uses; the file decides the colour.

## Adding to it

1. Drop the new SVG in `assets/icons/` (24×24, `fill="none"`, `stroke-width` ~1.8, one stroke colour).
2. Add an entry to `data.json` under the right group:

```json
{
  "id": "blog-tags",
  "title": "Tags",
  "ref": "src/blog/Blog.tsx:22",
  "size": 16,
  "current": { "name": "hash", "palette": ["currentColor"] },
  "options": [
    { "name": "bookmark", "token": "wisteria", "verdict": "best" },
    { "name": "grid", "token": "wisteria", "verdict": "alt" }
  ]
}
```

`token` is one of `primary`, `pond`, `wisteria`, `rose`, `sunlight` (defined in `tokens` at the top of the file).
Use `"src"` instead of `"name"` if the icon lives somewhere else, e.g. a full-resolution project logo.

3. Push. `scripts/validate.mjs` runs first and fails the build if a referenced icon or token is missing, so a broken
entry never reaches the site.

Adding a whole new collection — project logos, favicons, anything with a current state and options — means adding a
second object to `collections` in `data.json`. The app already renders any number of them.

## Local preview

```sh
python3 -m http.server 8000
node scripts/validate.mjs
```

Then open `http://localhost:8000/`. Opening `index.html` from the file system will not work: the app fetches
`data.json`.

## Using it

- Click a placement in the left rail, or step through with `←` `→`.
- `↑` `↓` switch between the proposed options; `Enter` chooses the one on screen; `K` keeps the current icon.
- The app opens on a chooser: website icons, Levi project logos, Miracle project logos. Decisions are stored per set.
- **Review & export** shows the sheet and writes JSON, CSV, a Markdown table or TXT. The JSON is one entry per decided
  placement with `id`, `choice`, `ref` and `file` — nothing else, so it can be handed straight to a maintainer or an AI.

## Releases

Every push that touches `assets/` or `data.json` runs `.github/workflows/icons.yml`: it validates, optimises the SVGs
with SVGO, builds `manifest.json`, and publishes a release with a zip per set.

| What | URL |
|---|---|
| Whole set | `https://github.com/indpriyanshuraj-bot/Levi-icon/releases/latest/download/levimc-icons.zip` |
| One icon | `https://github.com/indpriyanshuraj-bot/Levi-icon/releases/latest/download/<name>.svg` |
| Manifest | `https://github.com/indpriyanshuraj-bot/Levi-icon/releases/latest/download/manifest.json` |

`AGENT.md` is written for an AI assistant picking this set up cold: where the icons live, what the grid and colour
rules are, and how to apply a decision file.

## Provenance

Placements, file references and the current icon set were read from `LiteLDev/levimc.org` at `a391a35`, kit 2.2.0.
The palette is the kit's own: `--color-primary`, `--color-accent-1..4`. LeviMC, LeviLamina and LeviLauncher remain
the property of their respective owners.
