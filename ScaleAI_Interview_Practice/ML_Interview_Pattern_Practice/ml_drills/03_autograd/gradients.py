def backward_loss(loss,optimizer):
    #RuntimeError: element 0 of tensors does not require grad and does not have a grad_fn
    # breakpoint()
    # loss.requires_grad = True
    optimizer.zero_grad()
    loss.backward()

