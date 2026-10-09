import torch
import torch.nn.functional as F

def gradient_report(model):
    """Return a list of dictionaries, in named_parameters order, with name, requires_grad, has_grad, and grad_norm (None when no gradient, otherwise a Python float L2 norm)."""
    raise NotImplementedError("Write your solution here")
