Aufgabe: {FIGUR} bekommt ein Körper-Rig. Dazu gehören Skelett, Gewichte, Prüfposen und drei kurze Testanimationen. Das Modell darfst Du anpassen, wo es für gute Verformung nötig oder sinnvoll ist.

Ausgangslage
- Arbeitsdatei: {WORK}/figur_rig_input.blend. Sie ist eine Kopie des letzten Stands, das Original liegt schreibgeschützt in {CHECKPOINT}.
- Die Figur steht in A-Pose: {HÖHE} m hoch, Z nach oben, sie schaut nach −Y.
  - Der Körper `CH_{NAME}` stammt aus dem Image-to-3D-Generator Pixal3D: ein verschmolzenes Netz aus einem Stück mit {N} Dreiecken.
  - Modellierte Teile mit Shape Keys `expr_*` und Treibern: {LISTE}.
  - Accessoires als eigene Objekte: {LISTE}.
  - Was bisher gemacht wurde und was offen ist: {NOTIZEN}.
- Zielbilder in {WORK}/ref/: Konzeptbild und Turnaround-Ansichten. So soll die Figur wirken. Nimm sie als Maßstab, wenn Du am Modell etwas änderst.
- {URTEILE, z. B. Mit einem spezialisierten Auto-Rig-Modell gab es bisher nie gute Ergebnisse. Dieser Lauf soll zeigen, ob es klassisch in Blender besser geht.}
- Mir ist schon aufgefallen: {z. B. Die Finger sind im Modell an der Wurzel zu einer Art Fäustling verschmolzen. In den Zielbildern sind sie klar getrennt.}

Ziel
1. Ein Rig für den Körper, mit dem man die Figur animieren kann.
   - Wirbelsäule, Hals, Kopf, Schultern, Arme, Hände mit Fingern, Beine und Füße mit Zehenknick.
   - Wie Du es baust, entscheidest Du. Rigify bietet sich an. Die Ruhepose bleibt die A-Pose.
   - Im .blend liegt ein Steuer-Rig zum Animieren, mit IK/FK, wo es hilft.
   - Für Spiel und Web braucht es ein sauberes Skelett nur aus Deform-Knochen, mit verständlichen Namen und einer Wurzel am Boden. Es soll sich auf übliche Humanoid-Skelette abbilden lassen (Godot, Mixamo-artig).
   - Höchstens 4 Einflüsse pro Punkt, normalisiert. Mehr kann three.js nicht.
2. Gewichte, die gut aussehen, nicht nur rechnerisch vollständig sind.
   - Wo es meist hakt: Schultern und Achseln, Ellbogen und Knie (Volumenverlust, Knick), Handgelenk (Candy-Wrapper), Schritt und Hüfte, Saum und Kapuze beim Kopfdrehen, Finger.
   - Schuhe bleiben fest und knicken nur am Ballen.
   - Gesichtsteile hängen am Kopf. Für Accessoires findest Du selbst heraus, woran sie hängen müssen, damit sie beim Drehen und Nicken nicht eintauchen.
3. Das Modell anpassen, wo es fürs Rig nötig oder sinnvoll ist, zum Beispiel Finger trennen, Achseln, Schritt oder Bündchen säubern oder fehlende Geometrie an Gelenken ergänzen.
   - Look, Farben, Proportionen und Design bleiben. Die Zielbilder sind der Maßstab.
   - Das Gesicht und alle Ausdrücke bleiben, wie sie sind, und funktionieren auch bei gedrehtem Kopf.
   - Eine komplette Retopologie ist nicht das Ziel. Wenn es ohne sie nicht gut wird, schreib es in die Notizen.
4. Prüfposen und Testanimationen als Actions.
   - `qa_poses`: Extreme, die zeigen, ob die Verformung hält. Arme über Kopf, nach vorn und hängend; Ellbogen und Knie stark gebeugt; Handgelenk; Faust und gespreizte Hand; Hocke, Ausfallschritt, Bein seitlich; Rumpf vor, zurück und gedreht; Kopf drehen und nicken.
   - `anim_idle` (Stehen mit Atmen, als Schleife), `anim_walk` (Gehen auf der Stelle, als Schleife), `anim_wave` (Winken mit der rechten Hand). Sie dienen der Beurteilung, sollen aber nicht steif wirken.
- Für den Web-Viewer gilt: three.js mit Meshopt, also werden die Positionen quantisiert. Plane keine übereinanderliegenden Flächen mit weniger als etwa 0,5 mm Abstand. Farben, die nur prozedural im Blender-Shader entstehen, kommen im Browser nicht an.

Arbeitsweise
- Blender 5.2.3 läuft headless: `{BLENDER} -b … --python …`. Renders zum Ansehen liest Du mit dem Read-Werkzeug ({ANSEHEN}). Bilder zusammensetzen kannst Du mit python3 und PIL, dazu gibt es numpy und OpenCV.
- Prüfblätter in {TOOLS}/blender: `face_sheet.py` und `body_sheet.py` (`--only` für einzelne Ansichten). Für Posen brauchst Du eigene Kameras. Achte auf gleiches Licht in Vorher und Nachher.
- Export-Vorlage: {TOOLS}/blender/export_glb.py. Ein Beispiel mit Steuer-Rig, gebackenem Deform-Skelett und 16-bit-Rotationen für Meshopt liegt in {TOOLS}/../examples/sid_rig/export_glb_sid.py.
- Speichere Zwischenstände regelmäßig als eigene .blend in {WORK}.
- Schreiben nur in {WORK}. Lesen darfst Du außerdem {CHECKPOINT}, {TOOLS} und {TOOLS}/../examples.
- Kein Internet, keine 3D- oder Bildgeneratoren, kein Mixamo, keine Live-Blender-Instanz eines Menschen. Die blender-*-Skills darfst Du nutzen, zum Beispiel blender-character-rigging, blender-animation, blender-facial-shapekeys, blender-export-pipelines und blender-asset-qa.
- Zeitrahmen: {ZEIT, bei uns bis etwa 5 Stunden}. Hör auf, wenn Du zufrieden bist oder der Rest den Aufwand nicht lohnt.

Abgabe
1. {WORK}/figur_rig_v1.blend, in sich geschlossen, Texturen eingepackt. Darin liegen Steuer-Rig, Spiel-Skelett und Actions.
2. {WORK}/exports/figur_rig_v1_web.glb mit nur dem Deform-Skelett, Shape Keys (beim Export auf 0), allen vier Actions als getrennten Animationen, Meshopt und WebP. Importier die Datei zur Kontrolle wieder und prüf, dass Skelett, Gewichte, Keys und Animationen ankommen.
3. Prüfbilder: die Prüfposen als Blatt mit Nahansichten der kritischen Gelenke in {WORK}/poses_v1/, je Testanimation ein Streifen in {WORK}/anim_v1/, dazu face_sheet und body_sheet aus der Ruhepose.
4. Für jede Modelländerung ein Vorher/Nachher-Paar mit derselben Kamera und demselben Licht als {WORK}/compare/NN_kurzname.png.
5. {WORK}/notizen_rig_v1.md mit:
   - Rig: Aufbau, Knochenliste, wie Gesichtsteile und Accessoires hängen,
   - „Am Modell geändert“, nummeriert, mit Vergleichsbild,
   - wie Du die Gewichte geprüft und nachgebessert hast,
   - „Gesehen, aber nicht behoben“, mit Grund,
   - wie Du geprüft hast, dass Gesicht und Ausdrücke erhalten sind,
   - bekannten Schwächen und was es für ein Spiel noch bräuchte.
Antworte am Ende kurz mit denselben Punkten.
