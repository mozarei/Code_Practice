"""Copyable working CLI/JSON/CSV template. Replace extract_rows for a new schema.

This example's schema is a top-level list of {text: nonblank str, label: int 0|1}.
All inputs are validated before the output file is opened.
"""
import argparse
import csv
import json
from pathlib import Path

def extract_rows(payload):
    if not isinstance(payload,list):raise ValueError('Expected a list of records')
    rows=[]
    for index,record in enumerate(payload):
        if not isinstance(record,dict):raise ValueError(f'record {index}: expected an object')
        text=record.get('text');label=record.get('label')
        if not isinstance(text,str) or not text.strip():raise ValueError(f'record {index}: invalid text')
        if type(label) is not int or label not in {0,1}:raise ValueError(f'record {index}: invalid label')
        rows.append([text.strip(),label])
    return rows

def write_rows(rows,output_csv):
    output_path=Path(output_csv)
    output_path.parent.mkdir(parents=True,exist_ok=True)
    with output_path.open('w',encoding='utf-8',newline='') as csv_file:
        writer=csv.writer(csv_file)
        writer.writerow(['text','label'])
        writer.writerows(rows)

def convert(input_dir,output_csv):
    input_path=Path(input_dir)
    if not input_path.is_dir():raise ValueError('Input directory does not exist')
    files=sorted(path for path in input_path.glob('*.json') if path.is_file())
    if not files:raise ValueError('No JSON files')
    rows=[]
    for path in files:
        try:
            with path.open(encoding='utf-8') as source:
                payload=json.load(source)
            rows.extend(extract_rows(payload))
        except (ValueError,OSError) as error:
            raise ValueError(f'{path.name}: {error}') from error
    if not rows:raise ValueError('No training records')
    write_rows(rows,output_csv)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--input-dir',required=True,help='Directory containing JSON files')
    parser.add_argument('--output-csv',required=True,help='Output CSV file')
    args=parser.parse_args()
    try:
        convert(args.input_dir,args.output_csv)
    except (ValueError,OSError) as exc:
        parser.exit(1,f'Error: {exc}\n')

if __name__=='__main__':
    main()
