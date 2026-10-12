import csv
from torch.utils.data import Dataset


class TextRows(Dataset):
    def __init__(self, path):
        with open(path, encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames != ["text", "label"]:
                raise ValueError("Expected exactly text,label in that order")
            self.rows = []
            for index, row in enumerate(reader):
                if None in row or not row.get("text", "").strip() or row.get("label") not in {"0", "1"}:
                    raise ValueError(f"Invalid CSV record {index}")
                self.rows.append({"text": row["text"], "label": int(row["label"])})
        if not self.rows:
            raise ValueError("Empty training CSV")

    def __len__(self):
        return len(self.rows)

    def __getitem__(self, index):
        return self.rows[index]
