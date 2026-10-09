import torch
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from labs.common import fresh_model, snapshot, report
class Rows(Dataset):
    def __init__(self):
        self.rows = [{'features': [1., 2.], 'label': 0},
                     {'features': [-1., .5], 'label': 1},
                     {'features': [.5, -2.], 'label': 1}]
    def __len__(self): return len(self.rows)
    def __getitem__(self, i): return self.rows[i]
def collate(examples):
    return {'features': torch.tensor([r['features'] for r in examples]),
            'labels': torch.tensor([r['label'] for r in examples], dtype=torch.long)}
def run(debug=False):
    dataset = Rows()
    print('Dataset record:', dataset[0], type(dataset[0]))
    loader = DataLoader(dataset, batch_size=2, collate_fn=collate, drop_last=False)
    model = fresh_model(); optimizer = torch.optim.AdamW(model.parameters(), lr=.01, weight_decay=0)
    for batch in loader:
        before = snapshot(model)
        for key, x in batch.items():
            print(key, type(x), tuple(x.shape), x.dtype, x.device, x.requires_grad)
        optimizer.zero_grad(set_to_none=True)
        inputs = batch['features']; labels = batch['labels']
        logits = model(inputs); loss = F.cross_entropy(logits, labels)
        print('Model -> loss:', type(logits), tuple(logits.shape), loss.item(), loss.requires_grad)
        if debug:
            print('Try: p loss.requires_grad; p model.backbone[0].weight.grad; c')
            breakpoint()
        loss.backward(); optimizer.step()
        report(model, before, optimizer)
        if debug:
            print('Try: p model.backbone[0].weight.grad; p optimizer.param_groups[0]["lr"]; c')
            breakpoint()
