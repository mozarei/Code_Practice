import torch
import torch.nn.functional as F

def accumulated_gradient(weight, repeats):
    """Start with weight.grad=None. Repeat fresh loss=weight.square() and backward repeats times. Do not step or clear between backwards. Return an independent gradient tensor."""
    raise NotImplementedError("Write your solution here")
