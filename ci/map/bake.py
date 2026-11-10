# Bakes a CoN-quality painted map for an invented region, fully procedural (free, no assets).
# Output: art/map/terrain.png (base texture), art/map/provinces.png (ID map), art/map/preview.png
import numpy as np, os, sys
from PIL import Image
from scipy import ndimage as ndi

S = int(os.environ.get('MAP_SIZE', '2048'))
SEED = int(os.environ.get('MAP_SEED', '11'))
OUT = sys.argv[1] if len(sys.argv) > 1 else 'art/map'
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(SEED)

def value_noise(cells, size=S):
    g = rng.random((cells + 3, cells + 3))
    z = ndi.zoom(g, (size + 3 * size / cells) / (cells + 3), order=3)
    return z[:size, :size]

def fbm(base=4, octaves=7, gain=0.5):
    out = np.zeros((S, S)); amp = 1; tot = 0; c = base
    for _ in range(octaves):
        out += amp * value_noise(c); tot += amp; amp *= gain; c *= 2
        if c > S // 2: break
    return out / tot

def norm(a):
    return (a - a.min()) / (a.max() - a.min() + 1e-9)

def warp(a, strength=40):
    dx = (fbm(3, 5) - 0.5) * strength * 2; dy = (fbm(3, 5) - 0.5) * strength * 2
    yy, xx = np.mgrid[0:S, 0:S]
    return ndi.map_coordinates(a, [np.clip(yy + dy, 0, S - 1), np.clip(xx + dx, 0, S - 1)], order=1)

print('land')
yy, xx = np.mgrid[0:S, 0:S] / S
cont = warp(norm(fbm(3, 8)), 60)
# a big landmass west/centre, sea to the east and a gulf in the south
shape = 1.0 - 1.25 * np.clip((xx - 0.55) * 1.6, 0, 1) ** 1.4 - 0.9 * np.exp(-(((xx - 0.45) / 0.12) ** 2 + ((yy - 0.95) / 0.18) ** 2))
land_f = cont * 0.55 + shape * 0.6
land = land_f > 0.62
land = ndi.binary_opening(land, iterations=2)
lab, n = ndi.label(land)
sizes = ndi.sum(land, lab, range(1, n + 1))
keep = np.isin(lab, 1 + np.where(sizes > S * S * 0.0008)[0])
land = keep

print('height')
ridge = 1 - np.abs(fbm(5, 7) * 2 - 1)
ridge = ridge ** 3
mount_zone = np.clip((norm(fbm(2, 4)) - 0.55) * 4, 0, 1)
dist_coast = ndi.distance_transform_edt(land)
height = (np.clip(dist_coast / (S * 0.08), 0, 1) * 0.35 + ridge * mount_zone * 0.9 + fbm(8, 6) * 0.12) * land
height = ndi.gaussian_filter(height, 1.2)

def hillshade(h, az=315, alt=40, z=18.0):
    gy, gx = np.gradient(h * z * S / 1024)
    slope = np.pi / 2 - np.arctan(np.hypot(gx, gy))
    aspect = np.arctan2(-gx, gy)
    a, b = np.radians(az), np.radians(alt)
    return np.clip(np.sin(b) * np.sin(slope) + np.cos(b) * np.cos(slope) * np.cos(a - aspect), 0, 1)

shade = hillshade(height)

print('forest canopy')
# canopy: dense little tree crowns, clumped by a forest-density field
density = norm(warp(fbm(6, 6), 30))
forest = np.clip((density - 0.42) * 3.2, 0, 1) * land * (1 - np.clip((height - 0.55) * 4, 0, 1))
# round tree crowns: scatter seeds (denser in thick forest), each seed grows a little dome
r = max(2.2, S / 420)
bush = np.clip(norm(fbm(20, 4)) - 0.55, 0, 1) * land * 0.5           # scattered copses in open country
seeds = (rng.random((S, S)) < (forest + bush) * 0.09 / (r * r) * 3.0)
d = ndi.distance_transform_edt(~seeds)
crown = np.clip(1 - d / (r * 1.6), 0, 1) ** 0.7
canopy_h = np.maximum(forest * (0.25 + crown), crown * (bush > 0) * 0.8)
canopy_shade = hillshade(canopy_h, z=40)

print('farmland')
# patchwork of fields: rotated grid with random tints, only on low, flat, non-forest land
ang = np.radians(23)
u = (xx * np.cos(ang) - yy * np.sin(ang)) * S / 34
v = (xx * np.sin(ang) + yy * np.cos(ang)) * S / 22
uw = u + (fbm(6, 3) - 0.5) * 1.2; vw = v + (fbm(6, 3) - 0.5) * 1.2
cell = (np.floor(uw).astype(np.int64) * 73856093 ^ np.floor(vw).astype(np.int64) * 19349663) & 0xFFFF
tint = (cell % 997) / 997.0
edge = (np.abs(uw - np.round(uw)) < 0.05) | (np.abs(vw - np.round(vw)) < 0.05)
farm_zone = np.clip((norm(fbm(4, 5)) - 0.5) * 4, 0, 1) * land * (1 - forest) * (height < 0.45)

print('rivers')
river = np.zeros((S, S), bool)
for k in range(12):
    # walk downhill-ish from a high point towards the coast with wandering
    hi = np.argwhere((height > 0.5) & land)
    if len(hi) == 0: break
    y, x = hi[rng.integers(len(hi))].astype(float)
    pts = []
    heading = rng.uniform(0, 2 * np.pi)
    for step in range(4000):
        pts.append((y, x))
        iy, ix = int(y), int(x)
        if not land[iy, ix]: break
        gy, gx = np.gradient(height[max(iy - 3, 0):iy + 4, max(ix - 3, 0):ix + 4])
        g = np.array([gy.mean(), gx.mean()])
        target = np.arctan2(-g[0], -g[1]) if np.hypot(*g) > 1e-5 else heading
        heading += 0.15 * np.angle(np.exp(1j * (target - heading))) + rng.normal(0, 0.12)
        y += 2.0 * np.sin(heading); x += 2.0 * np.cos(heading)
        if not (5 < y < S - 5 and 5 < x < S - 5): break
    iy, ix = int(pts[-1][0]), int(pts[-1][1])
    if land[iy, ix] or len(pts) < 60: continue                            # never reached the sea: drop it
    for i, (py, px) in enumerate(pts):
        w = 2 + 5 * i / max(len(pts), 1)
        y0, y1 = int(max(py - w, 0)), int(min(py + w + 1, S)); x0, x1 = int(max(px - w, 0)), int(min(px + w + 1, S))
        sy, sx = np.mgrid[y0:y1, x0:x1]
        river[y0:y1, x0:x1] |= (sy - py) ** 2 + (sx - px) ** 2 <= w * w
river &= land
water = ~land | river

print('colour')
img = np.zeros((S, S, 3))
# land base: meadow green, varied
meadow = np.array([0.40, 0.62, 0.27]); dry = np.array([0.55, 0.60, 0.33]); rock = np.array([0.40, 0.50, 0.34])
var = norm(fbm(12, 5))[..., None]
grain = (value_noise(S // 3) - 0.5)[..., None] * 0.10
base = (meadow * (1 - var * 0.35) + dry * (var * 0.35)) * (1 + grain)
alt_rock = np.clip((height - 0.7) * 2, 0, 0.6)[..., None]
base = base * (1 - alt_rock) + rock * alt_rock
# fields
field_cols = np.array([[0.42, 0.60, 0.26], [0.55, 0.62, 0.30], [0.30, 0.48, 0.20], [0.62, 0.60, 0.36], [0.35, 0.54, 0.30]])
fc = field_cols[(tint * len(field_cols)).astype(int) % len(field_cols)]
fc = np.where(edge[..., None], fc * 0.75, fc)
fz = farm_zone[..., None]
base = base * (1 - fz * 0.85) + fc * fz * 0.85
# forest canopy: dark green crowns with lit tops
fcol = np.array([0.13, 0.30, 0.10]) * (0.7 + 0.6 * canopy_shade[..., None])
ff = np.clip(np.maximum(forest * 1.4, crown * (bush > 0) * 0.9), 0, 1)[..., None]
base = base * (1 - ff) + fcol * ff
# terrain light
base *= (0.62 + 0.5 * shade[..., None])
# water
dist_land = ndi.distance_transform_edt(~land)
shallow = np.clip(1 - dist_land / (S * 0.035), 0, 1)[..., None]
deep = np.array([0.10, 0.22, 0.33]); shal = np.array([0.20, 0.40, 0.48])
waves = fbm(S // 24, 3, 0.6)
waves = ndi.gaussian_filter(waves, (0.6, 2.2))                         # stretched ripples
wcol = deep * (1 - shallow) + shal * shallow
wcol = wcol * (0.82 + 0.4 * (waves[..., None] - 0.5) + 0.12)
rcol = np.array([0.20, 0.36, 0.44]) * (0.85 + 0.35 * (waves[..., None] - 0.5))
img = np.where(land[..., None], base, wcol)
img = np.where(river[..., None], rcol, img)
# coast: thin dark rim on land and a soft drop shadow on the water, the "raised land" look
rim = (ndi.binary_dilation(water, iterations=2) & land & ~river)
img[rim] *= 0.7
shadow = ndi.gaussian_filter(np.roll(np.roll(land.astype(float), 6, 0), 5, 1), 4) * (~land)
img *= (1 - 0.35 * shadow[..., None])
img = np.clip(img, 0, 1)
Image.fromarray((img * 255).astype(np.uint8)).save(os.path.join(OUT, 'terrain.png'), optimize=True)

print('provinces')
# provinces: relaxed Voronoi on land, wiggly borders
n_prov = int(os.environ.get('PROVINCES', '60'))
pts = np.argwhere(land)[rng.choice(land.sum(), n_prov, replace=False)].astype(float)
small = 256; sc = S / small
ys, xs = np.mgrid[0:small, 0:small] * sc
land_s = land[::int(sc), ::int(sc)][:small, :small]
for it in range(6):
    d = (ys[..., None] - pts[:, 0]) ** 2 + (xs[..., None] - pts[:, 1]) ** 2
    lab = d.argmin(-1)
    for k in range(n_prov):
        m = (lab == k) & land_s
        if m.any(): pts[k] = [ys[m].mean(), xs[m].mean()]
wy = (fbm(14, 4) - 0.5) * 26; wx = (fbm(14, 4) - 0.5) * 26
YY, XX = np.mgrid[0:S, 0:S]
best = np.full((S, S), np.inf); pid = np.zeros((S, S), np.int32)
for k, (py, px) in enumerate(pts):
    d = (YY + wy - py) ** 2 + (XX + wx - px) ** 2
    m = d < best; best[m] = d[m]; pid[m] = k + 1
pid[~land] = 0
idimg = np.stack([pid % 256, pid // 256, np.zeros_like(pid)], -1).astype(np.uint8)
Image.fromarray(idimg).save(os.path.join(OUT, 'provinces.png'))
np.save(os.path.join(OUT, 'centres.npy'), pts)

print('preview')
# preview with borders and one highlighted nation, as the game will draw them
nation = np.zeros(n_prov + 1, int)
order = np.argsort(pts[:, 1])                                           # split into 4 nations west to east
for i, k in enumerate(order): nation[k + 1] = 1 + (i * 4) // n_prov
nat = nation[pid]
prev = img.copy()
others = (nat > 0) & (nat != 2)
prev[others] = prev[others] * np.array([0.55, 0.62, 0.58])             # foreign land darker, CoN-style
pb = (pid != np.roll(pid, 1, 0)) | (pid != np.roll(pid, 1, 1))
nb = (nat != np.roll(nat, 1, 0)) | (nat != np.roll(nat, 1, 1))
pb &= land; nb &= land & ndi.binary_erosion(land, iterations=3)
pb &= ndi.binary_erosion(land, iterations=2)
prev[ndi.binary_dilation(pb)] = prev[ndi.binary_dilation(pb)] * 0.4 + 0.6 * np.array([0.92, 0.95, 0.92])
prev[ndi.binary_dilation(nb, iterations=2)] = np.array([0.97, 0.98, 0.96])
Image.fromarray((np.clip(prev, 0, 1) * 255).astype(np.uint8)).save(os.path.join(OUT, 'preview.png'), optimize=True)
print('done', n_prov, 'provinces')
