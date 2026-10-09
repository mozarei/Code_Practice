import torch
import torch.nn.functional as F

def compute_loss(model, x, labels):
    """Return (raw_logits, scalar_loss) using F.cross_entropy. Preserve the computation graph so the caller can run loss.backward(). Do not apply softmax first."""
    raise NotImplementedError("Write your solution here")
