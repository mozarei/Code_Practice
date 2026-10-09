from labs.common import fresh_model
def run(debug=False):
    model = fresh_model()
    print(model)
    print('Immediate children:', [name for name, _ in model.named_children()])
    print('All registered modules:', [name or '<root>' for name, _ in model.named_modules()])
    for name, p in model.named_parameters():
        print(name, tuple(p.shape), 'scalar count=', p.numel())
    print('Parent parameter tensors:', len(list(model.parameters())))
    print('Backbone tensors:', len(list(model.backbone.parameters())))
    print('Head tensors:', len(list(model.classifier.parameters())))
    print('Parent direct tensors:', len(list(model.parameters(recurse=False))))
    head_ids = {id(p) for p in model.classifier.parameters()}
    print('Head objects are also in parent:', head_ids <= {id(p) for p in model.parameters()})
