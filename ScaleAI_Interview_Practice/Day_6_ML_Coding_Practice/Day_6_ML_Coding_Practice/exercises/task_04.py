import torch
import torch.nn.functional as F

def observe_backward(weight, x, target):
    """Clear weight.grad, independently snapshot weight, compute (weight*x-target)^2, and backward. Return (before_clone, after_clone, gradient_clone). Do not update weight."""
    raise NotImplementedError("Write your solution here")
