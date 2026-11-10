# Blender: renders the downloaded artist models as game icons, tinted per side, with the same
# real-sky lighting and camera as the rest of the art. Run: blender -b -P render_models.py -- models out
import bpy, math, os, sys, glob, json
from mathutils import Vector
args = sys.argv[sys.argv.index('--') + 1:]
SRC, OUT = args[0], args[1]
os.makedirs(OUT, exist_ok=True)
SIZE = int(os.environ.get('ICON_SIZE', '512'))
ROT = json.load(open('ci/models/rotations.json')) if os.path.exists('ci/models/rotations.json') else {}
TINT = {
    'green': {'ground': (0.55, 0.62, 0.42), 'air': (0.62, 0.66, 0.64), 'sea': (0.66, 0.69, 0.71)},
    'tan':   {'ground': (0.86, 0.74, 0.55), 'air': (0.80, 0.76, 0.68), 'sea': (0.80, 0.77, 0.70)},
}
KIND = {'fighter': 'air', 'heli': 'air', 'destroyer': 'sea', 'sub': 'sea'}

def scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    s = bpy.context.scene
    s.render.engine = 'CYCLES'; s.cycles.device = 'CPU'; s.cycles.samples = 64; s.cycles.use_denoising = True
    s.render.film_transparent = True; s.render.resolution_x = s.render.resolution_y = SIZE
    s.render.image_settings.color_mode = 'RGBA'
    try: s.view_settings.view_transform = 'AgX'
    except Exception: pass
    w = bpy.data.worlds.new('w'); s.world = w; w.use_nodes = True
    nt = w.node_tree; bg = nt.nodes['Background']
    if os.path.exists('tex/sky.hdr'):
        env = nt.nodes.new('ShaderNodeTexEnvironment'); env.image = bpy.data.images.load(os.path.abspath('tex/sky.hdr'))
        nt.links.new(env.outputs['Color'], bg.inputs[0])
    sun = bpy.data.lights.new('sun', 'SUN'); sun.energy = 2.4; sun.angle = math.radians(5)
    so = bpy.data.objects.new('sun', sun); s.collection.objects.link(so); so.rotation_euler = (math.radians(48), 0, math.radians(150))
    bpy.ops.mesh.primitive_plane_add(size=400); bpy.context.object.is_shadow_catcher = True; bpy.context.object.name = 'ground'
    return s

def tint_materials(objs, col):
    done = set()
    for o in objs:
        for slot in o.material_slots:
            m = slot.material
            if not m or m.name in done or not m.use_nodes: continue
            done.add(m.name)
            nt = m.node_tree
            for p in [n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED']:
                inp = p.inputs['Base Color']
                hs = nt.nodes.new('ShaderNodeHueSaturation'); hs.inputs['Saturation'].default_value = 0.3
                mix = nt.nodes.new('ShaderNodeMixRGB'); mix.blend_type = 'MULTIPLY'; mix.inputs['Fac'].default_value = 0.9
                mix.inputs['Color2'].default_value = (*col, 1)
                if inp.is_linked:
                    src = inp.links[0].from_socket
                    nt.links.new(src, hs.inputs['Color'])
                else:
                    hs.inputs['Color'].default_value = inp.default_value
                nt.links.new(hs.outputs['Color'], mix.inputs['Color1'])
                nt.links.new(mix.outputs['Color'], inp)

def load(unit):
    files = glob.glob(f'{SRC}/{unit}/**/*.gltf', recursive=True) + glob.glob(f'{SRC}/{unit}/**/*.glb', recursive=True)
    if not files: return []
    bpy.ops.import_scene.gltf(filepath=files[0])
    objs = [o for o in bpy.context.scene.objects if o.type == 'MESH' and o.name != 'ground']
    # normalise: longest side 7 units, standing on the ground, centred, facing the chosen way
    root = bpy.data.objects.new('root', None); bpy.context.scene.collection.objects.link(root)
    for o in bpy.context.scene.objects:
        if o.parent is None and o not in (root,) and o.name not in ('ground', 'sun'): o.parent = root
    bpy.context.view_layer.update()
    pts = [o.matrix_world @ Vector(c) for o in objs for c in o.bound_box]
    mn = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    mx = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    size = max(mx - mn)
    k = 7.0 / size
    root.scale = (k, k, k)
    root.location = (-(mn.x + mx.x) / 2 * k, -(mn.y + mx.y) / 2 * k, -mn.z * k)
    root.rotation_euler[2] = math.radians(ROT.get(unit, 0))
    bpy.context.view_layer.update()
    return objs

def frame_and_render(name, objs, alt=0.0, elev=28, azim=-38):
    s = bpy.context.scene
    if alt:
        for o in s.objects:
            if o.name == 'root': o.location.z += alt
    bpy.context.view_layer.update()
    cam_d = bpy.data.cameras.new('cam'); cam_d.type = 'ORTHO'
    cam = bpy.data.objects.new('cam', cam_d); s.collection.objects.link(cam); s.camera = cam
    e, a = math.radians(elev), math.radians(azim)
    d = Vector((math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)))
    pts = [o.matrix_world @ Vector(c) for o in objs for c in o.bound_box]
    if alt: pts += [Vector((p.x - alt * 0.9, p.y + alt * 0.5, 0)) for p in pts]   # keep the ground shadow in frame
    c = sum(pts, Vector()) / len(pts)
    cam.location = c + d * 80; cam.rotation_euler = (-d).to_track_quat('-Z', 'Y').to_euler()
    bpy.context.view_layer.update()
    inv = cam.matrix_world.inverted(); q = [inv @ p for p in pts]
    xs = [p.x for p in q]; ys = [p.y for p in q]
    cam_d.ortho_scale = max(max(xs) - min(xs), max(ys) - min(ys)) * 1.1
    cam.location = cam.matrix_world @ Vector(((max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2, 0))
    s.render.filepath = os.path.join(OUT, name + '.png')
    bpy.ops.render.render(write_still=True)
    print('rendered', name)

units = sorted(d for d in os.listdir(SRC) if os.path.isdir(os.path.join(SRC, d)))
for unit in units:
    for side in ('green', 'tan'):
        scene()
        objs = load(unit)
        if not objs: print('no model for', unit); break
        tint_materials(objs, TINT[side][KIND.get(unit, 'ground')])
        frame_and_render(f'{unit}_{side}', objs, alt=3.0 if unit in ('fighter', 'heli') else 0.0)
