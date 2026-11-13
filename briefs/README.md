# Auftragsvorlagen für Fable-Subagenten

Eine Datei pro Runde. Der Hauptagent füllt die Platzhalter aus und startet damit einen Subagenten mit Modell `fable`, Effort `xhigh`, im Hintergrund.

| Datei | Runde |
|---|---|
| `01_turnaround_prompt.md` | Turnaround-Blatt per Bildgenerator. Das ist ein Prompt für den Hauptagenten, kein Subagenten-Auftrag |
| `02_gesicht.md` | modelliertes, animierbares Gesicht mit Ausdrücken als Shape Keys |
| `03_accessoires.md` | ein verschmolzenes Accessoire als eigenes Objekt |
| `04_aufraeumen.md` | Aufräumrunde am ganzen Modell |
| `05_rig.md` | Körper-Rig, Gewichte, Prüfposen, Testanimationen, Web-Export |

## Platzhalter

| Platzhalter | Beispiel |
|---|---|
| `{FIGUR}` | Sid, ein stilisierter Avatar im Spielzeugfigur-Look, ca. 3 Köpfe hoch |
| `{WORK}` | Arbeitsordner der Runde, z. B. `~/work/sid_v3` |
| `{CHECKPOINT}` | schreibgeschützter letzter Stand, z. B. `~/work/checkpoints/sid_v2` |
| `{BLENDER}` | Aufruf von Blender, z. B. `CUDA_VISIBLE_DEVICES=0 ~/blender-5.2.3-linux-x64/blender` (oder `ssh gpu "cd {WORK} && …"`) |
| `{TOOLS}` | Pfad zu diesem Repo, z. B. `~/3d-figuren-workflow/tools` |
| `{ANSEHEN}` | wohin der Agent Renders zum Ansehen legt, falls Blender auf einem anderen Rechner läuft |
| `{MENSCH}` | wer am Ende urteilt |
| `{URTEILE}` | was {MENSCH} bisher gesagt oder abgelehnt hat, wörtlich |
| `{ZEIT}` | Zeitrahmen, z. B. „bis etwa 3 Stunden“ |

Ein guter Auftrag ist kurz und **nicht vorschreibend**: Er sagt was und woran es gemessen wird, nicht wie. Mehr dazu in `../docs/03-fable-auftraege.md`.
