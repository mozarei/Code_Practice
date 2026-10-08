import argparse
import csv
import json
from pathlib import Path

LABELS = {"benign": 0, "risky": 1}


def convert(input_dir, output_csv):
    files = sorted(input_dir.glob("*.json"))
    if not files:
        raise ValueError(f"No top-level JSON files found in {input_dir}")
    rows = []
    for path in files:
        with path.open(encoding="utf-8") as f:
            try:
                payload = json.load(f)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path.name}: invalid JSON") from exc
        if not isinstance(payload, dict) or not isinstance(payload.get("examples"), list):
            raise ValueError(f"{path.name}: expected an examples list")
        for index, example in enumerate(payload["examples"]):
            location = f"{path.name}, record {index}"
            if not isinstance(example, dict):
                raise ValueError(f"{location}: example must be an object")
            if example.get("excluded") is True:
                continue
            try:
                title = example["document"]["title"]
                body = example["document"]["body"]
                risk = example["annotation"]["risk"]
            except (KeyError, TypeError) as exc:
                raise ValueError(f"{location}: missing or invalid required field") from exc
            if not isinstance(title, str) or not isinstance(body, str):
                raise ValueError(f"{location}: title and body must be strings")
            title, body = title.strip(), body.strip()
            if not title or not body:
                raise ValueError(f"{location}: title and body must be nonempty")
            if not isinstance(risk, str) or risk not in LABELS:
                raise ValueError(f"{location}: unknown risk category {risk!r}")
            rows.append({"text": title + "\n" + body, "label": LABELS[risk]})
    if not rows:
        raise ValueError("No retained examples")
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["text", "label"])
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output-csv", type=Path, required=True)
    args = parser.parse_args()
    print(f"Wrote {convert(args.input_dir, args.output_csv)} rows")
