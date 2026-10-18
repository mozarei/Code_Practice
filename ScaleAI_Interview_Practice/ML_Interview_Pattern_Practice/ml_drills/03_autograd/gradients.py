def backward_loss(loss,optimizer):
    loss.backward()
    optimizer.zero_grad(set_to_none=True)
