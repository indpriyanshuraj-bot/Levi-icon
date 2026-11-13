#!/usr/bin/env python3
"""Build multicolour outline and multicolour filled presentations for the website icon proposals."""
from pathlib import Path
from xml.etree import ElementTree as ET
import copy

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'assets' / 'icons'
OUT = SOURCE / 'styles'
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)

def tag(name):
    return f'{{{NS}}}{name}'

# Semantic families use distinct but related accent triads; every mark has more than one hue.
PALETTES = {
    'blue': ('#244f83', '#24a6b8', '#e4a34e', '#e7f0f8', '#d9f2f1'),
    'cyan': ('#1c5879', '#19a9a6', '#ed9c4b', '#e0edf4', '#d8f1ed'),
    'violet': ('#51428c', '#a16dcb', '#e0a34d', '#ece7f7', '#f5e4f0'),
    'green': ('#285c45', '#2a9b87', '#e1a24c', '#e4f0e8', '#d8f1eb'),
    'orange': ('#985532', '#e18b42', '#358ca9', '#f5e9dc', '#e0edf3'),
    'rose': ('#8f3e62', '#dc6b77', '#e5aa4e', '#f5e3ea', '#f8e7df'),
}
FAMILIES = {
    'devices':'blue','laptop':'blue','smartphone':'blue','user-round':'blue','users':'blue','info':'blue','id-card':'blue',
    'terminal':'cyan','code':'cyan','braces':'cyan','file-code':'cyan','git-branch':'cyan','git-pull-request':'cyan','code-merge':'cyan','wrench':'cyan','network':'cyan',
    'languages':'violet','book-open':'violet','bookmark':'violet','file-text':'violet','scroll':'violet',
    'server':'green','database':'green','package-check':'green','layers':'green','blocks':'green','folder':'green','grid':'green','github':'green',
    'download':'orange','lightbulb':'orange','message-question':'orange','badge-help':'orange','circle-dollar':'orange',
    'gamepad':'rose','person-play':'rose','heart':'rose','heart-handshake':'rose',
}

def build_variant(src: Path, dest: Path, mode: str, palette):
    root = ET.parse(src).getroot()
    deep, accent, warm, pale, light = palette
    defs = ET.Element(tag('defs'))
    stroke = ET.SubElement(defs, tag('linearGradient'), {'id':'iconStroke','x1':'0','y1':'0','x2':'24','y2':'24','gradientUnits':'userSpaceOnUse'})
    for offset, color in (('0%', deep), ('48%', accent), ('100%', warm)):
        ET.SubElement(stroke, tag('stop'), {'offset':offset,'stop-color':color})
    fill = ET.SubElement(defs, tag('linearGradient'), {'id':'iconFill','x1':'0','y1':'0','x2':'24','y2':'24','gradientUnits':'userSpaceOnUse'})
    for offset, color in (('0%', pale), ('30%', accent), ('68%', warm), ('100%', light)):
        ET.SubElement(fill, tag('stop'), {'offset':offset,'stop-color':color})
    root.insert(0, defs)
    root.set('stroke', 'url(#iconStroke)' if mode == 'multicolor' else deep)
    root.set('stroke-width', '2.05' if mode == 'multicolor' else '1.9')
    for el in list(root):
        if el.tag == tag('title') or el.tag == tag('desc') or el.tag == tag('defs'):
            continue
        name = el.tag.rsplit('}', 1)[-1]
        if name not in {'path','rect','circle','ellipse','polygon','polyline','line'}:
            continue
        old_fill = el.attrib.get('fill', 'none')
        if mode == 'multicolor':
            if el.attrib.get('stroke', 'none') != 'none':
                el.set('stroke', 'url(#iconStroke)')
                el.set('stroke-width', '2.05')
            # Fill closed geometries while retaining open contours for visual separation.
            d = el.attrib.get('d', '')
            closed = ('Z' in d or 'z' in d)
            if name in {'rect','circle','ellipse','polygon'} or closed:
                el.set('fill', 'url(#iconFill)')
                el.set('fill-opacity', '0.96')
            elif old_fill != 'none':
                el.set('fill', warm)
        else:  # filled: multi-colour surfaces, with a dark keyline for definition
            if el.attrib.get('stroke', 'none') != 'none':
                el.set('stroke', deep)
                el.set('stroke-width', '1.9')
            d = el.attrib.get('d', '')
            closed = ('Z' in d or 'z' in d)
            if name in {'rect','circle','ellipse','polygon'} or closed:
                el.set('fill', 'url(#iconFill)')
                el.set('fill-opacity', '1')
            elif old_fill != 'none':
                el.set('fill', warm)
    # A tiny warm highlight ensures even a one-path outline glyph has an additional colour cue.
    # It sits inside the mark's lower-right visual quadrant and does not alter the icon's silhouette.
    highlight = ET.SubElement(root, tag('circle'), {
        'cx':'18.9','cy':'18.6','r':'1.45',
        'fill':warm if mode == 'multicolor' else accent,
        'stroke':deep,'stroke-width':'0.65'
    })
    title = root.find(tag('title'))
    if title is not None:
        title.text = (title.text or '').replace(' — ', ' · ') + (' · multicolour outline' if mode == 'multicolor' else ' · multicolour filled')
    root.set('width','96'); root.set('height','96')
    dest.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(root).write(dest, encoding='utf-8', xml_declaration=True)

for src in sorted(SOURCE.glob('*.svg')):
    name = src.stem
    palette = PALETTES[FAMILIES.get(name, 'blue')]
    build_variant(src, OUT/'multicolor'/src.name, 'multicolor', palette)
    build_variant(src, OUT/'filled'/src.name, 'filled', palette)

print(f'Generated {len(list(OUT.glob("multicolor/*.svg")))} multicolour and {len(list(OUT.glob("filled/*.svg")))} filled SVG variants.')
