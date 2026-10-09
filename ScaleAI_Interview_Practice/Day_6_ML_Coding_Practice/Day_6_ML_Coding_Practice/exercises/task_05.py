import torch
import torch.nn.functional as F

def make_optimizer(model, scope):
    """Return AdamW(lr=0.01, weight_decay=0). scope='all' manages every parameter; scope='head' manages only model.classifier parameters."""
    raise NotImplementedError("Write your solution here")
