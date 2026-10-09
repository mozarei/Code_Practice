import torch


def make_collator(tokenizer):
    def collate(examples):
        texts=[row["text"] for row in examples]
        batch=tokenizer(texts,padding=True,truncation=True,max_length=64,return_tensors="pt")
        # batch["input_ids"]=batch["input_ids"]#.float()
        batch["labels"]=torch.tensor([row["label"] for row in examples],dtype=torch.long)
        return batch
    return collate
