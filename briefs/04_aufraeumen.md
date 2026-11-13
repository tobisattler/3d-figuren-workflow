Aufgabe: {FIGUR}, eine Aufräumrunde am ganzen Modell.

Ausgangslage
- Arbeitsdatei: {WORK}/figur_input.blend. Sie ist eine Kopie des letzten Stands, das Original liegt schreibgeschützt in {CHECKPOINT}.
- Die Figur steht in A-Pose: {HÖHE} m hoch, Z nach oben, sie schaut nach −Y.
  - Der Körper `CH_{NAME}` stammt aus einem Image-to-3D-Generator: ein verschmolzenes Netz mit Generator-Textur.
  - Modellierte Teile: {LISTE, z. B. Augen, Lider, Brauen, Mund mit expr_*-Keys und Treibern, Ohren, Kopfhörer als eigene Objekte}.
  - Was in jeder Runde gemacht wurde und welche Schwächen offen sind, steht in {NOTIZEN}.
- {MENSCH} sieht noch Unsauberkeiten am Modell und möchte eine Runde, die allgemein Unreinheiten verbessert. Am Ende interessiert vor allem, was alles verbessert wurde. {URTEILE}
- Bekannte Kandidaten, ohne Anspruch auf Vollständigkeit: {KANDIDATEN aus den Notizen}. Den Rest der Figur hat bisher niemand genau angesehen, zum Beispiel Hände, Hose, Schuhe, Rücken und Unterseiten.
- Hinweis aus früheren Figuren: Risse, Splitter und dunkle Nähte auf Generator-Meshes kamen meist aus kaputten Stellen der Normal-Map, nicht aus Geometrie oder Farbe. `{TOOLS}/fix_normal_map.py` hilft.

Ziel
- Finde die Unsauberkeiten am ganzen Modell und behebe so viele wie sinnvoll möglich. Was wichtig ist und in welcher Reihenfolge, entscheidest Du: am wichtigsten ist, was im normalen Betrachten auffällt.
  - Gemeint sind Geometrie (Dellen, Beulen, Zacken, Durchdringungen, verschmolzene Teile, Löcher, Schuppen-Artefakte) und Textur (Nähte, Flecken, verwaschene oder falsche Farbgrenzen, eingebackenes Licht, das stört).
- Look, Farben, Proportionen und Design bleiben. Das ist Aufräumen, kein Neuentwurf.
- Die Gesichtsausdrücke bleiben erhalten: Alle Shape Keys und Treiber behalten Namen und Wirkung. Wenn Du im Gesicht etwas behebst, dann so, dass kein Ausdruck sich verändert, und zeig es in allen Ausdrücken.
- Accessoires bleiben eigene Objekte. Verfeinern ist erlaubt.
- Für den Web-Viewer gilt: three.js mit Meshopt, also werden die Positionen quantisiert. Plane keine übereinanderliegenden Flächen mit weniger als etwa 0,5 mm Abstand.

Arbeitsweise
- Blender 5.2.3 läuft headless: `{BLENDER} -b … --python …`. Renders zum Ansehen liest Du mit dem Read-Werkzeug ({ANSEHEN}). Bilder zusammensetzen kannst Du mit python3 und PIL.
- Ein Prüfblatt der ganzen Figur gibt es schon: `{TOOLS}/blender/body_sheet.py` mit 31 Ansichten von Figur, Torso, Händen, Füßen, Beinen und Haaren. `--only name1,name2` rendert einzelne. Dazu kommt `face_sheet.py`.
- Speichere Zwischenstände regelmäßig als eigene .blend in {WORK}, damit ein Absturz höchstens eine Etappe kostet.
- Schreiben nur in {WORK}. Lesen darfst Du außerdem {CHECKPOINT} und {TOOLS}.
- Kein Internet, keine 3D- oder Bildgeneratoren, keine Live-Blender-Instanz eines Menschen. Die blender-*-Skills darfst Du nutzen, zum Beispiel blender-asset-qa oder blender-texturing.
- Zeitrahmen: {ZEIT}. Hör auf, wenn Du zufrieden bist oder der Rest den Aufwand nicht lohnt.

Abgabe
1. {WORK}/figur_vN.blend, in sich geschlossen, Texturen eingepackt.
2. Prüfblätter aus der finalen Datei, mit face_sheet.py nach {WORK}/sheet_vN und body_sheet.py nach {WORK}/body_vN, jeweils `--samples 64`.
3. Für jede Verbesserung ein Vorher/Nachher-Paar mit derselben Kamera und demselben Licht, links aus {CHECKPOINT}, rechts aus der Abgabe, als {WORK}/compare/NN_kurzname.png, nummeriert wie in Punkt 4.
4. {WORK}/notizen_vN.md mit:
   - einer nummerierten Liste „Verbessert“: Stelle, was unsauber war, was Du gemacht hast, Vergleichsbild,
   - „Gesehen, aber nicht behoben“, mit Grund,
   - welche Objekte es jetzt gibt,
   - wie Du geprüft hast, dass Gesicht und Ausdrücke erhalten sind,
   - bekannten Schwächen.
Antworte am Ende kurz mit denselben Punkten.
