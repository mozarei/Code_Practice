import torch
import torch.nn.functional as F

def gradient_report(model):
    return [{'name': name, 'requires_grad': p.requires_grad,
             'has_grad': p.grad is not None,
             'grad_norm': None if p.grad is None else p.grad.norm().item()}
            for name, p in model.named_parameters()]
