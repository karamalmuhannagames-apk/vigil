# Real hills and mountains: downloads open elevation tiles (Terrain Tiles on AWS Open Data: SRTM, GMTED, ETOPO
# and others, mostly public domain) and computes our own hill shading from them, lit from the north-west
# to match the shadows on the map. One consistent source, so no joins or bands.
#   python3 ci/world/fetch_dem.py data/world.relief.jpg
import sys, io, math, time, urllib.request
import numpy as np
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
from scipy import ndimage as ndi

OUT = sys.argv[1]
Z = 5; N = 2 ** Z; T = 256
URL = 'https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png'

def get(xy):
    x, y = xy
    for i in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(URL.format(z=Z, x=x, y=y), headers={'User-Agent': 'vigil-map-build'}), timeout=60) as r:
                a = np.asarray(Image.open(io.BytesIO(r.read())).convert('RGB')).astype(np.float32)
            return x, y, a[..., 0] * 256 + a[..., 1] + a[..., 2] / 256 - 32768
        except Exception as e:
            time.sleep(2 * (i + 1)); err = e
    raise SystemExit(f'tile {x},{y} failed: {err}')

dem = np.zeros((N * T, N * T), np.float32)
with ThreadPoolExecutor(16) as ex:
    for k, (x, y, e) in enumerate(ex.map(get, [(x, y) for y in range(N) for x in range(N)])):
        dem[y * T:(y + 1) * T, x * T:(x + 1) * T] = e
        if k % 128 == 0: print('tiles', k, flush=True)
dem = np.clip(dem, 0, None)                                   # sea floor ignored: only land relief is shaded
S = N * T
# metres per pixel shrinks towards the poles in this projection
yy = (np.arange(S) + 0.5) / S
lat = np.arctan(np.sinh(np.pi * (1 - 2 * yy)))
mpp = (40075016.0 / S * np.cos(lat))[:, None]
dem = ndi.gaussian_filter(dem, 0.8)
gy, gx = np.gradient(dem)
slope = (gx + gy) / (math.sqrt(2) * mpp)                      # facing north-west = lit
hs = 0.5 + 0.5 * np.tanh(slope * 16)
hs8 = (hs * 255).astype(np.uint8)
# to the plain latitude/longitude grid the map builder samples from
H2 = 8192
la = np.radians(90 - (np.arange(H2) + 0.5) / H2 * 180)
la = np.clip(la, -1.484, 1.484)
rows = np.clip(((1 - np.arcsinh(np.tan(la)) / np.pi) / 2 * S).astype(int), 0, S - 1)
img = Image.fromarray(hs8[rows]).resize((16384, H2), Image.BILINEAR)
img.save(OUT, quality=92)
print('saved relief', img.size, 'mid', float(np.median(hs8)) / 255)
