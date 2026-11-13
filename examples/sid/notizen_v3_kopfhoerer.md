# Sid v3 – Kopfhörer als eigene Objekte

Abgabe: `sid_face_v3.blend` (in sich geschlossen, alle 5 Texturen eingepackt, keine Bibliotheken), Prüfblätter in
`sheet_v3/` und `neck_v3/`. Ausgangsdatei war `sid_face_v2_input.blend`.

## Was ich gemacht habe

**1. Alte Kopfhörer aus dem Körper geschnitten**
- Die Generator-Kopfhörer sind vermessen (Muschelachse, Kappenmitte, Bügel als ebenes U in einer um ca. 25° geneigten
  Ebene) und mit einer analytischen Hülle aus `CH_Sid` herausgeschnitten: 26 756 Dreiecke. Auf Haut ist die Hülle
  knapp (ca. 6–10 mm über der alten Muschel), auf Stoff und Haar 6 mm weiter, damit die dunklen Nahtkanten des
  Generators mit wegfallen. Zusätzlich entfernt: die dunklen Brückenflächen zwischen Nacken und altem Bügel.
- Die Ohr-Patches aus v2 (`M_Sid_HeadSide`) sind geschützt; die Hülle hat dort 0 Flächen getroffen.

**2. Körper darunter geschlossen (7 Löcher, 13 348 neue Punkte)**
- Kieferecke links/rechts (Haut), Hoodie unter den Muscheln links/rechts, Kapuzenrand links/rechts (wo der Bügel
  auflag), Nacken/Haaransatz hinten (wo der Bügel mit dem Haar verschmolzen war).
- Jedes Loch: Dreiecksfächer, auf ca. 2,2 mm Kantenlänge verfeinert, dann als Thin-Plate-Fläche geglättet
  (Bi-Laplace mit zwei festen Randringen, also tangentenstetig zum alten Netz). Blenders numpy hat kein schnelles
  BLAS, deshalb matrixfrei mit konjugierten Gradienten.
- Farbe und ORM der neuen Flächen sind vom Lochrand harmonisch nach innen interpoliert und in den freien Platz von
  `T_Sid_HeadSide_BaseColor/ORM` (1024²) geschrieben; die neuen Flächen nutzen `M_Sid_HeadSide`. Kein drittes
  Material, keine Vertexfarben. Vorhandene Texel dieser Textur sind unverändert (nachgemessen: 51 650 Texel
  geändert, davon 0 in den UV-Inseln aus v2, auch nicht in 4 px Rand darum). Im Nacken trifft Haut auf Haar:
  dort eine klare Haarlinie statt Verlauf.
- Alte Punkte: Position unverändert (max. Abweichung 0,0), Shape-Key-Deltas unverändert (max. Abweichung 0,0 bei
  allen 8 Keys).

**3. Neue Kopfhörer (3 Objekte, an `CH_Sid` geparentet, Transform = Identität wie die Gesichtsteile)**
- `CH_Sid_Headphones_Band`: grauer Bügel (34 × 12 mm, verrundet) als ebenes U um den Nacken, dazu zwei magentafarbene
  Arme, die in die Gehäuse laufen. 13 596 Dreiecke.
- `CH_Sid_Headphones_Cup_L` / `_Cup_R` (L = Sids linke Seite = +X): je vier Drehkörper – Kappe, Gehäuse, Schale,
  Polster mit vertiefter Öffnung. Je 4 608 Dreiecke.
- Materialien (einfarbig, ohne Textur, ohne UVs): `M_Sid_HP_Band`, `M_Sid_HP_Housing`, `M_Sid_HP_Shell`,
  `M_Sid_HP_Cushion`, `M_Sid_HP_Cap`, `M_Sid_HP_Grille`. Farben angelehnt an die Mediane der alten Textur, teils nach Auge
  nachgezogen. Gehäuse und Kappe haben eine Lackschicht (Coat), das Polster Sheen.
- Alle Maße in `scripts/hp_params.py`, Modell in `scripts/hp_model.py`.

**Gegenüber dem Original bewusst geändert:** Die alten Muscheln steckten ca. 15 mm tief im Kiefer und im Hoodie. Damit
ein Abstand zur Haut bleibt, sind die neuen kleiner (Radius 44 statt ca. 48 mm, Tiefe 61 statt ca. 70 mm), sitzen
tiefer und weiter außen und sind um den Arm 8° geschwenkt (Polsterseite tiefer). Die leichte Vorwärtsdrehung der
alten Muscheln (ca. 11°) gibt es nicht mehr. Der Bügel ist schlanker (12 statt ca. 22 mm) und liegt hinten tiefer,
mit Abstand zum Haar statt damit verschmolzen.

## Objekte in der Datei
`CH_Sid` (172 508 Punkte, 344 460 Dreiecke; v2: 172 229 / 343 926), `CH_Sid_Brows`, `CH_Sid_Eye_L/R`,
`CH_Sid_Lashes`, `CH_Sid_Mouth` (alle unverändert), neu `CH_Sid_Headphones_Band`, `_Cup_L`, `_Cup_R`.

## Prüfung (mit Herkunft der Zahlen)
- **Netz** (`sid_v2/scripts/qa_v2.py` auf der finalen Datei): ein zusammenhängendes Stück, 0 nicht-mannigfaltige
  Kanten/Punkte, 0 Null-Flächen, offene Ränder weiterhin nur die 3 Lid-/Lippenschleifen (574 Kanten). Kopfhörer:
  geschlossene Körper, keine offenen Ränder.
- **Keys/Treiber** (`keys_drivers.py` gegen `kd_v2.json`): alle Objekte gleiche Key-Namen, gleiche Treiber, gleiche
  Materialien. Gesichtsteile: gleiche Dreieckszahl.
- **Abstand zur Haut** (`scripts/check_v3.py`, Muscheln, alle `expr_*` einzeln bei 1,0 und drei Summen):
  neutral 6,4 mm (L) / 5,3 mm (R); kleinster Wert 4,0 / 2,8 mm bei `expr_smile` + `expr_mouth_open` beide 1,0;
  bei `expr_mouth_open` allein 5,1 / 4,0 mm. In keinem Zustand eine Durchdringung der Haut gemeldet.
- **Durchdringung allgemein** (`scripts/check_parity.py`, Strahl-Parität, nur Neutralpose): Bügel 0 von 13 530
  Messpunkten im Körper. Muscheln 57 (L) / 46 (R) Punkte im Stoff, höchstens 3,6 / 2,8 mm tief, alle am unteren
  hinteren Rand – das ist die Auflage auf der Brust-/Schulterschräge.
- Bügel zum Stoff: kleinster Abstand 1,3 mm (seitlich am Kapuzenrand).
- **Ohren** (`scripts/check_ear.py`, unabhängig von Farbklassen): Muscheln zu den Ohr-Patches 43,4 / 42,9 mm. Der
  nächste Punkt am Kopf ist die Kieferunterseite bei (±0,069 | −0,062 | 0,606) – das ist die neu gefüllte Fläche,
  der Hautabstand wird also gegen eine von mir gebaute Fläche gemessen.
- **Gesicht im Bild** (Pixelvergleich `sheet_v3` gegen `checkpoints/sid_v2/sheet_v2`, 21 der 22 Ansichten): in den
  oberen 60 % jedes Kopfbilds 0,000 % geänderte Pixel (Schwelle 12/255), in allen Ausdrücken. Alle Unterschiede
  liegen ab Bildzeile 705–753 von 900, also an Kieferlinie, Kopfhörern und Kragen. `head_tq_expr_surprised` war
  beim Vergleich noch nicht fertig und ist nicht verglichen. `body_front` hat einen anderen Ausschnitt und ist
  kein Gesichtsmaß.
- **Prüfblätter**: beide vollständig (10 bzw. 22 Bilder), nach dem letzten Bau aus `sid_face_v3.blend` gerendert.

## Wie die Platzierung zustande kam
Die Lage ist nicht in einem Schritt entstanden, sondern in vier Runden: ein erster Ansatz (Bügel steckte seitlich
tief in der Kapuze), fünf Kandidaten A–E, drei Kandidaten F–H nur für den Bügel, dann der finale Bau. Gewählt:
Muscheln aus E, Bügel aus H. `scripts/cand.txt` enthält nur noch F–H. Die Kandidaten wurden an einem Zwischenstand
des Körpers (`tmp/build_a.blend`) gemessen; der finale Körper hat einen weiter ausgeschnittenen und neu gefüllten
Hoodie. Dadurch sinken die Muscheln im Endstand bis 3,6 mm in den Stoff statt der dort gemessenen 1,2 mm.

## Bekannte Schwächen
- **Dunkle Kanten auf dem Hoodie.** Reste der Generator-Nahtlinien liegen außerhalb des Schnitts: neben den
  Kordel-Ansätzen, auf den Schultern und entlang der Kapuzen-Schulter-Kante. Die an den Kordel-Ansätzen sind auch
  mit Kopfhörern in jeder Frontansicht des Halsblatts zu sehen; verdeckt sind nur die an den Schultern.
- **Kragenkante nicht gesäubert.** Die gezackte Farbgrenze Haut/Stoff am V-Ausschnitt ist die alte Textur und
  unverändert. Geschlossen sind die Löcher unter den Kopfhörern, nicht der Kragenrand selbst.
- **Abstand links/rechts ungleich.** Die Kopfhörer sind exakt gespiegelt, Kiefer und Füllung nicht: Sids rechte
  Seite (−X) ist enger (5,3 statt 6,4 mm neutral). Im Extrem `expr_smile` + `expr_mouth_open` bleiben dort 2,8 mm –
  ein Abstand, aber knapp.
- **Mund-Ausdrücke wirken in den Kieferecken interpoliert.** Die dort gelöschten Punkte hatten Deltas; die neuen
  Punkte tragen vom Rand interpolierte (bis 7,4 mm bei `expr_surprised`, 5,0 mm bei `expr_mouth_open`, 4,7 mm bei
  `expr_smile`). Die Summe der Verschiebungen je Key ist deshalb nicht mehr identisch zu v2 (`expr_smile` 109,53
  statt 108,10; `expr_mouth_open` 100,40 statt 98,71). Blink-Keys identisch.
- **Die Muscheln drücken 2,8–3,6 mm in den Stoff**, der Stoff gibt nicht nach (keine Delle modelliert).
- **Der Bügel liegt nirgends wirklich auf.** Seitlich 1,3 mm über dem Kapuzenrand, hinten frei über der Kapuze
  (das war auch in v2 so).
- **Nacken und Haaransatz hinten sind erfunden.** Unter dem alten Bügel gab es keine Vorlage; Form ist die
  geglättete Füllung, die Haarlinie liegt etwa mittig zwischen Haarkante und Hals.
- **Füllflächen grob texturiert** (ca. 1 mm/Texel, nur weiche Farben, keine Normal-Map). Die UV-Inseln sind
  Kreisabbildungen und zum Bemalen ungeeignet.
- **Kopfhörer ohne UVs**, nur einfarbige Materialien; Grundform schlicht (kein Gelenk, keine Nähte am Polster).
  Linke und rechte Muschel sind gespiegelt identisch.
- **`check_v3.py` ist für Durchdringungen unzuverlässig.** Sein Vorzeichentest (Normale der nächsten Fläche) meldet
  am Bügel je nach Ausdruck 0 bis 67 „Durchdringungen“ bis 20 mm, obwohl sich dort nichts bewegt, und an der linken
  Muschel vereinzelt 29 mm. Die Paritätsprüfung bestätigt davon nichts. Die Abstandswerte zur Haut stammen aus dem
  anderen Zweig des Skripts und sind über alle Zustände stimmig.
- Datei 58,9 MB (v2: 39,9 MB), unkomprimiert gespeichert; Ursache des Zuwachses nicht untersucht.
- Alles aus v1/v2 Genannte gilt weiter (kein Retopo, Haar oberhalb der Patches, offene Lidränder innen usw.).

## Nicht geprüft
- Paritätsprüfung nur in der Neutralpose. Für die Ausdrücke gibt es nur die Abstandswerte aus `check_v3.py`.
- Zwischenwerte der Keys und andere Summen als die drei genannten.
- `blender-asset-qa` (`qa_check.py`) ist nicht gelaufen, nur `qa_v2.py`.
- Zwischen Bügel und Haar habe ich keinen Wert für den Endstand gemessen; im Kandidatenvergleich waren es 15 mm,
  in `neck_back`/`neck_side_*` ist der Abstand sichtbar.

## Was die Prüfblätter zeigen (alle 10 Halsbilder angesehen)
- Front, Front tief, beide Dreiviertel: Muscheln unter den Kieferecken, Spalt zur Haut auf beiden Seiten sichtbar.
- Seiten: Bügel → Arm → Gehäuse sauber, Bügel mit Abstand unter der Haarkante, kein Durchstich am Kapuzenrand.
- Hinten: Bügel frei vom Haar, Hals im Spalt zwischen Bügel und Kapuze sichtbar, klare Haarlinie im Nacken.
- `expr_mouth_open` (zwei Ansichten, neben Neutral gelegt): Kinn senkt sich zwischen die Muscheln, Spalt bleibt.
- `neck_under_R`: Die rechte Muschel überlappt im Bild das Ohrläppchen. Das ist Verdeckung durch den Kamerawinkel
  (gemessen 43 mm Abstand), keine Berührung. Am Gehäuserand dort ein heller Saum; vermutlich das Gegenlicht auf der
  Lackschicht, nicht untersucht.
- Die Polsteröffnung wirkt in Schrägansichten als schwarzes Loch (dunkles Gitter-Material).
- Ohne Kopfhörer habe ich nur eigene Vorschauen angesehen (6 Ansichten, 16 Samples), keine Prüfblatt-Qualität.

## GLB-Export (Test, nicht Teil der Abgabe)
`sid_v2/export_glb_pablo.py --meshopt` läuft durch: 8,12 MB (v2: 7,75 MB), 9 Mesh-Knoten, `CH_Sid` 2 Primitive mit je
8 Morph-Targets und den alten Namen, 5 WebP-Texturen. Liegt in `tmp/glb/sid_v3_test.glb`.
- **Nicht in three.js geladen.** Geprüft ist nur der Aufbau der Datei. Die 0,5-mm-Regel ist konstruktiv eingehalten
  (verschachtelte Muschelteile ≥ 1,5 mm versetzt und nicht koplanar, Bügel 1,3 mm über dem Stoff), aber nicht am
  quantisierten Ergebnis angesehen.
- **Neu: drei Material-Erweiterungen** (`KHR_materials_clearcoat`, `_sheen`, `_specular`) durch Coat und Sheen der
  Kopfhörer. Nicht „required“, aber three.js nimmt dafür das teurere MeshPhysicalMaterial. Wer das nicht will:
  `coat`/`sheen` in `hp_model.py` auf 0 setzen.
- **Neu: 12 zusätzliche Primitive** (Bügel 2, Muscheln je 5), also 12 Draw Calls mehr. Ließe sich durch weniger
  Materialien je Muschel senken.

## Dateien in diesem Ordner
- `sid_face_v3.blend` – Abgabe. `sheet_v3/`, `neck_v3/` – Prüfblätter (64 Samples). `neck_v2/` – Stand vorher.
- `scripts/build_v3.py` – Aufbau; neu bauen mit
  `blender -b sid_face_v2_input.blend --python scripts/build_v3.py -- --out sid_face_v3.blend`
- `scripts/hp_params.py` (alle Maße), `scripts/hp_model.py` (Kopfhörer), `scripts/check_v3.py` (Abstände je
  Ausdruck), `scripts/check_parity.py` (Durchdringung), `scripts/tune_hp.py` + `cand.txt` (Kandidatenvergleich),
  `scripts/diag.py` (Nahaufnahmen, `--hide Headphones` rendert ohne Kopfhörer).
- `tex/` – die zwei geänderten Texturen als PNG (in der .blend eingepackt). `tmp/` – Zwischenstände und Logs.
