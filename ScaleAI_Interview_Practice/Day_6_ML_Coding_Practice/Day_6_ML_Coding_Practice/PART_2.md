# Part 2 - Debug a CPU fine-tuning repository (40 minutes)

Run src/train.py. There are THREE intentional sequential project defects.
Read the error before looking at hints. Repair the source and rerun the same
command. Earlier-stage bugs can prevent later stages from being reached.

```bash
python src/train.py --csv output/train.csv
# Or, independently of Part 1:
python src/train.py --csv fixtures/reference_train.csv
# Optional breakpoint on the first batch:
python src/train.py --csv fixtures/reference_train.csv --debug
```

The model is a local pretrained BERT-tiny encoder with a two-class head.
This exercise explicitly requires FULL fine-tuning. The model wrapper exposes
raw logits; study how it calls the underlying BERT encoder and classifier.
No model-quality, accuracy or loss-decrease target is required.

Success contract:

- CPU; exact text,label CSV; all records visited; batch size 4; two epochs;
  max token length 64; learning rate 1e-4. Keep the partial final batch.
- 21 supplied records -> six batches per epoch, final batch size one;
  12 updates and 42 example visits. Handle B=1 and B=4 correctly.
- Integer token IDs; valid model input names; floating raw logits [B,2];
  long integer class targets [B]; scalar differentiable finite loss.
- Finite gradients; both tracked encoder and classifier weights change.
- Save reloadable model/tokenizer under output/run/checkpoint and metrics.json.
  Final line TRAINING_COMPLETE appears only when the checks succeed.

Files:

| File | Responsibility |
|---|---|
| src/data.py | CSV reader and Dataset |
| src/batching.py | Tokenization and collator output |
| src/model.py | nn.Module wrapper and model forward |
| src/objective.py | Classification loss |
| src/train.py | CLI, optimizer, training loop, verification and saving |

Inspect these boundaries: record -> collator -> model -> loss -> backward
-> optimizer -> actual changed weights. Some problems raise immediately;
others appear only for a particular batch or at the completion check.
DataLoader, parameter checks and optimizer configuration are part of the
contract: do not drop records, fabricate metrics, suppress errors, freeze the
encoder, change the training target, or edit outside libraries to bypass a failure.

After repairing the repo:

```bash
python tools/check_training.py --csv output/train.csv
```

This independently reruns your CURRENT code in a fresh temporary directory,
checks counts, compares persisted encoder/head weights, reloads the checkpoint,
and checks batching/loss at batch sizes 1 and 4. Existing output cannot pass it.

Think aloud: "I expected ____. The traceback shows ____. I will inspect ____.
My hypothesis is ____. I changed ____. This rerun verifies ____."
The bugs here are practice choices, not predictions of the exact interview code.
