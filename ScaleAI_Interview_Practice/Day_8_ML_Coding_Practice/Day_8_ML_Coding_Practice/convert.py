"""Day 8 Part 1. Join documents and final reviews into CSV."""
import argparse
import csv
import json
from pathlib import Path


def convert(input_dir, output_csv):
    input_path = Path(input_dir)

    # ADDED: Only process regular JSON files, in sorted filename order.
    input_files = sorted(
        file for file in input_path.glob("*.json") if file.is_file()
    )
    # ADDED: Reject an input directory with no regular JSON files.
    if not input_files:
        raise ValueError(f"{input_path}: no regular JSON files found")

    rows = []
    for files in input_files:
        # ADDED: Report malformed JSON with the filename.
        try:
            with open(files, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, UnicodeError) as exc:
            raise ValueError(f"{files}: invalid JSON: {exc}") from exc

        # ADDED: Validate the top-level JSON object before calling .get().
        if not isinstance(data, dict):
            raise ValueError(f"{files}: top-level JSON must be an object")

        documents = data.get("documents")
        reviews = data.get("reviews")
        # FIXED: Include filename in container validation errors.
        if not isinstance(documents, list):
            raise ValueError(f"{files}: documents must be a list")
        if not isinstance(reviews, list):
            raise ValueError(f"{files}: reviews must be a list")

        seen_ids = set()
        for number_id, items in enumerate(documents):
            # FIXED: Include file and zero-based document record number in errors.
            location = f"{files}: documents record {number_id}"
            if not isinstance(items, dict):
                raise ValueError(f"{location}: document must be an object")
            ids = items.get("id")
            if not isinstance(ids, str) or not ids.strip():
                raise ValueError(f"{location}: id must be a nonblank string")
            if ids in seen_ids:
                raise ValueError(f"{location}: duplicate document id {ids!r}")
            seen_ids.add(ids)

            contents = items.get("content")
            if not isinstance(contents, dict):
                raise ValueError(f"{location}: content must be an object")
            title = contents.get("title")
            body = contents.get("body")
            if not isinstance(title, str) or not title.strip():
                raise ValueError(f"{location}: title must be a nonblank string")
            if not isinstance(body, str) or not body.strip():
                raise ValueError(f"{location}: body must be a nonblank string")

        last_review = {}
        for number_id, items in enumerate(reviews):
            # FIXED: Include file and zero-based review record number in errors.
            location = f"{files}: reviews record {number_id}"
            if not isinstance(items, dict):
                raise ValueError(f"{location}: review must be an object")
            document_id = items.get("document_id")
            if not isinstance(document_id, str) or not document_id.strip():
                raise ValueError(f"{location}: document_id must be a nonblank string")

            status = items.get("status")
            decision = items.get("decision")
            valid_status = ("draft", "final")
            valid_decision = ("allow", "review")
            if status not in valid_status:
                raise ValueError(f"{location}: status must be draft or final")
            if status == "final" and decision not in valid_decision:
                raise ValueError(f"{location}: final decision must be allow or review")
            # Draft decisions are ignored. Later final decisions overwrite earlier ones.
            if status == "final" and document_id in seen_ids:
                last_review[document_id] = decision

        # Preserve the original document order within each sorted file.
        for items in documents:
            document_id = items["id"]
            if document_id not in last_review:
                continue
            contents = items["content"]
            text = contents["title"].strip() + "\n" + contents["body"].strip()
            label = 0 if last_review[document_id] == "allow" else 1
            rows.append([text, label])

    # ADDED: Reject empty exports before creating directories or opening CSV.
    if not rows:
        raise ValueError(f"{input_path}: no rows to export")

    output_path = Path(output_csv)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["text", "label"])
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser()
    # FIXED: Both CLI flags are required by the contract.
    parser.add_argument("--input-dir", required=True, help="Directory containing JSON files")
    parser.add_argument("--output-csv", required=True, help="Output CSV file")
    args = parser.parse_args()
    # ADDED: Show useful input errors on stderr without a Python traceback.
    try:
        convert(args.input_dir, args.output_csv)
    except (ValueError, OSError) as exc:
        parser.exit(1, f"Error: {exc}\n")


if __name__ == "__main__":
    main()
