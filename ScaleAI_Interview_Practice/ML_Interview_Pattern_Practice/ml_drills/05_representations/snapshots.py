def take_snapshot(model):
    # breakpoint()
    return {name:p.detach().clone() for name,p in model.backbone.named_parameters()}
