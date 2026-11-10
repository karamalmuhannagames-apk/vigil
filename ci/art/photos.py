"""Fetches public-domain military photographs from Wikimedia Commons, with credits,
and cuts the subject out of the background. Only files marked Public domain are taken."""
import json, os, sys, time, urllib.parse, urllib.request
UA = {'User-Agent': 'vigil-game-art/1.0 (private hobby project; contact via GitHub karamalmuhannagames-apk)'}
UNITS = {
    'tank': 'M1A2 Abrams tank', 'ifv': 'M2 Bradley fighting vehicle', 'artillery': 'M109 Paladin howitzer',
    'rockets': 'M142 HIMARS launcher', 'airdefense': 'Patriot missile launcher', 'truck': 'HEMTT truck convoy',
    'helicopter': 'AH-64 Apache helicopter flight', 'fighter': 'F-16 Fighting Falcon in flight', 'drone': 'MQ-9 Reaper in flight',
    'destroyer': 'Arleigh Burke class destroyer underway', 'infantry': 'infantry soldiers patrol rear view',
}
os.makedirs('art/photo', exist_ok=True); os.makedirs('art/cut', exist_ok=True)
credits = json.load(open('art/CREDITS.json')) if os.path.exists('art/CREDITS.json') else {}
def api(params):
    url = 'https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode(params)
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60))
for name, query in UNITS.items():
    if any(k.startswith(name + '_') for k in credits): continue
    try:
        d = api({'action': 'query', 'format': 'json', 'generator': 'search', 'gsrnamespace': 6, 'gsrsearch': query + ' filetype:bitmap', 'gsrlimit': 30,
                 'prop': 'imageinfo', 'iiprop': 'url|extmetadata|size|mime', 'iiurlwidth': 1280})
    except Exception as e:
        print('search failed', name, repr(e)[:200]); continue
    pages = sorted(d.get('query', {}).get('pages', {}).values(), key=lambda p: p.get('index', 99))
    n = 0
    for p in pages:
        ii = (p.get('imageinfo') or [{}])[0]; meta = ii.get('extmetadata', {})
        lic = meta.get('LicenseShortName', {}).get('value', '')
        if ii.get('mime') != 'image/jpeg' or not lic.lower().startswith('public domain') or ii.get('width', 0) < 1200: continue
        key = f'{name}_{n + 1}'
        try:
            data = urllib.request.urlopen(urllib.request.Request(ii['thumburl'], headers=UA), timeout=120).read()
        except Exception as e:
            print('download failed', key, repr(e)[:120]); continue
        open(f'art/photo/{key}.jpg', 'wb').write(data)
        credits[key] = {'title': p['title'], 'page': ii.get('descriptionurl'), 'license': lic,
                        'artist': meta.get('Artist', {}).get('value', '')[:200], 'credit': meta.get('Credit', {}).get('value', '')[:200]}
        print('ok', key, p['title'][:70]); n += 1; time.sleep(1)
        if n >= 4: break
    time.sleep(1)
json.dump(credits, open('art/CREDITS.json', 'w'), indent=1, ensure_ascii=False)
# Cut the subjects out.
try:
    from rembg import remove, new_session
    from PIL import Image
    sess = new_session('isnet-general-use')
    for f in sorted(os.listdir('art/photo')):
        out = 'art/cut/' + f.replace('.jpg', '.png')
        if os.path.exists(out): continue
        im = Image.open('art/photo/' + f).convert('RGB')
        cut = remove(im, session=sess); box = cut.getbbox()
        if box: cut = cut.crop(box)
        cut.thumbnail((640, 640)); cut.save(out); print('cut', f, cut.size)
except Exception as e:
    print('cutout step failed', repr(e)[:300])
