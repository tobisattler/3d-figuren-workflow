# Aufträge an Fable-Subagenten

## Warum Fable 5.2 auf Effort xhigh

Im November 2026 haben wir das mit demselben Auftrag an derselben Figur verglichen:

| Test | Ergebnis |
|---|---|
| Modelliertes Gesicht auf Sid, Fable 5.2 xhigh gegen Opus 5.5 xhigh, blind bewertet | Fable „deutlich besser“: wirklich neutral, Ausdrücke treffen, keine Dellen. Opus lag im neutralen Gesicht näher am Original, lächelte aber und hatte Dellen. |
| Figur nur aus Code (bpy), Score aus Silhouetten-IoU + DINO | Fable 0,920 nach 11 Läufen. Opus 5.5 kam vorher auf 0,847 nach 10 und 0,869 nach 40 Läufen. Pixal3D erreichte 0,91–0,92. |
| Fable mit xhigh, high und medium | Im Viewer sichtbar: xhigh vor high, high klar vor medium. Der automatische Score sah high vorn, weil eingebackene Schattierung den DINO-Anteil aufbläht. |

Kosten: Fable kostet pro Token doppelt so viel und verbraucht bei uns 25–35 % mehr Tokens. Eine Runde kostete 300k–560k Tokens. Für 3D-Arbeit hat sich das gelohnt. Für Routinearbeit wie Bilder prüfen, Dateien kopieren oder Exporte reicht der Hauptagent.

## Aufbau eines Auftrags

Immer dieselben vier Teile, kurz und **nicht vorschreibend**. Das Ziel und die Maßstäbe stehen fest, den Weg wählt der Agent.

1. **Ausgangslage:**
   - Arbeitsdatei als Kopie, wo der schreibgeschützte Checkpoint liegt,
   - was die Figur ist, mit Maßen und Konventionen,
   - welche Teile es gibt,
   - die Notizen der früheren Runden.
2. **Ziel:**
   - was am Ende anders sein soll,
   - was gleich bleiben muss, zum Beispiel Gesicht und Shape Keys mit Namen und Wirkung,
   - wonach der Mensch urteilt, mit seinen eigenen Worten und dem, was er früher abgelehnt hat,
   - die technischen Grenzen des Ziels, etwa der Mindestabstand bei Meshopt, 4 Einflüsse pro Punkt oder nur gebackene Farben.
3. **Arbeitsweise:**
   - wie Blender aufgerufen wird,
   - welche GPU,
   - wo der Agent schreiben und lesen darf,
   - was verboten ist: Internet, Generatoren, die Live-Blender-Instanz eines Menschen,
   - welche Skills und Prüfblätter er nutzen darf,
   - Zeitrahmen mit „hör auf, wenn Du zufrieden bist“,
   - bei wackliger Hardware: Zwischenstände speichern.
4. **Abgabe:**
   - .blend in sich geschlossen,
   - Prüfblätter mit genau angegebenem Befehl,
   - Vorher/Nachher-Paare `compare/NN_name.png`,
   - `notizen.md` mit „Verbessert“, „Gesehen, aber nicht behoben“, Objektliste, wie geprüft wurde und bekannten Schwächen,
   - eine kurze Antwort mit denselben Punkten.

Die Vorlagen in `briefs/` haben genau diese Form. Die Platzhalter stehen in geschweiften Klammern.

## Was gut funktioniert hat

- **Eine Runde, ein Thema:** Gesicht, Accessoires, Aufräumen und Rig jeweils getrennt. Wo viel auf einmal geändert wurde, wusste man nicht mehr, woher ein Fehler kommt.
- **Checkpoints:** Nach jeder abgenommenen Runde kommen .blend, Prüfblätter und Notizen schreibgeschützt nach `checkpoints/vN`. Der nächste Auftrag beginnt mit einer Kopie davon.
- **Den Menschen zitieren:** Urteile wie „schrecklich“ für aufgemalte Züge über modellierten, „Halloween Horror“ für zu große, tiefe Augen oder „ziemlich gut“ steuern den Agenten besser als lange Vorgaben.
- **Bekannte Schwächen mitgeben**, aber als „Kandidaten, ohne Anspruch auf Vollständigkeit“. Der Agent findet dann noch mehr.
- **Zielbilder als Maßstab, nicht als Vorlage zum Abpausen.** Beim Rig zum Beispiel Posenbilder nur als Look-Hinweis.
- **Feste Prüfblätter** aus `tools/blender/`, mit genauem Befehl in der Abgabe. So lassen sich Runden und sogar verschiedene Agenten blind vergleichen.
- **Der Koordinator prüft selbst nach**, bevor der Mensch etwas sieht: Bilder ansehen, Zahlen nachrechnen, die tatsächliche Laufzeit nachsehen. Agenten schätzen ihre eigene Dauer gern falsch.

## Was man nicht tun sollte

- **Keine Schritt-für-Schritt-Anleitung.** Die Agenten haben eigene, oft bessere Wege gefunden: Gewichte per Formel statt Heat, Hände neu bauen statt reparieren, die Normal-Map als Ursache der Risse.
- **Kein Internet und keine Generatoren in Modellier-Runden.** Sonst weiß man nicht, was der Agent selbst gebaut hat.
- **Keine Live-Blender-Instanz eines Menschen** für Subagenten. Sie arbeiten headless auf eigenen Kopien.

## Starten aus Claude Code

Im Hauptagenten zum Beispiel so:

> Fülle briefs/04_aufraeumen.md für die Figur in work/figur_v4 aus (Checkpoint checkpoints/v3) und starte damit einen Subagenten: Modell fable, Effort xhigh, im Hintergrund. Wenn er fertig ist, sieh Dir die Vorher/Nachher-Bilder an, prüf die Notizen und zeig mir eine Übersicht.

Zusätzliche Informationen bekommt ein laufender Subagent per SendMessage. Das haben wir genutzt, um nachgereichte Kritik des Menschen weiterzugeben.
