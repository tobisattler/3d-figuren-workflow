"""Review renders for a Pixal3D GLB (full body + head), Cycles GPU.
blender -b --python px_review.py -- MODEL.glb OUTDIR [nonorm] [--front -Y|+Y|-X|+X]
Figure assumed Z up after glTF import; 'front' = direction the face points (default -Y).
"""
import bpy, sys, os, math
from mathutils import Vector

a = sys.argv[sys.argv.index("--") + 1:]
glb, out = a[0], a[1]
nonorm = "nonorm" in a
front = "-Y"
if "--front" in a:
    front = a[a.index("--front") + 1]
os.makedirs(out, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=glb)
sc = bpy.context.scene
objs = [o for o in sc.objects if o.type == "MESH"]
dg = bpy.context.evaluated_depsgraph_get()

if nonorm:
    for o in objs:
        for slot in o.material_slots:
            m = slot.material
            if not m or not m.use_nodes:
                continue
            for n in m.node_tree.nodes:
                if n.type == "BSDF_PRINCIPLED":
                    for l in list(n.inputs["Normal"].links):
                        m.node_tree.links.remove(l)

V = []
for o in objs:
    e = o.evaluated_get(dg)
    me = e.to_mesh()
    V += [o.matrix_world @ v.co for v in me.vertices]
    e.to_mesh_clear()
zmin = min(v.z for v in V); zmax = max(v.z for v in V); H = zmax - zmin
xs = [v.x for v in V]; ys = [v.y for v in V]
cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
band = [v for v in V if v.z > zmax - 0.12 * H]
hx = sum(v.x for v in band) / len(band); hy = sum(v.y for v in band) / len(band)
hz = zmax - 0.068 * H
print("BBOX H=%.4f center=(%.4f,%.4f) head=(%.4f,%.4f,%.4f) verts=%d" % (H, cx, cy, hx, hy, hz, len(V)))

# front direction -> azimuth 0
base = {"-Y": -math.pi / 2, "+Y": math.pi / 2, "-X": math.pi, "+X": 0.0}[front]

# render setup
sc.render.engine = "CYCLES"
try:
    pr = bpy.context.preferences.addons["cycles"].preferences
    for t in ("OPTIX", "CUDA"):
        try:
            pr.compute_device_type = t
            pr.get_devices()
            if any(d.type == t for d in pr.devices):
                for d in pr.devices:
                    d.use = d.type == t
                break
        except TypeError:
            pass
    sc.cycles.device = "GPU"
except Exception as ex:
    print("GPU setup failed", ex)
sc.cycles.samples = 48
sc.cycles.use_denoising = True
try:
    sc.view_settings.view_transform = "Standard"
except TypeError:
    pass
sc.render.film_transparent = False
w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True
bg = next(n for n in w.node_tree.nodes if n.type == "BACKGROUND")
bg.inputs[0].default_value = (0.8, 0.8, 0.8, 1); bg.inputs[1].default_value = 0.5

sun_d = bpy.data.lights.new("key", "SUN"); sun_d.energy = 1.6; sun_d.angle = math.radians(12)
sun = bpy.data.objects.new("key", sun_d); sc.collection.objects.link(sun)
cam_d = bpy.data.cameras.new("cam"); cam_d.lens = 85; cam_d.sensor_fit = "VERTICAL"; cam_d.sensor_height = 36
cam = bpy.data.objects.new("cam", cam_d); sc.collection.objects.link(cam); sc.camera = cam

def shoot(name, target, az_deg, el_deg, frame_h, rx, ry):
    sc.render.resolution_x, sc.render.resolution_y = rx, ry
    az = base + math.radians(az_deg); el = math.radians(el_deg)
    d = frame_h / (2 * math.tan(math.atan(18 / 85)))
    dirv = Vector((math.cos(az) * math.cos(el), math.sin(az) * math.cos(el), math.sin(el)))
    cam.location = target + dirv * d
    cam.rotation_euler = (target - cam.location).to_track_quat("-Z", "Y").to_euler()
    # key light from camera-left, above
    kaz = az + math.radians(35); kel = math.radians(35)
    kd = Vector((math.cos(kaz) * math.cos(kel), math.sin(kaz) * math.cos(kel), math.sin(kel)))
    sun.rotation_euler = (-kd).to_track_quat("-Z", "Y").to_euler()
    sc.render.filepath = os.path.join(out, name + ".png")
    bpy.ops.render.render(write_still=True)

body = Vector((cx, cy, zmin + H / 2)); head = Vector((hx, hy, hz))
# azimuth: 0 = front, +90 = figure's left side seen from its left (camera at figure's left)
for nm, az in [("full_front", 0), ("full_fl45", 45), ("full_left", 90), ("full_bl135", 135), ("full_back", 180),
               ("full_br225", 225), ("full_right", 270), ("full_fr315", 315)]:
    shoot(nm, body, az, 0, H * 1.08, 750, 1000)
shoot("full_top_fl", body, 30, 30, H * 1.12, 750, 1000)
for nm, az in [("head_front", 0), ("head_fl45", 45), ("head_left", 90), ("head_back", 180), ("head_right", 270), ("head_fr315", 315)]:
    shoot(nm, head, az, 4, H * 0.19, 800, 800)
shoot("head_top", head, 20, 55, H * 0.2, 800, 800)
print("DONE", out)
