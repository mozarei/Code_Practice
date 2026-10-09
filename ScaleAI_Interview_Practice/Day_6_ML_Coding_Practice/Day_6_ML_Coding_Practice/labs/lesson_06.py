import torch
import torch.nn.functional as F
from labs.common import fresh_model, data
def run(debug=False):
    w = torch.nn.Parameter(torch.tensor(2.))
    optimizer = torch.optim.SGD([w], lr=.1)
    w.square().backward(); print('First backward grad:', w.grad.item())
    w.square().backward(); print('Second fresh backward grad:', w.grad.item())
    optimizer.zero_grad(set_to_none=False); print('Clear to zero:', w.grad)
    w.square().backward(); print('New backward:', w.grad)
    optimizer.zero_grad(set_to_none=True); print('Clear to None:', w.grad)
    optimizer.zero_grad(set_to_none=False); print('False does not allocate missing grad:', w.grad)
    model = fresh_model(); x, y = data()
    head_optimizer = torch.optim.AdamW(model.classifier.parameters(), lr=.01)
    F.cross_entropy(model(x), y).backward()
    g1 = model.backbone[0].weight.grad.clone()
    head_optimizer.zero_grad(set_to_none=True)
    print('Head-only clear leaves encoder gradient:', model.backbone[0].weight.grad is not None)
    F.cross_entropy(model(x), y).backward()
    print('Excluded backbone gradients accumulated:', torch.allclose(model.backbone[0].weight.grad, 2*g1))
    model.zero_grad(set_to_none=True)
    print('Whole-model clear removes backbone gradient:', model.backbone[0].weight.grad)
