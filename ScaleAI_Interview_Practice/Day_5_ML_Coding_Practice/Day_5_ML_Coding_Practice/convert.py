"""Implement the contract in PART_1.md from this starter."""
import argparse
import csv
import json
from pathlib import Path


def convert(input_dir, output_csv):
    # raise NotImplementedError("Implement conversion")
    print("It is working")
    input_path = Path(input_dir)
    files = list(input_path.glob("*json"))
    files.sort()


    rows = []
    for file_path in files:
        with open(file_path, "r") as file:
            data = json.load(file)

            for record in data:
                if not isinstance(record, dict):
                    raise ValueError("record is not Dict")
                skip = record.get("skip")
                #print(skip)
                if skip is True:
                    continue
                messages = record.get('messages')
                if not isinstance(messages, list):
                    raise ValueError("Messages are not List")

                last_user = None
                label = None
                for message in messages:
                    if not isinstance(message, dict):
                        raise ValueError("message is not a list")
                    role = message.get("role")
                    if not isinstance(role, str):
                        raise ValueError("role is not str")
                    if role == "user":
                        last_user = message
                if last_user is None:
                    raise ValueError("last user is none")

                content = last_user.get("content")
                if not isinstance(content, str):
                    raise ValueError("content is not str")
                text = content.strip() 
                if not text:
                    raise ValueError("content is empty after strip")

                
                annotations = record.get("annotation")
                if not isinstance(annotations, dict):
                    raise ValueError("anno is not Dict")

                ann = annotations.get("needs_review")
                if not isinstance(ann, bool):
                    raise ValueError("ann is not a bool")
                if ann is False:
                    label = 0
                elif ann is True:
                    label = 1
                else: 
                    raise("ann is missing")

                rows.append([text,label])

    output_path = Path(output_csv)
    output_path.parent.mkdir(parents=True, exist_ok=True)


    with open(output_path, "w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["text","label"])
        writer.writerows(rows)
                

              
                        
                    
                    

                
                    
               
                
            


    



def main():
    # raise NotImplementedError("Implement --input-dir and --output-csv")
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input-dir",
        #required=True
        help= "Dir containing JSON files",
        default="fixtures/raw"
    )

    parser.add_argument(
        "--output-csv",
        help="output in csv",
        default="output/train.csv"
    )

    args = parser.parse_args()
    convert(args.input_dir, args.output_csv)



if __name__ == "__main__":
    main()
