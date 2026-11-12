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
MAGS = [(14, 49, 0.22, 0.7), (42, 30, 0.22, 0.45), (35.3, 32.0, 0.055, 1.9), (50.5, 26.5, 0.05, 1.4), (106, 14, 0.16, 0.3), (-72, 12, 0.12, 0.3)] if os.environ.get('WARP', '0') == '1' else []   # off: the owner wants one true scale everywhere, no stretched regions
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
# the magnifier must never fold the map over itself: check the stretch stays positive everywhere
_e = 1e-4; _gx, _gy = base_xy(_lo, _la)
_ax, _ = warp(_gx + _e, _gy); _bx, _ = warp(_gx - _e, _gy); _, _ay = warp(_gx, _gy + _e); _, _by = warp(_gx, _gy - _e)
print('min stretch x %.3f y %.3f' % (((_ax - _bx) / (2 * _e)).min(), ((_ay - _by) / (2 * _e)).min()))
assert ((_ax - _bx) > 0).all() and ((_ay - _by) > 0).all(), 'magnifier folds the map'
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
ALWAYS_PLAYABLE = {'JOR', 'PSE', 'GBR', 'KOR'}
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

# ---------- doctrine (small stat flavour, docs/research/regional_doctrines.md): 6 doctrines ----------
ARAB_LEAGUE = {'DZA', 'BHR', 'COM', 'DJI', 'EGY', 'IRQ', 'JOR', 'KWT', 'LBN', 'LBY', 'MRT', 'MAR', 'OMN', 'PSE', 'QAT', 'SAU', 'SOM', 'SDN', 'SYR', 'TUN', 'ARE', 'YEM'}
EURASIA = {'RUS', 'BLR', 'KAZ', 'KGZ', 'TJK', 'TKM', 'UZB', 'ARM', 'AZE', 'MNG'}
for c in countries.values():
    i, r = c['iso'], c['region_un'] or ''
    if i in ARAB_LEAGUE or i in ('TUR', 'IRN'): c['doctrine'] = 'mena'
    elif i in EURASIA: c['doctrine'] = 'eurasia'
    elif r == 'Europe' or i in ('GEO', 'UKR', 'MDA', 'CYP'): c['doctrine'] = 'europe'
    elif r == 'Asia': c['doctrine'] = 'asia'
    elif r == 'Africa': c['doctrine'] = 'africa'
    else: c['doctrine'] = 'americas'
    if i in ARAB_LEAGUE: c['art'] = 'gulf'

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
    want = ncities(c) if c['class'] != 'playable' else max(3, ncities(c))
    gap = MIN_GAP
    while len(chosen) < min(want, len(cand)) and gap > MIN_GAP * 0.3:   # small playable states still get 3+ cities
        gap *= 0.75
        for p in cand:
            if p in chosen or len(chosen) >= want: continue
            if 'x' in p and nation[int(np.clip(p['y'], 0, H - 1)), int(np.clip(p['x'], 0, W - 1))] == ids.index(a3) \
               and all(math.hypot(p['x'] - q['x'], p['y'] - q['y']) >= gap for q in chosen):
                chosen.append(p)
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
    # provinces like CoN: start from the real states/provinces (keeps their names and where people live),
    # merge the tiny ones, split the huge ones into a few clean pieces (straight edges, like CoN's provinces)
    kpx = (c.get('area_km2') or 1) / max(1, int(sub_m.sum()))              # km2 per pixel for this country
    carea = c.get('area_km2') or 0
    tiny = max(4000.0, carea / 70) / kpx
    big = min(700000.0, max(40000.0, carea / 14)) / kpx
    tgt_max = max(len(c['cities']) + 1, min(int(round(carea / 15000)), 90))
    if c['class'] == 'neutral': tiny, big, tgt_max = 1e18, 1e18, 1
    areas = collections.Counter(reg[reg >= 0].ravel().tolist())
    a1_px = dict(areas)
    members = {r: [labs[r]] for r in areas if r < len(labs) and labs[r] >= 0}   # which real states/provinces each region holds
    named_by_city = {}
    suffix = {}
    def neighbours(r):
        mm = reg == r
        ring = ndi.binary_dilation(mm, iterations=2) & ~mm & (reg >= 0)
        return collections.Counter(reg[ring].tolist())
    guard = 0
    while len(areas) > 1 and guard < 3000:
        guard += 1
        r = min(areas, key=lambda k: areas[k] + (10 ** 12 if k in city_reg else 0))
        if not (areas[r] < tiny or len(areas) > tgt_max): break
        nb = neighbours(r)
        opts = [n for n in nb if not (n in city_reg and r in city_reg)]
        if not opts:
            if r in city_reg: break
            others = [k for k in areas if k != r]
            if not others: break
            opts = [others[0]]
        n = min(opts, key=lambda k: areas[k])
        reg[reg == r] = n; areas[n] += areas.pop(r)
        members.setdefault(n, []).extend(members.pop(r, []))
        if r in city_reg: city_reg[n] = city_reg.pop(r)
    # split huge regions into k compact pieces (k-means on the pixels: straight borders between the pieces)
    DIRS = [('North', 'الشمالية'), ('South', 'الجنوبية'), ('East', 'الشرقية'), ('West', 'الغربية'), ('Central', 'الوسطى')]
    for r in list(areas):
        if areas[r] <= big * 1.25: continue
        k = int(min(8, np.ceil(areas[r] / big)))
        rr = np.argwhere(reg == r).astype(np.float64)
        rng_ = np.random.default_rng(int(r) + 7)
        cen = rr[rng_.choice(len(rr), k, replace=False)]
        for _ in range(12):
            own_ = np.argmin(((rr[::7, None, :] - cen[None]) ** 2).sum(-1), 1)
            for j in range(k):
                sel = rr[::7][own_ == j]
                if len(sel): cen[j] = sel.mean(0)
        own_ = np.argmin(((rr[:, None, :] - cen[None]) ** 2).sum(-1), 1)
        mid = rr.mean(0)
        nxt = reg.max() + 1
        for j in range(k):
            sel = rr[own_ == j].astype(np.int64)
            dy, dx = cen[j] - mid
            d = 4 if np.hypot(dy, dx) < np.sqrt(len(rr)) * 0.15 else (0 if -dy > abs(dx) else 1 if dy > abs(dx) else 2 if dx > 0 else 3)
            if j == 0: suffix[int(r)] = d; continue
            reg[sel[:, 0], sel[:, 1]] = nxt
            members[nxt] = list(members.get(r, [])); suffix[nxt] = d
            # a city inside this piece moves with it
            for kk in list(city_reg.get(r, [])):
                q = cities[kk]
                if reg[int(np.clip(q['y'] - y0, 0, y1 - y0 - 1)), int(np.clip(q['x'] - x0, 0, x1 - x0 - 1))] == nxt:
                    city_reg[r].remove(kk); city_reg.setdefault(nxt, []).append(kk)
            nxt += 1
        if r in city_reg and not city_reg[r]: city_reg.pop(r)
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
                if int(r) in suffix and not ks:
                    de, da = DIRS[suffix[int(r)]]; pname_en = f'{de} {pname_en}'; pname_ar = f'{pname_ar} {da}'
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
    # sea: the satellite ocean is nearly black; use a calm game sea instead, lighter near coasts like real shallows
    sea = ~land
    dist = ndi.distance_transform_edt(sea) * (8192 / W)
    shallow = np.exp(-dist / 18.0)[..., None]
    deep = np.array([44, 86, 122], np.float32); coast = np.array([82, 140, 160], np.float32)   # lighter, fresher sea (dark seas read as old)
    noise = ndi.zoom(ndi.gaussian_filter(np.random.default_rng(5).random((H // 16 + 1, W // 16 + 1)), 2), 16, order=1)[:H, :W, None]
    seacol = deep * (1 - shallow) + coast * shallow
    seacol *= 0.94 + 0.12 * (noise - noise.mean()) / (noise.std() + 1e-6) * 0.5
    # keep a little of the real satellite colour in shallow water (reefs, sandbanks)
    seacol = seacol * (1 - 0.25 * shallow) + img.astype(np.float32) * 0.25 * shallow
    img = np.where(sea[..., None], np.clip(seacol, 0, 255), img).astype(np.uint8)
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
        for c in cs: f.write(f"- {c['name_en']} / {c['name_ar']} ({c['iso']}): {c['area_km2']:,} km², {len(c['cities'])} cities, {len(c['provinces'])} provinces, art {c['art']}, doctrine {c['doctrine']}\n")
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

# ---------- tiles for the game ----------
# Land is graded into one natural green terrain (like CoN): real satellite detail and relief, with every
# region textured (forest canopy, fields, dry scrub, hills). The game recolours it per relation with
# shadow-to-highlight ramps, so the terrain always shows through and nothing looks painted on.
# Sea pixels carry a light/shadow code (128 = no change): the land's shadow falls on the water and
# shallows are lighter. The game lays this over its animated waves.
if sat:
    T = 512; M = 2 * W; MH = 2 * H
    nat4 = (raster([(i + 1, countries[a]['geoms']) for i, a in enumerate(ids)], (M, MH)) - 1).astype(np.int16)
    if os.path.exists(lakes_f):
        nat4[raster([(1, [f['geometry'] for f in load('ne_10m_lakes.geojson') if (f['properties'].get('scalerank') or 0) <= 3])], (M, MH)) > 0] = -1
    # canals and narrow straits: far too thin to see at world scale, so they are cut a few pixels wide.
    # Ships can sail through them, and whoever holds the land can close them.
    CANALS = {'suez': [(32.31, 31.30), (32.33, 30.80), (32.36, 30.45), (32.56, 30.20), (32.56, 29.90)],
              'panama': [(-79.93, 9.40), (-79.80, 9.18), (-79.62, 9.02), (-79.53, 8.88)],
              'bosphorus': [(29.14, 41.25), (29.05, 41.05), (28.98, 40.98)],
              'dardanelles': [(26.18, 40.02), (26.40, 40.20), (26.72, 40.42)],
              'kiel': [(9.12, 53.88), (9.45, 54.10), (9.80, 54.28), (10.16, 54.38)]}
    cim = Image.new('L', (M, MH), 0); cd_ = ImageDraw.Draw(cim)
    for nm, pts in CANALS.items():
        xs, ys = to_px([q[0] for q in pts], [q[1] for q in pts])
        cd_.line(list(zip((xs * 2).tolist(), (ys * 2).tolist())), fill=255, width=5, joint='curve')
    nat4[np.asarray(cim) > 0] = -1
    del cim
    lf = (nat4 >= 0).astype(np.float32)
    shallow = np.clip(ndi.gaussian_filter(lf, 26) * 2.0, 0, 1) ** 1.4
    dsh = 9
    shadow = np.zeros_like(lf); shadow[dsh:, dsh:] = lf[:-dsh, :-dsh]              # sun from the north-west
    shadow = ndi.gaussian_filter(shadow, 5)
    S4 = np.asarray(Image.open(sat).convert('RGB')); sh4, sw4 = S4.shape[:2]
    relief_f = os.path.join(DATA, 'world.relief.jpg')
    HS = np.asarray(Image.open(relief_f).convert('L')) if os.path.exists(relief_f) else None
    hs_mid = float(np.median(HS[::16, ::16])) / 255 if HS is not None else 0.5
    print('relief', HS is not None, hs_mid)
    # source crops over north Arabia, kept for checking joins in the source images
    def _crop(img, name):
        hh, ww = img.shape[:2]
        Image.fromarray(img[int((90 - 33) / 180 * hh):int((90 - 28) / 180 * hh), int((38 + 180) / 360 * ww):int((48 + 180) / 360 * ww)]).save(os.path.join(OUT, name), quality=90)
    _crop(S4, 'debug_sat.jpg')
    if HS is not None: _crop(HS, 'debug_relief.jpg')
    PD = 1024
    def detail(names):
        out = []
        for nm in names:
            f = os.path.join('art/sat', nm + '.jpg')
            if not os.path.exists(f): continue
            a = np.asarray(Image.open(f).convert('RGB').resize((PD, PD), Image.LANCZOS)).astype(np.float32) / 255
            a = a - ndi.gaussian_filter(a, (9, 9, 0))                                # fine grain only: no big shapes that could repeat
            a = a / (a.std() + 1e-6) * 0.05
            # seamless tile: cross-fade with a half-shifted copy (no mirrors, so no butterfly patterns)
            u = np.clip((1 - np.abs(np.linspace(-1, 1, PD, endpoint=False))) * 4, 0, 1)
            a = a * u[None, :, None] + np.roll(a, PD // 2, 1) * (1 - u[None, :, None])     # wrap left-right
            a = a * u[:, None, None] + np.roll(a, PD // 2, 0) * (1 - u[:, None, None])     # then top-bottom
            out.append(a)
        return out
    D = {'forest': detail(['forest', 'forest2']), 'farm': detail(['farmland', 'farmland2', 'grass']), 'arid': detail(['scrub']), 'rock': detail(['hills'])}
    def dsample(lst, yy, xx, k=0):
        if not lst: return 0
        a = lst[k % len(lst)]
        return a[np.ix_((yy + 311 * k) % PD, (xx + 173 * k) % PD)]
    big = ndi.zoom(ndi.gaussian_filter(np.random.default_rng(9).random((MH // 64 + 2, M // 64 + 2)), 1.5), 64, order=1)[:MH, :M]
    big = (big - big.mean()) / big.std()
    # ---- tiles in the new format (the CoN way: one painted ground, coloured per owner by the game) ----
    #   {x}_{y}.jpg   grey: big light and shade only (real relief, land shadow on the sea)
    #   {x}_{y}_b.png half size, land: R forest density, G desert, B bare rock; sea: R = coastal water
    #   {x}_{y}_n.png country ids
    # The game paints the ground itself from small textures (forest, fields, desert, rock), crisp at every zoom.
    # coastal water band (sea zones near the coast are lighter grey-blue, open ocean deep blue, hard edge)
    lf8 = lf[::8, ::8]
    lab8, nl8 = ndi.label(lf8 > 0.5)
    big8 = np.isin(lab8, np.nonzero(np.bincount(lab8.ravel()) >= 40)[0][1:])      # islands smaller than ~15,000 km2 don't push the band out
    near = (ndi.distance_transform_edt(~big8) < 13) | (ndi.distance_transform_edt(lf8 < 0.5) < 4)
    deep = ~near
    dl, nd_ = ndi.label(deep)
    deep &= np.isin(dl, np.nonzero(np.bincount(dl.ravel()) >= 900)[0][1:])        # no small deep pockets inside enclosed seas
    coast8 = ndi.gaussian_filter((~deep).astype(np.float32), 3.0)                 # coastal waters, soft-cornered outline
    del lab8, dl
    rng8 = np.random.default_rng(21)
    clump8 = ndi.gaussian_filter(rng8.standard_normal(lf8.shape), 1.6); clump8 /= clump8.std()      # forest clumps
    depth8 = ndi.gaussian_filter(rng8.standard_normal(lf8.shape), 7.0); depth8 /= depth8.std()      # slow dark patches in deep water
    half = np.zeros((H, W), np.uint8); halfb = np.zeros((H // 2, W // 2, 3), np.uint8)
    manifest = {str(z): [] for z in range(5)}
    d4 = os.path.join(OUT, 'tiles', '4'); os.makedirs(d4, exist_ok=True)
    MARG = 200                     # wider than the 4-sigma reach of the brightness blur: no lines between strips
    def write_tile(d, z, tx, ty, lum, bio, nid):
        if not ((nid >= 0).any() or (np.abs(lum.astype(np.int16) - 128).max() > 6) or bio[..., 0].any()): return
        Image.fromarray(lum, 'L').save(os.path.join(d, f'{tx}_{ty}.jpg'), quality=90)
        Image.fromarray(bio, 'RGB').save(os.path.join(d, f'{tx}_{ty}_b.png'), optimize=True)
        v = nid.astype(np.int32) + 1
        Image.fromarray(np.dstack([v % 256, v // 256, np.zeros_like(v)]).astype(np.uint8)).save(os.path.join(d, f'{tx}_{ty}_n.png'), optimize=True)
        manifest[str(z)].append(f'{tx}_{ty}')
    for ty in range(0, MH, T):
        a0, a1 = max(0, ty - MARG), min(MH, ty + T + MARG)
        py, px = np.mgrid[a0:a1, 0:M].astype(np.float64)
        lon, lat = from_px(px / 2 + 0.25, py / 2 + 0.25)
        sx = np.clip(((lon + 180) / 360 * sw4).astype(np.int32), 0, sw4 - 1)
        sy = np.clip(((90 - lat) / 180 * sh4).astype(np.int32), 0, sh4 - 1)
        del py, px, lon, lat
        c = S4[sy, sx].astype(np.float32) / 255
        r, g, b = c[..., 0], c[..., 1], c[..., 2]
        L = 0.3 * r + 0.59 * g + 0.11 * b
        veg = np.clip((g - 0.92 * r) * 9 + 0.25, 0, 1)
        forest = ndi.gaussian_filter(veg * np.clip((0.27 - L) * 8, 0, 1), 1.5)
        arid = ndi.gaussian_filter((1 - veg) * np.clip((L - 0.2) * 5, 0, 1), 1.5)
        snow = np.clip((c.min(-1) - 0.72) * 6, 0, 1)
        # big brightness, heavily flattened: only a hint of the real land (river valleys, oases) stays
        Lb = ndi.gaussian_filter(L, 6) + 0.04
        broad = np.clip((Lb / 0.3) ** 0.18, 0.85, 1.12)
        if HS is not None:
            h = HS[np.clip((sy.astype(np.float64) * HS.shape[0] / sh4).astype(np.int32), 0, HS.shape[0] - 1),
                   np.clip((sx.astype(np.float64) * HS.shape[1] / sw4).astype(np.int32), 0, HS.shape[1] - 1)].astype(np.float32) / 255
            h = ndi.gaussian_filter(h, 2.6)                                         # painted, broad soft ridges (no crumpled noise)
            # only real mountain ranges show: where the ground is rough over a wide area. Plains stay calm.
            hm = ndi.gaussian_filter(h, 10)
            hstd = np.sqrt(np.maximum(ndi.gaussian_filter(h * h, 10) - hm * hm, 0))
            mnt = np.clip((hstd - 0.05) / 0.05, 0, 1)
            relief = np.clip(1 + 2.4 * (h - hm) * mnt + 0.25 * (hm - hs_mid) * mnt, 0.45, 1.5)
            rough = mnt * np.clip(np.abs(h - hm) * 8, 0, 1)
        else: relief = np.ones_like(L); rough = np.zeros_like(L)
        # forest as clumps: dense real forest keeps its own shape, everywhere else a few scattered woods
        cl = ndi.zoom(clump8[a0 // 8:a1 // 8 + 2], 8, order=1)[:a1 - a0, :M]
        dry = np.clip((ndi.gaussian_filter(arid, 24) - 0.3) * 3, 0, 1)           # inside deserts: no satellite 'forest' (dark coasts, towns, oases)
        forest = forest * (1 - dry)
        woods = np.clip((cl - 1.6) * 2.5, 0, 1) * (1 - 0.75 * arid)          # a few scattered woods, not a carpet
        forest = np.clip(np.maximum(forest * np.clip((forest - 0.25) * 2.2, 0, 1) * np.clip(cl * 0.35 + 0.8, 0, 1), woods), 0, 1)
        rock = np.clip(np.maximum(rough * (1 - forest), snow), 0, 1)
        lum = np.clip(0.5 * relief * broad + 0.25 * snow, 0, 1)
        k0 = ty - a0; rows = min(T, MH - ty)
        sl = slice(k0, k0 + rows)
        lum, forest, arid, rock = lum[sl], forest[sl], arid[sl], rock[sl]
        nidr = nat4[ty:ty + rows]
        seam = nidr < 0
        dp = ndi.zoom(depth8[ty // 8:(ty + rows) // 8 + 2], 8, order=1)[:rows, :M]
        v = (128 - 82 * shadow[ty:ty + rows] + 22 * shallow[ty:ty + rows] - 9 * np.clip(dp, -1.5, 2.5)) / 255
        lum = np.where(seam, v, lum)
        coast = np.clip((ndi.zoom(coast8[ty // 8:(ty + rows) // 8 + 2], 8, order=1)[:rows, :M] - 0.3) / 0.4, 0, 1)   # soft edge, like CoN's sea zones
        bio = np.dstack([np.where(seam, coast * 1.0, forest), np.where(seam, 0, arid), np.where(seam, 0, rock)])
        lum8 = (np.clip(lum, 0, 1) * 255).astype(np.uint8); bio8 = (np.clip(bio, 0, 1) * 255).astype(np.uint8)
        bio2 = bio8[::2, ::2]
        for tx in range(0, M, T):
            write_tile(d4, 4, tx // T, ty // T, lum8[:, tx:tx + T], bio2[:, tx // 2:(tx + T) // 2], nidr[:, tx:tx + T])
        half[ty // 2:ty // 2 + rows // 2] = np.asarray(Image.fromarray(lum8).resize((W, rows // 2), Image.LANCZOS))
        halfb[ty // 4:ty // 4 + rows // 4] = bio8[::4, ::4][:rows // 4, :W // 2]
        print('tile row', ty // T, flush=True)
    del S4, shadow, shallow, lf
    nat3 = nat4[::2, ::2]
    for z in range(4):
        f = 2 ** (3 - z); w, h = W // f, H // f
        sa = np.asarray(Image.fromarray(half).resize((w, h), Image.LANCZOS)) if f > 1 else half
        sb = np.asarray(Image.fromarray(halfb).resize((w // 2, h // 2), Image.BILINEAR))
        ni = nat3[::f, ::f][:h, :w]
        d = os.path.join(OUT, 'tiles', str(z)); os.makedirs(d, exist_ok=True)
        for ty in range(0, h, T):
            for tx in range(0, w, T):
                write_tile(d, z, tx // T, ty // T, sa[ty:ty + T, tx:tx + T], sb[ty // 2:(ty + T) // 2, tx // 2:(tx + T) // 2], ni[ty:ty + T, tx:tx + T])
    json.dump(manifest, open(os.path.join(OUT, 'tiles', 'tiles.json'), 'w'), separators=(',', ':'))
    print('tiles written', {z: len(v) for z, v in manifest.items()})
    del nat4

# ---------- smooth vector borders: shared segments between two countries (no coastlines) ----------
# Drawn live by the game as anti-aliased lines, styled by relation, crisp at every zoom.
from skimage import measure
def shared_borders(label, n_labels, same_group=None, tol=0.45):
    """Smooth contour segments shared by two labels (never coastlines). same_group(a, b) filters pairs."""
    segs = collections.defaultdict(list)
    pad = 2
    objs = ndi.find_objects(label + 1)
    for ci in range(n_labels):
        sl = objs[ci] if ci < len(objs) else None     # find_objects(label + 1)[ci] is label value ci
        if sl is None: continue
        y0, y1 = max(sl[0].start - pad, 0), min(sl[0].stop + pad, H)
        x0, x1 = max(sl[1].start - pad, 0), min(sl[1].stop + pad, W)
        nsub = label[y0:y1, x0:x1]
        sub = (nsub == ci).astype(np.float32)
        for cont in measure.find_contours(ndi.gaussian_filter(sub, 0.7), 0.5):
            cur, owner_prev = [], None
            for kk in range(len(cont)):
                yy, xx = cont[kk]
                a = cont[max(kk - 1, 0)]; b = cont[min(kk + 1, len(cont) - 1)]
                ty, tx = b[0] - a[0], b[1] - a[1]; L = math.hypot(ty, tx) or 1
                best = -1
                for sgn in (1, -1):
                    py, px = int(round(yy + sgn * tx / L * 2.2)), int(round(xx - sgn * ty / L * 2.2))
                    if 0 <= py < nsub.shape[0] and 0 <= px < nsub.shape[1]:
                        v = nsub[py, px]
                        if v != ci: best = v
                ok = best >= 0 and best > ci and (same_group is None or same_group(ci, best))
                if ok:
                    if owner_prev not in (None, best) and len(cur) > 1:
                        segs[(ci, owner_prev)].append(cur); cur = []
                    cur.append((xx + x0, yy + y0)); owner_prev = best
                else:
                    if len(cur) > 1: segs[(ci, owner_prev)].append(cur)
                    cur, owner_prev = [], None
            if len(cur) > 1: segs[(ci, owner_prev)].append(cur)
    out = []
    for (a, b), lines in segs.items():
        for ln in lines:
            arr = measure.approximate_polygon(np.array(ln), tolerance=tol)
            if len(arr) >= 2: out.append({'a': int(a), 'b': int(b), 'p': [round(float(v), 1) for xy in arr for v in xy]})
    return out
# thin gaps between neighbouring countries (polygon rasterising) would hide their shared border: fill them first
_land = nation >= 0
_gap = ndi.binary_closing(_land, structure=np.ones((5, 5)), iterations=1) & ~_land
_, (_iy, _ix) = ndi.distance_transform_edt(~_land, return_indices=True)
nation_f = nation.copy(); nation_f[_gap] = nation[_iy[_gap], _ix[_gap]]
print('border gaps filled', int(_gap.sum()))
borders_out = shared_borders(nation_f, len(ids))
json.dump(borders_out, open(os.path.join(OUT, 'borders.json'), 'w'), separators=(',', ':'))
print('border segments', len(borders_out))
pcountry = [p['country'] for p in prov_meta]
pb = shared_borders(province, len(prov_meta), lambda a, b: pcountry[a] == pcountry[b], tol=2.2)   # clean straight segments, like CoN's provinces
json.dump([[round(v) if False else v for v in x['p']] for x in pb], open(os.path.join(OUT, 'province_lines.json'), 'w'), separators=(',', ':'))
print('province lines', len(pb))
