# Map ground textures, drawn the way Conflict of Nations paints its land: a top-down illustration lit by one
# sun from the north-west, in light and dark only (the game colours it per owner), seamless in both directions.
#   python3 ci/world/textures.py app/world/tex
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

# forest is rendered in Blender (ci/render/forest.py): real 3D crowns
yy, xx = np.mgrid[0:N, 0:N]

# ---------- open land: smooth grass, faint field patches and grain ----------
fields = wrap_noise(22, 5, 3) * 0.055 + wrap_noise(5, 6, 2) * 0.022 + wrap_noise(0.7, 7, 1) * 0.025
openl = 0.62 + fields
save('open.png', openl)

# ---------- arid: sand ripples, a few dark bushes ----------
warp = wrap_noise(25, 8, 2) * 6
rip = np.sin((xx * 0.7 + yy * 0.35 + warp) * 2 * np.pi / 14) * 0.5 + 0.5
dune = wrap_noise(30, 9, 3)
hs = dune * 6 + rip * 0.8
arid = 0.6 + (shade(hs, 0.8) - 0.6) * 0.32 + wrap_noise(20, 13, 2) * 0.04 + wrap_noise(0.8, 10, 1) * 0.02
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
rock = 0.56 + (shade(ndi.gaussian_filter(rk, 1.2, mode='wrap'), 1.4) - 0.6) * 0.34
save('rock.png', rock)
