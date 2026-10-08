import sys
from pathlib import Path

print("Interpreter:", sys.executable)
try:
    import torch
    import transformers
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
except ImportError as exc:
    raise SystemExit("SETUP REQUIRED: activate your environment and install requirements.txt. " + str(exc))
print("Versions:", torch.__version__, transformers.__version__)
path = Path(__file__).resolve().parents[1] / "models/bert-tiny"
torch.set_num_threads(2)
tokenizer = AutoTokenizer.from_pretrained(path, local_files_only=True)
model = AutoModelForSequenceClassification.from_pretrained(path, local_files_only=True).to("cpu").eval()
encoded = tokenizer(["Setup smoke test."], return_tensors="pt", truncation=True, max_length=64)
with torch.no_grad():
    outputs = model(**encoded)
assert outputs.logits.shape == (1,2)
assert torch.isfinite(outputs.logits).all()
print("SETUP_OK: offline tokenizer/model forward on CPU. Exercise code was not run.")
