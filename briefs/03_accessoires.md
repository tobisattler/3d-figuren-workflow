Aufgabe: {FIGUR}, {ACCESSOIRE} wird ein eigenes Objekt.

Ausgangslage
- Arbeitsdatei: {WORK}/figur_input.blend. Sie ist eine Kopie des letzten Stands, das Original liegt schreibgeschützt in {CHECKPOINT}.
- Die Figur: {HÖHE} m hoch, Z nach oben, sie schaut nach −Y.
  - Der Körper `CH_{NAME}` stammt aus einem Image-to-3D-Generator: ein verschmolzenes Netz mit gemeinsamer Textur.
  - {WAS SCHON MODELLIERT IST, z. B. Gesicht mit Shape Keys expr_* und Treibern}.
  - Die Notizen der früheren Runden: {NOTIZEN}.
- Das Problem: {ACCESSOIRE, z. B. die Kopfhörer um den Hals} gehört zum selben verschmolzenen Generator-Mesh wie Haut und Kleidung. {WO ES VERSCHMILZT, z. B. die Ohrmuscheln verschmelzen mit Kinn und Kiefer}, eine echte Grenze gibt es nicht. {SCREENSHOT DES MENSCHEN, falls vorhanden}

Ziel
- {ACCESSOIRE} wird ein eigenes Objekt oder mehrere, mit eigenen Materialien. Look, Farben, Proportionen und Lage bleiben wie bisher, gern sauberer ausgearbeitet.
- Am Körper wird die Geometrie des Accessoires entfernt. Darunter wird alles sauber geschlossen, sodass die Figur auch ohne das Accessoire vollständig aussieht.
- Das Accessoire liegt glaubwürdig auf. Zur Haut bleibt ein kleiner, sichtbarer Abstand, es gibt keine Durchdringung. Das gilt auch bei allen Ausdrücken, zum Beispiel bewegt `expr_mouth_open` das Kinn.
- Unverändert bleiben {WAS GLEICH BLEIBT: Gesicht, Ohren, alle Shape Keys und Treiber mit Namen und Wirkung}.
- Für den Web-Viewer gilt: three.js mit Meshopt-Kompression, also werden die Positionen quantisiert. Plane keine übereinanderliegenden Flächen mit weniger als etwa 0,5 mm Abstand.
- {MENSCH} will hochwertige Spielfiguren. Ein stimmiger Gesamteindruck ist wichtiger als ein billiger Trick. {URTEILE}

Arbeitsweise
- Blender 5.2.3 läuft headless: `{BLENDER} -b … --python …`. Renders zum Ansehen liest Du mit dem Read-Werkzeug ({ANSEHEN}).
- Schreiben nur in {WORK}. Lesen darfst Du außerdem {CHECKPOINT} und {TOOLS}.
- Kein Internet, keine 3D- oder Bildgeneratoren, keine Live-Blender-Instanz eines Menschen. Die blender-*-Skills darfst Du nutzen, zum Beispiel blender-asset-qa.
- Zeitrahmen: {ZEIT}. Hör auf, wenn Du zufrieden bist.

Abgabe
1. {WORK}/figur_vN.blend, in sich geschlossen, Texturen eingepackt.
2. Prüfblätter aus der finalen Datei:
   - `{BLENDER} -b {WORK}/figur_vN.blend --python {TOOLS}/blender/face_sheet.py -- --out {WORK}/sheet_vN --samples 64`
   - `{BLENDER} -b {WORK}/figur_vN.blend --python {TOOLS}/blender/body_sheet.py -- --out {WORK}/body_vN --samples 64 --only {ANSICHTEN rund um das Accessoire, z. B. torso_front,torso_tq_R,torso_back}`
3. Vorher/Nachher-Paare mit derselben Kamera und demselben Licht als {WORK}/compare/NN_kurzname.png.
4. {WORK}/notizen_vN.md: was Du gemacht hast, welche Objekte es jetzt gibt, gemessene Abstände (auch in den Ausdrücken), bekannte Schwächen.
Antworte am Ende kurz mit denselben Punkten.
