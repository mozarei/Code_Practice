import torch
import torch.nn.functional as F
from labs.common import fresh_model, data, snapshot, changes
def run(debug=False):
    model = fresh_model(); optimizer = torch.optim.AdamW(model.parameters(), lr=.01, weight_decay=0)
    x, labels = data(); before = snapshot(model)
    def state(label):
        norms = {n: None if p.grad is None else round(p.grad.norm().item(),6)
                 for n,p in model.named_parameters()}
        print('\n' + label)
        print('max deltas:', changes(model, before))
        print('gradient norms:', norms, 'optimizer state entries:', len(optimizer.state))
    state('Initial')
    optimizer.zero_grad(set_to_none=True); state('1. zero_grad')
    logits = model(x); state('2. forward')
    loss = F.cross_entropy(logits, labels); state('3. loss')
    print('loss=', loss.item(), 'requires_grad=', loss.requires_grad)
    loss.backward(); state('4. backward')
    optimizer.step(); state('5. step')
    optimizer.zero_grad(set_to_none=True); state('6. next iteration clear')
