# Map ground textures, drawn the way Conflict of Nations paints its land: a top-down illustration lit by one
# sun from the north-west, in light and dark only (the game colours it per owner), seamless in both directions.
#   python3 ci/world/textures.py app/world/tex
# forest.png : rounded tree clumps, lit tops, dark gaps. Alpha = canopy height (used to cut crisp forest edges).
# open.png   : grass and fields: smooth, quiet, a faint grain.
# arid.png   : sand and scrub: soft ripples and small dark bushes.
# rock.png   : bare mountain ground: fine cracked grain.
import sys, os, numpy as np
from PIL import Image
from scipy import ndimage as ndi

OUT = sys.argv[1] if len(sys.argv) > 1 else 'app/world/tex'
os.makedirs(OUT, exist_ok=True)
N = 512
rng = np.random.default_rng(7)
SUN = np.array([-0.55, -0.6, 0.58]); SUN /= np.linalg.norm(SUN)        # from the north-west, fairly high

def wrap_noise(scale, seed, octaves=4):
    """Seamless fractal noise: sum of wrapped blurred white noise."""
    r = np.random.default_rng(seed); out = np.zeros((N, N)); amp = 1; tot = 0
    for o in range(octaves):
        s = scale / 2 ** o
        out += amp * ndi.gaussian_filter(r.standard_normal((N, N)), max(s, 0.6), mode='wrap'); tot += amp; amp *= 0.5
    out /= out.std() + 1e-9
    return out

def shade(h, strength=1.0):
    gy, gx = np.gradient(np.pad(h, 1, mode='wrap'))
    gx, gy = gx[1:-1, 1:-1] * strength, gy[1:-1, 1:-1] * strength
    nz = 1 / np.sqrt(gx ** 2 + gy ** 2 + 1)
    return np.clip((-gx * SUN[0] - gy * SUN[1] + SUN[2]) * nz, 0, 1)

def save(name, lum, alpha=None):
    a = (np.clip(lum, 0, 1) * 255).astype(np.uint8)
    if alpha is None: Image.fromarray(a, 'L').save(os.path.join(OUT, name), optimize=True)
    else: Image.fromarray(np.dstack([a, a, a, (np.clip(alpha, 0, 1) * 255).astype(np.uint8)]), 'RGBA').save(os.path.join(OUT, name), optimize=True)
    print('saved', name, round(float(lum.mean()), 3), round(float(lum.std()), 3))

# ---------- forest: rounded crowns gathered in clumps, the clumps standing taller in the middle ----------
yy, xx = np.mgrid[0:N, 0:N]
h = np.zeros((N, N))
def crown(px, py, r, base):
    x0, y0 = int(px - r - 1), int(py - r - 1); sz = int(2 * r + 3)
    ys, xs = np.mgrid[y0:y0 + sz, x0:x0 + sz]
    d2 = ((xs - px) ** 2 + (ys - py) ** 2) / r ** 2
    dome = np.where(d2 < 1, (np.clip(1 - d2, 0, 1) ** 0.6) * r * 0.8 + base, -99)
    iy, ix = ys % N, xs % N
    h[iy, ix] = np.maximum(h[iy, ix], dome)
for _ in range(150):                                                   # clumps
    cx, cy = rng.random(2) * N; sig = rng.uniform(9, 26); n = int(sig * sig * 0.16)
    for _ in range(n):
        dx, dy = rng.normal(0, sig, 2); d = np.hypot(dx, dy) / sig
        crown(cx + dx, cy + dy, rng.uniform(4.5, 8.5) * (1.1 - 0.3 * d), 6 * max(0, 1 - d * 0.7))
for (px, py) in rng.random((1400, 2)) * N:                             # loose trees between clumps
    crown(px, py, rng.uniform(3.5, 6), 0)
h = np.maximum(h, 0)
hs = ndi.gaussian_filter(h, 1.4, mode='wrap') + wrap_noise(1.0, 3, 2) * 0.10     # soft, painted crowns + leaf grain
lit = shade(hs, 0.45) ** 1.6
ao = np.clip(1 - (ndi.gaussian_filter(h, 7, mode='wrap') - h) * 0.12, 0.18, 1) ** 1.3    # dark gaps between crowns
sh = np.zeros((N, N))
for k in range(1, 8):                                                  # crowns throw shadows to the south-east
    sh = np.maximum(sh, np.roll(np.roll(h, k, 0), k, 1) - k * 1.1 - h)
shadow = np.clip(1 - sh * 0.06, 0.5, 1)
forest = 0.08 + 0.95 * lit * ao * shadow
forest = forest * (0.95 + 0.05 * wrap_noise(40, 4, 2))
save('forest.png', forest, np.clip(h / np.percentile(h, 98), 0, 1))

# ---------- open land: smooth grass, faint field patches and grain ----------
fields = wrap_noise(60, 5, 2) * 0.018 + wrap_noise(4, 6, 2) * 0.012 + wrap_noise(0.7, 7, 1) * 0.022
openl = 0.62 + fields
save('open.png', openl)

# ---------- arid: sand ripples, a few dark bushes ----------
warp = wrap_noise(25, 8, 2) * 6
rip = np.sin((xx * 0.7 + yy * 0.35 + warp) * 2 * np.pi / 14) * 0.5 + 0.5
dune = wrap_noise(30, 9, 3)
hs = dune * 6 + rip * 0.8
arid = 0.6 + (shade(hs, 0.8) - 0.6) * 0.18 + wrap_noise(0.8, 10, 1) * 0.02
bush = np.zeros((N, N))
for (px, py) in rng.random((700, 2)) * N:
    r = rng.uniform(1.2, 2.6)
    bush[int(py) % N, int(px) % N] = r
bush = ndi.grey_dilation(bush, size=(4, 4), mode='wrap')
bush = ndi.gaussian_filter((bush > 0).astype(float), 0.8, mode='wrap')
bsh = ndi.shift(bush, (1.5, 1.5), mode='wrap', order=1)
arid = arid * (1 - 0.35 * bush) * (1 - 0.15 * np.clip(bsh - bush, 0, 1))
save('arid.png', arid)

# ---------- rock: bare mountain ground ----------
rk = wrap_noise(10, 11, 4) * 2 + np.abs(wrap_noise(3, 12, 2)) * 1.2
rock = 0.56 + (shade(ndi.gaussian_filter(rk, 1.2, mode='wrap'), 1.4) - 0.6) * 0.22
save('rock.png', rock)
