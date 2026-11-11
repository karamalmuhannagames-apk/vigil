# Finds and downloads artist-made 3D vehicle models from Sketchfab that are free for commercial use.
# Only CC0 (no conditions) and CC-BY (credit required) are accepted. Share-alike, no-derivatives and
# non-commercial licences are rejected. Every chosen model is recorded in art/models/CREDITS.json.
#   python3 ci/models/fetch.py search     -> art/models/candidates.json (no token needed)
#   python3 ci/models/fetch.py download   -> models/<unit>/... (needs SKETCHFAB_TOKEN)
import json, os, sys, time, urllib.request, urllib.parse, zipfile, io

API = 'https://api.sketchfab.com/v3'
OK_LICENCES = {'cc0', 'by'}
QUERIES = {
    'infantry':   ['soldier rifleman', 'modern soldier'],
    'motor_inf':  ['humvee', 'mrap vehicle', 'military jeep'],
    'airborne':   ['paratrooper', 'airborne soldier'],
    'specops':    ['special forces operator', 'navy seal'],
    'light_tank': ['light tank', 'm8 ags', 'sprut'],
    'atgm':       ['tank destroyer', 'atgm vehicle', 'kornet vehicle'],
    'mortar':     ['mortar carrier', 'self propelled mortar'],
    'towed':      ['towed howitzer', 'm777'],
    'sam_mid':    ['buk', 'nasams', 'sam launcher'],
    'sam_long':   ['patriot missile', 's-300', 's-400'],
    'heli_trans': ['black hawk', 'uh-60', 'mi-8', 'nh90'],
    'heli_naval': ['seahawk', 'ka-27', 'naval helicopter'],
    'multirole':  ['f-18', 'rafale', 'gripen', 'mig-29'],
    'stealth_f':  ['f-35', 'f-22', 'su-57', 'j-20'],
    'strike':     ['a-10', 'su-25', 'su-34'],
    'bomber':     ['b-52', 'tu-95', 'b-1 lancer', 'tu-160'],
    'stealth_b':  ['b-2 spirit', 'b-21'],
    'awacs':      ['e-3 sentry', 'awacs', 'a-50'],
    'mpa':        ['p-8 poseidon', 'p-3 orion'],
    'transport':  ['c-130', 'c-17', 'il-76'],
    'drone_recon':['global hawk', 'mq-1 predator', 'recon drone'],
    'drone_strike':['mq-9 reaper', 'bayraktar tb2', 'attack drone'],
    'loiter':     ['shahed', 'loitering munition', 'switchblade drone'],
    'corvette':   ['corvette warship', 'patrol boat military'],
    'cruiser':    ['ticonderoga cruiser', 'slava cruiser'],
    'carrier':    ['aircraft carrier', 'nimitz'],
    'landing':    ['landing ship', 'amphibious assault ship', 'landing craft'],
    'sub_missile':['ohio class', 'cruise missile submarine'],
    'sub_ballistic':['ballistic missile submarine', 'borei submarine'],
    'coastal':    ['coastal missile launcher', 'bastion missile', 'anti ship missile truck'],
    'cruise_m':   ['tomahawk missile', 'cruise missile'],
    'ballistic_m':['iskander', 'ballistic missile launcher', 'scud launcher'],
    'engineer':   ['combat engineer vehicle', 'armoured bridge layer'],
    'minesweeper':['minesweeper', 'mine countermeasure ship'],
}

def get(url, token=None, tries=6):
    for i in range(tries):
        req = urllib.request.Request(url, headers={'User-Agent': 'vigil-game-art-pipeline'})
        if token: req.add_header('Authorization', 'Token ' + token)
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 429 and i < tries - 1:
                wait = 30 * (i + 1); print('rate limited, waiting', wait, 's'); time.sleep(wait); continue
            raise

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
    old = json.load(open('art/models/CREDITS.json')) if os.path.exists('art/models/CREDITS.json') else []
    credits = [c for c in old if os.path.exists(f"art/units/{c['unit']}_green.png") and not os.environ.get('FORCE')]
    done = {c['unit'] for c in credits}
    for unit, uid in picks.items():
        if unit in done: print('already rendered', unit); continue
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
        time.sleep(6)
    os.makedirs('art/models', exist_ok=True)
    json.dump(credits, open('art/models/CREDITS.json', 'w'), indent=1)

if __name__ == '__main__':
    {'search': search, 'download': download}[sys.argv[1]]()
