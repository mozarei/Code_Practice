from copy import deepcopy
import torch
def build_optimizer(model,lr):
    working_model=model
    parameters=working_model.parameters()
    return torch.optim.AdamW(parameters,lr=lr)
