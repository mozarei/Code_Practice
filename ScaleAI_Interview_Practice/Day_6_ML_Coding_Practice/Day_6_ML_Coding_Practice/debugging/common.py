import torch
from torch import nn
class MiniClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.backbone=nn.Embedding(8,3)
        self.classifier=nn.Linear(3,2)
    def forward(self,input_ids,attention_mask):
        tokens=self.backbone(input_ids)
        mask=attention_mask.unsqueeze(-1).to(tokens.dtype)
        features=(tokens*mask).sum(1)/mask.sum(1).clamp_min(1)
        return self.classifier(features)
def fresh_model():
    torch.manual_seed(23)
    return MiniClassifier()
def run_case(build,prepare,update):
    torch.set_num_threads(2)
    model,optimizer=build()
    ids=torch.tensor([[1,2,0],[3,4,5],[2,5,0]],dtype=torch.long)
    mask=(ids!=0).long();labels=torch.tensor([0,1,0],dtype=torch.long)
    for count in (3,1,3):
        before={name:p.detach().clone() for name,p in model.named_parameters()}
        inputs,targets=prepare(ids[:count],mask[:count],labels[:count])
        loss=update(model,optimizer,inputs,targets)
        assert isinstance(loss,float) and torch.isfinite(torch.tensor(loss)), 'Need finite loss'
        assert targets.shape==(count,) and targets.dtype==torch.long, 'Class-index target contract'
        assert inputs['input_ids'].dtype==torch.long, 'Token index contract'
        for name in ('backbone.weight','classifier.weight'):
            parameter=dict(model.named_parameters())[name]
            assert parameter.requires_grad, f'Full fine-tuning requires trainable {name}'
            assert parameter.grad is not None and torch.isfinite(parameter.grad).all(), f'Missing/invalid gradient: {name}'
            assert not torch.equal(before[name],parameter.detach()), f'Weight did not update: {name}'
        print('PASS batch=',count,'loss=',round(loss,6))
    print('DRILL_COMPLETE: fresh full fine-tuning at batch sizes 3 and 1')
