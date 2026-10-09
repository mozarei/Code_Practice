import torch
import torch.nn.functional as F

def freeze_backbone(model):
    for p in model.backbone.parameters():
        p.requires_grad_(False)
        p.grad = None
