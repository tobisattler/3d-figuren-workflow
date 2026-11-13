"""Whole-figure review sheet (same cameras for every version, so before/after pairs line up).
blender -b FILE.blend --python body_sheet.py -- --out DIR [--samples 64] [--res 1000] [--only name1,name2] [--head-frac 0.36]
--head-frac: share of the figure height that is head (0.36 for ~3-head stylised figures, ~0.14 for realistic adults).

Renders every visible mesh/curve object. Figure: metres, Z up, faces -Y, ~1.0 m tall, A-pose.
Regions are derived from the figure's bounding box and the main (largest) mesh, so the cameras are the same for
every version as long as the figure itself does not move.
Light rig follows the camera azimuth (key front-left of the camera, fill right, rim behind), so back views are lit too.
Views: full_* (8), torso_* (5), hand_{R,L}_* (4 each), feet_* (4), legs_* (2), hair_* (4)  = 31 images.
"""
import bpy, sys, os, math, argparse
from mathutils import Vector

a = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
p = argparse.ArgumentParser()
p.add_argument("--out", required=True)
p.add_argument("--samples", type=int, default=64)
p.add_argument("--res", type=int, default=1000)
p.add_argument("--only", default="")
p.add_argument("--head-frac", type=float, default=0.36)
a = p.parse_args(a)
only = set(s for s in a.only.split(",") if s)
os.makedirs(a.out, exist_ok=True)
sc = bpy.context.scene

objs = [o for o in sc.objects if o.type in {"MESH", "CURVE"} and not o.hide_render and o.visible_get()]
dg = bpy.context.evaluated_depsgraph_get()
pts = []
for o in objs:
    e = o.evaluated_get(dg)
    pts += [e.matrix_world @ Vector(c) for c in e.bound_box]
x0 = min(q.x for q in pts); x1 = max(q.x for q in pts)
y0 = min(q.y for q in pts); y1 = max(q.y for q in pts)
zmin = min(q.z for q in pts); zmax = max(q.z for q in pts); H = zmax - zmin
cx, cy = (x0 + x1) / 2, (y0 + y1) / 2

main = max((o for o in objs if o.type == "MESH"), key=lambda o: len(o.data.vertices))
me = main.evaluated_get(dg).to_mesh()
mw = main.matrix_world
V = [mw @ v.co for v in me.vertices]
main.evaluated_get(dg).to_mesh_clear()


def centre(vs):
    n = max(len(vs), 1)
    return Vector((sum(v.x for v in vs) / n, sum(v.y for v in vs) / n, sum(v.z for v in vs) / n))


xr = max(abs(min(v.x for v in V) - cx), abs(max(v.x for v in V) - cx))
# hands: outermost 6 % of the half-width on each side (A-pose); feet: lowest 7 % of the height, split by side
HAND = {"R": centre([v for v in V if v.x < cx - 0.94 * xr]), "L": centre([v for v in V if v.x > cx + 0.94 * xr])}
HAND = {k: centre([v for v in V if (v - c).length < 0.07]) for k, c in HAND.items()}
feet = [v for v in V if v.z < zmin + 0.07 * H]
FEET = centre(feet)
FEET.z = zmin + 0.06 * H
TORSO = Vector((cx, cy, zmin + 0.47 * H))
LEGS = Vector((cx, cy, zmin + 0.22 * H))
head = [v for v in V if v.z > zmax - a.head_frac * H]
HEAD = centre(head)
HAIR = Vector((HEAD.x, HEAD.y, zmax - 0.14 * H))
print("FIG H", round(H, 3), "HAND", {k: tuple(round(c, 3) for c in v) for k, v in HAND.items()},
      "FEET", tuple(round(c, 3) for c in FEET), "HEAD", tuple(round(c, 3) for c in HEAD))

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
w = bpy.data.worlds.new("BodySheetWorld"); sc.world = w; w.use_nodes = True
bg = next(n for n in w.node_tree.nodes if n.type == "BACKGROUND")
bg.inputs[0].default_value = (0.62, 0.62, 0.64, 1); bg.inputs[1].default_value = 0.6
for o in [o for o in sc.objects if o.type == "LIGHT"]:
    o.hide_render = True


def mklight(name, energy, size):
    ld = bpy.data.lights.new(name, "AREA"); ld.energy = energy; ld.size = size
    ob = bpy.data.objects.new(name, ld); sc.collection.objects.link(ob)
    return ob


KEY, FILL, RIM = mklight("BKey", 260, 1.2), mklight("BFill", 90, 1.6), mklight("BRim", 140, 1.0)


def place_lights(target, az_deg, scale):
    # offsets defined for az = 0 (camera on -Y), rotated with the camera azimuth about Z
    az = math.radians(az_deg)
    rot = lambda v: Vector((v.x * math.cos(az) + v.y * math.sin(az), -v.x * math.sin(az) + v.y * math.cos(az), v.z))
    for ob, off, e in ((KEY, Vector((-1.2, -1.6, 1.0)), 260), (FILL, Vector((1.4, -1.0, 0.2)), 90),
                       (RIM, Vector((0.3, 1.6, 0.9)), 140)):
        ob.location = target + rot(off) * scale
        ob.rotation_euler = (target - ob.location).to_track_quat("-Z", "Y").to_euler()
        ob.data.energy = e * scale * scale


camd = bpy.data.cameras.new("BodySheetCam"); cam = bpy.data.objects.new("BodySheetCam", camd)
sc.collection.objects.link(cam); sc.camera = cam
camd.lens = 85
fov = 2 * math.atan(18 / 85)


def dist_for(extent):
    return (extent * 1.12) / 2 / math.tan(fov / 2)


def shoot(name, target, az_deg, el_deg, extent, light_scale=1.0):
    if only and name not in only:
        return
    az, el = math.radians(az_deg), math.radians(el_deg)
    # az 0 = front (camera on -Y looking +Y); az > 0 moves the camera towards -X, i.e. the figure's right side
    d = dist_for(extent)
    off = Vector((-math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el), math.sin(el))) * d
    cam.location = target + off
    cam.rotation_euler = (target - cam.location).to_track_quat("-Z", "Y").to_euler()
    camd.clip_start = 0.01
    place_lights(target, az_deg, light_scale)
    sc.render.resolution_x = sc.render.resolution_y = a.res
    sc.render.filepath = os.path.join(a.out, name + ".png")
    bpy.ops.render.render(write_still=True)
    print("WROTE", sc.render.filepath)


FULL = Vector((cx, cy, zmin + H / 2))
for nm, az, el in (("front", 0, 4), ("back", 180, 4), ("side_R", 90, 0), ("side_L", -90, 0), ("tq_R", 40, 8),
                   ("tq_L", -40, 8), ("tq_back_R", 140, 8), ("high", 25, 40)):
    shoot("full_" + nm, FULL, az, el, H * 1.02)
for nm, az, el in (("front", 0, 4), ("back", 180, 4), ("tq_R", 40, 6), ("tq_L", -40, 6), ("side_R", 90, 0)):
    shoot("torso_" + nm, TORSO, az, el, 0.50 * H, 0.8)
for side, sgn in (("R", 1), ("L", -1)):
    for nm, az, el, ext in (("front", 0, 5, 0.26), ("back", 180, 5, 0.26), ("top", sgn * 20, 55, 0.32),
                            ("under", sgn * 20, -40, 0.32)):
        shoot(f"hand_{side}_{nm}", HAND[side], az, el, ext * H, 0.5)
for nm, az, el in (("front", 0, 12), ("back", 180, 12), ("tq_R", 40, 18), ("side_R", 90, 4)):
    shoot("feet_" + nm, FEET, az, el, 0.44 * H, 0.6)
for nm, az, el in (("front", 0, 4), ("back", 180, 4)):
    shoot("legs_" + nm, LEGS, az, el, 0.36 * H, 0.7)
for nm, az, el in (("top", 0, 70), ("back", 180, 15), ("tq_back_R", 135, 20), ("tq_back_L", -135, 20)):
    shoot("hair_" + nm, HAIR, az, el, 0.52 * H, 0.7)
print("DONE", a.out)
