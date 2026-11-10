# Blender script: builds modern military vehicles and city blocks from code
# and renders them as small realistic icons (transparent PNG, soft shadow).
# Run: blender -b -P ci/render/units.py -- <outdir>
import bpy, bmesh, math, sys, os, random
from mathutils import Vector

OUT = sys.argv[sys.argv.index('--') + 1] if '--' in sys.argv else 'art/render'
os.makedirs(OUT, exist_ok=True)
SIZE = int(os.environ.get('ICON_SIZE', '512'))
SAMPLES = int(os.environ.get('ICON_SAMPLES', '96'))

# ---------- scene ----------
def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    s = bpy.context.scene
    s.render.engine = 'CYCLES'
    s.cycles.device = 'CPU'
    s.cycles.samples = SAMPLES
    s.cycles.use_denoising = True
    s.render.film_transparent = True
    s.render.resolution_x = SIZE
    s.render.resolution_y = SIZE
    s.render.image_settings.file_format = 'PNG'
    s.render.image_settings.color_mode = 'RGBA'
    s.view_settings.view_transform = 'AgX' if 'AgX' in [i.identifier for i in s.view_settings.bl_rna.properties['view_transform'].enum_items] else 'Filmic'
    s.view_settings.look = 'None'
    s.view_settings.exposure = -0.2
    w = bpy.data.worlds.new('w'); s.world = w; w.use_nodes = True
    nt = w.node_tree; bg = nt.nodes['Background']
    # soft blue-grey sky fill; the sun does the real lighting
    bg.inputs[0].default_value = (0.55, 0.62, 0.72, 1); bg.inputs[1].default_value = 0.55
    sun = bpy.data.lights.new('sun', 'SUN'); sun.energy = 3.2; sun.angle = math.radians(6)
    sun.color = (1.0, 0.96, 0.9)
    so = bpy.data.objects.new('sun', sun); s.collection.objects.link(so)
    so.rotation_euler = (math.radians(48), 0, math.radians(150))
    # shadow catcher ground
    bpy.ops.mesh.primitive_plane_add(size=60, location=(0, 0, 0))
    g = bpy.context.object; g.is_shadow_catcher = True; g.name = 'ground'
    return s

MATS = {}
def mat(name, color, rough=0.6, metal=0.0, noise=0.0, dirt=0.0, spec=0.4):
    key = (name, color, rough, metal, noise, dirt)
    if key in MATS: return MATS[key]
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; p = nt.nodes['Principled BSDF']
    p.inputs['Roughness'].default_value = rough
    p.inputs['Metallic'].default_value = metal
    base = (*color, 1)
    if noise > 0 or dirt > 0:
        tex = nt.nodes.new('ShaderNodeTexNoise'); tex.inputs['Scale'].default_value = 28.0
        tex.inputs['Detail'].default_value = 12; tex.inputs['Roughness'].default_value = 0.62
        ramp = nt.nodes.new('ShaderNodeValToRGB')
        c = color
        dark = tuple(max(0, v * (1 - noise - dirt)) for v in c)
        light = tuple(min(1, v * (1 + noise * 0.6)) for v in c)
        ramp.color_ramp.elements[0].color = (*dark, 1)
        ramp.color_ramp.elements[1].color = (*light, 1)
        ramp.color_ramp.elements[0].position = 0.42
        ramp.color_ramp.elements[1].position = 0.58
        nt.links.new(tex.outputs['Fac'], ramp.inputs['Fac'])
        if dirt > 0:
            # darker toward the ground (dust and mud on lower panels)
            geo = nt.nodes.new('ShaderNodeNewGeometry')
            sep = nt.nodes.new('ShaderNodeSeparateXYZ')
            nt.links.new(geo.outputs['Position'], sep.inputs[0])
            mr = nt.nodes.new('ShaderNodeMapRange')
            mr.inputs['From Min'].default_value = 0.2; mr.inputs['From Max'].default_value = 1.4
            nt.links.new(sep.outputs['Z'], mr.inputs['Value'])
            mix = nt.nodes.new('ShaderNodeMixRGB'); mix.blend_type = 'MIX'
            mud = (0.16, 0.13, 0.09, 1)
            mix.inputs['Color1'].default_value = mud
            nt.links.new(mr.outputs['Result'], mix.inputs['Fac'])
            nt.links.new(ramp.outputs['Color'], mix.inputs['Color2'])
            out = mix.outputs['Color']
        else:
            out = ramp.outputs['Color']
        # worn, lighter paint on sharp edges (reads as real metal at icon size)
        geo2 = nt.nodes.new('ShaderNodeNewGeometry')
        mr2 = nt.nodes.new('ShaderNodeMapRange')
        mr2.inputs['From Min'].default_value = 0.52; mr2.inputs['From Max'].default_value = 0.6
        mr2.inputs['To Max'].default_value = 0.55
        nt.links.new(geo2.outputs['Pointiness'], mr2.inputs['Value'])
        wear = nt.nodes.new('ShaderNodeMixRGB'); wear.blend_type = 'SCREEN'
        nt.links.new(mr2.outputs['Result'], wear.inputs['Fac'])
        nt.links.new(out, wear.inputs['Color1'])
        wear.inputs['Color2'].default_value = (0.5, 0.48, 0.42, 1)
        nt.links.new(wear.outputs['Color'], p.inputs['Base Color'])
    else:
        p.inputs['Base Color'].default_value = base
    MATS[key] = m
    return m

def finish(o, m, bevel=0.04, seg=2):
    o.data.materials.append(m)
    if bevel > 0:
        b = o.modifiers.new('bev', 'BEVEL'); b.width = bevel; b.segments = seg
        b.limit_method = 'ANGLE'
    for f in o.data.polygons: f.use_smooth = True
    try:
        o.data.shade_smooth_by_angle(angle=math.radians(35))
    except Exception:
        try:
            o.data.use_auto_smooth = True; o.data.auto_smooth_angle = math.radians(35)
        except Exception:
            pass
    return o

def box(sx, sy, sz, loc, m, bevel=0.04, seg=2, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = bpy.context.object; o.scale = (sx, sy, sz)
    bpy.ops.object.transform_apply(scale=True)
    return finish(o, m, bevel, seg)

def cyl(r, depth, loc, m, axis='Y', verts=24, bevel=0.02):
    rot = {'X': (0, math.pi / 2, 0), 'Y': (math.pi / 2, 0, 0), 'Z': (0, 0, 0)}[axis]
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, vertices=verts, location=loc, rotation=rot)
    return finish(bpy.context.object, m, bevel, 2)

def prism_xz(profile, y0, y1, m, bevel=0.05):
    """Side profile in (x,z), extruded across y."""
    me = bpy.data.meshes.new('p'); bm = bmesh.new()
    a = [bm.verts.new((x, y0, z)) for x, z in profile]
    b = [bm.verts.new((x, y1, z)) for x, z in profile]
    bm.faces.new(a[::-1]); bm.faces.new(b)
    n = len(profile)
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new((a[i], a[j], b[j], b[i]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new('p', me); bpy.context.scene.collection.objects.link(o)
    return finish(o, m, bevel, 2)

def prism_xy(profile, z0, z1, m, bevel=0.05):
    """Top-down outline in (x,y), extruded up in z."""
    me = bpy.data.meshes.new('t'); bm = bmesh.new()
    a = [bm.verts.new((x, y, z0)) for x, y in profile]
    b = [bm.verts.new((x, y, z1)) for x, y in profile]
    bm.faces.new(a[::-1]); bm.faces.new(b)
    n = len(profile)
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new((a[i], a[j], b[j], b[i]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new('t', me); bpy.context.scene.collection.objects.link(o)
    return finish(o, m, bevel, 2)

# ---------- palettes ----------
PALETTE = {
    'green': dict(paint=(0.115, 0.13, 0.065), canvas=(0.17, 0.165, 0.10)),
    'tan':   dict(paint=(0.42, 0.33, 0.20),  canvas=(0.36, 0.30, 0.19)),
}

def common(side):
    P = PALETTE[side]
    return dict(
        paint=mat('paint_' + side, P['paint'], 0.55, 0.0, noise=0.12, dirt=0.25),
        canvas=mat('canvas_' + side, P['canvas'], 0.92, 0.0, noise=0.18, dirt=0.15),
        rubber=mat('rubber', (0.025, 0.025, 0.025), 0.85),
        metal=mat('metal', (0.06, 0.06, 0.055), 0.45, 0.7),
        glass=mat('glass', (0.03, 0.045, 0.06), 0.08, 0.0),
        steel=mat('steel', (0.35, 0.35, 0.33), 0.35, 0.9),
        light=mat('lamp', (0.9, 0.85, 0.6), 0.2),
    )

def wheel(x, y, z, r, w, M):
    cyl(r, w, (x, y, z), M['rubber'], 'Y', 32, 0.06)
    cyl(r * 0.55, w + 0.04, (x, y, z), M['paint'], 'Y', 20, 0.02)
    cyl(r * 0.18, w + 0.1, (x, y, z), M['metal'], 'Y', 12, 0.01)

# ---------- vehicles (meters; +X is forward) ----------
def truck(side):
    M = common(side)
    box(7.2, 1.2, 0.35, (0, 0, 1.0), M['metal'], 0.02)               # chassis rails
    box(1.9, 2.45, 1.75, (2.65, 0, 2.05), M['paint'], 0.09, 3)        # cab
    box(0.05, 2.0, 0.65, (3.61, 0, 2.45), M['glass'], 0.01)           # windscreen
    for y in (-1.235, 1.235):
        box(0.8, 0.04, 0.55, (2.85, y, 2.45), M['glass'], 0.01)       # side windows
        box(0.12, 0.12, 0.35, (3.5, y * 1.06, 2.5), M['metal'], 0.01) # mirrors
    box(0.25, 2.5, 0.35, (3.7, 0, 1.05), M['metal'], 0.03)            # bumper
    for y in (-0.85, 0.85):
        box(0.05, 0.28, 0.18, (3.83, y, 1.4), M['light'], 0.01)
    box(1.7, 0.9, 0.12, (2.65, 0, 2.98), M['paint'], 0.03)            # roof hatch
    box(4.7, 2.5, 0.55, (-0.95, 0, 1.55), M['paint'], 0.05)           # cargo bed
    box(4.6, 2.45, 1.45, (-0.95, 0, 2.5), M['canvas'], 0.32, 5)       # canvas cover
    for x in (-2.8, -1.6, -0.35, 0.9):                                # cover hoops
        box(0.08, 2.5, 0.06, (x, 0, 3.2), M['canvas'], 0.02)
    box(0.9, 0.5, 0.5, (0.9, 1.25, 1.05), M['metal'], 0.08)           # fuel tank
    box(0.7, 0.5, 0.6, (0.9, -1.2, 1.1), M['metal'], 0.05)            # tool box
    for x in (2.55, -0.85, -2.25):
        for y in (-1.08, 1.08):
            wheel(x, y, 0.58, 0.58, 0.45, M)
    return M

def tracks(x0, x1, y, width, M, h=1.0, wheels=5, skirt=None):
    prof = [(x0, 0.35), (x0 + 0.4, 0.02), (x1 - 0.4, 0.02), (x1, 0.4), (x1 - 0.15, h), (x0 + 0.15, h)]
    prism_xz(prof, y - width / 2, y + width / 2, M['rubber'], 0.08)
    step = (x1 - x0 - 1.0) / (wheels - 1)
    for i in range(wheels):
        x = x0 + 0.5 + i * step
        cyl(0.36, width + 0.06, (x, y, 0.42), M['paint'], 'Y', 24, 0.04)
        cyl(0.12, width + 0.12, (x, y, 0.42), M['metal'], 'Y', 10, 0.01)
    cyl(0.28, width + 0.04, (x1 - 0.25, y, 0.62), M['metal'], 'Y', 18, 0.03)
    if skirt:
        box(x1 - x0 - 0.6, 0.08, 0.55, (0.5 * (x0 + x1), y + (width / 2 + 0.05) * (1 if y > 0 else -1), 0.85), M['paint'], 0.03)

def apc(side):
    M = common(side)
    tracks(-2.5, 2.4, 1.18, 0.55, M, 1.0, 5)
    tracks(-2.5, 2.4, -1.18, 0.55, M, 1.0, 5)
    prof = [(-2.45, 0.55), (2.05, 0.55), (2.6, 1.15), (2.15, 2.15), (-2.45, 2.15)]
    prism_xz(prof, -1.42, 1.42, M['paint'], 0.06)
    box(0.12, 2.9, 0.12, (2.5, 0, 1.15), M['metal'], 0.02)
    box(0.9, 0.9, 0.3, (-0.3, 0.4, 2.3), M['paint'], 0.06)            # cupola base
    cyl(0.38, 0.35, (-0.3, 0.4, 2.55), M['paint'], 'Z', 20, 0.04)
    cyl(0.05, 1.4, (0.45, 0.4, 2.65), M['metal'], 'X', 10, 0.0)       # heavy MG
    box(0.35, 0.18, 0.22, (-0.05, 0.4, 2.65), M['metal'], 0.02)
    box(1.2, 1.1, 0.1, (-1.6, -0.3, 2.2), M['paint'], 0.03)           # rear hatch
    box(0.6, 0.35, 0.3, (1.3, -0.9, 2.25), M['canvas'], 0.1)          # stowage
    for y in (-1.0, 1.0):
        box(0.05, 0.22, 0.14, (2.58, y, 1.55), M['light'], 0.01)
    return M

def tank(side):
    M = common(side)
    tracks(-3.4, 3.4, 1.45, 0.7, M, 1.05, 7, skirt=True)
    tracks(-3.4, 3.4, -1.45, 0.7, M, 1.05, 7, skirt=True)
    prof = [(-3.4, 0.6), (3.0, 0.6), (3.65, 1.05), (3.15, 1.6), (-3.4, 1.6)]
    prism_xz(prof, -1.82, 1.82, M['paint'], 0.06)
    tur = [(-2.3, -1.45), (0.9, -1.6), (1.9, -0.75), (1.9, 0.75), (0.9, 1.6), (-2.3, 1.45)]
    prism_xy(tur, 1.6, 2.45, M['paint'], 0.07)
    top = [(-2.0, -1.2), (0.7, -1.3), (1.5, -0.6), (1.5, 0.6), (0.7, 1.3), (-2.0, 1.2)]
    prism_xy(top, 2.45, 2.55, M['paint'], 0.03)
    box(0.7, 0.9, 0.6, (2.05, 0, 2.05), M['paint'], 0.06)             # mantlet
    cyl(0.11, 5.2, (4.9, 0, 2.08), M['paint'], 'X', 20, 0.01)         # gun
    cyl(0.17, 1.0, (4.0, 0, 2.08), M['paint'], 'X', 20, 0.02)         # thermal sleeve
    cyl(0.14, 0.5, (7.3, 0, 2.08), M['metal'], 'X', 16, 0.02)         # muzzle
    cyl(0.32, 0.3, (-0.6, -0.65, 2.7), M['paint'], 'Z', 16, 0.03)     # commander hatch
    box(0.45, 0.35, 0.4, (-0.1, -0.7, 2.75), M['metal'], 0.04)        # sight
    cyl(0.04, 1.0, (-0.6, 0.7, 3.0), M['metal'], 'Z', 6, 0.0)         # antenna
    box(1.3, 2.7, 0.55, (-2.85, 0, 2.05), M['canvas'], 0.1)           # bustle rack
    box(0.4, 0.5, 0.18, (3.45, 1.2, 1.4), M['metal'], 0.02)
    return M

def howitzer(side):
    M = common(side)
    tracks(-3.0, 2.9, 1.42, 0.6, M, 1.0, 6)
    tracks(-3.0, 2.9, -1.42, 0.6, M, 1.0, 6)
    prof = [(-3.0, 0.55), (2.5, 0.55), (3.05, 1.05), (2.7, 1.55), (-3.0, 1.55)]
    prism_xz(prof, -1.7, 1.7, M['paint'], 0.06)
    box(3.6, 3.0, 1.45, (-0.9, 0, 2.3), M['paint'], 0.1, 3)           # big turret
    box(0.6, 1.1, 0.8, (1.1, 0, 2.15), M['paint'], 0.06)
    cyl(0.12, 5.6, (3.7, 0, 2.25), M['paint'], 'X', 18, 0.01)
    cyl(0.2, 0.7, (6.3, 0, 2.25), M['metal'], 'X', 16, 0.03)          # muzzle brake
    box(0.5, 0.5, 0.4, (-1.5, 1.0, 3.2), M['paint'], 0.04)
    cyl(0.04, 0.9, (-2.3, -1.0, 3.4), M['metal'], 'Z', 6, 0.0)
    box(1.0, 2.6, 0.5, (-3.0, 0, 1.9), M['canvas'], 0.1)
    return M


def ifv(side):
    """Infantry fighting vehicle: APC-like body but a real turret and long thin autocannon."""
    M = common(side)
    tracks(-2.9, 2.8, 1.35, 0.55, M, 1.0, 6, skirt=True)
    tracks(-2.9, 2.8, -1.35, 0.55, M, 1.0, 6, skirt=True)
    prof = [(-2.9, 0.55), (2.2, 0.55), (3.0, 1.0), (2.4, 1.85), (-2.9, 1.95)]
    prism_xz(prof, -1.7, 1.7, M['paint'], 0.06)
    tur = [(-0.9, -0.85), (0.6, -0.95), (1.1, -0.45), (1.1, 0.45), (0.6, 0.95), (-0.9, 0.85)]
    prism_xy(tur, 1.9, 2.55, M['paint'], 0.05)
    cyl(0.06, 3.0, (2.5, -0.2, 2.25), M['metal'], 'X', 12, 0.0)      # autocannon
    cyl(0.1, 0.6, (1.2, -0.2, 2.25), M['paint'], 'X', 12, 0.02)
    box(0.5, 0.3, 0.35, (0.2, 0.75, 2.75), M['paint'], 0.04)          # missile box
    box(0.35, 0.3, 0.3, (-0.3, -0.5, 2.7), M['metal'], 0.03)          # sight
    box(1.4, 1.2, 0.08, (-2.0, 0, 2.0), M['paint'], 0.02)             # rear door
    for y in (-1.25, 1.25):
        box(0.05, 0.22, 0.14, (2.95, y * 0.8, 1.25), M['light'], 0.01)
    return M

def spaa(side):
    """Air defence: tracked, tall boxy turret, big radar dish on a mast, twin guns."""
    M = common(side)
    tracks(-3.0, 2.9, 1.45, 0.6, M, 1.0, 6)
    tracks(-3.0, 2.9, -1.45, 0.6, M, 1.0, 6)
    prof = [(-3.0, 0.55), (2.5, 0.55), (3.1, 1.0), (2.7, 1.55), (-3.0, 1.55)]
    prism_xz(prof, -1.75, 1.75, M['paint'], 0.06)
    box(2.6, 2.4, 1.3, (-0.4, 0, 2.2), M['paint'], 0.08, 3)
    for y in (-1.45, 1.45):                                            # twin guns on the sides
        box(0.7, 0.35, 0.5, (0.6, y, 2.3), M['paint'], 0.04)
        cyl(0.07, 2.6, (2.1, y, 2.35), M['metal'], 'X', 12, 0.0)
    cyl(0.07, 1.4, (-1.3, 0, 3.5), M['metal'], 'Z', 10, 0.0)           # mast
    bpy.ops.mesh.primitive_cylinder_add(radius=0.95, depth=0.12, vertices=40, location=(-1.3, 0, 4.25), rotation=(0, math.radians(70), 0))
    finish(bpy.context.object, M['metal'], 0.02)                       # search radar dish
    box(0.6, 0.9, 0.5, (0.5, 0, 3.05), M['paint'], 0.05)               # tracking radar
    return M

def mlrs(side):
    """Rocket artillery: truck with a big tilted launcher box of rocket tubes."""
    M = common(side)
    box(7.6, 1.2, 0.35, (0, 0, 1.0), M['metal'], 0.02)
    box(1.9, 2.45, 1.6, (2.85, 0, 2.0), M['paint'], 0.1, 3)
    box(0.05, 2.0, 0.6, (3.82, 0, 2.35), M['glass'], 0.01)
    box(0.25, 2.5, 0.35, (3.9, 0, 1.05), M['metal'], 0.03)
    box(4.9, 2.4, 0.4, (-0.9, 0, 1.4), M['paint'], 0.04)               # flatbed
    pod = box(3.8, 2.2, 1.3, (-1.0, 0, 2.6), M['paint'], 0.06, rot=(0, math.radians(-14), 0))
    tube = mat('tube', (0.02, 0.02, 0.02), 0.9)
    for i in range(3):                                                  # tube mouths on the front face
        for j in range(5):
            y = -0.8 + j * 0.4; z = 2.25 + i * 0.36
            cyl(0.13, 0.08, (0.86, y, z + 0.47), tube, 'X', 12, 0.0)
    for x in (2.75, 0.4, -0.9, -2.2):
        for y in (-1.08, 1.08):
            wheel(x, y, 0.58, 0.58, 0.45, M)
    return M

def armored_car(side):
    """8x8 wheeled armour: low sharp hull, small turret, four big wheels a side."""
    M = common(side)
    prof = [(-3.1, 0.75), (2.6, 0.75), (3.3, 1.25), (2.8, 1.95), (-3.0, 2.0)]
    prism_xz(prof, -1.45, 1.45, M['paint'], 0.06)
    tur = [(-0.8, -0.8), (0.5, -0.85), (1.0, -0.4), (1.0, 0.4), (0.5, 0.85), (-0.8, 0.8)]
    prism_xy(tur, 2.0, 2.55, M['paint'], 0.05)
    cyl(0.07, 3.6, (2.7, 0, 2.3), M['paint'], 'X', 12, 0.0)
    cyl(0.04, 1.0, (-0.5, 0.6, 3.0), M['metal'], 'Z', 6, 0.0)
    for x in (2.1, 0.8, -1.0, -2.3):
        for y in (-1.42, 1.42):
            wheel(x, y, 0.6, 0.6, 0.5, M)
    box(0.9, 0.5, 0.35, (-2.2, 1.2, 2.15), M['canvas'], 0.08)
    return M

def facade(name, wall, win=(0.06, 0.07, 0.08), rows=6):
    """Wall colour with rows of dark windows (brick texture used as a window grid)."""
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; p = nt.nodes['Principled BSDF']
    p.inputs['Roughness'].default_value = 0.7
    tc = nt.nodes.new('ShaderNodeTexCoord')
    br = nt.nodes.new('ShaderNodeTexBrick')
    br.offset = 0.0
    br.inputs['Color1'].default_value = (*win, 1); br.inputs['Color2'].default_value = (*win, 1)
    br.inputs['Mortar'].default_value = (*wall, 1)
    br.inputs['Scale'].default_value = rows / 6.0
    br.inputs['Mortar Size'].default_value = 0.2
    br.inputs['Brick Width'].default_value = 0.5; br.inputs['Row Height'].default_value = 0.45
    nt.links.new(tc.outputs['Object'], br.inputs['Vector'])
    nt.links.new(br.outputs['Color'], p.inputs['Base Color'])
    return m

def city(seed=3, style='mid'):
    random.seed(seed)
    concrete = facade('concrete', (0.44, 0.43, 0.40))
    roof = mat('roof', (0.30, 0.31, 0.30), 0.8, 0, noise=0.15)
    glass = facade('cglass', (0.16, 0.2, 0.24), win=(0.05, 0.08, 0.1), rows=10)
    warm = facade('brick', (0.45, 0.35, 0.26))
    tree = mat('tree', (0.06, 0.12, 0.04), 0.9, 0, noise=0.3)
    road = mat('road', (0.09, 0.09, 0.09), 0.9)
    ground = mat('lot', (0.24, 0.25, 0.20), 0.95, 0, noise=0.2)
    cyl(9.5, 0.1, (0, 0, 0.05), ground, 'Z', 48, 0.0)
    for x in (-3.5, 3.5):
        box(0.9, 18, 0.06, (x, 0, 0.12), road, 0.0)
        box(18, 0.9, 0.06, (0, x, 0.12), road, 0.0)
    blocks = [(-7, -7), (0, -7), (7, -7), (-7, 0), (0, 0), (7, 0), (-7, 7), (0, 7), (7, 7)]
    for bx, by in blocks:
        if math.hypot(bx, by) > 9.5: continue
        for k in range(random.randint(2, 4)):
            w = random.uniform(1.4, 2.6); d = random.uniform(1.4, 2.6)
            cx = bx + random.uniform(-1.6, 1.6); cy = by + random.uniform(-1.6, 1.6)
            if math.hypot(cx, cy) > 8.6: continue
            centre = math.exp(-math.hypot(cx, cy) / 4.5)
            h = random.uniform(1.0, 2.5) + centre * random.uniform(2, 9 if style == 'big' else 5)
            m = random.choice([concrete, concrete, warm, glass]) if h > 4 else random.choice([concrete, warm])
            box(w, d, h, (cx, cy, 0.1 + h / 2), m, 0.05)
            box(w * 0.92, d * 0.92, 0.12, (cx, cy, 0.1 + h + 0.06), roof, 0.02)
            if random.random() < 0.4:
                box(w * 0.3, d * 0.3, 0.35, (cx, cy, 0.1 + h + 0.3), roof, 0.02)
    for i in range(26):
        a = random.uniform(0, 2 * math.pi); r = random.uniform(2, 9)
        x, y = r * math.cos(a), r * math.sin(a)
        bpy.ops.mesh.primitive_ico_sphere_add(radius=random.uniform(0.45, 0.8), subdivisions=2, location=(x, y, 0.7))
        finish(bpy.context.object, tree, 0)

# ---------- camera & render ----------
def frame_and_render(name, elev=34, azim=-38, margin=1.12):
    s = bpy.context.scene
    objs = [o for o in s.objects if o.type == 'MESH' and o.name != 'ground']
    cam_d = bpy.data.cameras.new('cam'); cam_d.type = 'ORTHO'
    cam = bpy.data.objects.new('cam', cam_d); s.collection.objects.link(cam); s.camera = cam
    e, a = math.radians(elev), math.radians(azim)
    dirv = Vector((math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)))
    bpy.context.view_layer.update()
    pts = []
    for o in objs:
        for c in o.bound_box:
            pts.append(o.matrix_world @ Vector(c))
    centre = sum(pts, Vector()) / len(pts)
    cam.location = centre + dirv * 60
    cam.rotation_euler = (-dirv).to_track_quat('-Z', 'Y').to_euler()
    bpy.context.view_layer.update()
    inv = cam.matrix_world.inverted()
    xs, ys = [], []
    for p in pts:
        q = inv @ p; xs.append(q.x); ys.append(q.y)
    span = max(max(xs) - min(xs), max(ys) - min(ys))
    cam_d.ortho_scale = span * margin
    # recentre on the projected box
    cx = (max(xs) + min(xs)) / 2; cy = (max(ys) + min(ys)) / 2
    cam.location = cam.matrix_world @ Vector((cx, cy, 0))
    s.render.filepath = os.path.join(OUT, name + '.png')
    bpy.ops.render.render(write_still=True)
    print('rendered', name)

JOBS = []
for side in ('green', 'tan'):
    JOBS += [('ifv_' + side, ifv, side), ('spaa_' + side, spaa, side),
             ('mlrs_' + side, mlrs, side), ('car_' + side, armored_car, side)]
    JOBS += [('truck_' + side, truck, side), ('apc_' + side, apc, side),
             ('tank_' + side, tank, side), ('arty_' + side, howitzer, side)]
only = os.environ.get('ONLY')
for name, fn, side in JOBS:
    if only and only not in name: continue
    reset(); MATS.clear(); fn(side); frame_and_render(name)
for i, style in enumerate(('mid', 'big')):
    if only and only != 'city': continue
    reset(); MATS.clear(); city(seed=7 + i, style=style); frame_and_render('city_' + style, elev=40, azim=-45, margin=1.02)
