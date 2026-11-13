---
name: 3d-figuren-workflow
description: Use when turning a concept image or turnaround into an animatable 3D game character (GLB) - image generator turnaround, Pixal3D multi-view via ComfyUI (img23d.py), Fable 5.2 xhigh subagents in headless Blender for face, accessories, clean-up and rig, fixed review sheets, GLB export for three.js/Godot. Includes the proven pitfalls (Pixal3D side slots / Janus face, normal-map cracks, fused accessories and fingers, meshopt precision).
---

# 3D-Figuren-Workflow (erprobt im November 2026)

Das Repo „3d-figuren-workflow“ (https://github.com/tobisattler/3d-figuren-workflow) enthält Skripte, Auftragsvorlagen und Doku. Den Pfad zum Checkout als `$WF` merken, zum Beispiel `~/3d-figuren-workflow`. Ist er unbekannt, frag den Nutzer.

- Ausführlich: `$WF/docs/02-ablauf.md`
- Aufträge: `$WF/briefs/`
- Stolperfallen: `$WF/docs/04-lehren.md`

## Deine Rolle: Koordinator

Die 3D-Arbeit machen **Fable-5.2-Subagenten**: Agent-Werkzeug mit `model: "fable"`, `effort: "xhigh"`, `run_in_background: true`. Der Nutzer hat das mit diesem Skill so angeordnet. Effort high oder medium nur, wenn er ausdrücklich Tempo oder ein kleineres Budget will.

Du selbst:
- schreibst die Aufträge aus den Vorlagen,
- legst Arbeitskopien und schreibgeschützte Checkpoints an,
- siehst Prüfblätter und Vorher/Nachher selbst an, bevor der Nutzer sie sieht,
- prüfst Zahlen, Dateien und die tatsächliche Laufzeit nach,
- zeigst ehrlich auch die Schwächen,
- machst Routinearbeit wie Turnaround, Pixal3D-Aufruf, Export und Viewer selbst.

## Ablauf

1. **Turnaround** (`$WF/briefs/01_turnaround_prompt.md`):
   - Blatt mit vorne | Seite **mit Blick nach Bild-links** | hinten, 16:9, 2K.
   - Gleicher Maßstab, Scheitel und Sohlen auf denselben Zeilen, A-Pose, Hände leer, hellgrauer Hintergrund, weiches Licht.
   - Referenz: das Konzeptbild. Driften die Proportionen, kommt ein abgenommenes Blatt als zweite Referenz dazu.
   - Zerlegen mit `python3 $WF/tools/split_turnaround.py blatt.png out name`.
2. **Pixal3D:**
   - Aufruf: `python3 $WF/tools/img23d.py --views name_front.png name_side_left.png name_back.png --side-faces left --out name_px.glb` (2–4 min, ~9–10 GB VRAM).
   - Danach prüfen mit `blender -b --python $WF/tools/blender/px_review.py -- name_px.glb review/`, einmal mit und einmal mit `nonorm` als drittem Argument.
3. **Ins .blend:** Meter, Z oben, Blick nach −Y, Ursprung am Boden. Dann schreibgeschützt als Checkpoint v0 ablegen.
4. **Fable-Runden, je ein Thema pro Runde:**
   - Gesicht: `02_gesicht.md`
   - Accessoires als eigene Objekte: `03_accessoires.md`
   - Aufräumen: `04_aufraeumen.md`
   - Rig mit Prüfposen und Testanimationen: `05_rig.md`

   Nach jeder abgenommenen Runde: `checkpoints/vN` schreibgeschützt anlegen, der nächste Auftrag startet mit einer Kopie davon.
5. **Export und Viewer:**
   - `blender -b figur.blend --python $WF/tools/blender/export_glb.py -- --out figur_web.glb --meshopt [--anim]`
   - Mit Steuer-Rig vorher backen, siehe `$WF/examples/sid_rig/export_glb_sid.py`.
   - Viewer: `$WF/tools/viewer/index.html?model=…`

## Aufträge schreiben

- **Vier Teile:**
  - Ausgangslage: Datei, Checkpoint, Konventionen, Notizen früherer Runden.
  - Ziel: was sich ändert, was bleibt, die Maßstäbe des Nutzers wörtlich.
  - Arbeitsweise: Blender-Aufruf, GPU, Lese- und Schreibrechte, Verbote, Skills, Zeitrahmen.
  - Abgabe: .blend, Prüfblätter mit exaktem Befehl, `compare/NN_*.png`, `notizen.md`.
- **Nicht vorschreibend:** was und woran gemessen, nicht wie.
- **Verboten in Modellier-Runden:** Internet, Generatoren, die Live-Blender-Instanz eines Menschen.
- **Zusatzinfos an einen laufenden Agenten** per SendMessage.

## Prüfen

- **Feste Prüfblätter** mit `$WF/tools/blender/face_sheet.py` und `body_sheet.py`. `--head-frac` ist 0,36 für Figuren mit ~3 Köpfen und 0,14 für realistische.
- **Immer auch schräg:** ¾ vorne, ¾ hinten, von oben, von unten. Dazu Zahlen-Checks: nicht-mannigfaltige Kanten, lose Teile, Normalen, Maßstab, Abstände in allen Ausdrücken.
- **Scores** (Silhouetten-IoU, DINO) reichen nur für grobe Abstände. Die feinen entscheidet der Nutzer im Viewer. Bleibt der Score stehen, Methode wechseln.

## Stolperfallen (alle selbst erlebt)

- **Pixal3D-Slots:**
  - `left` = Blick nach **Bild-links**. Falsch belegt, oder ohne Rückansicht, gibt es ein Doppelgesicht am Hinterkopf.
  - Abhilfe: `--swap-sides`.
- **Generator-Mesh ist ein einziges Stück:** Accessoires herausschneiden, darunter schließen und als eigene Objekte mit Abstand zur Haut neu bauen. Verschmolzene Finger durch neu gebaute Hände ersetzen.
- **Risse und dunkle Nähte = kaputte Normal-Map:**
  - Erst mit und ohne rendern, dann `$WF/tools/fix_normal_map.py` oder die Normal-Map ganz weglassen.
  - Den AO-Kanal der ORM-Textur prüfen.
- **Keine aufgemalten Züge über modellierten Gesichtern.** Ausdrücke kommen aus Geometrie: Augäpfel, Lider, Mundöffnung, Shape Keys `expr_*` mit Treibern.
- **Rig auf dichten Generator-Meshes:**
  - Formelgewichte entlang der Knochenketten statt Heat-Gewichten, höchstens 4 Einflüsse.
  - Was um den Hals liegt, begrenzt die Kopfdrehung.
- **Export:**
  - Meshopt quantisiert, also Schichten unter 0,5 mm ohne Meshopt exportieren.
  - Animations-Rotationen auf 16 bit (`QUAT_FILTER_BITS`).
  - Keine Morph-Animationen exportieren.
  - Prozedurale Farben vorher backen.
- **Blender 5.x:**
  - `sculpt_brush_type` statt `sculpt_tool`, `Bone.select*` gibt es nicht mehr.
  - Sculpt-Operatoren laufen nicht headless.
  - Kein scipy, stattdessen `mathutils.kdtree`.
  - Bake nur in der Ruhepose.

## Lizenzen

- **Nur Grünes ins Endprodukt:** MIT, Apache-2.0, BSD.
- **Bekannte Lizenzen:**
  - Pixal3D: MIT.
  - DINOv3: Meta-Lizenz, kommerziell ok.
  - ComfyUI und Blender: GPL, nur als Werkzeug.
- **Meiden:**
  - Hunyuan3D, weil die Lizenz die EU ausschließt.
  - Nicht-kommerzielle Face-Rigs und SMPL-basiertes Mocap.
