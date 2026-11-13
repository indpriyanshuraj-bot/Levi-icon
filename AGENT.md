# AGENT.md

Instructions for an AI assistant working on this repository or applying this icon set to a site.

## What this is

An icon set and review tool for **levimc.org**. The placements, their file references and the current icons were read
from `LiteLDev/levimc.org` at commit `a391a35` (kit 2.2.0). The proposals here are not merged upstream.

- Review app: https://indpriyanshuraj-bot.github.io/Levi-icon
- Repository: https://github.com/indpriyanshuraj-bot/Levi-icon

## Where to get the icons

**Always use the published release, not the working tree.** The release is built by CI, optimised with SVGO, and is
the only version that is guaranteed to be consistent with `data.json`.

| What | URL |
|---|---|
| Whole set (zip) | `https://github.com/indpriyanshuraj-bot/Levi-icon/releases/latest/download/levimc-icons.zip` |
| One icon | `https://github.com/indpriyanshuraj-bot/Levi-icon/releases/latest/download/<name>.svg` |
| Manifest | `https://github.com/indpriyanshuraj-bot/Levi-icon/releases/latest/download/manifest.json` |
| Source of truth | `https://github.com/indpriyanshuraj-bot/Levi-icon/blob/main/data.json` |

The manifest is the machine-readable index: for every icon it gives `name`, `title`, `palette` (the three gradient
stops), `accent` (the second colour) and `usedIn` (placement id, title, page, source `ref`, render `size`, verdict).

## What each icon is

Read `data.json`, not a screenshot. Each item is:

```json
{
  "id": "platforms",
  "title": "Windows and Android",
  "ref": "src/components/Features.tsx:13",
  "size": 32,
  "current": { "name": "monitor", "palette": ["#26313a", "..."] },
  "options": [
    { "name": "devices", "token": "primary", "verdict": "best" },
    { "name": "laptop",  "token": "primary", "verdict": "alt"  }
  ]
}
```

`ref` is the exact place in levimc.org that renders the icon, `size` is the px it renders at. `verdict: "best"` is the
maintainer's pick; `alt` is the fallback.

## Applying a decision file

The review app exports `levimc-icon-choices-<date>.json`:

```json
{ "changes": [ { "id": "platforms", "ref": "src/components/Features.tsx:13", "size": 32,
                 "from": "monitor", "to": "devices", "action": "replace",
                 "file": "assets/icons/devices.svg", "colour": "#4f8a5b" } ] }
```

For every entry with `action: "replace"`, swap the icon rendered at `ref` for `file`. Skip `action: "keep"`. In
levimc.org the icons are `<PixelIcon name="…" />` from `kit/components`; a replacement means adding the new SVG to the
kit's sprite source (`kit/assets/sprites.mjs`) or switching the component to the new file — do not paste the SVG into
a page.

## Rules for the artwork — do not break these

- **Grid:** 24 × 24, `viewBox="0 0 24 24"`, no other size.
- **Stroke:** `stroke-width="1.8"`, `stroke-linecap="round"`, `stroke-linejoin="round"`, `fill="none"`.
- **Two colours, always.** The main stroke is a `<linearGradient id="g">` with three stops (light → token → dark).
  A second colour appears either on one child element (a tick, a light, a button) or as the offset shadow group.
  Never flatten an icon to a single colour, and never add a third hue.
- **Shadow group:** `<g stroke="{accent}" stroke-opacity=".3" transform="translate(.75 1)">` holds a copy of the
  geometry behind the main group. Keep the offset; it is what gives the set its depth.
- **Title:** every file has a `<title>` for accessibility. Do not strip it.
- **Palette:** only these tokens, taken from the levimc.org kit.

| Token | Hex | Use |
|---|---|---|
| `primary` | `#4f8a5b` | product, gameplay, servers, default |
| `pond` | `#3e6e8e` | anything developer-facing: code, git, terminal |
| `wisteria` | `#9a86c2` | content and identity: docs, files, accounts |
| `rose` | `#d98a9e` | community and giving |
| `sunlight` | `#c9922e` | attention and ideas, sparingly |

Accent pairings: `primary`/`pond`/`rose` → `#e9c46a`; `wisteria` → `#d98a9e`; `sunlight` → `#3e6e8e`.

## Adding an icon

1. Add `assets/icons/<name>.svg` following the rules above.
2. Add an entry to `data.json` under the right group with `id`, `title`, `ref`, `size`, `current` and `options`.
3. Push. CI validates, optimises, and publishes a new release. Nothing else to do — the app and the release both
   read from `data.json`.

## Things not to do

- Do not reintroduce the old multicolour gradient pass (one blue→teal→orange ramp on every icon). That is what made
  the previous set unreadable at 16 px.
- Do not use `stroke="currentColor"`. The set carries its own palette.
- Do not copy icons into a consumer site's own `assets/` folder when a release URL will do.
- Do not mark a placement as decided on the maintainer's behalf. `verdict: "best"` is theirs to change.
