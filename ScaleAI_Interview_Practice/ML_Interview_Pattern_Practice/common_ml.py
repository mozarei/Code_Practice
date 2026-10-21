"""Correct shared training harness and explicit learning-contract checks. Do not edit."""
import argparse,csv,importlib.util,json,math,tempfile
from pathlib import Path
import torch
from torch.utils.data import Dataset,DataLoader
from transformers import AutoTokenizer,AutoModelForSequenceClassification
ROOT=Path(__file__).resolve().parent
PROBES=['bert.encoder.layer.0.attention.self.query.weight','classifier.weight']
def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
def modules(directory):
    return {name:load(directory/(name+'.py'),directory.name+'_'+name) for name in ['model','batching','objective','gradients','optim','snapshots']}
class TextRows(Dataset):
    def __init__(self,path):
        with Path(path).open(encoding='utf-8',newline='') as f:
            reader=csv.DictReader(f)
            if reader.fieldnames!=['text','label']:raise ValueError('Expected exact text,label CSV')
            self.rows=[]
            for row in reader:
                if not row['text'].strip() or row['label'] not in {'0','1'}:raise ValueError('Invalid CSV record')
                self.rows.append({'text':row['text'],'label':int(row['label'])})
        if not self.rows:raise ValueError('Empty dataset')
    def __len__(self):return len(self.rows)
    def __getitem__(self,index):return self.rows[index]
def gradient_contract(model,optimizer):
    named=dict(model.backbone.named_parameters())
    head=named[PROBES[1]];encoder=named[PROBES[0]]
    # breakpoint()
    if head.grad is None:raise RuntimeError('Classifier gradient missing after backward')
    if encoder.grad is None or not encoder.requires_grad:raise RuntimeError('Encoder gradient missing after backward')
    for parameter in model.parameters():
        if not parameter.requires_grad or parameter.grad is None or not torch.isfinite(parameter.grad).all():
            raise RuntimeError('Full fine-tuning gradient contract failed')
    live={id(p) for p in model.parameters()}
    managed=[p for group in optimizer.param_groups for p in group['params']]
    owned={id(p) for p in managed}
    if not owned<=live:raise RuntimeError('Optimizer includes parameters from a different model')
    # breakpoint()
    if owned!=live:raise RuntimeError('Optimizer omits live trainable parameters')
    if len(managed)!=len(live):raise RuntimeError('Optimizer has duplicate parameters')
    if any(group['lr']!=1e-4 for group in optimizer.param_groups):raise RuntimeError('Optimizer learning rate must be 0.0001')
def train(directory,csv_path,out,debug=False,quiet=False):
    torch.set_num_threads(2);torch.manual_seed(17)
    checkpoint=ROOT/'models/bert-tiny'
    m=modules(Path(directory))
    tokenizer=AutoTokenizer.from_pretrained(checkpoint,local_files_only=True)
    dataset=TextRows(csv_path)
    collate=m['batching'].make_collator(tokenizer)
    loader=DataLoader(dataset,batch_size=4,shuffle=False,drop_last=False,collate_fn=collate)
    model=m['model'].Classifier(checkpoint).to('cpu')
    model.train()
    optimizer=m['optim'].build_optimizer(model,lr=1e-4)
    before=m['snapshots'].take_snapshot(model)
    losses=[];sizes=[]
    for epoch in range(2):
        # ValueError: text input must be of type `str` (single example), `list[str]` (batch or single pretokenized example) or `list[list[str]]` (batch of pretokenized examples).
        # breakpoint()
        for batch_index,batch in enumerate(loader):
            optimizer.zero_grad(set_to_none=True)
            labels=batch['labels'];inputs={k:v for k,v in batch.items() if k!='labels'}
            if debug and not losses:breakpoint()
            logits=model(**inputs)
            loss=m['objective'].classification_loss(logits,labels)
            records=dataset.rows[batch_index*4:batch_index*4+len(labels)]
            expected=tokenizer([r['text'] for r in records],padding=True,truncation=True,max_length=64,return_tensors='pt')
            if inputs['attention_mask'].shape!=expected['attention_mask'].shape or not torch.equal(inputs['attention_mask'],expected['attention_mask']):
                raise RuntimeError('Attention mask does not mark padding correctly')
            # breakpoint()
            if labels.dtype!=torch.long or labels.shape!=(len(labels),) or logits.shape!=(len(labels),2):
                raise RuntimeError('Classification shape/dtype contract failed')
            if loss.ndim!=0 or not torch.isfinite(loss):raise RuntimeError('Expected finite scalar loss')
            m['gradients'].backward_loss(loss,optimizer)
            gradient_contract(model,optimizer)
            optimizer.step()
            losses.append(loss.detach().item());sizes.append(len(labels))
            if not quiet:print(f'epoch={epoch+1} step={len(losses)} batch={len(labels)} loss={losses[-1]:.6f}',flush=True)
    parameters=dict(model.backbone.named_parameters())
    changes={name:(parameters[name].detach()-before[name]).abs().max().item() for name in PROBES}
    if any(not math.isfinite(v) or v<=0 for v in changes.values()):
        raise RuntimeError('Weights appear unchanged according to snapshot')
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    model.backbone.save_pretrained(out/'checkpoint',safe_serialization=True);tokenizer.save_pretrained(out/'checkpoint')
    metrics={'rows':len(dataset),'epochs':2,'steps':len(losses),'visits':sum(sizes),'batch_sizes':sizes,'losses':losses,'changes':changes}
    (out/'metrics.json').write_text(json.dumps(metrics,indent=2)+'\n')
    print('TRAINING_COMPLETE',flush=True)
    return metrics
def verify(directory,csv_path=None):
    directory=Path(directory);csv_path=Path(csv_path) if csv_path else ROOT/'fixtures/train.csv'
    with tempfile.TemporaryDirectory(prefix='patterns-check-') as temporary:
        out=Path(temporary)/'run';metrics=train(directory,csv_path,out,quiet=True)
        n=len(TextRows(csv_path));expected=([4]*(n//4)+([n%4] if n%4 else []))*2
        assert metrics['batch_sizes']==expected and metrics['visits']==2*n and metrics['steps']==len(expected)
        assert all(math.isfinite(value) for value in metrics['losses'])
        original=AutoModelForSequenceClassification.from_pretrained(ROOT/'models/bert-tiny',local_files_only=True)
        saved=AutoModelForSequenceClassification.from_pretrained(out/'checkpoint',local_files_only=True).eval()
        for name in PROBES:assert not torch.equal(original.state_dict()[name],saved.state_dict()[name]),'Persisted weights unchanged'
        m=modules(directory);model=m['model'].Classifier(out/'checkpoint').eval()
        snap=m['snapshots'].take_snapshot(model);named=dict(model.backbone.named_parameters())
        for name in PROBES:
            assert not snap[name].requires_grad and snap[name].data_ptr()!=named[name].data_ptr(),'Snapshot must own independent storage'
        tokenizer=AutoTokenizer.from_pretrained(out/'checkpoint',local_files_only=True)
        for b in (1,4):
            examples=[{'text':'Hi.' if i==0 else 'A longer example with many words. '*(i+1),'label':i%2} for i in range(b)]
            batch=m['batching'].make_collator(tokenizer)(examples);labels=batch.pop('labels')
            assert batch['input_ids'].dtype==torch.long and labels.dtype==torch.long and labels.shape==(b,)
            expected_inputs=tokenizer([example['text'] for example in examples],padding=True,truncation=True,max_length=64,return_tensors='pt')
            assert torch.equal(batch['attention_mask'],expected_inputs['attention_mask'])
            with torch.no_grad():
                actual=model(**batch);expected_logits=saved(**batch).logits
            assert actual.shape==(b,2) and torch.isfinite(actual).all()
            assert torch.allclose(actual,expected_logits,rtol=1e-5,atol=1e-6),'Changed pretrained classifier architecture'
            logits=torch.randn(b,2,requires_grad=True)
            loss=m['objective'].classification_loss(logits,labels)
            loss.backward();assert logits.grad is not None and torch.isfinite(logits.grad).all()
        print('PASS fresh current-code run, persisted weights, B=1/4, mixed lengths, snapshot storage and reload')
        return metrics
def cli(directory):
    parser=argparse.ArgumentParser();parser.add_argument('--csv',type=Path,default=ROOT/'fixtures/train.csv')
    parser.add_argument('--output-dir',type=Path,default=ROOT/'output'/Path(directory).name)
    parser.add_argument('--pdb',action='store_true');a=parser.parse_args()
    train(directory,a.csv,a.output_dir,a.pdb)
