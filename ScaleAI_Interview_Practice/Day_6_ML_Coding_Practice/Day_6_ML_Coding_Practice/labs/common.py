"""Small deterministic CPU models. Read this file before the lessons."""
import torch
from torch import nn

class TinyClassifier(nn.Module):
    def __init__(self):
        super().__init__()  # Register children with nn.Module.
        self.backbone = nn.Sequential(nn.Linear(2, 3), nn.Tanh())
        self.classifier = nn.Linear(3, 2)

    def forward(self, x):
        features = self.backbone(x)
        return self.classifier(features)  # Raw scores, not probabilities.

def fresh_model():
    torch.manual_seed(19)
    return TinyClassifier().to('cpu')

def data(count=4):
    x = torch.tensor([[1., 2.], [-1., .5], [.5, -2.], [2., 1.]])[:count]
    y = torch.tensor([0, 1, 1, 0], dtype=torch.long)[:count]
    return x, y

def snapshot(model):
    # clone is essential: detach alone still shares storage with the parameter.
    return {name: p.detach().clone() for name, p in model.named_parameters()}

def report(model, before, optimizer=None):
    ids = {id(p) for g in optimizer.param_groups for p in g['params']} if optimizer else set()
    print('name | requires_grad | grad norm | in optimizer | max weight change')
    for name, p in model.named_parameters():
        grad = 'None' if p.grad is None else f'{p.grad.norm().item():.6f}'
        change = (p.detach() - before[name]).abs().max().item()
        print(f'{name} | {p.requires_grad} | {grad} | {id(p) in ids} | {change:.8f}')

def changes(model, before):
    return {name: (p.detach()-before[name]).abs().max().item()
            for name, p in model.named_parameters()}

def expected_error(label, operation):
    # Lessons deliberately show failing operations. The interview mock does not catch them.
    import traceback
    print('\nEXPECTED FAILURE:', label)
    try:
        operation()
    except (RuntimeError, ValueError, TypeError, IndexError):
        traceback.print_exc()
    else:
        raise AssertionError('This experiment was expected to fail')
