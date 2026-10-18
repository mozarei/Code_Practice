"""Standard-library-only behavior checks and optional predict/observe demos."""
import argparse,copy,importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
def check_folder(folder,question=None,solution=False,demo=False,auto=False):
    metadata=json.loads((ROOT/'python_drills'/folder/'cases.json').read_text(encoding='utf-8'))
    path=(ROOT/'solutions/python'/folder if solution or demo else ROOT/'python_drills'/folder)/'starter.py'
    module=load(path,'answers_'+folder);passed=failed=0
    for problem in metadata['problems']:
        if question is not None and problem['number']!=question:continue
        print(f"\n{folder} | Q{problem['number']}: {problem['function']}")
        if demo:print('REFERENCE DEMO: predict before revealing the output.')
        for index,case in enumerate(problem['cases'][:2] if demo else problem['cases'],1):
            args=copy.deepcopy(case['args']);before=copy.deepcopy(args)
            if demo:
                print('Arguments:',json.dumps(args,ensure_ascii=False))
                if not auto and input('Predict, then Enter to run; q stops: ').strip().lower()=='q':return passed,failed
            try:
                try:actual=getattr(module,problem['function'])(*args)
                except Exception as error:
                    if not case['error'] or type(error).__name__!=case['error']:raise
                    actual=None
                else:
                    assert not case['error'],f"Expected {case['error']}"
                    assert type(actual) is type(case['expected']), 'Wrong result type (False and 0 are different states)'
                    assert actual==case['expected'],f"Expected {case['expected']!r}; got {actual!r}"
                assert args==before,'Input was mutated'
            except Exception as error:
                failed+=1;print(f'FAIL case {index}: {type(error).__name__}: {error}')
            else:
                passed+=1
                if demo:print('Observed:',repr(actual) if not case['error'] else case['error'])
        if not demo:print('Lookup clue:',problem['lookup'])
    print(f'Result: {passed} passed, {failed} failed')
    return passed,failed
def cli(folder=None):
    parser=argparse.ArgumentParser()
    parser.add_argument('--question',type=int,choices=[1,2,3])
    parser.add_argument('--solution',action='store_true',help='Explicitly check reference solutions')
    parser.add_argument('--demo',action='store_true',help='Predict/observe a reference example')
    parser.add_argument('--auto',action='store_true',help='Noninteractive reference demo')
    parser.add_argument('--all',action='store_true')
    parser.add_argument('--folder')
    args=parser.parse_args();selected=folder or args.folder
    if args.all:names=sorted(p.name for p in (ROOT/'python_drills').iterdir() if p.is_dir())
    elif selected:names=[selected]
    else:parser.error('Choose --folder NAME or --all')
    failed=0
    for name in names:
        _,n=check_folder(name,args.question,args.solution,args.demo,args.auto);failed+=n
    raise SystemExit(bool(failed))
