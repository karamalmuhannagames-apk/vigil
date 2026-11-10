# Blender: turns the baked layers into a real 3D landscape (relief, instanced trees, simulated ocean)
# and photographs it from straight above, the way top-down strategy maps are made.
# Run: blender -b -P ci/map/render3d.py -- <layers dir> <out png>
import bpy, math, os, sys
args = sys.argv[sys.argv.index('--') + 1:]
LAY, OUT = args[0], args[1]
RES = int(os.environ.get('MAP_RES', '2048'))
SAMPLES = int(os.environ.get('MAP_SAMPLES', '24'))
W = 20.0                  # world size of the map in Blender units
RELIEF = float(os.environ.get('RELIEF', '0.55'))
SEA_DEPTH_SCALE = 1.4     # height16 stores -0.35..1.05

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'
sc.cycles.samples = SAMPLES; sc.cycles.use_denoising = True
sc.render.resolution_x = RES; sc.render.resolution_y = RES
sc.render.image_settings.file_format = 'PNG'
try:
    sc.view_settings.view_transform = 'AgX'
except Exception:
    sc.view_settings.view_transform = 'Filmic'
sc.view_settings.exposure = -0.3

def img(name, data=True):
    im = bpy.data.images.load(os.path.join(LAY, name))
    if data: im.colorspace_settings.name = 'Non-Color'
    return im

# ---------- world and sun ----------
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
bg = w.node_tree.nodes['Background']
bg.inputs[0].default_value = (0.52, 0.62, 0.78, 1); bg.inputs[1].default_value = 0.7
sun = bpy.data.lights.new('sun', 'SUN'); sun.energy = 3.4; sun.angle = math.radians(2.5)
sun.color = (1.0, 0.97, 0.92)
so = bpy.data.objects.new('sun', sun); sc.collection.objects.link(so)
so.rotation_euler = (math.radians(52), 0, math.radians(-40))   # light from the north-west, like CoN

# ---------- terrain mesh ----------
N = int(os.environ.get('MESH_DIV', '1024'))
bpy.ops.mesh.primitive_grid_add(x_subdivisions=N, y_subdivisions=N, size=W)
terr = bpy.context.object; terr.name = 'terrain'
htex = bpy.data.textures.new('h', 'IMAGE'); htex.image = img('height16.png'); htex.extension = 'EXTEND'
htex.use_interpolation = True
d = terr.modifiers.new('relief', 'DISPLACE'); d.texture = htex; d.texture_coords = 'UV'
d.strength = RELIEF * SEA_DEPTH_SCALE; d.mid_level = 0.35 / SEA_DEPTH_SCALE
for p in terr.data.polygons: p.use_smooth = True

m = bpy.data.materials.new('ground'); m.use_nodes = True
nt = m.node_tree; P = nt.nodes['Principled BSDF']
P.inputs['Roughness'].default_value = 0.92
uv = nt.nodes.new('ShaderNodeTexCoord')
alb = nt.nodes.new('ShaderNodeTexImage'); alb.image = img('albedo.png', data=False); alb.extension = 'EXTEND'
nt.links.new(uv.outputs['UV'], alb.inputs['Vector'])
# fine ground grain so close zoom is never smooth
grain = nt.nodes.new('ShaderNodeTexNoise'); grain.inputs['Scale'].default_value = 900; grain.inputs['Detail'].default_value = 6
gr = nt.nodes.new('ShaderNodeMapRange'); gr.inputs['To Min'].default_value = 0.85; gr.inputs['To Max'].default_value = 1.12
nt.links.new(grain.outputs['Fac'], gr.inputs['Value'])
mul = nt.nodes.new('ShaderNodeMixRGB'); mul.blend_type = 'MULTIPLY'; mul.inputs['Fac'].default_value = 1.0
nt.links.new(alb.outputs['Color'], mul.inputs['Color1'])
comb = nt.nodes.new('ShaderNodeCombineRGB')
for c in 'RGB': nt.links.new(gr.outputs['Result'], comb.inputs[c])
nt.links.new(comb.outputs[0], mul.inputs['Color2'])
# steep slopes show bare rock
geo = nt.nodes.new('ShaderNodeNewGeometry'); sep = nt.nodes.new('ShaderNodeSeparateXYZ')
nt.links.new(geo.outputs['Normal'], sep.inputs[0])
sl = nt.nodes.new('ShaderNodeMapRange'); sl.inputs['From Min'].default_value = 0.93; sl.inputs['From Max'].default_value = 0.72
nt.links.new(sep.outputs['Z'], sl.inputs['Value'])
rock = nt.nodes.new('ShaderNodeMixRGB'); rock.inputs['Color2'].default_value = (0.36, 0.37, 0.32, 1)
nt.links.new(sl.outputs['Result'], rock.inputs['Fac']); nt.links.new(mul.outputs['Color'], rock.inputs['Color1'])
nt.links.new(rock.outputs['Color'], P.inputs['Base Color'])
terr.data.materials.append(m)

# ---------- trees: instanced 3D trees scattered by the forest map ----------
def make_tree(name, crown_col, h=0.05, r=0.022):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=r, location=(0, 0, h * 0.62))
    crown = bpy.context.object; crown.scale = (1, 1, 1.25)
    bpy.ops.mesh.primitive_cylinder_add(radius=r * 0.18, depth=h * 0.5, location=(0, 0, h * 0.25))
    trunk = bpy.context.object
    tm = bpy.data.materials.new(name + '_c'); tm.use_nodes = True
    tp = tm.node_tree.nodes['Principled BSDF']; tp.inputs['Roughness'].default_value = 0.85
    oi = tm.node_tree.nodes.new('ShaderNodeObjectInfo')
    ramp = tm.node_tree.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].color = (crown_col[0] * 0.7, crown_col[1] * 0.75, crown_col[2] * 0.7, 1)
    ramp.color_ramp.elements[1].color = (crown_col[0] * 1.25, crown_col[1] * 1.2, crown_col[2] * 1.1, 1)
    tm.node_tree.links.new(oi.outputs['Random'], ramp.inputs['Fac'])
    tm.node_tree.links.new(ramp.outputs['Color'], tp.inputs['Base Color'])
    crown.data.materials.append(tm)
    bm = bpy.data.materials.new(name + '_t'); bm.use_nodes = True
    bm.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.08, 0.06, 0.04, 1)
    trunk.data.materials.append(bm)
    bpy.ops.object.select_all(action='DESELECT'); crown.select_set(True); trunk.select_set(True)
    bpy.context.view_layer.objects.active = crown; bpy.ops.object.join()
    t = bpy.context.object; t.name = name; t.location = (0, 0, -50)   # parked out of sight
    return t

broad = make_tree('broadleaf', (0.07, 0.17, 0.05))
pine = make_tree('pine', (0.04, 0.12, 0.05), h=0.06, r=0.017)
coll = bpy.data.collections.new('trees'); sc.collection.children.link(coll)
for t in (broad, pine):
    sc.collection.objects.unlink(t); coll.objects.link(t)

def scatter(mask_png, count, name):
    ftex = bpy.data.textures.new(name, 'IMAGE'); ftex.image = img(mask_png); ftex.extension = 'EXTEND'
    terr.modifiers.new(name, 'PARTICLE_SYSTEM')
    ps = terr.particle_systems[-1]; st = ps.settings
    st.type = 'HAIR'; st.use_advanced_hair = True; st.count = count; st.hair_length = 0.05
    st.render_type = 'COLLECTION'; st.instance_collection = coll; st.use_collection_pick_random = True
    st.particle_size = 1.0; st.size_random = 0.5
    st.use_rotations = True; st.rotation_mode = 'GLOB_Z'; st.phase_factor_random = 2.0
    st.distribution = 'RAND'; st.use_modifier_stack = True
    slot = st.texture_slots.add(); slot.texture = ftex; slot.texture_coords = 'UV'
    slot.use_map_density = True; slot.use_map_time = False; slot.density_factor = 1.0
    ps.seed = len(terr.particle_systems)

scatter('forest.png', int(os.environ.get('TREES', '400000')), 'forest')
scatter('bush.png', int(os.environ.get('BUSHES', '60000')), 'copses')

# ---------- ocean: a simulated sea surface over the sea floor ----------
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0.0))
sea = bpy.context.object; sea.name = 'sea'
oc = sea.modifiers.new('ocean', 'OCEAN')
oc.geometry_mode = 'GENERATE'
oc.spatial_size = int(os.environ.get('OCEAN_TILE', '2'))
oc.repeat_x = oc.repeat_y = int(W / oc.spatial_size)
oc.resolution = int(os.environ.get('OCEAN_RES', '14'))
oc.wave_scale = float(os.environ.get('WAVE_SCALE', '0.004'))
oc.choppiness = 1.2
oc.wind_velocity = float(os.environ.get('WIND', '9'))
oc.wave_alignment = 0.35; oc.wave_direction = math.radians(30)
oc.random_seed = 7
sea.location = (-W / 2, -W / 2, 0.0) if False else (0, 0, 0)
wm = bpy.data.materials.new('water'); wm.use_nodes = True
wp = wm.node_tree.nodes['Principled BSDF']
wp.inputs['Base Color'].default_value = (0.02, 0.06, 0.09, 1)
wp.inputs['Roughness'].default_value = 0.06
wp.inputs['IOR'].default_value = 1.333
for key in ('Transmission Weight', 'Transmission'):
    if key in wp.inputs: wp.inputs[key].default_value = 0.82
sea.data.materials.append(wm)

# ---------- camera straight down ----------
cam_d = bpy.data.cameras.new('cam'); cam_d.type = 'ORTHO'; cam_d.ortho_scale = W
cam_d.clip_end = 200
cam = bpy.data.objects.new('cam', cam_d); sc.collection.objects.link(cam); sc.camera = cam
cam.location = (0, 0, 30); cam.rotation_euler = (0, 0, 0)

sc.render.filepath = OUT
bpy.ops.render.render(write_still=True)
print('rendered map', OUT)
