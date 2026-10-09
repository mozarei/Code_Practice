import torch
import torch.nn.functional as F

def train_step(model, optimizer, x, labels):
    optimizer.zero_grad(set_to_none=True)
    logits = model(x)
    loss = F.cross_entropy(logits, labels)
    loss.backward()
    optimizer.step()
    return loss.detach().item()
