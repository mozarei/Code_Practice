"""Read the agreed CSV contract and create numerical features."""
import csv
from model import features


def load_data(path):
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != ["text", "label"]:
            raise ValueError("Expected CSV header text,label")
        rows = list(reader)
    if not rows:
        raise ValueError("Dataset is empty")
    data = [(features(row["text"]), int(row["label"])) for row in rows]
    if any(label not in (0, 1) for _, label in data):
        raise ValueError("Expected binary class labels")
    return data
