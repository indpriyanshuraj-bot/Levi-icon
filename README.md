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
| `assets/icons/*.svg` | the candidate icons, single-colour, tinted at runtime |

The current icons are **not stored here**. They are hotlinked from the `LiteLDev/levimc.org` repository
(`kit/assets/icons/`) through jsDelivr, with a `raw.githubusercontent.com` fallback, so the comparison always shows
what is live in the source rather than a copy that can drift.

Candidates are drawn through a CSS mask, which is why one single-colour SVG can carry any token colour without
being duplicated per palette. The tint is a three-stop gradient built from the token at runtime (light edge, token,
shadowed edge), so the artwork stays colourless and the palette stays in `data.json`.

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
- Decisions are stored in the browser. **Review** shows the sheet; **Download** in the header writes
  `levimc-icon-choices-<date>.json` at any time.
- That JSON is written to be handed straight to a maintainer or an AI: one entry per decided placement with `ref`,
  `size`, `from`, `to`, `file`, `colour` and an `instructions` line.

## Provenance

Placements, file references and the current icon set were read from `LiteLDev/levimc.org` at `a391a35`, kit 2.2.0.
The palette is the kit's own: `--color-primary`, `--color-accent-1..4`. LeviMC, LeviLamina and LeviLauncher remain
the property of their respective owners.
