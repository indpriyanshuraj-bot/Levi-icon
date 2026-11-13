# AGENT.md

Instructions for an AI assistant picking this repository up cold, or applying its artwork to a site.

## What this is

A review tool and icon library for **levimc.org**. Placements, file references and the current icons were read from
`LiteLDev/levimc.org` at commit `a391a35` (kit 2.2.0). The proposals are not merged upstream.

- Review app: https://indpriyanshuraj-bot.github.io/Levi-icon
- Repository: https://github.com/indpriyanshuraj-bot/Levi-icon

## Sets

`data.json` holds three sets. Each has its own folder and its own decisions.

| Set id | Title | Folder | State |
|---|---|---|---|
| `website` | Website icons | `assets/website/` | 20 placements, decided |
| `levi` | Levi project logos | `assets/levi/` | empty, ready for items |
| `miracle` | Miracle project logos | `assets/miracle/` | empty, ready for items |

To fill an empty set, add items to its `groups` in `data.json` and drop the SVGs in its folder. Nothing else.

## Where to get the artwork

**Use the published release, not the working tree.** CI optimises the SVGs and publishes them; that is the only
version guaranteed to match `data.json`.

| What | URL |
|---|---|
| Everything | `https://github.com/indpriyanshuraj-bot/Levi-icon/releases/latest/download/levimc-icons.zip` |
| Website icons | `…/releases/latest/download/website-icons.zip` |
| Levi logos | `…/releases/latest/download/levi-icons.zip` |
| Miracle logos | `…/releases/latest/download/miracle-icons.zip` |
| One icon | `…/releases/latest/download/<name>.svg` |
| Manifest | `…/releases/latest/download/manifest.json` |

`manifest.json` is the machine-readable index: per set, per icon — `name`, `path`, `title`, `palette` (the three
gradient stops), `accent` (the second colour) and `usedIn` (placement id, title, page, source `ref`, render `size`,
verdict).

## Reading data.json

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
maintainer's pick and shows as *recommended* in the app; `alt` shows as *alternative*.

## Applying a decision file

The app exports four formats — JSON, CSV, Markdown table, TXT — from **Review & export**. The JSON is the one to
parse:

```json
{
  "set": "website",
  "choices": [
    { "id": "platforms", "choice": "devices", "keep": false,
      "ref": "src/components/Features.tsx:13", "file": "assets/website/devices.svg" }
  ]
}
```

For every entry, replace the icon rendered at `ref` with `file`. `keep: true` means the current icon stays; `file` is
empty in that case. In levimc.org icons are `<PixelIcon name="…" />` from `kit/components`, so a replacement means
adding the sprite to `kit/assets/sprites.mjs` (or switching the component to the new file) — never paste SVG into a
page.

## Rules for the artwork — do not break these

- **Grid:** 24 × 24, `viewBox="0 0 24 24"`, no other size.
- **Stroke:** `stroke-width="1.8"`, `stroke-linecap="round"`, `stroke-linejoin="round"`, `fill="none"`.
- **Two colours, always.** Main stroke is a `<linearGradient id="g">` with three stops (light → base → dark). A second
  colour sits on one child element (a tick, a light, a button, a second person) and repeats as the offset shadow group
  at 30% opacity. Never flatten to one colour, never add a third hue.
- **Shadow group:** `<g stroke="{accent}" stroke-opacity=".3" transform="translate(.75 1)">` behind the main group.
  Keep the offset — it is what gives the set its depth.
- **Title:** every file has a `<title>`. Do not strip it.

### Palettes in use

| Subject | Body gradient | Accent |
|---|---|---|
| Product, gameplay, servers | `#8bcd9a → #4f8a5b → #2f5b3c` | `#e9c46a` |
| Developer (code, git) | `#6d7781 → #39424c → #171d22` | `#3e6e8e` blue, `#d23b3b` red for branches |
| Terminal | `#4a4a4a → #242424 → #0b0b0b` | `#4e9a06` Termux green |
| Content, identity | `#c8b8e3 → #9a86c2 → #67528f` | `#d98a9e` |
| Community, giving | `#f4c3d0 → #d98a9e → #a0576c` | `#e9c46a` |
| Books, history | `#b07a4c → #8b4a2b → #4a2413` | `#f4ecd6` cream |
| Neutral (language) | `#8d97a1 → #5b6570 → #2b333a` | none, gradient only |

## Things not to do

- Do not reintroduce the old multicolour pass (one blue→teal→orange ramp on every icon). It is what made the previous
  set unreadable at 16 px.
- Do not use `stroke="currentColor"`. The artwork owns its palette.
- Do not copy icons into a consumer site's own `assets/` folder when a release URL will do.
- Do not change a `verdict`. `best` is the maintainer's decision, not a suggestion.
- Do not reuse one icon name across two sets; CI fails the release on a duplicate.
