# Sid v4 – Aufräumrunde am ganzen Modell

Abgabe: `sid_face_v4.blend` (in sich geschlossen, 4 Texturen eingepackt, keine Bibliotheken, 36,9 MB), Prüfblätter in
`sheet_v4/`, `neck_v4/`, `body_v4/`, Vorher/Nachher-Paare in `compare/`. Ausgangsdatei war `sid_face_v3_input.blend`.

Der wichtigste Befund vorweg: Die meisten „Risse“ – im Haar, an den Kordel-Ansätzen, unter den Achseln, an der
Kapuzen-Schulter-Kante, zwischen den Fingern – waren weder Geometrie noch Farbe. Die Geometrie ist dort glatt, die
Farbtextur sauber. Sie kamen aus kaputten Flecken in der **Normal-Map** des Generators (5,2 % der benutzten Texel,
im Haar 11,4 %). Das hat eine einzige Reparatur am ganzen Modell behoben.

## Verbessert

Alle Vergleichsbilder: links v3 (`checkpoints/sid_v3/sid_face_v3.blend`), rechts v4, gleiche Kamera, gleiches Licht
(Lichtaufbau der Prüfblätter, `scripts/shot.py`, Kameras in `scripts/views_compare.txt`), 1000 px, 64 Samples.

1. **Haar: Risse, Splitter, braune Spalten, fleckiger Glanz.**
   `compare/01_haar_hinten.png`, `01b_haar_seite.png`, `01c_haar_vorn.png`, `01d_haar_oben.png`
   - Unsauber: Zwischen den Strähnen sahen die Spalten aus wie aufgeplatzt – schwarze Löcher, abstehende Splitter,
     helle Grate. Dazu ein bräunlich-oliver Schimmer in allen Spalten und hellere Bänder quer über einzelne Strähnen
     (z. B. auf der Tolle von oben).
   - Ursache: vier verschiedene Dinge. (a) Kaputte Flecken der Normal-Map – die Haar-Geometrie selbst ist glatt.
     (b) In die Farbtextur eingebackenes warmes „Streulicht“ in den Spalten. (c) Eine fleckige Metallic-Textur
     (0,11 bis 0,31 quer durchs Haar), die Strähnen streifenweise heller glänzen ließ. (d) Eingebackene helle und
     dunkle Felder in der Haarfarbe, am deutlichsten ein blasses Feld mit harter Kante oben auf der Tolle.
   - Gemacht: (a) Normal-Map repariert, siehe Punkt 2. (b) Rund 206 000 Texel in den Spalten auf den Farbton der
     umliegenden Strähne zurückgeführt (Helligkeit höchstens die der Strähne); pinke Strähne und Haaransatz zur Haut
     sind ausgenommen. (c) Rauheit und Metallic im Haar auf je einen Wert gesetzt (dunkles Haar 0,59 / 0,23, pinke
     Strähne 0,60 / 0,34 – die Mediane von vorher). 118 einzelne helle Pünktchen übermalt. (d) Mittlere
     Helligkeitsschwankungen im dunklen Haar (Felder 17 % dunkler bis 33 % heller als ihr Umfeld) auf knapp ein
     Drittel reduziert; das blasse Feld auf der Tolle ist schwächer, aber von oben noch zu ahnen.

2. **Hoodie: dunkle Nahtreste.**
   `compare/02_nahtreste_kordeln.png`, `02b_nahtreste_achsel.png`, `02c_nahtreste_kapuze_schulter.png`
   - Unsauber: schwarze, ausgefranste Striche neben den Kordel-Ansätzen, unter beiden Achseln und entlang der
     Kapuzen-Schulter-Kante (rechts hinten am stärksten).
   - Gemacht: Normal-Map repariert. Texel mit unsinniger Richtung (mehr als ca. 17° Abweichung) samt ihrem Umfeld sind
     neutral gesetzt: 108 573 benutzte Texel (5,2 %). Was danach übrig blieb, war Rauschen ohne erkennbares Detail
     (Median unter 1°): In 11 Testansichten unterscheidet sich ein Render mit dieser Rest-Map von einem ganz ohne in
     höchstens 0,11 % der Pixel (Schwelle 12/255), sichtbar nur als unruhige Streifen auf der Hose. Deshalb hat
     `Material_0` in v4 **keine Normal-Map mehr** (wie `M_Sid_HeadSide` seit v2). Die reparierte Map liegt als
     `tex/T_Sid_Normal.png` im Ordner, falls sie jemand zurückhaben will.

3. **V-Ausschnitt: gezackte Farbgrenze Haut/Stoff.** `compare/03_kragen.png`
   - Gemacht: Die Grenze wird auf der Oberfläche neu gezogen: Haut/Stoff-Zugehörigkeit je Texel, über das Netz
     geglättet (ca. 1,5 mm), daraus eine glatte Linie. In einem Streifen von 2–4,5 mm beiderseits sind die Texel mit
     der sauberen Farbe ihrer Seite neu gefüllt (8 550 Texel), versprengte Texel der falschen Farbe ebenso.

4. **Kordeln: dunkle Flecken und ausgefranste Enden.** `compare/04_kordeln.png`
   - Unsauber: dunkle Schmierer am oberen Ende und entlang der Flanken, die Metallenden mit zackigem Rand.
   - Gemacht: Texel, die deutlich dunkler sind als ihr Umfeld (unter 90 % bis 72 %), auf die Umgebungsfarbe gehoben
     (5 446 Texel, nur auf den Kordeln); Grenze Stoff/Kordelende wie bei Punkt 3 geglättet.

5. **Anstecker: aus dem Klecks wird das Pixel-Herz.** `compare/05_anstecker.png`, `05b_anstecker_seite.png`
   - Unsauber: ein 4–5,5 mm dicker, schief umrandeter roter Klecks mit ausgefranstem schwarzem Rand, einem Graben
     ringsum und einem hellen Schein darüber (der Schein war ein v3-Rest: die Farbe des Klecks war in die Füllfläche
     unter der Muschel hineingezogen worden).
   - Gemacht: (a) Der Klecks ist aus `CH_Sid` herausgeglättet: 711 Punkte liegen jetzt auf einer Thin-Plate-Fläche
     durch den sauberen Stoff ringsum (364 Stützpunkte, Abweichung 0,07 mm); von der Fläche weggedrehte Dreiecke
     dort vorher 115, jetzt 0. Stofffarbe, Rauheit und AO darüber neu gefüllt (8 712 Texel in beiden Texturen).
     Der Hoodie ist unter dem Anstecker also vollständig. (b) Neues Objekt `CH_Sid_Badge`: das Pixel-Herz aus dem Avatar-Bild
     (7 × 6 Pixel zu 4,6 mm, dunkler Rand, zwei Rottöne, weißer Glanzpixel), 37 × 32 mm, folgt der Stoffwölbung,
     Rand 1,6 mm und Herz 2,6 mm über dem Stoff, Kanten gefast, matt-glänzend (Rauheit 0,55). Gleiche Stelle wie der
     alte Klecks, etwas kleiner (der war mit Rand ca. 45 × 36 mm).

6. **Hände: Risse zwischen den Fingern.** `compare/06_hand_oben.png`, `06b_hand_vorn.png`
   - Gemacht: Folge von Punkt 2 (Normal-Map). Geometrie und Farbe der Hände sind unverändert.

7. **Ärmelbündchen: gezackte Grenze Haut/Stoff an beiden Handgelenken.** `compare/07_buendchen.png`
   - Gemacht: wie Punkt 3, je Seite ca. 7 300–8 000 Texel.

8. **Schuhe und Hosensaum: ausgefranste Farbgrenzen.**
   `compare/08_schuhe.png`, `08b_hosensaum.png`, `08c_saum_hose.png`
   - Unsauber: Hose/Schuh mit weißen und schwarzen Zipfeln, die pinken Flächen und Riemen mit rauen Rändern, dazu
     die Grenze Hoodie-Saum/Hose.
   - Gemacht: wie Punkt 3, hier mit drei Farbklassen (Hose, Weiß, Pink), 38 942 Texel an den Schuhen und 21 669 am
     Hoodie-Saum.

9. **Hoodie: Farbbänder und Facetten.** `compare/09_hoodie_ruecken.png`, `09b_hoodie_aermel.png`
   - Unsauber: senkrechte Streifen auf Rücken und Ärmeln, ein helleres Feld mitten auf dem Rücken.
   - Ursache: zwei Dinge. (a) Eingebackene Helligkeitsstufen in der Farbtextur (einzelne Felder 34 % dunkler bis
     30 % heller als ihr Umfeld). (b) Die Generator-Geometrie hat lange flache Grate zwischen ebenen Feldern.
   - Gemacht: (a) Mittlere Farbschwankungen (zwischen ca. 7 mm und 4 cm) im Stoff auf ein Fünftel reduziert; feine
     Struktur und der große Verlauf bleiben. (b) Kantenerhaltende Glättung von Hoodie und Hose: kleine Knicke (wenige
     Grad) werden ausgeglichen, echte Kanten (Tasche, Saum, Bündchen, Kapuzenfalten) bleiben. 27 450 Punkte bewegt,
     im Median 0,15 mm, höchstens 1,4 mm. Kordeln, Anstecker-Stelle und alles in Hautnähe sind ausgenommen.

10. **Hose: unruhige Glanzstreifen.** `compare/10_hose.png`
    - Gemacht: Folge aus Punkt 2 (keine Normal-Map mehr) und 9 (Glättung). Die Falten der Hose sind Geometrie und
      bleiben, sie wirken jetzt etwas weicher.

11. **Kopfhörerbügel liegt auf.** `compare/11_buegel.png`, `11b_buegel_hinten.png`
    - Unsauber: Der Bügel schwebte hinten ca. 10 mm über dem Kapuzenrand, seitlich 1,3 mm über dem Stoff.
    - Gemacht: Der Bügel ist nicht mehr eben. Ab 40° des Bogens senkt er sich weich um bis zu 10 mm, so dass seine
      Unterkante ringsum auf Höhe des Kapuzenrands läuft (hinten z = 0,606 statt 0,616 m). Er liegt jetzt hinten
      seitlich auf dem Kapuzenrand: links bis 0,4 mm im Stoff (17 von 13 530 Messpunkten), rechts 0,2 mm darüber.
      Draufsicht, Arme und beide Muscheln sind unverändert (Muscheln: 0,0 mm Abweichung).

12. **Haarecke unter dem Ohr.** `compare/12_haarecke_ohr.png`
    - Unsauber: Unter beiden Ohrläppchen schaute von vorn ein rotbrauner, ausgefranster Haarzipfel hervor.
    - Gemacht: je Seite ca. 850–900 braune Texel auf die Haarfarbe daneben gesetzt, Haar/Haut-Grenze dort geglättet.

13. **Kleine Dellen und Spitzen.** `compare/13_sohlen.png` (die Delle im Haar: `01_haar_hinten.png`, dunkler Punkt
    links auf der großen Strähne)
    - Unsauber: einzelne Punkte, die 0,5–2,4 mm aus einer sonst glatten Fläche heraus- oder hineinragen.
    - Gemacht: 41 Stellen (49 Punkte) auf die Fläche ihrer Nachbarn zurückgesetzt: 16 an den Sohlen, 12 im Haar,
      9 am Hoodie, 3 an den Händen, 1 am Schuh. Strähnenspitzen sind keine Fehler und bleiben.

14. **AO-Kanal der Textur (wirkt nur im Web-Viewer).** `compare/14_ao_kanal.png`, `14b_ao_kanal_haar.png`
    - Unsauber: Wo die Normal-Map kaputt war, hat auch der AO-Kanal von `T_Sid_ORM` dunkle Kleckse (Median 0,47
      statt 0,68 im Umfeld). Blender-Renders benutzen den Kanal nicht, three.js schon.
    - Gemacht: AO dort auf den Wert des Umfelds angehoben (84 934 Texel). Die Vergleichsbilder zeigen die ORM-Textur
      direkt, kein normales Render (Rot = AO, Grün = Rauheit, Blau = Metallic; grünliche Stellen haben wenig AO).
      Im Haarbild sieht man auch die vereinheitlichte Metallic-Textur aus Punkt 1.

## Gesehen, aber nicht behoben

- **Abstand der rechten Muschel zum Kiefer** (2,8 mm bei `expr_smile` + `expr_mouth_open`, neutral 5,3 mm): gemessen,
  unverändert. Es ist ein Abstand, kein sichtbarer Fehler. Mehr Luft hieße entweder die Muscheln ungleich zu setzen
  oder die Kieferfläche bzw. deren Ausdrucks-Deltas zu ändern – beides wollte ich in einer Aufräumrunde nicht.
- **Der Bügel überspannt hinten weiter die Kapuzenmulde.** Der Kapuzenrand liegt hinten 27 mm weiter außen als der
  Bügel. Aufliegen kann er dort nur mit einem längeren Bügel oder einer höheren Kapuze; das wäre ein neuer Entwurf.
  Von hinten bleibt bei Blick leicht von oben ein schmaler Spalt.
- **Oranger Hals gegen helles Gesicht.** Die harte Farbstufe an der Kieferlinie ist eingebackener Schatten des
  Generators. Sie gehört zum bisherigen Look und grenzt direkt ans Gesicht; nicht angefasst.
- **Lila Schimmer auf den weißen Schuhen** zur Sohle hin: ebenfalls eingebacken, liest sich aber als Verlauf, nicht
  als Fehler.
- **Oberkante des Schuhschafts** ist in der Geometrie leicht wellig; nur die Farbgrenze ist gesäubert.
- **Gürtelschlaufen-Knubbel am Hosenbund**, fast ganz unter dem Hoodie-Saum.
- **Seitennähte unten am Hoodie-Rücken:** zwei senkrechte Kanten sind nach der Glättung weicher, aber noch da. Sie
  könnten gewollte Nähte sein.
- **Stirn-Haaransatz und Nacken** sind weiter nur in der Textur gesäubert (Stand v2/v3).
- **Naht mitten in der Tolle** (dunkle Linie zwischen den beiden vorderen Strähnen): das ist eine echte Kehle in der
  Geometrie.
- **Kragen ganz oben neben den Muscheln:** dort sind ein paar kleine Zacken in der Farbgrenze geblieben (Übergang
  zu den v3-Füllflächen).
- **Kleine umgeklappte Dreiecke im Generator-Netz** (unter 100, jeweils winzig) außerhalb der bearbeiteten Stellen:
  nicht systematisch gesucht, in keinem Bild zu sehen.

## Objekte in der Datei

`CH_Sid` (172 508 Punkte, 344 460 Dreiecke – Anzahl und Reihenfolge wie v3, Materialien `Material_0`,
`M_Sid_HeadSide`), `CH_Sid_Brows`, `CH_Sid_Eye_L/R`, `CH_Sid_Lashes`, `CH_Sid_Mouth` (alle unverändert),
`CH_Sid_Headphones_Band` (Form geändert, 13 596 Dreiecke), `CH_Sid_Headphones_Cup_L/R` (unverändert),
neu `CH_Sid_Badge` (788 Punkte, 1 568 Dreiecke, ein Material `M_Sid_Badge`, Farben als Farbattribut `Col` wie bei den
Augen, keine UVs). Alle Teile sind an `CH_Sid` geparentet, Transform = Identität.

Texturen: `T_Sid_BaseColor`, `T_Sid_ORM` (2048²), `T_Sid_HeadSide_BaseColor`, `T_Sid_HeadSide_ORM` (1024²).
`T_Sid_Normal` ist nicht mehr in der Datei. Geändert sind gegenüber v3 in `T_Sid_BaseColor` 57 % der benutzten Texel
(36 % um mehr als 2 von 255 Stufen – das meiste davon Haar und Hoodie-Stoff), in `T_Sid_ORM` 28 %, in den beiden
HeadSide-Texturen 7,8 % und 0,5 %. UVs und Netzaufbau sind unverändert.

## Wie ich geprüft habe, dass Gesicht und Ausdrücke erhalten sind

- **Shape Keys und Treiber** (`scripts/dump_keys.py` auf v3-Checkpoint und v4, Vergleich `scripts/cmp_keys.py`): alle
  Objekte gleiche Key-Namen, gleiche Treiber, gleiche Materialien. Für alle 32 Keys (8 `expr_*` auf `CH_Sid`, dazu
  Brauen, Wimpern, Mund, Augen) ist die größte Abweichung der Verschiebung gegenüber v3 **0,000000 mm**.
  Summen je Key identisch (z. B. `expr_smile` 109,5265).
- **Kein bewegter Punkt wird von einem Ausdruck bewegt.** In `CH_Sid` sind 28 200 Punkte verschoben (Hoodie, Hose,
  Anstecker-Stelle, Dellen). Davon liegt keiner zwischen z = 0,62 und 0,80 m, und keiner hat in irgendeinem Key ein
  Delta. Alle Verschiebungen sind in Basis und jedem Key gleich eingetragen.
- **Texturen im Gesicht:** In einem Kasten um das Gesicht (69 637 Texel) sind 5 Farb-Texel (am Kinnansatz zum Kragen)
  und 4 ORM-Texel geändert.
- **Im Bild:** `sheet_v4` gegen `checkpoints/sid_v3/sheet_v3`, alle 21 Kopfansichten (neutral von fünf Seiten, jeder der 8
  Ausdrücke von vorn und im Dreiviertelprofil), nur die Gesichtsfläche (Haut samt Augen, Brauen, Mund, 8 px
  innerhalb des Umrisses, `scripts/facediff.py`): in jeder Ansicht 0,000 % der Pixel über der Schwelle 12/255,
  größte Einzelabweichung 12 Stufen (`head_low`, am Kinnrand), mittlere Abweichung 0,12–0,21 Stufen (Rauschen).
  Außerhalb des Gesichts unterscheiden sich die Bilder natürlich: Haar, Kragen, Kopfhörerbügel.
- **Abstand Kopfhörer–Haut** (`sid_v3/scripts/check_v3.py`, alle Ausdrücke und drei Summen): dieselben Werte wie v3,
  neutral 6,4 / 5,3 mm, kleinster 4,0 / 2,8 mm. Der Anstecker ist 15,7 mm von der linken Muschel entfernt.
- **Netz** (`sid_v2/scripts/qa_v2.py`): `CH_Sid` ein Stück, 0 nicht-mannigfaltige Kanten/Punkte, 0 Null-Flächen,
  offene Ränder weiter nur die 3 Lid-/Lippenschleifen (574 Kanten). Anstecker und Kopfhörer geschlossen.
  Alle Bilder eingepackt, keine verwaisten Daten.

## Bekannte Schwächen

- **Farbgrenzen sind sauber, aber weich.** Kragen, Bündchen, Schuhe und Saum sind in der alten Textur neu gezogen
  (ca. 0,7 mm je Texel). Sie sind glatt, aber nicht so scharf wie die Haarkanten aus v2, die auf Netzkanten liegen.
- **Der Bügel ist nicht mehr eben** und berührt den Stoff (links 0,4 mm darin, rechts 0,2 mm darüber). Das ist
  enger als die 0,5-mm-Regel. Die beiden Flächen sehen sich dort aber an (Bügelunterseite nach unten, Stoff nach
  oben) und sind nie zugleich im Bild; im quantisierten Web-Modell kann höchstens die Berührlinie um Bruchteile
  eines Millimeters wandern. Im Viewer nicht nachgesehen.
- **Anstecker:** schlicht (Platte plus Herz, flach schattiert), 1 568 Dreiecke, ein zusätzlicher Draw Call. Er ist
  etwas kleiner als der alte Klecks. Wer ihn nicht will, kann das Objekt löschen; darunter ist glatter Stoff.
- **Keine Normal-Map mehr.** Der Körper bezieht alle Form aus der Geometrie. Feine Stoff- oder Hautstruktur müsste
  neu gemacht werden.
- **Hoodie- und Haarfarbe sind gleichmäßiger als in v3.** Das eingebackene Licht ist im Stoff zu etwa 80 %, im
  dunklen Haar zu etwa 70 % herausgenommen. Die Figur hängt damit stärker vom Licht der Szene ab – gewollt, aber
  eine Änderung am Look.
- **Die Glättung von Hoodie und Hose** hat rund 500 Punkte an winzigen Splitter-Dreiecken ausgelassen (dort wäre das
  Netz umgeklappt). An der Kapuze sind die Flächen etwas ebener geworden.
- **Zwei, drei kleine Dellen an den Sohlen** sind geblieben (sie hängen an einer Kante und gelten dem Filter nicht
  als einzelner Punkt).
- **Im Haar** sind in extremer Nahaufnahme einzelne helle Pünktchen übrig; die hellen Linien in manchen Kehlen sind
  schwächer, aber nicht überall weg.
- **Web-Viewer nicht getestet.** GLB-Export mit Meshopt läuft durch (`tmp/glb/sid_v4_test.glb`, 7,93 MB statt 8,12 MB
  in v3, 4 statt 5 Texturen, 10 Mesh-Knoten, `CH_Sid` 2 Primitive mit 8 Morph-Targets, Anstecker mit `COLOR_0`).
  In three.js habe ich nichts geladen; die AO-Korrektur (Punkt 14) ist deshalb nur an der Textur geprüft.
- Alles aus v1–v3 Genannte gilt weiter: kein Retopo, offene Lid-/Lippenränder innen, interpolierte Ausdrucks-Deltas
  in den Kieferecken, Kopfhörer ohne UVs, Füllflächen aus v3 grob texturiert.

## Aufwand

Rund 65 Render-Läufe (Diagnose in Farbe, Clay, Albedo und ohne Normal-Map; Vergleichspaare nach jedem Schritt; drei
Prüfblatt-Durchläufe) und rund 25 Bau-Läufe. Vorschauen auf GPU 0; die Prüfblatt-Skripte rendern auf der CPU.
Kein Internet, keine Generatoren, kein Blender-MCP.

## Dateien in diesem Ordner

- `sid_face_v4.blend` – Abgabe. `sheet_v4/`, `neck_v4/`, `body_v4/` – Prüfblätter (64 Samples). `compare/` – Paare.
- `body_v3/` – Körperblatt von v3 zum Vergleich (der Lauf, der beim Start schon lief; gleiche Kameras wie `body_v4/`).
- `stage_a.blend` … `stage_g.blend` – Zwischenstände (können weg): a Normal-Map, b Farbgrenzen und Haar-Spalten,
  c Anstecker und Kordeln, d Hoodie-Farbe, e Bügel, f Dellen und Haar-Glanz, g Haarecke. Stoff-Glättung, AO-Kanal,
  die Haar-Felder und das Entfernen der Normal-Map stecken nur in der Abgabe.
- `scripts/build_v4.sh` – setzt die Datei aus `sid_face_v3_input.blend`, `tex/*.png` und `geo/*.npz` zusammen
  (`apply_tex.py`, `geo_apply.py`, `hp_model4.py`/`hp_params4.py` = v3-Kopfhörer plus Absenkung).
- Texturen und Punktverschiebungen sind auf dem Arbeitsrechner gerechnet (numpy + OpenCV, Blenders Python hat kein
  OpenCV): `texmap.py` (Texel → Oberfläche), `surf.py`, `bclean.py` (Farbgrenzen), `fix_normal.py`, `stage_b.py`
  (alle Texturschritte), `badge_geo.py`, `pits.py`, `geo_smooth.py`. Die Skripte liegen zur Dokumentation in
  `scripts/`, mit lokalen Pfaden; Eingabe ist der Export aus `scripts/dump4.py`.
- Prüfung: `dump_keys.py`, `cmp_keys.py`, `facediff.py`, `check_badge.py`, `meas_band.py`; Bilder: `shot.py`.
- `tex/` – die vier geänderten Texturen als PNG (eingepackt) und die reparierte, nicht mehr benutzte Normal-Map.
