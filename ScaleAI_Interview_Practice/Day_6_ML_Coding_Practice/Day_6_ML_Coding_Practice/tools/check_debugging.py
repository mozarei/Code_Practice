import argparse
import importlib.util
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'debugging'))
from debugging.common import run_case
p=argparse.ArgumentParser();p.add_argument('--file',type=Path,required=True);a=p.parse_args()
spec=importlib.util.spec_from_file_location('candidate_case',a.file.resolve())
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
run_case(m.build,m.prepare,m.update)
