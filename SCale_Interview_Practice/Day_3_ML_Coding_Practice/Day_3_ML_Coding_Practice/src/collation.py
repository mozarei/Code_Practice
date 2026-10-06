import torch


def make_collator(tokenizer):
    def collate(examples):
        texts = list(examples)
        labels = [item["label"] for item in examples]
        batch = tokenizer(
            texts, padding=True, truncation=True, max_length=64,
            return_tensors="pt",
        )
        batch["labels"] = torch.tensor(labels, dtype=torch.long)
        return batch
    return collate
