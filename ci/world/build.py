# Builds the real-world game map from free public-domain data.
#   Natural Earth (public domain) vectors, Palestine point-of-view borders: countries, states/provinces, cities, rivers, lakes
#   NASA Blue Marble (public domain) satellite colour
# Output (art/world/): world.jpg, nations.png, provinces.png, world.json, preview.jpg, classes.md
# Run: python3 ci/world/build.py <data dir> <out dir>      env: W=8192  WARP=1
import json, math, os, sys, collections
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage as ndi
from pyproj import Geod

DATA, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
Image.MAX_IMAGE_PIXELS = None
W = int(os.environ.get('W', '8192'))
LAT_N, LAT_S = 80.0, -56.0          # Antarctica and the far Arctic are cut: nothing to fight over, wasted space
GEOD = Geod(ellps='WGS84')

# ---------- projection: Miller cylindrical + a gentle magnifier on crowded regions ----------
def miller(lat): return 1.25 * np.log(np.tan(np.pi / 4 + 0.4 * np.radians(lat)))
Y_N, Y_S = miller(LAT_N), miller(LAT_S)
H = int(round(W * (Y_N - Y_S) / (2 * np.pi)))
# magnifiers: centre (lon, lat), radius in map units, strength. Monotonic (no folding) while strength < 2.
# Europe and the Middle East have many small countries close together; the oceans and Siberia give room.
MAGS = [(14, 49, 0.22, 0.55), (42, 30, 0.22, 0.45), (36, 33, 0.07, 0.6), (106, 14, 0.16, 0.3), (-72, 12, 0.12, 0.3)] if os.environ.get('WARP', '1') == '1' else []
def base_xy(lon, lat):
    return np.radians(lon), miller(np.clip(lat, LAT_S - 5, LAT_N + 5))
MAGP = [(*base_xy(lo, la), r, s) for lo, la, r, s in MAGS]
def warp(x, y):
    dx = np.zeros_like(x); dy = np.zeros_like(y)
    for cx, cy, r, s in MAGP:
        ex, ey = x - cx, y - cy
        g = s * np.exp(-(ex * ex + ey * ey) / (r * r))
        dx += ex * g; dy += ey * g
    return x + dx, y + dy
def unwarp(X, Y):
    x, y = X.copy(), Y.copy()
    for _ in range(25):                      # fixed point: x = X - D(x)
        wx, wy = warp(x, y)
        x -= (wx - X) * 0.8; y -= (wy - Y) * 0.8
    return x, y
# frame the warped world so the whole land fits
_lo, _la = np.meshgrid(np.linspace(-180, 180, 721), np.linspace(LAT_S, LAT_N, 300))
_x, _y = warp(*base_xy(_lo, _la))
X0, X1, YB0, YB1 = _x.min(), _x.max(), _y.min(), _y.max()
H = int(round(W * (YB1 - YB0) / (X1 - X0)))
def to_px(lon, lat):
    x, y = warp(*base_xy(np.asarray(lon, float), np.asarray(lat, float)))
    return (x - X0) / (X1 - X0) * W, (YB1 - y) / (YB1 - YB0) * H
def from_px(px, py):
    X = X0 + px / W * (X1 - X0); Y = YB1 - py / H * (YB1 - YB0)
    x, y = unwarp(X, Y)
    lat = np.degrees((np.arctan(np.exp(y / 1.25)) - np.pi / 4) / 0.4)
    return np.degrees(x), lat
print('map', W, 'x', H)

# ---------- countries ----------
def load(name):
    p = os.path.join(DATA, name)
    return json.load(open(p, encoding='utf-8'))['features']
src = 'ne_10m_admin_0_countries_pse.geojson' if os.path.exists(os.path.join(DATA, 'ne_10m_admin_0_countries_pse.geojson')) else 'ne_10m_admin_0_countries.geojson'
print('countries from', src)
feats = load(src)
P = lambda f, *ks: next((f['properties'][k] for k in ks if f['properties'].get(k) not in (None, '', '-99')), None)
MERGE = {'ISR': 'PSE', 'PSX': 'PSE', 'PSR': 'PSE', 'GAZ': 'PSE', 'WEB': 'PSE', 'SAH': 'MAR', 'ESH': 'MAR'}
# Arab-world view: one Palestine (no Israel); Western Sahara part of Morocco; Golan stays Syrian (fixed below by city/admin data)
countries = collections.OrderedDict()
for f in feats:
    a3 = P(f, 'ADM0_A3', 'ADM0_A3_PS', 'ISO_A3', 'SOV_A3')
    if a3 in ('ATA', 'ATF'): continue
    a3 = MERGE.get(a3, a3)
    c = countries.setdefault(a3, {'iso': a3, 'geoms': [], 'name_en': None, 'name_ar': None,
                                  'subregion': P(f, 'SUBREGION'), 'region_un': P(f, 'REGION_UN'), 'continent': P(f, 'CONTINENT')})
    if a3 == P(f, 'ADM0_A3', 'ISO_A3') or c['name_en'] is None:
        c['name_en'] = P(f, 'NAME_EN', 'NAME', 'ADMIN'); c['name_ar'] = P(f, 'NAME_AR')
    c['geoms'].append(f['geometry'])
pal = countries.get('PSE')
if pal: pal.update(name_en='Palestine', name_ar='فلسطين', subregion='Western Asia', region_un='Asia')
if 'MAR' in countries: countries['MAR'].update(name_en='Morocco', name_ar='المغرب')

def polys(g):
    if g['type'] == 'Polygon': return [g['coordinates']]
    if g['type'] == 'MultiPolygon': return g['coordinates']
    return []
def geod_area(c):
    a = 0.0
    for g in c['geoms']:
        for poly in polys(g):
            for k, ring in enumerate(poly):
                lon, lat = zip(*[(p[0], p[1]) for p in ring])
                ar, _ = GEOD.polygon_area_perimeter(lon, lat)
                a += abs(ar) * (1 if k == 0 else -1)
    return a / 1e6
for c in countries.values(): c['area_km2'] = round(geod_area(c))

# ---------- who plays: owner's rules ----------
#   tiny (Bahrain-like): neutral land, 2 free infantry, anyone can take it
#   small (Qatar-size up to below the playable line): AI nation
#   Oman-like and bigger: playable, plus Jordan and Palestine
NEUTRAL_MAX = float(os.environ.get('NEUTRAL_MAX', '6000'))
PLAYABLE_MIN = float(os.environ.get('PLAYABLE_MIN', '100000'))
ALWAYS_PLAYABLE = {'JOR', 'PSE'}
for c in countries.values():
    a = c['area_km2']
    c['class'] = 'playable' if (a >= PLAYABLE_MIN or c['iso'] in ALWAYS_PLAYABLE) else ('neutral' if a < NEUTRAL_MAX else 'ai')

# ---------- art region (building style); doctrine is a separate table ----------
MENA = {'Western Asia', 'Northern Africa'}
GULF_EXTRA = {'IRN', 'AFG', 'PAK', 'SDN', 'MRT', 'SOM', 'DJI', 'ERI'}
EURO_FROM_WASIA = {'GEO', 'ARM', 'AZE', 'CYP'}
for c in countries.values():
    s, r = c['subregion'] or '', c['region_un'] or ''
    if (s in MENA or c['iso'] in GULF_EXTRA) and c['iso'] not in EURO_FROM_WASIA: c['art'] = 'gulf'
    elif r == 'Europe' or c['iso'] in EURO_FROM_WASIA: c['art'] = 'europe'
    elif r == 'Asia': c['art'] = 'asia'
    else: c['art'] = 'americas'

# ---------- rasterise countries ----------
ids = list(countries)
SS = 2  # supersample for clean coastlines
def raster(features_by_id, size):
    w, h = size
    im = Image.new('I', (w, h), 0); d = ImageDraw.Draw(im)
    for idx, geoms in features_by_id:
        for g in geoms:
            for poly in polys(g):
                for k, ring in enumerate(poly):
                    xs, ys = to_px([p[0] for p in ring], [p[1] for p in ring])
                    # skip rings crossing the date line wrap (Chukotka, Fiji): split at the seam
                    pts = list(zip((xs * w / W).tolist(), (ys * h / H).tolist()))
                    if len(pts) < 3: continue
                    if np.ptp(xs) > W * 0.7:
                        for side in (0, 1):
                            q = [(x if (x < w / 2) == (side == 0) else (0 if side == 0 else w - 1), y) for x, y in pts]
                            d.polygon(q, fill=(idx if k == 0 else 0))
                    else:
                        d.polygon(pts, fill=(idx if k == 0 else 0))
    return np.asarray(im, np.int32)
nation = raster([(i + 1, countries[a]['geoms']) for i, a in enumerate(ids)], (W, H)) - 1   # -1 = sea
land = nation >= 0
print('land px', land.sum())

# lakes back to water
lakes_f = os.path.join(DATA, 'ne_10m_lakes.geojson')
if os.path.exists(lakes_f):
    lk = raster([(1, [f['geometry'] for f in load('ne_10m_lakes.geojson') if (f['properties'].get('scalerank') or 0) <= 3])], (W, H)) > 0
    nation[lk] = -1; land = nation >= 0

# ---------- cities ----------
places = load('ne_10m_populated_places.geojson')
by_c = collections.defaultdict(list)
for f in places:
    pr = f['properties']
    a3 = MERGE.get(pr.get('ADM0_A3'), pr.get('ADM0_A3'))
    if a3 not in countries: continue
    lon, lat = f['geometry']['coordinates'][:2]
    if not (LAT_S < lat < LAT_N): continue
    x, y = to_px(lon, lat)
    by_c[a3].append({'name_en': pr.get('NAME_EN') or pr.get('NAME'), 'name_ar': pr.get('NAME_AR') or pr.get('NAME'),
                     'pop': int(pr.get('POP_MAX') or 0), 'capital': 'Admin-0 capital' in (pr.get('FEATURECLA') or '') and 'alt' not in (pr.get('FEATURECLA') or '').lower(),
                     'x': float(x), 'y': float(y), 'lon': lon, 'lat': lat})
CAP_FIX = {'PSE': 'Jerusalem', 'MAR': 'Rabat'}
MIN_GAP = W * float(os.environ.get('CITY_GAP', '0.0085'))       # cities never closer than this on screen: no crowding (UK gets few, spaced cities)
def ncities(c):
    if c['class'] == 'neutral': return 1
    if c['class'] == 'ai': return 2 if c['area_km2'] < 40000 else 3
    return int(np.clip(round(3 + 1.3 * math.log2(max(c['area_km2'], 50000) / 50000)), 4, 9))
for a3, c in countries.items():
    cand = sorted(by_c.get(a3, []), key=lambda p: (-(p['capital'] or p['name_en'] == CAP_FIX.get(a3)), -p['pop']))
    chosen = []
    for p in cand:
        xi, yi = int(np.clip(p['x'], 0, W - 1)), int(np.clip(p['y'], 0, H - 1))
        if nation[yi, xi] != ids.index(a3):                         # snap to own land (coastal capitals on the edge)
            near = np.argwhere(nation[max(0, yi - 12):yi + 13, max(0, xi - 12):xi + 13] == ids.index(a3))
            if not len(near): continue
            yi, xi = near[np.argmin(((near - 12) ** 2).sum(1))] + [max(0, yi - 12), max(0, xi - 12)]
            p['x'], p['y'] = float(xi), float(yi)
        if all(math.hypot(p['x'] - q['x'], p['y'] - q['y']) >= MIN_GAP for q in chosen):
            chosen.append(p)
        if len(chosen) >= ncities(c): break
    for k, p in enumerate(chosen): p['kind'] = 'capital' if k == 0 else ('major' if k <= 2 else 'minor')
    c['cities'] = chosen

# ---------- provinces: real states/provinces, merged or split to a size that plays well ----------
adm1 = load('ne_10m_admin_1_states_provinces.geojson')
groups = collections.defaultdict(list)
for f in adm1:
    a3 = MERGE.get(f['properties'].get('adm0_a3'), f['properties'].get('adm0_a3'))
    if a3 in countries: groups[a3].append(f)
a1_list = [(a3, f) for a3, fs in groups.items() for f in fs]
a1 = raster([(i + 1, [f['geometry']]) for i, (a3, f) in enumerate(a1_list)], (W, H)) - 1
a1[~land] = -1
province = np.full((H, W), -1, np.int32)
prov_meta = []
def target_prov(c):
    n = len(c['cities'])
    if c['class'] == 'neutral': return 1
    return int(max(n + 2, round(n * 2.2)))
for ci, a3 in enumerate(ids):
    c = countries[a3]
    m = nation == ci
    if not m.any(): c['provinces'] = []; continue
    ys, xs = np.where(m)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    if x1 - x0 > W * 0.6:  # wraps around the date line (Russia, USA with Aleutians): work on the full width
        x0, x1 = 0, W
    sub_m = m[y0:y1, x0:x1]
    sub = np.where(sub_m, a1[y0:y1, x0:x1], -1)
    # pixels of this country not covered by any admin-1 polygon: give them the nearest admin-1
    hole = sub_m & (sub < 0)
    if hole.any() and (sub >= 0).any():
        _, (iy, ix) = ndi.distance_transform_edt(sub < 0, return_indices=True)
        sub[hole] = sub[iy[hole], ix[hole]]
    if not (sub >= 0).any(): sub = np.where(sub_m, 0, -1)
    labs = [l for l in np.unique(sub) if l >= 0]
    lab = {l: i for i, l in enumerate(labs)}
    lut = np.full(sub.max() + 2, -1); lut[np.array(labs) + 1] = np.arange(len(labs)); reg = lut[sub + 1]
    # city in each region
    cities = c['cities']
    city_reg = {}
    for k, p in enumerate(cities):
        r = reg[int(np.clip(p['y'] - y0, 0, y1 - y0 - 1)), int(np.clip(p['x'] - x0, 0, x1 - x0 - 1))]
        city_reg.setdefault(int(r), []).append(k)
    # merge smallest regions into the smallest neighbour until the target count (never two city regions together)
    tgt = target_prov(c)
    areas = collections.Counter(reg[reg >= 0].ravel().tolist())
    a1_px = dict(areas)
    members = {r: [labs[r]] for r in areas if r < len(labs) and labs[r] >= 0}   # which real states/provinces each region holds
    named_by_city = {}
    def neighbours(r):
        mm = reg == r
        ring = ndi.binary_dilation(mm, iterations=2) & ~mm & (reg >= 0)
        return collections.Counter(reg[ring].tolist())
    guard = 0
    while len(areas) > tgt and guard < 2000:
        guard += 1
        r = min(areas, key=lambda k: areas[k] + (10 ** 12 if k in city_reg else 0))
        nb = neighbours(r)
        opts = [n for n in nb if not (n in city_reg and r in city_reg)]
        if not opts:
            if r in city_reg: break
            # island with no neighbour: join the nearest region
            others = [k for k in areas if k != r]
            if not others: break
            opts = [others[0]]
        n = min(opts, key=lambda k: areas[k])
        reg[reg == r] = n; areas[n] += areas.pop(r)
        members.setdefault(n, []).extend(members.pop(r, []))
        if r in city_reg: city_reg[n] = city_reg.pop(r)
    # split regions holding 2+ cities between those cities (nearest city wins)
    for r, ks in list(city_reg.items()):
        if len(ks) < 2: continue
        rr = np.argwhere(reg == r)
        pts = np.array([[cities[k]['y'] - y0, cities[k]['x'] - x0] for k in ks])
        owner = np.argmin(((rr[:, None, :] - pts[None]) ** 2).sum(-1), 1)
        nxt = reg.max() + 1
        for j, k in enumerate(ks[1:], 1):
            sel = rr[owner == j]; reg[sel[:, 0], sel[:, 1]] = nxt; city_reg[nxt] = [k]; named_by_city[nxt] = k; nxt += 1
        city_reg[r] = [ks[0]]
    plist = []
    for r in np.unique(reg[reg >= 0]):
        pm = reg == r
        pid = len(prov_meta)
        province[y0:y1, x0:x1][pm] = pid
        cy, cx = ndi.center_of_mass(pm)
        ks = city_reg.get(int(r), [])
        if ks: cx, cy = cities[ks[0]]['x'] - x0, cities[ks[0]]['y'] - y0
        # real name: the better-known state/province it holds (Natural Earth label rank, then size);
        # a piece split off for a second city takes that city's name
        if int(r) in named_by_city:
            q = cities[named_by_city[int(r)]]; pname_en, pname_ar = q['name_en'], q['name_ar']
        else:
            mem = members.get(int(r), [])
            def fame(i):
                pr = a1_list[i][1]['properties']
                return (pr.get('labelrank') or 9, -(a1_px.get(labs.index(i), 0) if i in labs else 0))
            if mem:
                best = a1_list[min(mem, key=fame)][1]['properties']
                pname_en = best.get('name_en') or best.get('name'); pname_ar = best.get('name_ar') or pname_en
            else:
                pname_en, pname_ar = c['name_en'], c['name_ar']
        prov_meta.append({'id': pid, 'country': a3, 'name_en': pname_en, 'name_ar': pname_ar, 'centre': [round(float(cx + x0), 1), round(float(cy + y0), 1)],
                          'city': cities[ks[0]]['kind'] if ks else 'rural', 'city_name_en': cities[ks[0]]['name_en'] if ks else None,
                          'city_name_ar': cities[ks[0]]['name_ar'] if ks else None, 'px': int(pm.sum())})
        plist.append(pid)
    c['provinces'] = plist
print('provinces', len(prov_meta))

# ---------- satellite colour ----------
sat = None
for nm in sorted(os.listdir(DATA)):
    if nm.startswith('world.') and nm.endswith(('.jpg', '.png')): sat = os.path.join(DATA, nm)
if sat:
    S = Image.open(sat).convert('RGB')
    if S.width > 2 * W: S = S.resize((2 * W, W), Image.LANCZOS)
    S = np.asarray(S); sh, sw = S.shape[:2]
    img = np.zeros((H, W, 3), np.uint8)
    for y0 in range(0, H, 256):
        py, px = np.mgrid[y0:min(H, y0 + 256), 0:W].astype(np.float64)
        lon, lat = from_px(px + 0.5, py + 0.5)
        sx = np.clip(((lon + 180) / 360 * sw).astype(int), 0, sw - 1)
        sy = np.clip(((90 - lat) / 180 * sh).astype(int), 0, sh - 1)
        img[y0:y0 + 256] = S[sy, sx]
    Image.fromarray(img).save(os.path.join(OUT, 'world.jpg'), quality=90)
else:
    img = np.where(land[..., None], np.array([90, 110, 70], np.uint8), np.array([20, 40, 60], np.uint8))
    print('no satellite image found')

# ---------- save layers ----------
def save_ids(a, name):
    v = a + 1
    Image.fromarray(np.dstack([v % 256, v // 256, np.zeros_like(v)]).astype(np.uint8)).save(os.path.join(OUT, name))
save_ids(nation, 'nations.png'); save_ids(province, 'provinces.png')
out = {'size': [W, H], 'projection': {'type': 'miller+magnify', 'lat': [LAT_S, LAT_N], 'mags': MAGS, 'frame': [X0, X1, YB0, YB1]},
       'countries': [{k: v for k, v in c.items() if k != 'geoms'} | {'index': i} for i, c in enumerate(countries.values())],
       'provinces': prov_meta}
json.dump(out, open(os.path.join(OUT, 'world.json'), 'w', encoding='utf-8'), ensure_ascii=False)

# ---------- report: who is playable, for the owner to check ----------
with open(os.path.join(OUT, 'classes.md'), 'w', encoding='utf-8') as f:
    for cl in ('playable', 'ai', 'neutral'):
        cs = sorted((c for c in countries.values() if c['class'] == cl), key=lambda c: -c['area_km2'])
        f.write(f'## {cl} ({len(cs)})\n\n')
        for c in cs: f.write(f"- {c['name_en']} / {c['name_ar']} ({c['iso']}): {c['area_km2']:,} km², {len(c['cities'])} cities, {len(c['provinces'])} provinces, art {c['art']}\n")
        f.write('\n')

# ---------- preview: random country colours, borders, cities ----------
rng = np.random.default_rng(1)
pal = rng.integers(60, 230, (len(ids), 3))
prev = img.astype(np.float32)
tint = np.where(land[..., None], pal[np.clip(nation, 0, None)], 0)
prev = np.where(land[..., None], prev * 0.55 + tint * 0.45, prev)
def edges(a):
    e = np.zeros(a.shape, bool); e[1:] |= a[1:] != a[:-1]; e[:, 1:] |= a[:, 1:] != a[:, :-1]; return e
prev[edges(province) & land] = prev[edges(province) & land] * 0.5 + 120
prev[ndi.binary_dilation(edges(nation)) & land] = 250
pim = Image.fromarray(np.clip(prev, 0, 255).astype(np.uint8)); d = ImageDraw.Draw(pim)
for c in countries.values():
    for p in c['cities']:
        r = {'capital': 7, 'major': 5, 'minor': 3}[p['kind']] * W / 8192
        d.ellipse([p['x'] - r, p['y'] - r, p['x'] + r, p['y'] + r], fill=(255, 220, 60) if p['kind'] == 'capital' else (255, 255, 255), outline=(0, 0, 0))
pim.save(os.path.join(OUT, 'preview.jpg'), quality=88)
pim.resize((2048, int(2048 * H / W)), Image.LANCZOS).save(os.path.join(OUT, 'preview_small.jpg'), quality=88)
# crops of crowded areas at full size to check spacing
for nm, (lo, la) in {'europe': (10, 50), 'mideast': (42, 28), 'levant': (36, 32)}.items():
    x, y = to_px(lo, la); x, y = int(x), int(y)
    pim.crop((x - 1000, y - 700, x + 1000, y + 700)).save(os.path.join(OUT, f'crop_{nm}.jpg'), quality=88)
print('done')
