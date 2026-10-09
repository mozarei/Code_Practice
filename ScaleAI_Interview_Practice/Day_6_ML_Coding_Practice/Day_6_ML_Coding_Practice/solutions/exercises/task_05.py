import torch
import torch.nn.functional as F

def make_optimizer(model, scope):
    parameters = model.parameters() if scope == 'all' else model.classifier.parameters()
    return torch.optim.AdamW(parameters, lr=.01, weight_decay=0)
