# City miniatures for the world map: each city stands on the map as a small model of itself instead of a symbol.
# Capitals carry a regional landmark (great mosque, cathedral, capitol, tower), big cities a skyline, towns a few
# roofs. Same sun and materials as the buildings and blocks, shadows on a transparent catcher, so they sit on
# the land. The game colours them with the land's own relation colours.
# Run: blender -b -P ci/render/citymarks.py -- <outdir>        env: REGIONS=gulf SIZE=384
import bpy, math, sys, os, random
OUT = sys.argv[sys.argv.index('--') + 1] if '--' in sys.argv else 'art/citymarks'
os.makedirs(OUT, exist_ok=True)
os.environ.setdefault('SIZE', '384'); os.environ.setdefault('SAMPLES', '64')
import importlib.util
spec = importlib.util.spec_from_file_location('bld', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'buildings.py'))
src = open(spec.origin).read().split('\nonly = set(')[0]
G = {'__name__': 'bld', '__file__': spec.origin}
exec(compile(src, spec.origin, 'exec'), G)
reset, mat, box, cyl, sphere_cap, gable, Kit, REGIONS = G['reset'], G['mat'], G['box'], G['cyl'], G['sphere_cap'], G['gable'], G['Kit'], G['REGIONS']
FRAME = 150.0
ELEV = 52                      # a model on a table: you see roofs and facades

def cone(x, y, z, r, h, m, verts=16):
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r, radius2=0.0, depth=h, location=(x, y, z + h / 2))
    o = bpy.context.object; o.data.materials.append(m); return o

def tower(k, x, y, w, d, h, m, crown=True):
    box(x, y, 0, w, d, h, m, bevel=0.15)
    if crown: box(x, y, h, w * 0.7, d * 0.7, 1.6, k.metal if hasattr(k, 'metal') else m, bevel=0.1)

def mosque(k, x, y, s=1.0):
    wall = mat((0.86, 0.84, 0.78), 0.6); dome = mat((0.80, 0.78, 0.70), 0.35)
    box(x, y, 0, 26 * s, 26 * s, 9 * s, wall, bevel=0.2)
    cyl(x, y, 9 * s, 8.5 * s, 4 * s, wall, verts=32)                      # drum
    sphere_cap(x, y, 13 * s, 9 * s, dome)                                 # the great dome
    cone(x, y, 21.5 * s, 0.6 * s, 3.5 * s, dome, 8)                        # finial
    for dx, dy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):                   # four minarets
        mx, my = x + dx * 15 * s, y + dy * 15 * s
        cyl(mx, my, 0, 1.4 * s, 30 * s, wall, verts=12)
        cyl(mx, my, 22 * s, 2.0 * s, 1.0 * s, wall, verts=12)             # balcony
        cone(mx, my, 30 * s, 1.4 * s, 4.5 * s, dome, 12)

def cathedral(k, x, y, s=1.0):
    st = mat((0.72, 0.69, 0.63), 0.7); roof = mat((0.36, 0.40, 0.42), 0.5)
    box(x, y, 0, 12 * s, 40 * s, 14 * s, st, bevel=0.2); gable(x, y, 14 * s, 12 * s, 40 * s, 7 * s, roof, overhang=0.3)
    box(x, y + 4 * s, 0, 30 * s, 10 * s, 12 * s, st, bevel=0.2); gable(x, y + 4 * s, 12 * s, 30 * s, 10 * s, 6 * s, roof, rot=90, overhang=0.3)
    box(x, y - 22 * s, 0, 10 * s, 10 * s, 30 * s, st, bevel=0.2)          # bell tower
    cone(x, y - 22 * s, 30 * s, 6.5 * s, 18 * s, roof, 8)                  # spire

def capitol(k, x, y, s=1.0):
    w = mat((0.88, 0.87, 0.84), 0.55)
    box(x, y, 0, 44 * s, 16 * s, 10 * s, w, bevel=0.2)
    for i in range(10): cyl(x - 18 * s + i * 4 * s, y - 9 * s, 0, 0.8 * s, 9 * s, w, verts=10)   # colonnade
    cyl(x, y, 10 * s, 8 * s, 8 * s, w, verts=32); sphere_cap(x, y, 18 * s, 8 * s, w); cone(x, y, 25.5 * s, 1.2 * s, 5 * s, w, 10)

def pagoda(k, x, y, s=1.0):
    w = mat((0.62, 0.60, 0.56), 0.6); roof = mat((0.22, 0.34, 0.40), 0.5)
    for i in range(6):
        r = (9 - i * 1.2) * s; z = i * 7 * s
        box(x, y, z, r * 1.2, r * 1.2, 5 * s, w, bevel=0.1)
        bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=r * 1.25, radius2=r * 0.55, depth=2.2 * s, location=(x, y, z + 6 * s), rotation=(0, 0, math.radians(45)))
        bpy.context.object.data.materials.append(roof)
    cone(x, y, 42 * s, 0.8 * s, 9 * s, roof, 8)

LANDMARK = {'gulf': mosque, 'europe': cathedral, 'americas': capitol, 'asia': pagoda}

def skyline(k, R, rnd, n, hmax, spread, avoid=0):
    glass = mat((0.42, 0.50, 0.56), 0.25, metal=0.3)
    for i in range(n):
        for _ in range(30):
            a = rnd.random() * 6.283; d = avoid + rnd.random() ** 0.7 * spread
            x, y = math.cos(a) * d, math.sin(a) * d * 0.9
            if abs(x) < 70 and abs(y) < 70: break
        f = 1 - d / (avoid + spread + 1)
        h = 6 + hmax * f * rnd.uniform(0.5, 1.0)
        w = rnd.uniform(7, 12); dd = rnd.uniform(7, 12)
        m = glass if h > 30 and rnd.random() < 0.6 else (k.white if rnd.random() < 0.5 else mat(R['wall'], 0.7))
        box(x, y, 0, w, dd, h, m, bevel=0.15)
        if h > 18: box(x, y, h, w * 0.6, dd * 0.6, 1.4, k.white, bevel=0.1)

def houses(k, R, rnd, n, spread, avoid=0):
    roof = mat(R['roof'], 0.7)
    for i in range(n):
        a = rnd.random() * 6.283; d = avoid + rnd.random() * spread
        x, y = math.cos(a) * d, math.sin(a) * d * 0.9
        w, dd = rnd.uniform(6, 10), rnd.uniform(6, 9); h = rnd.uniform(3, 7)
        rot = rnd.choice((0, 90)) + rnd.uniform(-8, 8)
        box(x, y, 0, w, dd, h, mat(R['wall'], 0.75), bevel=0.12, rot=rot)
        if R['roof_kind'] == 'gable': gable(x, y, h, w, dd, 2.6, roof, rot=rot, overhang=0.3)
    for i in range(n // 2):
        a = rnd.random() * 6.283; d = avoid + rnd.random() * spread * 1.1
        k.plant(math.cos(a) * d, math.sin(a) * d * 0.9)

def mark(reg, kind):
    s = reset(); G['MATS'].clear()
    R = REGIONS[reg]; k = Kit(R); rnd = random.Random(hash((reg, kind)) & 0xffff)
    if kind == 'capital':
        LANDMARK[reg](k, 0, 0, 1.0)
        skyline(k, R, rnd, 14, 46 if reg != 'europe' else 22, 34, avoid=30)
        houses(k, R, rnd, 16, 14, avoid=52)
    elif kind == 'major':
        skyline(k, R, rnd, 12, 34 if reg != 'europe' else 16, 30, avoid=0)
        houses(k, R, rnd, 14, 14, avoid=34)
    else:
        houses(k, R, rnd, 13, 26, avoid=0)
    cd = bpy.data.cameras.new('cam'); cd.type = 'ORTHO'; cd.ortho_scale = FRAME
    cam = bpy.data.objects.new('cam', cd); s.collection.objects.link(cam); s.camera = cam
    e = math.radians(ELEV); cam.location = (0, -math.cos(e) * 300, math.sin(e) * 300 + 12); cam.rotation_euler = (math.radians(90 - ELEV), 0, 0)
    s.render.filepath = os.path.abspath(os.path.join(OUT, f'mark_{reg}_{kind}.png'))
    bpy.ops.render.render(write_still=True)
    print('rendered mark', reg, kind, flush=True)

regs = list(filter(None, os.environ.get('REGIONS', '').split(','))) or list(REGIONS)
for reg in regs:
    for kind in ('capital', 'major', 'minor'):
        mark(reg, kind)
