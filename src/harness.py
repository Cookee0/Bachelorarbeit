# Benchmark run: asks each model every question per condition and scores the SQL against gold.
import argparse
import csv
import datetime
import os
import re
import sqlite3
from pathlib import Path

import ollama

from db import BENCH, DBS, ROOT
from scoring import run_sql, same_result

MODELS = {
    "1.7b": "qwen3:1.7b-8k-nothink-recommended",
    "4b": "qwen3:4b-8k-nothink-recommended",
    "8b": "qwen3:8b-8k-nothink-recommended",
}

# (label, context level, context source); source None = the model's own context
CONDITIONS = [
    ("A", "A", None),
    ("B", "B", None),
    ("C", "C", None),
    ("B_ctx8b", "B", "8b"),
    ("C_ctx8b", "C", "8b"),
]

RUNS = [1, 2, 3, 4, 5]
NUM_CTX = 8192
NUM_PREDICT = 2048
OPTIONS = {
    "temperature": 0.7,
    "top_p": 0.8,
    "top_k": 20,
    "min_p": 0,
    "repeat_penalty": 1.0,
    "num_ctx": NUM_CTX,
    "num_predict": NUM_PREDICT
}
REFUSAL = "CANNOT_ANSWER"
OUT = f"{ROOT}/results/runs.csv"

# Dry run: small subset, separate output file, overwritten on every start.
DRY_OUT = f"{ROOT}/results/dry_run.csv"
DRY_RUNS = [1]
DRY_QUESTIONS = 5

FIELDS = [
    "timestamp",
    "model",
    "tag",
    "digest",
    "condition",
    "context_source",
    "qid",
    "answerable",
    "run",
    "seed",
    "prompt_tokens",
    "output_tokens",
    "latency_s",
    "truncation_risk",
    "done_reason",
    "category",
    "correct_official",
    "correct_extended",
    "sql",
    "raw",
]


def read(path):
    return Path(path).read_text(encoding="utf-8")


SYSTEM = read(f"{ROOT}/prompts/system_prompt.txt")
TASK = read(f"{ROOT}/prompts/task.txt")
DDL = read(BENCH / "DDL/ACME_small.ddl")


def build_context(source, level):
    # A = schema, B = + column descriptions, C = + semantic model.
    # XML-style tags instead of markdown headings, because B_checked.md has its own "## <table>" headings.
    parts = [f"<schema>\n{DDL.strip()}\n</schema>"]
    if level in ("B", "C"):
        text = read(f"{ROOT}/context/{source}/checked/B_checked.md")
        parts.append(f"<column_descriptions>\n{text.strip()}\n</column_descriptions>")
    if level == "C":
        text = read(f"{ROOT}/context/{source}/checked/C_checked.yaml")
        parts.append(f"<semantic_model>\n{text.strip()}\n</semantic_model>")
    return "\n\n".join(parts)


def extract_sql(text):
    # First code block if there is one (also matches "``` sql"), otherwise the whole answer.
    match = re.search(r"```\s*(?:sql)?\s*(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if match:
        text = match.group(1)
    return text.strip().rstrip(";")


def ask(tag, prompt, seed):
    return ollama.chat(
        model=tag,
        think=False,
        keep_alive="30m",
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": prompt},
        ],
        options={**OPTIONS, "seed": seed},
    )


def warm_up(tag):
    # Throwaway request so the model is loaded (with the real options) before the first recorded run.
    ask(tag, "hi", seed=0)


def score(question, answer, gold):
    # Returns (category, sql, correct_official, correct_extended).
    if REFUSAL in answer:
        return "refusal", "", "", ""

    sql = extract_sql(answer)
    try:
        results = {name: run_sql(db, sql) for name, db in DBS.items()}
    except (sqlite3.Error, sqlite3.Warning):
        return "error", sql, "", ""

    if question["answerable"] != "1":
        # any runnable answer to an unanswerable question is wrong
        return "wrong", sql, "", ""

    qid = question["ID"]
    official = same_result(results["official"], gold[(qid, "official")])
    extended = same_result(results["extended"], gold[(qid, "extended")])
    category = "correct" if official and extended else "wrong"
    return category, sql, official, extended


def load_done(path):
    # Runs already in the output file, so an interrupted benchmark can be resumed.
    if not os.path.exists(path):
        return set()
    with open(path, encoding="utf-8") as f:
        return {
            (r["model"], r["condition"], r["qid"], r["run"]) for r in csv.DictReader(f)
        }


def main(dry_run=False, resume=False):
    out = DRY_OUT if dry_run else OUT
    runs = DRY_RUNS if dry_run else RUNS

    with open(f"{ROOT}/questions/questions.csv", encoding="utf-8") as f:
        questions = list(csv.DictReader(f))
    if dry_run:
        questions = questions[:DRY_QUESTIONS]

    digests = {m.model: m.digest for m in ollama.list().models}

    # Gold results per (question, database), only for answerable questions.
    gold = {}
    for q in questions:
        if q["answerable"] == "1":
            for name, db in DBS.items():
                gold[(q["ID"], name)] = run_sql(db, q["gold_sql"])

    if dry_run and os.path.exists(out):
        os.remove(out)
    elif not resume and os.path.exists(out):
        # Fresh start: keep the old results under a timestamped name instead of deleting them.
        stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup = out.replace(".csv", f"_{stamp}.csv")
        os.rename(out, backup)
        print(f"Previous results moved to {backup}")
    done = load_done(out)

    with open(out, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, FIELDS)
        if not done:
            writer.writeheader()

        for model, tag in MODELS.items():
            warm_up(tag)
            for run in runs:
                for condition, level, source in CONDITIONS:
                    # the 8B's own B and C runs already are its shared-context runs
                    if source == model:
                        continue
                    context_source = source or model
                    context = build_context(context_source, level)

                    for q in questions:
                        if (model, condition, q["ID"], str(run)) in done:
                            continue

                        prompt = TASK.replace("<<CONTEXT>>", context)
                        prompt = prompt.replace("<<QUESTION>>", q["question"])
                        response = ask(tag, prompt, seed=run)
                        answer = response["message"]["content"]
                        category, sql, official, extended = score(q, answer, gold)

                        writer.writerow(
                            {
                                "timestamp": datetime.datetime.now().isoformat(),
                                "model": model,
                                "tag": tag,
                                "digest": digests.get(tag, ""),
                                "condition": condition,
                                "context_source": context_source,
                                "qid": q["ID"],
                                "answerable": q["answerable"],
                                "run": run,
                                "seed": run,
                                "prompt_tokens": response["prompt_eval_count"],
                                "output_tokens": response["eval_count"],
                                "latency_s": round(response["total_duration"] / 1e9, 3),
                                "truncation_risk": response["prompt_eval_count"]
                                >= NUM_CTX - 256,
                                "done_reason": response["done_reason"],
                                "category": category,
                                "correct_official": official,
                                "correct_extended": extended,
                                "sql": sql,
                                "raw": answer,
                            }
                        )
                        f.flush()


def summarize(path):
    # Dry-run check: anything here means the setup is not ready for the main runs.
    with open(path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    cut = [r for r in rows if r["done_reason"] != "stop"]
    risky = [r for r in rows if r["truncation_risk"] == "True"]
    errors = [r for r in rows if r["category"] == "error"]
    print(f"{len(rows)} rows written to {path}")
    print(f"  cut off (done_reason != stop): {len(cut)}")
    print(f"  prompt near context limit:     {len(risky)}")
    print(f"  SQL errors:                    {len(errors)}")
    for r in cut:
        print(f"    cut: {r['model']} {r['condition']} {r['qid']} ({r['done_reason']})")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help=f"{DRY_QUESTIONS} questions, run 1 only, writes to dry_run.csv",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="continue an interrupted run instead of starting a fresh runs.csv",
    )
    args = parser.parse_args()
    main(dry_run=args.dry_run, resume=args.resume)
    if args.dry_run:
        summarize(DRY_OUT)
