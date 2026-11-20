# Bachelorarbeit – Text-to-SQL mit lokalen Qwen3-Modellen

Dieses Repository enthält den Code, die Prompts, den erzeugten Kontext und die Ergebnisse der Benchmark-Läufe.
Drei Qwen3-Modelle (1.7B, 4B, 8B) bekommen über Ollama 60 Fragen zur ACME-Versicherungsdatenbank
und sollen dafür SQL erzeugen. Dabei erhalten sie unterschiedlich viel Kontext:

| Bedingung | Kontext                                                                 |
| --------- | ----------------------------------------------------------------------- |
| A         | nur das Schema (DDL)                                                    |
| B         | Schema + Spaltenbeschreibungen (`B_checked.md`)                         |
| C         | Schema + Spaltenbeschreibungen + semantisches Modell (`C_checked.yaml`) |
| B_ctx8b / C_ctx8b | wie B / C, aber mit dem Kontext des 8B-Modells                  |

Das erzeugte SQL wird ausführungsbasiert bewertet: Es läuft auf zwei Datenbanken (`official` und
`extended`), und das Ergebnis wird mit dem des Gold-SQL verglichen.

## Projektstruktur

```
benchmark/Bachelorarbeit/   Offizielle Benchmark-Daten (DDL, CSVs, Ontologie)
context/                    Erzeugter und geprüfter Kontext je Modell + Prüfprotokolle
  {modell}/raw/             Rohausgabe des Modells (wird nie bearbeitet)
  {modell}/checked/         Manuell geprüfte Fassung (wird im Harness verwendet)
  {modell}/*_review.csv     Prüfprotokoll je Artefakt
data/                       SQLite-Datenbanken (nicht im Repository, siehe unten)
docs/Pruefanweisung.md      Regeln für die manuelle Prüfung des Kontexts
logs/                       GPU- und Ollama-Logs der Läufe
modelfiles/                 Ollama-Modelfiles (Temp0 = Kontexterzeugung, Temp0.7 = Benchmark)
prompts/                    System-Prompt, Aufgaben-Prompt, Prompts zur Kontexterzeugung
questions/questions.csv     Fragen, Gold-SQL, Beantwortbarkeit
results/                    Ergebnisse (runs.csv, dry_run.csv)
src/                        Alle Skripte
versions.txt                Commit der Benchmark-Daten, SQLite-Version, SHA256 der Datenbanken
```

## 1. Einrichtung

### Python

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

**Wichtig:** Der Projektpfad ist in `src/db.py` fest eingetragen:

```python
ROOT = pathlib.Path("G:/Programmieren/__Projekte/Bachelorarbeit")
```

Diesen Pfad vor dem ersten Start auf den eigenen Speicherort des Repositorys ändern.

### Ollama und Modelle

[Ollama](https://ollama.com) installieren, die Basismodelle laden und daraus mit den Modelfiles
die verwendeten Modelle erzeugen. Die Namen müssen genau so lauten, weil die Skripte sie erwarten:

```bash
ollama pull qwen3:1.7b
ollama pull qwen3:4b
ollama pull qwen3:8b

# Benchmark (Temperatur 0.7, verwendet von harness.py)
ollama create qwen3:1.7b-8k-nothink-recommended -f modelfiles/Temp0.7/1.7B-Modelfile
ollama create qwen3:4b-8k-nothink-recommended   -f modelfiles/Temp0.7/4B-Modelfile
ollama create qwen3:8b-8k-nothink-recommended   -f modelfiles/Temp0.7/8B-Modelfile

# Kontexterzeugung (Temperatur 0, verwendet von generate_context.py)
ollama create qwen3:1.7b-8k-nothink-Temp0 -f modelfiles/Temp0/1.7B-Modelfile
ollama create qwen3:4b-8k-nothink-Temp0   -f modelfiles/Temp0/4B-Modelfile
ollama create qwen3:8b-8k-nothink-Temp0   -f modelfiles/Temp0/8B-Modelfile
```

Ollama muss laufen (`ollama serve`), bevor eines der Skripte gestartet wird.

## 2. Datenbanken erzeugen

Der Ordner `data/` ist nicht im Repository (`.gitignore`). Beide Datenbanken lassen sich aber
vollständig aus den Dateien im Repository erzeugen. Alle Befehle werden im Projektordner ausgeführt.

### 2.1 Offizielle Datenbank (`data/official.sqlite`)

```bash
python src/load_official.py
```

Das Skript liest `benchmark/Bachelorarbeit/DDL/ACME_small.ddl`, legt die 13 Tabellen in SQLite an
und lädt die zugehörigen CSV-Dateien aus `benchmark/Bachelorarbeit/data/`. Die Datenbank wird bei
jedem Aufruf neu erzeugt. Zwei Anpassungen sind nötig, damit SQLite die Daten annimmt:

- Die DDL ist im T-SQL-Stil ohne `;` zwischen den Anweisungen. Das Skript ergänzt sie.
- Die offiziellen Beispieldaten verletzen einige `NOT NULL`-Bedingungen. Diese werden beim Laden
  gelockert. Primärschlüssel und Datentypen bleiben erhalten.

Herkunft der Daten: `datadotworld/cwd-benchmark-data`, Commit
`0b75eb62eaf7ea315a863cd7611ebc908149f7e0` (siehe `versions.txt`).

### 2.2 Erweiterte Datenbank (`data/extended.sqlite`)

```bash
python src/generate_extended.py
```

Voraussetzung: `official.sqlite` existiert bereits. Das Skript kopiert die offizielle Datenbank und
fügt erzeugte Zeilen hinzu (8 Katastrophen, 300 Policen, dazu Schadenfälle und Beträge). Die Regeln:

- Nur allgemeine Mengen und Verteilungen, keine Zeilen, die auf einzelne Fragen zugeschnitten sind.
- Keine erfundenen Werte: Spalten, die in der offiziellen Datenbank durchgehend `NULL` sind, bleiben
  `NULL`. Code- und Namensspalten verwenden nur Werte, die in der offiziellen Datenbank vorkommen.
- Erzeugte IDs beginnen bei 100000 und kollidieren so nicht mit den offiziellen IDs.
- Feste Zufallszahl (`SEED = 20261114`) und festes Stichtagsdatum. Dadurch entsteht bei jedem Lauf
  byte-identisch dieselbe Datenbank.

Am Ende prüft das Skript automatisch alle Fremdschlüssel, die Datentypen und die Regel
„keine erfundenen Werte“. Schlägt eine Prüfung fehl, bricht es mit einer Fehlermeldung ab.

### 2.3 Prüfen, ob die Datenbanken stimmen

Die SHA256-Werte beider Datenbanken stehen in `versions.txt`. Vergleich unter Windows:

```powershell
Get-FileHash data\official.sqlite
Get-FileHash data\extended.sqlite
```

### 2.4 Die erweiterte Datenbank anpassen

Alle Stellschrauben stehen am Anfang von `src/generate_extended.py`:

| Konstante           | Bedeutung                                                     |
| ------------------- | ------------------------------------------------------------- |
| `SEED`              | Zufallszahl; eine andere ergibt eine andere, aber wieder feste Datenbank |
| `N_PH`, `N_AG`      | Anzahl Versicherungsnehmer und Vermittler                     |
| `N_POLICIES`        | Anzahl Policen                                                |
| `N_CATASTROPHES`    | Anzahl Katastrophen                                           |
| `CLAIMS_PER_POLICY` | Schadenfälle je Police und ihre Gewichte                      |

Für eine neue Tabelle oder Spalte wird eine eigene `gen_…`-Funktion geschrieben und unten im Skript
in der Reihenfolge „Eltern vor Kindern“ aufgerufen, damit alle Fremdschlüssel aufgelöst werden.
Anschließend das Skript neu ausführen und den neuen SHA256-Wert in `versions.txt` eintragen.

**Achtung:** Eine geänderte Datenbank verändert auch die Gold-Ergebnisse. Bereits vorhandene
Ergebnisse in `results/runs.csv` sind danach nicht mehr vergleichbar.

### 2.5 Datenbank von Hand abfragen

```bash
python src/query.py "SELECT COUNT(*) FROM Claim"                  # gegen extended
python src/query.py --db official "SELECT COUNT(*) FROM Claim"    # gegen official
python src/query.py                                               # interaktiver Modus
```

Die Verbindung ist schreibgeschützt.

## 3. Kontext erzeugen (Artefakte B und C)

Der Kontext wird von jedem Modell selbst erzeugt und danach von Hand geprüft. Die geprüften Dateien
liegen bereits im Repository, dieser Schritt ist für den Benchmark also nicht nötig. Er ist hier
beschrieben, damit er sich nachvollziehen lässt.

### 3.1 Eingaben vorbereiten

```bash
python src/write_inputs.py      # -> context/inputs.txt (Schema + Beispieldaten aus official.sqlite)
python src/write_ontology.py    # -> context/ontology_reference.txt (Belegquelle für die Prüfung)
```

`context/reference_relationships.csv` ist ebenfalls eine Belegquelle für die Prüfung und liegt
bereits im Repository.

### 3.2 Artefakt erzeugen

```bash
python src/generate_context.py <modell> <B|C>
# Beispiel:
python src/generate_context.py 1.7b B
```

`<modell>` ist `1.7b`, `4b`, `8b` (oder `pilot` für den Test des Prüfablaufs). Die Ausgabe landet in
`context/<modell>/raw/B_raw.md` bzw. `C_raw.yaml`. Gearbeitet wird mit Temperatur 0 und festem Seed.

**Wichtig – jeden Aufruf zweimal starten:** Um ein reproduzierbares Ergebnis zu bekommen, muss
`generate_context.py` für jedes Modell und Artefakt **zweimal hintereinander** ausgeführt werden. Erst
die Ausgabe des zweiten Aufrufs ist reproduzierbar und wird verwendet (der zweite Aufruf überschreibt
die Rohdatei des ersten).

Die Reihenfolge ist festgelegt:

1. B für alle drei Modelle erzeugen
2. Alle B prüfen (→ `checked/B_checked.md`)
3. C für alle drei Modelle erzeugen. C baut auf dem **geprüften** B des jeweiligen Modells auf.
4. Alle C prüfen (→ `checked/C_checked.yaml`)

### 3.3 Manuelle Prüfung

Die Prüfung folgt `docs/Pruefanweisung.md`. Kurz gefasst: Die Rohdatei wird nach `checked/` kopiert
und in Einheiten (Tabellen, Spalten, Codes, Entitäten, Beziehungen, Kennzahlen) zerlegt. Jede
Einheit wird mit einer Aktion (`keep`, `correct`, `delete`, `unverifiable`, `syntax`) und einem Beleg
in `{artefakt}_review.csv` protokolliert. Änderungen sind nur mit Beleg erlaubt, Ergänzungen gar nicht.
Die aufgewendete Zeit steht in `context/review.csv`.

## 4. Benchmark (Harness) ausführen

### 4.1 Testlauf

Vor dem eigentlichen Lauf sollte ein kurzer Testlauf gemacht werden:

```bash
python src/harness.py --dry-run
```

Er nimmt nur die ersten 5 Fragen und Lauf 1, schreibt nach `results/dry_run.csv` und zeigt am Ende
an, ob Antworten abgeschnitten wurden, ob der Prompt nahe am Kontextlimit liegt und ob SQL-Fehler
aufgetreten sind.

### 4.2 Hauptlauf

```bash
python src/harness.py
```

Jedes Modell beantwortet jede Frage in jeder Bedingung fünfmal (Seeds 1–5). Die Ergebnisse werden
Zeile für Zeile nach `results/runs.csv` geschrieben. Eine vorhandene `runs.csv` wird vorher nicht
gelöscht, sondern in `runs_<zeitstempel>.csv` umbenannt.

Wurde ein Lauf unterbrochen, setzt dieser Befehl ihn fort, ohne bereits erledigte Zeilen zu wiederholen:

```bash
python src/harness.py --resume
```

### 4.3 Bewertung

Die Bewertung passiert direkt im Harness (`src/scoring.py`):

- Enthält die Antwort `CANNOT_ANSWER`, gilt sie als `refusal`.
- Sonst wird das SQL aus der Antwort gezogen und auf beiden Datenbanken ausgeführt (schreibgeschützt,
  30 Sekunden Zeitlimit). Schlägt das fehl, gilt sie als `error`.
- Bei nicht beantwortbaren Fragen ist jede ausführbare Antwort `wrong`.
- Bei beantwortbaren Fragen ist eine Antwort nur dann `correct`, wenn das Ergebnis auf **beiden**
  Datenbanken mit dem des Gold-SQL übereinstimmt. Verglichen wird als Multimenge von Zeilen.
  Zeilenreihenfolge, Spaltenreihenfolge und Spaltennamen spielen keine Rolle, Zahlen werden auf
  4 Nachkommastellen gerundet.

Die wichtigsten Spalten in `runs.csv`: `model`, `condition`, `qid`, `run`, `category`,
`correct_official`, `correct_extended`, `sql` (extrahiertes SQL) und `raw` (vollständige Modellantwort).
Außerdem werden Tokens, Laufzeit und der Digest des Modells festgehalten.
