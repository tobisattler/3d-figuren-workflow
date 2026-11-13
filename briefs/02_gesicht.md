Aufgabe: Gib der Figur {FIGUR} ein modelliertes, animierbares Gesicht.

Ausgangslage
- Die Figur liegt in {WORK}/figur_input.blend, als Kopie von {CHECKPOINT}.
- Ein Mesh `CH_{NAME}`, ca. {N}k Faces, aus dem Image-to-3D-Generator Pixal3D. Die Texturen sind eingepackt. Maße: {HÖHE} m hoch, Z nach oben, die Figur schaut nach −Y.
- Augen, Brauen und Mund sind bisher nur in die Textur gemalt oder grob geformt.
- Referenzen in {WORK}/ref/: das Konzeptbild (so soll die Figur wirken) und die Turnaround-Ansichten. So sieht das Original im Standard-Render aus: {WORK}/sheet_original/.

Ziel
Die Figur bekommt ein echtes, modelliertes Gesicht, das sich animieren lässt und ihren Charakter wie im Konzeptbild behält:
- Augen mit Augäpfeln (Iris und Pupille), die nach vorn schauen.
- Lider, die sich schließen können.
- Ein Mund, der sich öffnen kann.
- Brauen, wenn es passt.
Ausdrücke als Shape Keys mit dem Präfix `expr_`, mindestens expr_blink, expr_smile, expr_surprised, expr_angry. Der neutrale Zustand soll mindestens so gut aussehen wie das Original.

Was {MENSCH} bei früheren Versuchen abgelehnt hat (Beispiele, durch eigene ersetzen):
- Aufgemalte Gesichtszüge über modellierten: Das wirkte doppelt, „schrecklich“.
- Ein modelliertes Gesicht mit zu großen, tiefen Augen und unheimlichen Lidern: „Halloween Horror“.
- Ein übertragenes Realismus-Face-Rig: „sieht nicht gut aus“.
{URTEILE}
{MENSCH} will hochwertige Spielfiguren. Ein stimmiger Gesamteindruck ist wichtiger als ein billiger Animationstrick. Maßstäbe: wirklich neutrale Ruhepose, Ausdrücke, die klar treffen, keine Beulen oder Dellen.

Arbeitsweise
- Blender 5.2.3 läuft headless: `{BLENDER} -b … --python …`. Renders zum Ansehen liest Du mit dem Read-Werkzeug ({ANSEHEN}).
- Schreiben nur in {WORK}. Lesen darfst Du außerdem {CHECKPOINT} und {TOOLS}.
- Kein Internet, keine 3D- oder Bildgeneratoren, keine Live-Blender-Instanz eines Menschen. Die blender-*-Skills darfst Du nutzen.
- Für Web und Spiel: Das Modell wird in three.js gezeigt, eventuell mit Meshopt-Kompression (quantisierte Positionen). Plane keine übereinanderliegenden Flächen mit weniger als etwa 0,5 mm Abstand, oder sag in den Notizen, dass ohne Meshopt exportiert werden muss.
- Zeitrahmen: {ZEIT}. Hör auf, wenn Du zufrieden bist.

Abgabe
1. {WORK}/figur_gesicht.blend, in sich geschlossen, Texturen eingepackt.
2. Das Standard-Prüfblatt: `{BLENDER} -b {WORK}/figur_gesicht.blend --python {TOOLS}/blender/face_sheet.py -- --out {WORK}/sheet_final --samples 64` (bei realistischen Proportionen `--head-frac 0.14`).
3. {WORK}/notizen.md: was Du gemacht hast, welche Objekte und Shape Keys es gibt, bekannte Schwächen, ungefähre Zahl der Render-Runden.
Antworte am Ende kurz mit denselben Punkten.
