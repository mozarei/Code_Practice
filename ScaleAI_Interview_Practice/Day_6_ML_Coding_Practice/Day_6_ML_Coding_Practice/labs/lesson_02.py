import torch
from torch import nn
import torch.nn.functional as F
from labs.common import fresh_model, data, snapshot, report
def run(debug=False):
    model = fresh_model()
    model.unused = nn.Parameter(torch.tensor([5.]))  # Registered, but forward never reads it.
    before = snapshot(model)
    print('BEFORE backward'); report(model, before)
    x, labels = data()
    loss = F.cross_entropy(model(x), labels)
    loss.backward()
    print('AFTER backward'); report(model, before)
    model.zero_grad(set_to_none=True)
    print('AFTER clearing'); report(model, before)
