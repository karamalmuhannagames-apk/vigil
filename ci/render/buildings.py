# Blender script: city buildings, 7 types x 5 levels x 4 regional styles, rendered as map sprites.
# Every sprite of a type uses the SAME camera frame, so a level 5 building is visibly bigger than level 1.
# Shadows fall onto a transparent shadow catcher, so they land on the map like real shadows.
# Run: blender -b -P ci/render/buildings.py -- <outdir>
#   env ONLY=factory,airport  REGIONS=gulf  LEVELS=1,5  SIZE=384  SAMPLES=48
import bpy, math, sys, os, random
from mathutils import Vector

OUT = sys.argv[sys.argv.index('--') + 1] if '--' in sys.argv else 'art/buildings'
os.makedirs(OUT, exist_ok=True)
SIZE = int(os.environ.get('SIZE', '384'))
SAMPLES = int(os.environ.get('SAMPLES', '48'))
FRAME = 46.0            # metres across the sprite; one city plot
ELEV, AZIM = 76, 0      # nearly straight down like the satellite city under it, with a hint of facades; shadows to the north-west like Sentinel-2's morning sun

# ---------- regional styles: same buildings, different architecture ----------
REGIONS = {
    # Middle East and North Africa: sand stone, flat roofs with parapets, domes, white water tanks
    'gulf':    dict(wall=(0.66, 0.57, 0.43), wall2=(0.72, 0.68, 0.60), roof=(0.64, 0.58, 0.48), roof_kind='flat',
                    accent=(0.20, 0.42, 0.40), metal=(0.72, 0.72, 0.70), ground=(0.70, 0.62, 0.48), green=(0.30, 0.38, 0.18), dome=True),
    # Europe: light render, red-brown tiled pitched roofs, grey slate on industry
    'europe':  dict(wall=(0.66, 0.63, 0.57), wall2=(0.52, 0.47, 0.42), roof=(0.48, 0.20, 0.13), roof_kind='gable',
                    accent=(0.25, 0.28, 0.32), metal=(0.50, 0.53, 0.56), ground=(0.40, 0.42, 0.36), green=(0.22, 0.36, 0.16), dome=False),
    # East and South Asia: grey concrete, blue and teal metal roofs
    'asia':    dict(wall=(0.58, 0.59, 0.58), wall2=(0.66, 0.66, 0.64), roof=(0.18, 0.40, 0.55), roof_kind='shallow',
                    accent=(0.62, 0.16, 0.12), metal=(0.58, 0.62, 0.64), ground=(0.46, 0.46, 0.42), green=(0.20, 0.38, 0.18), dome=False),
    # Americas, Africa south of the Sahara, Oceania: white and grey big boxes, flat roofs full of machinery
    'americas':dict(wall=(0.62, 0.62, 0.60), wall2=(0.48, 0.48, 0.47), roof=(0.66, 0.66, 0.64), roof_kind='flat',
                    accent=(0.55, 0.36, 0.18), metal=(0.60, 0.62, 0.62), ground=(0.44, 0.44, 0.40), green=(0.24, 0.36, 0.16), dome=False),
}
MAXLEVEL = {'hospital': 3}

# ---------- scene ----------
def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    s = bpy.context.scene
    s.render.engine = 'CYCLES'; s.cycles.device = 'CPU'; s.cycles.samples = SAMPLES; s.cycles.use_denoising = True
    s.render.film_transparent = True
    s.render.resolution_x = s.render.resolution_y = SIZE
    s.render.image_settings.file_format = 'PNG'; s.render.image_settings.color_mode = 'RGBA'
    vt = [i.identifier for i in s.view_settings.bl_rna.properties['view_transform'].enum_items]
    s.view_settings.view_transform = 'AgX' if 'AgX' in vt else 'Filmic'
    s.view_settings.exposure = -1.25   # satellite roofs are mid-tones, never paper white
    for look in ('AgX - Medium High Contrast', 'AgX - Punchy', 'Medium High Contrast'):
        try: s.view_settings.look = look; break
        except Exception: pass
    w = bpy.data.worlds.new('w'); s.world = w; w.use_nodes = True
    nt = w.node_tree; bg = nt.nodes['Background']
    hdri = os.environ.get('HDRI', 'tex/sky.hdr')
    if os.path.exists(hdri):
        env = nt.nodes.new('ShaderNodeTexEnvironment'); env.image = bpy.data.images.load(os.path.abspath(hdri))
        nt.links.new(env.outputs['Color'], bg.inputs[0]); bg.inputs[1].default_value = 0.45
    else:
        bg.inputs[0].default_value = (0.58, 0.66, 0.78, 1); bg.inputs[1].default_value = 0.6
    sun = bpy.data.lights.new('sun', 'SUN'); sun.energy = 2.6; sun.angle = math.radians(4); sun.color = (1.0, 0.96, 0.9)
    so = bpy.data.objects.new('sun', sun); s.collection.objects.link(so)
    so.rotation_euler = (math.radians(42), 0, math.radians(135))      # from the north-west
    bpy.ops.mesh.primitive_plane_add(size=400, location=(0, 0, 0))
    g = bpy.context.object; g.is_shadow_catcher = True; g.name = 'catcher'
    return s

MATS = {}
def mat(color, rough=0.75, metal=0.0, noise=0.12, scale=6.0, emit=None):
    key = (tuple(round(c, 3) for c in color), rough, metal, noise, scale, emit)
    if key in MATS: return MATS[key]
    m = bpy.data.materials.new('m%d' % len(MATS)); m.use_nodes = True
    nt = m.node_tree; p = nt.nodes['Principled BSDF']
    p.inputs['Roughness'].default_value = rough; p.inputs['Metallic'].default_value = metal
    if noise:
        # weathering: stains and colour variation so nothing looks like flat plastic
        tc = nt.nodes.new('ShaderNodeTexCoord')
        tx = nt.nodes.new('ShaderNodeTexNoise'); tx.inputs['Scale'].default_value = scale; tx.inputs['Detail'].default_value = 8
        nt.links.new(tc.outputs['Object'], tx.inputs['Vector'])
        rp = nt.nodes.new('ShaderNodeValToRGB')
        rp.color_ramp.elements[0].color = (*[c * (1 - noise) for c in color], 1)
        rp.color_ramp.elements[1].color = (*[min(1, c * (1 + noise * 0.5)) for c in color], 1)
        rp.color_ramp.elements[0].position = 0.35; rp.color_ramp.elements[1].position = 0.65
        nt.links.new(tx.outputs['Fac'], rp.inputs['Fac']); nt.links.new(rp.outputs['Color'], p.inputs['Base Color'])
        bm = nt.nodes.new('ShaderNodeBump'); bm.inputs['Strength'].default_value = 0.15
        nt.links.new(tx.outputs['Fac'], bm.inputs['Height']); nt.links.new(bm.outputs['Normal'], p.inputs['Normal'])
    else:
        p.inputs['Base Color'].default_value = (*color, 1)
    if emit:
        p.inputs['Emission Color'].default_value = (*emit, 1); p.inputs['Emission Strength'].default_value = 1.5
    MATS[key] = m
    return m

def _finish(o, m, bevel):
    o.data.materials.append(m)
    if bevel:
        b = o.modifiers.new('b', 'BEVEL'); b.width = bevel; b.segments = 2; b.limit_method = 'ANGLE'
    for f in o.data.polygons: f.use_smooth = False
    return o

def box(x, y, z, sx, sy, sz, m, bevel=0.06, rot=0):
    bpy.ops.mesh.primitive_cube_add(location=(x, y, z + sz / 2), rotation=(0, 0, math.radians(rot)))
    o = bpy.context.object; o.scale = (sx / 2, sy / 2, sz / 2); bpy.ops.object.transform_apply(scale=True)
    return _finish(o, m, bevel)

def cyl(x, y, z, r, h, m, verts=24, axis='Z', rot=0):
    r_ = (0, 0, 0) if axis == 'Z' else ((0, math.pi / 2, math.radians(rot)) if axis == 'X' else (math.pi / 2, 0, math.radians(rot)))
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=h, location=(x, y, z + (h / 2 if axis == 'Z' else 0)), rotation=r_)
    return _finish(bpy.context.object, m, 0.03)

def sphere_cap(x, y, z, r, m):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=(x, y, z), segments=24, ring_count=12)
    o = bpy.context.object; o.scale.z = 0.8
    return _finish(o, m, 0)

def gable(x, y, z, sx, sy, h, m, rot=0, overhang=0.3):
    # pitched roof running along x
    import bmesh
    me = bpy.data.meshes.new('roof'); bm = bmesh.new()
    hx, hy = sx / 2 + overhang, sy / 2 + overhang
    v = [bm.verts.new(p) for p in [(-hx, -hy, 0), (hx, -hy, 0), (hx, hy, 0), (-hx, hy, 0), (-hx, 0, h), (hx, 0, h)]]
    for f in [(0, 1, 5, 4), (2, 3, 4, 5), (0, 4, 3), (1, 2, 5), (0, 3, 2, 1)]: bm.faces.new([v[i] for i in f])
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new('roof', me); bpy.context.collection.objects.link(o)
    o.location = (x, y, z); o.rotation_euler.z = math.radians(rot)
    return _finish(o, m, 0)

def prism(x0, x1, y0, y1, z, h, m):
    # right-angle tooth: vertical face at x0 (height h), slope down to x1; extruded from y0 to y1
    import bmesh
    me = bpy.data.meshes.new('tooth'); bm = bmesh.new()
    v = [bm.verts.new(p) for p in [(x0, y0, z), (x1, y0, z), (x0, y0, z + h), (x0, y1, z), (x1, y1, z), (x0, y1, z + h)]]
    for f in [(0, 1, 2), (3, 5, 4), (0, 2, 5, 3), (1, 4, 5, 2), (0, 3, 4, 1)]: bm.faces.new([v[i] for i in f])
    bm.normal_update(); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new('tooth', me); bpy.context.collection.objects.link(o)
    return _finish(o, m, 0)

def sawtooth(x, y, z, sx, sy, n, h, m, glass):
    # factory roof: teeth run across the hall, glass faces turned to the north light
    d = sy / n
    for i in range(n):
        y0 = y - sy / 2 + d * i
        import bmesh
        me = bpy.data.meshes.new('tooth'); bm = bmesh.new()
        x0, x1 = x - sx / 2, x + sx / 2
        v = [bm.verts.new(p) for p in [(x0, y0, z), (x0, y0 + d, z), (x0, y0 + d, z + h), (x1, y0, z), (x1, y0 + d, z), (x1, y0 + d, z + h)]]
        for f in [(0, 1, 2), (3, 5, 4), (0, 3, 4, 1), (1, 4, 5, 2), (0, 2, 5, 3)]: bm.faces.new([v[k] for k in f])
        bm.normal_update(); bm.to_mesh(me); bm.free()
        o = bpy.data.objects.new('tooth', me); bpy.context.collection.objects.link(o); _finish(o, m, 0)
        box(x, y0 + d - 0.04, z, sx * 0.97, 0.06, h * 0.92, glass, bevel=0)                   # skylight glass on the steep face

def windows(x, y, z, sx, sy, sz, floors, m, side_axes='xy'):
    # thin dark strips around the facade: reads as windows from above at an angle
    for f in range(floors):
        zz = z + sz * (f + 0.55) / floors
        box(x, y - sy / 2 - 0.02, zz, sx * 0.86, 0.06, sz / floors * 0.32, m, bevel=0)
        box(x, y + sy / 2 + 0.02, zz, sx * 0.86, 0.06, sz / floors * 0.32, m, bevel=0)
        box(x - sx / 2 - 0.02, y, zz, 0.06, sy * 0.86, sz / floors * 0.32, m, bevel=0)
        box(x + sx / 2 + 0.02, y, zz, 0.06, sy * 0.86, sz / floors * 0.32, m, bevel=0)

class Kit:
    """materials and common shapes in one region's style"""
    def __init__(s, R):
        s.R = R
        s.wall = mat(R['wall'], noise=0.10); s.wall2 = mat(R['wall2'], noise=0.10)
        s.roof = mat(R['roof'], rough=0.6, noise=0.14, scale=10); s.accent = mat(R['accent'], noise=0.08)
        s.metal = mat(R['metal'], rough=0.35, metal=0.7, noise=0.08, scale=20)
        s.rust = mat((0.42, 0.24, 0.14), rough=0.8, noise=0.25)
        s.glass = mat((0.10, 0.14, 0.18), rough=0.12, metal=0.3, noise=0)
        s.win = mat((0.08, 0.10, 0.12), rough=0.2, noise=0)
        s.concrete = mat((0.34, 0.34, 0.32), rough=0.9, noise=0.22, scale=3)
        s.asphalt = mat((0.16, 0.16, 0.16), rough=0.9, noise=0.2, scale=2)
        s.paint = mat((0.92, 0.92, 0.88), rough=0.6, noise=0)
        s.yellow = mat((0.85, 0.68, 0.12), rough=0.6, noise=0)
        s.ground = mat(R['ground'], rough=1, noise=0.25, scale=1.5)
        s.green = mat(R['green'], rough=1, noise=0.35, scale=2)
        s.olive = mat((0.28, 0.30, 0.20), rough=0.8, noise=0.2)
        s.sand = mat((0.62, 0.55, 0.40), rough=1, noise=0.3, scale=4)
        s.white = mat((0.62, 0.62, 0.60), rough=0.5, noise=0.08)
        # industrial metal roof: ribbed grey with streaks of grime
        s.indroof = mat((0.36, 0.39, 0.42), rough=0.45, metal=0.4, noise=0.3, scale=14)
        s.dark = mat((0.12, 0.12, 0.12), rough=0.8, noise=0.1)
        s.water = mat((0.10, 0.22, 0.30), rough=0.08, noise=0)
        s.red = mat((0.70, 0.12, 0.10), rough=0.6, noise=0.05)

    def lot(s, sx, sy, m=None, force=False):
        # no slab under buildings: the real city streets show around them, so nothing looks pasted on.
        # Only functional ground (runways, harbours) is modelled; shadows land on the map through the shadow catcher.
        if force: box(0, 0, 0, sx, sy, 0.08, m or s.concrete, bevel=0.02)

    def house(s, x, y, sx, sy, floors, rot=0, wall=None, roof=None, flat=False):
        h = floors * 3.2; wall = wall or s.wall
        box(x, y, 0.08, sx, sy, h, wall, rot=rot)
        if rot == 0: windows(x, y, 0.08, sx, sy, h, floors, s.win)
        k = 'flat' if flat else s.R['roof_kind']
        if k == 'gable':
            gable(x, y, h + 0.08, sx, sy, min(sx, sy) * 0.35, roof or s.roof, rot=rot if sx >= sy else rot + 90)
        elif k == 'shallow':
            gable(x, y, h + 0.08, sx, sy, min(sx, sy) * 0.14, roof or s.roof, rot=rot if sx >= sy else rot + 90, overhang=0.4)
        else:
            box(x, y, h + 0.08, sx, sy, 0.15, roof or s.roof, bevel=0, rot=rot)
            # parapet and rooftop machinery
            for dx, dy, lx, ly in [(0, sy / 2, sx, 0.25), (0, -sy / 2, sx, 0.25), (sx / 2, 0, 0.25, sy), (-sx / 2, 0, 0.25, sy)]:
                if rot == 0: box(x + dx, y + dy, h + 0.08, lx, ly, 0.7, wall, bevel=0.02)
            if rot == 0:
                box(x + sx * 0.2, y - sy * 0.15, h + 0.2, 1.4, 1.0, 0.8, s.metal)
                if s.R is REGIONS['gulf']: cyl(x - sx * 0.25, y + sy * 0.2, h + 0.2, 0.55, 1.0, s.white)    # roof water tank
        return h

    def tree(s, x, y, r=1.2):
        cyl(x, y, 0, 0.15, 1.2, s.dark, verts=6)
        sphere_cap(x, y, 1.2 + r * 0.7, r, s.green)

    def palm(s, x, y):
        cyl(x, y, 0, 0.14, 4.5, mat((0.40, 0.32, 0.22)), verts=6)
        for a in range(6):
            ang = a * math.pi / 3
            box(x + math.cos(ang) * 0.9, y + math.sin(ang) * 0.9, 4.3, 2.0, 0.5, 0.1, s.green, bevel=0, rot=math.degrees(ang))

    def plant(s, x, y):
        (s.palm if s.R is REGIONS['gulf'] else s.tree)(x, y)

    def flag(s, x, y, h=9):
        cyl(x, y, 0.08, 0.08, h, s.metal, verts=8)
        box(x + 0.9, y, h - 1.2, 1.8, 0.06, 1.1, s.accent, bevel=0)

    def truck(s, x, y, rot=0):
        box(x, y, 0.1, 4.0, 1.8, 1.4, s.olive, rot=rot)
        bx = x - math.sin(math.radians(rot)) * 0 + math.cos(math.radians(rot)) * 2.3
        by = y + math.sin(math.radians(rot)) * 2.3
        box(bx, by, 0.1, 1.4, 1.8, 1.7, s.olive, rot=rot)

    def fence(s, sx, sy):
        # thin wire fence: barely visible from above, like the real thing
        for dx, dy, lx, ly in [(0, sy / 2, sx, 0.06), (0, -sy / 2, sx, 0.06), (sx / 2, 0, 0.06, sy), (-sx / 2, 0, 0.06, sy)]:
            box(dx, dy, 0.08, lx, ly, 1.2, mat((0.45, 0.45, 0.43), noise=0), bevel=0)

# ---------- the seven buildings; each level adds to the one before ----------
def training_camp(k, L):
    sx = 18 + L * 4.5; sy = 16 + L * 3.5
    k.lot(sx, sy, k.ground)
    k.fence(sx, sy)
    box(-sx * 0.12, -sy * 0.08, 0.08, sx * 0.45, sy * 0.38, 0.05, k.asphalt, bevel=0)       # parade ground
    for i in range(3): box(-sx * 0.12 - sx * 0.15 + i * sx * 0.15, -sy * 0.08, 0.13, 0.25, sy * 0.3, 0.01, k.paint, bevel=0)
    # barracks rows: tents at level 1, real blocks from level 2
    n = 2 + L
    for i in range(n):
        y = sy / 2 - 2.5 - i * 3.6
        if y < -sy / 2 + 2: break
        if L == 1: box(sx * 0.3, y, 0.08, 6.0, 2.6, 2.0, k.olive, bevel=0.5)
        else: k.house(sx * 0.3, y, 7.0, 2.8, 1)
    k.flag(-sx * 0.12, sy * 0.2)
    if L >= 2: k.house(-sx * 0.33, sy * 0.33, 6, 4.5, 2, wall=k.wall2)                         # headquarters
    if L >= 3:                                                                                  # firing range lanes
        for i in range(4): box(-sx * 0.3 + i * 1.4, -sy * 0.38, 0.08, 0.3, sy * 0.18, 0.4, k.sand, bevel=0)
    if L >= 4:                                                                                  # vehicle park
        for i in range(3): k.truck(sx * 0.05 + i * 2.4, -sy * 0.38, rot=90)
    if L >= 5:                                                                                  # obstacle course + jump tower
        for i in range(5): box(-sx * 0.42, -sy * 0.05 + i * 1.8, 0.08, 1.6, 0.3, 1.0 + (i % 2), k.dark, bevel=0)
        box(sx * 0.42, sy * 0.38, 0.08, 1.8, 1.8, 9.0, k.metal)
    for i in range(L): k.plant(-sx / 2 + 1.2 + i * 2.2, -sy / 2 + 1.0)

def factory(k, L):
    sx = 16 + L * 5; sy = 14 + L * 4
    k.lot(sx, sy)
    halls = [(0.0, 0.1, 0.55, 0.5)] + [(-0.3, -0.25, 0.32, 0.38), (0.3, -0.25, 0.32, 0.38), (0.32, 0.3, 0.3, 0.3)][:max(0, L - 1)]
    for fx, fy, fw, fd in halls:
        w, d = sx * fw, sy * fd
        box(fx * sx, fy * sy, 0.08, w, d, 6.0, k.wall2)
        sawtooth(fx * sx, fy * sy, 6.08, w, d, max(3, int(d / 2.2)), 2.0, k.indroof, k.glass)
        for j in range(3): box(fx * sx - w * 0.3 + j * w * 0.3, fy * sy + d * 0.3, 8.1, 1.0, 0.8, 0.6, k.metal)   # roof fans
    for i in range(min(L, 3)):                                                                  # chimneys grow with level
        cyl(-sx * 0.42 + i * 2.2, sy * 0.38, 0.08, 0.8, 10 + L * 3, mat((0.50, 0.45, 0.42), noise=0.2))
        cyl(-sx * 0.42 + i * 2.2, sy * 0.38, 10 + L * 3 + 0.08, 0.85, 1.2, k.red)
    if L >= 3:                                                                                  # storage tanks
        for i in range(2): cyl(sx * 0.42, -sy * 0.42 + i * 3.2, 0.08, 1.4, 4.5, k.white)
    if L >= 2:
        for i in range(L): k.truck(-sx * 0.42 + i * 2.4, -sy * 0.43, rot=90)
    if L >= 4:                                                                                  # rail spur along the edge
        box(0, -sy / 2 + 0.6, 0.08, sx, 1.4, 0.1, k.dark, bevel=0)
        for i in range(3): box(-sx * 0.3 + i * 5.2, -sy / 2 + 0.6, 0.18, 4.8, 1.2, 1.6, k.rust)
    if L >= 5:                                                                                  # gantry crane over the yard
        box(sx * 0.1, -sy * 0.42, 6.0, sx * 0.5, 0.6, 0.6, k.yellow)
        for dx in (-0.15, 0.35): box(sx * dx, -sy * 0.42, 0.08, 0.5, 0.5, 6.0, k.yellow)

def airport(k, L):
    rl = 20 + L * 5                                                                             # runway grows with level
    k.lot(rl + 4, 12 + L * 3.5, k.green)
    box(0, -2, 0.08, rl, 3.6, 0.06, k.asphalt, bevel=0)
    for i in range(int(rl / 3)): box(-rl / 2 + 1.5 + i * 3, -2, 0.15, 1.2, 0.18, 0.01, k.paint, bevel=0)
    for e in (-1, 1):
        for j in range(4): box(e * (rl / 2 - 0.8), -2.9 + j * 0.6, 0.15, 1.0, 0.3, 0.01, k.paint, bevel=0)
    box(0, 1.6, 0.08, rl * 0.6, 1.0, 0.06, k.asphalt, bevel=0)                                 # taxiway
    box(-rl * 0.2, 4.2, 0.08, rl * 0.42, 4.2, 0.06, k.concrete, bevel=0)                        # apron
    hangars = min(1 + L // 2, 3)
    for i in range(hangars):                                                                    # curved-roof hangars
        hx = -rl * 0.34 + i * 6.5
        cyl(hx, 4.6 + L * 0.4, 0.08, 2.6, 5.5, k.metal, verts=24, axis='Y')
        box(hx, 4.6 + L * 0.4, 0.08, 5.2, 5.5, 0.1, k.concrete, bevel=0)
    if L >= 3:                                                                                  # control tower
        cyl(rl * 0.22, 5.5, 0.08, 0.9, 9, k.wall2); cyl(rl * 0.22, 5.5, 9.08, 1.5, 1.6, k.glass); cyl(rl * 0.22, 5.5, 10.68, 1.6, 0.25, k.wall)
    if L >= 2:
        for i in range(L - 1):                                                                  # parked jets as small grey crosses
            px, py = -rl * 0.05 + i * 2.6, 3.4
            box(px, py, 0.2, 0.5, 3.0, 0.4, mat((0.45, 0.48, 0.50)), bevel=0.1)
            box(px, py + 0.2, 0.25, 2.6, 0.7, 0.1, mat((0.45, 0.48, 0.50)), bevel=0)
    if L >= 4:                                                                                  # hardened aircraft shelters
        for i in range(2):
            cyl(rl * 0.38, 4.0 + i * 4.2, 0.08, 1.8, 4.0, k.concrete, verts=16, axis='X')
    if L >= 5:                                                                                  # radar dome
        cyl(rl * 0.05, 7.6, 0.08, 1.0, 2.0, k.wall); sphere_cap(rl * 0.05, 7.6, 2.6, 1.3, k.white)

def port(k, L):
    sx = 22 + L * 4; sy = 18 + L * 2
    box(0, -sy * 0.28, 0, sx, sy * 0.44, 0.02, k.water, bevel=0)                                # harbour water (front)
    box(0, sy * 0.22, 0, sx, sy * 0.56, 1.0, k.concrete, bevel=0.05)                           # quay
    for i in range(min(1 + L // 2, 3)):                                                         # piers
        box(-sx * 0.3 + i * sx * 0.3, -sy * 0.2, 0, 2.2, sy * 0.36, 1.0, k.concrete, bevel=0.05)
    for i in range(L):                                                                          # containers
        for j in range(3):
            c = mat([(0.62, 0.18, 0.12), (0.12, 0.32, 0.52), (0.72, 0.58, 0.18), (0.25, 0.45, 0.30)][(i + j) % 4], noise=0.1)
            box(-sx * 0.4 + i * 2.8, sy * 0.38 - j * 1.4, 1.0, 2.4, 1.1, 1.1 + (j % 2) * 1.1, c, bevel=0.02)
    for i in range(min(L, 4)):                                                                  # cranes
        cx = -sx * 0.25 + i * 5.5
        for dx in (-0.8, 0.8): box(cx + dx, sy * 0.03, 1.0, 0.35, 0.35, 8.0, k.yellow)
        box(cx, sy * 0.03 - 1.5, 9.0, 0.6, 7.0, 0.6, k.yellow)
    k.house(sx * 0.36, sy * 0.33, 5, 4, 2, wall=k.wall2)                                         # harbour office
    if L >= 2: box(sx * 0.1, -sy * 0.3, 0.02, 8 + L, 2.0, 1.4, mat((0.36, 0.38, 0.40)), bevel=0.4)   # a moored patrol boat
    if L >= 4: k.house(-sx * 0.36, sy * 0.15, 6, 3.5, 1)                                         # dry dock workshop
    if L >= 5: box(sx * 0.32, -sy * 0.08, 0.02, 1.4, sy * 0.28, 1.0, k.concrete, bevel=0.05)    # breakwater

def industry(k, L):
    sx = 16 + L * 4.5; sy = 14 + L * 4
    k.lot(sx, sy, k.ground)
    for i in range(L + 1):                                                                       # silos and tanks for the city's resource
        cyl(-sx * 0.35 + (i % 3) * 3.4, sy * 0.25 - (i // 3) * 3.4, 0.08, 1.4, 5 + (i % 2) * 2, k.white if i % 2 else k.metal)
    k.house(sx * 0.22, sy * 0.18, sx * 0.35, sy * 0.35, 2, wall=k.wall2)                         # processing hall
    for i in range(min(L, 4)):                                                                    # warehouses
        box(-sx * 0.25 + i * 4.6, -sy * 0.35, 0.08, 4.0, 3.2, 3.2, k.wall)
        gable(-sx * 0.25 + i * 4.6, -sy * 0.35, 3.28, 4.0, 3.2, 0.8, k.roof, rot=90, overhang=0.1)
    if L >= 2: box(-sx * 0.05, sy * 0.25, 4.0, sx * 0.3, 0.4, 0.4, k.metal)                     # pipe bridge
    if L >= 3: cyl(sx * 0.42, sy * 0.42, 0.08, 0.6, 12 + L * 2, mat((0.55, 0.5, 0.48), noise=0.2))  # flare stack
    if L >= 4:
        for i in range(2): k.truck(sx * 0.1 + i * 2.6, -sy * 0.05, rot=90)
    if L >= 5: box(sx * 0.42, -sy * 0.2, 0.08, 2.0, 6.0, 3.0, k.rust)                             # conveyor housing

def hospital(k, L):
    sx = 18 + L * 6; sy = 16 + L * 5
    k.lot(sx, sy)
    floors = 1 + L
    k.house(0, sy * 0.05, sx * 0.62, sy * 0.24, floors, wall=k.white, flat=True)                  # main block
    k.house(-sx * 0.22, sy * 0.05, sx * 0.16, sy * 0.62, floors, wall=k.white, flat=True)          # wings: H shape
    k.house(sx * 0.22, sy * 0.05, sx * 0.16, sy * 0.62, floors, wall=k.white, flat=True)
    if k.R['dome']: cyl(0, -sy * 0.08, 0.08, 2.0, 4.0, k.wall2); sphere_cap(0, -sy * 0.08, 4.3, 2.0, k.accent)   # domed entrance hall
    h = floors * 3.2 + 0.25
    cyl(0, sy * 0.05, h, 1.6, 0.06, k.dark, verts=32)                                             # rooftop helipad, plain H
    box(-0.5, sy * 0.05, h + 0.06, 0.25, 1.6, 0.01, k.paint, bevel=0); box(0.5, sy * 0.05, h + 0.06, 0.25, 1.6, 0.01, k.paint, bevel=0)
    box(0, sy * 0.05, h + 0.06, 1.0, 0.25, 0.01, k.paint, bevel=0)
    box(0, -sy * 0.38, 0.08, sx * 0.5, sy * 0.15, 0.04, k.asphalt, bevel=0)                       # ambulance bay
    for i in range(L + 1): box(-sx * 0.15 + i * 2.2, -sy * 0.38, 0.12, 1.0, 2.2, 1.2, k.white, bevel=0.15)
    for i in range(2 + L): k.plant(-sx * 0.45 + i * 3, sy * 0.44)

def bunker(k, L):
    sx = 14 + L * 3.5; sy = 12 + L * 3
    k.lot(sx, sy, k.sand)
    sandbag = mat((0.52, 0.46, 0.32), noise=0.3, scale=12)
    # sandbag ring at every level
    for a in range(16):
        ang = a / 16 * 2 * math.pi
        box(math.cos(ang) * sx * 0.38, math.sin(ang) * sy * 0.38, 0.08, 2.2, 0.9, 0.9, sandbag, bevel=0.3, rot=math.degrees(ang) + 90)
    if L >= 2:                                                                                    # concrete pillboxes
        for x, y in [(-sx * 0.25, 0), (sx * 0.25, 0)][:L - 1 if L < 4 else 2]:
            cyl(x, y, 0.08, 1.8, 1.6, k.concrete, verts=8); box(x, y - 1.6, 0.9, 1.8, 0.3, 0.3, k.dark, bevel=0)
    if L >= 3:                                                                                    # zig-zag trench
        for i in range(6):
            box(-sx * 0.3 + i * sx * 0.12, -sy * 0.2 + (i % 2) * 1.2, 0.0, sx * 0.13, 0.9, 0.12, k.dark, bevel=0, rot=25 if i % 2 else -25)
    if L >= 4:                                                                                    # earth-covered command bunker
        sphere_cap(0, sy * 0.15, 0.4, 3.2, mat((0.40, 0.42, 0.28), noise=0.3)); box(0, sy * 0.15 - 3.0, 0.08, 1.4, 1.2, 1.4, k.concrete)
    if L >= 5:                                                                                    # anti-air guns and dragon's teeth
        for x in (-sx * 0.3, sx * 0.3):
            cyl(x, sy * 0.3, 0.08, 1.1, 0.6, k.concrete, verts=12); box(x, sy * 0.3 + 0.9, 0.9, 0.25, 2.2, 0.25, k.dark, bevel=0, rot=20)
        for i in range(8): box(-sx * 0.42 + i * sx * 0.12, -sy * 0.45, 0.08, 0.9, 0.9, 0.9, k.concrete, bevel=0.1, rot=45)

TYPES = {'training_camp': training_camp, 'factory': factory, 'airport': airport, 'port': port,
         'industry': industry, 'hospital': hospital, 'bunker': bunker}

def camera(s):
    cd = bpy.data.cameras.new('cam'); cd.type = 'ORTHO'; cd.ortho_scale = FRAME
    cam = bpy.data.objects.new('cam', cd); s.collection.objects.link(cam); s.camera = cam
    e, a = math.radians(ELEV), math.radians(AZIM)
    d = 120
    cam.location = (math.sin(a) * math.cos(e) * -d, -math.cos(a) * math.cos(e) * d, math.sin(e) * d)
    cam.rotation_euler = (math.radians(90 - ELEV), 0, a)
    cam.location.z += 2.0

only = set(filter(None, os.environ.get('ONLY', '').split(',')))
regs = list(filter(None, os.environ.get('REGIONS', '').split(','))) or list(REGIONS)
levels = [int(v) for v in filter(None, os.environ.get('LEVELS', '').split(','))] or [1, 2, 3, 4, 5]
for reg in regs:
    for name, fn in TYPES.items():
        if only and name not in only: continue
        for L in levels:
            if L > MAXLEVEL.get(name, 5): continue
            s = reset(); MATS.clear()
            random.seed(L * 7 + len(name))
            fn(Kit(REGIONS[reg]), L)
            camera(s)
            s.render.filepath = os.path.abspath(os.path.join(OUT, f'{name}_{reg}_{L}.png'))
            bpy.ops.render.render(write_still=True)
            print('rendered', name, reg, L, flush=True)
