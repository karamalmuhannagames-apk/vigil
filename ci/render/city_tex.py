# Blender: a large dense city seen from high above, rendered as a map texture (and a sparse village one),
# so cities can be baked into the map ground like in CoN instead of floating icons.
import bpy, math, os, sys, random
OUT = sys.argv[sys.argv.index('--') + 1]
os.makedirs(OUT, exist_ok=True)
RES = int(os.environ.get('TEX_RES', '2048'))
def scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    s = bpy.context.scene
    s.render.engine = 'CYCLES'; s.cycles.samples = 48; s.cycles.use_denoising = True
    s.render.resolution_x = s.render.resolution_y = RES
    s.render.film_transparent = True; s.render.image_settings.color_mode = 'RGBA'
    s.view_settings.view_transform = 'Standard'
    w = bpy.data.worlds.new('w'); s.world = w; w.use_nodes = True
    w.node_tree.nodes['Background'].inputs[0].default_value = (0.6, 0.66, 0.72, 1)
    w.node_tree.nodes['Background'].inputs[1].default_value = 0.6
    sun = bpy.data.lights.new('sun', 'SUN'); sun.energy = 3.0; sun.angle = math.radians(3)
    so = bpy.data.objects.new('sun', sun); s.collection.objects.link(so); so.rotation_euler = (math.radians(50), 0, math.radians(-40))
    return s
def mat(name, c, r=0.8):
    m = bpy.data.materials.new(name); m.use_nodes = True
    p = m.node_tree.nodes['Principled BSDF']; p.inputs['Base Color'].default_value = (*c, 1); p.inputs['Roughness'].default_value = r
    return m
def box(w, d, h, x, y, m):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, h / 2)); o = bpy.context.object
    o.scale = (w, d, h); o.data.materials.append(m)
def build(size, density, maxh, block=6.0, road=1.4, seed=1):
    random.seed(seed)
    roofs = [mat('r%d' % i, (v, v, v * 0.98)) for i, v in enumerate((0.55, 0.62, 0.70, 0.78, 0.48))]
    tree = mat('tree', (0.12, 0.22, 0.10))
    ground = mat('ground', (0.36, 0.38, 0.34), 0.95)
    roadm = mat('road', (0.30, 0.31, 0.30), 0.95)
    bpy.ops.mesh.primitive_plane_add(size=size * 1.2); bpy.context.object.data.materials.append(ground)
    n = int(size / block)
    for i in range(n):
        x = -size / 2 + (i + 0.5) * block
        box(road * 0.7, size, 0.02, x - block / 2, 0, roadm)
        box(size, road * 0.7, 0.02, 0, x - block / 2, roadm)
    for i in range(n):
        for j in range(n):
            cx = -size / 2 + (i + 0.5) * block; cy = -size / 2 + (j + 0.5) * block
            r = math.hypot(cx, cy) / (size / 2)
            for k in range(4):
                if random.random() > density * (1 - 0.5 * r): continue
                bw = random.uniform(1.0, 2.2); bd = random.uniform(1.0, 2.2)
                bx = cx + random.uniform(-1.3, 1.3); by = cy + random.uniform(-1.3, 1.3)
                h = random.uniform(0.6, 1.6) + maxh * max(0, 1 - r) ** 2 * random.random()
                box(bw, bd, h, bx, by, random.choice(roofs))
            if random.random() < 0.35:
                bpy.ops.mesh.primitive_ico_sphere_add(radius=random.uniform(0.5, 0.9), subdivisions=1, location=(cx + random.uniform(-2, 2), cy + random.uniform(-2, 2), 0.5))
                bpy.context.object.data.materials.append(tree)
def shoot(name, size):
    s = bpy.context.scene
    cd = bpy.data.cameras.new('c'); cd.type = 'ORTHO'; cd.ortho_scale = size
    cam = bpy.data.objects.new('c', cd); s.collection.objects.link(cam); s.camera = cam
    cam.location = (0, -size * 0.35, 100); cam.rotation_euler = (math.radians(12), 0, 0)   # nearly top-down, a little tilt shows walls
    s.render.filepath = os.path.join(OUT, name + '.png'); bpy.ops.render.render(write_still=True); print('rendered', name)
scene(); build(120, 0.95, 9, seed=3); shoot('city_dense', 100)
scene(); build(120, 0.30, 0.5, block=9, seed=8); shoot('village', 100)
