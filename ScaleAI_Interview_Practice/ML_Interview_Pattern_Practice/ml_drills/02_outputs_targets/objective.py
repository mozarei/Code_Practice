import torch.nn.functional as F
def classification_loss(logits,labels):
    #TypeError: cross_entropy_loss(): argument 'input' (position 1) must be Tensor, not SequenceClassifierOutput
    # breakpoint()
    targets=labels#.unsqueeze(-1).squeeze()
    
    # breakpoint()
    return F.cross_entropy(logits,targets)
