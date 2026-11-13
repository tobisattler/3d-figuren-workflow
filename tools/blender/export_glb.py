"""GLB export for the web (three.js) and Godot, with the settings that worked for our figures.
blender -b FIGUR.blend --python export_glb.py -- --out figur_web.glb [--meshopt] [--anim] [--morph-normals]

- All shape keys are set to 0 first, so the exported rest pose is neutral (the .blend is not saved).
- Textures as WebP (quality 85), sparse shape keys, shared accessors.
- --meshopt: EXT_meshopt_compression (three.js needs MeshoptDecoder). Caveat: positions are quantised, so layered
  surfaces closer than about 0.5 mm (an iris over the eye white) can z-fight; export such models without --meshopt.
- --anim: export all actions as separate glTF animations. With --meshopt the exporter packs rotations with an 8-bit
  quaternion filter (about 1.3-1.7 degrees per bone, ~6 mm at the fingertips); we raise it to 16 bit, same decoder.
- Figures rigged with a control rig (Rigify) need the deform skeleton baked first: see examples/sid_rig/export_glb_sid.py.
"""
import bpy, os, sys, importlib
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
out = os.path.abspath(argv[argv.index("--out") + 1]) if "--out" in argv else os.path.abspath("figur_web.glb")
os.makedirs(os.path.dirname(out), exist_ok=True)
for ob in bpy.data.objects:
    if ob.type == "MESH" and ob.data.shape_keys:
        for kb in ob.data.shape_keys.key_blocks[1:]:
            kb.value = 0.0
anim = "--anim" in argv
props = {p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
kw = dict(filepath=out, export_format="GLB", use_selection=False, export_apply=False, export_yup=True,
          export_morph=True, export_morph_normal="--morph-normals" in argv, export_try_sparse_sk=True,
          export_image_format="WEBP", export_image_quality=85, export_shared_accessors=True,
          export_vertex_color="MATERIAL", export_all_vertex_colors=False, export_cameras=False, export_lights=False,
          export_animations=anim)
if anim:
    kw.update(export_animation_mode="ACTIONS", export_force_sampling=True, export_anim_slide_to_zero=True,
              export_morph_animation=False, export_skins=True, export_def_bones=True, export_all_influences=False,
              export_reset_pose_bones=True, export_rest_position_armature=True)
if "--meshopt" in argv:
    kw["export_meshopt_compression_enable"] = True
    try:
        mo = importlib.import_module("io_scene_gltf2.io.exp.meshopt")
        print("meshopt quaternion filter bits", mo.QUAT_FILTER_BITS, "-> 16"); mo.QUAT_FILTER_BITS = 16
    except Exception as ex:
        print("could not raise QUAT_FILTER_BITS:", ex)
kw = {k: v for k, v in kw.items() if k in props or k == "filepath"}
print("EXPORT", {k: v for k, v in kw.items() if k != "filepath"})
bpy.ops.export_scene.gltf(**kw)
print("SIZE", os.path.getsize(out), out)
