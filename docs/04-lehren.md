# Lehren und Stolperfallen

## Turnaround und Bildgenerator

- **Proportionen driften**, wenn nur das Avatarbild als Referenz dient. 3 von 6 Figuren kamen mit 5–6 statt 3 Kopflängen. Ein abgenommenes Blatt als zweite Referenz („Proportionen, Stil, Pose und Licht aus Bild 2“) brachte 5 von 5.
- **Hände leer lassen.** Requisiten werden eigene Objekte.
- **Hintergrund einfarbig, ohne Bodenlinie.** Sonst schneidet die Hintergrundentfernung in Pixal3D falsch.

## Pixal3D

- **Seitenkonvention:**
  - Slot `left` = Blick nach **Bild-links**.
  - Falsch belegte Seiten ergeben ein Doppelgesicht am Hinterkopf („Janus“).
  - Ohne Rückansicht passiert dasselbe.
  - Das Comfy-Beispielblatt belegt die Slots andersherum. Bei einem Doppelgesicht deshalb `--swap-sides` probieren.
- **Ein einziges verschmolzenes Mesh:** Accessoires, Haut und Kleidung haben keine echten Grenzen, Finger sind oft Fäustlinge. Das plant man als eigene Runden ein.
- **Risse, Splitter und dunkle Nähte** kommen meist aus kaputten Stellen der **Normal-Map**, nicht aus Geometrie oder Farbe. Bei Sid waren 5 % der genutzten Texel betroffen, im Haar 11 %.
  - Erst mit und ohne Normal-Map rendern, dann `tools/fix_normal_map.py`.
  - Bleibt danach nur Rauschen, ist die Normal-Map ganz wegzulassen oft das Sauberste.
  - Auch der AO-Kanal der ORM-Textur hatte an denselben Stellen dunkle Flecken. Sichtbar war das nur in three.js.
- **Textur-Auflösung:** Bei 3 × 2048 für die ganze Figur bekommt das Gesicht nur einen kleinen Fleck. Für stilisierte Figuren hat das gereicht.

## Gesicht

- **Keine aufgemalten Gesichtszüge über modellierten.** Das wirkte doppelt: Augen in Höhlen, ein „O“ auf geschlossenen Lippen.
- **Ausdrücke kommen aus Geometrie:** Augäpfel als eigene Kugeln, Lidringe, eine echte Mundöffnung, Shape Keys mit Treibern.
- **Ein auf Cartoon-Proportionen übertragenes Realismus-Face-Rig** (ICT-FaceKit per Non-Rigid-ICP) sah nicht gut aus. Das modellierte Gesicht von Fable war besser.
- **Maßstäbe des Menschen:**
  - die Ruhepose wirklich neutral,
  - Ausdrücke, die klar treffen,
  - keine Beulen oder Dellen,
  - die Augen lebendig.

## Accessoires und Kleidung

- **Immer eigene Objekte:** Kopfhörer, Brille, Mütze, Schmuck, Taschen. Kleidung wird getrennt, sobald sie tauschbar sein oder sich bewegen soll.
- **Bei Generator-Meshes:** das Accessoire herausschneiden, Haut und Kragen darunter schließen und neu bauen. Bei Sid ergab das 4–6 mm Abstand, auch bei offenem Mund.
- **Was um den Hals liegt, begrenzt die Bewegung:** Mit Kopfhörern um den Hals ging bei Sid nur etwa 15° Kopfdrehung bei geradem Kopf, und die Arme ließen sich kaum nach vorn nehmen. Das ist eine Designfrage, kein Gewichtsproblem.

## Rig

- **Auf dichten, verschmolzenen Generator-Meshes sind Heat- bzw. Auto-Gewichte unruhig.** Gewichte entlang der Knochenketten per Formel, danach geglättet, hielten bei Sid in allen 29 Prüfposen.
- **Verschmolzene Finger** bekommen neu gebaute Hände mit fünf Fingern. Jede Hand sitzt als eigenes geschlossenes Teil im Bündchen, damit sich das Handgelenk nicht wie ein Bonbonpapier verdreht.
- **Achseln** sieht man erst bei gehobenem Arm. Textur und Mesh dort säubern.
- **Formen:** höchstens 4 Einflüsse pro Punkt (three.js). Spiel-Skelett nur aus Deform-Knochen, mit Namen nach Godots Humanoid-Profil.

## Export und Web

- **Meshopt quantisiert Positionen.** Schichten unter etwa 0,5 mm Abstand flimmern, also dünne Augenteile ohne Meshopt exportieren.
- **Meshopt packt Animations-Rotationen mit 8 bit** (bis 1,7° Fehler pro Knochen). `QUAT_FILTER_BITS = 16` im Export-Skript behebt das ohne Änderung am Decoder.
- **Morph-Animationen nicht mit exportieren.** Sonst überschreiben die Treiber-Spuren die Ausdrucksregler im Viewer.
- **Prozedurale Shader-Farben** kommen im Browser nicht an. Vorher auf Texturen backen.

## Prüfen

- **Schrägansichten zeigen, was Silhouetten verbergen:** ¾ vorne und hinten, von oben, von unten.
- **Der Score (IoU + DINO) misst grobe Abstände gut**, feine schlecht. Eingebackene Schattierung bläht DINO auf. Bei feinen Unterschieden entscheidet der Mensch im Viewer.
- **Bleibt der Score stehen**, wechselt man Methode oder Eingabe, statt mehr Iterationen zu rechnen.
- **Blender-5.x-API:**
  - `brush.sculpt_tool` heißt jetzt `sculpt_brush_type`.
  - `Bone.select*` gibt es nicht mehr.
  - Die UV-Auswahl ist neu.
  - Sculpt-Operatoren laufen nicht headless.
  - Surface Deform hat in 5.2.3 nicht gebunden.
  - Bake nur in der Ruhepose, aktive Posen ergeben schwarz.
