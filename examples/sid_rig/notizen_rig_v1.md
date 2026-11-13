# Sid rig v1 – Körper-Rig, Gewichte, Prüfposen, Testanimationen

Abgabe: `sid_rig_v1.blend` (in sich geschlossen, 4 Texturen eingepackt, keine Bibliotheken, 40,6 MB,
sha256 `8b9c25fd…`), `exports/sid_rig_v1_web.glb` (9,35 MB, sha256 `97d00f82…`), Prüfbilder in `poses_v1/`, `anim_v1/`,
`sheet_rig_v1/`, `body_rig_v1/`, Vorher/Nachher-Paare in `compare/`. Ausgangsdatei war `sid_rig_input.blend` (= Sid v4).

Das Wichtigste vorweg:

- **Das Rig ist klassisch gebaut und trägt:** Rigify-Steuer-Rig, daraus ein Spiel-Skelett mit 62 Knochen, Gewichte aus
  Formeln entlang der Knochenketten statt aus der Automatik. Alle Prüfposen halten ohne Beulen und Knicke.
- **Die Hände sind neu.** Die Fäustlinge des Generators sind durch modellierte Hände mit fünf getrennten Fingern
  ersetzt. Sie stecken wie bei einer Spielfigur als eigenes, geschlossenes Teil im Bündchen. Dadurch gibt es am
  Handgelenk keinen Bonbon-Effekt.
- **Die Kopfhörer hängen an der oberen Brust, nicht an Hals oder Kopf.** Jede Variante, die dem Kopf folgt, schiebt
  Bügel und Muscheln in Kapuze und Schultern. Der Preis: Der Kopf hat wenig freien Weg, weil die Muscheln 5 mm unter
  dem Kiefer sitzen (flach gedreht 15°, mit 10° angehobenem Kinn 40°). Zahlen in Abschnitt 4.
- **Ein Befund am Export:** Blenders Meshopt-Export packt Animations-Drehungen mit 8 Bit (bis 1,7° Fehler je Knochen,
  bis 6 mm an den Fingerspitzen). Das Export-Skript stellt das für diesen Lauf auf 16 Bit. Abschnitt 6.

## 1. Rig

### Aufbau

Drei Armaturen liegen in der Datei:

- **`RIG_Sid`** – Steuer-Rig zum Animieren, mit Rigify (Blender 5.2.3) erzeugt. 381 Knochen, davon 124 Steuerknochen.
  - Rumpf: `torso` (alles ab Hüfte), `hips`, `chest`, `spine_fk` bis `spine_fk.003`, `neck`, `head`, `shoulder.L/R`.
  - Arme und Beine je mit IK und FK. Umschalten über `upper_arm_parent.L/R["IK_FK"]` und `thigh_parent.L/R["IK_FK"]`
    (0 = IK, 1 = FK). IK: `hand_ik`, `foot_ik`, Abrollen über `foot_heel_ik`, Knie-/Ellbogenrichtung über
    `thigh_ik` / `upper_arm_ik`. FK: `upper_arm_fk`, `forearm_fk`, `hand_fk`, `thigh_fk`, `shin_fk`, `foot_fk`, `toe_fk`.
  - Finger: je drei FK-Glieder (`f_index.01.L` …, `thumb.01.L` …) und ein Master je Finger.
  - `headphones` – eigener Steuerknochen für die Kopfhörer.
  - Gegenüber dem Rigify-Standard geändert (alles in `scripts/stage2_rig.py`):
    - Kein dehnbares IK (`ik_stretch` auf 8 Knochen = 0, `IK_Stretch` = 0). Rigify lässt die Glieder sonst auch
      schrumpfen: in der tiefen Hocke waren die Beine 3,5 % kürzer, und das Spiel-Skelett bekam Skalierungs-Kurven.
    - `torso["head_follow"]` und `["neck_follow"]` = 1. Im Standard (0 / 0,5) bleibt der Kopf am `torso`-Regler
      ausgerichtet, während sich die Wirbelsäule darunter biegt. Jede Rumpfbeuge wurde so zu einer Kopfdrehung gegen
      die Kopfhörer (Bügel 24 mm im Hinterkopf bei `torso_fwd`). Jetzt ist es eine schlichte Hierarchie.
    - Alle Steuerknochen stehen auf Quaternion.
- **`RIG_Sid_Game`** – Spiel- und Web-Skelett: `Root` am Boden (Ursprung) plus 61 Deform-Knochen. Jeder Knochen folgt
  über „Copy Transforms“ seinem Rigify-DEF-Knochen. Alle Meshes sind an dieses Skelett gebunden, in der Datei ist also
  dieselbe Verformung zu sehen, die exportiert wird. Im Viewport ausgeblendet.
- **`RIG_Sid_Meta`** – Rigify-Metarig (ausgeblendet). Das menschliche Metarig ohne Gesicht, Brust- und Becken-Helfer und
  Handflächenknochen, mit einem statt zwei Halsknochen, dazu `headphones`. Die Gelenke sind am Netz ausgemessen
  (`scripts/rigdefs.py`): Schulter (±0,112 | 0,022 | 0,515), Ellbogen (±0,178 | 0,026 | 0,449), Handgelenk
  (±0,242 | 0,007 | 0,384), Hüfte (±0,058 | 0,004 | 0,295), Knie (±0,066 | −0,006 | 0,195), Knöchel
  (±0,078 | 0,012 | 0,085), Ballen (±0,090 | −0,060 | 0,022), Halsansatz z = 0,575, Kopfgelenk z = 0,635. Ellbogen und
  Knie sind um gut 1 cm aus der Geraden gerückt, damit das IK die Beugerichtung kennt.

Dazu kommen 128 Rigify-Widget-Objekte `WGT-RIG_Sid_*` in der ausgeblendeten Sammlung `WGTS_RIG_Sid` und der Textblock
`RIG_Sid_ui.py` (Rigify-Bedienfeld). In der Datei steht außerdem `README_Sid_Rig`.

### Knochenliste des Spiel-Skeletts

Die Namen sind die des Humanoid-Profils von Godot (gleich Unity Humanoid), damit die Zuordnung dort ohne Tabelle geht.
62 Knochen, eine Wurzel. Rechts wie links (`Right…`).

| Knochen | Elternknochen | folgt Rigify | Mixamo-Entsprechung |
|---|---|---|---|
| `Root` | – | `root` | – (Wurzel am Boden, ohne Gewichte) |
| `Hips` | `Root` | `DEF-spine` | Hips |
| `Spine` | `Hips` | `DEF-spine.001` | Spine |
| `Chest` | `Spine` | `DEF-spine.002` | Spine1 |
| `UpperChest` | `Chest` | `DEF-spine.003` | Spine2 |
| `Neck` | `UpperChest` | `DEF-spine.004` | Neck |
| `Head` | `Neck` | `DEF-spine.005` | Head |
| `Headphones` | `UpperChest` | `DEF-headphones` | – (Zusatz) |
| `LeftShoulder` | `UpperChest` | `DEF-shoulder.L` | LeftShoulder |
| `LeftUpperArm` | `LeftShoulder` | `DEF-upper_arm.L` | LeftArm |
| `LeftUpperArmTwist` | `LeftUpperArm` | `DEF-upper_arm.L.001` | – (Zusatz) |
| `LeftLowerArm` | `LeftUpperArm` | `DEF-forearm.L` | LeftForeArm |
| `LeftLowerArmTwist` | `LeftLowerArm` | `DEF-forearm.L.001` | – (Zusatz) |
| `LeftHand` | `LeftLowerArm` | `DEF-hand.L` | LeftHand |
| `LeftThumbMetacarpal` → `…Proximal` → `…Distal` | `LeftHand` | `DEF-thumb.01–03.L` | LeftHandThumb1–3 |
| `LeftIndexProximal` → `…Intermediate` → `…Distal` | `LeftHand` | `DEF-f_index.01–03.L` | LeftHandIndex1–3 |
| `LeftMiddleProximal` → `…Intermediate` → `…Distal` | `LeftHand` | `DEF-f_middle.01–03.L` | LeftHandMiddle1–3 |
| `LeftRingProximal` → `…Intermediate` → `…Distal` | `LeftHand` | `DEF-f_ring.01–03.L` | LeftHandRing1–3 |
| `LeftLittleProximal` → `…Intermediate` → `…Distal` | `LeftHand` | `DEF-f_pinky.01–03.L` | LeftHandPinky1–3 |
| `LeftUpperLeg` | `Hips` | `DEF-thigh.L` | LeftUpLeg |
| `LeftUpperLegTwist` | `LeftUpperLeg` | `DEF-thigh.L.001` | – (Zusatz) |
| `LeftLowerLeg` | `LeftUpperLeg` | `DEF-shin.L` | LeftLeg |
| `LeftLowerLegTwist` | `LeftLowerLeg` | `DEF-shin.L.001` | – (Zusatz) |
| `LeftFoot` | `LeftLowerLeg` | `DEF-foot.L` | LeftFoot |
| `LeftToes` | `LeftFoot` | `DEF-toe.L` | LeftToeBase |

- Die Hauptkette ist rein humanoid (`Shoulder → UpperArm → LowerArm → Hand`, `UpperLeg → LowerLeg → Foot → Toes`). Die
  acht Twist-Knochen sind Blätter daneben.
- So verteilt sich die Drehung um die Längsachse (gemessen, 60° am Regler):
  - 60° am Oberarm: `UpperArm` 0°, `UpperArmTwist` 30°, `LowerArm` 58,5°.
  - 60° an der Hand: `LowerArm` 0°, `LowerArmTwist` 30°, `Hand` 60°.
  - Beine genauso (0° / 30° / 58°; 0° / 28° / 60°).
  - Das obere Gliedstück hängt also an `UpperArm`, das untere an `UpperArmTwist`. Wer in einer Engine nur die
    Humanoid-Knochen ansteuert und die Twist-Knochen in Ruhe lässt, bekommt einen starren Arm ohne Verteilung – wie bei
    jedem Skelett ohne Twist-Logik.
- Kein Knochen wird skaliert, und außer `Root` und `Hips` wird keiner verschoben (beim Backen nachgemessen: größte
  Skalen-Abweichung 0,00016).

### Wie Gesichtsteile und Accessoires hängen

- Alle Meshes sind an `RIG_Sid_Game` geparentet (vorher an `CH_Sid`) und haben einen Armature-Modifier darauf.
- `CH_Sid_Eye_L/R`, `CH_Sid_Brows`, `CH_Sid_Lashes`, `CH_Sid_Mouth`: eine Gruppe `Head`, Gewicht 1. Shape Keys und
  Treiber sind unverändert, der Modifier wirkt nach den Keys.
- `CH_Sid_Headphones_Band`, `_Cup_L`, `_Cup_R`: eine Gruppe `Headphones`, Gewicht 1 (starr). Warum an der oberen Brust,
  steht in Abschnitt 4.
- `CH_Sid_Badge`: Gewichte vom jeweils nächsten Punkt des Hoodies übernommen (`Chest`, `UpperChest`, etwas
  `LeftShoulder`/`LeftUpperArm`). Er folgt damit genau dem Stoff unter ihm.

## 2. Am Modell geändert

Vergleichsbilder: links `checkpoints/sid_v4/sid_face_v4.blend`, rechts die Abgabe, gleiche Kamera, gleiches Licht
(Lichtaufbau der Prüfblätter, `scripts/rshot.py`, Kameras in `scripts/views_compare.txt`), 1000 px, 64 Samples.
`compare/00_gesamt_vorn.png`, `00b_gesamt_hinten.png` und `00c_gesamt_schraeg.png` zeigen die ganze Figur.

1. **Hände: aus den Fäustlingen werden Hände mit fünf getrennten Fingern.**
   `compare/01_hand_R_oben.png`, `01b_hand_R_vorn.png`, `01c_hand_R_unten.png`, `01d_hand_R_aussen.png`,
   `01e_hand_R_fingerspitzen.png`, `01f_hand_L_oben.png`, `01g_hand_L_hinten.png`
   - Stelle und Grund: Beim Generator waren Zeige-, Mittel-, Ring- und kleiner Finger bis kurz vor die Spitzen
     verschmolzen, Mittel- und Ringfinger zu einem Lappen. Damit lässt sich keine Faust und keine gespreizte Hand
     bilden. In den Zielbildern sind es vier Finger und ein Daumen.
   - Gemacht: Die alte Hand ist ab dem Bündchen entfernt (5 993 Punkte samt Bündchen-Ende). Die neue Hand ist aus
     Grundkörpern modelliert: vier Mittelhandknochen als Kegel, ein flaches Polster in der Handfläche, je Finger drei
     Glieder, Daumen mit drei Gliedern, Daumen- und Kleinfingerballen, weich verschmolzen, die Finger untereinander
     nicht. Alle Maße stehen in
     `scripts/handlib.py`. Die Finger sind in Ruhe leicht gekrümmt wie vorher (je Gelenk 10–18°) und leicht gefächert.
     Die Lücken an den Knöcheln sind 2,3–2,6 mm breit und werden zur Spitze weiter.
   - Größe wie vorher: 113 mm lang ab Bündchen (alt 116), 120 mm breit mit Daumen (alt 118).
   - Netz: je Hand ein geschlossenes Teil in `CH_Sid`, 9 501 Punkte, 18 998 Dreiecke (aus einem 1,25-mm-Raster,
     danach auf ein Viertel reduziert). `CH_Sid` besteht jetzt aus drei Stücken.
   - Farbe: Die Hände nutzen `M_Sid_HeadSide`. In den freien Block von `T_Sid_HeadSide_BaseColor/ORM` (Pixel 684–1022 ×
     2–215) ist der Hautton der alten Hände geschrieben (sRGB 252/171/146, Rauheit und Metallic wie vorher). Zwischen
     den Fingern und in den Beugefalten ist er etwas dunkler und rötlicher, berechnet aus der Form. Kein drittes
     Material, keine Vertexfarben, im Browser also sichtbar.
   - Gebeugt (nur nachher, in v4 gab es kein Rig): `poses_v1/04_haende.png`, neben dem Zielbild
     `poses_v1/24_ziel_haende.png`.

2. **Bündchen: Die Hand steckt im Ärmel, statt mit ihm verwachsen zu sein.**
   `compare/02_buendchen_R.png`, `02b_buendchen_R_unten.png`, `02c_buendchen_L_oben.png`
   - Grund: Bei einem durchgehenden Netz muss das Handgelenk jede Drehung der Hand zwischen Ärmel und Hand
     aufnehmen (Bonbon-Effekt). Steckt die Hand im Bündchen, dreht sie sich darin wie bei einer Spielfigur.
   - Gemacht: Der Ärmel ist 3 mm hinter der alten Farbgrenze Haut/Stoff eben abgeschnitten. Der Rand ist auf den
     letzten 5 mm nach innen gezogen (311 und 315 Punkte, bis 7,3 und 7,9 mm), so dass die Öffnung eine saubere
     Ellipse von 77 × 62 mm ist. Dahinter liegt eine 6,5 mm tiefe, dunkle Tasche als Abschluss.
   - Das Handgelenk der neuen Hand ist an dieser Stelle rundum 1–3 mm größer als die Öffnung, der Bündchenrand sitzt
     also leicht in der Haut. In der Beuge-Ebene ist das Handgelenk kreisrund um das Gelenk. Beim Beugen und Strecken
     ändert sich die Naht deshalb nicht.
   - Geprüft für den Web-Export: 80 und 79 Punkte der Hand liegen näher als 1 mm am Ärmel, alle an der Schnittlinie.
     Keiner davon liegt parallel zur Ärmelfläche (`scripts/qa_final.py`), es gibt also keine fast deckungsgleichen
     Flächen.
   - Die gezackte Farbgrenze Haut/Stoff an den Handgelenken aus v4 (dort Punkt 7) ist damit weg.

3. **Achseln: ausgefranster dunkler Saum und heller Fleck in der Textur, feine Grate im Netz.**
   `compare/03_achsel_L_vorn.png`, `03b_achsel_L_hinten.png` (Ruhepose, dort ist kaum etwas zu sehen);
   mit gehobenem Arm: `compare/03c_achsel_arme_hoch_hinten.png`, `03d_…_seite.png`, `03e_…_vorn.png`, dazu dieselben
   Ansichten als reine Farbe (`…_albedo.png`). Links steht dort das Rig mit Achsel-Textur und -Netz von v4.
   - Grund: In der A-Pose liegt die Achsel im Verborgenen. Sobald der Arm hochgeht, kommt dort ein Stück Textur ans
     Licht, das der Generator nie sauber gemalt hat: ein hellerer Fleck mit ausgefranstem, dunklem Rand. Dazu feine
     Grate im Netz, die als Streifen glänzen.
   - Gemacht an der Textur: Im Umkreis von 6,5 cm um jede Achsel (bis 9 cm auslaufend) sind Farbe, AO, Rauheit und
     Metallic durch einen glatten Verlauf aus dem umliegenden Stoff ersetzt, samt einem 6 Texel breiten Rand um die
     betroffenen UV-Inseln. Ohne den Rand blutete die alte dunkle Randfarbe als feine, gezackte Linie entlang der
     UV-Nähte durch. In `T_Sid_BaseColor` sind 181 739 Texel geändert, davon 29 958 um mehr als 6 von 255 Stufen; in
     `T_Sid_ORM` 203 910, davon 121 956 um mehr als 6 Stufen.
   - Gemacht am Netz: Glättung ohne Schrumpfen (Taubin, 12 Durchgänge) im Umkreis von 6 cm, ab 3,5 cm auslaufend.
     1 033 und 1 089 Punkte bewegt, höchstens 1,7 und 2,1 mm.
   - Geblieben sind die großen Falten, die von der Achsel ausstrahlen. Das sind modellierte Stofffalten.

Sonst ist am Modell nichts geändert. Kopf, Gesicht, Haare, Hoodie-Körper, Hose, Schuhe, Kopfhörer und Anstecker sind
punktgleich mit v4 (Abschnitt 8). Neu an `CH_Sid` sind zwei Hilfsattribute: `orig_id` (Punktnummer in v4 plus 1, 0 =
neuer Punkt) und `hand_side` (+1 linke Hand, −1 rechte Hand). Sie machen den Vergleich mit v4 nachprüfbar und werden
nicht exportiert.

## 3. Gewichte

### Verfahren

Keine Gewichts-Automatik. Sids Netz ist verschmolzen und sehr dicht, dort verteilt die Automatik unruhig und zieht
Kapuze und Haare mit. Stattdessen (`scripts/stage3_weights.py`):

- **Körper:** Für jeden Punkt werden die Gewichte aus seiner Lage zu den Knochenketten gerechnet.
  - Arm oder Rumpf entscheidet der Abstand zur Armachse und die Lage hinter der Schulterebene.
  - Entlang von Arm und Bein: weiche Übergänge an Ellbogen und Knie (±2,4 und ±2,1 cm). Die Außenseite (Ellbogenspitze,
    Kniescheibe) bleibt 7–8 mm länger beim oberen Knochen, das hält das Volumen.
  - Twist-Knochen: weicher Übergang über die Mitte jedes Gliedstücks.
  - Rumpf: nach Höhe auf `Hips`, `Spine`, `Chest`, `UpperChest` (Übergänge ±3,2 cm), an den Schultern bis 70 %
    `Shoulder`.
  - Hüfte: Die Beugelinie läuft vom Schritt schräg zur Hüftseite. Vorn ist der Übergang eng, hinten am Gesäß weiter und
    3 cm tiefer.
  - Hoodie-Saum: folgt dem Oberschenkel höchstens zu 45 %, nach oben auslaufend.
  - Kapuze: ganz an `UpperChest`.
  - Danach 24 Durchgänge Glättung über das Netz und 36 weitere nur um Schultern und Achseln.
- **Kopf und Hals:** Der Kopfbereich ist per Flutfüllung vom Scheitel bis zum Kragen bestimmt (112 673 Punkte). Alles
  oberhalb des Halses hängt starr an `Head`. Am Hals läuft das Gewicht über 3,6 cm entlang der Oberfläche vom Kragen
  (`UpperChest`) über `Neck` nach `Head`.
- **Schuhe:** unterhalb von z = 9 cm starr an `Foot` bzw. `Toes`. Der Knick liegt am Ballen und ist ±9 mm breit.
  Zwischen Schuhkragen und Hosensaum ein 3,4 cm breiter Übergang zum Unterschenkel.
- **Hände:** aus der Hand-Konstruktion gerechnet. Jeder Punkt gehört zu dem Finger, dessen Grundkörper ihm am nächsten
  ist, und wird an den drei Gelenken über ±4 bis ±6,5 mm überblendet (Daumenwurzel ±9 mm). Das Handgelenk hängt starr an `Hand`.
- Am Ende höchstens 4 Einflüsse je Punkt, normalisiert. In `CH_Sid` haben 141 053 Punkte einen Einfluss, 30 195 zwei,
  11 281 drei und 4 094 vier. Keiner ist ohne Gewicht, die Summe ist überall 1,0000.

### Wie ich geprüft und nachgebessert habe

Geprüft habe ich an Bildern, nicht an Zahlen: jede Prüfpose ganz, dann jedes kritische Gelenk in Nahansichten von
mehreren Seiten, in Farbe und als einfarbiges Tonmodell (das zeigt Grate und Dellen ohne Textur), dazu eine
Farbdarstellung der Gewichte. Das waren rund 40 Render-Durchläufe mit zusammen etwa 500 Bildern. Die Endstände liegen
in `poses_v1/`. Nachgebessert habe ich nach dem Ansehen:

- **Saum hinten:** Beim Knieheben zeigte der Hoodie-Saum hinten einen Sägezahn-Rand. Ursache war meine Trennung von
  Saum und Hose nach Farbklasse, die in der Nut dazwischen von Punkt zu Punkt sprang. Jetzt entscheidet nur die Höhe.
- **Gesäß:** Die Beugelinie lag hinten zu hoch, die versteckte Nut zwischen Saum und Hose klappte auf. Hinten liegt sie
  jetzt 3 cm tiefer.
- **Achseln:** Der Übergang Arm/Rumpf war zu schmal und gab bei gehobenem Arm Grate. Dafür der zweite
  Glättungs-Durchgang (und Punkt 3 am Modell).
- **Finger:** Die Beugerichtung war im ersten Anlauf verkehrt (die „Faust“ war eine überstreckte Hand). Der Fehler lag
  in den Posen, nicht in den Gewichten.
- **Hocke und Ausfallschritt:** Beine 3,5 % kürzer durch Rigifys dehnbares IK, abgestellt (Abschnitt 1).
- **Rumpfbeugen:** Kopf blieb stehen und drückte in die Kopfhörer, abgestellt (Abschnitt 1).

Was die Bilder zeigen, Gelenk für Gelenk:

- Schultern und Achseln (`poses_v1/01_schulter_achsel.png`): Arme hängend, zur Seite, nach hinten und nach oben geben
  glatte Schultern. Die Rumpfseite geht beim Heben mit, wie im Zielbild.
- Ellbogen (`02_ellbogen.png`): Der weite Ärmel behält sein Volumen. Bei stark gebeugtem Arm schiebt er sich in der
  Beuge ineinander.
- Handgelenk (`03_handgelenk.png`): 65° gebeugt und gestreckt, 28° zur Seite, 85° gedreht – die Hand dreht sich im
  Bündchen, der Ärmel bleibt unverzerrt.
- Hände (`04_haende.png`): Faust mit eingeschlagenem Daumen, gespreizte Hand.
- Hüfte, Schritt, Knie, Saum (`05_huefte_knie.png`): Hocke, Ausfallschritt, Bein 50° zur Seite, Knie 80° gehoben,
  Unterschenkel nach hinten.
- Schuhe (`06_schuhe.png`): starr, Knick nur am Ballen.
- Rumpf (`07_rumpf.png`): 42° vor, 24° zurück, 48° gedreht, 26° zur Seite. Die Kapuze bleibt in Form.
- Kopf und Hals (`08_kopf_hals.png`, ohne Kopfhörer und weiter gedreht `09_hals_ohne_kopfhoerer.png`): Der Hals
  verdreht sich sauber, der Kragen bleibt stehen.
- Ausdruck bei gedrehtem Kopf (`10_ausdruck_bei_gedrehtem_kopf.png`): `expr_smile` und `expr_mouth_open` wirken auch
  mit gedrehtem und genicktem Kopf.

## 4. Kopfhörer: woran sie hängen

Ergebnis: **an `UpperChest`, starr, ohne dem Kopf zu folgen.**

Gemessen habe ich, wie tief Bügel und Muscheln in den Körper tauchen (`scripts/hp_test.py`, Strahl-Parität, jeder
zweite Punkt der drei Objekte, tiefster Punkt in mm). In Ruhe sind es 3,6 mm – die Muscheln drücken seit v3 so weit in
den Stoff. Alles darüber ist neu. Winkel = Kopf gegenüber der Brust.

| Kopfpose | obere Brust | Hals | Kopf | Brust, dreht 30 % mit | Brust, dreht 50 % mit |
|---|---|---|---|---|---|
| 30° gedreht | 13,6 | 14,7 | 37,3 | 13,5 | 21,3 |
| 45° gedreht | 19,8 | 21,3 | 43,2 | 19,3 | 30,2 |
| 40° gedreht, Kinn 10° hoch | **4,8** | 16,7 | 37,4 | 15,4 | 23,0 |
| 15° genickt | 9,9 | 7,3 | 23,7 | 6,9 | 9,2 |
| 20° nach oben | 7,8 | 9,4 | 18,5 | 8,8 | 12,2 |
| 14° geneigt | 8,0 | 7,0 | 19,8 | 6,7 | 8,7 |
| 30° gedreht und 10° genickt | 24,9 | 17,2 | 43,2 | 15,5 | 23,7 |

- Am Kopf ist es überall am schlechtesten: Muscheln und Bügel pflügen durch Schultern und Kapuze.
- Am Hals oder mit 30 % Mitdrehen ist es beim Nicken und Neigen 1–3 mm besser als an der Brust. Dafür gibt es dort
  keine Kopfdrehung ohne Eintauchen: Was am Kinn gewonnen wird, taucht in Schulter und Kapuze.
- An der Brust gibt es sie: Mit leicht gehobenem Kinn geht der Kiefer über die Muschel hinweg (Zeile 3). Deshalb die
  Brust. Die Kopfhörer liegen auf Kapuze und Schultern auf, und dort bleiben sie.
- Schwach ist die Brust, wenn der Kopf zugleich dreht und nickt (letzte Zeile): Dann geht das Kinn geradewegs in
  die Muschel.

Der Haken ist der Platz: Die Muscheln sitzen 5–6 mm unter den Kieferecken. Freier Weg des Kopfes gegenüber der Brust
(Hals und Kopf zusammen, `scripts/hp_limits.py`, Werte = tiefster Punkt in mm, 3,6 = wie in Ruhe):

| Drehung | Kinn gerade | Kinn 5° hoch | Kinn 10° hoch | Kinn 15° hoch |
|---|---|---|---|---|
| 10° | 3,6 | 3,6 | 3,6 | 3,6 |
| 15° | 4,3 | 3,6 | 3,6 | 4,4 |
| 20° | 7,4 | 3,6 | 3,6 | 5,7 |
| 30° | 13,6 | 7,2 | 3,6 | 8,4 |
| 40° | 18,5 | 11,6 | 4,8 | 10,3 |
| 50° | 20,4 | 13,4 | 6,4 | 11,1 |

- Nicken nach unten: frei bis 8°, bei 10° 5,0 mm, bei 15° 9,9 mm, bei 20° 14,5 mm (beide Muscheln).
- Nach oben: frei bis 15°, bei 20° liegen die Haare 7,8 mm im Bügel.
- Zur Seite neigen: frei bis 10°, bei 14° 8,0 mm.
- Faustregel fürs Animieren: Wer den Kopf dreht, hebt das Kinn um ein Viertel des Drehwinkels. Dann sind 40° frei.

Die Prüfposen für den Kopf liegen deshalb innerhalb dieses Bereichs (`head_turn` 40° mit 10° Kinn hoch, `head_down`
10°, `head_up` 15°, `head_tilt` 10°). `head_turn_R` ist bewusst eine flache Drehung um 30°, also über den freien Bereich
hinaus: Dort drückt das Kinn 14 mm in die rechte Muschel.

Dasselbe gilt für die Arme, denn die Muscheln liegen vorn auf den Schultern (`scripts/hp_arms.py`):

- Arm nach vorn schwingen: frei bis 55°, bei 70° 6 mm, waagrecht nach vorn 36 mm (`arms_forward_max`).
  Die Pose `arms_forward` greift deshalb mit gebeugtem Ellbogen nach vorn.
- Arme zur Seite: frei bis über die Waagrechte. Steiler als etwa 40° über der Waagrechten drücken die Ärmel in den
  Bügel (`arms_up_max`, fast senkrecht: 18 mm). Die Pose `arms_up` folgt dem Zielbild: Oberarme schräg nach außen,
  Unterarme senkrecht, Handflächen nach vorn (Bügel 2,2 mm, Muscheln 5,4 mm).
- Alle anderen Prüfposen und `anim_idle`, `anim_walk` liegen bei höchstens 5 mm, `anim_wave` bei 7 mm (rechte Muschel,
  weil die Schulter hochgeht).

## 5. Prüfposen und Testanimationen

Vier Actions auf `RIG_Sid`, 24 Bilder je Sekunde, alle mit Fake User. In der Abgabedatei ist keine Action zugewiesen,
die Figur steht in der Ruhepose (A-Pose).

- **`qa_poses`**, Frames 1–485: 29 Posen, jede 8 Frames gehalten, dazwischen 8 Frames Übergang. Die Beine sind für
  Hocke und Ausfallschritt auf IK, sonst auf FK. Umgeschaltet wird in der Ruhepose (`rest_ik`, `rest_fk`), wo beide
  Ketten deckungsgleich sind. Die Posennamen stehen als Pose-Marker in der Action und in ihrer Eigenschaft `pose_frames`.

  | Frames | Pose | | Frames | Pose |
  |---|---|---|---|---|
  | 1–9 | rest | | 251–259 | squat (Hocke) |
  | 17–25 | arms_up | | 267–275 | lunge (Ausfallschritt) |
  | 33–41 | arms_up_max | | 293–301 | leg_side |
  | 49–57 | arms_side | | 309–317 | knee |
  | 65–73 | arms_forward | | 325–333 | leg_back (mit Zehenknick) |
  | 81–89 | arms_forward_max | | 341–349 | torso_fwd |
  | 97–105 | arms_down | | 357–365 | torso_back |
  | 113–121 | arms_back | | 373–381 | torso_twist |
  | 129–137 | elbows | | 389–397 | torso_side |
  | 145–153 | elbows_max | | 405–413 | head_turn |
  | 161–169 | wrist_flex | | 421–429 | head_turn_R |
  | 177–185 | wrist_side_twist | | 437–445 | head_down |
  | 193–201 | fist_half | | 453–461 | head_up |
  | 209–217 | fist | | 469–477 | head_tilt |
  | 225–233 | spread | | | |

  Übersichten: `poses_v1/00_qa_poses_vorn.png` und `00_qa_poses_schraeg.png`.
- **`anim_idle`**, Frames 1–97, Schleife (Frame 97 = Frame 1, Unterschied am Spiel-Skelett 0,0000 mm): Arme hängen
  locker, ein Atemzug in 4 Sekunden (Brust, Schultern, Kopf gleicht aus), leichte Gewichtsverlagerung, die Finger
  arbeiten mit. `anim_v1/anim_idle.png`
- **`anim_walk`**, Frames 1–33, Schleife (Frame 33 = Frame 1, 0,0000 mm): Gehen auf der Stelle, zwei Schritte in 1,33 s.
  Füße über IK mit Fersenaufsatz, Abrollen über den Ballen und Zehenknick, Becken und Brust drehen gegeneinander, Arme
  schwingen gegengleich mit mehr Beuge vorn. Nach dem Aufsetzen läuft der Fuß in der Standphase gleichmäßig mit rund 7,8 mm je Frame
  nach hinten. `anim_v1/anim_walk.png`
- **`anim_wave`**, Frames 1–80: aus der Idle-Haltung den rechten Arm heben, gut dreimal winken mit nachlaufender Hand,
  Handfläche nach vorn, Oberkörper und Kopf gehen leicht mit, zurück. Erster und letzter Frame sind gleich und gleich
  dem ersten Frame von `anim_idle`. `anim_v1/anim_wave_a.png`, `anim_wave_b.png`
  - Er winkt mit der **rechten** Hand, wie im Auftrag. Das Zielbild winkt mit der linken. Rechts lässt den Anstecker
    auf der linken Brust frei.
- Neben den Zielbildern: `poses_v1/20_ziel_arme_hoch.png`, `21_ziel_winken.png`, `22_ziel_gehen.png`,
  `23_ziel_hocke.png`, `24_ziel_haende.png`. Die Hocke ist flacher als im Zielbild, weil Sids Beine dort länger sind
  als am Modell (Hüfte bis Knöchel 21 cm).

## 6. Web-Export

`scripts/export_glb.py` (aus `export_glb_v4_vorlage.py` erweitert), Aufruf im Skriptkopf.

- Ablauf: Shape Keys auf 0. Das Steuer-Rig spielt jede Action ab, dabei wird das Spiel-Skelett Frame für Frame
  abgetastet. Dann werden in der laufenden Sitzung Steuer-Rig, Metarig und Widgets entfernt, die Constraints gelöscht
  und vier gebackene Actions gleichen Namens auf `RIG_Sid_Game` angelegt. Gespeichert wird davon nichts.
- Inhalt der GLB (`glb_info.py`): 1 Skin mit 62 Joints, 10 Mesh-Knoten (alle mit Skin), `CH_Sid` mit 2 Primitiven und
  8 Morph-Targets, Gesichtsteile mit ihren Targets wie in v4, 4 WebP-Texturen, 4 Animationen (`qa_poses` 20,17 s,
  `anim_idle` 4,00 s, `anim_walk` 1,33 s, `anim_wave` 3,29 s), Meshopt.
- Keine Morph-Animation in den Clips (`export_morph_animation` aus). Sonst schreibt der Exporter für die drei Objekte
  mit Treibern (Brauen, Wimpern, Mund) Gewichts-Spuren in jede Animation, und die überschreiben im Viewer die
  Ausdrucks-Regler, sobald ein Clip läuft.
- **Meshopt und Drehungen:** Blenders Exporter filtert Animations-Quaternionen mit 8 Bit. Gegenüber einem Export ohne
  Meshopt lagen einzelne Knochen bis 1,7° daneben und die Fingerspitzen bis 6,4 mm; langsame Bewegungen wie das Atmen
  würden stufig. Das Skript setzt `QUAT_FILTER_BITS` im Exporter-Modul für diesen Lauf auf 16, das ist die volle
  Genauigkeit derselben Kodierung. Der Decoder muss dafür nichts wissen, Blender selbst bleibt unverändert. Die
  Positionen bleiben bei den üblichen 12 Bit (bis 0,41 mm), wie in den bisherigen Exporten.
- **Kontrolle durch Wieder-Import** (`scripts/verify_glb.py`, `logs/verify_glb.txt`):
  - Skelett: 62 Knochen, eine Wurzel `Root` bei (0 | 0 | 0), Hierarchie wie in der Tabelle oben.
  - Gewichte: alle 10 Meshes am Skelett, höchstens 4 Einflüsse, Summe 1,000, kein Punkt ohne Gewicht.
  - Keys: alle Namen da (`CH_Sid` 8, Brauen 4, Wimpern 7, Mund 5, Augen je 4).
  - Animationen: 4 Actions mit den richtigen Längen.
  - Verformung: An je zwei Frames jeder Animation sind die verformten Punkte von `CH_Sid`, Mund und Bügel mit der
    Quelle verglichen (24 Vergleiche): größte Abweichung 0,41–1,01 mm, im Mittel 0,20–0,70 mm. In einem Probe-Export ohne Meshopt waren es
    0,001–0,009 mm, der Rest ist also die Quantisierung.
- **Nicht in three.js geladen.** Geprüft sind Aufbau und Wieder-Import in Blender.
- Für den Viewer:
  - Die Treiber kommen wie bisher nicht mit. Ausdrücke müssen auf `CH_Sid` und den Gesichtsteilen gesetzt werden.
  - Die Animationen enthalten für jeden Knochen auch Verschiebungs- und Skalen-Spuren. Sie sind konstant (der Exporter
    schreibt sie so), außer an `Hips`.
  - `KHR_materials_clearcoat`, `_sheen` und `_specular` stammen wie in v3/v4 von den Kopfhörern.
  - Die Datei ist 9,35 MB groß (v4 ohne Rig: 7,92 MB). Der Zuwachs sind Gewichte, Animationen und die Hände.

## 7. Gesehen, aber nicht behoben

- **Kopfhörer und Bewegungsfreiheit** (Abschnitt 4): Kopf flach nur 15° frei, Arm nach vorn nur bis 55°. Das liegt an
  der Lage der Muscheln unter dem Kiefer und auf den Schultern, nicht an den Gewichten. Mehr Luft hieße, die
  Kopfhörer tiefer oder weiter außen zu setzen oder die Muscheln einzeln beweglich zu machen. Beides ist eine
  Entwurfsfrage und ginge gegen die Zielbilder.
- **Kragenrand im Nacken:** Die Farbgrenze Stoff/Haut ist dort gezackt (bekannt aus v4). Sie liegt unter dem Bügel und
  wird beim Nicken sichtbar (`poses_v1/09_hals_ohne_kopfhoerer.png`). Nicht angefasst, weil sie zur Textur der Kapuze
  gehört und nichts mit der Verformung zu tun hat.
- **Stofffalten an der Achsel:** Bei gehobenem Arm bleiben die ausstrahlenden Falten und feine Glanzstreifen an der
  Rumpfseite. Die Falten sind modelliert, die Streifen sind die aus v4 bekannten Facetten des Hoodies.
- **Ellbogenbeuge:** Bei stark gebeugtem Arm (`elbows_max`) schiebt sich der Ärmel innen ineinander. Sauber ginge das
  nur mit einer Korrekturform je Seite. Bei dem weiten Ärmel fällt es nicht auf.
- **Kniekehle und Hocke:** Ober- und Unterschenkel berühren und durchdringen sich in der tiefen Hocke hinten leicht.
- **Hoodie-Saum:** Er folgt dem Oberschenkel nur teilweise und legt sich in der Hocke nicht wie Stoff über die Beine.
  Die Nut zwischen Saum und Hose hat innen eine gezackte Farbgrenze, die bei stark gehobenem Bein am Saumrand als
  feiner, unruhiger Strich zu ahnen ist.
- **Schuhkragen:** Der obere Rand des Schuhs und der Hosensaum teilen sich einen 3,4 cm breiten Übergang, der
  Schuhkragen gibt beim Abrollen also etwas nach. Mit einem Schnitt wie am Bündchen wäre er starr; das habe ich nicht
  gemacht, weil Hose und Schuh dort bündig aufeinandersitzen und keine Lippe haben.
- **Kordeln und Kapuze:** Die Hoodie-Bänder sind Teil des Körpernetzes und hängen fest am Stoff, die Kapuze ist starr.
  Beide schwingen nicht nach.
- **Gehen:** Der Fußballen taucht beim Abrollen bis 2,7 mm unter den Boden.

## 8. Gesicht und Ausdrücke erhalten – wie geprüft

- **Punkt für Punkt gegen v4** (`scripts/keys_check.py`, `logs/keys_check.txt`; die Meshes aus
  `checkpoints/sid_v4/sid_face_v4.blend` werden dazugeladen, `CH_Sid` wird über `orig_id` zugeordnet):
  - Alle Objekte: gleiche Key-Namen, gleiche Treiber, gleiche Materialien.
  - `CH_Sid`: 166 515 der 172 508 Punkte aus v4 sind übernommen, 5 993 entfernt (alte Hände und Bündchen-Enden),
    20 108 neu. Für alle 8 Keys ist die größte Abweichung der Verschiebung gegenüber v4 **0,000000 mm**, die Summen sind
    gleich (z. B. `expr_smile` 109,5265). Die entfernten Punkte trugen in keinem Key eine Verschiebung, die neuen
    tragen keine.
  - Bewegt wurden 2 424 übernommene Punkte (Bündchenränder und Achseln, höchstens 7,8 mm). Keiner davon wird von
    einem Key bewegt.
  - Augen, Brauen, Wimpern, Mund, Kopfhörer, Anstecker: Positionen und Key-Verschiebungen 0,000000 mm Abweichung.
- **Texturen:** In `T_Sid_HeadSide_*` sind 74 298 Texel geändert, alle im vorher unbenutzten Block. In `T_Sid_BaseColor`
  und `T_Sid_ORM` liegen alle Änderungen in den UV-Inseln der Achseln und ihrem Rand.
- **Im Bild** (`scripts/facediff.py`, `sheet_rig_v1` gegen `checkpoints/sid_v4/sheet_v4`, nur die Gesichtsfläche):
  in allen 21 Kopfansichten (neutral von fünf Seiten, jeder der 8 Ausdrücke von vorn und im Dreiviertelprofil) liegen
  0,000 % der Pixel über der Schwelle 12/255. Größte Einzelabweichung 9 Stufen, mittlere Abweichung 0,01–0,03 Stufen.
- **Körper im Bild** (`body_rig_v1` gegen `checkpoints/sid_v4/body_v4`, `logs/bodydiff.txt`): Über der Schwelle
  unterscheiden sich nur Bilder, in denen Hände und Bündchen zu sehen sind: die acht Hand-Ansichten zu 6–13 %, die
  Ganzfigur zu 0,4–0,8 %, der Rumpf zu 1,0–2,4 %, das Haar von oben zu 0,9 % (die Hände liegen dort am Bildrand).
  Füße, Beine und Haar von hinten: unter 0,01 %.
- **Mit Rig:** Ausdruck bei gedrehtem und genicktem Kopf gerendert (`poses_v1/10_ausdruck_bei_gedrehtem_kopf.png`).
- **Netz** (`scripts/qa_final.py`): `CH_Sid` 0 nicht-mannigfaltige Kanten, 0 lose Punkte, 0 Null-Flächen; offene Ränder
  weiter nur die 3 Lid- und Lippenschleifen (574 Kanten). Drei Stücke: Körper und zwei Hände.

## 9. Bekannte Schwächen und was es für ein Spiel noch bräuchte

- **Kein Retopo.** `CH_Sid` hat 186 623 Punkte und 372 682 Dreiecke (v4: 344 460; die Hände bringen 38 000). Im GLB
  werden daraus durch die vielen kleinen UV-Inseln 472 470 Punkte, die alle geskinnt werden. Für ein Spiel braucht es
  ein Netz mit einem Zehntel davon und LODs. Die Gewichte ließen sich dann neu rechnen, das Verfahren hängt nicht an
  der Punktzahl.
- **Eine komplette Retopologie war für gute Verformung nicht nötig.** Die Dichte reicht überall. Nötig waren nur
  die Hände.
- **Hände sind schlicht:** keine Nägel, keine Handlinien, Farbe fast einheitlich. Die Finger sind etwas schlanker als
  in den Zielbildern.
- **Bewegungsfreiheit von Kopf und Armen** ist durch die Kopfhörer begrenzt (Abschnitt 4). Ein Spiel müsste den
  Kopf-Blick begrenzen oder mit dem Kinn koppeln.
- **Twist-Knochen:** In den gebackenen Clips stimmen sie. Steuert eine Engine den Arm selbst (IK, Retargeting), muss
  sie die acht Twist-Knochen mitführen (halbe Verdrehung des Folgeknochens) oder auf die Verteilung verzichten.
- **Keine Korrekturformen, keine Nebenbewegung:** Haare, Kapuze, Kordeln und Kopfhörer sind starr.
- **Animationen sind Testclips.** Alles ist per Skript gesetzt, nicht von Hand poliert: Das Gehen ist gleichmäßig
  und brav, ohne Vorwärtsbewegung der Wurzel. Blinzeln und Ausdrücke sind nicht Teil der Clips.
- **Steuer-Rig nur per Skript bewegt.** Ich habe die Datei nicht in einer Blender-Oberfläche geöffnet. Das
  Rigify-Bedienfeld (`RIG_Sid_ui.py`) und das Umschnappen IK/FK sind ungeprüft. Neu erzeugen lässt sich das Rig nur
  über `scripts/stage2_rig.py`, weil nach dem Erzeugen die Änderungen aus Abschnitt 1 und das Spiel-Skelett
  dazukommen.
- **Nicht in three.js oder Godot geladen.** Die Namen passen zum Humanoid-Profil von Godot, die Zuordnung dort habe
  ich nicht ausprobiert.
- **Meshopt-Genauigkeit** hängt an einer Zeile im Export-Skript (Abschnitt 6). Wer anders exportiert, bekommt wieder
  8 Bit.
- **Links und rechts sind nicht spiegelgleich gewichtet.** Die Formeln sind dieselben, das Generator-Netz ist es
  nicht ganz. Die Hände sind exakt gespiegelt.
- Alles aus v1–v4 Genannte gilt weiter (offene Lid- und Lippenränder innen, Kopfhörer ohne UVs, weiche Farbgrenzen).

## Aufwand

Rund 40 Render-Durchläufe mit etwa 500 Bildern (Diagnose, Posen in Farbe und als Tonmodell, Gewichtsfarben,
Animationsstreifen), dazu die Abgabe-Bilder (281 Einzelbilder, 53 Prüfblatt-Bilder; sie liefen nach späten
Korrekturen mehrmals) und rund 60 Bau- und Mess-Läufe. Knapp drei Stunden. Renders auf GPU 0, die Prüfblatt-Skripte auf der CPU. Kein Internet, keine Generatoren, kein Blender-MCP.

## Dateien in diesem Ordner

- `sid_rig_v1.blend` – Abgabe. `exports/sid_rig_v1_web.glb` – Web-Export.
- `poses_v1/` – Posenblätter (`00_…` Übersicht, `01_…` bis `10_…` Nahansichten, `20_…` bis `24_…` neben den
  Zielbildern). `anim_v1/` – Streifen je Animation. `sheet_rig_v1/`, `body_rig_v1/` – Prüfblätter der Ruhepose
  (64 Samples). `compare/` – Paare v4 / Abgabe.
- Einzelbilder zu allen Blättern liegen jeweils im Unterordner `einzeln/`.
- `stage1_model.blend` … `stage4_anim.blend` – Zwischenstände (können weg): Modell, Rig, Gewichte, Actions.
- `tmp/stage4_before_armpitgeo.blend` und `tmp/tex_v4_main/` – nur für die linke Hälfte der Achsel-Paare 03c–03e
  (Rig mit Achsel-Netz und -Textur wie v4). `tmp/dump/` – Netz und Texturen von v4 als Ausgang der lokalen Skripte.
- `scripts/` – alles zum Neubauen, in dieser Reihenfolge:
  `stage1_model.py` (Hände, Bündchen, Achseln, Texturen) → `stage2_rig.py` (Metarig, Rigify, Spiel-Skelett) →
  `stage3_weights.py` → `stage4_anim.py` (`poses.py`, `poselib.py`) → `finalize.py` → `export_glb.py`.
  Die Befehle stehen in den Skriptköpfen. `handlib.py` und `rigdefs.py` enthalten alle Maße.
  `scripts/data/` – Hand-Netz, Gelenke, Farbklassen der v4-Punkte, die geänderten Texturen als PNG.
- Auf dem Arbeitsrechner gerechnet (numpy, OpenCV; liegen zur Dokumentation in `scripts/local/`, mit lokalen Pfaden):
  `hand_build.py` (Hand-Netz aus `handlib.py`), `hand_tex.py`, `armpit_tex.py`, `an_classify.py` (Farbklassen),
  `an_*.py` (Vermessung), `compose.py` (Bildblätter), `glb_info.py`, dazu die Aufruf-Skripte (`build.sh` baut alle
  Stufen).
- Prüfung: `qa_final.py`, `keys_check.py`, `verify_glb.py`, `cmp_glb.py`, `loop_check.py`, `hp_test.py`,
  `hp_limits.py`, `hp_arms.py`; Bilder: `rshot.py`, `final_renders.sh`. Ausgaben in `logs/`.
