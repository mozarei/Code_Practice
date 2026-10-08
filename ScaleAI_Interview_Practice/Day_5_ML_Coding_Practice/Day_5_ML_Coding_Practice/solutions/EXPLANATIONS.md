# Reference repairs: open after attempting

1. batching.py casts input_ids to float. A token ID is an embedding-table index, so preserve
   integer IDs (torch.long here). Continuous hidden states can be floating point; indices cannot.
   Minimal repair: use the tokenizer's IDs unchanged or preserve .long().
2. objective.py expands labels from [B] to [B,1]. With logits [B,2], integer class targets must be
   a vector [B]. Use labels directly. Removing every singleton dimension with squeeze() is unsafe
   at B=1; the fixture deliberately contains a one-example final batch.
3. train.py constructs AdamW from classifier parameters only. Encoder gradients exist, but the
   optimizer cannot update parameters it does not own. The full fine-tuning contract requires
   model.parameters(). This also makes optimizer.zero_grad clear all the optimized parameters.
   Classifier-only training can be a valid separate design; it is not this exercise's contract.

The model wrapper correctly returns raw logits and the loss is not detached before backward.
Do not repeat Day 3 repairs without evidence. data.py and model.py are correct in this pack.

Reference commands from project root:
```bash
python solutions/convert.py --input-dir fixtures/raw --output-csv output/reference.csv
python tools/check_converter.py --script solutions/convert.py
python solutions/train.py --csv output/reference.csv --output-dir output/reference_run
python tools/check_training.py --train-script solutions/train.py --csv output/reference.csv
```

The independent completion checker reruns current code in a fresh folder, compares persisted
encoder/head weights with the source checkpoint, reloads the saved model/tokenizer and tests
batch/loss contracts at B=1 and B=4. It does not use a previous successful output directory.

Concise explanations to practice:
"The IDs were converted to floating point. The embedding needs integer indices, so I preserved
the integer tensor from tokenization."
"The helper added an extra target dimension. I kept one integer label per example and checked
both full batches and the final single-example batch."
"The encoder had gradients but was excluded from the optimizer. I included all trainable model
parameters, then verified that the saved encoder and classifier weights changed."
