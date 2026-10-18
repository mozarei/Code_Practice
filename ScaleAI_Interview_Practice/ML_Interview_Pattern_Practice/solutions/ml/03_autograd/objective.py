import torch.nn.functional as F
def classification_loss(logits,labels):
    targets=labels
    return F.cross_entropy(logits,targets)
