# Blender: simulates a real ocean surface (FFT ocean, periodic, so the tile is seamless) and saves its
# surface normals seen from straight above. The map baker then paints our sea colours with these waves.
import bpy, math, os, sys
OUT = sys.argv[sys.argv.index('--') + 1]
RES = int(os.environ.get('TILE_RES', '1024'))
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'CYCLES'; sc.cycles.samples = 4; sc.cycles.use_denoising = False
sc.render.resolution_x = sc.render.resolution_y = RES
sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_depth = '16'
sc.view_settings.view_transform = 'Standard'
sc.render.filter_size = 0.8
bpy.ops.mesh.primitive_plane_add(size=1)
sea = bpy.context.object
oc = sea.modifiers.new('ocean', 'OCEAN')
oc.geometry_mode = 'GENERATE'
oc.spatial_size = 50; oc.size = 1.0; oc.repeat_x = oc.repeat_y = 1
oc.resolution = int(os.environ.get('OCEAN_RES', '16'))
oc.wave_scale = 1.0; oc.choppiness = 1.0
oc.wind_velocity = float(os.environ.get('WIND', '14'))
oc.wave_alignment = 0.55; oc.wave_direction = math.radians(25)
oc.use_normals = True; oc.random_seed = 3
for p in sea.data.polygons: p.use_smooth = True
m = bpy.data.materials.new('n'); m.use_nodes = True
nt = m.node_tree; nt.nodes.remove(nt.nodes['Principled BSDF'])
geo = nt.nodes.new('ShaderNodeNewGeometry')
mp = nt.nodes.new('ShaderNodeVectorMath'); mp.operation = 'MULTIPLY_ADD'
mp.inputs[1].default_value = (0.5, 0.5, 0.5); mp.inputs[2].default_value = (0.5, 0.5, 0.5)
nt.links.new(geo.outputs['Normal'], mp.inputs[0])
em = nt.nodes.new('ShaderNodeEmission'); nt.links.new(mp.outputs['Vector'], em.inputs['Color'])
nt.links.new(em.outputs['Emission'], nt.nodes['Material Output'].inputs['Surface'])
sea.data.materials.append(m)
bpy.context.view_layer.update()
ev = sea.evaluated_get(bpy.context.evaluated_depsgraph_get())
xs = [v.co.x for v in ev.data.vertices]; ys = [v.co.y for v in ev.data.vertices]
cx, cy = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
cam_d = bpy.data.cameras.new('c'); cam_d.type = 'ORTHO'; cam_d.ortho_scale = oc.spatial_size * 0.98
cam = bpy.data.objects.new('c', cam_d); sc.collection.objects.link(cam); sc.camera = cam
cam.location = (cx, cy, 30)
sc.render.filepath = OUT
bpy.ops.render.render(write_still=True)
print('rendered ocean tile', OUT, 'extent', max(xs) - min(xs))
