import torch
import torch.nn.functional as F
from common import fresh_model,run_case
def build():
    model=fresh_model()
    optimizer=torch.optim.AdamW(model.parameters(),lr=.01,weight_decay=0)
    return model,optimizer
def prepare(ids,mask,labels):
    return {'input_ids':ids,'attention_mask':mask},labels
def update(model,optimizer,inputs,targets):
    optimizer.zero_grad(set_to_none=True)
    logits=model(**inputs)
    loss=F.cross_entropy(logits,targets).detach()
    loss.backward()
    optimizer.step()
    return loss.detach().item()
if __name__=='__main__':run_case(build,prepare,update)
