# LeviMC Icon Refresh Proposal

An unofficial, static showcase of icon replacement ideas for [LiteLDev/levimc.org](https://github.com/LiteLDev/levimc.org).

**This is a proposal, not an official LeviMC project or an approved design change.** It does not modify the source repository.

## What is included

- 15 source placements reviewed across the homepage, role selector, LeviLauncher showcase, About page, Support page, and blog navigation.
- 3 candidate SVGs per placement (45 proposed SVGs total).
- A “best fit” recommendation plus two alternatives for every placement.
- Approximate current-icon previews under `assets/icons/current/`. These are simple drawings based on the current icon names, **not extracted copies of the kit's pixel sprites**.
- A filterable comparison page and a copyable replacement map.
- A refreshed light UI with six consistent accent-colour groups; the existing-icon previews remain neutral grey so the proposed options stand out.

## Preview locally

Run a static HTTP server from this directory. For example, with Python:

```sh
python3 -m http.server 8000
```

Then open `http://localhost:8000`.

Opening `index.html` directly with a `file://` URL may prevent the page from fetching `data.json`; use a local HTTP server instead.

## Publish with GitHub Pages

1. Create a **public** GitHub repository and upload/push the contents of this folder.
2. In the repository, open **Settings → Pages** and select **GitHub Actions** as the build/deployment source.
3. Push to the `main` branch. The workflow in `.github/workflows/pages.yml` deploys the static site.

## Mapping overview

| Area | Current icon | Recommended | Alternatives |
|---|---|---|---|
| Homepage · Windows + Android | `monitor` | `devices` | `smartphone`, `laptop` |
| Homepage · One-command installs | `chest` | `terminal` | `download`, `package-check` |
| Homepage · Multiple languages | `bookQuill` | `code` | `languages`, `braces` |
| Homepage · Open source | `emerald` | `git-branch` | `github`, `code-merge` |
| Role · Play | `diamond` | `gamepad` | `blocks`, `person-play` |
| Role · Host | `monitor` | `server` | `network`, `database` |
| Role · Develop | `pickaxe` | `code` | `terminal`, `file-code` |
| LeviLauncher · Mod management | `chest` | `package-check` | `layers`, `blocks` |
| LeviLauncher · Accounts | `heart` | `user-round` | `users`, `id-card` |
| About · Story introduction | `bookQuill` | `book-open` | `file-text`, `scroll` |
| About · Why this project exists | `question` | `lightbulb` | `message-question`, `badge-help` |
| Support · Contribute | `pickaxe` | `git-pull-request` | `code`, `wrench` |
| Support · Donate | `emerald` | `heart-handshake` | `heart`, `circle-dollar` |
| Blog · Categories | `chest` | `folder` | `bookmark`, `grid` |
| Blog · About link | `quote` | `info` | `book-open`, `file-text` |

## Important implementation caveat

The live site uses the shared kit's pixel-art `PixelIcon` system. The candidate SVGs here are semantic and visual concept references; they are not drop-in `PixelIcon` names and should not be plugged into the React app as-is. After maintainers select concepts, redraw/adapt them to the kit's pixel grid and update the kit icon registry and its consumers.

## Source locations checked

- `src/components/Features.tsx`
- `src/components/Roles.tsx`
- `src/pages/About.tsx`
- `src/pages/Support.tsx`
- `src/blog/Blog.tsx`

The file paths identify the current placements at the time this proposal was prepared. Source may change independently.

## License

The SVG concepts and website code in this repository are provided under the MIT License. The LeviMC name and source project remain the property of their respective owners. This repository is independent and unaffiliated.
