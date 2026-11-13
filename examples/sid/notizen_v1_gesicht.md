# Sid – modelliertes, animierbares Gesicht (Kandidat A)

Abgabe: `sid_face.blend` (in sich geschlossen, Texturen eingepackt), Prüfblatt in `sheet_final/`.

## Was ich gemacht habe

**1. Aufgemaltes Gesicht entfernt** (`stage_a.py` → `stage_a.blend`)
- Augen, Brauen und Mund waren nicht nur gemalt, sondern auch als Relief im Mesh (Brauenwülste, Lidränder,
  Mundhöhle). Die Flächen sind mit einer Thin-Plate-Spline-Fläche aus der umliegenden sauberen Haut gefüllt,
  die dabei gefalteten Dreiecke entfaltet, die Nase bleibt unangetastet.
- Textur: Im selben Bereich ist die Hautfarbe über das Mesh harmonisch aufgefüllt und in den vorhandenen
  UV-Atlas gebacken (BaseColor, ORM, Normal → `T_Sid_BaseColor/ORM/Normal`, eingepackt). Außerhalb des Gesichts
  sind die Texturen pixelgleich. Es gibt keine gemalten Gesichtszüge mehr – alles Sichtbare ist Geometrie.
- Die Custom-Normals des Generators sind entfernt (sie hätten das alte Relief weiter schattiert).

**2. Gesicht aufgebaut** (`build_face.py`, alle Zahlen in `face_params.py`)
- Gesichtshaut lokal unterteilt (ca. 2 mm, an Lid- und Lippenkanten ca. 1 mm), der Rest der Figur ist unverändert.
- Drei gerade Schnitte in der Haut: Auge rechts, Auge links, Mund. Die Kanten haben nach innen gezogene Ränder
  (Lidstärke 1,3 mm, Lippen 7,5 mm tief), die Kanten sind scharf markiert.
- Jeder Gesichtszustand ist dieselbe parametrische Verformung dieses Zustands: Die Schnittkanten werden auf
  Lid-/Lippenkurven gelegt, die Haut gleitet mit linearem Abfall auf der Gesichtsoberfläche (Höhenfeld) mit.
  Neutral = Basis, alle anderen Zustände = Shape Keys. Das geschlossene Auge ist dadurch einfach die glatte Haut.
- **Augäpfel** (`CH_Sid_Eye_L/R`): geschlossene, linsenförmige Körper, die 1,3 mm hinter der Lidfläche liegen
  und bündig in der Gesichtswölbung sitzen (nicht tief). Iris (Verlauf, dunkler Rand), Pupille und Glanzpunkt
  sind modelliert bzw. als Farbattribut auf der Geometrie, Blick geradeaus, leicht konvergent wie im Avatar.
- **Wimpernlinie** (`CH_Sid_Lashes`): dunkler, sich verjüngender Körper auf der Oberlidkante, folgt dem Lid in
  jedem Ausdruck.
- **Brauen** (`CH_Sid_Brows`): modellierte, flach gewölbte Körper, leicht asymmetrisch (rechte Braue tiefer,
  linke höher – der freche Zug aus dem Avatar).
- **Mund** (`CH_Sid_Mouth`): dunkle Mundhöhle, obere Zahnreihe als glattes Band, Zunge. Im Ruhezustand hinter
  den Lippen verborgen.

**3. Ausdrücke** (Shape Keys auf `CH_Sid`, Wert 0–1)
- Gefordert: `expr_blink`, `expr_smile` (das offene Grinsen aus dem Avatar), `expr_surprised`, `expr_angry`.
- Zusätzlich: `expr_mouth_open`, `expr_sad`, `expr_blink_L`, `expr_blink_R` (Zwinkern; L/R aus Sids Sicht).
- Wimpern, Brauen und Mundteile tragen gleichnamige Keys und folgen `CH_Sid` über Treiber – es reicht, die
  Keys auf `CH_Sid` zu animieren.
- Blick: Keys `eye_look_left/right/up/down` auf beiden Augenobjekten (bewusst ohne `expr_`-Präfix, daher nicht
  im Prüfblatt; einzeln geprüft).
- Geprüft: Zwischenwerte (0,5) aller Ausdrücke, Kombinationen blink+smile, blink+angry, smile+surprised,
  Ansichten von oben/unten in den offenen Mund, Treiberkette.

**4. Prüfung**
- Mesh: keine nicht-mannigfaltigen Kanten, keine losen Teile, keine Null-Flächen, Normalen konsistent,
  Maßstab/Lage unverändert (1,0 m, Ursprung am Boden). `qa.py` gibt die Zahlen aus.
- Neutralzustand gegen `common/sheet_original` verglichen.

## Bekannte Schwächen
- **Augäpfel sind keine Kugeln.** An der Augenposition ist der Kopf um ca. 29° nach außen geneigt; eine Kugel
  läge dort entweder tief in der Höhle oder würde schielen. Deshalb linsenförmige Augkörper, die der Wölbung
  folgen. Folge: Blickrichtung über die `eye_look_*`-Keys (Iris gleitet auf dem Auge), nicht über Rotation.
- **Neutral hat den Mund geschlossen** (Schmunzeln mit leicht hochgezogenem linken Mundwinkel). Das offene
  Grinsen des Originals/Avatars steckt in `expr_smile`. Wer das Grinsen als Ruhepose will, muss den Key setzen.
- **Kein Retopo.** Es bleibt das dichte Dreiecksnetz des Generators (jetzt ca. 127 000 Vertices, 254 000
  Dreiecke). Für die Verformung reicht die Dichte, für eine Engine müsste man reduzieren.
- **Offene Ränder im Kopfinneren:** Die drei Lid-/Lippenränder enden innen offen (3 Randschleifen), der Kopf
  ist also nicht mehr wasserdicht. Von außen nicht sichtbar.
- **Mikro-Faltungen an den Winkeln:** Je Zustand kippen bis zu ca. 25 Dreiecke (jeweils unter 1 mm²) direkt an
  Augen- oder Mundwinkeln um. In allen Nahaufnahmen unsichtbar, aber vorhanden (`build_face.py` loggt die Zahl).
- **Zähne/Zunge schlicht:** nur obere Zahnreihe als durchgehendes Band (wie im Avatar), keine unteren Zähne,
  Zunge ist ein einfacher Körper. Die Zähne werden im Lächeln per Shape Key etwas nach unten geführt.
- **Stirn bewegt sich nicht mit:** Brauen gleiten als aufgesetzte Körper über die Stirn; die Haut darunter
  bleibt unverändert, es gibt keine Falten.
- **Getrennte Objekte:** Augen, Wimpern, Brauen und Mundteile sind eigene Objekte (an `CH_Sid` geparentet,
  per Treiber gekoppelt), kein Einzelmesh. Sie haben keine UVs, nur einfarbige Materialien bzw. ein Farbattribut.
- **`expr_sad`** liest sich eher „müde/enttäuscht“ als traurig; `expr_surprised` hat eine leicht kantige O-Form.
- **Summen mehrerer Mund-Ausdrücke** (z. B. surprised + mouth_open bei 1,0) überziehen den Mund; dafür gibt es
  keine Korrektur-Shapes.
- **Hautmaterial unverändert:** Die ORM-Textur des Generators hat auf der Haut Metallic 0,2–0,3, dadurch
  wirkt die Haut im Prüflicht blasser als im Avatar. Bewusst nicht angefasst (betrifft auch Hände).
- Der Glanzpunkt im Auge ist modelliert und wandert nicht mit dem Licht.
- Das äußere Ende der rechten Braue liegt dicht an der pinken Haarsträhne.

## Aufwand
- Ungefähr 21 Render-Runden: 2 für das bereinigte Gesicht, 5 komplette Prüfblätter in niedriger Qualität,
  9 Nahaufnahme-Sätze, 4 Diagnose-Renders (Clay/Wireframe/Albedo), 1 Endblatt. Dazu ca. 25 Build-Läufe
  (je etwa 15 s).
- Kein Internet, keine Generatoren, kein Blender-MCP; nur GPU 0.

## Dateien in diesem Ordner
- `sid_face.blend` – Abgabe. `stage_a.blend` – Zwischenstand (Gesicht bereinigt, noch ohne Züge).
- `sheet_final/` – Prüfblatt (64 Samples).
- `stage_a.py`, `build_face.py`, `face_params.py`, `facelib.py` – Aufbau; neu bauen mit
  `blender -b ../common/sid.blend --python stage_a.py` und danach
  `blender -b stage_a.blend --python build_face.py`.
- `qa.py` (Mesh-/Datei-Prüfung), `closeup.py` (Nahaufnahmen mit dem Licht des Prüfblatts).
- `tex/` – die drei neu geschriebenen Texturen als PNG (in der .blend eingepackt), `tmp/stage_a.npz` – Masken
  für den zweiten Schritt.
