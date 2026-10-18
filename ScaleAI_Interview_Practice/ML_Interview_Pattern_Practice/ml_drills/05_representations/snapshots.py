def take_snapshot(model):
    return {name:p.detach() for name,p in model.backbone.named_parameters()}
