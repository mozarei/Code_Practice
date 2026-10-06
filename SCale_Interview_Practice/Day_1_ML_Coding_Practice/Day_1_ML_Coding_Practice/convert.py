"""Question 1 starter. Implement the contract in PART_1.md."""

import argparse
import csv
import json
from pathlib import Path


def convert(input_dir, output_csv):
    input_path = Path(input_dir)

    # Find immediate lowercase *.json files and sort lexicographically
    files = list(input_path.glob("*.json"))
    files.sort()

    # Reject if there are no input JSON files
    if not files:
        raise ValueError("No input JSON files found")

    # Collect rows first. Do NOT open output file yet.
    rows = []

    # -------------------------
    # PHASE 1: VALIDATE
    # -------------------------
    for file_path in files:

        # Load JSON
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"{file_path}: malformed JSON") from e

        # Top-level JSON must be an object
        if not isinstance(data, dict):
            raise ValueError(f"{file_path}: expected top-level object")

        # "examples" must exist and be a list
        examples = data.get("examples")

        if not isinstance(examples, list):
            raise ValueError(f"{file_path}: 'examples' must be a list")

        # enumerate gives us the zero-based record index
        for index, example in enumerate(examples):

            # Each example must be an object
            if not isinstance(example, dict):
                raise ValueError(
                    f"{file_path}: record {index}: example must be an object"
                )

            # Skip before validating other fields
            if example.get("excluded") is True:
                continue

            # Validate document
            document = example.get("document")

            if not isinstance(document, dict):
                raise ValueError(
                    f"{file_path}: record {index}: missing or invalid document"
                )

            title = document.get("title")
            body = document.get("body")

            if not isinstance(title, str) or not title.strip():
                raise ValueError(
                    f"{file_path}: record {index}: missing or invalid title"
                )

            if not isinstance(body, str) or not body.strip():
                raise ValueError(
                    f"{file_path}: record {index}: missing or invalid body"
                )

            # Build text
            text = f"{title.strip()}\n{body.strip()}"

            # Validate annotation
            annotation = example.get("annotation")

            if not isinstance(annotation, dict):
                raise ValueError(
                    f"{file_path}: record {index}: missing or invalid annotation"
                )

            risk = annotation.get("risk")

            # Exact category mapping
            if risk == "benign":
                label = 0
            elif risk == "risky":
                label = 1
            else:
                raise ValueError(
                    f"{file_path}: record {index}: unknown risk category"
                )

            # Record is valid
            rows.append([text, label])

    # Empty lists in individual files are fine.
    # But the FINAL retained dataset cannot be empty.
    if not rows:
        raise ValueError("No retained records")

    # -------------------------
    # PHASE 2: WRITE
    # -------------------------

    output_path = Path(output_csv)

    # Allowed only after validation succeeds
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow(["text", "label"])
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input-dir",
        required=True,
        help="Directory containing JSON files"
    )

    parser.add_argument(
        "--output-csv",
        required=True,
        help="Path to output CSV file"
    )

    args = parser.parse_args()

    convert(args.input_dir, args.output_csv)


if __name__ == "__main__":
    main()