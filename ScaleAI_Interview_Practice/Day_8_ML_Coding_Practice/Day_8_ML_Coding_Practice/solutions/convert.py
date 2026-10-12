import argparse
import csv
import json
from pathlib import Path
import sys

def nonblank(value):
    return isinstance(value,str) and bool(value.strip())

def convert(input_dir,output_csv):
    directory=Path(input_dir)
    if not directory.is_dir():raise ValueError('Input directory does not exist')
    files=sorted(p for p in directory.glob('*.json') if p.is_file())
    if not files:raise ValueError('No immediate JSON files')
    rows=[]
    for path in files:
        try:
            with path.open(encoding='utf-8') as f:data=json.load(f)
        except (ValueError,OSError) as error:
            raise ValueError(f'{path.name}: {error}') from error
        if not isinstance(data,dict):raise ValueError(f'{path.name}: expected an object')
        documents=data.get('documents');reviews=data.get('reviews')
        if not isinstance(documents,list) or not isinstance(reviews,list):
            raise ValueError(f'{path.name}: documents and reviews must be lists')
        ordered=[];seen=set()
        for index,document in enumerate(documents):
            prefix=f'{path.name}: documents record {index}'
            if not isinstance(document,dict):raise ValueError(prefix+': expected an object')
            identifier=document.get('id');content=document.get('content')
            if not nonblank(identifier):raise ValueError(prefix+': invalid id')
            if identifier in seen:raise ValueError(prefix+': duplicate id')
            seen.add(identifier)
            if not isinstance(content,dict):raise ValueError(prefix+': invalid content')
            title=content.get('title');body=content.get('body')
            if not nonblank(title) or not nonblank(body):raise ValueError(prefix+': invalid title/body')
            ordered.append((identifier,title.strip()+'\n'+body.strip()))
        latest={}
        for index,review in enumerate(reviews):
            prefix=f'{path.name}: reviews record {index}'
            if not isinstance(review,dict):raise ValueError(prefix+': expected an object')
            identifier=review.get('document_id');status=review.get('status')
            if not nonblank(identifier):raise ValueError(prefix+': invalid document_id')
            if not isinstance(status,str) or status not in {'draft','final'}:
                raise ValueError(prefix+': invalid status')
            if status=='draft':continue  # Decision is intentionally irrelevant for drafts.
            decision=review.get('decision')
            if not isinstance(decision,str) or decision not in {'allow','review'}:
                raise ValueError(prefix+': invalid final decision')
            if identifier in seen:latest[identifier]=0 if decision=='allow' else 1
        for identifier,text in ordered:
            if identifier in latest:rows.append([text,latest[identifier]])
    if not rows:raise ValueError('No documents with final reviews')
    output=Path(output_csv);output.parent.mkdir(parents=True,exist_ok=True)
    with output.open('w',encoding='utf-8',newline='') as f:
        w=csv.writer(f);w.writerow(['text','label']);w.writerows(rows)
    return len(rows)

def main():
    p=argparse.ArgumentParser();p.add_argument('--input-dir',required=True);p.add_argument('--output-csv',required=True)
    a=p.parse_args()
    try:n=convert(a.input_dir,a.output_csv)
    except (ValueError,OSError) as error:
        print(error,file=sys.stderr);raise SystemExit(1)
    print(f'Wrote {n} CSV records')
if __name__=='__main__':main()
