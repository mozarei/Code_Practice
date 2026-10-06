"""A tiny randomly initialized text classifier; no transformer or downloads."""
import torch
from torch import nn


class TinyClassifier(nn.Module):
    def __init__(self, vocabulary_size, classes, dimension=16):
        super().__init__()
        self.embedding = nn.Embedding(vocabulary_size, dimension, padding_idx=0)
        self.classifier = nn.Linear(dimension, classes)

    def forward(self, input_ids, mask):
        embedded = self.embedding(input_ids)
        weights = mask.unsqueeze(-1).to(embedded.dtype)
        pooled = (embedded * weights).sum(dim=1) / weights.sum(dim=1).clamp_min(1)
        return self.classifier(pooled)


def check_padding_invariance(model, input_ids, mask):
    """For this architecture, appending only PAD must preserve logits."""
    one = input_ids[:1]
    one_mask = mask[:1]
    extra = torch.zeros((1, 5), dtype=one.dtype)
    was_training = model.training
    model.eval()
    with torch.no_grad():
        a = model(one, one_mask)
        b = model(torch.cat([one, extra], dim=1), torch.cat([one_mask, extra.bool()], dim=1))
    model.train(was_training)
    if not torch.allclose(a, b, atol=1e-6, rtol=1e-5):
        raise AssertionError("Padding changed logits: inspect pooling sum and denominator")
