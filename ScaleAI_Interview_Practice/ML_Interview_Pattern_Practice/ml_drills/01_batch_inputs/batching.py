import torch
def make_collator(tokenizer):
    def collate(records):
        # breakpoint()
        # texts=records

        # values = [i['label'] for i in records]
        texts = [i['text'] for i in records]

        batch=tokenizer(texts,padding=True,truncation=True,max_length=64,return_tensors='pt')
        # breakpoint()
       # batch['input_ids']=batch['input_ids']#.float()
        #batch['attention_mask']=torch.ones_like(batch['input_ids'])
        batch['labels']=torch.tensor([record['label'] for record in records],dtype=torch.long)

        
        return batch
    return collate
