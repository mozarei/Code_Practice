# Graph connection, clearing and freezing
This folder has exactly THREE deliberate sequential defects.
Focus: Detached losses, gradient-buffer lifetime and a trainable encoder.

Run from the pack root:
```bash
python ml_drills/03_autograd/run.py
python check_ml.py --set 03_autograd
```
The CSV/model/tokenizer and correct training harness are shared. Edit only
this folder's model.py, batching.py, objective.py, gradients.py, optim.py
and snapshots.py. No CSV-converter work is needed here.

Keep batch size 4, two epochs, CPU, max_length 64 and LR 1e-4.
Use right padding to the longest sequence in each batch, as supplied by the tokenizer.
The shared CSV has 9 rows -> 6 updates / 18 visits, including a final B=1
batch each epoch. Keep every record. Full fine-tuning must update both
the encoder and head. Preserve the supplied pretrained classifier forward.
Correct IDs/masks, [B,2] logits, long [B] class labels, finite tracked loss,
connected gradients, live optimizer coverage and independent snapshots
are part of the contract. No accuracy or loss-decrease target is required.

These are focused learning repositories. Their diagnostic checks are
supplied teaching aids; an actual interview may have fewer checks.
Use hints/ml/03_autograd/stage_N_level_1.md only when stuck. The separate
solutions tree is for review. Do not weaken common_ml.py to bypass errors.
Use --pdb to pause before the first model call; step until later values exist.
