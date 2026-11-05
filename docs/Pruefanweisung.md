# Prüfanweisung für den modellerzeugten Kontext
Version: 1.0 (not to be changed anymore unless necessary (Abschnitt 9 for example))
Stand 05.11.2026
## 1 Ziel

Diese Prüfanweisung wird verwendet, um die erstellten Artefakte B und C systematisch zu testen.
Es werden die Artefakte `b_raw.md` und `c_raw.yaml` überprüft und in `b_checked.md` und `c_checked.yaml` überführt.

Jede Änderung wird in einem eigenen Prüfprotokoll `{artefakt}_review.csv` und einer gemeinsamen `review.csv` festgehalten. `{artefakt}_review.csv` dient der Nachvollziehbarkeit der Änderungen. `review.csv` macht den zeitlichen Prüfaufwand sichtbar.

## 2 Grundregeln

1. **Beweispflicht:**  Es darf keine Änderung (correct, delete...) ohne Beleg aus einer Quelle vorgenommen werden.
2. **Minimalprinzip:** Korrekturen dürfen nur den widerlegten Teil der Aussage durch eine belegbare, korrekte Aussage ersetzt werden. Es darf nichts hinzugefügt werden.
3. **Ergänzungsverbot:** Es darf nichts hinzugefügt werden, auch wenn eine Einheit belegbar fehlt.
4. **Vollständigkeit:** Jede Einheit jedes Artefakts erhält eine eigene Zeile im Protokoll, auch wenn sie nicht berührt wird.

## 3 Zulässige Belegquellen

| Quelle                          | Datei                                 | Zitationsstil                                           | Wofür                                                                              |
| ------------------------------- | ------------------------------------- | ------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Schema                          | `benchmark/Bachelorarbeit/DDL/ACME_small.ddl` | Zeilennummer, z. B. `DDL Line 36`                | Existenz von Tabellen und Spalten, Datentypen, Schlüssel, NOT NULL, Fremdschlüssel |
| Daten der offiziellen Datenbank | `data/official.sqlite`                | Die SQL-Abfrage                                         | Vorkommende Werte, Wertebereiche, Formate                                          |
| Ontologie                       | `context/ontology_reference.txt`      | z.B. `Classes`, `Relationships`, `Attributes`           | Fachliche Bedeutung von Begriffen                                                  |
| Tabellenbeziehungen             | `context/reference_relationships.csv` | Zeilennummer, z. B. `reference_relationships.csv Line 3` | Fremdschlüsselbeziehungen zwischen Tabellen                                        |

**Nicht zulässig sind:**
- eigenes Fachwissen
- Referenzfragen und Gold-SQL
- Artefakte anderer Modelle

## 4 Prüfeinheiten

### 4.1 Definition

Eine Prüfeinheit ist eine Aussage über ein Element.

| Artefakt | Einheitentyp (`unit_type`) | Eine Einheit ist                                                    | Benennung (`unit`)                        |
| -------- | -------------------------- | ------------------------------------------------------------------- | ----------------------------------------- |
| B        | `table`                    | die Beschreibung einer Tabelle                                      | `claim`                                   |
| B        | `column`                   | die Beschreibung einer Spalte                                       | `claim.claim_open_date`                   |
| B        | `code`                     | die Bedeutung eines Codewertes                                      | `Agreement_Party_Role.Party_Role_Code=PH` |
| C        | `entity`                   | eine Entität mit Name, zugeordneter Tabelle, Schlüssel und Beschreibung           | `entity:Claim`                            |
| C        | `relationship`             | eine Beziehung mit beiden Enden, Join-Spalten und ggf. Kardinalität | `rel:claim->policy`                       |
| C        | `metric`                   | eine Kennzahl mit Formel, Filtern und Granularität                  | `metric:total_loss_amount`                |

### 4.2 Zerlegungsregeln

- Enthält eine Spaltenbeschreibung Codebedeutungen, wird jeder Codewert als eigene Einheit (`code`) geführt. Die Spaltenbeschreibung selbst wird als `column` geführt.
- Eine Kennzahl wird als eine Einheit geprüft. Ist ein Bestandteil (Formel, Filter, Granularität) widerlegt, gilt die ganze Einheit als falsch.
- Text, der nicht zur Beschreibung der Tabellen dient (Einleitungen, Überschriften, Hinweise des LLM) ist keine Prüfeinheit. Sie werden sofort gelöscht.

## 5 Ablauf

### 5.1 Reihenfolge und Zeitpunkt

- **Zeitpunkt:** Die Prüfung findet vor der Validierung des Gold-SQL statt.
- **Vorbereitung:** `ontology_reference.txt` und `reference_relationships.csv` werden erstellt, bevor das erste Artefakt erzeugt wird.
- **Reihenfolge:** B für alle drei Modelle erzeugen → alle B prüfen → C für alle drei Modelle erzeugen → alle C prüfen.

### 5.2 Schritte je Artefakt

| Schritt | Tätigkeit                                                                                                                                                                                                                 | Ergebnis                             |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------ |
| 1       | Zeitmessung starten. `*_raw.*` nach `*_checked.*` kopieren. Die Rohdatei wird nie bearbeitet.                                                                                                                             | Kopie der Rohdatei                   |
| 2       | Artefakt vollständig in Einheiten zerlegen. Jede Einheit mit `unit_id`, `artefact`, `unit`, `unit_type`, `action`, `original`, `evidence_source`, `evidence` und `reason` in `{artefakt}_review.csv` eintragen.                  | Liste aller Einheiten                |
| 3       | Jede Einheit nach dem Entscheidungsbaum ([[#6 Entscheidungsbaum]]) prüfen. Aktion, Beleg und Begründung eintragen.                                                                                                        | Ausgefülltes Protokoll               |
| 4       | Korrekturen und Löschungen exakt wie protokolliert in `*_checked.*` umsetzen.                                                                                                                                             | Geprüfte Datei                       |
| 5       | Nur C: YAML-Gültigkeit prüfen (`yaml.safe_load`). Bei Fehlern ausschließlich syntaktisch reparieren und als `syntax` protokollieren (Abschnitt 7).                                                                        | Parsbare Datei                       |
| 6       | Prüfung: Jede `correct`- und `delete`-Zeile hat einen Beleg. Die Zahl der Protokollzeilen (ohne `syntax`-Zeilen) entspricht der Zahl der Einheiten aus Schritt 2. `syntax`-Zeilen sind keine Einheiten und werden zusätzlich geführt. Die Differenz zwischen Roh- und Prüfdatei zeigt nur protokollierte Änderungen. | Kontrolliertes Ergebnis              |
| 7       | Zeitmessung stoppen und in `review.csv` eintragen.                                                                                                                                                                        | Abgeschlossenes , geprüftes Artefakt |

## 6 Entscheidungsbaum

Jede Einheit durchläuft die Fragen der Reihe nach. Die erste zutreffende Antwort bestimmt die Aktion.

| Nr. | Prüffrage                                                                                                         | Wenn ja                                                                              | Wenn nein                           |
| --- | ----------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ | ----------------------------------- |
| 1   | Bezieht sich die Einheit auf eine Tabelle oder Spalte, die es in der DDL nicht gibt?                              | `delete` (Beleg: DDL)                                                                | weiter mit F2                       |
| 2   | Nur B: Beschreibt die Einheit Verknüpfungen, Join-Pfade oder Berechnungsregeln? | Betroffenen Teil streichen: `correct`, oder ganz `delete`, wenn nichts übrig bleibt. | weiter mit F3                       |
| 3   | Steht mindestens eine maßgebliche Quelle (Abschnitt 3) im direkten Widerspruch zur Aussage?                       | weiter mit F4                                                                        | weiter mit F5                       |
| 4   | Lässt sich der widerlegte Teil durch eine Aussage ersetzen, die der Beleg direkt stützt, ohne Neues hinzuzufügen? | `correct`                                                                            | `delete`                            |
| 5   | Wird die Aussage durch mindestens eine Quelle gestützt?                                                           | `keep`                                                                               | `unverifiable` (unverändert lassen) |

## 7 Grenzfälle

| Fall                                                                                       | Regel                                                                                      | Aktion                                             |
| ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ | -------------------------------------------------- |
| Aussage ist teilweise richtig                                                              | Den widerlegten Teil minimal berichtigen oder streichen, den Rest unverändert lassen       | `correct`                                          |
| Element doppelt beschrieben                                                                | Erste Beschreibung prüfen, zweite löschen. Beleg: `evidence_source=rule`, `evidence=unit_id X` (die behaltene Einheit). Gleichheit wird nach der Korrektur beurteilt: Eine Beziehung in umgekehrter Richtung ist dieselbe Beziehung. Ist die erste Fassung widerlegt und erst die spätere belegt oder korrigierbar, wird die erste gelöscht und die spätere behalten (Verweis auf diese `unit_id`). | `delete`                                           |
| Codewert ohne Definition in der Ontologie (z. B. `PH`, `AG`)                               | Bedeutung weder bestätigt noch widerlegt                                                   | `unverifiable`                                     |
| Codewert, der in den Daten nicht vorkommt                                                  | Die offizielle Datenbank ist zu klein, um ihn auszuschließen                               | `unverifiable`, wenn nicht anders widerlegt        |
| Beschreibung nennt eine andere Tabelle oder bezeichnet die Spalte als Fremdschlüssel (B beschreibt nur Spalten, keine Beziehungen) | Nennung bzw. Fremdschlüssel-Aussage streichen (F2). Bleibt eine belegbare Aussage übrig, nur den Teil streichen, sonst ganz löschen. | `correct` bzw. `delete`                            |
| DDL enthält Fremdschlüssel auf nicht existierende Tabelle, die Beschreibung nennt sie nicht | Die Zieltabelle ist keine Belegquelle. Die Einheit wird nur danach beurteilt, ob ihr eigener Inhalt gestützt ist (F5). | `keep` / `unverifiable`                            |
| Beschreibung wiederholt nur den Spaltennamen                                               | Durch die Existenz der Spalte in der DDL gestützt (F5)                                     | `keep`, Quelle `ddl`                               |
| Nur C: Der DDL-Fremdschlüssel einer Beziehung verweist auf eine Tabelle, die es in der DDL nicht gibt (`declared_target_not_in_db`), die Beziehung im Artefakt nennt eine andere Zieltabelle | Eine Korrektur würde auf eine nicht vorhandene Tabelle verweisen und SQL-Abfragen fehlschlagen lassen. Die Einheit wird nicht korrigiert, sondern gelöscht. | `delete` |
| Beziehung ohne Fremdschlüssel in der DDL                                                   | Bestätigt, wenn in `reference_relationships.csv` enthalten. Ansonsten nicht verifizierbar. | `keep` / `unverifiable`                            |
| Kardinalität angegeben (1:1, 1:n)                                                          | Nur über DDL verifizierbar. Ist die Fremdschlüsselspalte in der Kindtabelle zugleich der vollständige Primärschlüssel, ist die Kardinalität `one_to_one`, `many_to_one` ist widerlegt. | `keep`, `delete`, `correct` nach Entscheidungsbaum |
| Nur C: Richtung von `from` und `to`                                                        | `from` ist die Tabelle, die den Fremdschlüssel enthält (Kindtabelle), `to` die referenzierte Tabelle. Vertauschte Richtung ist widerlegt und wird durch Tauschen korrigiert. | `correct` nach Entscheidungsbaum |
| Kennzahl mit plausibler, aber nicht belegter Formel                                        | Weder bestätigt noch widerlegt                                                             | `unverifiable`                                     |
| Kennzahl aggregiert eine nicht numerische Spalte oder nutzt eine nicht existierende Spalte | Widerlegt durch DDL                                                                        | `delete` oder `correct` nach Entscheidungsbaum     |
| YAML parst nicht korrekt                                                                   | Nur syntaktisch reparieren, Inhalt unverändert                                             | `syntax`                                           |
| Fließtext außerhalb der YAML-Struktur                                                      | Entfernen, wenn er das Parsen verhindert, sonst behalten                                   | `syntax` bzw. keine Einheit                        |
| Nur C: Markdown-Code-Fences (` ```yaml ` am Anfang, ` ``` ` am Ende)                       | Verhindern `yaml.safe_load`, daher entfernen. Je Fence eine `syntax`-Zeile (`unit` = `syntax:code_fence`, `unit_type` = `syntax`, `evidence_source` = `rule`); sie zählt nicht als Einheit (Schritt 6) | `syntax`                                           |
| YAML weicht von der Vorlage ab (andere Schlüssel, andere Struktur)                         | Nicht umstrukturieren. Ausschließlich Parsbarkeit herstellen                               | keine Aktion bzw. `syntax`                         |
| Ausgabe ist abgeschnitten                                                                  | Die unvollständige letzte Einheit löschen; Beleg „abgeschnitten“                           | `delete`                                           |

## 8 Protokollformat

## 8.1 Einzelne Artefakte

`context/{modell}/{artefakt}_review.csv`

| Spalte            | Inhalt                                                                                            | Pflicht                 |
| ----------------- | ------------------------------------------------------------------------------------------------- | ----------------------- |
| `unit_id`         | fortlaufend je Artefakt                                                                           | immer                   |
| `artefact`        | `B` oder `C`                                                                                      | immer                   |
| `unit`            | Benennung der Einheit (Tabelle, Spalte, Spalte=Code, Entität, Beziehung, Kennzahl), siehe 4.1      | immer                   |
| `unit_type`       | `table`, `column`, `code`, `entity`, `relationship`, `metric`                                     | immer                   |
| `action`          | `keep`, `correct`, `delete`, `unverifiable`, `syntax`                                             | immer                   |
| `original`        | Wortlaut der Einheit im Rohartefakt                                                               | immer                   |
| `corrected`       | Wortlaut nach der Prüfung (leer bei `delete`)                                                     | bei `correct`, `syntax` |
| `evidence_source` | `ddl`, `data`, `ontology`, `relationship`, `rule`, `none`; mehrere Quellen mit `;` trennen | immer                   |
| `evidence`        | DDL-Zeile (`DDL Line N`), Zeile der Referenzbeziehungen (`reference_relationships.csv Line N`), SQL-Abfrage im Wortlaut (auf `official.sqlite`), Verweis auf `unit_id`. Bei mehreren Quellen in `evidence_source` enthält `evidence` je Quelle einen Beleg, mit `;` getrennt, in derselben Reihenfolge | bei `correct`, `delete`. Bei `keep` empfohlen |
| `reason`          | Begründung für die Änderung                                                                       | bei `correct`, `delete`, `unverifiable`                   |

## 8.2 Gemeinsame `review.csv`

`context/review.csv`

| Spalte             | Inhalt                                                 |
| ------------------ | ------------------------------------------------------ |
| Modell             | Modellname                                             |
| Artefakt           | Artefakt (`B`, `C`)                                    |
| Gesamtdauer in min | Zeit in Minuten, die für die Prüfung aufgewendet wurde |

## NOCH OFFEN: 9 Zweitprüfung (Übereinstimmung)

**Mit zweiter Person:**

1. Einarbeitung mit dieser Anweisung und dem Probeartefakt (`context/pilot`).
2. Stichprobe: je Artefakt 20 % der Einheiten, geschichtet nach `unit_type`, mit festem Startwert gezogen.
3. Die zweite Person erhält Rohartefakt, Belegquellen (inkl. `official.sqlite`) und die Einheitenliste mit `unit_id`, `unit` und `original`, **ohne** die Spalten `action`, `corrected`, `evidence` und `reason`.
4. Sie entscheidet je Einheit nach dem Entscheidungsbaum.
5. **NOCH OFFEN:** Ausgewertet werden prozentuale Übereinstimmung und Cohens Kappa auf der Spalte `action` (Cohen, 1960), gesamt und je Artefakttyp.
6. Abweichende Entscheidungen werden berichtet und qualitativ eingeordnet. Die geprüften Artefakte bleiben unverändert; maßgeblich ist die Erstprüfung. Das verhindert, dass die Kontexte im Nachhinein angepasst werden.

**Ohne zweite Person (Rückfalloption):** Die prüfende Person prüft dieselbe Stichprobe nach frühestens einer Woche erneut, ohne Einsicht in die eigenen Entscheidungen, und berichtet die Intra-Rater-Übereinstimmung. Das ist schwächer als eine Zweitprüfung und wird als Limitation benannt.

## 10 Kennzahlen aus dem Protokoll

Je Modell und Artefakt (berechnet mit `src/effort.py`, rein deskriptiv):

| Kennzahl                    | Berechnung                                                                      |
| --------------------------- | ------------------------------------------------------------------------------- |
| Einheiten                   | Zahl der Protokollzeilen                                                        |
| Aktionsanteile              | Anteil `keep`, `correct`, `delete`, `unverifiable`, `syntax` an allen Einheiten |
| Abdeckung B                 | beschriebene Spalten nach der Prüfung / alle Spalten der DDL                    |
| Abdeckung C                 | Beziehungen nach der Prüfung / Referenzbeziehungen aus der DDL                  |
| Prüfzeit                    | Minuten je Artefakt                                                             |
| NOCH OFFEN: Übereinstimmung | Prozent und Cohens Kappa aus Abschnitt 9                                       |
