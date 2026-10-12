"""Fresh training plus independent batching/model/optimizer/checkpoint contracts."""
import argparse,csv,importlib.util,json,math,os,subprocess,sys,tempfile
from pathlib import Path
import torch
from transformers import AutoModelForSequenceClassification,AutoTokenizer
ROOT=Path(__file__).resolve().parents[1]
def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def main():
    p=argparse.ArgumentParser();p.add_argument('--csv',type=Path,default=ROOT/'fixtures/reference_train.csv')
    p.add_argument('--train-script',type=Path,default=ROOT/'src/train.py');p.add_argument('--checkpoint',type=Path,default=ROOT/'models/bert-tiny');a=p.parse_args()
    script=a.train_script.resolve();checkpoint=a.checkpoint.resolve();csv_path=a.csv.resolve()
    with csv_path.open(encoding='utf-8',newline='') as f:
        reader=csv.DictReader(f);assert reader.fieldnames==['text','label'];rows=list(reader)
    n=len(rows);assert n>0;torch.set_num_threads(2)
    with tempfile.TemporaryDirectory(prefix='day8-check-') as directory:
        out=Path(directory)/'run'
        env=dict(os.environ,HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',TOKENIZERS_PARALLELISM='false')
        r=subprocess.run([sys.executable,str(script),'--csv',str(csv_path),'--checkpoint',str(checkpoint),'--output-dir',str(out)],capture_output=True,text=True,timeout=150,env=env,cwd=ROOT)
        if r.returncode:
            print(r.stdout);print(r.stderr,file=sys.stderr);raise SystemExit('FAIL fresh training run')
        assert 'TRAINING_COMPLETE' in r.stdout
        metrics=json.loads((out/'metrics.json').read_text())
        expected=([4]*(n//4)+([n%4] if n%4 else []))*2
        assert metrics['rows']==n and metrics['epochs']==2 and metrics['device']=='cpu'
        assert metrics['steps']==2*math.ceil(n/4) and metrics['examples_seen']==2*n and metrics['batch_sizes']==expected
        assert len(metrics['losses'])==metrics['steps'] and all(math.isfinite(v) and v>=0 for v in metrics['losses'])
        original=AutoModelForSequenceClassification.from_pretrained(checkpoint,local_files_only=True)
        persisted=AutoModelForSequenceClassification.from_pretrained(out/'checkpoint',local_files_only=True).eval()
        for name in ['bert.encoder.layer.0.attention.self.query.weight','classifier.weight']:
            assert not torch.equal(original.state_dict()[name],persisted.state_dict()[name]),name+' unchanged'
        tokenizer=AutoTokenizer.from_pretrained(out/'checkpoint',local_files_only=True)
        batching=load(script.parent/'batching.py','candidate_batching')
        model_module=load(script.parent/'model.py','candidate_model')
        optim_module=load(script.parent/'optim.py','candidate_optim')
        objective=load(script.parent/'objective.py','candidate_objective')
        model=model_module.ReviewClassifier(checkpoint).eval()
        optimizer=optim_module.build_optimizer(model,lr=1e-4)
        live_ids={id(param) for param in model.parameters() if param.requires_grad}
        managed=[param for group in optimizer.param_groups for param in group['params']]
        assert {id(param) for param in managed}==live_ids, 'Optimizer must manage live model parameters'
        assert len(managed)==len(live_ids),'Duplicate optimizer parameter'
        assert all(group['lr']==1e-4 for group in optimizer.param_groups)
        collate=batching.make_collator(tokenizer)
        for count in (1,4):
            examples=[{'text':'Hi.' if i==0 else 'A much longer piece of text. '*(i+2),'label':i%2} for i in range(count)]
            batch=collate(examples);labels=batch.pop('labels')
            assert labels.shape==(count,) and labels.dtype==torch.long
            assert batch['input_ids'].dtype==torch.long and batch['input_ids'].ndim==2
            assert batch['attention_mask'].shape==batch['input_ids'].shape
            optimizer.zero_grad(set_to_none=True)
            logits=model(**batch)
            assert logits.shape==(count,2) and torch.isfinite(logits).all()
            # The wrapper must preserve the supplied pretrained classifier architecture.
            with torch.no_grad():expected_logits=model.backbone(**batch).logits
            assert torch.allclose(logits.detach(),expected_logits,rtol=1e-5,atol=1e-6), 'Wrapper changes intended pretrained forward'
            loss=objective.classification_loss(logits,labels)
            assert loss.ndim==0 and torch.isfinite(loss) and loss.requires_grad
            loss.backward()
            assert all(param.grad is not None and torch.isfinite(param.grad).all() for param in model.parameters()), 'Missing/invalid full fine-tuning gradients'
            probes=dict(model.backbone.named_parameters())
            names=['bert.encoder.layer.0.attention.self.query.weight','classifier.weight']
            before={name:probes[name].detach().clone() for name in names}
            optimizer.step()
            assert all(not torch.equal(before[name],probes[name].detach()) for name in names), 'No live weight update'
        # Save/reload equivalence: independently reload, then compare wrapper with saved model.
        candidate=model_module.ReviewClassifier(out/'checkpoint').eval()
        inputs=tokenizer(['Short text.','Longer text with extra details.'],padding=True,return_tensors='pt')
        with torch.no_grad():
            actual=candidate(**inputs);expected=persisted(**inputs).logits
            assert actual.shape==(2,2) and torch.isfinite(actual).all()
            assert torch.allclose(actual,expected,rtol=1e-5,atol=1e-6)
        # Padding robustness: the short sentence should not change when batched with a longer one.
        single=tokenizer(['Short text.'],return_tensors='pt')
        with torch.no_grad():
            assert torch.allclose(candidate(**single)[0],candidate(**inputs)[0],rtol=1e-4,atol=1e-5)
        print(f'PASS fresh run: {n} rows, {metrics["steps"]} updates, {2*n} examples, changed encoder/head')
        print('PASS variable-length batches, B=1/4, live optimizer ownership, intended forward and reload equivalence')
if __name__=='__main__':main()
