# City miniatures for the world map: each city stands on the map as a small model of itself instead of a symbol.
# Capitals carry a regional landmark (great mosque, cathedral, capitol, tower), big cities a skyline, towns a few
# roofs. Same sun and materials as the buildings and blocks, shadows on a transparent catcher, so they sit on
# the land. The game colours them with the land's own relation colours.
# Run: blender -b -P ci/render/citymarks.py -- <outdir>        env: REGIONS=gulf SIZE=384
import bpy, math, sys, os, random
OUT = sys.argv[sys.argv.index('--') + 1] if '--' in sys.argv else 'art/citymarks'
os.makedirs(OUT, exist_ok=True)
os.environ.setdefault('SIZE', '512'); os.environ.setdefault('SAMPLES', '64')
import importlib.util
spec = importlib.util.spec_from_file_location('bld', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'buildings.py'))
src = open(spec.origin).read().split('\nonly = set(')[0]
G = {'__name__': 'bld', '__file__': spec.origin}
exec(compile(src, spec.origin, 'exec'), G)
reset, mat, box, cyl, sphere_cap, gable, Kit, REGIONS = G['reset'], G['mat'], G['box'], G['cyl'], G['sphere_cap'], G['gable'], G['Kit'], G['REGIONS']
FRAME = 118.0
ELEV = 42                      # a model on a table: you see roofs and facades


FAC = {}
def facade(color, glass=(0.07, 0.09, 0.11), floor=3.2, bay=2.6, roofc=None):
    """walls with rows of windows (a grid in metres, so every building has real floors), plain roofs"""
    key = (tuple(round(c, 3) for c in color), floor, bay, roofc)
    if key in FAC: return FAC[key]
    m = bpy.data.materials.new('fac%d' % len(FAC)); m.use_nodes = True
    nt = m.node_tree; N = nt.nodes; L = nt.links; p = N['Principled BSDF']
    p.inputs['Roughness'].default_value = 0.7
    tc = N.new('ShaderNodeTexCoord'); sep = N.new('ShaderNodeSeparateXYZ'); L.new(tc.outputs['Object'], sep.inputs[0])
    add_ = N.new('ShaderNodeMath'); add_.operation = 'ADD'; L.new(sep.outputs[0], add_.inputs[0]); L.new(sep.outputs[1], add_.inputs[1])
    comb = N.new('ShaderNodeCombineXYZ'); L.new(add_.outputs[0], comb.inputs[0]); L.new(sep.outputs[2], comb.inputs[1])
    br = N.new('ShaderNodeTexBrick'); br.offset = 0.0; br.squash = 1.0
    br.inputs['Scale'].default_value = 1.0; br.inputs['Brick Width'].default_value = bay; br.inputs['Row Height'].default_value = floor
    br.inputs['Mortar Size'].default_value = 0.55; br.inputs['Mortar Smooth'].default_value = 0.0
    br.inputs['Color1'].default_value = (*glass, 1); br.inputs['Color2'].default_value = (*[g * 1.3 for g in glass], 1)
    br.inputs['Mortar'].default_value = (*color, 1)
    L.new(comb.outputs[0], br.inputs['Vector'])
    geo = N.new('ShaderNodeNewGeometry'); sz = N.new('ShaderNodeSeparateXYZ'); L.new(geo.outputs['Normal'], sz.inputs[0])
    gt = N.new('ShaderNodeMath'); gt.operation = 'GREATER_THAN'; gt.inputs[1].default_value = 0.5; L.new(sz.outputs[2], gt.inputs[0])
    mix = N.new('ShaderNodeMixRGB'); L.new(gt.outputs[0], mix.inputs['Fac'])
    L.new(br.outputs['Color'], mix.inputs['Color1']); mix.inputs['Color2'].default_value = (*(roofc or [c * 0.92 for c in color]), 1)
    L.new(mix.outputs['Color'], p.inputs['Base Color'])
    FAC[key] = m
    return m

def plaza(r, color=(0.74, 0.71, 0.64)):
    m = mat(color, 0.9, noise=0.1, scale=3)
    cyl(0, 0, 0, r, 0.25, m, verts=48)

def cone(x, y, z, r, h, m, verts=16):
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r, radius2=0.0, depth=h, location=(x, y, z + h / 2))
    o = bpy.context.object; o.data.materials.append(m); return o

def tower(k, x, y, w, d, h, m, crown=True):
    box(x, y, 0, w, d, h, m, bevel=0.15)
    if crown: box(x, y, h, w * 0.7, d * 0.7, 1.6, k.metal if hasattr(k, 'metal') else m, bevel=0.1)

def mosque(k, x, y, s=1.0):
    wall = facade((0.88, 0.86, 0.80), glass=(0.20, 0.30, 0.30), floor=5, bay=3.2); dome = mat((0.84, 0.82, 0.74), 0.35)
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
    st = facade((0.72, 0.69, 0.63), glass=(0.18, 0.16, 0.2), floor=6, bay=4); roof = mat((0.30, 0.36, 0.38), 0.5)
    box(x, y + 4 * s, 0, 13 * s, 38 * s, 15 * s, st, bevel=0.2); gable(x, y + 4 * s, 15 * s, 13 * s, 38 * s, 8 * s, roof, rot=90, overhang=0.3)   # nave
    box(x, y + 12 * s, 0, 32 * s, 11 * s, 13 * s, st, bevel=0.2); gable(x, y + 12 * s, 13 * s, 32 * s, 11 * s, 7 * s, roof, overhang=0.3)        # transept
    cyl(x, y + 12 * s, 21 * s, 5 * s, 4 * s, st, verts=16); cone(x, y + 12 * s, 25 * s, 5.5 * s, 7 * s, roof, 16)                         # crossing
    for dx in (-5, 5):                                                                                                                      # two west towers
        box(x + dx * s, y - 16 * s, 0, 8 * s, 8 * s, 30 * s, st, bevel=0.2); cone(x + dx * s, y - 16 * s, 30 * s, 5.2 * s, 14 * s, roof, 4)

def capitol(k, x, y, s=1.0):
    w = facade((0.90, 0.89, 0.86), floor=4, bay=3); wd = mat((0.90, 0.89, 0.86), 0.5)
    box(x, y, 0, 44 * s, 16 * s, 10 * s, w, bevel=0.2)
    for i in range(10): cyl(x - 18 * s + i * 4 * s, y - 9 * s, 0, 0.8 * s, 9 * s, w, verts=10)   # colonnade
    cyl(x, y, 10 * s, 8 * s, 8 * s, w, verts=32); sphere_cap(x, y, 18 * s, 8 * s, wd); cone(x, y, 25.5 * s, 1.2 * s, 5 * s, wd, 10)

def pagoda(k, x, y, s=1.0):
    w = mat((0.62, 0.60, 0.56), 0.6); roof = mat((0.22, 0.34, 0.40), 0.5)
    for i in range(6):
        r = (9 - i * 1.2) * s; z = i * 7 * s
        box(x, y, z, r * 1.2, r * 1.2, 5 * s, w, bevel=0.1)
        bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=r * 1.25, radius2=r * 0.55, depth=2.2 * s, location=(x, y, z + 6 * s), rotation=(0, 0, math.radians(45)))
        bpy.context.object.data.materials.append(roof)
    cone(x, y, 42 * s, 0.8 * s, 9 * s, roof, 8)

LANDMARK = {'gulf': mosque, 'europe': cathedral, 'americas': capitol, 'asia': pagoda}

def fabric(k, R, rnd, radius, hc, he, clear=0.0, tall_glass=True):
    """dense city on a street grid: tall in the middle, low at the edge, real floors and windows"""
    glassf = facade((0.46, 0.54, 0.60), glass=(0.16, 0.22, 0.27), floor=3.6, bay=1.8)
    walls = [facade(R['wall']), facade(R['wall2']), facade(tuple(min(1, c * 1.12) for c in R['wall']))]
    roof = mat(R['roof'], 0.7)
    lot, street = 10.0, 2.8
    n = int(radius / lot) + 1
    for i in range(-n, n + 1):
        for j in range(-n, n + 1):
            x, y = i * lot + rnd.uniform(-0.8, 0.8), j * lot + rnd.uniform(-0.8, 0.8)
            d = math.hypot(x, y) / radius
            if d > 1 or math.hypot(x, y) < clear: continue
            if d > 0.72 and rnd.random() < (d - 0.72) * 3: continue          # ragged edge
            if rnd.random() < 0.05: k.plant(x, y); continue                  # a small square with a tree
            f = (1 - d) ** 1.5
            h = he + (hc - he) * f * rnd.uniform(0.45, 1.0)
            w = lot - street - rnd.uniform(0, 2.2); dd = lot - street - rnd.uniform(0, 2.2)
            wall = rnd.choice(walls)
            if h < 9 and R['roof_kind'] == 'gable':
                box(x, y, 0, w, dd, h, wall, bevel=0.1); gable(x, y, h, w, dd, 2.6, roof, rot=rnd.choice((0, 90)), overhang=0.25)
            elif h > 22:                                                       # podium and a slimmer tower
                box(x, y, 0, w, dd, 7, wall, bevel=0.1)
                m = glassf if (tall_glass and rnd.random() < 0.7) else wall
                box(x + rnd.uniform(-0.6, 0.6), y + rnd.uniform(-0.6, 0.6), 7, w * 0.68, dd * 0.68, h - 7, m, bevel=0.12)
                box(x, y, h, w * 0.4, dd * 0.4, 1.8, k.white, bevel=0.1)
            else:
                box(x, y, 0, w, dd, h, wall, bevel=0.1)
                if R['dome'] and rnd.random() < 0.4: cyl(x - w * 0.2, y + dd * 0.2, h, 0.7, 1.1, k.white, verts=10)   # water tank
                elif h > 12: box(x, y, h, w * 0.5, dd * 0.5, 1.4, k.white, bevel=0.1)
    for _ in range(int(radius * 0.9)):                                     # trees along the edge
        a = rnd.random() * 6.283; r = radius * rnd.uniform(0.75, 1.08)
        k.plant(math.cos(a) * r, math.sin(a) * r)

def mark(reg, kind):
    s = reset(); G['MATS'].clear(); FAC.clear()
    R = REGIONS[reg]; k = Kit(R); rnd = random.Random(hash((reg, kind)) & 0xffff)
    if kind == 'capital':
        plaza(23); LANDMARK[reg](k, 0, 0, 1.2)
        fabric(k, R, rnd, 48, 40 if reg != 'europe' else 20, 5, clear=24)
    elif kind == 'major':
        fabric(k, R, rnd, 38, 34 if reg != 'europe' else 18, 4)
    else:
        fabric(k, R, rnd, 24, 8, 3, tall_glass=False)
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
