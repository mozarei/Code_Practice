from pathlib import Path
import argparse
from common_ml import ROOT,verify
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--set',required=True);p.add_argument('--solution',action='store_true');p.add_argument('--csv',type=Path)
    a=p.parse_args();directory=ROOT/('solutions/ml' if a.solution else 'ml_drills')/a.set
    verify(directory,a.csv)
