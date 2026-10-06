import argparse
import csv
import json
from pathlib import Path


def convert(input_dir, output_csv):
    files = sorted(input_dir.glob("*.json"))
    if not files:
        raise ValueError(f"No JSON files found in {input_dir}")
    rows = []
    for path in files:
        with path.open(encoding="utf-8") as f:
            try:
                payload = json.load(f)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path.name}: invalid JSON") from exc
        if not isinstance(payload, list):
            raise ValueError(f"{path.name}: expected a top-level list")
        for index, item in enumerate(payload):
            location = f"{path.name}, record {index}"
            try:
                title = item["message"]["title"]
                body = item["message"]["body"]
                approved = item["decision"]["approved"]
            except (KeyError, TypeError) as exc:
                raise ValueError(f"{location}: missing or invalid field") from exc
            if not isinstance(title, str) or not isinstance(body, str):
                raise ValueError(f"{location}: expected text strings")
            title, body = title.strip(), body.strip()
            if not title or not body or type(approved) is not bool:
                raise ValueError(f"{location}: nonempty text and a boolean approval are required")
            rows.append({"sentence": title + " | " + body,
                         "target": 0 if approved else 1})
    if not rows:
        raise ValueError("No review records")
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["sentence", "target"])
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output-csv", type=Path, required=True)
    args = parser.parse_args()
    print(f"Wrote {convert(args.input_dir, args.output_csv)} rows")
