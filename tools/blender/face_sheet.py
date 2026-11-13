"""Standard face review sheet: head views plus every expression shape key (same cameras for every version/candidate).
blender -b FILE.blend --python face_sheet.py -- --out DIR [--samples 64] [--head-frac 0.36]
--head-frac: share of the figure height that is head (0.36 for ~3-head stylised figures, ~0.14 for realistic adults).

Renders every visible mesh/curve object. Figure: metres, Z up, faces -Y, ~1.0 m tall.
Views: body_front, head_front, head_tq (3/4, figure's right side), head_side, head_high (3/4 from above), head_low (3/4 from below).
For each shape key whose name starts with "expr_" (on any object; keys with the same name on several objects are
driven together): head_front_<key>, head_tq_<key> at value 1.0, all other expr_ keys at 0.
"""
import bpy, sys, os, math, argparse
from mathutils import Vector

a = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
p = argparse.ArgumentParser()
p.add_argument("--out", required=True)
p.add_argument("--samples", type=int, default=64)
p.add_argument("--head-frac", type=float, default=0.36)
p.add_argument("--res", type=int, default=900)
a = p.parse_args(a)
os.makedirs(a.out, exist_ok=True)
sc = bpy.context.scene

objs = [o for o in sc.objects if o.type in {"MESH", "CURVE"} and not o.hide_render and o.visible_get()]
dg = bpy.context.evaluated_depsgraph_get()
pts = []
for o in objs:
    e = o.evaluated_get(dg)
    pts += [e.matrix_world @ Vector(c) for c in e.bound_box]
zmin = min(p.z for p in pts); zmax = max(p.z for p in pts); H = zmax - zmin
# head region from the main (largest) mesh's vertices
main = max((o for o in objs if o.type == "MESH"), key=lambda o: len(o.data.vertices))
me = main.evaluated_get(dg).to_mesh()
mw = main.matrix_world
hz = zmax - a.head_frac * H
hv = [mw @ v.co for v in me.vertices if (mw @ v.co).z > hz]
hx0, hx1 = min(v.x for v in hv), max(v.x for v in hv)
hy0, hy1 = min(v.y for v in hv), max(v.y for v in hv)
hz0, hz1 = min(v.z for v in hv), max(v.z for v in hv)
hc = Vector(((hx0 + hx1) / 2, (hy0 + hy1) / 2, (hz0 + hz1) / 2))
hsize = max(hx1 - hx0, hz1 - hz0)
main.evaluated_get(dg).to_mesh_clear()
print("HEAD centre", tuple(round(c, 3) for c in hc), "size", round(hsize, 3), "fig H", round(H, 3))

def _enable_gpu():
    """Enable OptiX (or CUDA) devices; falls back to CPU if none are found."""
    try:
        pr = bpy.context.preferences.addons["cycles"].preferences
        for t in ("OPTIX", "CUDA", "HIP", "METAL", "ONEAPI"):
            try:
                pr.compute_device_type = t
            except TypeError:
                continue
            pr.get_devices()
            if any(d.type == t for d in pr.devices):
                for d in pr.devices:
                    d.use = d.type == t
                print("Cycles device:", t)
                return "GPU"
    except Exception as ex:
        print("GPU setup failed:", ex)
    print("Cycles device: CPU")
    return "CPU"

try:
    sc.render.engine = "CYCLES"
except TypeError as e:
    print(e)
sc.cycles.device = _enable_gpu(); sc.cycles.samples = a.samples; sc.cycles.use_denoising = True
sc.render.film_transparent = False
sc.render.image_settings.file_format = "PNG"; sc.render.image_settings.color_mode = "RGB"
try:
    sc.view_settings.view_transform = "AgX"
except TypeError:
    pass
w = bpy.data.worlds.new("SheetWorld"); sc.world = w; w.use_nodes = True
bg = next(n for n in w.node_tree.nodes if n.type == "BACKGROUND")
bg.inputs[0].default_value = (0.62, 0.62, 0.64, 1); bg.inputs[1].default_value = 0.6
for o in [o for o in sc.objects if o.type == "LIGHT"]:
    o.hide_render = True


def area(name, loc, energy, size):
    ld = bpy.data.lights.new(name, "AREA"); ld.energy = energy; ld.size = size
    ob = bpy.data.objects.new(name, ld); sc.collection.objects.link(ob); ob.location = loc
    d = hc - Vector(loc); ob.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    return ob


area("Key", (hc.x - 1.2, hc.y - 1.6, hc.z + 1.0), 260, 1.2)
area("Fill", (hc.x + 1.4, hc.y - 1.0, hc.z + 0.2), 90, 1.6)
area("Rim", (hc.x + 0.3, hc.y + 1.6, hc.z + 0.9), 140, 1.0)

camd = bpy.data.cameras.new("SheetCam"); cam = bpy.data.objects.new("SheetCam", camd)
sc.collection.objects.link(cam); sc.camera = cam
camd.lens = 85


def shoot(name, target, az_deg, el_deg, dist, res=(a.res, a.res)):
    az, el = math.radians(az_deg), math.radians(el_deg)
    # az 0 = front (camera on -Y looking +Y); az > 0 moves the camera towards -X, i.e. the figure's right side
    off = Vector((-math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el), math.sin(el))) * dist
    cam.location = target + off
    cam.rotation_euler = (target - cam.location).to_track_quat("-Z", "Y").to_euler()
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.filepath = os.path.join(a.out, name + ".png")
    bpy.ops.render.render(write_still=True)
    print("WROTE", sc.render.filepath)


# distance so that the head (plus margin) fills ~80 % of the frame with an 85 mm lens (36 mm sensor)
fov = 2 * math.atan(18 / 85)
hd = (hsize * 1.35) / 2 / math.tan(fov / 2)
bd = (H * 1.12) / 2 / math.tan(fov / 2)

expr = {}
for o in objs:
    if o.type == "MESH" and o.data.shape_keys:
        for kb in o.data.shape_keys.key_blocks:
            if kb.name.startswith("expr_"):
                expr.setdefault(kb.name, []).append(kb)
print("EXPR", sorted(expr))


def set_expr(active=None):
    for k, kbs in expr.items():
        for kb in kbs:
            kb.value = 1.0 if k == active else 0.0


set_expr(None)
shoot("body_front", Vector((hc.x, hc.y, zmin + H / 2)), 0, 5, bd, (a.res * 2 // 3, a.res))
shoot("head_front", hc, 0, 3, hd)
shoot("head_tq", hc, 35, 6, hd)
shoot("head_side", hc, 90, 3, hd)
shoot("head_high", hc, 30, 32, hd)
shoot("head_low", hc, 25, -22, hd)
for k in sorted(expr):
    set_expr(k)
    shoot("head_front_" + k, hc, 0, 3, hd)
    shoot("head_tq_" + k, hc, 35, 6, hd)
set_expr(None)
print("DONE", a.out)
