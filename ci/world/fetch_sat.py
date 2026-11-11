# Downloads NASA Blue Marble (public domain) from NASA GIBS as a 16384 x 8192 equirectangular mosaic.
# GIBS is NASA's open imagery service; tiles are requested with plain WMS GetMap calls.
#   python3 ci/world/fetch_sat.py data/world.sat.jpg
import sys, io, time, urllib.request
from PIL import Image

OUT = sys.argv[1]
TILE, NX, NY = 2048, 8, 4
LAYERS = ['BlueMarble_NextGeneration', 'BlueMarble_ShadedRelief']
BASE = 'https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi'

def get(layer, lat0, lon0, lat1, lon1):
    url = (f'{BASE}?SERVICE=WMS&REQUEST=GetMap&VERSION=1.3.0&LAYERS={layer}&STYLES=&CRS=EPSG:4326'
           f'&BBOX={lat0},{lon0},{lat1},{lon1}&WIDTH={TILE}&HEIGHT={TILE}&FORMAT=image/jpeg')
    for i in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'vigil-map-build'}), timeout=120) as r:
                data = r.read()
            return Image.open(io.BytesIO(data)).convert('RGB')
        except Exception as e:
            print('retry', layer, lat0, lon0, e); time.sleep(5 * (i + 1))
    return None

for layer in LAYERS:
    mosaic = Image.new('RGB', (TILE * NX, TILE * NY)); ok = True
    for j in range(NY):
        for i in range(NX):
            lon0 = -180 + i * 45; lat1 = 90 - j * 45
            t = get(layer, lat1 - 45, lon0, lat1, lon0 + 45)
            if t is None: ok = False; break
            mosaic.paste(t, (i * TILE, j * TILE))
        if not ok: break
        print('row', j, 'done', flush=True)
    if ok:
        mosaic.save(OUT, quality=92); print('saved', layer, mosaic.size); break
