from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from common_ml import cli
if __name__=='__main__':cli(Path(__file__).resolve().parent)
