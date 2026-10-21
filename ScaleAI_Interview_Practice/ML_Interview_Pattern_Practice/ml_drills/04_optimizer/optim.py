from copy import deepcopy
import torch
def build_optimizer(model,lr):
    # working_model=deepcopy(model)
    # parameters=working_model.backbone.classifier.parameters()
    parameters=model.parameters()
    return torch.optim.AdamW(parameters,lr=0.0001)
