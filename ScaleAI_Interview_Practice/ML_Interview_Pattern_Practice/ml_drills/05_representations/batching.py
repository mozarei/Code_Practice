import torch
def make_collator(tokenizer):
    def collate(records):
        texts=[record['text'] for record in records]
        batch=tokenizer(texts,padding=False,truncation=True,max_length=64,return_tensors='pt')
        batch['input_ids']=batch['input_ids'].long()
        batch['attention_mask']=batch['attention_mask']
        batch['labels']=torch.tensor([record['label'] for record in records],dtype=torch.long)
        return batch
    return collate
