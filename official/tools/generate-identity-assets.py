from pathlib import Path
from xml.etree import ElementTree as ET
import json, re, hashlib
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

# Detailed, brand-coherent marks. Each variant is independently authored; the first
# direction in each group is the preferred master icon.svg.
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
    'name':'LeviAntiCheat','slug':'levi-anticheat','summary':'A technical protection and detection identity for monitoring suspicious activity.',
    'subtitle':'Protection and detection','og_pattern':'scan','variants':[
      ('guardian-aperture','Guardian aperture','A layered shield encloses a multi-ring scanning aperture with a leaf-shaped detection core, combining protection and active inspection.',
       # shield with double edge and bevel details
       path('M256 52 C309 81 356 102 402 119 V237 C402 326 350 402 256 465 C162 402 110 326 110 237 V119 C156 102 203 81 256 52Z',F,P,13)
       + path('M256 73 C306 98 343 114 380 130 V237 C380 309 338 373 256 429 C174 373 132 309 132 237 V130 C169 114 206 98 256 73Z',T,F,12)
       + path('M166 170 C206 145 306 145 346 170', 'none',S,9)
       + circle(256,261,94,P,F,13)
       + circle(256,261,70,L,M,11)
       + path('M172 261 C194 217 224 196 256 196 C288 196 318 217 340 261 C318 305 288 326 256 326 C224 326 194 305 172 261Z',T,F,9)
       + leaf_mark(252,270,0.29,-5)
       + path('M200 349 C225 366 287 366 312 349', 'none',M,10)),
      ('scan-vault','Scan vault','A sealed technical enclosure uses a rotating scan ring, radial notches and a protected leaf core to suggest integrity checks and detection.',
       path('M256 67 L366 111 L394 218 L349 362 L256 440 L163 362 L118 218 L146 111Z',T,F,16)
       + path('M256 101 L339 136 L360 219 L326 333 L256 390 L186 333 L152 219 L173 136Z',P,M,10)
       + circle(256,245,84,L,F,13)
       + circle(256,245,58,T,F,9)
       + path('M256 161 V125 M340 245 H376 M256 329 V365 M172 245 H136', 'none',M,12)
       + path('M190 209 C219 182 293 182 322 209 M190 281 C219 308 293 308 322 281', 'none',S,9)
       + leaf_mark(256,255,0.27,0)
       + circle(256,245,8,F,'none',0)),
      ('radar-sentinel','Radar sentinel','A segmented radial sweep sits behind a compact shield, giving the symbol a monitoring-first reading without weapon or combat cues.',
       path('M256 63 C316 94 359 110 397 124 V239 C397 322 348 392 256 452 C164 392 115 322 115 239 V124 C153 110 196 94 256 63Z',F,P,12)
       + path('M256 93 C305 118 341 131 372 145 V238 C372 304 331 361 256 411 C181 361 140 304 140 238 V145 C171 131 207 118 256 93Z',D,S,8)
       + path('M186 275 A83 83 0 0 1 326 191 M186 275 A83 83 0 0 0 326 359', 'none',P,12)
       + path('M256 275 L329 197', 'none',L,15)
       + circle(256,275,20,T,F,8)
       + leaf_mark(257,276,0.20,-10)
       + path('M166 151 L186 170 M346 151 L326 170', 'none',S,9)),
    ]
  },
  {
    'name':'LeviOptimize','slug':'levioptimize','summary':'A performance optimization project for reducing overhead across computational hot paths.',
    'subtitle':'Performance and efficiency','og_pattern':'compute','variants':[
      ('processing-core','Processing core','A six-sided compute engine combines a layered central core, precision channels and a botanical processing motif. It signals system efficiency without a generic speedometer.',
       poly('256,43 375,111 421,238 375,365 256,433 137,365 91,238 137,111',F,P,14)
       + poly('256,70 352,125 389,238 352,351 256,406 160,351 123,238 160,125',T,F,11)
       + path('M256 70 V113 M352 125 L322 143 M389 238 H348 M352 351 L322 333 M256 406 V363 M160 351 L190 333 M123 238 H164 M160 125 L190 143', 'none',M,12)
       + poly('256,129 338,176 338,270 256,317 174,270 174,176',L,F,12)
       + poly('256,166 305,194 305,250 256,278 207,250 207,194',P,M,9)
       + leaf_mark(256,239,0.22,0)
       + circle(256,43,11,P,F,6) + circle(421,238,11,P,F,6) + circle(256,433,11,P,F,6) + circle(91,238,11,P,F,6)),
      ('pipeline-flow','Pipeline flow','Three controlled execution channels converge through a compact leaf-bearing processor, representing streamlined work and reduced redundant processing.',
       path('M62 135 C130 135 153 176 205 214 C220 225 239 232 256 232 H448', 'none',S,22)
       + path('M62 256 H448', 'none',L,22)
       + path('M62 377 C130 377 153 336 205 298 C220 287 239 280 256 280 H448', 'none',M,22)
       + poly('256,162 350,256 256,350 162,256',T,F,15)
       + poly('256,195 317,256 256,317 195,256',P,M,9)
       + leaf_mark(256,273,0.22,0)
       + circle(62,135,13,P,F,7) + circle(62,256,13,P,F,7) + circle(62,377,13,P,F,7)
       + path('M373 211 L405 256 L373 301', 'none',F,11)),
      ('layered-engine','Layered engine','Nested computational plates and aligned routing channels depict optimizations applied across several hot paths, with a leaf at the shared execution junction.',
       poly('256,70 400,145 256,220 112,145',T,F,14)
       + poly('112,145 256,220 256,260 112,185',S,F,9)
       + poly('400,145 256,220 256,260 400,185',L,F,9)
       + poly('256,214 400,289 256,364 112,289',P,F,14)
       + poly('112,289 256,364 256,405 112,330',S,F,9)
       + poly('400,289 256,364 256,405 400,330',M,F,9)
       + path('M256 220 V433', 'none',F,12)
       + leaf_mark(256,322,0.25,0)
       + path('M150 450 H362', 'none',P,10)),
    ]
  },
  {
    'name':'MoreDimensions','slug':'moredimensions','summary':'A science-fiction dimensional architecture API for adding custom Bedrock dimensions.',
    'subtitle':'Spatial and dimensional API','og_pattern':'dimensions','variants':[
      ('dimensional-arch','Dimensional arch','A nested, engineered portal uses layered elliptical frames, coordinate markers and a floating dimensional core. The leaf is embedded as the transition anchor.',
       path('M104 409 V245 C104 147 166 74 256 74 C346 74 408 147 408 245 V409', 'none',F,28)
       + path('M143 409 V247 C143 173 190 119 256 119 C322 119 369 173 369 247 V409', 'none',S,20)
       + path('M180 409 V251 C180 197 212 160 256 160 C300 160 332 197 332 251 V409', 'none',L,15)
       + path('M84 409 H428', 'none',P,16)
       + ellipse(256,409,142,30,T,F,8)
       + path('M150 409 C175 378 207 365 256 365 C305 365 337 378 362 409', 'none',M,8)
       + poly('256,215 306,244 306,302 256,331 206,302 206,244',P,F,10)
       + leaf_mark(256,284,0.18,0)
       + circle(104,245,9,P,F,5) + circle(408,245,9,P,F,5)),
      ('coordinate-cube','Coordinate cube','A dimensional wireframe cube intersects multiple offset coordinate planes, with a living botanical core marking the stable point between spaces.',
       poly('256,75 393,154 393,313 256,392 119,313 119,154', 'none',F,17)
       + path('M256 75 V232 M119 154 L256 232 L393 154 M256 232 V392 M119 313 L256 232 L393 313', 'none',S,15)
       + path('M168 104 L305 183 V342 M344 126 L207 205 V364', 'none',L,10)
       + poly('256,178 319,214 319,286 256,322 193,286 193,214',T,F,10)
       + leaf_mark(256,264,0.20,-8)
       + circle(256,75,10,P,F,5) + circle(393,154,10,P,F,5) + circle(119,313,10,P,F,5)),
      ('parallel-frames','Parallel frames','Three overlapping portal planes show parallel dimensional spaces and the transitions between them, avoiding a literal Nether-portal silhouette.',
       path('M93 388 V245 C93 154 147 103 221 103 C295 103 349 154 349 245 V388', 'none',F,23)
       + path('M163 388 V245 C163 190 197 158 256 158 C315 158 349 190 349 245 V388', 'none',S,17)
       + path('M233 388 V245 C233 218 245 202 277 202 C309 202 321 218 321 245 V388', 'none',L,12)
       + path('M146 129 L365 348 M365 129 L146 348', 'none',P,8)
       + poly('256,240 309,270 256,300 203,270',T,F,9)
       + leaf_mark(256,274,0.17,0)
       + path('M90 414 H422', 'none',F,10)),
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

# Build flat manifest + project metadata.
manifest = {
  'title':'LeviMC project identity concepts',
  'status':'Unofficial concepts for review. The /official/ route is a directory label, not an approval claim.',
  'reference': {
    'name':'LeviLamina official vector identity',
    'source':'https://github.com/LiteLDev/LeviLamina/blob/main/docs/main/contents/logo.svg',
    'palette':C,
    'style_note':'Organic botanical silhouettes, layered forest-green fills and restrained sage contrasts, based on the current official vector mark.'
  },
  'projects':[], 'icons':[]
}

for project in PROJECTS:
    slug = project['slug']; folder = LOGO_ROOT / slug; folder.mkdir(parents=True, exist_ok=True)
    variants = []
    for idx, (variant_slug,label,description,body) in enumerate(project['variants']):
        file_path = 'logos/' + slug + ('/icon.svg' if idx == 0 else '/variants/' + variant_slug + '.svg')
        if idx > 0:
            (folder/'variants').mkdir(exist_ok=True)
            out = folder/'variants'/f'{variant_slug}.svg'
        else:
            out = folder/'icon.svg'
        svg = svg_doc(f"{project['name']} — {label}", description, body)
        out.write_text(svg, encoding='utf-8')
        variants.append({'slug':variant_slug,'label':label,'description':description,'file':file_path,'recommended':idx==0})
        manifest['icons'].append({'project':project['name'],'project_slug':slug,'slug':variant_slug,'label':label,'description':description,'file':file_path,'recommended':idx==0,'summary':project['summary']})
    # Project banner, SVG master with no opaque background.
    banner = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="240" viewBox="0 0 1200 240" role="img" aria-labelledby="title desc">
<title id="title">{project['name']} — project identity</title><desc id="desc">{project['subtitle']}; proposed LeviMC project identity.</desc>
<g transform="translate(24 24) scale(.375)"><g>{PROJECTS[[p['slug'] for p in PROJECTS].index(slug)]['variants'][0][3]}</g></g>
<path d="M226 43 V197" stroke="{P}" stroke-width="3" opacity=".7"/><path d="M253 78 H1155" stroke="{S}" stroke-width="2" opacity=".65"/>
<text x="278" y="116" fill="{L}" font-family="Inter,Segoe UI,sans-serif" font-size="64" font-weight="700" letter-spacing="-1.5">{project['name']}</text>
<text x="281" y="159" fill="{M}" font-family="Inter,Segoe UI,sans-serif" font-size="27" font-weight="500">{project['subtitle']}</text>
</svg>\n'''
    ET.fromstring(banner)
    (folder/'icon-banner.svg').write_text(banner, encoding='utf-8')
    # OG image vector source: dark forest composition, project-specific low-contrast pattern.
    pattern = project['og_pattern']
    pattern_parts = {
      'archive': path('M680 80 V550 M730 100 V530 M780 80 V550 M830 100 V530', 'none',S,3, 'opacity=".16"') + path('M650 160 H1150 M650 260 H1150 M650 360 H1150 M650 460 H1150','none',P,2,'opacity=".10"'),
      'packages': path('M690 120 L900 20 L1110 120 L900 220Z M690 300 L900 200 L1110 300 L900 400Z M690 480 L900 380 L1110 480 L900 580Z','none',L,5,'opacity=".18"'),
      'scan': ''.join(circle(925,315,r,'none',P,3,'opacity=".12"') for r in (90,150,210,270)) + path('M925 315 L1140 130','none',L,6,'opacity=".16"'),
      'compute': path('M730 95 H1120 M730 185 H1120 M730 275 H1120 M730 365 H1120 M730 455 H1120 M730 545 H1120','none',S,3,'opacity=".15"') + path('M760 70 V570 M850 70 V570 M940 70 V570 M1030 70 V570 M1120 70 V570','none',P,2,'opacity=".10"'),
      'dimensions': path('M710 500 V300 C710 125 810 55 925 55 C1040 55 1140 125 1140 300 V500 M770 500 V300 C770 165 835 110 925 110 C1015 110 1080 165 1080 300 V500','none',L,8,'opacity=".15"'),
      'network': path('M690 120 L900 315 L1110 120 M690 510 L900 315 L1110 510 M900 315 V75','none',P,8,'opacity=".14"') + ''.join(circle(x,y,16,'none',L,5,'opacity=".25"') for x,y in ((690,120),(1110,120),(690,510),(1110,510),(900,75))),
      'catalogue': ''.join(rect(x,y,130,130,20,'none',P,5,'opacity=".13"') for x,y in ((730,90),(890,90),(730,250),(890,250),(730,410),(890,410)))
    }[pattern]
    og_title_size = 46 if len(project['name']) > 14 else 58
    og_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630" role="img" aria-labelledby="title desc">
<title id="title">{project['name']} — LeviMC project identity</title><desc id="desc">{project['summary']}</desc>
<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{D}"/><stop offset="1" stop-color="{F}"/></linearGradient></defs>
<rect width="1200" height="630" fill="url(#bg)"/>
<g>{pattern_parts}</g>
<path d="M0 523 C245 481 402 564 630 528 C823 498 1030 500 1200 545 V630 H0Z" fill="{M}" opacity=".18"/>
<circle cx="302" cy="310" r="207" fill="{P}" opacity=".07"/><circle cx="302" cy="310" r="181" fill="{F}" stroke="{S}" stroke-width="2" opacity=".85"/>
<g transform="translate(46 54) scale(.82)">{project['variants'][0][3]}</g>
<path d="M571 120 V508" stroke="{S}" stroke-width="3" opacity=".65"/>
<text x="626" y="184" fill="{P}" font-family="Inter,Segoe UI,sans-serif" font-size="20" font-weight="600" letter-spacing="5">LEVIMC PROJECT CONCEPT</text>
<text x="626" y="275" fill="{L}" font-family="Inter,Segoe UI,sans-serif" font-size="{og_title_size}" font-weight="750" letter-spacing="-1.5">{project['name']}</text>
<text x="630" y="333" fill="{P}" font-family="Inter,Segoe UI,sans-serif" font-size="25" font-weight="500">{project['subtitle']}</text>
<path d="M630 380 H1080" stroke="{S}" stroke-width="3"/>
<text x="630" y="433" fill="{T}" font-family="Inter,Segoe UI,sans-serif" font-size="19">Distinct project identity · shared Levi botanical language</text>
<text x="630" y="535" fill="{S}" font-family="Inter,Segoe UI,sans-serif" font-size="16" letter-spacing="2">UNOFFICIAL DESIGN CONCEPT · FOR REVIEW</text>
</svg>\n'''
    ET.fromstring(og_svg)
    (folder/'og-image.svg').write_text(og_svg, encoding='utf-8')
    # Per-project asset derivatives from the preferred icon.svg.
    icon_bytes = (folder/'icon.svg').read_bytes()
    # apple-touch-icon: 180px, solid pale brand canvas, no baked rounded corners.
    icon180 = cairosvg.svg2png(bytestring=icon_bytes, output_width=122, output_height=122)
    mark = Image.open(BytesIO(icon180)).convert('RGBA')
    app = Image.new('RGBA',(180,180),C['paper'])
    d = ImageDraw.Draw(app)
    d.ellipse((7,7,173,173), fill='#e4eadc', outline=C['sage'], width=2)
    app.alpha_composite(mark,((180-mark.width)//2,(180-mark.height)//2))
    app.convert('RGB').save(folder/'apple-touch-icon.png',quality=95)
    # Multi-resolution favicon ICO plus explicit PNG sizes for consumers that prefer PNG links.
    for sz in (16,32,48,64,128,256):
        data = cairosvg.svg2png(bytestring=icon_bytes, output_width=sz, output_height=sz)
        im = Image.open(BytesIO(data)).convert('RGBA')
        im.save(folder/f'favicon-{sz}x{sz}.png', optimize=True)
    base = Image.open(BytesIO(cairosvg.svg2png(bytestring=icon_bytes,output_width=256,output_height=256))).convert('RGBA')
    base.save(folder/'favicon.ico',format='ICO',sizes=[(16,16),(32,32),(48,48),(64,64),(128,128),(256,256)])
    # OG raster from SVG source; exact 1200x630 dimensions.
    cairosvg.svg2png(bytestring=og_svg.encode(),write_to=str(folder/'og-image.png'),output_width=1200,output_height=630)
    # Manifest project-level asset paths.
    manifest['projects'].append({
      'name':project['name'],'slug':slug,'summary':project['summary'],'subtitle':project['subtitle'],
      'palette':[F,M,L,S,P],
      'icon':f'logos/{slug}/icon.svg','banner':f'logos/{slug}/icon-banner.svg',
      'favicon':f'logos/{slug}/favicon.ico','apple_touch_icon':f'logos/{slug}/apple-touch-icon.png',
      'og_image':f'logos/{slug}/og-image.png','og_image_svg':f'logos/{slug}/og-image.svg',
      'asset_bundle':f'logos/{slug}/asset-family.zip',
      'variants':variants
    })
    with zipfile.ZipFile(folder/'asset-family.zip','w',zipfile.ZIP_DEFLATED,compresslevel=9) as bundle:
        for asset in sorted(folder.rglob('*')):
            if asset.is_file() and asset.name != 'asset-family.zip':
                bundle.write(asset, asset.relative_to(folder).as_posix())

(ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

# Gallery-owned icon family, derived from the same branded botanical master.
site_body = leaf_mark(256,256,0.72,0)
site_svg = svg_doc('LeviMC project identity gallery','A botanical mark based on the current LeviLamina family identity.',site_body)
(ROOT/'site-icon.svg').write_text(site_svg,encoding='utf-8')
site_png = cairosvg.svg2png(bytestring=site_svg.encode(),output_width=180,output_height=180)
mark = Image.open(BytesIO(site_png)).convert('RGBA')
site_touch = Image.new('RGBA',(180,180),C['paper']); ImageDraw.Draw(site_touch).ellipse((7,7,173,173),fill='#e4eadc',outline=S,width=2); site_touch.alpha_composite(mark)
site_touch.convert('RGB').save(ROOT/'apple-touch-icon.png',quality=95)
for sz in (16,32,48,64,128,256):
    Image.open(BytesIO(cairosvg.svg2png(bytestring=site_svg.encode(),output_width=sz,output_height=sz))).save(ROOT/f'favicon-{sz}x{sz}.png',optimize=True)
Image.open(BytesIO(cairosvg.svg2png(bytestring=site_svg.encode(),output_width=256,output_height=256))).convert('RGBA').save(ROOT/'favicon.ico',format='ICO',sizes=[(16,16),(32,32),(48,48),(64,64),(128,128),(256,256)])
site_og = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630" role="img" aria-labelledby="title desc"><title id="title">LeviMC project identity concepts</title><desc id="desc">A family of proposed LeviMC project marks built around the LeviLamina botanical identity.</desc><defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{D}"/><stop offset="1" stop-color="{F}"/></linearGradient></defs><rect width="1200" height="630" fill="url(#bg)"/><circle cx="300" cy="315" r="190" fill="{P}" opacity=".08"/><g transform="translate(44 54) scale(.82)">{site_body}</g><path d="M570 120 V510" stroke="{S}" stroke-width="3"/><text x="630" y="190" fill="{P}" font-family="Inter,Segoe UI,sans-serif" font-size="23" letter-spacing="5">LEVIMC · PROJECT BRANDING</text><text x="630" y="292" fill="{L}" font-family="Inter,Segoe UI,sans-serif" font-size="61" font-weight="700">Project identities</text><text x="634" y="352" fill="{P}" font-family="Inter,Segoe UI,sans-serif" font-size="26">A shared botanical visual language</text><text x="634" y="535" fill="{S}" font-family="Inter,Segoe UI,sans-serif" font-size="17" letter-spacing="2">UNOFFICIAL DESIGN CONCEPT · FOR REVIEW</text></svg>\n'''
ET.fromstring(site_og)
(ROOT/'og-image.svg').write_text(site_og,encoding='utf-8')
cairosvg.svg2png(bytestring=site_og.encode(),write_to=str(ROOT/'og-image.png'),output_width=1200,output_height=630)

# Validation: SVG XML, 512px viewBox, no raster embedding, all sizes rendered.
count = 0
for pth in ROOT.rglob('*.svg'):
    root = ET.parse(pth).getroot()
    assert root.attrib.get('viewBox'), f'missing viewBox: {pth}'
    if pth.name == 'icon.svg' or '/variants/' in str(pth):
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
    draw.rounded_rectangle((x+cell_w//2+2,y+52,x+cell_w-22,y+205),radius=14,fill=(25,47,30))
    for bx in (x+22,x+cell_w//2+2):
      draw.text((bx+12,y+59),'LIGHT' if bx==x+22 else 'DARK',font=small,fill=(81,105,79) if bx==x+22 else (185,204,172))
      sheet.alpha_composite(img,(bx+(cell_w//2-190)//2,y+68)) if sheet.mode=='RGBA' else sheet.paste(img,(bx+(cell_w//2-190)//2,y+68),img)
    idx += 1
sheet.save(BASE/'official-contact-sheet.png',quality=94)
print(f'Generated {len(PROJECTS)} project identities, {sum(len(p["variants"]) for p in PROJECTS)} SVG icon variants, {count} SVG masters including banners and OG sources.')
print('Asset derivatives: ICO multi-resolution (16,32,48,64,128,256), PNG favicons, 180px Apple touch icons, 1200x630 OG PNG + SVG.')
