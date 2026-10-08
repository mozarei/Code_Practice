import sys
import importlib.util
print("Python:", sys.version.split()[0])
if sys.version_info < (3, 10):
    raise SystemExit("Use Python 3.10 or newer for this practice pack.")
print("Core Day 1 route: ready; only the Python standard library is needed.")
if importlib.util.find_spec("torch") is None:
    print("Optional PyTorch route: not installed. Use src/train.py today.")
else:
    try:
        import torch
        print("Optional PyTorch route:", torch.__version__, "CPU available")
    except Exception as exc:
        print("Optional PyTorch import failed:", type(exc).__name__, str(exc))
        print("Use the standard-library route today.")
