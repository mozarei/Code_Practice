"""Day 6 Part 1: implement PART_1.md. Start the timer after reading the contract."""
import argparse
import csv
import json
from pathlib import Path

def convert(input_dir, output_csv):
    input_path = Path(input_dir)
    files = list(input_path.glob("*.json"))
    files.sort()


    rows = []
    for file in files:
        if not file.is_file():
            continue
        try:
            with open(file, "r") as json_file:
                data = json.load(json_file)
        except json.JSONDecodeError as e:
            raise ValueError(f"{file}: invalid JSON: {e}") from e
    
        if not isinstance(data, dict):
            raise ValueError("Data must be Dict")
        tickets = data.get("tickets")
        if not isinstance(tickets, list):
            raise ValueError(f"{file}: tickets must be a list")
        for record_num, items in enumerate(tickets):
            if not isinstance(items, dict):
                raise ValueError(f"{file}: record {record_num}:items is not a dict")
            synthetic = items.get("synthetic")
            if synthetic is True:
                continue
            payload = items.get("payload")
            if not isinstance(payload, dict):
                raise ValueError(f"{file}: record {record_num}: invalid payload")
            title = payload.get("title")
            if not isinstance(title, str):
                raise ValueError(f"{file}: record {record_num}: title is not a str")
            if len(title.strip()) < 1:
                raise ValueError("Title is empty")
            paragraphs = payload.get("paragraphs")
            if not isinstance(paragraphs, list):
                raise ValueError("paragraphs must be a list")
            clean_paragraphs = []
            for paragraph in paragraphs:
                if not isinstance(paragraph, str):
                    raise ValueError("Paragraph must be a string")
                paragraph = paragraph.strip()
                if len(paragraph) < 1:
                    continue
                clean_paragraphs.append(paragraph)
            if len(clean_paragraphs) < 1:
                raise ValueError("NO nonblank paragraphs")
            
            text = title.strip() + "\n" + "\n".join(clean_paragraphs)
            routing = items.get("routing")
            if routing == "normal":
                label = 0
            elif routing == "review":
                label = 1
            else:
                raise ValueError("routing should be either normal or review")

            rows.append([text,label])

    output_path = Path(output_csv)

    if not rows:
        raise ValueError("No retained rows")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)

        writer.writerow(["text","label"])
        writer.writerows(rows)

                
                




def main():
    # Add argparse input/output flags and call convert.
    #raise NotImplementedError('Write your CLI here')
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input-dir",
        default="fixtures/raw",
        help="dir contains jsons"
    )

    parser.add_argument(
        "--output-csv",
        default="output/train.csv",
        help="output csv"
    )

    args = parser.parse_args()
    convert(args.input_dir, args.output_csv)

if __name__ == '__main__':
    main()
