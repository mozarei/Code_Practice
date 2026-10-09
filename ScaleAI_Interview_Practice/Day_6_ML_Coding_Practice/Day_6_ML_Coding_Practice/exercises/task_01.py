import torch
import torch.nn.functional as F

def select_parameters(model, scope):
    """Return a LIST of parameter objects. scope is 'all', 'backbone', or 'head'. Use the actual registered modules; do not return names or copied tensors."""
    raise NotImplementedError("Write your solution here")
