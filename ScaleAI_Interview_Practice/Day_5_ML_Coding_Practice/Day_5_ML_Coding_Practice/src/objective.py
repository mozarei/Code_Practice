import torch.nn.functional as F


def classification_loss(logits, labels):
    """Return a scalar classification loss for this batch."""
    targets=labels.unsqueeze(-1)
    return F.cross_entropy(logits,targets)
