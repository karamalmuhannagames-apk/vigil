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

def perlin(c, size=S):
    ang = rng.random((c + 2, c + 2)) * 2 * np.pi
    gxg, gyg = np.cos(ang), np.sin(ang)
    t = np.linspace(0, c, size, endpoint=False)
    xi = t.astype(int); xf = t - xi
    X0, Y0 = np.meshgrid(xi, xi); FX, FY = np.meshgrid(xf, xf)
    def dot(ox, oy):
        return gxg[Y0 + oy, X0 + ox] * (FX - ox) + gyg[Y0 + oy, X0 + ox] * (FY - oy)
    f = lambda v: v * v * v * (v * (v * 6 - 15) + 10)
    u, v = f(FX), f(FY)
    a = dot(0, 0) + u * (dot(1, 0) - dot(0, 0))
    b = dot(0, 1) + u * (dot(1, 1) - dot(0, 1))
    return a + v * (b - a)          # roughly -0.7..0.7

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
def ridged(base, octaves=10):
    out = np.zeros((S, S)); amp = 1; tot = 0; c = base; weight = np.ones((S, S))
    for _ in range(octaves):
        n = 1 - np.abs(perlin(c) * 1.4); n = np.clip(n, 0, 1) ** 2 * weight
        out += n * amp; tot += amp; weight = np.clip(n * 1.6, 0, 1); amp *= 0.55; c *= 2
        if c > S // 3: break
    return out / tot
mount_zone = np.clip((norm(fbm(2, 4)) - 0.45) * 3.0, 0, 1)
mount = norm(warp(ridged(4), 28))
hills = ridged(14, 6)
dist_coast = ndi.distance_transform_edt(land)
height = (np.clip(dist_coast / (S * 0.06), 0, 1) * 0.22 + mount ** 1.5 * mount_zone * 1.3 + hills * 0.10) * land

def hillshade(h, az=315, alt=38, z=34.0):
    gy, gx = np.gradient(h * z * S / 1024)
    slope = np.pi / 2 - np.arctan(np.hypot(gx, gy))
    aspect = np.arctan2(-gx, gy)
    a, b = np.radians(az), np.radians(alt)
    return np.clip(np.sin(b) * np.sin(slope) + np.cos(b) * np.cos(slope) * np.cos(a - aspect), 0, 1)


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

print('rivers: water flow')
import heapq
M = 512; f = S // M
hs = height[::f, ::f][:M, :M].copy(); ls = land[::f, ::f][:M, :M]
# priority-flood: fill pits so every drop of rain finds the sea
filled = np.where(ls, np.inf, 0.0); done = ~ls.copy()
heap = []
coast_cells = ls & ndi.binary_dilation(~ls)
for y, x in np.argwhere(coast_cells):
    filled[y, x] = hs[y, x]; done[y, x] = True; heapq.heappush(heap, (hs[y, x], y, x))
nb = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
while heap:
    h, y, x = heapq.heappop(heap)
    for dy, dx in nb:
        yy2, xx2 = y + dy, x + dx
        if 0 <= yy2 < M and 0 <= xx2 < M and not done[yy2, xx2]:
            done[yy2, xx2] = True
            filled[yy2, xx2] = max(hs[yy2, xx2], h + 1e-6)
            heapq.heappush(heap, (filled[yy2, xx2], yy2, xx2))
filled[~ls] = 0
# each cell drains to its lowest neighbour; accumulate rain from high to low
recv = np.full((M, M, 2), -1)
low = filled.copy()
for dy, dx in nb:
    sh = np.full((M, M), np.inf)
    src = filled[max(dy, 0):M + min(dy, 0), max(dx, 0):M + min(dx, 0)]
    sh[max(-dy, 0):M + min(-dy, 0), max(-dx, 0):M + min(-dx, 0)] = src
    better = sh < low
    low = np.where(better, sh, low)
    recv[better] = (np.argwhere(better) + [dy, dx])
acc = np.ones((M, M)) * ls
order = np.argsort(-filled, axis=None)
for idx in order:
    y, x = divmod(idx, M)
    if not ls[y, x]: continue
    ry, rx = recv[y, x]
    if ry >= 0: acc[ry, rx] += acc[y, x]
# carve valleys into the terrain so the relief shows the drainage
carve = ndi.gaussian_filter(ndi.zoom(np.log1p(acc), f, order=1)[:S, :S], f * 1.2)
height = np.clip(height - carve * 0.012 * land, 0, None)
thr = M * M * float(os.environ.get('RIVER_THR', '0.012'))
rv = (acc > thr) & ls
width = ndi.zoom(np.where(rv, np.sqrt(acc / thr), 0), f, order=0)[:S, :S]
rv_big = ndi.zoom(rv.astype(np.uint8), f, order=0)[:S, :S].astype(bool)
rv_big = ndi.binary_closing(rv_big, iterations=2)
# smooth the river ribbon: blur the mask and re-threshold, width grows downstream
soft = ndi.gaussian_filter(rv_big.astype(float) * (0.55 + 0.45 * np.clip(width, 1, 3)), f * 1.6)
river = soft > 0.3
river &= land
bank = ndi.binary_dilation(river, iterations=max(1, S // 1024)) & land & ~river
water = ~land | river

shade = hillshade(height)
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
# --- export layers for the 3D map render (Blender): unshaded colours, height, forest, rivers
if os.environ.get('EXPORT_LAYERS'):
    dsea = ndi.distance_transform_edt(~land)
    depth = np.clip(dsea / (S * 0.05), 0, 1)
    sand = np.array([0.55, 0.62, 0.52]); dark = np.array([0.05, 0.12, 0.18])
    sea_alb = sand * (1 - depth[..., None]) ** 2 + dark * (1 - (1 - depth[..., None]) ** 2)
    alb = np.where(land[..., None], base, sea_alb)
    alb = np.where(river[..., None], np.array([0.12, 0.17, 0.2]), alb)
    Image.fromarray((np.clip(alb, 0, 1) * 255).astype(np.uint8)).save(os.path.join(OUT, 'albedo.png'))
    hn = height / max(height.max(), 1e-6)
    hh = np.where(land, 0.03 + hn * 0.97 - river * 0.02, -0.02 - depth * 0.3)
    hh16 = ((hh + 0.35) / 1.4 * 65535).clip(0, 65535).astype(np.uint16)  # stored as 0..1 = -0.35..1.05
    Image.fromarray(hh16).save(os.path.join(OUT, 'height16.png'))
    Image.fromarray((np.clip(forest * 1.3, 0, 1) * 255).astype(np.uint8)).save(os.path.join(OUT, 'forest.png'))
    Image.fromarray((np.clip(bush * 2, 0, 1) * 255).astype(np.uint8)).save(os.path.join(OUT, 'bush.png'))
# forest canopy: dark green crowns with lit tops
fcol = np.array([0.13, 0.30, 0.10]) * (0.7 + 0.6 * canopy_shade[..., None])
ff = np.clip(np.maximum(forest * 1.4, crown * (bush > 0) * 0.9), 0, 1)[..., None]
base = base * (1 - ff) + fcol * ff
# terrain light
base *= (0.62 + 0.5 * shade[..., None])
# water
dist_land = ndi.distance_transform_edt(~land)
YY2, XX2 = np.mgrid[0:S, 0:S].astype(np.float32)
rip = np.zeros((S, S), np.float32)
main = np.radians(25)
for k in range(16):
    ang = main + rng.normal(0, 0.6); per = rng.uniform(7, 28)
    ph = ((fbm(6, 4) - 0.5) * 14).astype(np.float32)
    rip += np.sin((np.cos(ang) * XX2 + np.sin(ang) * YY2) * (2 * np.pi / per) + ph) * rng.uniform(0.5, 1.0)
rip += ((value_noise(S // 9) - 0.5) * 1.5).astype(np.float32)
rip *= (0.6 + 0.8 * fbm(5, 4)).astype(np.float32)                     # calmer and rougher patches
gy, gx = np.gradient(rip)
nz = 1.0 / np.sqrt(gx * gx * 0.08 + gy * gy * 0.08 + 1)
glint = np.clip((-gx * 0.22 - gy * 0.22) * nz + nz * 0.1, 0, 1) ** 5 * (fbm(10, 4) > 0.4)   # sun from top-left, patchy
band_w = S * (0.012 + 0.03 * fbm(5, 5))
band = np.clip(1 - (dist_land - band_w) / (S * 0.006), 0, 1)        # shallow coastal water, width varies
deep = np.array([0.11, 0.24, 0.36]); shal = np.array([0.22, 0.42, 0.50])
depth_dark = np.clip(dist_land / (S * 0.25), 0, 1)[..., None] * 0.18
wcol = deep * (1 - band[..., None]) + shal * band[..., None]
lam = np.clip(0.5 + (-gx - gy) * 0.35, 0, 1)[..., None]               # each ripple lit on one side
wcol = wcol * (1 - depth_dark) * (0.78 + 0.38 * lam) + glint[..., None] * np.array([0.45, 0.5, 0.52])
rcol = np.array([0.17, 0.25, 0.30]) * (0.9 + 0.08 * rip[..., None] / 3) + glint[..., None] * np.array([0.7, 0.75, 0.78])
img = np.where(land[..., None], base, wcol)
img = np.where(river[..., None], rcol, img)
img[bank] = img[bank] * 0.3 + 0.7 * np.array([0.80, 0.84, 0.82])
# coast: thin dark rim on land and a soft drop shadow on the water, the "raised land" look
rim = (ndi.binary_dilation(water, iterations=2) & land & ~river)
img[rim] *= 0.7
shadow = ndi.gaussian_filter(np.roll(np.roll(land.astype(float), 6, 0), 5, 1), 4) * (~land)
img *= (1 - 0.35 * shadow[..., None])
blur = ndi.gaussian_filter(img, (1.2, 1.2, 0))
img = np.where(land[..., None] & ~river[..., None], img + (img - blur) * 0.6, img)
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
