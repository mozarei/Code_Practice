import torch
import torch.nn.functional as F

def freeze_backbone(model):
    """Freeze every model.backbone parameter and clear its existing .grad. Leave classifier parameters trainable. Modify model in place."""
    raise NotImplementedError("Write your solution here")
