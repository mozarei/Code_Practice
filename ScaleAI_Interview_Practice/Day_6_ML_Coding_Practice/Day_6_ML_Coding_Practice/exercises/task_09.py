import torch
import torch.nn.functional as F

def prepare_inputs(batch):
    """Return a NEW dict with input_ids and attention_mask as torch.long, plus token_type_ids as torch.long if present. Omit labels. Supplied ID values are already integer-valued. Do not mutate the original dictionary or tensors in place."""
    raise NotImplementedError("Write your solution here")
