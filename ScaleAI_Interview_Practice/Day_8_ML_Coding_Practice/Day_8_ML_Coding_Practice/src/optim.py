from copy import deepcopy
import torch
def build_optimizer(model,lr):
    # trainable_model=deepcopy(model)
    return torch.optim.AdamW(model.parameters(),lr=lr)
