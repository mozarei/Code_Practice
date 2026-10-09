import torch
def run(debug=False):
    weight = torch.nn.Parameter(torch.tensor(2.))
    before = weight.detach().clone()
    print('Before: w=', weight.item(), 'grad=', weight.grad)
    loss = (weight * 3. - 1.).square()
    print('After forward: loss=', loss.item(), 'w=', weight.item(), 'grad=', weight.grad)
    loss.backward()
    print('After backward: w=', weight.item(), 'grad=', weight.grad.item())
    print('Weights unchanged:', torch.equal(weight.detach(), before))
    optimizer = torch.optim.SGD([weight], lr=.1)
    optimizer.step()
    print('After SGD step: w=', weight.item(), 'grad still=', weight.grad.item())
