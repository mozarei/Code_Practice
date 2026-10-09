import torch
import torch.nn.functional as F
from labs.common import expected_error
def run(debug=False):
    for b in (4, 1):
        logits = torch.randn(b, 2, requires_grad=True)
        labels = torch.tensor([i % 2 for i in range(b)], dtype=torch.long)
        column = labels.unsqueeze(-1)
        print('\nB=', b, 'logits=', tuple(logits.shape), logits.dtype)
        print('labels=', tuple(labels.shape), labels.dtype,
              'column=', tuple(column.shape), 'squeeze=', tuple(column.squeeze().shape),
              'squeeze(-1)=', tuple(column.squeeze(-1).shape))
        expected_error('column-shaped targets', lambda: F.cross_entropy(logits, column))
        expected_error('float class-index targets', lambda: F.cross_entropy(logits, labels.float()))
        if b == 1:
            expected_error('scalar targets with batched logits', lambda: F.cross_entropy(logits, column.squeeze()))
        loss = F.cross_entropy(logits, column.squeeze(-1))
        loss.backward(); print('Correct scalar loss:', loss.item(), 'gradient shape:', tuple(logits.grad.shape))
