import torch
import torch.nn.functional as F

def prepare_inputs(batch):
    keys = ['input_ids', 'attention_mask']
    if 'token_type_ids' in batch:
        keys.append('token_type_ids')
    return {key: batch[key].long() for key in keys}
