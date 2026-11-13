# Turnaround-Blatt per Bildgenerator

Dieser Prompt ist für den Hauptagenten oder einen Menschen am Bildgenerator, kein Subagenten-Auftrag.

**Einstellungen:** 16:9, 2K. Als Referenz das Konzept- bzw. Avatarbild der Figur. Wenn die Proportionen driften, kommt ein bereits abgenommenes Turnaround-Blatt als zweite Referenz dazu.

**Prompt (englisch funktioniert am zuverlässigsten):**

> Character turnaround sheet of exactly the character in the reference image: same face, {MERKMALE: Frisur, Haarfarbe, Accessoires, Kleidung, Farben}, the same {STIL, z. B. stylised 3D toy-figure render style}, about {N} heads tall. Full body, three views side by side on one wide image: left a front view, middle a side view in profile facing image-left, right a back view. All three views at exactly the same scale and height: top of the head on one horizontal line and the soles of the feet on one horizontal line. Standing in a relaxed A-pose, arms angled about 30 degrees away from the body, hands open and empty, feet slightly apart. {HOSE UND SCHUHE}. Straight-on camera at mid-body height with minimal perspective. Plain light grey seamless background, even soft lighting, no cast shadows on the background, no floor line. No text, no labels, no {REQUISITEN} in the hands.

**Mit zweiter Referenz** am Anfang ergänzen:
> The character from image 1; proportions, style, pose, lighting and layout from image 2.

**Prüfen, bevor es weitergeht:**
- **Drei Figuren, die Seite blickt nach Bild-links.** Danach `python3 {TOOLS}/split_turnaround.py blatt.png out figur` und die Ausgabe auf gleiche Scheitel- und Sohlenzeilen prüfen.
- **Rückansicht vorhanden, Hände leer, keine Texte.**
- **Proportionen wie im Konzept**, Kopflängen zählen.
