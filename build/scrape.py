#!/usr/bin/env python3
import re, json, base64, urllib.request, concurrent.futures, os, html as htmllib

UA = {'User-Agent':'Mozilla/5.0'}
BASE = 'https://darktide.gameslantern.com'
CLASSES = [
 {'key':'veteran','name':'Veteran','ig':'veteran','build':'9a4f4fdd-f4ef-4ea1-b7d6-71bf513e90d1/havoc-bolter-vet-fuplaayz'},
 {'key':'zealot','name':'Zealot','ig':'zealot','build':'9a4fa304-0b88-4cf8-827a-d0435327a8c3/zealot-infodump-no-stealth-auric'},
 {'key':'ogryn','name':'Ogryn','ig':'ogryn','build':'a07df7b0-bb70-49fc-972e-237b68db7582/the-immortal-shieldgryn-h-40'},
 {'key':'psyker','name':'Psyker','ig':'psyker','build':'9ba81400-4c60-4362-9756-f93428dfc021/azyr-psyker'},
 {'key':'arbites','name':'Arbites','ig':'adamant','build':'9f35c673-7c83-4bd1-9d77-a25d7b19984d/execution-order-nuncio-aquila-arbites'},
 {'key':'skitarii','name':'Skitarii','ig':'cryptic','build':'a21148b3-6004-4042-a145-af61ce6b67ee/skitarii-sniper'},
 {'key':'hivescum','name':'Hive Scum','ig':'broker','build':'a0aaf6c0-6b02-4472-b679-1a93866ad0a2/the-chemist-v4'},
]

def get(url, binary=False, tries=3):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read() if binary else r.read().decode('utf-8','replace')
        except Exception as e:
            if i==tries-1: return None

IMG_RE = re.compile(r'<image\b[^>]*?(?:xlink:href|href)="([^"]+)"[^>]*?/?>', re.S)
def img_attrs(tag):
    d={}
    for k in ('x','y','width','height'):
        m=re.search(k+r'="([^"]+)"', tag); d[k]=float(m.group(1)) if m else None
    m=re.search(r'(?:xlink:href|href)="([^"]+)"', tag); d['href']=m.group(1) if m else ''
    return d

def pick_main_svg(html):
    svgs = re.findall(r'<svg\b.*?</svg>', html, re.S)
    if not svgs: return ''
    return max(svgs, key=lambda s: s.count('<line'))

FOLDER_CAT = {'keystone':'keystone','keystone_modifier':'keymod','ability':'ability',
              'ability_modifier':'abilmod','aura':'aura','tactical':'blitz','default':'passive',
              'broker_stimm':'stimm'}

def extract_svg(svg, ig, rootkey):
    nodes=[]
    icon_urls={}   # key -> art url
    for am in re.finditer(r'<a\b[^>]*?href="([^"]+)"[^>]*>(.*?)</a>', svg, re.S):
        href, inner = am.group(1), am.group(2)
        if '/abilities/' not in href: continue
        slug = href.split('/abilities/')[-1].strip('/')
        imgs=[]
        for im in re.finditer(r'<image\b[^>]*?/?>', inner, re.S):
            imgs.append(img_attrs(im.group(0)))
        if not imgs: continue
        # position from any frame/base image (all share x,y,width)
        base_im = imgs[0]
        x,y,w = base_im['x'],base_im['y'],base_im['width'] or 80
        # shape from frame href
        allh = ' '.join(i['href'] for i in imgs)
        shape='c'
        if 'square' in allh: shape='s'
        elif 'hex' in allh: shape='h'
        elif 'diamond' in allh: shape='d'
        stat = 'circular_small' in allh
        # art icon
        art=None; cat='passive'
        for i in imgs:
            h=i['href']
            if f'/talents/{ig}/' in h:
                art=h
                mfold=re.search(rf'/talents/{ig}/([^/]+)/', h)
                cat=FOLDER_CAT.get(mfold.group(1),'passive') if mfold else 'passive'
                x,y,w=i['x'],i['y'],i['width'] or w
                break
            if '/talent_root/' in h:
                art=h; cat='root'; x,y,w=i['x'],i['y'],i['width'] or w
        if art is None:
            cat='stat'
        if slug=='' :
            cat='root'
        key = slug if slug else rootkey
        if art: icon_urls[key]=(art if art.startswith('http') else BASE+art)
        nodes.append({'s':key,'slug':slug,'x':round(x+w/2),'y':round(y+w/2),'shape':shape,'cat':cat})
    # class-root emblem (its anchor does not link to /abilities/, so capture its image directly)
    rootm=re.search(r'<image\b[^>]*?(?:xlink:href|href)="([^"]*?/talent_root/[^"]+)"[^>]*?/?>', svg, re.S)
    if rootm and not any(n['cat']=='root' for n in nodes):
        ri=img_attrs(rootm.group(0)); rurl=ri['href']; rurl=rurl if rurl.startswith('http') else BASE+rurl
        rw=ri['width'] or 90
        icon_urls[rootkey]=rurl
        nodes.append({'s':rootkey,'slug':'','x':round(ri['x']+rw/2),'y':round(ri['y']+rw/2),'shape':'c','cat':'root'})
    # edges
    edges=set()
    for lm in re.finditer(r'<line\b[^>]*>', svg):
        t=lm.group(0)
        def gv(k):
            m=re.search(k+r'="([^"]+)"',t); return round(float(m.group(1))) if m else None
        x1,y1,x2,y2=gv('x1'),gv('y1'),gv('x2'),gv('y2')
        if None in (x1,y1,x2,y2): continue
        a=(x1,y1); b=(x2,y2)
        if a>b: a,b=b,a
        edges.add((a[0],a[1],b[0],b[1]))
    return nodes, sorted(edges), icon_urls

def parse_class(cl):
    html = get(f'{BASE}/builds/{cl["build"]}')
    svg = pick_main_svg(html)
    cl['nodes'],cl['edges'],cl['icon_urls'] = extract_svg(svg, cl['ig'], f'root-{cl["ig"]}')
    cl['budget']=30
    print(f'{cl["name"]}: {len(cl["nodes"])} nodes, {len(cl["edges"])} edges, {len(cl["icon_urls"])} icons')
    return cl

# ---- phase 1: parse graphs ----
for cl in CLASSES:
    parse_class(cl)

# ---- phase 1b: Hive Scum Stimm sub-tree (a second SVG on the Hive Scum page) ----
hs_html = get(f'{BASE}/builds/{CLASSES[-1]["build"]}')   # Hive Scum is last in CLASSES
stimm_svg = next((s for s in re.findall(r'<svg\b.*?</svg>', hs_html, re.S)
                  if 'broker_stimm' in s and s.count('<line')>10), '')
n,e,ic = extract_svg(stimm_svg, 'broker', 'root-brokerstimm')
STIMM={'key':'hivescum-stimm','name':'Hive Scum — Stimm','ig':'broker',
       'nodes':n,'edges':e,'icon_urls':ic,'budget':None}
CLASSES.append(STIMM)
print(f'{STIMM["name"]}: {len(n)} nodes, {len(e)} edges, {len(ic)} icons')

# ---- phase 2: descriptions (unique slugs) ----
slugs = sorted({n['slug'] for cl in CLASSES for n in cl['nodes'] if n['slug'] and n['cat']!='stat'})
print('unique slugs to fetch:', len(slugs))
TYPE_RE = re.compile(r'text-\[#707d67\][^>]*>\s*<div>([^<]+)</div>')
NAME_RE = re.compile(r'text-\[#d7e4ce\][^"]*text-lg[^"]*">([^<]+)<')
DESC_RE = re.compile(r'text-\[#a7be97\][^"]*leading-5[^"]*">(.*?)</div>', re.S)
def strip_tags(s):
    s=re.sub(r'<[^>]+>',' ',s); s=htmllib.unescape(s); return re.sub(r'\s+',' ',s).strip()
def fetch_desc(slug):
    h=get(f'{BASE}/abilities/{slug}')
    if not h: return slug,{'n':slug,'t':'','d':''}
    t=TYPE_RE.search(h); n=NAME_RE.search(h); d=DESC_RE.search(h)
    return slug,{'n':strip_tags(n.group(1)) if n else slug,
                 't':strip_tags(t.group(1)) if t else '',
                 'd':strip_tags(d.group(1)) if d else ''}
DESC={}
with concurrent.futures.ThreadPoolExecutor(max_workers=24) as ex:
    for slug,info in ex.map(fetch_desc, slugs):
        DESC[slug]=info
missing=[s for s in slugs if not DESC[s]['d']]
print('descriptions fetched; missing text:', len(missing), missing[:10])

# attach desc to nodes
for cl in CLASSES:
    for n in cl['nodes']:
        info=DESC.get(n['slug'],{})
        n['n']=info.get('n') or (n['slug'].replace('-',' ').title() if n['slug'] else cl['name']+' (class node)')
        n['t']=info.get('t') or ('' )
        n['d']=info.get('d') or ('Minor stat node.' if n['cat']=='stat' else ('The '+cl['name']+' class node — always active.' if n['cat']=='root' else ''))

# ---- phase 3: download icons ----
ICONS={}
allicons={}
for cl in CLASSES:
    allicons.update(cl['icon_urls'])
def dl(item):
    key,url=item
    b=get(url,binary=True)
    if not b: return key,None
    return key,'data:image/webp;base64,'+base64.b64encode(b).decode()
with concurrent.futures.ThreadPoolExecutor(max_workers=24) as ex:
    for key,uri in ex.map(dl, allicons.items()):
        if uri: ICONS[key]=uri
print('icons downloaded:', len(ICONS), 'of', len(allicons))

# ---- phase 4: assemble data.json ----
PAD=70
out={'classes':[], 'icons':ICONS}
for cl in CLASSES:
    xs=[n['x'] for n in cl['nodes']]; ys=[n['y'] for n in cl['nodes']]
    vb=[min(xs)-PAD, min(ys)-PAD, (max(xs)-min(xs))+2*PAD, (max(ys)-min(ys))+2*PAD]
    out['classes'].append({'key':cl['key'],'name':cl['name'],'ig':cl['ig'],'viewbox':vb,'budget':cl.get('budget',30),
        'nodes':[{k:n[k] for k in ('s','x','y','shape','cat','n','t','d')} for n in cl['nodes']],
        'edges':cl['edges']})
with open('data.json','w',encoding='utf-8') as f:
    json.dump(out,f,ensure_ascii=False,separators=(',',':'))
print('WROTE data.json size(MB):', round(os.path.getsize('data.json')/1e6,2))
