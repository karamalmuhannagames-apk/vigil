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

# sea: plain deep blue, lighter shallow band, faint waves
dist = ndi.distance_transform_edt(~land)
band = np.clip(1 - (dist - S * 0.02) / (S * 0.015), 0, 1)[..., None]
deep = np.array([0.15, 0.27, 0.36]); shallow = np.array([0.22, 0.35, 0.42])
sea = deep * (1 - band) + shallow * band
tile_p = 'art/map/ocean_normals.png'
if os.path.exists(tile_p):
    n = np.asarray(Image.open(tile_p).convert('RGB').resize((S // 6, S // 6), Image.LANCZOS)).astype(np.float32) / 255
    n = np.tile(n, (7, 7, 1))[:S, :S]
    lit = (n[..., 1] - n[..., 0]) * 0.5
    sea = sea * (1 + lit[..., None] * 0.8)
shadow = ndi.gaussian_filter(np.roll(np.roll(land.astype(np.float32), 5, 0), 4, 1), 3) * (~land)
sea *= (1 - 0.3 * shadow[..., None])

img = np.where(land[..., None], ground, sea)
riv = river & land
img[riv] = np.array([0.17, 0.27, 0.34])
img[ndi.binary_dilation(riv) & ~riv & land] *= 0.8
# provinces and nations, thin white lines
pid_img = np.asarray(Image.open('art/map/provinces.png').convert('RGB')).astype(np.int32)
pid = pid_img[..., 0] + pid_img[..., 1] * 256
pb = ((pid != np.roll(pid, 1, 0)) | (pid != np.roll(pid, 1, 1))) & ndi.binary_erosion(land, iterations=2)
img[pb] = img[pb] * 0.45 + 0.55 * np.array([0.95, 0.97, 0.95])
img = np.clip(img, 0, 1)
Image.fromarray((img * 255).astype(np.uint8)).save(OUT, quality=90)
print('saved', OUT)
