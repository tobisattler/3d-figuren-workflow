# Setup

## Hardware, wie bei uns

- **Koordinator:** ein kleiner Linux-Container ohne GPU (4 Kerne, 8 GB RAM). Dort laufen Claude Code und die Fable-Subagenten.
- **GPU-Rechner:** 2× RTX 2080 Ti mit je 11 GB (Turing), per `ssh` erreichbar. Darauf laufen Pixal3D/ComfyUI und Blender 5.2.3 headless mit Cycles (OptiX).
  - Wir nutzen nur GPU 0. Die zweite GPU ist für einen parallelen Lauf da.

Alles auf einem Rechner mit NVIDIA-GPU geht genauso. Dann fällt das `ssh gpu …` vor den Befehlen weg. Mit einem getrennten GPU-Rechner schreibt man in die Aufträge, wie der Agent Befehle dort ausführt und Dateien hin- und zurückkopiert. Beispiele stehen in den Vorlagen in `briefs/`.

Speicher: Pixal3D braucht im Lauf 8,6–9,8 GB VRAM, die Modelle belegen etwa 9,3 GB Platte.

## 1. Claude Code

- Für die 3D-Runden braucht es Zugriff auf **Claude Fable 5.2** (Modell-Alias `fable`). Der Hauptagent kann ein beliebiges Modell sein, bei uns Opus 5.5.
- Subagenten startet der Hauptagent mit dem Agent-Werkzeug: Modell `fable`, Effort `xhigh`, im Hintergrund. Der Skill sagt ihm, dass er das so machen soll.
- **Skill einbinden:** `cp -r skills/3d-figuren-workflow ~/.claude/skills/` für alle Projekte, oder nach `.claude/skills/` im Projekt.

## 2. Blender-Skills (empfohlen)

Wir nutzen zusätzlich 29 öffentliche Blender-Skills, alle unter MIT, Stand 06.11.2026. Sie stammen aus diesen beiden Repos:

- https://github.com/EL4CTEO/blender-skills, Commit `fb92cfb`
- https://github.com/majidmanzarpour/blender-game-skills, Commit `f0ef293`

Die Unterordner mit `SKILL.md` kommen nach `~/.claude/skills/`. Davor bitte selbst prüfen, was drinsteht: Skills sind Anweisungen an den Agenten. Die Fable-Agenten nutzen davon vor allem `blender-core`, `blender-asset-qa`, `blender-character-rigging`, `blender-facial-shapekeys`, `blender-export-pipelines` und `blender-texturing`.

## 3. Blender 5.2.3

- Offizielles Linux-Archiv von blender.org, entpacken, fertig. Wir rufen es immer headless auf: `blender -b DATEI.blend --python skript.py -- args`.
- Für Cycles auf der GPU wählen die Skripte in `tools/blender/` OptiX bzw. CUDA selbst aus.
- Blenders Python hat kein scipy. Für Nachbarschaftssuchen nimmt man `mathutils.kdtree`.

Optional gibt es das **Blender-MCP** für eine sichtbare, live laufende Blender-Instanz: [ahujasid/blender-mcp](https://github.com/ahujasid/blender-mcp), bei uns Version 2.2.7. Die Fable-Läufe brauchen es nicht, sie arbeiten headless. Hinweise dazu:
- Die Abfrage „Contribute session data?“ ablehnen, sie blockiert sonst das Terminal (Escape lehnt ab).
- Telemetrie ausschalten.
- Die Cloud-Generatoren des Add-ons (Hyper3D, Sketchfab, Meshy, Tripo) haben wir nicht freigegeben.

## 4. ComfyUI + Pixal3D

```bash
COMFY_BASE=~/comfy tools/comfyui/install.sh
```

Das Skript macht dasselbe wie unsere Installation vom 06.11.2026:
- ComfyUI v0.44.1 (Commit `49b61c3`),
- ein venv mit `uv` und Python 3.12,
- torch 2.11.0 für CUDA 12.8,
- die Modelle von Hugging Face, beschrieben in der [Comfy-Doku zu Pixal3D](https://docs.comfy.org/tutorials/3d/pixal3d):

| Datei | Ordner | Größe | Quelle |
|---|---|---|---|
| `pixal3d_multiview_int8_convrot.safetensors` | `models/diffusion_models` | 5,58 GB | `Comfy-Org/Pixal3D` |
| `trellis_2_shape_vae_bf16.safetensors` | `models/vae` | 1,10 GB | `Comfy-Org/Pixal3D` |
| `trellis_2_texture_vae_bf16.safetensors` | `models/vae` | 0,95 GB | `Comfy-Org/Pixal3D` |
| `dino_v3_L_naf_fp32.safetensors` | `models/clip_vision` | 1,22 GB | `Comfy-Org/Pixal3D` |
| `birefnet.safetensors` | `models/background_removal` | 0,44 GB | `Comfy-Org/BiRefNet` |

Eigene Custom Nodes braucht es nicht, die Pixal3D- und Trellis2-Knoten sind in ComfyUI 0.44 eingebaut.

**Aufruf:**
```bash
export COMFY_BASE=~/comfy
python3 tools/img23d.py --views front.png side_left.png back.png --out figur.glb          # Seite blickt nach Bild-links
python3 tools/img23d.py --views ... --out figur.glb --dry-run                              # nur den API-Prompt schreiben
```
- `img23d.py` startet ein eigenes ComfyUI auf `127.0.0.1:8190+GPU`, schickt den Workflow, holt das GLB und beendet ComfyUI wieder.
- Mit `--keep-server` bleibt ComfyUI für mehrere Läufe hintereinander an.
- Wenn ein ComfyUI hängen bleibt: `pkill -f "main.py --listen 127.0.0.1 --port 8190"`.

**Standardwerte und was sie bedeuten:**
- `--res 1024`: das Comfy-Template nimmt 1536. Mit 1024 passt der Lauf sicher in 11 GB.
- `--faces 200000`
- `--tex 2048`: das Template nimmt 4096.

Mit diesen Werten liefert ein Lauf ein Mesh mit rund 200k Faces und drei 2048er-Texturen (BaseColor, Normal, ORM). Größere Werte für Gesichter, die nah gezeigt werden, haben wir auf 11 GB nicht getestet.

**Workflow neu erzeugen:** Das ist nötig, wenn sich das Comfy-Template ändert. Dazu das Template `3d_pixal3d_multi_views` in der ComfyUI-Oberfläche als JSON speichern und dann:
`COMFY_URL=http://127.0.0.1:8190 python3 tools/comfyui/ui2api.py template.json 372 tools/comfyui/workflows/pixal3d_mv_api_full.json`.
`img23d.py` verlässt sich auf die Knoten-IDs des Templates (324, 372, 94, 288, 186 und die Seeds 3/12/18/23). Nach einem Neuerzeugen also die IDs prüfen.

## 5. Bildgenerator

Wir nutzen Googles Gemini-Bildmodell **Nano Banana 2.1** über einen eigenen kleinen Dienst als MCP-Werkzeug. Ein 2K-Blatt im Format 16:9 kostet etwa 0,06 $, eine 4K-Bearbeitung etwa 0,13 $.

Jeder Generator, der ein oder mehrere **Referenzbilder** annimmt und Bilder bearbeiten kann, geht. Wichtig ist nur, dass das Ergebnis die Regeln aus [02-ablauf.md](02-ablauf.md#1-konzept-und-turnaround) einhält.

## 6. Viewer

`tools/viewer/index.html` ist eine einzelne Seite mit three.js 0.162 vom CDN.
- **Aufruf:** über einen beliebigen Webserver, zum Beispiel `python3 -m http.server`, dann `index.html?model=figur_web.glb`.
- **Funktionen:** drehen, alle Morph Targets als Regler, alle Animationen als Liste.
- Mit Meshopt komprimierte GLBs gehen auch.
