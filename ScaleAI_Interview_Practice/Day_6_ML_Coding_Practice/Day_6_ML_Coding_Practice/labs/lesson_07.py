import torch
import torch.nn.functional as F
from labs.common import fresh_model, data, snapshot, report
def run(debug=False):
    x, y = data()
    for mode in ('full', 'head_only_unfrozen', 'frozen_backbone'):
        model = fresh_model()
        if mode == 'frozen_backbone':
            for p in model.backbone.parameters():
                p.requires_grad_(False); p.grad = None
        selected = model.parameters() if mode == 'full' else model.classifier.parameters()
        optimizer = torch.optim.AdamW(selected, lr=.01, weight_decay=0)
        before = snapshot(model)
        optimizer.zero_grad(set_to_none=True)
        F.cross_entropy(model(x), y).backward(); optimizer.step()
        print('\nMODE:', mode); report(model, before, optimizer)
