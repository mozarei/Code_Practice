import torch
import torch.nn.functional as F

def compute_loss(model, x, labels):
    logits = model(x)
    return logits, F.cross_entropy(logits, labels)
