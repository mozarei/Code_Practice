import torch
import torch.nn.functional as F

def train_step(model, optimizer, x, labels):
    """Perform one standard training step with F.cross_entropy and return the loss as a Python float. Clear old optimizer gradients before the forward. Keep the loss graph until backward; then step."""
    raise NotImplementedError("Write your solution here")
