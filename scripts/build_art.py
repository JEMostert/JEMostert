#!/usr/bin/env python3
"""Build the original Noctis artwork with the Python standard library."""
from html import escape
from pathlib import Path
import random

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
ASSETS.mkdir(exist_ok=True)
(ASSETS / 'badges').mkdir(exist_ok=True)

def svg(width, height, title, body, description=''):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(description or title)}</desc>
<defs>
 <linearGradient id="night" x2="1" y2="1"><stop stop-color="#080e20"/><stop offset=".52" stop-color="#10172e"/><stop offset="1" stop-color="#1b1535"/></linearGradient>
 <linearGradient id="silver" x2=".2" y2="1"><stop stop-color="#ffffff"/><stop offset=".55" stop-color="#dce5ff"/><stop offset="1" stop-color="#8398cc"/></linearGradient>
 <linearGradient id="crystal" x2="1" y2="1"><stop stop-color="#d9edff"/><stop offset=".35" stop-color="#8ab8ff"/><stop offset=".7" stop-color="#8868e8"/><stop offset="1" stop-color="#413f81"/></linearGradient>
 <linearGradient id="accent" x2="1"><stop stop-color="#76cbff"/><stop offset=".5" stop-color="#a594ff"/><stop offset="1" stop-color="#dda3ff"/></linearGradient>
 <radialGradient id="nebula"><stop stop-color="#6452d2" stop-opacity=".34"/><stop offset="1" stop-color="#6452d2" stop-opacity="0"/></radialGradient>
 <radialGradient id="blue-nebula"><stop stop-color="#387fd1" stop-opacity=".23"/><stop offset="1" stop-color="#387fd1" stop-opacity="0"/></radialGradient>
 <filter id="glow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="3"/></filter>
</defs>
<style>
 text{{font-family:Arial,Helvetica,sans-serif}} .mono{{font-family:'Courier New',monospace}}
 .twinkle{{animation:twinkle 5s ease-in-out infinite alternate}} .float{{animation:float 7s ease-in-out infinite}} .pulse{{animation:pulse 6s ease-in-out infinite}}
 @keyframes twinkle{{from{{opacity:.25}}to{{opacity:1}}}} @keyframes float{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-9px)}}}} @keyframes pulse{{0%,100%{{opacity:.42}}50%{{opacity:.85}}}}
 @media(prefers-reduced-motion:reduce){{.twinkle,.float,.pulse{{animation:none}}}}
</style>
{body}
</svg>\n'''

def write(name, width, height, title, body, description=''):
    (ASSETS / name).write_text(svg(width, height, title, body, description))

def stars(width, height, number=65):
    rng = random.Random(713)
    result = []
    for i in range(number):
        x, y = rng.randrange(20, width-20), rng.randrange(12, height-12)
        radius = rng.choice([.7, 1, 1.3, 1.8])
        cls = f'class="twinkle" style="animation-delay:-{i%7}s"' if i%9 == 0 else ''
        result.append(f'<circle cx="{x}" cy="{y}" r="{radius}" fill="#d1dbff" opacity="{rng.uniform(.15,.65):.2f}" {cls}/>')
    return ''.join(result)

def diamond(x, y, size=9, opacity=.7):
    return f'<path d="M{x} {y-size}l{size/2} {size}l{-size/2} {size}l{-size/2} {-size}Z" fill="url(#crystal)" opacity="{opacity}"/>'

def blade():
    return '''<g>
 <circle cy="-10" r="150" fill="url(#nebula)"/>
 <circle cy="-10" r="133" fill="none" stroke="#879ce0" stroke-opacity=".2"/>
 <circle cy="-10" r="120" fill="none" stroke="#a398ee" stroke-opacity=".16" stroke-dasharray="2 12"/>
 <ellipse cy="-10" rx="165" ry="64" fill="none" stroke="#81bbff" stroke-opacity=".18" transform="rotate(-28)"/>
 <path d="M-190-10H-152M152-10H190M0-200V-172M0 151V179" stroke="#7fa5e6" stroke-opacity=".35"/>
 <g class="float">
 <path d="M-12-145L0-196L12-145L8 51L0 78L-8 51Z" fill="url(#crystal)"/>
 <path d="M0-196V78L-8 51L-12-145Z" fill="#d5e7ff" opacity=".52"/>
 <path d="M0-181L6-140L4 42L0 64Z" fill="#fbfdff" opacity=".65"/>
 <path d="M-66 50L-38 37L-11 44L0 51L11 44L38 37L66 50L39 53L13 60H-13L-39 53Z" fill="url(#silver)"/>
 <path d="M-7 63H7L5 110H-5Z" fill="#354266" stroke="#b3c4ef" stroke-width="1.4"/>
 <path d="M-6 74L6 82M-6 87L6 95M-5 101L5 106" stroke="#9a9dcc" stroke-width="2"/>
 <path d="M0 108L10 119L0 133L-10 119Z" fill="url(#crystal)"/>
 <path d="M-67-83L-42-162L-32-96L-39-28Z" fill="url(#crystal)" opacity=".5"/>
 <path d="M62-105L88-156L87-75L70-14Z" fill="url(#crystal)" opacity=".6"/>
 <path d="M-91 28L-114-7L-99-55L-78-16Z" fill="url(#crystal)" opacity=".32"/>
 <path d="M114 42L99 13L122-41L130-5Z" fill="url(#crystal)" opacity=".38"/>
 <path d="M-32 103L-50 148L-48 99Z" fill="url(#crystal)" opacity=".42"/>
 <path d="M48 80L63 111L38 145Z" fill="url(#crystal)" opacity=".52"/>
 </g>
 <circle cx="-123" cy="-55" r="3" fill="#badfff" class="pulse"/>
 <circle cx="107" cy="68" r="2" fill="#c9b1ff"/>
</g>'''

for compact in [False, True]:
    w, h = (640, 560) if compact else (1200, 440)
    background = f'<rect width="{w}" height="{h}" rx="18" fill="url(#night)"/><ellipse cx="{w*.85}" cy="{h*.38}" rx="390" ry="270" fill="url(#nebula)"/><ellipse cx="200" cy="360" rx="430" ry="210" fill="url(#blue-nebula)"/>' + stars(w,h)
    if compact:
        art = '<g transform="translate(505 336) scale(.72) rotate(16)">' + blade() + '</g>'
        text = '''<text x="40" y="54" class="mono" fill="#a4b4d6" font-size="15" letter-spacing="4">JEMOSTERT / AFTER DARK</text>
<text x="35" y="174" fill="url(#silver)" style="font-family:Georgia,'Times New Roman',serif" font-size="108" letter-spacing="6">NOCTIS</text>
<path d="M40 204H370" stroke="url(#accent)" stroke-opacity=".7"/>
<text x="40" y="253" fill="#dce7ff" font-size="26">Software under the stars.</text>
<text x="40" y="299" fill="#9cafd5" font-size="18">LOCAL AI</text><text x="40" y="331" fill="#9cafd5" font-size="18">DESKTOP TOOLS</text><text x="40" y="363" fill="#9cafd5" font-size="18">REAL-WORLD SOFTWARE</text>
<text x="40" y="508" class="mono" fill="#929bc1" font-size="14" letter-spacing="3">BUILD. SHIP. REFINE.</text>'''
    else:
        art = '<g transform="translate(991 237) rotate(16)">' + blade() + '</g>'
        text = '''<text x="63" y="58" class="mono" fill="#a4b4d6" font-size="13" letter-spacing="4">JEMOSTERT / AFTER DARK</text>
<text x="57" y="213" fill="url(#silver)" style="font-family:Georgia,'Times New Roman',serif" font-size="141" letter-spacing="13">NOCTIS</text>
<path d="M65 245H676" stroke="url(#accent)" stroke-opacity=".65"/>
<text x="65" y="291" fill="#e0e9ff" font-size="28" letter-spacing=".5">Software under the stars.</text>
<text x="65" y="329" class="mono" fill="#9cafd5" font-size="14" letter-spacing="1.5">LOCAL AI  /  DESKTOP TOOLS  /  REAL-WORLD SOFTWARE</text>
<text x="65" y="393" class="mono" fill="#818eaf" font-size="11" letter-spacing="3">BUILD. SHIP. REFINE.</text>'''
    mountains = f'<path d="M0 {h}V{h-32}L{w*.12} {h-51}L{w*.24} {h-24}L{w*.4} {h-42}L{w*.52} {h-18}L{w*.69} {h-55}L{w*.8} {h-28}L{w} {h-62}V{h}Z" fill="#070d1d" opacity=".6"/>'
    write('noctis-hero'+('-compact' if compact else '')+'.svg',w,h,'Noctis — software under the stars',background+mountains+art+text)

def waveform():
    rng = random.Random(12)
    bars = ''.join(f'<rect x="{i*11-94}" y="{-v/2}" width="5" height="{v}" rx="2.5" fill="url(#accent)" opacity="{.4+(i%4)*.16}" class="pulse" style="animation-delay:-{i%6}s"/>' for i,v in enumerate([rng.randrange(12,90) for _ in range(18)]))
    return '<circle r="90" fill="url(#blue-nebula)"/><circle r="77" fill="none" stroke="#7dc7fa" stroke-opacity=".25"/><ellipse cy="40" rx="90" ry="24" fill="none" stroke="#79b6e9" stroke-opacity=".18"/>'+bars+'<circle cy="80" r="5" fill="#b8dfff"/>'

def cursors():
    return '''<circle r="94" fill="url(#nebula)"/><path d="M-78-36H69V63H-78Z" fill="none" stroke="#9c9be7" stroke-opacity=".25"/>
<path d="M-65-66L-4-7L-35-2L-44 27Z" fill="#2e395d" stroke="#96adeb" stroke-width="2"/>
<g class="float"><path d="M20-19L81 40L50 45L41 74Z" fill="url(#crystal)" stroke="#bfd5ff" stroke-width="1.5"/></g>
<path d="M-68 60H-40M-64 78H-12M65-60V-34M52-47H78" stroke="#b19be8" stroke-width="2" stroke-opacity=".5"/>
<circle cx="-6" cy="-65" r="4" fill="#a4c9ff" class="pulse"/>'''

def evidence():
    edges = [(-64,-48,8,-68),(8,-68,63,-19),(63,-19,40,58),(40,58,-37,73),(-37,73,-64,-48),(-64,-48,0,0),(0,0,8,-68),(0,0,63,-19),(0,0,40,58),(0,0,-37,73)]
    lines=''.join(f'<path d="M{x} {y}L{x2} {y2}" stroke="#94a5ed" stroke-width="1.5" stroke-opacity=".42"/>' for x,y,x2,y2 in edges)
    nodes=''.join(f'<circle cx="{x}" cy="{y}" r="6" fill="url(#crystal)"/>' for x,y in [(-64,-48),(8,-68),(63,-19),(40,58),(-37,73)])
    return '<circle r="98" fill="url(#nebula)"/>'+lines+nodes+'<circle r="23" fill="#151d39" stroke="#bbcaff" stroke-width="2"/><path d="M-7-7L7 7M7-7L-7 7" stroke="#c6d7ff" stroke-width="2"/>'+diamond(0,0,8)

def workbench():
    return '''<circle r="95" fill="url(#blue-nebula)"/>
<rect x="-94" y="-65" width="188" height="123" rx="10" fill="#101b32" stroke="#83a4d2" stroke-width="1.5"/>
<path d="M-94-40H94M-32-40V58" stroke="#7c97c0" stroke-opacity=".35"/>
<circle cx="-79" cy="-53" r="3" fill="#bd9fe7"/><circle cx="-68" cy="-53" r="3" fill="#a4bbec"/><circle cx="-57" cy="-53" r="3" fill="#90ccd7"/>
<path d="M-77-20H-46M-77-2H-52M-77 16H-43M-77 34H-58" stroke="#7c93b9" stroke-width="4" stroke-linecap="round"/>
<g class="pulse"><path d="M25-21L54-5V27L25 43L-4 27V-5Z" fill="none" stroke="url(#accent)" stroke-width="2"/><path d="M25-21V10M-4-5L25 10L54-5M25 10V43" fill="none" stroke="url(#accent)" stroke-width="1.5"/></g>
<path d="M-44 77H44M-22 58V76M22 58V76" stroke="#788ebc" stroke-width="2"/>'''

projects = [
 ('delulu','01','DELULU TALKS','Your voice. Your machine.','LOCAL DESKTOP DICTATION','ELECTRON  /  PYTHON  /  MLX + CUDA',waveform),
 ('artist','02','COMPUTER ARTIST','A cursor of its own.','INDEPENDENT DESKTOP INPUT','PYTHON  /  C++  /  KDE WAYLAND',cursors),
 ('index','03','INDEXEXPRESS','Follow the evidence.','SOURCE-CITED WEB RESEARCH','PYTHON  /  MCP  /  SEARXNG',evidence),
 ('yard','04','MODEL YARD','A home for local intelligence.','THE LOCAL OLLAMA WORKBENCH','TAURI  /  RUST  /  REACT',workbench),
]
for name,number,title,tagline,label,tech,icon in projects:
    for compact in [False, True]:
        w,h = (640,300) if compact else (1200,210)
        background=f'<rect width="{w}" height="{h}" rx="14" fill="url(#night)"/><rect x=".75" y=".75" width="{w-1.5}" height="{h-1.5}" rx="14" fill="none" stroke="#9eabdf" stroke-opacity=".22"/><path d="M1 35V{h-35}" stroke="url(#accent)" stroke-width="3"/>'
        if compact:
            body=f'<text x="30" y="35" class="mono" fill="#a7a5d7" font-size="13" letter-spacing="2">{number} / {label}</text><text x="30" y="87" fill="#e8edff" font-size="35" font-weight="700">{title}</text><text x="30" y="125" fill="#a5b9e3" font-size="22">{tagline}</text><text x="30" y="267" class="mono" fill="#95a6c6" font-size="13">{escape(tech)}</text><g transform="translate(500 208) scale(.65)">{icon()}</g>'
        else:
            body=f'<text x="43" y="36" class="mono" fill="#a7a5d7" font-size="12" letter-spacing="2.3">{number} / {label}</text><text x="43" y="91" fill="#e8edff" font-size="36" font-weight="700" letter-spacing="1">{title}</text><text x="43" y="132" fill="#a5b9e3" font-size="27">{tagline}</text><text x="43" y="181" class="mono" fill="#95a6c6" font-size="12" letter-spacing="1">{escape(tech)}</text><path d="M872 35V175" stroke="#8a9ccb" stroke-opacity=".17"/><g transform="translate(1035 103) scale(.8)">{icon()}</g>'
        write(f'project-{name}'+('-compact' if compact else '')+'.svg',w,h,title+' — '+tagline,background+body)

write('labservant.svg',1200,170,'LabServant — software for the real world','''
<rect width="1200" height="170" rx="14" fill="url(#night)"/>
<ellipse cx="1080" cy="80" rx="200" ry="160" fill="url(#nebula)"/>
<text x="42" y="36" class="mono" fill="#a9a5d4" font-size="12" letter-spacing="3">THE DAYLIGHT CHAPTER</text>
<text x="42" y="89" fill="url(#silver)" font-size="38" font-weight="700">LABSERVANT</text>
<text x="43" y="132" fill="#a3b9df" font-size="22">Software for the real world.</text>
<g transform="translate(1060 82)">
<path d="M0-50L43-25V25L0 50L-43 25V-25Z" fill="none" stroke="#ad9aeb" stroke-width="1.5"/>
<path d="M0-31L27-15V15L0 31L-27 15V-15Z" fill="none" stroke="#8ebde7" stroke-opacity=".7"/>
<path d="M-13-18H13M-7-18V3L-21 21H21L7 3V-18" fill="none" stroke="#cadcff" stroke-width="2.5" stroke-linejoin="round"/>
<path d="M-13 12H13" stroke="#cadcff" stroke-width="2"/><circle cx="0" cy="6" r="2" fill="#b3a6f7"/>
</g>''')

write('labservant-compact.svg',640,210,'LabServant — software for the real world','''
<rect width="640" height="210" rx="14" fill="url(#night)"/>
<ellipse cx="580" cy="110" rx="170" ry="170" fill="url(#nebula)"/>
<text x="30" y="34" class="mono" fill="#a9a5d4" font-size="13" letter-spacing="2">THE DAYLIGHT CHAPTER</text>
<text x="30" y="89" fill="url(#silver)" font-size="37" font-weight="700">LABSERVANT</text>
<text x="30" y="127" fill="#a3b9df" font-size="22">Software for the real world.</text>
<g transform="translate(569 93) scale(.8)">
<path d="M0-50L43-25V25L0 50L-43 25V-25Z" fill="none" stroke="#ad9aeb" stroke-width="1.5"/>
<path d="M-13-18H13M-7-18V3L-21 21H21L7 3V-18" fill="none" stroke="#cadcff" stroke-width="2.5" stroke-linejoin="round"/>
<path d="M-13 12H13" stroke="#cadcff" stroke-width="2"/>
</g>
<text x="30" y="182" class="mono" fill="#869ac3" font-size="13" letter-spacing="1">WORKFLOWS / INTERFACES / INTEGRATIONS</text>''')

write('noctis-footer.svg',1200,145,'Keep building. Keep exploring.','''
<path d="M0 65H430M770 65H1200" stroke="#8c9ddb" stroke-opacity=".22"/>
<g transform="translate(600 64)"><path d="M-85 0L-42-16L0-35L42-16L85 0L42 17L0 34L-42 17Z" fill="none" stroke="#9394d7" stroke-opacity=".5"/>
<path d="M0-35V34M-85 0H85M-42-16L42 17M42-16L-42 17" stroke="#7c9fd5" stroke-opacity=".3"/>
<path d="M0-21L11 0L0 21L-11 0Z" fill="url(#crystal)" class="pulse"/>
<circle cx="-85" r="2.5" fill="#9db9ef"/><circle cx="85" r="2.5" fill="#b29fe9"/></g>
<text x="600" y="127" text-anchor="middle" class="mono" font-size="13" letter-spacing="4" fill="#929ac1">KEEP BUILDING. KEEP EXPLORING.</text>''')

write('noctis-footer-compact.svg',640,160,'Keep building. Keep exploring.','''
<path d="M0 55H207M433 55H640" stroke="#8c9ddb" stroke-opacity=".22"/>
<g transform="translate(320 55)"><path d="M-78 0L0-32L78 0L0 32Z" fill="none" stroke="#9394d7" stroke-opacity=".5"/>
<path d="M-78 0H78M0-32V32" stroke="#7c9fd5" stroke-opacity=".3"/>
<path d="M0-20L11 0L0 20L-11 0Z" fill="url(#crystal)" class="pulse"/></g>
<text x="320" y="123" text-anchor="middle" class="mono" font-size="17" letter-spacing="2" fill="#929ac1">KEEP BUILDING. KEEP EXPLORING.</text>''')

badges = [
 ('local-first','✦','LOCAL-FIRST','#9fbeff'),('labservant','◈','LABSERVANT','#c1a6ff'),('build-ship','↗','BUILD · SHIP · REFINE','#98d6e6'),
 ('typescript','TS','TYPESCRIPT','#90b8fb'),('python','Py','PYTHON','#d9c18a'),('php','php','PHP','#b0abed'),('rust','Rs','RUST','#d8b2a4'),
 ('react','⚛','REACT','#8cd4ec'),('laravel','La','LARAVEL','#e9a1b2'),('livewire','Lw','LIVEWIRE','#dca4d0'),('astro','A','ASTRO','#d2b0ee'),
 ('electron','E','ELECTRON','#a4d6de'),('tauri','T','TAURI','#a3cee9'),('linux','>_','LINUX','#cfcbac'),('mcp','◇','MCP','#ada7ee'),
]
for name,mark,label,color in badges:
    width = 43 + len(label)*7.1 + 16
    body=f'<rect x=".5" y=".5" width="{width-1}" height="29" rx="6" fill="#111a30" stroke="#7985b1" stroke-opacity=".38"/><path d="M38 6V24" stroke="#657496" stroke-opacity=".45"/><text x="19" y="20" text-anchor="middle" fill="{color}" font-size="12" font-weight="700">{escape(mark)}</text><text x="49" y="19" fill="#d4def4" font-size="10.5" font-weight="600" letter-spacing=".6">{escape(label)}</text>'
    (ASSETS/'badges'/f'{name}.svg').write_text(svg(round(width),30,label,body))

print('Built',len(list(ASSETS.rglob('*.svg'))),'SVG assets.')
