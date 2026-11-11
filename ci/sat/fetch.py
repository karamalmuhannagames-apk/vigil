# Downloads real satellite photo patches (Copernicus Sentinel-2, free for commercial use with credit)
# from the public AWS open-data catalogue, one patch per terrain type, true colour, 10 m per pixel.
import json, os, sys, urllib.request
import numpy as np, rasterio
from rasterio.windows import from_bounds
from rasterio.warp import transform_bounds
from PIL import Image
OUT = sys.argv[1] if len(sys.argv) > 1 else 'art/sat'
os.makedirs(OUT, exist_ok=True)
STAC = 'https://earth-search.aws.element84.com/v1/search'
# (name, lon, lat): typical places for each terrain, summer, no clouds
SPOTS = [
    ('farmland', 1.9, 49.6), ('farmland2', 10.5, 52.3), ('forest', 26.5, 61.5), ('forest2', 11.0, 48.0),
    ('mountain', 7.9, 46.3), ('mountain2', 44.5, 42.7), ('dry', 36.0, 31.5), ('desert', 46.5, 24.5),
    ('grass', -1.5, 53.3), ('coast', 21.0, 56.0),
]
SIZE_KM = 20
def search(lon, lat):
    body = {'collections': ['sentinel-2-l2a'], 'intersects': {'type': 'Point', 'coordinates': [lon, lat]},
            'datetime': '2023-06-01T00:00:00Z/2023-08-31T23:59:59Z', 'limit': 10,
            'query': {'eo:cloud_cover': {'lt': 3}}, 'sortby': [{'field': 'properties.eo:cloud_cover', 'direction': 'asc'}]}
    req = urllib.request.Request(STAC, data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'})
    return json.load(urllib.request.urlopen(req, timeout=60))['features']
credits = []
for name, lon, lat in SPOTS:
    try:
        feats = search(lon, lat)
        if not feats: print('no scene', name); continue
        f = feats[0]
        href = f['assets']['visual']['href']
        d = SIZE_KM / 111 / 2
        with rasterio.open(href) as src:
            b = transform_bounds('EPSG:4326', src.crs, lon - d / np.cos(np.radians(lat)), lat - d, lon + d / np.cos(np.radians(lat)), lat + d)
            arr = src.read(window=from_bounds(*b, transform=src.transform), boundless=True, fill_value=0)
        img = np.moveaxis(arr[:3], 0, -1)
        Image.fromarray(img).save(os.path.join(OUT, name + '.jpg'), quality=90)
        credits.append({'patch': name, 'scene': f['id'], 'date': f['properties']['datetime']})
        print('got', name, img.shape, f['id'])
    except Exception as e:
        print('failed', name, e)
json.dump({'licence': 'Contains modified Copernicus Sentinel data 2023', 'patches': credits},
          open(os.path.join(OUT, 'CREDITS.json'), 'w'), indent=1)
