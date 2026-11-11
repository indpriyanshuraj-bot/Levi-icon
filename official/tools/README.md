# V2 asset generation

From the repository root, run:

```sh
python -m pip install -r official/tools/requirements.txt
python official/tools/generate-identity-assets.py
python official/tools/retheme-projects.py
```

The first script builds the three SVG directions and base exports. The second script keeps the embedded LeviLamina leaf green, applies project-specific colours, adds extra detail to the preferred lip, LeviAntiCheat and LeviOptimize marks, and regenerates PNG/ICO derivatives and project bundles. Run both in order.

The gallery UI is shared with the root `index.html`, `styles.css` and `app.js`. `/official/` redirects to the V2 tab and does not contain a separate UI implementation.
