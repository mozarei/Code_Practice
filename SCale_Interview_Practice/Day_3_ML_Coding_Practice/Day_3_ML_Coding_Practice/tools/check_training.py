"""Verify training evidence and reload the saved checkpoint. Does not repair code."""
import argparse
import csv
import json
import math
from pathlib import Path
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument("--run-dir",type=Path,default=ROOT/"output/run")
parser.add_argument("--csv",type=Path,default=ROOT/"fixtures/reference_train.csv")
args=parser.parse_args()
metrics=json.loads((args.run_dir/"metrics.json").read_text())
with args.csv.open(encoding="utf-8",newline="") as f:
    reader=csv.DictReader(f)
    assert reader.fieldnames==["text","label"]
    rows=list(reader)
n=len(rows)
assert n>0
assert metrics["rows"]==n and metrics["epochs"]==2
assert metrics["steps"]==2*math.ceil(n/4)
assert metrics["examples_seen"]==2*n and metrics["device"]=="cpu"
assert len(metrics["losses"])==metrics["steps"]
assert all(math.isfinite(v) and v>=0 for v in metrics["losses"])
assert all(v>0 and math.isfinite(v) for v in metrics["max_parameter_changes"].values())
torch.set_num_threads(2)
path=args.run_dir/"checkpoint"
tokenizer=AutoTokenizer.from_pretrained(path,local_files_only=True)
model=AutoModelForSequenceClassification.from_pretrained(path,local_files_only=True).to("cpu").eval()
inputs=tokenizer([rows[0]["text"],rows[-1]["text"]],padding=True,truncation=True,max_length=64,return_tensors="pt")
with torch.no_grad():
    logits=model(**inputs).logits
assert logits.shape==(2,2) and torch.isfinite(logits).all()
print(f"PASS {n} rows, {metrics['steps']} updates, finite loss, changed parameters, offline checkpoint reload")
print("This verifies pipeline execution, not model quality.")
