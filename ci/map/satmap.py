# Builds the map from real satellite photo patches (Copernicus Sentinel-2) laid over our invented
# continent by terrain type, CoN-style: plain realistic land, plain blue sea, thin white borders.
import os, sys, glob
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
MASKS, SAT, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
m = np.load(MASKS)
land, height, forest, farm, river, shade = (m[k] for k in ('land', 'height', 'forest', 'farm', 'river', 'shade'))
S = land.shape[0]
rng = np.random.default_rng(5)
TARGET_MEAN = np.array([0.34, 0.52, 0.24]); TARGET_STD = np.array([0.05, 0.06, 0.045])

def load_patch(path):
    a = np.asarray(Image.open(path).convert('RGB')).astype(np.float32) / 255
    a = a[40:-40, 40:-40]
    valid = a.mean(-1) > 0.02
    mu = a[valid].mean(0); sd = a[valid].std(0) + 1e-4
    a = (a - mu) / sd * TARGET_STD + TARGET_MEAN            # every patch toned to one calm green palette
    g = a.mean(-1, keepdims=True); a = g + (a - g) * 1.0     # slightly muted, like CoN
    return np.clip(a, 0, 1)

def tiled(p, off):
    big = np.concatenate([p, p[:, ::-1]], 1); big = np.concatenate([big, big[::-1]], 0)   # mirrored: no seams
    h, w = big.shape[:2]
    oy, ox = off
    yy = (np.arange(S) + oy) % h; xx = (np.arange(S) + ox) % w
    return big[yy][:, xx]

def layer(names):
    ps = [load_patch(f) for n in names for f in glob.glob(os.path.join(SAT, n + '.jpg'))]
    if not ps: return None
    out = tiled(ps[0], rng.integers(0, 1500, 2))
    if len(ps) > 1:
        mix = ndi.gaussian_filter(rng.random((S // 64 + 2, S // 64 + 2)), 1)
        mix = ndi.zoom(mix, S / (S // 64 + 2), order=1)[:S, :S]
        mix = np.clip((mix - mix.mean()) * 8 + 0.5, 0, 1)[..., None]
        out = out * mix + tiled(ps[1], rng.integers(0, 1500, 2)) * (1 - mix)
    return out

L = {k: layer(v) for k, v in {'farm': ['farmland', 'farmland2'], 'forest': ['forest', 'forest2'],
                              'hills': ['hills', 'mountain'], 'base': ['grass', 'scrub']}.items()}
L = {k: v for k, v in L.items() if v is not None}
w_forest = np.clip(forest * 1.2, 0, 1)
w_hills = np.clip((height - 0.45) * 3, 0, 1) * (1 - w_forest)
w_farm = np.clip(farm * 1.2, 0, 1) * (1 - w_forest) * (1 - w_hills)
w_base = np.clip(1 - w_forest - w_hills - w_farm, 0, 1)
W = {'forest': w_forest, 'hills': w_hills, 'farm': w_farm, 'base': w_base}
W = {k: ndi.gaussian_filter(v, 6) for k, v in W.items() if k in L}
tot = sum(W.values()) + 1e-6
ground = sum(L[k] * (W[k] / tot)[..., None] for k in W)
ground *= (0.78 + 0.35 * shade[..., None])                 # real relief light: geography shows when zoomed

# ---------- sea ----------
YY, XX = np.mgrid[0:S, 0:S]
dist = ndi.distance_transform_edt(~land)
halo = np.exp(-dist / (S * 0.022))[..., None]                     # soft lighter water near every coast
deep = np.array([0.13, 0.25, 0.34]); shallow = np.array([0.24, 0.40, 0.46])
sea = deep * (1 - halo) + shallow * halo
far = np.clip(dist / (S * 0.3), 0, 1)[..., None]
sea *= (1 - 0.12 * far)                                            # open ocean a touch darker
broad = ndi.gaussian_filter(rng.random((S // 64, S // 64)), 1.5)
broad = ndi.zoom(broad, S / broad.shape[0], order=1)[:S, :S]
sea *= (0.94 + 0.12 * (broad - broad.mean()) / (broad.std() + 1e-6) * 0.5)[..., None]
tile_p = 'art/map/ocean_normals.png'
if os.path.exists(tile_p):
    src = Image.open(tile_p).convert('RGB')
    def waves(t, ang, off):
        a = np.asarray(src.resize((t, t), Image.LANCZOS)).astype(np.float32) / 255
        c, s_ = np.cos(np.radians(ang)), np.sin(np.radians(ang))
        u = ((XX * c - YY * s_ + off) % t).astype(int); v = ((XX * s_ + YY * c + off) % t).astype(int)
        n = a[v, u]
        return (n[..., 1] - 0.5) - (n[..., 0] - 0.5)            # light from the top left
    w = waves(S // 9, 0, 0) * 0.6 + waves(int(S / 9 * 1.41), 23, 157) * 0.4
    w = w / (np.abs(w).mean() + 1e-6)
    sea *= (1 + 0.055 * w[..., None])                              # fine waves: visible up close, calm from afar
    glint = (w > np.percentile(w, 99.85)) & (dist > 6)
    sea[glint] = sea[glint] * 0.6 + 0.4 * np.array([0.75, 0.82, 0.85])
shadow = ndi.gaussian_filter(np.roll(np.roll(land.astype(np.float32), 4, 0), 3, 1), 2.5) * (~land)
sea *= (1 - 0.28 * shadow[..., None])
rim = ndi.binary_dilation(land, iterations=2) & ~land
sea[rim] = sea[rim] * 0.75 + 0.25 * np.array([0.7, 0.78, 0.8])   # thin light rim where water meets land

img = np.where(land[..., None], ground, sea)
riv = river & land
riv = ndi.binary_erosion(riv) | (riv & (ndi.distance_transform_edt(riv) >= 1) & (ndi.gaussian_filter(riv.astype(float), 1) > 0.7))
img[riv] = np.array([0.17, 0.28, 0.35])

# ---------- nations, provinces and relation borders ----------
def ids(path):
    a = np.asarray(Image.open(path).convert('RGB')).astype(np.int32)
    return a[..., 0] + a[..., 1] * 256 - 1
POL = os.environ.get('POLITICAL', 'art/map')
nation = ids(os.path.join(POL, 'nations.png')); province = ids(os.path.join(POL, 'provinces.png'))
ME = int(os.environ.get('ME', '4'))
REL = {int(k): v for k, v in (x.split(':') for x in os.environ.get('RELATIONS', '0:ally,1:passage,2:enemy,3:neutral').split(','))}
TINT = {'me': (1.06, 1.06, 1.0), 'ally': (0.92, 1.0, 0.92), 'passage': (0.86, 0.9, 0.86), 'neutral': (0.78, 0.82, 0.8), 'enemy': (0.95, 0.66, 0.6)}
rel_of = lambda k: 'me' if k == ME else REL.get(k, 'neutral')
MIX = {'enemy': ((0.36, 0.03, 0.03), 0.78), 'neutral': ((0.10, 0.14, 0.12), 0.45), 'passage': ((0.04, 0.20, 0.07), 0.45), 'ally': ((0.45, 0.70, 0.40), 0.30)}
# allies: no national border at all, only the normal province outline

# cities baked into the ground: dense city clipped exactly to its province, a few villages nearby
import json
pol = json.load(open(os.path.join(POL, 'political.json')))
ct = 'art/citytex/city_dense.png'; vt = 'art/citytex/village.png'
SATCITY = [] if os.environ.get('NO_CITIES') else [f for f in ('art/sat/city1.jpg', 'art/sat/city2.jpg') if os.path.exists(f)]
SATTOWN = [f for f in ('art/sat/town1.jpg', 'art/sat/town2.jpg') if os.path.exists(f)]
img_base = img.copy()
def city_patch(path, frac, off=(0.5, 0.5)):
    a = np.asarray(Image.open(path).convert('RGB')).astype(np.float32) / 255
    h, w = a.shape[:2]; c = int(min(h, w) * frac / 2)
    cy, cx = int(h * off[0]), int(w * off[1])
    a = a[max(cy - c, 0):cy + c, max(cx - c, 0):cx + c]
    valid = a.mean(-1) > 0.02
    if valid.mean() < 0.95: return None                  # skip crops that touch empty satellite edges
    g = a.mean(-1, keepdims=True)
    a = g + (a - g) * 0.55                               # real colours, calmer
    a = a / a.mean() * 0.36                              # same brightness as the land
    return np.clip(a, 0, 1)
if SATCITY:
    edge_noise = ndi.gaussian_filter(rng.random((S // 8, S // 8)), 1.2)
    edge_noise = ndi.zoom(edge_noise, 8, order=1)[:S, :S]
    edge_noise = (edge_noise - edge_noise.mean()) / (edge_noise.std() + 1e-6)
    offs = [(0.5, 0.5), (0.45, 0.55), (0.55, 0.45), (0.5, 0.6), (0.6, 0.5), (0.4, 0.5)]
    cities_t = [t for f in SATCITY for o in offs for t in [city_patch(f, 0.35, o)] if t is not None]
    towns_t = [t for f in SATTOWN for o in offs for t in [city_patch(f, 0.12, o)] if t is not None] or cities_t
    def paste_real(tex, cx, cy, radius, mask_fn, strength=1.0):
        r = int(radius * 1.35)
        y0, y1, x0, x1 = max(cy - r, 0), min(cy + r, S), max(cx - r, 0), min(cx + r, S)
        if y1 <= y0 or x1 <= x0: return
        t = np.rot90(tex, rng.integers(0, 4))
        t = np.asarray(Image.fromarray((t * 255).astype(np.uint8)).resize((2 * r, 2 * r), Image.LANCZOS)).astype(np.float32) / 255
        t = t[(y0 - (cy - r)):(y1 - (cy - r)), (x0 - (cx - r)):(x1 - (cx - r))]
        yy, xx = np.mgrid[y0:y1, x0:x1]
        d = np.hypot(yy - cy, xx - cx) / radius + edge_noise[y0:y1, x0:x1] * 0.25
        fade = np.clip((1.05 - d) * 2.5, 0, 1) * mask_fn(y0, y1, x0, x1) * strength
        sub = img[y0:y1, x0:x1]
        sub[:] = sub * (1 - fade[..., None]) + t * fade[..., None]
    for p in pol['provinces']:
        if p['city'] == 'rural': continue
        cx, cy = int(p['centre'][0]), int(p['centre'][1])
        R = {'capital': 95, 'major': 70, 'minor': 48}[p['city']] * S / 2048
        own = province == p['id']
        paste_real(cities_t[p['id'] % len(cities_t)], cx, cy, R, lambda y0, y1, x0, x1: own[y0:y1, x0:x1].astype(np.float32))
        for k in range({'capital': 5, 'major': 3, 'minor': 2}[p['city']]):
            ang = rng.uniform(0, 2 * np.pi); dd = R * rng.uniform(1.3, 2.4)
            vx, vy = int(cx + np.cos(ang) * dd), int(cy + np.sin(ang) * dd)
            if 0 <= vx < S and 0 <= vy < S and land[vy, vx]:
                paste_real(towns_t[k % len(towns_t)], vx, vy, R * rng.uniform(0.22, 0.35), lambda y0, y1, x0, x1: land[y0:y1, x0:x1].astype(np.float32), 0.9)
elif os.path.exists(ct) and not os.environ.get('NO_CITIES'):
    city = np.asarray(Image.open(ct).convert('RGBA')).astype(np.float32) / 255
    vil = np.asarray(Image.open(vt).convert('RGBA')).astype(np.float32) / 255 if os.path.exists(vt) else None
    edge_noise = ndi.gaussian_filter(rng.random((S // 8, S // 8)), 1.2)
    edge_noise = ndi.zoom(edge_noise, 8, order=1)[:S, :S]
    edge_noise = (edge_noise - edge_noise.mean()) / (edge_noise.std() + 1e-6)
    def prep(tex):
        # buildings only: drop the flat ground the renderer saw, keep roofs, walls and shadows as light/dark
        g = tex[..., :3].mean(-1)
        ground = np.median(g)
        dev = g - ground
        build = np.clip(np.abs(dev) * 6, 0, 1)
        return dev, build
    def paste(tex, cx, cy, radius, mask_fn, strength=1.0):
        r = int(radius * 1.3)
        y0, y1, x0, x1 = max(cy - r, 0), min(cy + r, S), max(cx - r, 0), min(cx + r, S)
        if y1 <= y0 or x1 <= x0: return
        ang = rng.integers(0, 4)
        t = np.rot90(tex, ang)
        t = np.asarray(Image.fromarray((t * 255).astype(np.uint8)).resize((2 * r, 2 * r), Image.LANCZOS)).astype(np.float32) / 255
        t = t[(y0 - (cy - r)):(y1 - (cy - r)), (x0 - (cx - r)):(x1 - (cx - r))]
        dev, build = prep(t)
        yy, xx = np.mgrid[y0:y1, x0:x1]
        d = np.hypot(yy - cy, xx - cx) / radius + edge_noise[y0:y1, x0:x1] * 0.22
        fade = np.clip((1.0 - d) * 3, 0, 1) * mask_fn(y0, y1, x0, x1) * strength
        sub = img[y0:y1, x0:x1]
        sub *= (1 - 0.22 * fade)[..., None]                                   # built-up ground is darker than fields
        lit = 1 + dev * 2.2 * fade                                            # roofs lighter, shadows darker
        sub *= lit[..., None]
        grey = sub.mean(-1, keepdims=True)
        k = (build * fade * 0.35)[..., None]
        sub[:] = sub * (1 - k) + (grey * 1.05) * k                           # buildings a touch greyer, still in the land's colour
    for p in pol['provinces']:
        if p['city'] == 'rural': continue
        cx, cy = int(p['centre'][0]), int(p['centre'][1])
        R = {'capital': 95, 'major': 70, 'minor': 48}[p['city']] * S / 2048
        own = province == p['id']
        paste(city, cx, cy, R, lambda y0, y1, x0, x1: own[y0:y1, x0:x1].astype(np.float32))      # ends exactly at the border
        if vil is not None:                                                                       # a few villages spill into neighbours
            for k in range({'capital': 5, 'major': 3, 'minor': 2}[p['city']]):
                ang = rng.uniform(0, 2 * np.pi); dd = R * rng.uniform(1.3, 2.4)
                vx, vy = int(cx + np.cos(ang) * dd), int(cy + np.sin(ang) * dd)
                if 0 <= vx < S and 0 <= vy < S and land[vy, vx]:
                    paste(vil, vx, vy, R * rng.uniform(0.25, 0.4), lambda y0, y1, x0, x1: land[y0:y1, x0:x1].astype(np.float32), 0.9)
# nation tint goes over the cities too, so a city takes its owner's colour like in CoN
LAYERS = os.environ.get('LAYERS')   # live game: raw land + a separate border overlay, tint and cities drawn by the game
if LAYERS:
    Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8)).save(os.path.join(LAYERS, 'land.jpg'), quality=92)
for k in ([] if LAYERS else np.unique(nation[nation >= 0])):
    m = nation == k; r = rel_of(int(k))
    if r == 'me': continue
    col, a = MIX[r]
    g = img[m].mean(-1, keepdims=True)
    img[m] = (img[m] * 0.5 + g * 0.5) * (1 - a) + np.array(col) * a + (img[m] - g) * 0.15
def edges(a):
    e = np.zeros_like(a, bool)
    e[1:] |= a[1:] != a[:-1]; e[:, 1:] |= a[:, 1:] != a[:, :-1]
    return e & land & ndi.binary_erosion(land, iterations=1)
pe = edges(province)
img[pe] = img[pe] * 0.62 + 0.38 * np.array([0.95, 0.97, 0.95])   # thin province outline
ne = edges(nation)
def pair_rel(mask):
    """relation of the border: the foreign side's relation to me (borders between two foreign nations: neutral)."""
    out = np.full(mask.shape, 'neutral', object)
    ys, xs = np.where(mask)
    for y, x in zip(ys, xs):
        a = nation[y, x]; b = nation[max(y - 1, 0), x] if nation[max(y - 1, 0), x] != a else nation[y, max(x - 1, 0)]
        if ME in (a, b): out[y, x] = rel_of(int(b if a == ME else a))
    return out
rel = pair_rel(ne)
for kind in ('neutral', 'passage', 'enemy'):
    m = ne & (rel == kind)
    if kind == 'neutral':
        m = ndi.binary_dilation(m) & land
        img[m] = img[m] * 0.15 + 0.85 * np.array([0.97, 0.98, 0.96])          # standard: solid white
    elif kind == 'passage':
        m = ndi.binary_dilation(m) & land & (((XX + YY) // 9) % 2 == 0)
        img[m] = img[m] * 0.2 + 0.8 * np.array([0.97, 0.98, 0.96])            # right of passage: dashed white
    else:
        glow = ndi.gaussian_filter(ndi.binary_dilation(m, iterations=2).astype(float), 4) * land
        img *= (1 - 0.25 * glow[..., None]) + 0 * glow[..., None]
        img[..., 0] += 0.25 * glow
        m2 = ndi.binary_dilation(m, iterations=1) & land
        img[m2] = img[m2] * 0.1 + 0.9 * np.array([0.85, 0.18, 0.15])          # enemy: red line with a glow
if LAYERS:
    # province outlines only (thin white); nation borders are drawn live since relations change in game
    ov = np.zeros((S, S, 4), np.uint8)
    ov[pe] = (242, 247, 242, 110)
    Image.fromarray(ov).save(os.path.join(LAYERS, 'outlines.png'))
    print('saved layers'); raise SystemExit
out = Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8)).convert('RGBA')
out.convert('RGB').save(OUT, quality=90)
print('saved', OUT)
