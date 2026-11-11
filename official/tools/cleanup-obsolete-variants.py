from pathlib import Path

# Remove only the stale alternatives from the first gallery iteration. Missing files are expected.
root = Path(__file__).resolve().parents[1] / 'logos'
obsolete = [
    'legacy-script-engine/variants/dual-lineage.svg',
    'legacy-script-engine/variants/runtime-layers.svg',
    'lip/variants/open-module-set.svg',
    'lip/variants/dependency-chain.svg',
    'levi-anticheat/variants/protected-core.svg',
    'levi-anticheat/variants/radar-guard.svg',
    'levioptimize/variants/efficiency-crystal.svg',
    'levioptimize/variants/streamlined-paths.svg',
    'moredimensions/variants/spatial-cube.svg',
    'moredimensions/variants/interlocking-portals.svg',
    'bedboo/variants/api-bridge.svg',
    'bedboo/variants/node-bot.svg',
    'levimc-mods/variants/discovery-layers.svg',
    'levimc-mods/variants/catalogue-window.svg',
]
removed = 0
for rel in obsolete:
    target = root / rel
    if target.exists():
        target.unlink()
        removed += 1
print(f'Removed {removed} obsolete SVG variant files.')
