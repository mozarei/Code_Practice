"""Behavior checks for the small coding exercises. No mock bug answers are exposed."""
import importlib.util
from pathlib import Path
import math
import torch
from torch import nn
import torch.nn.functional as F
from labs.common import fresh_model, data, snapshot, changes
ROOT = Path(__file__).resolve().parents[1]

def check(number, directory=None):
    directory = Path(directory) if directory else ROOT / 'exercises'
    path = directory / f'task_{number:02}.py'
    spec = importlib.util.spec_from_file_location(f'task_{number}', path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    if number == 1:
        model = fresh_model()
        for scope, group in [('all',model),('backbone',model.backbone),('head',model.classifier)]:
            result = m.select_parameters(model,scope)
            assert isinstance(result,list), 'Return a list'
            assert [id(p) for p in result] == [id(p) for p in group.parameters()], 'Wrong parameter objects or order'
    elif number == 2:
        model = fresh_model(); model.unused = nn.Parameter(torch.tensor([2.]))
        for after in (False,True):
            if after:
                x,y=data(); F.cross_entropy(model(x),y).backward()
            result=m.gradient_report(model)
            assert len(result)==len(list(model.parameters()))
            for row,(name,p) in zip(result,model.named_parameters()):
                assert row['name']==name and row['requires_grad']==p.requires_grad
                assert row['has_grad']==(p.grad is not None)
                if p.grad is None: assert row['grad_norm'] is None
                else: assert isinstance(row['grad_norm'],float) and math.isclose(row['grad_norm'],p.grad.norm().item(),rel_tol=1e-5)
    elif number == 3:
        for b in (1,4):
            model=fresh_model(); x,y=data(b)
            logits,loss=m.compute_loss(model,x,y)
            assert logits.shape==(b,2) and torch.allclose(logits,model(x))
            assert loss.ndim==0 and loss.requires_grad
            assert torch.allclose(loss,F.cross_entropy(logits,y))
            loss.backward(); assert all(p.grad is not None for p in model.parameters())
    elif number == 4:
        for w,x,y,g in [(2.,3.,1.,30.),(1.,2.,3.,-4.)]:
            parameter=nn.Parameter(torch.tensor(w)); parameter.grad=torch.tensor(100.)
            a,b,grad=m.observe_backward(parameter,x,y)
            assert a.item()==w and b.item()==w and parameter.item()==w, 'Backward must not change weight'
            assert math.isclose(grad.item(),g), 'Wrong derivative or stale gradient'
            assert a.data_ptr()!=parameter.data_ptr() and b.data_ptr()!=parameter.data_ptr(), 'Use independent snapshots'
    elif number == 5:
        for scope in ('all','head'):
            model=fresh_model(); before=snapshot(model); x,y=data()
            opt=m.make_optimizer(model,scope)
            assert isinstance(opt,torch.optim.AdamW)
            expected=model.parameters() if scope=='all' else model.classifier.parameters()
            assert {id(p) for group in opt.param_groups for p in group['params']}=={id(p) for p in expected}
            assert all(group['lr']==.01 and group['weight_decay']==0 for group in opt.param_groups)
            F.cross_entropy(model(x),y).backward(); opt.step(); delta=changes(model,before)
            assert delta['classifier.weight']>0
            assert (delta['backbone.0.weight']>0)==(scope=='all')
            assert model.backbone[0].weight.grad is not None, 'Exclusion is not freezing'
    elif number == 6:
        for w,repeats in [(2.,2),(3.,4)]:
            parameter=nn.Parameter(torch.tensor(w)); parameter.grad=torch.tensor(50.)
            result=m.accumulated_gradient(parameter,repeats)
            assert math.isclose(result.item(),2*w*repeats), 'Clear initially; then accumulate'
            assert parameter.item()==w
            assert result.data_ptr()!=parameter.grad.data_ptr(), 'Return a clone'
    elif number == 7:
        model=fresh_model(); x,y=data(); F.cross_entropy(model(x),y).backward()
        m.freeze_backbone(model)
        assert all(not p.requires_grad and p.grad is None for p in model.backbone.parameters())
        assert all(p.requires_grad for p in model.classifier.parameters())
        before=snapshot(model); opt=torch.optim.AdamW(model.parameters(),lr=.01,weight_decay=0)
        opt.zero_grad(set_to_none=True); F.cross_entropy(model(x),y).backward(); opt.step()
        delta=changes(model,before); assert delta['backbone.0.weight']==0 and delta['classifier.weight']>0
    elif number == 8:
        for b in (1,4):
            for column in (False,True):
                source=torch.tensor([i%2 for i in range(b)],dtype=torch.float32)
                if column:source=source.unsqueeze(-1)
                old=source.clone(); result=m.prepare_labels(source)
                assert result.shape==(b,) and result.dtype==torch.long, 'Preserve B=1 batch dimension'
                assert torch.equal(source,old) and source.dtype==torch.float32
                logits=torch.randn(b,2,requires_grad=True)
                F.cross_entropy(logits,result).backward()
    elif number == 9:
        for segments in (False,True):
            batch={'input_ids':torch.tensor([[1.,2.,0.]]),'attention_mask':torch.tensor([[1.,1.,0.]]),'labels':torch.tensor([1])}
            if segments:batch['token_type_ids']=torch.zeros(1,3)
            prepared=m.prepare_inputs(batch)
            keys={'input_ids','attention_mask'}|({'token_type_ids'} if segments else set())
            assert prepared is not batch and set(prepared)==keys
            assert all(t.dtype==torch.long and t.shape==(1,3) for t in prepared.values())
            assert batch['input_ids'].dtype==torch.float32
            assert nn.Embedding(3,4)(prepared['input_ids']).shape==(1,3,4)
    elif number == 10:
        batch={'input_ids':torch.tensor([[1,2]]),'labels':torch.tensor([0]),'scores':torch.ones(1,2,requires_grad=True)}
        result=m.inspect_batch(batch)
        assert set(result)==set(batch)
        for key,tensor in batch.items():
            assert result[key]=={'shape':tuple(tensor.shape),'dtype':str(tensor.dtype),'device':str(tensor.device),'requires_grad':tensor.requires_grad}
    elif number == 11:
        model=fresh_model(); reference=fresh_model()
        opt=torch.optim.AdamW(model.parameters(),lr=.01,weight_decay=0)
        reference_opt=torch.optim.AdamW(reference.parameters(),lr=.01,weight_decay=0)
        for b in (4,1,4):
            x,y=data(b)
            reference_opt.zero_grad(set_to_none=True)
            expected=F.cross_entropy(reference(x),y); expected.backward(); reference_opt.step()
            result=m.train_step(model,opt,x,y)
            assert isinstance(result,float) and math.isclose(result,expected.item(),rel_tol=1e-5)
            for p,q in zip(model.parameters(),reference.parameters()):
                assert torch.allclose(p,q,rtol=1e-5,atol=1e-7), 'Repeated steps diverge: inspect clearing and ordering'
    print(f'PASS lesson {number:02}: exercise behavior verified')
