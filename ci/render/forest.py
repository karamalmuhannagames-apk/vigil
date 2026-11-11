# Forest ground texture for the world map, rendered in Blender the way strategy games paint woodland:
# real 3D crowns (broadleaf and conifer) lit by one north-west sun, seen straight from above, seamless.
#   blender -b -P ci/render/forest.py -- out
# Writes
#   forest.png    RGBA: trees and their shadows over a transparent ground (the game lays them on any ground)
#   forest_id.png L   : each tree's own random value (0 = ground). The game shows a tree only where the real
#                       forest density there is above its value, so forest edges follow whole trees, crisp,
#                       and thin woodland breaks into clumps instead of fading.
import bpy, bmesh, math, random, sys, os
from mathutils import Vector, noise

OUT = sys.argv[sys.argv.index('--') + 1] if '--' in sys.argv else 'out'
os.makedirs(OUT, exist_ok=True)
S = 100.0            # tile size in metres-ish units
RES = 1024
random.seed(11)

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'CYCLES'
sc.cycles.device = 'CPU'
sc.render.resolution_x = sc.render.resolution_y = RES
sc.render.film_transparent = True
sc.view_settings.view_transform = 'Standard'
sc.view_settings.look = 'None'

# ---------- periodic noise (seamless over the tile) ----------
PH = [(random.randint(1, 4), random.randint(1, 4), random.random() * 6.283, random.random() * 6.283, random.uniform(0.5, 1)) for _ in range(7)]
def pnoise(x, y):
    v = 0; t = 0
    for fx, fy, p1, p2, a in PH:
        v += a * math.sin(2 * math.pi * fx * x / S + p1) * math.cos(2 * math.pi * fy * y / S + p2); t += a
    return v / t      # roughly -1..1

# ---------- crown meshes ----------
def broadleaf(seed):
    bm = bmesh.new()
    rnd = random.Random(seed)
    for k in range(rnd.randint(3, 5)):                     # a crown is a few leafy lobes
        m = bmesh.ops.create_icosphere(bm, subdivisions=3, radius=rnd.uniform(0.5, 0.75))
        off = Vector((rnd.uniform(-0.35, 0.35), rnd.uniform(-0.35, 0.35), rnd.uniform(-0.1, 0.25)))
        for v in m['verts']:
            v.co += off
    for v in bm.verts:
        n = noise.noise(v.co * 3.1 + Vector((seed, 0, 0)))
        v.co += v.co.normalized() * n * 0.06
        v.co.z *= 0.75
    me = bpy.data.meshes.new(f'broad{seed}'); bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = True
    return me

def conifer(seed):
    bm = bmesh.new(); rnd = random.Random(seed)
    for k, (r, z) in enumerate([(0.75, 0.0), (0.55, 0.55), (0.32, 1.05)]):
        m = bmesh.ops.create_cone(bm, cap_ends=True, segments=16, radius1=r * rnd.uniform(0.9, 1.1), radius2=0.02, depth=0.9)
        for v in m['verts']:
            v.co.z += z + 0.45
            v.co.x += noise.noise(v.co * 4 + Vector((seed, 1, 0))) * 0.05
    me = bpy.data.meshes.new(f'con{seed}'); bm.to_mesh(me); bm.free()
    return me

MESH = [broadleaf(i) for i in range(4)] + [conifer(10 + i) for i in range(3)]

# ---------- materials: one for the look, one that writes each tree's random value ----------
def mat_look():
    m = bpy.data.materials.new('leaf'); m.use_nodes = True
    nt = m.node_tree; N = nt.nodes; L = nt.links
    bsdf = N['Principled BSDF']; bsdf.inputs['Roughness'].default_value = 0.95
    bsdf.inputs['Specular IOR Level'].default_value = 0.15
    info = N.new('ShaderNodeObjectInfo')
    ramp = N.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].color = (0.30, 0.30, 0.30, 1); ramp.color_ramp.elements[1].color = (0.50, 0.50, 0.50, 1)
    L.new(info.outputs['Random'], ramp.inputs['Fac'])
    tex = N.new('ShaderNodeTexNoise'); tex.inputs['Scale'].default_value = 9.0; tex.inputs['Detail'].default_value = 6
    bump = N.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = 0.6
    L.new(tex.outputs['Fac'], bump.inputs['Height']); L.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    mix = N.new('ShaderNodeMixRGB'); mix.blend_type = 'MULTIPLY'; mix.inputs['Fac'].default_value = 0.35
    L.new(ramp.outputs['Color'], mix.inputs[1]); L.new(tex.outputs['Color'], mix.inputs[2])
    L.new(mix.outputs['Color'], bsdf.inputs['Base Color'])
    return m

def mat_id():
    m = bpy.data.materials.new('id'); m.use_nodes = True
    nt = m.node_tree; N = nt.nodes; L = nt.links
    for n in list(N): N.remove(n)
    out = N.new('ShaderNodeOutputMaterial'); em = N.new('ShaderNodeEmission')
    attr = N.new('ShaderNodeAttribute'); attr.attribute_type = 'OBJECT'; attr.attribute_name = 'tid'
    L.new(attr.outputs['Fac'], em.inputs['Strength']); em.inputs['Color'].default_value = (1, 1, 1, 1)
    L.new(em.outputs['Emission'], out.inputs['Surface'])
    return m

LOOK, IDM = mat_look(), mat_id()

# ---------- place trees: dense packing, clumpy random values ----------
trees = []
cell = 2.0; grid = {}
def ok(x, y, r):
    gx, gy = int(x // cell), int(y // cell)
    for i in range(gx - 2, gx + 3):
        for j in range(gy - 2, gy + 3):
            for (tx, ty, tr) in grid.get((i % 50, j % 50), []):
                dx = (x - tx + S / 2) % S - S / 2; dy = (y - ty + S / 2) % S - S / 2
                if dx * dx + dy * dy < ((r + tr) * 0.5) ** 2: return False
    return True
tries = 0
while tries < 120000:
    tries += 1
    x, y = random.random() * S, random.random() * S
    con = pnoise(x * 0.7 + 13, y * 0.7) > 0.45                    # conifer stands in patches
    r = random.uniform(0.75, 1.0) if con else random.uniform(0.85, 1.5)
    if not ok(x, y, r): continue
    grid.setdefault((int(x // cell) % 50, int(y // cell) % 50), []).append((x, y, r))
    # value: clumpy (big-scale noise) plus a little per-tree chance, so thin forest keeps groups of trees
    v = 0.5 + 0.38 * pnoise(x, y) + random.uniform(-0.12, 0.12)
    trees.append((x, y, r, con, min(0.99, max(0.02, v))))
print('trees', len(trees))

col = bpy.data.collections.new('trees'); sc.collection.children.link(col)
for (x, y, r, con, v) in trees:
    me = MESH[4 + random.randint(0, 2)] if con else MESH[random.randint(0, 3)]
    for ox in (-S, 0, S):
        for oy in (-S, 0, S):
            px, py = x + ox, y + oy
            if not (-4 < px < S + 4 and -4 < py < S + 4): continue
            ob = bpy.data.objects.new('t', me); col.objects.link(ob)
            ob.location = (px, py, 0)
            s = r * (1.0 if not con else 1.15)
            ob.scale = (s, s, s * (1.0 if not con else 1.25))
            ob.rotation_euler.z = random.random() * 6.283
            ob['tid'] = v
for me in MESH:
    me.materials.append(LOOK)

# ground: catches shadows only
bpy.ops.mesh.primitive_plane_add(size=S * 3, location=(S / 2, S / 2, 0))
ground = bpy.context.active_object
ground.is_shadow_catcher = True

# sun from the north-west (game north is +y), a soft sky for the shadow side
sun = bpy.data.lights.new('sun', 'SUN'); sun.energy = 3.0; sun.angle = math.radians(3)
so = bpy.data.objects.new('sun', sun); sc.collection.objects.link(so)
so.rotation_euler = (math.radians(55), 0, math.radians(135))          # light comes from the north-west
world = bpy.data.worlds.new('w'); sc.world = world; world.use_nodes = True
world.node_tree.nodes['Background'].inputs['Color'].default_value = (0.55, 0.62, 0.75, 1)
world.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.9

cam = bpy.data.cameras.new('cam'); cam.type = 'ORTHO'; cam.ortho_scale = S
co = bpy.data.objects.new('cam', cam); sc.collection.objects.link(co)
co.location = (S / 2, S / 2, 50); co.rotation_euler = (0, 0, 0)
sc.camera = co

sc.cycles.samples = 96
sc.cycles.use_denoising = True
sc.render.image_settings.file_format = 'PNG'
sc.render.image_settings.color_mode = 'RGBA'
sc.render.filepath = os.path.join(OUT, 'forest.png')
bpy.ops.render.render(write_still=True)
print('rendered forest.png')

# second pass: the random value of each tree, crisp (no filtering, no lights)
for me in MESH:
    me.materials.clear(); me.materials.append(IDM)
ground.hide_render = True
sc.render.film_transparent = False
world.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.0
sun.energy = 0
sc.cycles.samples = 1; sc.cycles.use_denoising = False
sc.cycles.filter_width = 0.01
sc.render.image_settings.color_mode = 'BW'
sc.render.filepath = os.path.join(OUT, 'forest_id.png')
bpy.ops.render.render(write_still=True)
print('rendered forest_id.png')
