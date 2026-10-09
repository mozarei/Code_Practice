import torch
import torch.nn.functional as F

def accumulated_gradient(weight, repeats):
    weight.grad = None
    for _ in range(repeats):
        weight.square().backward()
    return weight.grad.detach().clone()
