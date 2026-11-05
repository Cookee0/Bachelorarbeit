import os
import sys

import ollama

from db import ROOT

MODELS = {
    "1.7": "qwen3:1.7b-8k-nothink-Temp0",
    "4": "qwen3:4b-8k-nothink-Temp0",
    "8": "qwen3:8b-8k-nothink-Temp0",
    "pilot": "qwen3:0.6b",
}  # pilot: review-protocol test only
OPTS = {
    "temperature": 0,
    "seed": 1,
    "num_ctx": 8192,
    "repeat_penalty": 1.1,
}  # deterministic decoding

key, artefact = (
    sys.argv[1],
    sys.argv[2],
)  # z.B. "1.7b" "B" for Column Descriptions with Model 1.7b

inputs = ""
with open(f"{ROOT}/context/inputs.txt", encoding="utf-8") as file:
    inputs = file.read()

prompt = ""
with open(f"{ROOT}/prompts/gen_{artefact}.txt", encoding="utf-8") as file:
    prompt = file.read()
prompt += "\n\n" + inputs

if artefact == "C":
    prompt += "\n\n## Checked descriptions\n"
    with open(f"{ROOT}/context/{key}/B_checked.md", encoding="utf-8") as file:
        prompt += file.read()

r = ollama.chat(
    model=MODELS[key],
    messages=[{"role": "user", "content": prompt}],
    think=False,
    options=OPTS,
)
print(
    "prompt tokens:",
    r["prompt_eval_count"],
    "output tokens:",
    r["eval_count"],
    r["done_reason"],
)
if r["prompt_eval_count"] >= OPTS["num_ctx"] - 256:
    print("WARNING: prompt probably truncated")
ext = "md" if artefact == "B" else "yaml"

if os.path.exists(f"{ROOT}/context/{key}/raw/"):
    with open(f"{ROOT}/context/{key}/raw/{artefact}_raw.{ext}", "w", encoding="utf-8") as file:
        file.write(r["message"]["content"])
else:
    os.mkdir(f"{ROOT}/context/{key}/raw/")
    with open(f"{ROOT}/context/{key}/raw/{artefact}_raw.{ext}", "w", encoding="utf-8") as file:
            file.write(r["message"]["content"])