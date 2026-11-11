# Blender script: dense city fabric seen from above, one set per regional style, for close zoom.
# Far away the game shows the satellite city; close up it blends into these sharper blocks
# rendered with the same camera, sun and materials as the buildings, so everything matches.
# Run: blender -b -P ci/render/cityblocks.py -- <outdir>       env: REGIONS=gulf VARIANTS=4 SIZE=1024
import bpy, math, sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
OUT = sys.argv[sys.argv.index('--') + 1] if '--' in sys.argv else 'art/cityblocks'
os.makedirs(OUT, exist_ok=True)
os.environ.setdefault('SIZE', '1024')
import importlib.util
spec = importlib.util.spec_from_file_location('bld', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'buildings.py'))
# reuse scene, materials and shapes from the buildings script without running its render loop
src = open(spec.origin).read().split('\nonly = set(')[0]
G = {'__name__': 'bld', '__file__': spec.origin}
exec(compile(src, spec.origin, 'exec'), G)
reset, mat, box, cyl, gable, Kit, REGIONS = G['reset'], G['mat'], G['box'], G['cyl'], G['gable'], G['Kit'], G['REGIONS']
FRAME = 360.0

STYLE = {
    # street spacing (m), lot depth, floors near centre / edge, chance of a park, flat-roof clutter
    'gulf':     dict(block=(46, 70), lot=(12, 18), floors=(4, 1), park=0.06, villas=True),
    'europe':   dict(block=(40, 64), lot=(9, 14), floors=(6, 2), park=0.08, villas=False),
    'asia':     dict(block=(36, 56), lot=(10, 16), floors=(12, 3), park=0.05, villas=False),
    'americas': dict(block=(60, 90), lot=(16, 26), floors=(8, 1), park=0.07, villas=False),
}

def city(reg, seed):
    s = reset(); G['MATS'].clear()
    for o in list(bpy.data.objects):
        if o.name == 'catcher': bpy.data.objects.remove(o)
    rnd = random.Random(seed)
    R = REGIONS[reg]; st = STYLE[reg]; k = Kit(R)
    gcol = {'gulf': (0.46, 0.40, 0.32), 'europe': (0.33, 0.33, 0.30), 'asia': (0.34, 0.34, 0.32), 'americas': (0.36, 0.36, 0.33)}[reg]
    ground = mat(gcol, rough=1, noise=0.08, scale=0.03)
    road = mat((0.19, 0.19, 0.19), rough=0.9, noise=0.06, scale=0.4)
    walls = [mat(tuple(min(1, c * f) for c in base), noise=0.08) for base in (R['wall'], R['wall2']) for f in (0.88, 1.0, 1.1)]
    box(0, 0, -0.1, FRAME * 1.2, FRAME * 1.2, 0.1, ground, bevel=0)
    rot = rnd.uniform(-25, 25)
    import mathutils
    rm = mathutils.Matrix.Rotation(math.radians(rot), 3, 'Z')
    # street grid with irregular spacing
    xs = [-FRAME * 0.56]
    while xs[-1] < FRAME * 0.56: xs.append(xs[-1] + rnd.uniform(*st['block']))
    ys = [-FRAME * 0.56]
    while ys[-1] < FRAME * 0.56: ys.append(ys[-1] + rnd.uniform(*st['block']))
    def place(x, y): v = rm @ mathutils.Vector((x, y, 0)); return v.x, v.y
    for x in xs:
        cx, cy = place(x, 0); box(cx, cy, 0.004, 7, FRAME * 1.6, 0.02, road, bevel=0, rot=rot)   # offset height: no flicker where streets cross
    for y in ys:
        cx, cy = place(0, y); box(cx, cy, 0, FRAME * 1.6, 7, 0.02, road, bevel=0, rot=rot)
    for x in xs:
        for t in range(-24, 25, 3):
            if rnd.random() < 0.45:
                tx, ty = place(x + 4.8, t * 7.5); k.plant(tx, ty)
    # a diagonal avenue cuts across like real cities
    ang = rnd.uniform(30, 60) * rnd.choice((1, -1))
    box(0, 0, 0.01, 14, FRAME * 1.8, 0.02, road, bevel=0, rot=rot + ang)
    av = (math.cos(math.radians(rot + ang + 90)), math.sin(math.radians(rot + ang + 90)))
    for i in range(len(xs) - 1):
        for j in range(len(ys) - 1):
            bx0, bx1, by0, by1 = xs[i] + 4.5, xs[i + 1] - 4.5, ys[j] + 4.5, ys[j + 1] - 4.5
            if bx1 - bx0 < 8 or by1 - by0 < 8: continue
            mx, my = place((bx0 + bx1) / 2, (by0 + by1) / 2)
            if abs(mx * av[0] + my * av[1]) < 10: continue                       # leave the avenue clear
            dc = math.hypot(mx, my) / (FRAME * 0.7)                              # 0 centre .. 1 edge
            if rnd.random() < st['park']:
                cx, cy = place((bx0 + bx1) / 2, (by0 + by1) / 2)
                box(cx, cy, 0, bx1 - bx0, by1 - by0, 0.05, k.green, bevel=0, rot=rot)
                for _ in range(6): k.plant(cx + rnd.uniform(-8, 8), cy + rnd.uniform(-8, 8))
                continue
            # lots around the block edge (perimeter blocks), inner courtyards stay open
            d = rnd.uniform(*st['lot'])
            x = bx0
            while x < bx1 - 4:
                w = min(rnd.uniform(*st['lot']), bx1 - x)
                for yy, side in ((by0 + d / 2, 0), (by1 - d / 2, 1)):
                    floors = max(1, round(st['floors'][0] * (1 - dc) + st['floors'][1] * dc + rnd.uniform(-1, 1.5)))
                    cx, cy = place(x + w / 2, yy)
                    wall = rnd.choice(walls)
                    if st['villas'] and dc > 0.45:
                        k.house(cx, cy, w * 0.7, d * 0.7, 1 + (rnd.random() < 0.4), rot=rot, wall=wall)
                    else:
                        k.house(cx, cy, w * 0.94, d * 0.92, floors, rot=rot, wall=wall)
                        if rnd.random() < 0.3:                                   # L-shaped wing into the courtyard
                            ix, iy = place(x + w / 2, yy + (d * 0.7 if side == 0 else -d * 0.7))
                            k.house(ix, iy, w * 0.45, d * 0.6, max(1, floors - 1), rot=rot, wall=wall)
                        # rooftop clutter: tanks, units, stair huts
                        h = floors * 3.2 + 0.25
                        for _ in range(rnd.randint(1, 3)):
                            ox, oy = rnd.uniform(-w * 0.3, w * 0.3), rnd.uniform(-d * 0.3, d * 0.3)
                            rx, ry = place(x + w / 2 + ox, yy + oy)
                            box(rx, ry, h, rnd.uniform(0.8, 2.2), rnd.uniform(0.8, 1.8), rnd.uniform(0.6, 1.6), k.metal if rnd.random() < 0.6 else k.white, rot=rot)
                x += w + rnd.uniform(0.3, 1.5)
            if by1 - by0 > 2 * d + 8 and rnd.random() < 0.5:                       # something in the courtyard
                cx, cy = place((bx0 + bx1) / 2, (by0 + by1) / 2)
                if rnd.random() < 0.5: k.plant(cx, cy)
                else: box(cx, cy, 0, (bx1 - bx0) * 0.5, (by1 - by0 - 2 * d) * 0.6, 0.04, road, bevel=0, rot=rot)   # parking
    cd = bpy.data.cameras.new('cam'); cd.type = 'ORTHO'; cd.ortho_scale = FRAME
    cam = bpy.data.objects.new('cam', cd); s.collection.objects.link(cam); s.camera = cam
    e = math.radians(G['ELEV']); cam.location = (0, -math.cos(e) * 300, math.sin(e) * 300); cam.rotation_euler = (math.radians(90 - G['ELEV']), 0, 0)
    s.render.film_transparent = False
    s.render.filepath = os.path.abspath(os.path.join(OUT, f'block_{reg}_{seed}.png'))
    bpy.ops.render.render(write_still=True)
    print('rendered block', reg, seed, flush=True)

regs = list(filter(None, os.environ.get('REGIONS', '').split(','))) or list(REGIONS)
for reg in regs:
    for v in range(int(os.environ.get('VARIANTS', '4'))):
        city(reg, v + 1)
