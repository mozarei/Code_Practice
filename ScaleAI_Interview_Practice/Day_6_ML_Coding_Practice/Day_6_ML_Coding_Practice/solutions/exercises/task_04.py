import torch
import torch.nn.functional as F

def observe_backward(weight, x, target):
    weight.grad = None
    before = weight.detach().clone()
    loss = (weight * x - target).square()
    loss.backward()
    return before, weight.detach().clone(), weight.grad.detach().clone()
