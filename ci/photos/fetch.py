# Fetch public-domain war photos for the loading screens from Wikimedia Commons.
# Keeps only files whose licence is public domain (mostly US military photos), at least 1600 px wide.
# Writes art/loading/raw/<topic>_<n>.jpg and art/loading/raw/credits.json
import json, os, re, sys, time, urllib.parse, urllib.request
API = 'https://commons.wikimedia.org/w/api.php'
UA = {'User-Agent': 'HalberdStudio-asset-fetch/1.0 (loading screen research)'}
TOPICS2 = {
  'cyber': 'Cyber Shield exercise soldiers computer',
  'cyber2': 'cyber protection team network defense',
  'cyber3': 'Army Cyber Command soldier laptop',
  'missile': 'missile launch test fire',
  'mlrs': 'M142 HIMARS live fire',
  'radar': 'military radar air defense night',
}
TOPICS = {
  'tank': 'M1A2 Abrams tank desert firing',
  'tank2': 'Leopard 2 tank exercise',
  'jet': 'F-16 Fighting Falcon afterburner takeoff',
  'jet2': 'F-35 Lightning flight formation',
  'ship': 'Arleigh Burke class destroyer underway',
  'carrier': 'aircraft carrier flight deck launch',
  'sub': 'submarine surfaced underway navy',
  'heli': 'AH-64 Apache helicopter flight',
  'soldiers': 'soldiers patrol desert exercise',
  'artillery': 'M109 howitzer firing',
  'missile': 'Patriot missile launch',
  'mlrs': 'HIMARS rocket launch',
  'cyber': 'cyber operations center army soldiers computers',
  'command': 'tactical operations center military screens',
}
def get(params):
    url = API + '?' + urllib.parse.urlencode(params)
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return json.load(r)
out = 'art/loading/raw'; os.makedirs(out, exist_ok=True)
credits = {}
import sys
if len(sys.argv) > 1 and sys.argv[1] == '2': TOPICS = TOPICS2
for topic, q in TOPICS.items():
    try:
        d = get({'action': 'query', 'format': 'json', 'generator': 'search', 'gsrsearch': f'{q} filetype:bitmap', 'gsrnamespace': 6, 'gsrlimit': 40,
                 'prop': 'imageinfo', 'iiprop': 'url|size|extmetadata', 'iiurlwidth': 2000})
    except Exception as e:
        print('search failed', topic, e); continue
    got = 0
    pages = sorted(d.get('query', {}).get('pages', {}).values(), key=lambda p: p.get('index', 99))
    for p in pages:
        ii = (p.get('imageinfo') or [{}])[0]; md = ii.get('extmetadata', {})
        lic = md.get('LicenseShortName', {}).get('value', '')
        if 'public domain' not in lic.lower(): continue
        if ii.get('width', 0) < 1600 or ii.get('width', 0) < ii.get('height', 1): continue
        src = ii.get('thumburl') or ii.get('url')
        name = f'{topic}_{got}.jpg'
        try:
            with urllib.request.urlopen(urllib.request.Request(src, headers=UA), timeout=120) as r, open(f'{out}/{name}', 'wb') as f: f.write(r.read())
        except Exception as e:
            print('download failed', src, e); continue
        artist = re.sub('<[^>]+>', '', md.get('Artist', {}).get('value', ''))[:200]
        credits[name] = {'title': p['title'], 'page': f"https://commons.wikimedia.org/wiki/{urllib.parse.quote(p['title'].replace(' ', '_'))}", 'licence': lic, 'author': artist}
        got += 1; print('ok', name, p['title'])
        if got >= 3: break
        time.sleep(0.5)
old = json.load(open(f'{out}/credits.json')) if os.path.exists(f'{out}/credits.json') else {}
old.update(credits)
json.dump(old, open(f'{out}/credits.json', 'w'), indent=1)
print('total', len(credits))
