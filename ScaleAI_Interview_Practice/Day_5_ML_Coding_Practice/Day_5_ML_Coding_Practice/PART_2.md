# Part 2: repair a CPU fine-tuning repository

Target: 40 minutes. The repo loads a local pretrained BERT-tiny encoder and a two-class
classification head. Fix exactly three deliberate sequential defects in project code until
the training command and independent completion check pass. These defects differ from Day 3.

```bash
python src/train.py --csv output/train.csv
# If conversion is unfinished:
python src/train.py --csv fixtures/reference_train.csv
```

## Required behavior
- Read the agreed text,label CSV and use CPU only.
- Keep batch size 4, two epochs, max_length 64 and LR 1e-4. Do not drop the final partial batch.
- Supplied fixture: 25 rows, 7 batches per epoch, final batch size 1; 14 updates and 50 total
  visited examples. Your repair must work at batch sizes 1 and 4.
- Model inputs must satisfy the tokenizer/model contract; integer labels are class indices.
  This is ordinary two-class classification with raw scores of shape [batch,2] and class-index
  labels of shape [batch]. Preserve the appropriate tensor dtypes.
- This exercise requests FULL fine-tuning: both encoder and classifier weights must update.
  Do not freeze layers or alter checks to turn it into classifier-only training.
- Loss and gradients are finite; save metrics.json plus model/tokenizer under output/run.
  The checkpoint must reload locally and produce finite two-class scores.
- Repair project source. Do not suppress errors, fabricate metrics, edit libraries or checks,
  replace the model, download another checkpoint, or change labels/hyperparameters to bypass bugs.
- No accuracy target, loss-decrease threshold, EDA, tuning or quality evaluation is required.

## Navigate the call chain
Entry: src/train.py. Project components: data.py, batching.py, model.py, objective.py.
Read callers as well as the line named in the exception. Record what crosses each boundary.
Use Cmd/Ctrl+Shift+F and Go to Definition; pause with breakpoint() before changing code.
If the last relevant project line calls a helper, step into it and inspect its local variables.

For each failure: full traceback -> project frame -> observed type/shape/value -> hypothesis ->
smallest repair -> rerun evidence. A log showing loss values is not by itself completion.
Keep the completion checks intact and diagnose a later contract failure as carefully as an exception.

## Verify current code after repairs
```bash
python tools/check_training.py --csv output/train.csv
# Or use the same fallback CSV you trained with:
python tools/check_training.py --csv fixtures/reference_train.csv
```
This checker runs your current code again in a fresh temporary output folder, compares saved
encoder/head weights against the starting checkpoint, reloads the trained artifact and exercises
batch/loss contracts at sizes 1 and 4. It does not rely on an old successful output/run folder.
Temporary checker artifacts are removed; your regular training output remains available.

Optional support after an attempt: hints/1.md, then 2.md, then 3.md for the current failure only.
Full repairs and explanations are in solutions/EXPLANATIONS.md; keep them closed during the timer.
