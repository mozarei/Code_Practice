import torch
import torch.nn.functional as F

def select_parameters(model, scope):
    if scope == 'all':
        return list(model.parameters())
    if scope == 'backbone':
        return list(model.backbone.parameters())
    if scope == 'head':
        return list(model.classifier.parameters())
    raise ValueError(scope)
