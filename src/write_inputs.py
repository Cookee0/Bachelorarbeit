import pathlib

BENCH = pathlib.Path("G:/Programmieren/__Projekte/Bachelorarbeit/benchmark/Bachelorarbeit")
DDL = (BENCH / "DDL/ACME_small.ddl").read_text(encoding="utf-8")
CONTEXT = pathlib.Path("G:/Programmieren/__Projekte/Bachelorarbeit/context")

with open(CONTEXT / "inputs.txt", "w", encoding="utf-8") as f:
    f.write(DDL)