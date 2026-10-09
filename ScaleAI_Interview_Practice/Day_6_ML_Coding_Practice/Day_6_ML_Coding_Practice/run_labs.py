"""One lesson at a time: explain -> predict -> observe -> edit -> check -> decide next."""
import argparse
import importlib
import json
from datetime import datetime, timezone
from pathlib import Path
import torch
from labs.checks import check
ROOT=Path(__file__).resolve().parent

def log(number, prediction):
    path=ROOT/'output/learning_log.jsonl'; path.parent.mkdir(exist_ok=True)
    with path.open('a',encoding='utf-8') as f:
        f.write(json.dumps({'time':datetime.now(timezone.utc).isoformat(),
                            'lesson':number,'prediction':prediction},ensure_ascii=False)+'\n')

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--lesson',type=int,choices=range(1,12),default=1)
    parser.add_argument('--demo',action='store_true',help='Run just this demo without questions')
    parser.add_argument('--all-demos',action='store_true',help='Explicit batch mode; not the recommended learning path')
    parser.add_argument('--check',action='store_true',help='Check the selected coding exercise only')
    parser.add_argument('--exercise-dir',type=Path,help='Optional alternative exercise folder')
    parser.add_argument('--pdb',action='store_true',help='Pause inside lesson 10 with breakpoint()')
    args=parser.parse_args(); torch.set_num_threads(2); torch.manual_seed(19)
    lessons=json.loads((ROOT/'labs/lessons.json').read_text(encoding='utf-8'))
    if args.check:
        check(args.lesson,args.exercise_dir); return
    if args.demo or args.all_demos:
        numbers=range(1,12) if args.all_demos else [args.lesson]
        for number in numbers:
            print(f'\n=== LESSON {number:02}: {lessons[number-1]["title"]} ===',flush=True)
            importlib.import_module(f'labs.lesson_{number:02}').run(debug=args.pdb)
        return
    number=args.lesson
    while number<=11:
        info=lessons[number-1]
        print(f'\nLESSON {number:02}: {info["title"]}\n\n{info["explanation"]}')
        print('\nPREDICT:',info['prediction'])
        prediction=input('Your prediction (or q to stop): ')
        if prediction.strip().lower()=='q':return
        log(number,prediction)
        importlib.import_module(f'labs.lesson_{number:02}').run(debug=args.pdb)
        print('\nCompare the printed observations with your prediction.')
        print('EXERCISE:',info['task_file'],'\n',info['task'])
        while True:
            choice=input('Edit the file in VS Code; enter c to check, r to rerun demo, or q to stop: ').strip().lower()
            if choice=='q':return
            if choice=='r':
                importlib.import_module(f'labs.lesson_{number:02}').run(debug=args.pdb); continue
            if choice!='c':continue
            try:check(number,args.exercise_dir)
            except Exception as error:
                print('Not passed yet:',type(error).__name__,str(error))
                print('Inspect the relevant values; use the coach prompt if you need one hint.')
            else:break
        print('Explain WHY the exercise passed in your own words before moving on.')
        if number==11 or input('Continue to the next topic? y / anything else to stop: ').strip().lower()!='y':return
        number+=1

if __name__=='__main__':main()
