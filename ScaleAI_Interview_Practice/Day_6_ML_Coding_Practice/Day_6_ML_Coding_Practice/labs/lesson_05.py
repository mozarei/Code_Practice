import torch
import torch.nn.functional as F
from labs.common import fresh_model, data, snapshot, report
def run(debug=False):
    x, labels = data()
    for scope in ('all', 'head'):
        model = fresh_model(); before = snapshot(model)
        selected = model.parameters() if scope == 'all' else model.classifier.parameters()
        optimizer = torch.optim.AdamW(selected, lr=.01, weight_decay=0)
        name_by_id = {id(p): name for name, p in model.named_parameters()}
        print('\nOPTIMIZER SCOPE:', scope)
        for group in optimizer.param_groups:
            print('lr=', group['lr'], 'names=', [name_by_id[id(p)] for p in group['params']])
        optimizer.zero_grad(set_to_none=True)
        F.cross_entropy(model(x), labels).backward()
        print('After backward'); report(model, before, optimizer)
        print('AdamW state entries BEFORE step:', len(optimizer.state))
        optimizer.step()
        print('After step'); report(model, before, optimizer)
        print('AdamW state entries AFTER step:', len(optimizer.state))
