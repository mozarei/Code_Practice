import torch
import torch.nn.functional as F

def prepare_labels(labels):
    if labels.ndim == 2:
        labels = labels.squeeze(-1)
    return labels.long()
