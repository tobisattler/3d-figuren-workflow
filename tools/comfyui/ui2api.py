#!/usr/bin/env python3
"""Convert a ComfyUI UI-format workflow to API format, pruned to the ancestors of TARGET (needs a running server for /object_info).
usage: COMFY_URL=http://127.0.0.1:8190 python3 ui2api.py template_ui.json TARGET_NODE_ID out_api.json
We made workflows/pixal3d_mv_api_full.json from the ComfyUI template "3d_pixal3d_multi_views" with TARGET 372 (Save3DAdvanced).
Caveat: ImageCropV2 crop dicts are not converted; img23d.py bypasses those nodes."""
import json, sys, urllib.request
import os
SRV = os.environ.get("COMFY_URL", "http://127.0.0.1:8190")
UI = sys.argv[1]; TARGET = int(sys.argv[2]); OUT = sys.argv[3]
oi = json.load(urllib.request.urlopen(SRV + "/object_info", timeout=60))
w = json.load(open(UI))
nodes = {n["id"]: n for n in w["nodes"]}
links = {l[0]: l for l in w["links"]}
WIDGET_T = {"INT", "FLOAT", "STRING", "BOOLEAN", "COMBO", "COLOR", "LOAD_3D", "COMFY_DYNAMICCOMBO_V3"}

def widget_list(ntype):
    spec = oi[ntype]["input"]; out = []
    for sec in ("required", "optional"):
        for name, v in spec.get(sec, {}).items():
            t = v[0]; o = v[1] if len(v) > 1 and isinstance(v[1], dict) else {}
            if isinstance(t, list) or t in WIDGET_T:
                out.append((name, t, o))
    return out

keep = set(); stack = [TARGET]
while stack:
    nid = stack.pop()
    if nid in keep: continue
    keep.add(nid)
    for inp in nodes[nid].get("inputs", []):
        if inp.get("link") is not None: stack.append(links[inp["link"]][1])

api = {}
for nid in sorted(keep):
    n = nodes[nid]; t = n["type"]
    inputs = {}
    for inp in n.get("inputs", []):
        if inp.get("link") is not None:
            l = links[inp["link"]]; inputs[inp["name"]] = [str(l[1]), l[2]]
    vals = n.get("widgets_values") if isinstance(n.get("widgets_values"), list) else []
    i = 0
    def take():
        global i
        v = vals[i] if i < len(vals) else None; i += 1; return v
    def assign(prefix, name, typ, o):
        key = prefix + name
        if typ == "COMFY_DYNAMICCOMBO_V3":
            sel = take(); inputs.setdefault(key, sel)
            for opt in o.get("options", []):
                if opt["key"] == sel:
                    for sn, sv in opt["inputs"].get("required", {}).items():
                        st = sv[0]; so = sv[1] if len(sv) > 1 else {}
                        assign(key + ".", sn, st, so)
            return
        v = take()
        if key not in inputs: inputs[key] = v
        if o.get("control_after_generate") or (typ == "COMBO" and o.get("image_upload")): take()
    for name, typ, o in widget_list(t):
        assign("", name, typ, o)
    inputs.pop("viewport_state", None)
    api[str(nid)] = {"class_type": t, "inputs": {k: v for k, v in inputs.items() if v is not None}, "_meta": {"title": n.get("title") or t}}
json.dump(api, open(OUT, "w"), indent=1)
print(len(api), "nodes ->", OUT)
