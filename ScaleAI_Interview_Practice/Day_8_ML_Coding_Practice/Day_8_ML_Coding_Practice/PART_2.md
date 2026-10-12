# Part 2 - Repair exactly three sequential CPU fine-tuning defects
Timed replay: 40 minutes. Learning pass: take the time you need.

```bash
python src/train.py --csv output/train.csv
# Independent fallback:
python src/train.py --csv fixtures/reference_train.csv
# Optional first-batch breakpoint:
python src/train.py --csv fixtures/reference_train.csv --debug
```

A teammate split fine-tuning into helpers. Navigate the source to repair
THREE deliberate defects. Each earlier repair reveals the next failure.
The repo uses a local pretrained BERT-tiny encoder plus a two-class head.

## Success contract
- Exact text,label CSV; every supplied row is used on CPU.
- Preserve batch size 4, two epochs, max_length 64, LR 1e-4 and drop_last=False.
  With 29 rows: 8 batches per epoch, including a last batch of one;
  16 updates and 58 example visits. Other positive row counts should also work.
- Tokenize mixed lengths into valid batches. Use integer IDs, matching masks
  and long vector labels [B]. Raw model logits must be floating [B,2].
- Preserve the supplied pretrained sequence-classification architecture:
  use its sequence-level pooled representation, existing dropout and classifier.
  Do not replace it with a different pooling strategy, token classifier or head.
  Wrapper outputs in eval mode must match the underlying classifier's forward.
- Full fine-tuning: intended trainable model parameters are connected to loss
  and the optimizer updates the LIVE model. Finite scalar losses/gradients;
  tracked encoder and classifier weights actually change.
- Save metrics.json and reloadable model/tokenizer under output/run/checkpoint;
  the reloaded forward matches the saved classifier. No accuracy/loss-decrease target.

## Navigate
| File | Responsibility |
|---|---|
| train.py | Entry point, training loop, completion checks and persistence |
| data.py | CSV validation and Dataset |
| batching.py | Tokenization and collation |
| model.py | Encoder representation and classification forward |
| objective.py | Cross-entropy interface |
| optim.py | Construction of the optimizer |

For each error: read the complete traceback; locate the project call; inspect
types/shapes/state; state a hypothesis; make one small repair; rerun.
Inspect values immediately before and after the failing boundary. Distinguish
tensors with identical values from the same underlying parameter object.
A loss log does not by itself prove that training updated the live model.

Do not fix outside libraries, drop difficult rows/final batches, change settings,
freeze the encoder, redesign the architecture, suppress errors or weaken checks.
These constraints define the exercise; model quality is outside its scope.

```bash
python tools/check_training.py --csv output/train.csv
```
Use the same fallback CSV if applicable. The checker uses a FRESH run of current
code, independently compares persisted weights, tests mixed lengths and B=1/4,
checks optimizer object membership, and compares wrapper/reload forwards.
A stale successful output folder cannot make broken code pass.
