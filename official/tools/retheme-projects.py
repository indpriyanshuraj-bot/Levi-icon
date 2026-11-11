"""Apply project-specific accent systems while retaining the original LeviLamina leaf.

Run after generate-identity-assets.py. Rebuilds all PNG/ICO derivatives and each
project asset-family.zip from the SVG masters.
"""
from pathlib import Path
from xml.etree import ElementTree as ET
from io import BytesIO
from PIL import Image, ImageDraw
import cairosvg, zipfile, json

ROOT = Path(__file__).resolve().parents[1]
LOGOS = ROOT / 'logos'
NS = '{http://www.w3.org/2000/svg}'
ET.register_namespace('', 'http://www.w3.org/2000/svg')
BASE = {
    '#294c2d':'forest', '#203b25':'deep', '#52784d':'mid', '#7ba46d':'leaf',
    '#90a08c':'sage', '#b9ccac':'pale', '#dce7d3':'mist', '#f1f4eb':'paper',
    '#f8faf5':'white', '#1d3322':'ink'
}
PALETTES = {
    'legacy-script-engine': {
        'forest':'#294c2d','deep':'#203b25','mid':'#52784d','leaf':'#7ba46d',
        'sage':'#90a08c','pale':'#b9ccac','mist':'#dce7d3','paper':'#f1f4eb','white':'#f8faf5','ink':'#1d3322',
        'accent':'#7ba46d','accent2':'#b9ccac','dark':'#203b25'
    },
    'lip': {
        'forest':'#183247','deep':'#102536','mid':'#23647d','leaf':'#20a8a3',
        'sage':'#75a9b3','pale':'#d2ecee','mist':'#e3f3f4','paper':'#edf7f7','white':'#fbfefe','ink':'#183247',
        'accent':'#20a8a3','accent2':'#e3a34f','dark':'#102536'
    },
    'levi-anticheat': {
        'forest':'#1b2a45','deep':'#111c31','mid':'#2c5f91','leaf':'#e36a69',
        'sage':'#7e9fbd','pale':'#e3ebf4','mist':'#edf3f8','paper':'#f3f6fb','white':'#fcfdff','ink':'#1b2a45',
        'accent':'#e36a69','accent2':'#44b8d0','dark':'#111c31'
    },
    'levioptimize': {
        'forest':'#1c2948','deep':'#101a32','mid':'#416bb0','leaf':'#27b6c8',
        'sage':'#879bc8','pale':'#d6e5f6','mist':'#e9f1fc','paper':'#f1f6fd','white':'#fcfdff','ink':'#1c2948',
        'accent':'#27b6c8','accent2':'#8568dc','dark':'#101a32'
    },
    'moredimensions': {
        'forest':'#25204d','deep':'#171333','mid':'#584b9b','leaf':'#9b70df',
        'sage':'#6caec5','pale':'#dce8f6','mist':'#eee7fa','paper':'#f6f3fc','white':'#fdfcff','ink':'#25204d',
        'accent':'#9b70df','accent2':'#49b5d2','dark':'#171333'
    },
    'bedboo': {
        'forest':'#1c344f','deep':'#112438','mid':'#2c6f8f','leaf':'#27a9b5',
        'sage':'#83a6b2','pale':'#d7ebef','mist':'#e7f4f5','paper':'#f1f8fa','white':'#fcfeff','ink':'#1c344f',
        'accent':'#27a9b5','accent2':'#eca65d','dark':'#112438'
    },
    'levimc-mods': {
        'forest':'#2a3453','deep':'#171f38','mid':'#6553a3','leaf':'#e0a04b',
        'sage':'#92a1be','pale':'#eee5f7','mist':'#f4eefb','paper':'#f8f5fc','white':'#fefcff','ink':'#2a3453',
        'accent':'#e0a04b','accent2':'#58a88c','dark':'#171f38'
    },
}

def recolour_tree(node, palette, preserve_leaf=True, skip_text=False):
    # The original botanical motif is a nested <g transform="... rotate(...) ...">.
    if preserve_leaf and node.tag == NS+'g' and 'rotate(' in node.attrib.get('transform',''):
        return
    if skip_text and node.tag == NS+'text':
        return
    for attr in ('fill','stroke','stop-color'):
        value = node.attrib.get(attr)
        if value in BASE:
            node.set(attr, palette[BASE[value]])
    for child in list(node):
        recolour_tree(child, palette, preserve_leaf=preserve_leaf, skip_text=skip_text)

def get_main_group(root):
    for child in list(root):
        if child.tag == NS+'g' and child.attrib.get('clip-path'):
            return child
    for child in list(root):
        if child.tag == NS+'g':
            return child
    raise RuntimeError('SVG has no main group')

def add_enhancements(slug, root, palette):
    g = get_main_group(root)
    def path(d, stroke, sw=9, fill='none', opacity='1'):
        ET.SubElement(g, NS+'path', {'d':d,'fill':fill,'stroke':stroke,'stroke-width':str(sw),'stroke-linecap':'round','stroke-linejoin':'round','opacity':opacity})
    def circle(cx,cy,r,fill,stroke,sw=6):
        ET.SubElement(g, NS+'circle', {'cx':str(cx),'cy':str(cy),'r':str(r),'fill':fill,'stroke':stroke,'stroke-width':str(sw)})
    if slug == 'lip':
        # Add dependency flow details and package-face markings without turning it into a parcel icon.
        path('M100 286 C127 250 160 232 194 220', palette['accent2'], 7, opacity='.95')
        path('M412 286 C385 250 352 232 318 220', palette['accent2'], 7, opacity='.95')
        path('M88 315 H117 M395 315 H424', palette['accent'], 8)
        circle(88,315,9,palette['accent2'],palette['forest'])
        circle(424,315,9,palette['accent2'],palette['forest'])
        for x in (238,256,274):
            path(f'M{x} 192 V211', palette['white'], 5, opacity='.95')
        path('M93 410 H112 M400 410 H419', palette['mid'], 6)
    elif slug == 'levi-anticheat':
        # Technical scan ticks and alert/verified markers give the shield a monitoring identity.
        path('M256 91 V113 M256 409 V431 M126 250 H148 M364 250 H386', palette['accent2'], 8)
        path('M166 153 C190 132 221 119 256 119 C291 119 322 132 346 153', palette['sage'], 6, opacity='.9')
        path('M166 355 C190 376 221 389 256 389 C291 389 322 376 346 355', palette['sage'], 6, opacity='.9')
        circle(170,170,9,palette['accent'],palette['forest'])
        circle(342,170,9,palette['accent2'],palette['forest'])
        circle(170,350,9,palette['accent2'],palette['forest'])
        circle(342,350,9,palette['accent'],palette['forest'])
    elif slug == 'levioptimize':
        # Extra execution lanes and telemetry nodes make this a compute core, not a speedometer.
        path('M72 173 H112 L142 191', palette['accent2'], 8)
        path('M72 303 H112 L142 285', palette['accent'], 8)
        path('M370 191 L400 173 H440', palette['accent2'], 8)
        path('M370 285 L400 303 H440', palette['accent'], 8)
        circle(72,173,10,palette['accent2'],palette['forest'])
        circle(72,303,10,palette['accent'],palette['forest'])
        circle(440,173,10,palette['accent2'],palette['forest'])
        circle(440,303,10,palette['accent'],palette['forest'])
        path('M213 150 L256 125 L299 150', palette['white'], 6, opacity='.9')
        path('M213 326 L256 351 L299 326', palette['white'], 6, opacity='.9')

for folder in sorted(p for p in LOGOS.iterdir() if p.is_dir()):
    slug = folder.name
    pal = PALETTES[slug]
    # Recolour every icon master and alternative. Leaf sub-groups retain LeviLamina green.
    for svg_path in [folder/'icon.svg', *sorted((folder/'variants').glob('*.svg'))]:
        root = ET.parse(svg_path).getroot()
        recolour_tree(root, pal, preserve_leaf=True)
        if svg_path.name == 'icon.svg':
            add_enhancements(slug, root, pal)
        ET.ElementTree(root).write(svg_path, encoding='utf-8', xml_declaration=False)
    # The icon in the banner/OG is recoloured; project-name typography deliberately stays leaf-green.
    for svg_path in (folder/'icon-banner.svg', folder/'og-image.svg'):
        root = ET.parse(svg_path).getroot()
        for child in list(root):
            recolour_tree(child, pal, preserve_leaf=True, skip_text=True)
        # Give any SVG gradients the project-specific dark base while preserving the shared wordmark green.
        for stop in root.iter(NS+'stop'):
            if stop.attrib.get('stop-color') in ('#203b25','#294c2d'):
                stop.set('stop-color', pal['dark'] if stop.attrib.get('stop-color') == '#203b25' else pal['forest'])
        for rect in root.findall(NS+'rect'):
            if rect.attrib.get('fill') == 'url(#bg)':
                rect.set('fill', pal['dark'])
        ET.ElementTree(root).write(svg_path, encoding='utf-8', xml_declaration=False)

    # Rebuild favicon/Apple touch/OG exports from the updated vector masters.
    icon_bytes = (folder/'icon.svg').read_bytes()
    for size in (16,32,48,64,128,256):
        png = cairosvg.svg2png(bytestring=icon_bytes, output_width=size, output_height=size)
        Image.open(BytesIO(png)).convert('RGBA').save(folder/f'favicon-{size}x{size}.png', optimize=True)
    base = Image.open(BytesIO(cairosvg.svg2png(bytestring=icon_bytes, output_width=256, output_height=256))).convert('RGBA')
    base.save(folder/'favicon.ico', format='ICO', sizes=[(16,16),(32,32),(48,48),(64,64),(128,128),(256,256)])
    mark = Image.open(BytesIO(cairosvg.svg2png(bytestring=icon_bytes, output_width=122, output_height=122))).convert('RGBA')
    app = Image.new('RGBA',(180,180),(255,255,255,255))
    draw = ImageDraw.Draw(app)
    draw.ellipse((7,7,173,173), fill=pal['paper'], outline=pal['sage'], width=2)
    app.alpha_composite(mark,((180-mark.width)//2,(180-mark.height)//2))
    app.convert('RGB').save(folder/'apple-touch-icon.png',quality=96)
    og_bytes = (folder/'og-image.svg').read_bytes()
    cairosvg.svg2png(bytestring=og_bytes, write_to=str(folder/'og-image.png'), output_width=1200, output_height=630)
    # Rebuild per-project package bundle; no icon.png is created.
    with zipfile.ZipFile(folder/'asset-family.zip','w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for f in sorted(folder.rglob('*')):
            if f.is_file() and f.name != 'asset-family.zip':
                z.write(f,f.relative_to(folder).as_posix())

# Update manifest palette with actual project-specific colors.
manifest_path = ROOT/'manifest.json'
manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
for project in manifest['projects']:
    pal = PALETTES[project['slug']]
    project['palette'] = [pal[k] for k in ('forest','mid','leaf','sage','pale')]
    project['accent_palette'] = {'primary':pal['accent'],'secondary':pal['accent2'],'dark':pal['dark']}
manifest['color_guidance'] = 'Project-specific accents are used in the product geometry. The embedded LeviLamina leaf remains in the official green palette as a secondary family mark.'
manifest_path.write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('Applied project-specific palettes, enriched lip/LeviAntiCheat/LeviOptimize, and regenerated raster derivatives/bundles.')
