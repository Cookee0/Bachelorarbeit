# Anpassungen des Gold-SQL an SQLite

## Vorgehen

1. Alle 44 Gold-SQL-Statements (A0–A43) wurden auf `data/official.sqlite` und `data/extended.sqlite` ausgeführt.
2. Alle Statements wurden zusätzlich nach Dialekt-Konstrukten durchsucht, die ohne Fehlermeldung laufen, aber andere Werte liefern können: Divisionen, Datumsfunktionen, `TOP`, Verkettung, Anführungszeichen, Kommentare.
3. Die Speicherform der betroffenen Spalten wurde geprüft.
4. Geändert wurde nur der betroffene Ausdruck. Danach wurden alle 44 Statements erneut auf beiden Datenbanken ausgeführt.

## Typische Anpassungen

| Fall                | Anpassung                          |
| ------------------- | ---------------------------------- |
| Datumsdifferenz     | `julianday(b) - julianday(a)`      |
| Jahr/Monat          | `strftime('%Y', x)`, `strftime('%m', x)` |
| Ganzzahldivision    | `* 1.0`                            |
| `TOP n`             | `LIMIT n`                          |
| Verkettung          | `\|\|`                             |

## Änderungen

| ID  | Fall             | Original                                                         | Angepasst                                                             | Grund / Beleg |
| --- | ---------------- | ---------------------------------------------------------------- | --------------------------------------------------------------------- | ------------- |
| A4  | Datumsdifferenz  | `avg(DATEDIFF("day", claim_open_date, claim_close_date))`        | `avg(julianday(claim_close_date) - julianday(claim_open_date))`       | Fehler `no such function: DATEDIFF`. `DATEDIFF(day, a, b)` berechnet `b - a`, deshalb kommt `claim_close_date` zuerst. Alle Datumswerte liegen als `YYYY-MM-DD` vor: `SELECT count(*) FROM claim WHERE claim_open_date NOT GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]' OR (claim_close_date IS NOT NULL AND claim_close_date NOT GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]')` → 0 (official und extended) |
| A13 | Ganzzahldivision | `SUM(policy_amount)/COUNT(DISTINCT policy_number)`               | `SUM(policy_amount) * 1.0 / COUNT(DISTINCT policy_number)`            | Läuft ohne Fehler, rechnet aber ganzzahlig. `policy_amount` ist `decimal(15,2)`, wird aber als `integer` gespeichert: `SELECT typeof(policy_amount), count(*) FROM policy_amount GROUP BY 1` → nur `integer` |
| A15 | Ganzzahldivision | `sum(... + ca_er.claim_amount)/policy_amount as LossRatio`       | `sum(... + ca_er.claim_amount) * 1.0 / policy_amount as LossRatio`    | Wie A13. Zusätzlich `claim_amount`: `SELECT typeof(claim_amount), count(*) FROM claim_amount GROUP BY 1` → nur `integer` |
| A20 | Ganzzahldivision | `sum(... + ca_er.claim_amount)/policy_amount as LossRatio`       | `sum(... + ca_er.claim_amount) * 1.0 / policy_amount as LossRatio`    | Wie A15 |
