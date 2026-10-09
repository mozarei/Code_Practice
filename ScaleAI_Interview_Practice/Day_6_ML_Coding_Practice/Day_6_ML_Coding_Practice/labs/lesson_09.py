from pathlib import Path
import torch
from transformers import AutoTokenizer
from labs.common import expected_error
def run(debug=False):
    checkpoint = Path(__file__).resolve().parents[1] / 'models/bert-tiny'
    tokenizer = AutoTokenizer.from_pretrained(checkpoint, local_files_only=True)
    inputs = tokenizer(['hello world', 'hi'], padding=True, return_tensors='pt')
    for key, value in inputs.items():
        print(key, 'shape=', tuple(value.shape), 'dtype=', value.dtype, 'values=', value.tolist())
    print('First tokens:', tokenizer.convert_ids_to_tokens(inputs['input_ids'][0].tolist()))
    table = torch.nn.Embedding(len(tokenizer), 4)
    embedded = table(inputs['input_ids'])
    print('Embedding output:', tuple(embedded.shape), 'requires_grad=', embedded.requires_grad)
    print('First output equals selected row:', torch.equal(embedded[0,0], table.weight[inputs['input_ids'][0,0]]))
    expected_error('floating token indices', lambda: table(inputs['input_ids'].float()))
    pair = tokenizer('first sentence', 'second sentence', return_tensors='pt')
    print('BERT pair segment IDs:', pair['token_type_ids'].tolist())
