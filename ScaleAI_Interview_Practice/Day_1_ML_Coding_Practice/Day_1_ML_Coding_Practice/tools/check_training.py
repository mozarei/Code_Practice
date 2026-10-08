"""Execute your repaired route with a known-good CSV. Does not inspect solutions."""
import argparse
import json
import math
import subprocess
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--route", choices=["stdlib", "torch"], default="stdlib")
    parser.add_argument("--csv", type=Path, default=ROOT / "fixtures/reference_train.csv")
    args = parser.parse_args()
    route = ROOT / ("src" if args.route == "stdlib" else "torch_src")
    result = subprocess.run([sys.executable, str(route / "train.py"), "--csv", str(args.csv.resolve())],
                            capture_output=True, text=True, timeout=90)
    print(result.stdout, end="")
    if result.returncode:
        print(result.stderr, end="", file=sys.stderr)
        raise SystemExit(result.returncode)
    if args.route == "stdlib":
        line = next(line for line in result.stdout.splitlines() if line.startswith("METRICS "))
        metrics = json.loads(line[len("METRICS "):])
        assert metrics["rows"] == 12, "Expected all 12 fixture rows"
        assert metrics["weights_changed"] is True
        assert math.isfinite(metrics["final_loss"]) and metrics["final_loss"] < metrics["initial_loss"]
    else:
        assert "rows=12 " in result.stdout
        assert "Success: parameters changed" in result.stdout
    print("PASS training completion and reported invariants")
