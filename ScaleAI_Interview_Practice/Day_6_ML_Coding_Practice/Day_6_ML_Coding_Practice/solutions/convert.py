import argparse
import csv
import json
from pathlib import Path
import sys

def convert(input_dir, output_csv):
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
        if not isinstance(data,dict) or not isinstance(data.get('tickets'),list):
            raise ValueError(f'{path.name}: expected an object with tickets list')
        for index,item in enumerate(data['tickets']):
            prefix=f'{path.name}: record {index}'
            if not isinstance(item,dict):raise ValueError(prefix+': expected an object')
            if item.get('synthetic') is True:continue
            payload=item.get('payload')
            if not isinstance(payload,dict):raise ValueError(prefix+': invalid payload')
            title=payload.get('title');paragraphs=payload.get('paragraphs')
            if not isinstance(title,str) or not title.strip():raise ValueError(prefix+': invalid title')
            if not isinstance(paragraphs,list):raise ValueError(prefix+': paragraphs must be a list')
            if not all(isinstance(p,str) for p in paragraphs):raise ValueError(prefix+': paragraph must be a string')
            parts=[p.strip() for p in paragraphs if p.strip()]
            if not parts:raise ValueError(prefix+': no nonblank paragraphs')
            routing=item.get('routing')
            if not isinstance(routing,str) or routing not in {'normal','review'}:
                raise ValueError(prefix+': invalid routing')
            rows.append([title.strip()+'\n'+'\n'.join(parts),0 if routing=='normal' else 1])
    if not rows:raise ValueError('No retained tickets')
    output=Path(output_csv);output.parent.mkdir(parents=True,exist_ok=True)
    with output.open('w',encoding='utf-8',newline='') as f:
        writer=csv.writer(f);writer.writerow(['text','label']);writer.writerows(rows)
    return len(rows)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--input-dir',required=True)
    parser.add_argument('--output-csv',required=True)
    args=parser.parse_args()
    try:count=convert(args.input_dir,args.output_csv)
    except (ValueError,OSError) as error:
        print(error,file=sys.stderr);raise SystemExit(1)
    print(f'Wrote {count} CSV records')

if __name__=='__main__':main()
