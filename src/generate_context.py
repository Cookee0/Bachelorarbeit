import sys, ollama

ROOT = "G:/Programmieren/__Projekte/Bachelorarbeit"
MODELS = {"1.7b": "qwen3:1.7b-8k-nothink-Temp0", "4b": "qwen3:4b-8k-nothink-Temp0", "8b": "qwen3:8b-8k-nothink-Temp0",
          "pilot": "qwen3:0.6b"}                      # pilot: review-protocol test only
OPTS = {
    "temperature": 0, 
    "seed": 1, 
    "num_ctx": 8192, 
    "repeat_penalty": 1.1
} # deterministic decoding

key, artefact = sys.argv[1], sys.argv[2]              # z.B. "1.7b" "B" for Column Descriptions with Model 1.7b
inputs = open(f"{ROOT}/context/inputs.txt", encoding="utf-8").read()
prompt = open(f"{ROOT}/prompts/gen_{artefact}.txt", encoding="utf-8").read() + "\n\n" + inputs
if artefact == "C":
    prompt += "\n\n## Checked descriptions\n" + open(f"{ROOT}/context/{key}/B_checked.md", encoding="utf-8").read()

r = ollama.chat(model=MODELS[key], messages=[{"role": "user", "content": prompt}], think=False, options=OPTS)
print("prompt tokens:", r["prompt_eval_count"], "output tokens:", r["eval_count"], r["done_reason"])
if r["prompt_eval_count"] >= OPTS["num_ctx"] - 256:
    print("WARNING: prompt probably truncated")
ext = "md" if artefact == "B" else "yaml"
open(f"{ROOT}/context/{key}/{artefact}_raw.{ext}", "w", encoding="utf-8").write(r["message"]["content"])