# Downloads NASA Blue Marble (public domain) from NASA GIBS as a 16384 x 8192 equirectangular mosaic.
# GIBS is NASA's open imagery service; tiles are requested with plain WMS GetMap calls.
#   python3 ci/world/fetch_sat.py data/world.sat.jpg
import sys, io, time, urllib.request
from PIL import Image

OUT = sys.argv[1]
TILE, NX, NY = 2048, 8, 4
LAYERS = sys.argv[2].split(',') if len(sys.argv) > 2 else ['BlueMarble_NextGeneration', 'BlueMarble_ShadedRelief']
BASE = 'https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi'

OV = 3.0                                   # degrees of overlap on each side, cross-faded: no visible joins
OVP = int(round(TILE * OV / 45))
SZ = TILE + 2 * OVP

def get(layer, lat0, lon0, lat1, lon1):
    url = (f'{BASE}?SERVICE=WMS&REQUEST=GetMap&VERSION=1.3.0&LAYERS={layer}&STYLES=&CRS=EPSG:4326'
           f'&BBOX={lat0},{lon0},{lat1},{lon1}&WIDTH={SZ}&HEIGHT={SZ}&FORMAT=image/jpeg')
    for i in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'vigil-map-build'}), timeout=120) as r:
                data = r.read()
            return Image.open(io.BytesIO(data)).convert('RGB')
        except Exception as e:
            print('retry', layer, lat0, lon0, e); time.sleep(5 * (i + 1))
    return None

import numpy as np
ramp = np.ones(SZ, np.float32)
ramp[:2 * OVP] = np.linspace(0, 1, 2 * OVP); ramp[-2 * OVP:] = np.linspace(1, 0, 2 * OVP)
for layer in LAYERS:
    W, H = TILE * NX, TILE * NY
    acc = np.zeros((H + 2 * OVP, W + 2 * OVP, 3), np.float32); wsum = np.zeros((H + 2 * OVP, W + 2 * OVP, 1), np.float32)
    ok = True
    for j in range(NY):
        for i in range(NX):
            lon0 = -180 + i * 45; lat1 = 90 - j * 45
            t = get(layer, max(-90, lat1 - 45 - OV), lon0 - OV, min(90, lat1 + OV), lon0 + 45 + OV)
            if t is None: ok = False; break
            a = np.asarray(t.resize((SZ, SZ)), np.float32)
            # poles: the request was clipped at +-90, so stretch rows back to place
            if lat1 + OV > 90 or lat1 - 45 - OV < -90:
                top = OVP if lat1 + OV > 90 else 0; bot = OVP if lat1 - 45 - OV < -90 else 0
                a = np.asarray(Image.fromarray(a.astype(np.uint8)).resize((SZ, SZ - top - bot)), np.float32)
                a = np.pad(a, ((top, bot), (0, 0), (0, 0)), mode='edge')
            wgt = (ramp[:, None] * ramp[None, :])[..., None]
            y, x = j * TILE, i * TILE
            acc[y:y + SZ, x:x + SZ] += a * wgt; wsum[y:y + SZ, x:x + SZ] += wgt
        if not ok: break
        print('row', j, 'done', flush=True)
    if ok:
        img = acc / np.maximum(wsum, 1e-6)
        img = img[OVP:OVP + H, OVP:OVP + W]
        # wrap the date line: the far left and right edges only had one side to blend with
        Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).save(OUT, quality=92)
        print('saved', layer, (W, H)); break
