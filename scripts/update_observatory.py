#!/usr/bin/env python3
"""Refresh artwork from public GitHub data; never read private repository APIs."""
from html import escape
import json
import os
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OWNER = 'JEMostert'

def api(path):
    headers={'Accept':'application/vnd.github+json','User-Agent':'JEMostert-profile-observatory'}
    token=os.environ.get('GITHUB_TOKEN')
    if token: headers['Authorization']='Bearer '+token
    with urlopen(Request('https://api.github.com/'+path,headers=headers),timeout=30) as response:
        return json.load(response)

def artwork(count, language_count, release, pushed, compact=False):
    w,h=(640,355) if compact else (1200,220)
    title=f'{count} original public builds · {language_count} primary languages · Delulu Talks {release}'
    panels=[('ORIGINAL PUBLIC BUILDS',str(count),'Forks and this profile excluded'),('PRIMARY LANGUAGES',str(language_count),'Across those public builds'),('DELULU TALKS',release,'Latest published release')]
    content=[]
    if compact:
        for i,(label,value,detail) in enumerate(panels):
            y=78+i*83
            content.append(f'<text x="28" y="{y}" fill="#9aadd3" font-size="13" letter-spacing="1.4">{label}</text><text x="610" y="{y+6}" text-anchor="end" fill="#e1e9ff" font-size="32" font-weight="700">{escape(value)}</text><text x="28" y="{y+24}" fill="#8497bd" font-size="13">{detail}</text>')
        content.append(f'<text x="28" y="325" fill="#8f9fc4" font-size="13">Last project push · {pushed}</text>')
    else:
        for i,(label,value,detail) in enumerate(panels):
            x=34+i*391
            content.append(f'<text x="{x}" y="78" fill="#9aadd3" font-size="12" letter-spacing="1.5">{label}</text><text x="{x}" y="136" fill="#e1e9ff" font-size="46" font-weight="700">{escape(value)}</text><text x="{x}" y="164" fill="#8497bd" font-size="12">{detail}</text>')
            if i: content.append(f'<path d="M{x-24} 59V171" stroke="#98a2d8" stroke-opacity=".16"/>')
        content.append(f'<text x="1166" y="199" text-anchor="end" fill="#8f9fc4" font-size="11">LAST PROJECT PUSH / {pushed}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">Live public-repository snapshot. {escape(title)}. Last public project push: {pushed}.</desc>
<defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#0a1226"/><stop offset="1" stop-color="#1a1834"/></linearGradient></defs>
<rect width="{w}" height="{h}" rx="14" fill="url(#bg)"/>
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="14" fill="none" stroke="#8e9aca" stroke-opacity=".22"/>
<g font-family="Arial,Helvetica,sans-serif"><circle cx="32" cy="27" r="3" fill="#b8a5f2"/><text x="46" y="31" font-size="11" letter-spacing="2.5" fill="#a89ace">PUBLIC SIGNAL</text>{''.join(content)}</g>
</svg>\n'''

def main():
    repos=[]
    for page in range(1,11):
        batch=api(f'users/{OWNER}/repos?type=owner&per_page=100&page={page}')
        repos.extend(batch)
        if len(batch)<100: break
    else: raise RuntimeError('Repository pagination exceeded the expected bound')
    original=[r for r in repos if not r.get('private') and not r['fork'] and r['name'].lower()!=OWNER.lower()]
    if not original: raise RuntimeError('No public builds returned; preserving the previous artwork')
    languages={r['language'] for r in original if r.get('language')}
    release=api(f'repos/{OWNER}/delulu-talks/releases/latest')['tag_name']
    pushed=max(r['pushed_at'] for r in original)[:10]
    # Gather everything before writing either variant. Partial API failures leave both untouched.
    outputs={f'observatory{"-compact" if compact else ""}.svg':artwork(len(original),len(languages),release,pushed,compact) for compact in [False,True]}
    for name,content in outputs.items(): (ROOT/'assets'/name).write_text(content)
    print(f'Public snapshot: {len(original)} original builds, {len(languages)} primary languages, release {release}.')

if __name__=='__main__': main()
