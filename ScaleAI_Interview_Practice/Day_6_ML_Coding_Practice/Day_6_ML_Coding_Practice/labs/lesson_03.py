import torch
import torch.nn.functional as F
from labs.common import fresh_model, data, expected_error
def run(debug=False):
    model = fresh_model(); x, labels = data()
    logits = model(x); loss = F.cross_entropy(logits, labels)
    print('logits:', logits, 'shape:', tuple(logits.shape))
    print('logits graph:', type(logits.grad_fn).__name__)
    print('loss:', loss.item(), 'graph:', type(loss.grad_fn).__name__)
    detached = loss.detach()
    print('detached:', detached.requires_grad, detached.grad_fn, detached.device)
    expected_error('backward through detached loss', detached.backward)
    with torch.no_grad():
        untracked = model(x)
    print('no_grad output:', untracked.requires_grad, untracked.grad_fn)
    model.eval()
    eval_logits = model(x)
    print('eval output still tracks:', eval_logits.requires_grad)
    loss.backward()  # Original tracked loss is still usable.
