# Lizenzen und Kosten

## Lizenzen (Stand 13.11.2026, bitte vor kommerzieller Nutzung selbst prüfen)

| Teil | Lizenz | Hinweis |
|---|---|---|
| Dieses Repo (Skripte, Skill, Vorlagen) | MIT | |
| Pixal3D (TencentARC), Comfy-Repack | MIT | |
| TRELLIS.2-VAEs im Pixal3D-Paket | MIT | |
| DINOv3 (`dino_v3_L_naf_fp32`) | Meta DINOv3-Lizenz | kommerziell ok, Militär/ITAR verboten, bei Weitergabe Lizenztext beilegen |
| BiRefNet | MIT | Lizenz der Trainingsdaten (DIS5K) nicht geprüft |
| ComfyUI | GPL-3.0 | nur Werkzeug, die Ausgaben sind davon nicht betroffen |
| Blender, Rigify | GPL | nur Werkzeug |
| Blender-Skills (EL4CTEO, majidmanzarpour) | MIT | |
| Blender-MCP (ahujasid/blender-mcp) | siehe Repo | optional, nicht nötig für die Fable-Runden |
| Gemini-Bildmodell | Google-Nutzungsbedingungen | die Bedingungen für generierte Bilder gelten |

**Bewusst nicht genutzt:**
- Hunyuan3D: die Lizenz schließt die EU aus, auch für die Ausgaben.
- FLAME, außer der Version 2023 Open.
- OmniFaceRig und TopoRig: nicht kommerziell.
- SMPL/AMASS-basierte Mocap-Modelle, solange es keine Lizenz dafür gibt.

## Kosten und Zeiten bei uns

| Schritt | Aufwand |
|---|---|
| Turnaround-Blatt 2K (Nano Banana 2.1) | ~0,06 $, ~30 s pro Bild |
| Bearbeitung in 4K | ~0,13 $ |
| Pixal3D-Lauf, RTX 2080 Ti | 117–255 s, 8,6–9,8 GB VRAM |
| Fable-Runde Gesicht (xhigh) | 81 min, ~500k Tokens |
| Fable-Runde Accessoires (xhigh) | ~50 min |
| Fable-Runde Rig (xhigh) | knapp 3 h |
| Prüfblatt mit 31 Ansichten (Cycles, 64 Samples, GPU) | 10–15 min |

Fable kostet pro Token doppelt so viel wie Opus und verbraucht bei uns 25–35 % mehr Tokens. Die Laufzeit war nicht wichtig, die höheren Kosten haben sich gelohnt, weil die Modelle brauchbar wurden.
