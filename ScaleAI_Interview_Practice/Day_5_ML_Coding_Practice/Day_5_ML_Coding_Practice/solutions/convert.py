import argparse
import csv
import json
from pathlib import Path


def convert(input_dir, output_csv):
    files=sorted(p for p in Path(input_dir).glob("*.json") if p.is_file())
    if not files:
        raise ValueError("No immediate JSON files")
    rows=[]
    for path in files:
        try:
            with path.open(encoding="utf-8") as f:
                records=json.load(f)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path.name}: malformed JSON") from exc
        if not isinstance(records,list):
            raise ValueError(f"{path.name}: expected a top-level list")
        for index,record in enumerate(records):
            where=f"{path.name}, record {index}"
            if not isinstance(record,dict):
                raise ValueError(f"{where}: record must be an object")
            if record.get("skip") is True:
                continue
            messages=record.get("messages")
            if not isinstance(messages,list):
                raise ValueError(f"{where}: messages must be a list")
            selected=None
            for message in messages:
                if not isinstance(message,dict) or not isinstance(message.get("role"),str):
                    raise ValueError(f"{where}: each message needs a string role")
                if message["role"]=="user":
                    selected=message
            if selected is None:
                raise ValueError(f"{where}: no user message")
            text=selected.get("content")
            if not isinstance(text,str) or not text.strip():
                raise ValueError(f"{where}: last user content must be a nonempty string")
            try:
                flag=record["annotation"]["needs_review"]
            except (KeyError,TypeError) as exc:
                raise ValueError(f"{where}: missing or invalid annotation") from exc
            if type(flag) is not bool:
                raise ValueError(f"{where}: needs_review must be a boolean")
            rows.append([text.strip(),int(flag)])
    if not rows:
        raise ValueError("No retained records")
    out=Path(output_csv);out.parent.mkdir(parents=True,exist_ok=True)
    with out.open("w",encoding="utf-8",newline="") as f:
        writer=csv.writer(f);writer.writerow(["text","label"]);writer.writerows(rows)
    return len(rows)


if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--input-dir",type=Path,required=True)
    parser.add_argument("--output-csv",type=Path,required=True)
    args=parser.parse_args()
    print(f"Wrote {convert(args.input_dir,args.output_csv)} rows")
