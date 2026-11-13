"""Web export for the three.js viewer: deform skeleton RIG_Sid_Game only, shape keys (at 0), the four actions baked from the
control rig as separate glTF animations, meshopt + WebP.   (extends export_glb_v4_vorlage.py)
blender -b sid_rig_v1.blend --python scripts/export_glb.py -- --out exports/sid_rig_v1_web.glb [--no-meshopt] [--dump tmp/export_check.npz]
Nothing is saved back to the .blend: baking, removing the control rig and muting constraints happen in this session only."""
import bpy, sys, os, json, numpy as np
from mathutils import Matrix
from bpy_extras import anim_utils
argv = sys.argv[sys.argv.index("--") + 1:]
out = os.path.abspath(argv[argv.index("--out") + 1]); os.makedirs(os.path.dirname(out), exist_ok=True)
ACTIONS = ["qa_poses", "anim_idle", "anim_walk", "anim_wave"]
rig = bpy.data.objects["RIG_Sid"]; gs = bpy.data.objects["RIG_Sid_Game"]; sc = bpy.context.scene
# shape keys to 0 (rest = neutral), as in the template
for ob in bpy.data.objects:
    if ob.type == "MESH" and ob.data.shape_keys:
        for kb in ob.data.shape_keys.key_blocks[1:]: kb.value = 0.0
# ---- 1. sample the game skeleton while the control rig plays each action
bones = [b.name for b in gs.data.bones]                       # parents come before children
rest = {b.name: b.matrix_local.copy() for b in gs.data.bones}; parent = {b.name: (b.parent.name if b.parent else None) for b in gs.data.bones}
samples = {}; check = {}
for an in ACTIONS:
    act = bpy.data.actions[an]; rig.animation_data_create(); rig.animation_data.action = act; rig.animation_data.action_slot = act.slots[0]
    f0, f1 = int(round(act.frame_range[0])), int(round(act.frame_range[1])); frames = list(range(f0, f1 + 1))
    data = np.zeros((len(frames), len(bones), 10))
    for fi, f in enumerate(frames):
        sc.frame_set(f)
        pm = {n: gs.pose.bones[n].matrix.copy() for n in bones}
        for bi, n in enumerate(bones):
            p = parent[n]
            lrest = rest[p].inverted() @ rest[n] if p else rest[n]
            lpose = pm[p].inverted() @ pm[n] if p else pm[n]
            loc, rot, scl = (lrest.inverted() @ lpose).decompose()
            data[fi, bi] = (*loc, *rot, *scl)
    for bi in range(len(bones)):                                # quaternion continuity
        q = data[:, bi, 3:7]
        for i in range(1, len(q)):
            if np.dot(q[i], q[i - 1]) < 0: q[i] = -q[i]
    samples[an] = (frames, data)
    print("sampled", an, "frames", f0, f1, "max |scale-1| %.5f" % np.abs(data[:, :, 7:] - 1).max(), "max |loc| of non-root/hips bones %.5f m" % np.abs(data[:, 2:, 0:3]).max())
# ---- 2. the game skeleton stands alone: drop its constraints, the control rig, the metarig and the widgets
rig.animation_data.action = None
for pb in gs.pose.bones:
    for c in list(pb.constraints): pb.constraints.remove(c)
    pb.rotation_mode = "QUATERNION"; pb.matrix_basis = Matrix.Identity(4)
for o in [o for o in bpy.data.objects if o.name.startswith(("WGT-", "RIG_Sid_Meta")) or o is rig]: bpy.data.objects.remove(o)
for a in [a for a in bpy.data.actions]: bpy.data.actions.remove(a)
# ---- 3. baked actions (same names), one slot for the game skeleton, one muted NLA track each
gs.animation_data_create()
for an in ACTIONS:
    frames, data = samples[an]; n = len(frames)
    act = bpy.data.actions.new(an); act.use_fake_user = True; slot = act.slots.new(id_type="OBJECT", name=gs.name)
    cb = anim_utils.action_ensure_channelbag_for_slot(act, slot)
    fr = np.array(frames, float)
    for bi, bn in enumerate(bones):
        base = 'pose.bones["%s"].' % bn
        for path, c0, cn, default in (("location", 0, 3, 0.0), ("rotation_quaternion", 3, 4, None), ("scale", 7, 3, 1.0)):
            vals = data[:, bi, c0:c0 + cn]
            if path == "scale":
                if np.abs(vals - 1).max() > 2e-3: print("WARNING scale animation on", bn, "in", an, "max dev %.4f" % np.abs(vals - 1).max())
                else: continue
            if path == "location" and np.abs(vals).max() < 1e-6: continue
            for i in range(cn):
                fc = cb.fcurves.new(base + path, index=i, group_name=bn); fc.keyframe_points.add(n)
                co = np.empty(n * 2); co[0::2] = fr; co[1::2] = vals[:, i]; fc.keyframe_points.foreach_set("co", co)
                fc.keyframe_points.foreach_set("interpolation", [1] * n); fc.update()
    act.frame_start = frames[0]; act.frame_end = frames[-1]; act.use_frame_range = True
    tr = gs.animation_data.nla_tracks.new(); tr.name = an; st = tr.strips.new(an, frames[0], act); st.name = an
    try: st.action_slot = slot
    except Exception as ex: print("strip slot", ex)
    tr.mute = True
    gs.animation_data.action = act; gs.animation_data.action_slot = slot
    if "--dump" in argv:                                        # reference positions for the re-import check
        for f in (frames[len(frames) // 3], frames[-1 - len(frames) // 4]):
            sc.frame_set(f); dg = bpy.context.evaluated_depsgraph_get()
            for on in ("CH_Sid", "CH_Sid_Mouth", "CH_Sid_Headphones_Band"):
                ev = bpy.data.objects[on].evaluated_get(dg); me = ev.to_mesh(); c = np.empty(len(me.vertices) * 3); me.vertices.foreach_get("co", c)
                check["%s|%d|%s" % (an, f, on)] = (np.array(ev.matrix_world) @ np.c_[c.reshape(-1, 3), np.ones(len(me.vertices))].T).T[:, :3].astype(np.float32); ev.to_mesh_clear()
gs.animation_data.action = None
for pb in gs.pose.bones: pb.matrix_basis = Matrix.Identity(4)
sc.frame_set(1)
if "--dump" in argv:
    dp = os.path.abspath(argv[argv.index("--dump") + 1]); os.makedirs(os.path.dirname(dp), exist_ok=True); np.savez_compressed(dp, **check); print("dumped check positions", dp, len(check))
# ---- 4. export
# The exporter's meshopt bridge packs animation rotations with an 8-bit quaternion filter (about 1.3 deg error per bone, up to 6 mm at the
# finger tips, visible as stepping in slow motion). 16 bits is the full precision of the same encoding; the decoder does not change.
import importlib
mo = importlib.import_module("io_scene_gltf2.io.exp.meshopt"); print("meshopt filter bits: quat", mo.QUAT_FILTER_BITS, "-> 16, exp", mo.EXP_FILTER_BITS, "oct", mo.OCT_FILTER_BITS)
mo.QUAT_FILTER_BITS = 16
props = {p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
kw = dict(filepath=out, export_format="GLB", use_selection=False, export_apply=False, export_morph=True, export_morph_normal=False, export_yup=True,
          export_animations=True, export_animation_mode="ACTIONS", export_force_sampling=True, export_frame_range=False, export_anim_slide_to_zero=True,
          export_morph_animation=False,
          export_skins=True, export_def_bones=True, export_all_influences=False, export_optimize_animation_size=True,
          export_optimize_animation_keep_anim_armature=True, export_anim_single_armature=True, export_reset_pose_bones=True, export_rest_position_armature=True,
          export_try_sparse_sk=True, export_image_format="WEBP", export_image_quality=85, export_shared_accessors=True,
          export_vertex_color="MATERIAL", export_all_vertex_colors=False, export_extras=False, export_cameras=False, export_lights=False)
if "--no-meshopt" not in argv: kw["export_meshopt_compression_enable"] = True
kw = {k: v for k, v in kw.items() if k in props or k == "filepath"}
print("EXPORT kw", {k: v for k, v in kw.items() if k != "filepath"})
bpy.ops.export_scene.gltf(**kw)
print("SIZE", os.path.getsize(out))
