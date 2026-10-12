import torch.nn.functional as F

def classification_loss(logits,labels):
    targets=labels#.unsqueeze(-1).squeeze()
    return F.cross_entropy(logits,targets)
