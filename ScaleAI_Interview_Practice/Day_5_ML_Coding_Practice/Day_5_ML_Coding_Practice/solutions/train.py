import argparse
import json
import math
from pathlib import Path
import torch
from torch.utils.data import DataLoader
from transformers import AutoTokenizer
from data import TextRows
from batching import make_collator
from model import ConversationClassifier
from objective import classification_loss

ROOT=Path(__file__).resolve().parents[1]


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--csv",type=Path,required=True)
    parser.add_argument("--checkpoint",type=Path,default=ROOT/"models/bert-tiny")
    parser.add_argument("--output-dir",type=Path,default=ROOT/"output/run")
    args=parser.parse_args()
    torch.manual_seed(17)
    torch.set_num_threads(2)
    tokenizer=AutoTokenizer.from_pretrained(args.checkpoint,local_files_only=True)
    dataset=TextRows(args.csv)
    loader=DataLoader(dataset,batch_size=4,shuffle=False,drop_last=False,collate_fn=make_collator(tokenizer))
    model=ConversationClassifier(args.checkpoint).to("cpu")
    model.train()
    optimizer=torch.optim.AdamW(model.parameters(),lr=1e-4)
    names={"encoder":"bert.encoder.layer.0.attention.self.query.weight","classifier":"classifier.weight"}
    parameters=dict(model.backbone.named_parameters())
    before={group:parameters[name].detach().clone() for group,name in names.items()}
    losses=[];sizes=[];steps=0;examples_seen=0
    print(f"CSV_ROWS={len(dataset)} DEVICE=cpu",flush=True)
    for epoch in range(2):
        for batch in loader:
            optimizer.zero_grad(set_to_none=True)
            inputs={k:v.to("cpu") for k,v in batch.items() if k!="labels"}
            labels=batch["labels"].to("cpu")
            logits=model(**inputs)
            loss=classification_loss(logits,labels)
            value=float(loss.detach())
            if not math.isfinite(value):
                raise RuntimeError("Nonfinite loss")
            loss.backward()
            gradients=[p.grad for p in model.parameters() if p.grad is not None]
            if not gradients or not all(torch.isfinite(g).all().item() for g in gradients):
                raise RuntimeError("Missing or nonfinite gradients")
            optimizer.step()
            losses.append(value);sizes.append(labels.shape[0])
            steps+=1;examples_seen+=labels.shape[0]
            print(f"epoch={epoch+1} step={steps} batch={labels.shape[0]} loss={value:.6f}",flush=True)
    changes={group:float((parameters[name].detach()-before[group]).abs().max()) for group,name in names.items()}
    for group,value in changes.items():
        print(f"PARAMETER_CHANGE {group}={value:.8f}",flush=True)
        if not math.isfinite(value) or value<=0:
            raise RuntimeError(f"{group} parameters did not change during full fine-tuning")
    args.output_dir.mkdir(parents=True,exist_ok=True)
    model.backbone.save_pretrained(args.output_dir/"checkpoint",safe_serialization=True)
    tokenizer.save_pretrained(args.output_dir/"checkpoint")
    metrics={"rows":len(dataset),"epochs":2,"steps":steps,"examples_seen":examples_seen,
             "device":"cpu","losses":losses,"batch_sizes":sizes,"max_parameter_changes":changes}
    (args.output_dir/"metrics.json").write_text(json.dumps(metrics,indent=2)+"\n")
    print("TRAINING_COMPLETE",flush=True)


if __name__=="__main__":
    main()
