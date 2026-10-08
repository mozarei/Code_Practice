import torch.nn.functional as F


def classification_loss(logits, labels):
    """Return a scalar classification loss for this batch."""
    targets=labels
    return F.cross_entropy(logits,targets)
