"""Implement the contract in PART_1.md. Use Python's standard library."""
import argparse
import csv
import json
from pathlib import Path


def convert(input_dir, output_csv):
    

    input_path = Path(input_dir)
    files = list(input_path.glob("*.json"))
    files.sort()
    # print(files)

    rows = []

    for file_path in files:
        # print(file_path)

        with open(file_path, "r") as file:

            data = json.load(file)
            # print(data)

            records = data.get("records")
            for record in records:
                if not isinstance(record, dict):
                    raise ValueError("record is not an object")
                include = record.get("include")
                if include == False:
                    continue

                titles = record["content"]["title"]
                bodies = record["content"]["body"]

                titles = titles.strip()
                bodies = bodies.strip()

                if len(titles) == 0:
                    continue
                if len(bodies) == 0:
                    continue

                text = titles + "\n" + bodies
                if record.get("review")["category"] == "routine":
                    label = 0
                else:
                    label = 1

                rows.append([text, label])


    output_path = Path(output_csv)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w" , encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["text","label"])
        writer.writerows(rows)
                
            
    


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input-dir",
        #required = True,
        help= "Dir containing JSON files",
        default="/Users/mzarei/Desktop/Practices/Code_Practice/SCale_Interview_Practice/Day_3_ML_Coding_Practice/Day_3_ML_Coding_Practice/fixtures/raw"
    )


    parser.add_argument(
        "--output-csv",
        #required = True,
        help= "Path to the csv file",
        default="/Users/mzarei/Desktop/Practices/Code_Practice/SCale_Interview_Practice/Day_3_ML_Coding_Practice/Day_3_ML_Coding_Practice/output/train.csv"
    )

    args = parser.parse_args()
    convert(args.input_dir, args.output_csv)


    # raise NotImplementedError("Implement --input-dir and --output-csv")


if __name__ == "__main__":
    main()
