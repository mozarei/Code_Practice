"""Day 8 Part 1. Implement the contract in PART_1.md from this starter."""
import argparse
import csv
import json
from pathlib import Path

def convert(input_dir,output_csv):
    # raise NotImplementedError('Implement the document/review join')
    print("It is working...")
    input_path = Path(input_dir)
    input_files = list(input_path.glob("*.json"))
    input_files.sort()

    for files in input_files:
        if not files.is_file():
            continue
        with open(files, "r") as f:
            data = json.load(f)

            documents = data.get("documents")
            reviews = data.get("reviews")

            print(reviews)
            break            

def main():
    # raise NotImplementedError('Add argparse input/output flags and call convert')
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input-dir",
        default="fixtures/raw",
        help="Dir contains input files"
    )


    parser.add_argument(
        "--output-csv",
        default="output/train.csv",
        help="Output csv file"
    )

    args = parser.parse_args()
    convert(args.input_dir, args.output_csv)

if __name__=='__main__':main()
