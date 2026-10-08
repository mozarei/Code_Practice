"""Run current training code in a fresh temporary output folder and independently verify it."""
import argparse
import csv
import importlib.util
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import torch
from transformers import AutoModelForSequenceClassification,AutoTokenizer

ROOT=Path(__file__).resolve().parents[1]


def load_module(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--csv",type=Path,default=ROOT/"fixtures/reference_train.csv")
    parser.add_argument("--train-script",type=Path,default=ROOT/"src/train.py")
    parser.add_argument("--checkpoint",type=Path,default=ROOT/"models/bert-tiny")
    args=parser.parse_args()
    csv_path=args.csv.resolve();script=args.train_script.resolve();checkpoint=args.checkpoint.resolve()
    with csv_path.open(encoding="utf-8",newline="") as f:
        reader=csv.DictReader(f);assert reader.fieldnames==["text","label"]
        rows=list(reader)
    n=len(rows);assert n>0
    torch.set_num_threads(2)
    with tempfile.TemporaryDirectory(prefix="day5-check-") as directory:
        out=Path(directory)/"run"
        env=dict(os.environ,HF_HUB_OFFLINE="1",TRANSFORMERS_OFFLINE="1")
        r=subprocess.run([sys.executable,str(script),"--csv",str(csv_path),"--checkpoint",str(checkpoint),
                          "--output-dir",str(out)],capture_output=True,text=True,timeout=120,env=env,cwd=ROOT)
        if r.returncode:
            print(r.stdout);print(r.stderr,file=sys.stderr)
            raise SystemExit("FAIL fresh training run")
        assert "TRAINING_COMPLETE" in r.stdout
        metrics=json.loads((out/"metrics.json").read_text())
        expected_sizes=([4]*(n//4)+([n%4] if n%4 else []))*2
        assert metrics["rows"]==n and metrics["epochs"]==2
        assert metrics["steps"]==2*math.ceil(n/4) and metrics["examples_seen"]==2*n
        assert metrics["batch_sizes"]==expected_sizes and metrics["device"]=="cpu"
        assert len(metrics["losses"])==metrics["steps"]
        assert all(math.isfinite(v) and v>=0 for v in metrics["losses"])
        before=AutoModelForSequenceClassification.from_pretrained(checkpoint,local_files_only=True)
        after=AutoModelForSequenceClassification.from_pretrained(out/"checkpoint",local_files_only=True).to("cpu").eval()
        for name in ['bert.encoder.layer.0.attention.self.query.weight','classifier.weight']:
            assert not torch.equal(before.state_dict()[name],after.state_dict()[name]),name+" unchanged"
        tokenizer=AutoTokenizer.from_pretrained(out/"checkpoint",local_files_only=True)
        with torch.no_grad():
            for count in (1,2):
                inputs=tokenizer([row["text"] for row in rows[:count]],padding=True,truncation=True,max_length=64,return_tensors="pt")
                logits=after(**inputs).logits
                assert logits.shape==(min(count,n),2) and torch.isfinite(logits).all()
        batching=load_module(script.parent/"batching.py","candidate_batching")
        objective=load_module(script.parent/"objective.py","candidate_objective")
        for count in (1,4):
            examples=[{"text":"short text "*(i+1),"label":i%2} for i in range(count)]
            batch=batching.make_collator(tokenizer)(examples)
            assert batch["input_ids"].dtype==torch.long
            assert batch["labels"].dtype==torch.long and batch["labels"].shape==(count,)
            logits=torch.randn(count,2,requires_grad=True)
            loss=objective.classification_loss(logits,batch["labels"])
            assert loss.ndim==0 and torch.isfinite(loss)
            loss.backward();assert logits.grad is not None and torch.isfinite(logits.grad).all()
        print(f"PASS fresh run: {n} rows, {metrics['steps']} updates, all batches, changed encoder/head, checkpoint reload")
        print("PASS batch/loss contracts at batch sizes 1 and 4")


if __name__=="__main__":main()
