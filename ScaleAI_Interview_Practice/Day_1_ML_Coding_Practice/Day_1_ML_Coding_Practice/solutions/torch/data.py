"""Read two-column CSV, tokenize, build a local vocabulary, and pad."""
import csv
import re
import torch


def load_batch(path):
    with path.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    if not rows:
        raise ValueError("Dataset has no rows")
    texts = [row["text"] for row in rows]
    labels = [int(row["label"]) for row in rows]
    if min(labels) < 0 or set(labels) != set(range(max(labels) + 1)):
        raise ValueError("Expected contiguous class IDs starting at zero")
    words = [re.findall(r"\w+", text.lower()) or ["<empty>"] for text in texts]
    vocabulary = {"<pad>": 0, "<unk>": 1}
    for word in sorted({word for sentence in words for word in sentence}):
        vocabulary[word] = len(vocabulary)
    encoded = [[vocabulary[word] for word in sentence] for sentence in words]
    width = max(map(len, encoded))
    ids = torch.tensor([seq + [0] * (width - len(seq)) for seq in encoded], dtype=torch.long)
    mask = ids.ne(0)
    targets = torch.tensor(labels, dtype=torch.long)
    return ids, mask, targets, vocabulary, max(labels) + 1
