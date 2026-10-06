import argparse
import csv
import json
from pathlib import Path

LABELS = {"routine": 0, "urgent": 1}


def convert(input_dir, output_csv):
    paths = sorted(p for p in Path(input_dir).glob("*.json") if p.is_file())
    if not paths:
        raise ValueError("No immediate JSON input files")
    rows = []
    for path in paths:
        try:
            with path.open(encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path.name}: malformed JSON") from exc
        if not isinstance(data, dict) or not isinstance(data.get("records"), list):
            raise ValueError(f"{path.name}: expected an object with a records list")
        for index, item in enumerate(data["records"]):
            location = f"{path.name}, record {index}"
            if not isinstance(item, dict):
                raise ValueError(f"{location}: record must be an object")
            if item.get("include") is False:
                continue
            try:
                title = item["content"]["title"]
                body = item["content"]["body"]
                category = item["review"]["category"]
            except (KeyError, TypeError) as exc:
                raise ValueError(f"{location}: missing or invalid required field") from exc
            if not isinstance(title, str) or not isinstance(body, str):
                raise ValueError(f"{location}: title/body must be strings")
            title, body = title.strip(), body.strip()
            if not title or not body:
                raise ValueError(f"{location}: empty title/body")
            if not isinstance(category, str) or category not in LABELS:
                raise ValueError(f"{location}: unknown category")
            rows.append([title + "\n" + body, LABELS[category]])
    if not rows:
        raise ValueError("No retained training rows")
    out = Path(output_csv)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["text", "label"])
        writer.writerows(rows)
    return len(rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output-csv", type=Path, required=True)
    args = parser.parse_args()
    print(f"Wrote {convert(args.input_dir, args.output_csv)} rows")
