"""Optional post-attempt evidence tool. It inspects current code; it does not repair it."""
import argparse,importlib.util,sys
from pathlib import Path
import torch
from transformers import AutoTokenizer
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from model import ReviewClassifier
from optim import build_optimizer
from batching import make_collator
from objective import classification_loss
def main():
    p=argparse.ArgumentParser();p.add_argument('--pdb',action='store_true');a=p.parse_args()
    torch.set_num_threads(2);torch.manual_seed(17)
    checkpoint=ROOT/'models/bert-tiny'
    tokenizer=AutoTokenizer.from_pretrained(checkpoint,local_files_only=True)
    model=ReviewClassifier(checkpoint);optimizer=build_optimizer(model,lr=1e-4)
    batch=make_collator(tokenizer)([{'text':'Hi.','label':0},{'text':'A longer example with several words.','label':1}])
    labels=batch.pop('labels');before={name:p.detach().clone() for name,p in model.named_parameters()}
    optimizer.zero_grad(set_to_none=True);logits=model(**batch);loss=classification_loss(logits,labels)
    if a.pdb:breakpoint()
    loss.backward()
    ids={id(p) for group in optimizer.param_groups for p in group['params']}
    def report(stage):
        print(stage)
        for name,param in model.named_parameters():
            if name in ['backbone.bert.encoder.layer.0.attention.self.query.weight','backbone.classifier.weight']:
                grad=None if param.grad is None else param.grad.norm().item()
                change=(param.detach()-before[name]).abs().max().item()
                print(name,'requires_grad=',param.requires_grad,'grad norm=',grad,'managed=',id(param) in ids,'delta=',change)
    report('AFTER BACKWARD');optimizer.step();report('AFTER STEP')
if __name__=='__main__':main()
