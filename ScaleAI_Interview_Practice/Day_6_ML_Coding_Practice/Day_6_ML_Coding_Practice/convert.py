"""Day 6 Part 1: implement PART_1.md. Start the timer after reading the contract."""
import argparse
import csv
import json
from pathlib import Path

def convert(input_dir, output_csv):
    input_path = Path(input_dir)
    files = list(input_path.glob("*.json"))
    files.sort()

    for file in files:
        if file.is_dir():
            continue

        with open(file, "r") as json_file:
            data = json.load(json_file)

            tickets = data.get("tickets")
            for items in tickets:
                print(type(items))
                # if items['synthetic']:
                #     continue
                
            # print(tickets)
            # break
            
       



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
