# SVG and asset generation

Run these commands from the repository root.

```sh
python -m pip install -r official/tools/requirements.txt
python official/tools/generate-identity-assets.py
python official/tools/generate-website-icon-styles.py
```

`generate-identity-assets.py` builds all project-logo SVG directions and their banner, favicon, Apple touch icon, OG and per-project ZIP exports. `generate-website-icon-styles.py` creates multicolour outline and multicolour filled derivatives of the website icon candidates while leaving original source SVGs untouched.
