from pathlib import Path
from xml.etree import ElementTree as ET
import json, re, hashlib, shutil
import cairosvg
from PIL import Image, ImageDraw
from io import BytesIO
import zipfile

BASE = Path(__file__).resolve().parents[2]
ROOT = BASE / 'official'
LOGO_ROOT = ROOT / 'logos'
LOGO_ROOT.mkdir(parents=True, exist_ok=True)

# Colours sampled directly from LiteLDev/LeviLamina/docs/main/contents/logo.svg.
C = {
    'forest': '#294c2d',
    'deep': '#203b25',
    'mid': '#52784d',
    'leaf': '#7ba46d',
    'sage': '#90a08c',
    'pale': '#b9ccac',
    'mist': '#dce7d3',
    'paper': '#f1f4eb',
    'white': '#f8faf5',
    'ink': '#1d3322',
}
F = C['forest']; D = C['deep']; M = C['mid']; L = C['leaf']; S = C['sage']; P = C['pale']; T = C['mist']; W = C['white']

PROJECT_PALETTES = {
    'legacy-script-engine': {'deep':'#294c2d','mid':'#52784d','leaf':'#7ba46d','sage':'#90a08c','pale':'#b9ccac','mist':'#dce7d3','paper':'#f1f4eb','white':'#f8faf5'},
    'lip': {'deep':'#17364b','mid':'#236f82','leaf':'#20a8a3','sage':'#78aab4','pale':'#d2ecee','mist':'#e7f4f3','paper':'#eff7f6','white':'#fbffff'},
    'levi-anticheat': {'deep':'#172d45','mid':'#2c5e8a','leaf':'#e36e70','sage':'#26a9c4','pale':'#e8f1f5','mist':'#d9e7f0','paper':'#f1f5f8','white':'#fbfcfe'},
    'levioptimize': {'deep':'#182d49','mid':'#476fc0','leaf':'#25b8c7','sage':'#8769d0','pale':'#e5a34f','mist':'#e9eff7','paper':'#f2f5fa','white':'#fcfdff'},
    'moredimensions': {'deep':'#25204d','mid':'#51458e','leaf':'#9b76df','sage':'#319dbb','pale':'#e47cc3','mist':'#e9e8f5','paper':'#f5f2fa','white':'#fdfbff'},
    'bedboo': {'deep':'#1c344f','mid':'#2c6f8f','leaf':'#27a9b5','sage':'#83a6b2','pale':'#d7ebef','mist':'#e5f2f4','paper':'#f1f7f8','white':'#fbfeff'},
    'levimc-mods': {'deep':'#362653','mid':'#68508d','leaf':'#9877c7','sage':'#d79a4b','pale':'#e9dcf4','mist':'#f1eafa','paper':'#f8f5fb','white':'#fffdfd'},
}
CURRENT_LOGOS = {
    'legacy-script-engine': ('https://raw.githubusercontent.com/LiteLDev/LegacyScriptEngine/develop/docs/img/logo.png','https://github.com/LiteLDev/LegacyScriptEngine/blob/develop/docs/img/logo.png'),
    'lip': ('https://raw.githubusercontent.com/LiteLDev/lip/main/docs/logo.png','https://github.com/LiteLDev/lip/blob/main/docs/logo.png'),
    'levi-anticheat': ('https://raw.githubusercontent.com/LiteLDev/LeviAntiCheat/release/docs/logo.png','https://github.com/LiteLDev/LeviAntiCheat/blob/release/docs/logo.png'),
    'levioptimize': ('https://raw.githubusercontent.com/LiteLDev/LeviOptimize/main/docs/logo.png','https://github.com/LiteLDev/LeviOptimize/blob/main/docs/logo.png'),
    'moredimensions': ('https://raw.githubusercontent.com/LiteLDev/MoreDimensions/develop/docs/logo.png','https://github.com/LiteLDev/MoreDimensions/blob/develop/docs/logo.png'),
    'bedboo': ('https://raw.githubusercontent.com/LiteLDev/bedboo/main/docs/public/logo.png','https://github.com/LiteLDev/bedboo/blob/main/docs/public/logo.png'),
    'levimc-mods': ('https://raw.githubusercontent.com/LiteLDev/levimc.org/main/mods/public/icon.png','https://github.com/LiteLDev/levimc.org/blob/main/mods/public/icon.png'),
}

def recolour_project_svg(svg: str, slug: str) -> str:
    palette = PROJECT_PALETTES[slug]
    replacements = {
        '#294c2d': palette['deep'], '#203b25': palette['deep'],
        '#52784d': palette['mid'], '#7ba46d': palette['leaf'],
        '#90a08c': palette['sage'], '#b9ccac': palette['pale'],
        '#dce7d3': palette['mist'], '#f1f4eb': palette['paper'],
        '#f8faf5': palette['white'],
    }
    for old, new in replacements.items():
        svg = svg.replace(old, new)
    return svg

# A consistent, organic LeviLamina-like botanical mark: one dominant blade, one
# smaller counter-leaf, and a descending stem. Kept as vector paths at every size.
def leaf_mark(x=256, y=256, scale=1.0, rotate=0, opacity=1.0):
    return f'''<g transform="translate({x} {y}) rotate({rotate}) scale({scale})" opacity="{opacity}">
      <path d="M-2 80 C-12 42 -5 -12 21 -62 C45 -108 89 -151 142 -172 C149 -114 138 -60 112 -16 C86 28 44 63 -2 80Z" fill="{L}" stroke="{F}" stroke-width="7" stroke-linejoin="round"/>
      <path d="M-2 80 C-33 56 -85 31 -112 -5 C-135 -36 -132 -71 -107 -91 C-65 -96 -23 -69 -4 -30 C8 -4 8 39 -2 80Z" fill="{P}" stroke="{M}" stroke-width="7" stroke-linejoin="round"/>
      <path d="M-3 82 C24 31 61 -42 139 -168" fill="none" stroke="{F}" stroke-width="8" stroke-linecap="round"/>
      <path d="M-7 54 C-45 27 -73 5 -110 -4" fill="none" stroke="{M}" stroke-width="7" stroke-linecap="round"/>
      <path d="M-3 83 C-7 116 -8 145 -4 177" fill="none" stroke="{F}" stroke-width="10" stroke-linecap="round"/>
      <path d="M24 27 C54 10 82 -12 100 -42 M43 -10 C69 -34 87 -58 103 -81 M-29 42 C-55 17 -75 4 -94 -2" fill="none" stroke="{S}" stroke-width="5" stroke-linecap="round"/>
    </g>'''

def path(d, fill='none', stroke=F, sw=12, extra=''):
    st = '' if stroke == 'none' else f' stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"'
    return f'<path d="{d}" fill="{fill}"{st} {extra}/>'
def circle(cx, cy, r, fill, stroke=F, sw=8, extra=''):
    st = '' if stroke == 'none' else f' stroke="{stroke}" stroke-width="{sw}"'
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"{st} {extra}/>'
def ellipse(cx, cy, rx, ry, fill, stroke=F, sw=8, extra=''):
    st = '' if stroke == 'none' else f' stroke="{stroke}" stroke-width="{sw}"'
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}"{st} {extra}/>'
def poly(points, fill, stroke=F, sw=10, extra=''):
    st = '' if stroke == 'none' else f' stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"'
    return f'<polygon points="{points}" fill="{fill}"{st} {extra}/>'
def rect(x,y,w,h,rx,fill,stroke=F,sw=10,extra=''):
    st = '' if stroke == 'none' else f' stroke="{stroke}" stroke-width="{sw}"'
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"{st} {extra}/>'

def outline(d, sw=18):
    # Dual outline makes the same vector readable on both a pale and a deep-green surface.
    return path(d, 'none', P, sw+9) + path(d, 'none', F, sw)

def svg_doc(title, desc, body, width=512, height=512, view='0 0 512 512'):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="{view}" role="img" aria-labelledby="title desc">
  <title id="title">{title}</title>
  <desc id="desc">{desc}</desc>
  <defs>
    <clipPath id="markClip"><rect x="0" y="0" width="512" height="512"/></clipPath>
  </defs>
  <g stroke-linecap="round" stroke-linejoin="round" clip-path="url(#markClip)">{body}</g>
</svg>\n'''
    ET.fromstring(svg)
    return svg

# Detailed, brand-coherent marks. Every direction is independently authored and
# is presented as an equal choice in the gallery. Root icon.svg is a naming convention.
PROJECTS = [
  {
    'name':'LegacyScriptEngine','slug':'legacy-script-engine',
    'summary':'A maintained compatibility layer for mods from the earlier Bedrock loader ecosystem.',
    'subtitle':'Legacy runtime compatibility',
    'og_pattern':'archive',
    'variants':[
      ('heritage-leaf','Heritage leaf','A maintained legacy crest: layered record plates, a mature botanical branch and a continuous lower stem express predecessor lineage without implying abandonment.',
       outline('M256 58 C319 88 365 101 393 116 V241 C393 323 344 393 256 451 C168 393 119 323 119 241 V116 C147 101 193 88 256 58Z',18)
       + path('M161 151 L256 113 L351 151 V235 C351 298 315 351 256 393 C197 351 161 298 161 235Z',T,M,10)
       + path('M190 214 C215 193 236 183 256 183 C276 183 297 193 322 214', 'none', S,10)
       + path('M177 267 H335 M194 300 H318 M214 332 H298', 'none', M,12)
       + path('M212 270 C230 245 251 235 276 236 C298 237 315 251 327 273', 'none', P,8)
       + leaf_mark(246,240,0.46,-8)
       + path('M202 371 C220 390 238 402 256 415 C274 402 292 390 310 371', 'none', L,9)),
      ('two-era-bridge','Two-era bridge','Two connected generations share one living stem, representing older scripts and APIs continuing inside the modern LeviLamina runtime.',
       outline('M104 299 C128 209 189 149 256 149 C323 149 384 209 408 299',20)
       + path('M114 309 C156 345 201 365 256 370 C311 365 356 345 398 309', 'none', S,15)
       + leaf_mark(218,285,0.62,-34)
       + leaf_mark(297,285,0.48,35,0.92)
       + path('M256 316 V409', 'none', F,12)
       + circle(256,414,13,L,F,7)
       + circle(122,302,12,P,M,7) + circle(390,302,12,P,M,7)
       + path('M140 233 C170 194 205 176 239 172 M273 172 C307 176 342 194 372 233', 'none', P,8)),
      ('runtime-strata','Runtime strata','Three substantial runtime strata are joined by a shared botanical spine to represent language and API compatibility.',
       poly('256,78 394,147 256,216 118,147',T,F,14)
       + poly('118,147 256,216 256,247 118,178',P,M,8)
       + poly('394,147 256,216 256,247 394,178',L,F,8)
       + poly('256,206 394,275 256,344 118,275', '#a9bf9d',F,14)
       + poly('118,275 256,344 256,376 118,307',S,F,8)
       + poly('394,275 256,344 256,376 394,307',M,F,8)
       + path('M256 216 V409', 'none', F,13)
       + leaf_mark(256,300,0.39,0)
       + path('M155 421 H357', 'none', P,10)),
    ]
  },
  {
    'name':'lip','slug':'lip','summary':'A general-purpose package installer that resolves packages and their dependencies through one command.',
    'subtitle':'Package and dependency installer','og_pattern':'packages',
    'variants':[
      ('package-lattice','Package lattice','Three interlocking isometric package modules form a compact dependency lattice; the Levi botanical mark is embedded into the central package face.',
       # top package
       poly('256,61 347,111 256,162 165,111',P,F,13)
       + poly('165,111 256,162 256,267 165,216',S,F,13)
       + poly('347,111 256,162 256,267 347,216',L,F,13)
       + path('M256 162 V267 M190 125 L256 162 L322 125', 'none',M,9)
       # lower side modules and dependency rails
       + poly('138,274 213,315 138,356 63,315',T,F,11)
       + poly('63,315 138,356 138,438 63,397',S,F,11)
       + poly('213,315 138,356 138,438 213,397',M,F,11)
       + poly('374,274 449,315 374,356 299,315',T,F,11)
       + poly('299,315 374,356 374,438 299,397',M,F,11)
       + poly('449,315 374,356 374,438 449,397',L,F,11)
       + path('M138 274 C165 248 188 233 210 224 M374 274 C347 248 324 233 302 224', 'none',P,15)
       + circle(138,274,10,L,F,5) + circle(374,274,10,L,F,5)
       + leaf_mark(256,252,0.27,-5)),
      ('dependency-constellation','Dependency constellation','A rooted package graph connects a primary package to dependent modules, showing resolution and installation order rather than delivery or shopping.',
       circle(256,248,104,T,F,14)
       + circle(256,248,72,L,M,10)
       + poly('256,172 319,208 319,280 256,316 193,280 193,208',P,F,10)
       + path('M256 315 V372 M193 245 H126 M319 245 H386', 'none',M,14)
       + path('M126 245 C105 245 92 258 92 278 M386 245 C407 245 420 258 420 278', 'none',F,12)
       + circle(92,292,26,S,F,8) + circle(420,292,26,S,F,8)
       + rect(219,370,74,62,16,P,F,10)
       + leaf_mark(256,262,0.28,-8)
       + path('M111 196 C150 114 361 114 401 196', 'none',S,9)),
      ('modular-cube','Modular cube',"A faceted installer core opens into three removable, linked modules; the central leaf acts as the package system's identity rather than a decorative sticker.",
       poly('256,83 383,153 256,224 129,153',T,F,15)
       + poly('129,153 256,224 256,384 129,313',S,F,15)
       + poly('383,153 256,224 256,384 383,313',L,F,15)
       + path('M256 224 V384 M179 181 L256 224 L333 181', 'none',M,10)
       + poly('256,268 312,299 256,331 200,299',P,F,9)
       + leaf_mark(256,310,0.22,-7)
       + circle(256,414,17,L,F,7)
       + path('M256 431 V456 M129 313 L99 330 M383 313 L413 330', 'none',F,11)),
    ]
  },
  {
    'name':'LeviAntiCheat','slug':'levi-anticheat','summary':'A detection and integrity layer for identifying suspicious client and server behaviour.',
    'subtitle':'Integrity monitoring and detection','og_pattern':'fingerprint',
    'variants':[
      ('integrity-fingerprint','Integrity fingerprint','A layered biometric-style trace pattern with a segmented scan pass. It communicates behavioural inspection and integrity analysis without defaulting to a shield or target.',
       path('M256 82 C184 82 132 129 120 194 C107 265 132 328 188 385', 'none', '#244d78', 22)
       + path('M256 121 C201 121 163 158 158 211 C152 264 175 309 216 345', 'none', '#e36e70', 18)
       + path('M256 160 C219 160 194 188 194 224 C194 264 214 292 244 312', 'none', '#26a9c4', 15)
       + path('M256 82 C328 82 380 129 392 194 C405 265 380 328 324 385', 'none', '#244d78', 22)
       + path('M256 121 C311 121 349 158 354 211 C360 264 337 309 296 345', 'none', '#26a9c4', 18)
       + path('M256 160 C293 160 318 188 318 224 C318 264 298 292 268 312', 'none', '#e36e70', 15)
       + path('M116 256 H396', 'none', '#e36e70', 9)
       + path('M154 256 H207 M305 256 H358', 'none', '#f2c27a', 6)
       + poly('256,219 291,239 291,279 256,299 221,279 221,239', '#e7f0f4', '#172d45', 10)
       + leaf_mark(255,258,0.105,-10)
       + circle(120,194,10,'#e36e70','#172d45',5) + circle(392,194,10,'#26a9c4','#172d45',5)),
      ('signal-weave','Signal weave','Three differently weighted signal paths weave across an inspection junction, showing continuous event observation and anomaly correlation.',
       path('M58 165 C139 165 154 221 220 221 C276 221 303 145 454 145', 'none', '#2c6d9d', 25)
       + path('M58 256 C139 256 163 256 224 256 C284 256 314 256 454 256', 'none', '#e36e70', 21)
       + path('M58 347 C139 347 154 291 220 291 C276 291 303 367 454 367', 'none', '#27a9bd', 25)
       + poly('256,164 349,256 256,348 163,256', '#e8eef5', '#172d45', 14)
       + poly('256,202 310,256 256,310 202,256', '#e36e70', '#172d45', 8)
       + path('M226 256 H286', 'none', '#f6d7a0', 9)
       + leaf_mark(256,256,0.095,0)
       + circle(58,165,13,'#e8eef5','#2c6d9d',7) + circle(58,347,13,'#e8eef5','#27a9bd',7)
       + circle(454,145,13,'#e8eef5','#2c6d9d',7) + circle(454,367,13,'#e8eef5','#27a9bd',7)),
      ('proof-lattice','Proof lattice','A compact integrity lattice uses interrupted paths and differently coloured verification nodes to represent cross-checking and tamper detection.',
       poly('256,58 410,147 410,325 256,414 102,325 102,147', '#e9eff5', '#172d45', 15)
       + path('M256 58 V414 M102 147 L410 325 M410 147 L102 325 M102 236 H410', 'none', '#537da4', 11)
       + path('M178 102 L178 370 M334 102 L334 370', 'none', '#26a9c4', 9)
       + poly('256,184 324,223 324,301 256,340 188,301 188,223', '#e36e70', '#172d45', 12)
       + path('M220 262 L246 287 L294 232', 'none', '#f7f0e6', 13)
       + leaf_mark(256,264,0.085,-8)
       + circle(102,147,12,'#26a9c4','#172d45',6) + circle(410,147,12,'#e36e70','#172d45',6)
       + circle(102,325,12,'#e9eff5','#537da4',6) + circle(410,325,12,'#e9eff5','#537da4',6)),
    ]
  },
  {
    'name':'LeviOptimize','slug':'levioptimize','summary':'A performance optimization project for reducing overhead across computational hot paths.',
    'subtitle':'Performance and execution efficiency','og_pattern':'flow','variants':[
      ('folded-impeller','Folded impeller','Four broad, offset execution blades form a compact computational rotor. Contrasting facets communicate reduced work and controlled throughput without a generic chip or speedometer.',
       '<g transform="rotate(0 256 256)"><path d="M256 53 C323 80 365 131 352 190 C344 229 303 247 256 257 C229 213 209 179 218 137 C224 103 238 75 256 53Z" fill="#25b8c7" stroke="#182d49" stroke-width="15" stroke-linejoin="round"/></g>'
       + '<g transform="rotate(90 256 256)"><path d="M256 53 C323 80 365 131 352 190 C344 229 303 247 256 257 C229 213 209 179 218 137 C224 103 238 75 256 53Z" fill="#476fc0" stroke="#182d49" stroke-width="15" stroke-linejoin="round"/></g>'
       + '<g transform="rotate(180 256 256)"><path d="M256 53 C323 80 365 131 352 190 C344 229 303 247 256 257 C229 213 209 179 218 137 C224 103 238 75 256 53Z" fill="#8769d0" stroke="#182d49" stroke-width="15" stroke-linejoin="round"/></g>'
       + '<g transform="rotate(270 256 256)"><path d="M256 53 C323 80 365 131 352 190 C344 229 303 247 256 257 C229 213 209 179 218 137 C224 103 238 75 256 53Z" fill="#e5a34f" stroke="#182d49" stroke-width="15" stroke-linejoin="round"/></g>'
       + poly('256,187 316,222 316,290 256,325 196,290 196,222', '#f0f4f8', '#182d49', 13)
       + poly('256,218 288,237 288,273 256,292 224,273 224,237', '#27b8c7', '#182d49', 8)
       + leaf_mark(256,256,0.095,-5)
       + path('M256 45 V22 M467 256 H490 M256 467 V490 M45 256 H22', 'none', '#a5b8d1', 8)),
      ('execution-weave','Execution weave','Three wide execution tracks merge through a faceted processor core, with a fourth return channel representing avoided repeated work.',
       path('M64 135 C142 135 160 201 220 219 C244 226 268 222 291 208 C351 173 376 128 448 128', 'none', '#25b8c7', 25)
       + path('M64 256 H448', 'none', '#476fc0', 24)
       + path('M64 377 C142 377 160 311 220 293 C244 286 268 290 291 304 C351 339 376 384 448 384', 'none', '#e5a34f', 25)
       + poly('256,151 361,212 361,300 256,361 151,300 151,212', '#e9eff7', '#182d49', 15)
       + poly('256,192 309,223 309,289 256,320 203,289 203,223', '#8769d0', '#182d49', 10)
       + leaf_mark(256,264,0.10,0)
       + path('M405 95 L448 128 L405 161 M405 351 L448 384 L405 417', 'none', '#182d49', 10)),
      ('cache-strata','Cache strata','A tiered sequence of compressed processing plates narrows into a shared execution path. The asymmetric facets suggest batching and less repeated work.',
       poly('256,70 420,157 256,244 92,157', '#25b8c7', '#182d49', 15)
       + poly('92,157 256,244 256,283 92,196', '#476fc0', '#182d49', 10)
       + poly('420,157 256,244 256,283 420,196', '#e5a34f', '#182d49', 10)
       + poly('256,221 420,308 256,395 92,308', '#8769d0', '#182d49', 15)
       + poly('92,308 256,395 256,430 92,343', '#25b8c7', '#182d49', 10)
       + poly('420,308 256,395 256,430 420,343', '#476fc0', '#182d49', 10)
       + path('M256 244 V430 M142 157 L256 217 L370 157', 'none', '#f3f6fa', 9)
       + leaf_mark(256,326,0.10,0)
       + path('M154 455 H358', 'none', '#e5a34f', 12)),
    ]
  },
  {
    'name':'MoreDimensions','slug':'moredimensions','summary':'A science-fiction dimensional architecture API for adding custom Bedrock dimensions.',
    'subtitle':'Spatial architecture and dimensional APIs','og_pattern':'phase',
    'variants':[
      ('phase-prism','Phase prism','Offset coordinate planes and a fractured central prism create a layered science-fiction spatial object. The composition suggests multiple coexisting dimensional spaces, not a fantasy portal.',
       poly('256,48 421,143 421,337 256,432 91,337 91,143', '#292353', '#211c4b', 15)
       + poly('256,48 421,143 256,238 91,143', '#9b76df', '#211c4b', 11)
       + poly('91,143 256,238 256,432 91,337', '#51458e', '#211c4b', 11)
       + poly('421,143 256,238 256,432 421,337', '#319dbb', '#211c4b', 11)
       + path('M132 119 L297 24 L462 119 L462 313', 'none', '#5dc5dd', 10, 'opacity=".75"')
       + path('M132 119 V313 L297 408', 'none', '#e47cc3', 10, 'opacity=".85"')
       + poly('256,174 326,214 326,296 256,336 186,296 186,214', '#eff0fa', '#211c4b', 12)
       + poly('256,203 298,227 298,279 256,303 214,279 214,227', '#e47cc3', '#211c4b', 8)
       + leaf_mark(256,254,0.085,-8)
       + path('M64 256 H104 M408 256 H448 M256 32 V70 M256 410 V464', 'none', '#f2b4d8', 8)),
      ('coordinate-fold','Coordinate fold','Three displaced coordinate grids fold through a shared origin. Perspective offsets and interrupted edges give the symbol a precise dimensional-engineering feel.',
       poly('256,68 390,145 390,300 256,377 122,300 122,145', 'none', '#292353', 17)
       + path('M256 68 V224 M122 145 L256 224 L390 145 M256 224 V377 M122 300 L256 224 L390 300', 'none', '#4b83bc', 14)
       + path('M160 112 L294 190 V346 M352 119 L218 197 V352', 'none', '#b06ee0', 12)
       + poly('256,162 332,206 332,294 256,338 180,294 180,206', '#55b5d0', '#292353', 12)
       + poly('256,197 304,225 304,275 256,303 208,275 208,225', '#ef8abf', '#292353', 8)
       + leaf_mark(256,249,0.08,0)
       + circle(122,145,11,'#e9e6fa','#292353',6) + circle(390,145,11,'#55b5d0','#292353',6)
       + circle(122,300,11,'#b06ee0','#292353',6) + circle(390,300,11,'#ef8abf','#292353',6)),
      ('dimensional-shear','Dimensional shear','Offset slabs of space overlap at different depths. The diagonal shear and split facets represent transitions between coordinate systems and custom dimensions.',
       poly('256,62 404,147 256,232 108,147', '#b184e9', '#25204d', 14)
       + poly('108,147 256,232 256,410 108,325', '#55499a', '#25204d', 14)
       + poly('404,147 256,232 256,410 404,325', '#36a8c4', '#25204d', 14)
       + poly('299,30 447,115 299,200 151,115', 'none', '#df78be', 10, 'opacity=".9"')
       + path('M151 115 V293 L299 378 L447 293 V115', 'none', '#68c9df', 10)
       + poly('256,188 316,223 316,291 256,326 196,291 196,223', '#eef0fa', '#25204d', 11)
       + path('M224 240 L288 277 M288 240 L224 277', 'none', '#df78be', 9)
       + leaf_mark(256,258,0.075,-8)),
    ]
  },
  {
    'name':'bedboo','slug':'bedboo','summary':'A bot library with a Mineflayer-compatible API surface and a Bedrock-focused identity.',
    'subtitle':'Bot library and API bridge','og_pattern':'network','variants':[
      ('bot-bridge','Bot bridge','A custom bot core is framed by API connection ports and a botanical antenna, conveying programmable agents and Mineflayer-compatible integration.',
       # top antenna and branching connector lines
       path('M256 71 V119 M256 119 C256 137 216 139 197 154 M256 119 C256 137 296 139 315 154', 'none',M,13)
       + circle(256,65,16,P,F,7)
       + circle(197,154,11,S,F,6) + circle(315,154,11,S,F,6)
       + rect(111,150,290,252,58,T,F,16)
       + rect(128,168,256,216,45,L,M,9)
       + path('M111 245 H75 V293 H111 M401 245 H437 V293 H401', 'none',F,13)
       + circle(75,269,14,P,F,7) + circle(437,269,14,P,F,7)
       + ellipse(204,256,24,31,P,F,8) + ellipse(308,256,24,31,P,F,8)
       + path('M203 326 C231 350 281 350 309 326', 'none',F,12)
       + leaf_mark(256,180,0.16,-1)
       + path('M165 402 V429 H347 V402', 'none',S,10)
       + circle(256,429,10,L,F,5)),
      ('api-bridge','API bridge','A central agent node connects to three differently shaped API ports, making the integration and transport layer the main visual idea.',
       circle(256,253,88,T,F,15)
       + circle(256,253,59,L,M,10)
       + leaf_mark(256,265,0.19,0)
       + path('M168 253 H91 V188 M344 253 H421 V188 M256 341 V411', 'none',F,16)
       + rect(55,116,73,73,18,P,F,10)
       + rect(384,116,73,73,18,P,F,10)
       + poly('256,393 300,418 256,443 212,418',S,F,9)
       + path('M80 151 H103 M409 151 H432 M244 418 H268', 'none',M,8)
       + circle(91,188,10,L,F,5) + circle(421,188,10,L,F,5)),
      ('autonomous-agent','Autonomous agent','A compact modular agent silhouette includes directional sensor fins, an articulated base and a leaf-shaped status mark.',
       path('M165 178 C165 131 203 101 256 101 C309 101 347 131 347 178 V323 C347 369 309 398 256 398 C203 398 165 369 165 323Z',F,P,14)
       + path('M190 190 C190 154 216 132 256 132 C296 132 322 154 322 190 V311 C322 347 296 368 256 368 C216 368 190 347 190 311Z',T,F,10)
       + path('M165 230 H125 L98 203 M347 230 H387 L414 203', 'none',M,13)
       + circle(98,203,12,L,F,6) + circle(414,203,12,L,F,6)
       + ellipse(224,248,16,21,P,F,6) + ellipse(288,248,16,21,P,F,6)
       + path('M216 309 C238 327 274 327 296 309', 'none',F,12)
       + leaf_mark(256,177,0.14,0)
       + path('M209 399 V430 M303 399 V430 M187 430 H325', 'none',F,11)),
    ]
  },
  {
    'name':'LeviMC Mods','slug':'levimc-mods','summary':'A curated catalogue for discovering and browsing LeviMC-compatible mods and tools.',
    'subtitle':'Mod discovery and catalogue','og_pattern':'catalogue','variants':[
      ('curated-catalogue','Curated catalogue','A structured catalogue of modular cards is arranged around a central discovery mark, balancing browsing, curation and the Levi botanical family cue.',
       rect(87,91,338,330,40,T,F,16)
       + rect(111,115,290,58,18,P,M,8)
       + circle(143,144,9,L,'none',0) + circle(171,144,9,S,'none',0) + circle(199,144,9,M,'none',0)
       + rect(119,204,112,87,18,P,F,9) + rect(281,204,112,87,18,P,F,9)
       + rect(119,315,112,80,18,S,F,9) + rect(281,315,112,80,18,L,F,9)
       + path('M139 264 H210 M301 264 H372 M139 369 H210 M301 369 H372', 'none',M,7)
       + circle(256,299,72,F,P,10)
       + circle(256,299,49,T,S,8)
       + leaf_mark(256,312,0.15,0)
       + path('M307 348 L357 398', 'none',F,16)
       + circle(361,402,15,P,F,7)),
      ('discovery-orbit','Discovery orbit','A discovery lens follows a ring of modular entries, representing search, sorting and exploration across a growing mod ecosystem.',
       circle(250,247,138,'none',S,12)
       + circle(250,247,105,T,F,11)
       + rect(187,181,70,70,15,P,F,9)
       + rect(274,181,70,70,15,S,F,9)
       + rect(187,267,70,70,15,L,F,9)
       + rect(274,267,70,70,15,P,F,9)
       + path('M350 344 L421 415', 'none',F,20)
       + circle(356,350,35,T,F,10)
       + leaf_mark(250,264,0.15,0)
       + path('M112 247 H82 M250 109 V80 M250 385 V414', 'none',M,9)),
      ('module-shelf','Module shelf','A tiered set of installed module tiles sits in a stable catalogue frame, with an embedded leaf marking the curated source.',
       path('M102 150 H410 L382 204 H130Z',T,F,13)
       + path('M130 204 H382 V378 H130Z',P,F,13)
       + path('M150 229 H362 M150 285 H362 M150 341 H362', 'none',S,9)
       + rect(154,224,71,48,12,S,F,7) + rect(244,224,71,48,12,L,F,7) + rect(334,224,28,48,9,P,F,7)
       + rect(154,292,71,40,10,P,F,7) + rect(244,292,71,40,10,S,F,7) + rect(334,292,28,40,9,L,F,7)
       + path('M94 397 H418 L395 439 H117Z',M,F,10)
       + leaf_mark(256,157,0.12,0)
       + circle(256,446,11,P,F,5)),
    ]
  },
]

# Build project manifests, one current-vs-proposed comparison, and all per-variant assets.
manifest = {
  'title':'LeviMC project identity concepts',
  'status':'Unofficial concepts for review. The /official/ route is a collection path, not an approval claim.',
  'reference': {
    'name':'LeviLamina official vector identity',
    'source':'https://github.com/LiteLDev/LeviLamina/blob/main/docs/main/contents/logo.svg',
    'palette':C,
    'style_note':'The original LeviLamina leaf silhouette and forest-green palette are used as a family reference; individual projects retain their own palettes.'
  },
  'projects':[], 'icons':[]
}

def project_palette(slug):
    return PROJECT_PALETTES[slug]

def create_banner(project, variant_body, palette, slug, variant_label):
    # The only decorative line is an underline well below the subtitle; no line intersects text.
    name = project['name']; subtitle = project['subtitle']
    mark = f'<g transform="translate(28 17) scale(.38)">{variant_body}</g>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="240" viewBox="0 0 1200 240" role="img" aria-labelledby="title desc">
<title id="title">{name} — {variant_label} banner</title><desc id="desc">{subtitle}; project identity concept.</desc>
{mark}
<text x="268" y="112" fill="{palette['deep']}" stroke="{palette['paper']}" stroke-width="4" stroke-linejoin="round" paint-order="stroke fill" font-family="Inter,Segoe UI,sans-serif" font-size="62" font-weight="760" letter-spacing="-1.4">{name}</text>
<text x="271" y="157" fill="{palette['deep']}" stroke="{palette['paper']}" stroke-width="2" stroke-linejoin="round" paint-order="stroke fill" font-family="Inter,Segoe UI,sans-serif" font-size="26" font-weight="620">{subtitle}</text>
<path d="M271 216 H414" stroke="{palette['leaf']}" stroke-width="5" stroke-linecap="round"/>
</svg>\n'''

def create_og(project, variant_body, palette, variant_label):
    name = project['name']; subtitle = project['subtitle']; summary = project['summary']
    # Each project gets a flat editorial composition and its own palette. No green wash or circular logo medallion.
    pattern = {
      'archive': f'<g opacity=".18" stroke="{palette["mid"]}" stroke-width="5"><path d="M1010 100 V500 M1070 100 V500 M1130 100 V500"/><path d="M990 160 H1170 M990 300 H1170 M990 440 H1170"/></g>',
      'packages': f'<g fill="none" stroke-width="8" opacity=".20"><path d="M1000 145 L1080 100 L1160 145 L1080 190Z M1000 290 L1080 245 L1160 290 L1080 335Z M1080 190 V245" stroke="{palette["mid"]}"/><path d="M1080 335 V390" stroke="{palette["leaf"]}"/></g>',
      'fingerprint': f'<g fill="none" stroke-width="9" opacity=".18"><path d="M1035 110 V520 M1085 110 V520 M1135 110 V520" stroke="{palette["mid"]}"/><path d="M1005 210 H1160 M1005 360 H1160" stroke="{palette["leaf"]}"/></g>',
      'flow': f'<g fill="none" stroke-width="18" stroke-linecap="round" opacity=".20"><path d="M970 145 H1145 L1105 110 M970 315 H1145 L1105 280 M970 485 H1145 L1105 450" stroke="{palette["leaf"]}"/></g>',
      'phase': f'<g fill="none" stroke-width="8" opacity=".20"><path d="M1000 160 L1100 100 L1180 146 V440 L1100 500 L1000 440Z" stroke="{palette["leaf"]}"/><path d="M1045 190 L1125 144 V390 L1045 436" stroke="{palette["sage"]}"/><path d="M1000 300 H1180" stroke="{palette["pale"]}"/></g>',
      'network': f'<g fill="none" stroke-width="8" opacity=".20"><path d="M1010 150 L1100 250 L1180 150 M1010 420 L1100 320 L1180 420 M1100 250 V320" stroke="{palette["mid"]}"/><circle cx="1010" cy="150" r="10" fill="{palette["leaf"]}"/><circle cx="1180" cy="150" r="10" fill="{palette["pale"]}"/><circle cx="1010" cy="420" r="10" fill="{palette["sage"]}"/></g>',
      'catalogue': f'<g fill="none" stroke="{palette["mid"]}" stroke-width="6" opacity=".18">' + ''.join(f'<rect x="{x}" y="{y}" width="60" height="72" rx="9"/>' for x,y in ((1000,130),(1080,130),(1160,130),(1000,225),(1080,225),(1160,225),(1000,320),(1080,320),(1160,320))) + '</g>'
    }.get(project['og_pattern'], '')
    title_size = 53 if len(name) > 14 else 64
    words = summary.split(); summary_lines=[]; line=''
    for word in words:
        candidate = (line + ' ' + word).strip()
        if len(candidate) > 48 and line:
            summary_lines.append(line); line = word
        else:
            line = candidate
    if line: summary_lines.append(line)
    summary_markup = ''.join(f'<tspan x="548" dy="{0 if i==0 else 29}">{line}</tspan>' for i,line in enumerate(summary_lines[:3]))
    # The mark sits in a project-tinted rectangular panel, not a circle.
    icon_panel = f'<rect x="52" y="82" width="410" height="466" rx="30" fill="{palette["paper"]}" stroke="{palette["mist"]}" stroke-width="3"/>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630" role="img" aria-labelledby="title desc">
<title id="title">{name} — LeviMC project identity concept</title><desc id="desc">{summary}</desc>
<rect width="1200" height="630" fill="#f6f7f8"/>
<path d="M0 0 H1200 V44 H0Z" fill="{palette['deep']}"/>
<path d="M500 80 H1200 V630 H500Z" fill="#fbfcfd"/>
{pattern}
{icon_panel}
<g transform="translate(72 102) scale(.72)">{variant_body}</g>
<text x="548" y="178" fill="{palette['mid']}" font-family="Inter,Segoe UI,sans-serif" font-size="19" font-weight="750" letter-spacing="4">LEVI MC PROJECT CONCEPT</text>
<text x="544" y="267" fill="#17202b" font-family="Inter,Segoe UI,sans-serif" font-size="{title_size}" font-weight="780" letter-spacing="-1.7">{name}</text>
<text x="548" y="327" fill="{palette['mid']}" font-family="Inter,Segoe UI,sans-serif" font-size="27" font-weight="650">{subtitle}</text>
<text x="548" y="389" fill="#4b5563" font-family="Inter,Segoe UI,sans-serif" font-size="18">{summary_markup}</text>
<path d="M548 474 H690" stroke="{palette['leaf']}" stroke-width="6" stroke-linecap="round"/>
<text x="548" y="540" fill="#68717e" font-family="Inter,Segoe UI,sans-serif" font-size="16" font-weight="650" letter-spacing="2">UNOFFICIAL DESIGN STUDY · FOR REVIEW</text>
</svg>\n'''

def export_assets(folder, project, variant_slug, variant_label, icon_svg, variant_body, palette):
    icon_path = folder/'icon.svg' if variant_slug == 'primary' else folder/'variants'/f'{variant_slug}.svg'
    if variant_slug == 'primary':
        banner_path = folder/'icon-banner.svg'
        fav_path = folder/'favicon.ico'
        apple_path = folder/'apple-touch-icon.png'
        og_svg_path = folder/'og-image.svg'
        og_png_path = folder/'og-image.png'
        stem = folder
    else:
        banner_path = folder/'variants'/f'{variant_slug}-banner.svg'
        fav_path = folder/'variants'/f'{variant_slug}-favicon.ico'
        apple_path = folder/'variants'/f'{variant_slug}-apple-touch-icon.png'
        og_svg_path = folder/'variants'/f'{variant_slug}-og-image.svg'
        og_png_path = folder/'variants'/f'{variant_slug}-og-image.png'
        stem = folder/'variants'
    banner = create_banner(project, variant_body, palette, project['slug'], variant_label)
    ET.fromstring(banner); banner_path.write_text(banner,encoding='utf-8')
    og_svg = create_og(project, variant_body, palette, variant_label)
    ET.fromstring(og_svg); og_svg_path.write_text(og_svg,encoding='utf-8')
    # Apple touch artwork uses a restrained project-tinted square canvas, not a green circular badge.
    icon180 = cairosvg.svg2png(bytestring=icon_svg.encode(),output_width=148,output_height=148)
    mark = Image.open(BytesIO(icon180)).convert('RGBA')
    app = Image.new('RGBA',(180,180),palette['paper'])
    app.alpha_composite(mark,((180-mark.width)//2,(180-mark.height)//2))
    app.convert('RGB').save(apple_path,quality=95)
    for sz in (16,32,48,64,128,256):
        data = cairosvg.svg2png(bytestring=icon_svg.encode(),output_width=sz,output_height=sz)
        Image.open(BytesIO(data)).convert('RGBA').save(stem/f'{variant_slug}-favicon-{sz}x{sz}.png' if variant_slug!='primary' else folder/f'favicon-{sz}x{sz}.png',optimize=True)
    base = Image.open(BytesIO(cairosvg.svg2png(bytestring=icon_svg.encode(),output_width=256,output_height=256))).convert('RGBA')
    base.save(fav_path,format='ICO',sizes=[(16,16),(32,32),(48,48),(64,64),(128,128),(256,256)])
    cairosvg.svg2png(bytestring=og_svg.encode(),write_to=str(og_png_path),output_width=1200,output_height=630)
    return banner_path, fav_path, apple_path, og_svg_path, og_png_path

for project in PROJECTS:
    slug = project['slug']; folder = LOGO_ROOT/slug; folder.mkdir(parents=True,exist_ok=True)
    # Remove stale variant exports so renamed/removed concepts cannot linger in bundles.
    variants_dir = folder/'variants'
    if variants_dir.exists():
        shutil.rmtree(variants_dir)
    palette = project_palette(slug)
    current_url, current_source = CURRENT_LOGOS[slug]
    variants=[]
    for idx,(variant_slug,label,description,body) in enumerate(project['variants']):
        svg = svg_doc(f"{project['name']} — {label}", description, body)
        svg = recolour_project_svg(svg,slug)
        if idx == 0:
            icon_path = folder/'icon.svg'; file_path=f'logos/{slug}/icon.svg'
        else:
            (folder/'variants').mkdir(exist_ok=True)
            icon_path = folder/'variants'/f'{variant_slug}.svg'; file_path=f'logos/{slug}/variants/{variant_slug}.svg'
        icon_path.write_text(svg,encoding='utf-8')
        # recolour embedded body for text/banner/OG source as well
        body_for_export = recolour_project_svg(body,slug)
        banner_path, fav_path, apple_path, og_svg_path, og_png_path = export_assets(folder,project,'primary' if idx==0 else variant_slug,label,svg,body_for_export,palette)
        variant = {
            'slug':variant_slug,'label':label,'description':description,'file':file_path,
            'banner':f'logos/{slug}/icon-banner.svg' if idx==0 else f'logos/{slug}/variants/{variant_slug}-banner.svg',
            'favicon':f'logos/{slug}/favicon.ico' if idx==0 else f'logos/{slug}/variants/{variant_slug}-favicon.ico',
            'apple_touch_icon':f'logos/{slug}/apple-touch-icon.png' if idx==0 else f'logos/{slug}/variants/{variant_slug}-apple-touch-icon.png',
            'og_image':f'logos/{slug}/og-image.png' if idx==0 else f'logos/{slug}/variants/{variant_slug}-og-image.png',
            'og_image_svg':f'logos/{slug}/og-image.svg' if idx==0 else f'logos/{slug}/variants/{variant_slug}-og-image.svg',
        }
        variants.append(variant)
        manifest['icons'].append({'project':project['name'],'project_slug':slug,**variant,'summary':project['summary']})
    manifest['projects'].append({
      'name':project['name'],'slug':slug,'summary':project['summary'],'subtitle':project['subtitle'],
      'palette':[palette[k] for k in ('deep','mid','leaf','sage','pale')],
      'current_icon':current_url,'current_source':current_source,
      'icon':'logos/'+slug+'/icon.svg','banner':'logos/'+slug+'/icon-banner.svg',
      'favicon':'logos/'+slug+'/favicon.ico','apple_touch_icon':'logos/'+slug+'/apple-touch-icon.png',
      'og_image':'logos/'+slug+'/og-image.png','og_image_svg':'logos/'+slug+'/og-image.svg',
      'asset_bundle':'logos/'+slug+'/asset-family.zip','variants':variants
    })
    with zipfile.ZipFile(folder/'asset-family.zip','w',zipfile.ZIP_DEFLATED,compresslevel=9) as bundle:
        for asset in sorted(folder.rglob('*')):
            if asset.is_file() and asset.name != 'asset-family.zip':
                bundle.write(asset,asset.relative_to(folder).as_posix())

(ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

# Gallery-owned icon family, derived from the same branded botanical master.
site_body = leaf_mark(256,256,0.72,0)
site_svg = svg_doc('LeviMC project identity gallery','A botanical mark based on the current LeviLamina family identity.',site_body)
(ROOT/'site-icon.svg').write_text(site_svg,encoding='utf-8')
site_png = cairosvg.svg2png(bytestring=site_svg.encode(),output_width=180,output_height=180)
mark = Image.open(BytesIO(site_png)).convert('RGBA')
site_touch = Image.new('RGBA',(180,180),'#f6f7f8'); site_touch.alpha_composite(mark)
site_touch.convert('RGB').save(ROOT/'apple-touch-icon.png',quality=95)
for sz in (16,32,48,64,128,256):
    Image.open(BytesIO(cairosvg.svg2png(bytestring=site_svg.encode(),output_width=sz,output_height=sz))).save(ROOT/f'favicon-{sz}x{sz}.png',optimize=True)
Image.open(BytesIO(cairosvg.svg2png(bytestring=site_svg.encode(),output_width=256,output_height=256))).convert('RGBA').save(ROOT/'favicon.ico',format='ICO',sizes=[(16,16),(32,32),(48,48),(64,64),(128,128),(256,256)])
site_og = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630" role="img" aria-labelledby="title desc">
<title id="title">LeviMC Icon Study</title><desc id="desc">An unofficial visual review gallery for website icons, project and application identities, and official Levi brand references.</desc>
<rect width="1200" height="630" fill="#f6f7f8"/><rect width="1200" height="16" fill="{F}"/>
<rect x="58" y="82" width="400" height="466" rx="28" fill="#ffffff" stroke="#e3e7e9" stroke-width="3"/>
<g transform="translate(82 110) scale(.68)">{site_body}</g>
<text x="548" y="185" fill="{M}" font-family="Inter,Segoe UI,sans-serif" font-size="20" font-weight="750" letter-spacing="4">UNOFFICIAL DESIGN STUDY</text>
<text x="544" y="285" fill="#171d24" font-family="Inter,Segoe UI,sans-serif" font-size="65" font-weight="780" letter-spacing="-2">LeviMC Icon Study</text>
<text x="548" y="347" fill="#59636e" font-family="Inter,Segoe UI,sans-serif" font-size="27">Website icons · Project identities · Brand references</text>
<path d="M548 405 H700" stroke="{L}" stroke-width="6" stroke-linecap="round"/>
<text x="548" y="535" fill="#69737d" font-family="Inter,Segoe UI,sans-serif" font-size="17" font-weight="650" letter-spacing="2">COMPARE · SELECT · REVIEW</text>
</svg>\n'''
ET.fromstring(site_og)
(ROOT/'og-image.svg').write_text(site_og,encoding='utf-8')
cairosvg.svg2png(bytestring=site_og.encode(),write_to=str(ROOT/'og-image.png'),output_width=1200,output_height=630)

# Validation: SVG XML, 512px viewBox, no raster embedding, all sizes rendered.
count = 0
for pth in ROOT.rglob('*.svg'):
    root = ET.parse(pth).getroot()
    assert root.attrib.get('viewBox'), f'missing viewBox: {pth}'
    if pth.name == 'icon.svg' or (pth.parent.name == 'variants' and not pth.name.endswith(('-banner.svg','-og-image.svg'))):
        assert root.attrib.get('viewBox') == '0 0 512 512', pth
        raw = pth.read_bytes().lower(); assert b'<image' not in raw, pth
        for sz in (16,24,32,48,64,128):
            cairosvg.svg2png(bytestring=pth.read_bytes(),output_width=sz,output_height=sz)
    count += 1
for project in PROJECTS:
    folder = LOGO_ROOT/project['slug']
    assert Image.open(folder/'apple-touch-icon.png').size == (180,180)
    assert Image.open(folder/'og-image.png').size == (1200,630)
    ico=Image.open(folder/'favicon.ico'); assert ico.format=='ICO'
    for sz in (16,32,48,64,128,256): assert (sz,sz) in ico.ico.sizes()

# Contact sheet: paired light/dark surfaces for every variant.
from PIL import ImageFont
font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
try:
    font = ImageFont.truetype(font_path,14)
    small = ImageFont.truetype(font_path,11)
except OSError:
    font = ImageFont.load_default()
    small = ImageFont.load_default()
cols=2; cell_w=740; cell_h=228; rows=(sum(len(p['variants']) for p in PROJECTS)+cols-1)//cols
sheet=Image.new('RGB',(cols*cell_w,rows*cell_h),(240,243,236)); draw=ImageDraw.Draw(sheet)
idx=0
for project in PROJECTS:
  for var in project['variants']:
    slug,label,desc,body=var; folder=LOGO_ROOT/project['slug']; file=folder/('icon.svg' if idx%3==0 else 'variants/'+slug+'.svg')
    if slug == project['variants'][0][0]: file=folder/'icon.svg'
    img=Image.open(BytesIO(cairosvg.svg2png(bytestring=file.read_bytes(),output_width=150,output_height=150))).convert('RGBA')
    x=(idx%cols)*cell_w; y=(idx//cols)*cell_h
    draw.rounded_rectangle((x+8,y+8,x+cell_w-8,y+cell_h-8),radius=12,fill=(255,255,255),outline=(204,214,200),width=1)
    draw.text((x+22,y+18),f"{project['name']} — {label}",font=font,fill=(35,59,38))
    # identical vector rendered over pale and deep backgrounds
    draw.rounded_rectangle((x+22,y+52,x+cell_w//2-18,y+205),radius=14,fill=(246,248,242))
    draw.rounded_rectangle((x+cell_w//2+2,y+52,x+cell_w-22,y+205),radius=14,fill=(0,0,0))
    for bx in (x+22,x+cell_w//2+2):
      draw.text((bx+12,y+59),'LIGHT' if bx==x+22 else 'OLED BLACK',font=small,fill=(81,105,79) if bx==x+22 else (190,196,202))
      sheet.alpha_composite(img,(bx+(cell_w//2-190)//2,y+68)) if sheet.mode=='RGBA' else sheet.paste(img,(bx+(cell_w//2-190)//2,y+68),img)
    idx += 1
sheet.save(BASE/'previews'/'project-logo-directions.png',quality=94)
print(f'Generated {len(PROJECTS)} project identities, {sum(len(p["variants"]) for p in PROJECTS)} SVG icon variants, {count} SVG masters including banners and OG sources.')
print('Asset derivatives: ICO multi-resolution (16,32,48,64,128,256), PNG favicons, 180px Apple touch icons, 1200x630 OG PNG + SVG.')
