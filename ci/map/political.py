# Divides the land into nations and provinces. Bigger nations get more provinces and more cities
# (5 to 9), every province has a minimum size, borders wiggle naturally.
# Output: art/map/nations.png, art/map/provinces.png (ids in R+G), art/map/political.json
import json, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
from scipy.spatial import cKDTree
MASKS, OUT = sys.argv[1], sys.argv[2]
N_NATIONS = int(os.environ.get('NATIONS', '5'))
PROV_PER_CITY = float(os.environ.get('PROV_PER_CITY', '2.2'))
rng = np.random.default_rng(int(os.environ.get('SEED', '4')))
land = np.load(MASKS)['land']
S = land.shape[0]

def smooth_noise(cells, amp):
    g = rng.random((cells + 3, cells + 3))
    return (ndi.zoom(g, S / cells, order=3)[:S, :S] - 0.5) * amp
YY, XX = np.mgrid[0:S, 0:S].astype(np.float32)
# warp the coordinates so every border wiggles like a real one
WY = YY + smooth_noise(10, 120) + smooth_noise(40, 30)
WX = XX + smooth_noise(10, 120) + smooth_noise(40, 30)
L = np.argwhere(land)

def farthest_points(mask_idx, k, weights=None):
    pts = [mask_idx[rng.integers(len(mask_idx))]]
    d = np.full(len(mask_idx), np.inf)
    for _ in range(k - 1):
        d = np.minimum(d, ((mask_idx - pts[-1]) ** 2).sum(1))
        pts.append(mask_idx[np.argmax(d * (rng.random(len(d)) * 0.4 + 0.8))])
    return np.array(pts, float)

def assign(mask, seeds, power=None):
    idx = np.argwhere(mask)
    q = np.stack([WY[mask], WX[mask]], 1)
    if power is None:
        _, lab = cKDTree(seeds).query(q)
    else:
        d = ((q[:, None, :] - seeds[None]) ** 2).sum(-1) - power[None]
        lab = d.argmin(1)
    out = np.full((S, S), -1, np.int32); out[idx[:, 0], idx[:, 1]] = lab
    return out

def relax(mask, seeds, it=4):
    for _ in range(it):
        lab = assign(mask, seeds)
        for k in range(len(seeds)):
            m = lab == k
            if m.any(): seeds[k] = [YY[m].mean(), XX[m].mean()]
    return seeds

# nations: different sizes on purpose (power diagram weights)
small = land[::4, ::4]; sidx = np.argwhere(small) * 4
nat_seeds = farthest_points(sidx, N_NATIONS)
weights = rng.uniform(0, (S * 0.18) ** 2, N_NATIONS)
nation = assign(land, nat_seeds, weights)
# keep only the largest connected piece of each nation; islands go to the nearest neighbour
for k in range(N_NATIONS):
    lab, n = ndi.label(nation == k)
    if n > 1:
        sizes = ndi.sum(np.ones_like(lab), lab, range(1, n + 1)); keep = 1 + np.argmax(sizes)
        nation[(lab > 0) & (lab != keep)] = -2
fill = nation == -2
if fill.any():
    good = nation >= 0
    _, (iy, ix) = ndi.distance_transform_edt(~good, return_indices=True)
    nation[fill] = nation[iy[fill], ix[fill]]

areas = np.array([(nation == k).sum() for k in range(N_NATIONS)])
order = np.argsort(areas)
cities_n = {int(k): int(round(5 + 4 * r / max(N_NATIONS - 1, 1))) for r, k in enumerate(order)}   # 5..9 by size
province = np.full((S, S), -1, np.int32)
info = {'nations': [], 'provinces': [], 'size': S}
pid = 0
for k in range(N_NATIONS):
    m = nation == k
    n_prov = max(cities_n[k] + 3, int(round(cities_n[k] * PROV_PER_CITY)))
    idx = np.argwhere(m[::4, ::4]) * 4
    seeds = relax(m, farthest_points(idx, n_prov), 4)
    lab = assign(m, seeds)
    sizes = np.array([(lab == j).sum() for j in range(n_prov)])
    # cities: the provinces nearest the nation's centre and spread out; the biggest-centre one is the capital
    centre = seeds.mean(0)
    score = -((seeds - centre) ** 2).sum(1) ** 0.5 * 0.4 + sizes ** 0.5
    chosen = []
    for j in np.argsort(-score):
        if all(((seeds[j] - seeds[c]) ** 2).sum() ** 0.5 > S * 0.06 for c in chosen): chosen.append(int(j))
        if len(chosen) == cities_n[k]: break
    for j in range(n_prov):
        province[lab == j] = pid
        kind = 'capital' if chosen and j == chosen[0] else ('major' if j in chosen[1:3] else ('minor' if j in chosen else 'rural'))
        info['provinces'].append({'id': pid, 'nation': k, 'centre': [float(seeds[j][1]), float(seeds[j][0])], 'city': kind, 'area': int(sizes[j])})
        pid += 1
    info['nations'].append({'id': k, 'area': int(areas[k]), 'cities': cities_n[k], 'provinces': n_prov})
    print('nation', k, 'area', areas[k], 'cities', cities_n[k], 'provinces', n_prov)

def save_ids(a, path):
    a = np.where(a < 0, 0, a + 1)
    Image.fromarray(np.stack([a % 256, a // 256, np.zeros_like(a)], -1).astype(np.uint8)).save(path)
save_ids(nation, os.path.join(OUT, 'nations.png'))
save_ids(province, os.path.join(OUT, 'provinces.png'))
json.dump(info, open(os.path.join(OUT, 'political.json'), 'w'))
print('provinces', pid)
