import torch
import torch.nn.functional as F

def prepare_labels(labels):
    """Input is integer-valued labels of shape [B] or [B,1], possibly float dtype. Return torch.long [B] for B=1 and B=4; never a scalar. Do not change the input tensor in place."""
    raise NotImplementedError("Write your solution here")
