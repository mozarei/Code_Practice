import torch
import torch.nn.functional as F

def inspect_batch(batch):
    return {key: {'shape': tuple(value.shape), 'dtype': str(value.dtype),
                  'device': str(value.device), 'requires_grad': value.requires_grad}
            for key, value in batch.items()}
