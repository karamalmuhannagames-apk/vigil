# Finds and downloads artist-made 3D vehicle models from Sketchfab that are free for commercial use.
# Only CC0 (no conditions) and CC-BY (credit required) are accepted. Share-alike, no-derivatives and
# non-commercial licences are rejected. Every chosen model is recorded in art/models/CREDITS.json.
#   python3 ci/models/fetch.py search     -> art/models/candidates.json (no token needed)
#   python3 ci/models/fetch.py download   -> models/<unit>/... (needs SKETCHFAB_TOKEN)
import json, os, sys, time, urllib.request, urllib.parse, zipfile, io

API = 'https://api.sketchfab.com/v3'
OK_LICENCES = {'cc0', 'by'}
QUERIES = {
    'tank':    ['main battle tank', 'abrams tank', 'leopard 2', 't-90 tank', 'challenger 2'],
    'ifv':     ['bradley ifv', 'bmp-2', 'cv90', 'infantry fighting vehicle'],
    'apc':     ['m113', 'armored personnel carrier', 'btr-80'],
    'car':     ['stryker', 'boxer 8x8', 'lav-25', '8x8 armored vehicle'],
    'spaa':    ['gepard', 'tunguska', 'pantsir', 'anti aircraft tank'],
    'arty':    ['m109 howitzer', 'pzh 2000', '2s19 msta', 'self propelled howitzer'],
    'mlrs':    ['himars', 'm270 mlrs', 'bm-21 grad', 'rocket launcher truck'],
    'truck':   ['military truck', 'kamaz military', 'mtvr', 'army truck'],
    'fighter': ['f-16', 'su-27', 'f-15 eagle', 'eurofighter typhoon', 'fighter jet'],
    'heli':    ['ah-64 apache', 'ka-52', 'mi-28', 'attack helicopter'],
    'frigate': ['frigate', 'destroyer warship', 'navy frigate'],
    'sub':     ['submarine', 'nuclear submarine'],
}

def get(url, token=None):
    req = urllib.request.Request(url, headers={'User-Agent': 'vigil-game-art-pipeline'})
    if token: req.add_header('Authorization', 'Token ' + token)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()

def search():
    out = {}
    for unit, qs in QUERIES.items():
        seen = {}
        for q in qs:
            for lic in OK_LICENCES:
                params = urllib.parse.urlencode({'type': 'models', 'q': q, 'downloadable': 'true',
                                                 'license': lic, 'sort_by': '-likeCount', 'count': 24})
                try:
                    data = json.loads(get(f'{API}/search?{params}'))
                except Exception as e:
                    print('search failed', unit, q, lic, e); continue
                for m in data.get('results', []):
                    l = (m.get('license') or {}).get('slug') or lic
                    if l not in OK_LICENCES: continue
                    seen[m['uid']] = {
                        'uid': m['uid'], 'name': m['name'], 'licence': l,
                        'author': (m.get('user') or {}).get('displayName') or (m.get('user') or {}).get('username'),
                        'author_url': (m.get('user') or {}).get('profileUrl'),
                        'url': m.get('viewerUrl'), 'likes': m.get('likeCount', 0),
                        'faces': m.get('faceCount'), 'query': q,
                        'thumb': max((m.get('thumbnails') or {}).get('images', [{'width': 0, 'url': ''}]), key=lambda t: t.get('width', 0)).get('url'),
                    }
                time.sleep(0.4)
        out[unit] = sorted(seen.values(), key=lambda m: -m['likes'])[:12]
        print(unit, len(seen), 'candidates;', ', '.join(f"{m['name']} ({m['licence']}, {m['likes']} likes)" for m in out[unit][:4]))
    os.makedirs('art/models', exist_ok=True)
    json.dump(out, open('art/models/candidates.json', 'w'), indent=1)

def download():
    token = os.environ.get('SKETCHFAB_TOKEN')
    if not token: sys.exit('SKETCHFAB_TOKEN missing: add it as a repository secret')
    picks = json.load(open('ci/models/picks.json'))
    credits = []
    for unit, uid in picks.items():
        info = json.loads(get(f'{API}/models/{uid}'))
        lic = (info.get('license') or {}).get('slug')
        if lic not in OK_LICENCES:
            print('skip', unit, uid, 'licence', lic); continue
        dl = json.loads(get(f'{API}/models/{uid}/download', token))
        url = (dl.get('gltf') or {}).get('url')
        if not url: print('no gltf for', unit); continue
        z = zipfile.ZipFile(io.BytesIO(get(url)))
        z.extractall(f'models/{unit}')
        credits.append({'unit': unit, 'name': info['name'], 'author': info['user']['displayName'],
                        'author_url': info['user'].get('profileUrl'), 'url': info.get('viewerUrl'),
                        'licence': 'CC0' if lic == 'cc0' else 'CC BY 4.0'})
        print('downloaded', unit, info['name'], lic)
        time.sleep(1)
    os.makedirs('art/models', exist_ok=True)
    json.dump(credits, open('art/models/CREDITS.json', 'w'), indent=1)

if __name__ == '__main__':
    {'search': search, 'download': download}[sys.argv[1]]()
