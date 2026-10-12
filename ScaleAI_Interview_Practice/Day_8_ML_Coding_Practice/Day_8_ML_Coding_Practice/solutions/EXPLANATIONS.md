# Answers - open after the attempt
## Converter
Validate documents and collect them in original order. Use a per-file ID set
and a map from known ID to its latest final label. Each later final overwrites
that map entry; drafts do not. Walk ordered documents to emit selected rows.
Reinitialize maps per file. With dictionary lookup, expected work is O(D+R)
per file, excluding text size and filename sorting; repeated nested scans can
approach O(D*R). All validation occurs before output is opened.

## Bug 1 - Unequal token lengths cannot directly form a rectangular batch
batching.py uses padding=False together with return_tensors='pt'. Mixed
lengths produce nested lists of unequal sizes; truncation alone does not
make them equal. Set padding=True (or an equivalent valid padding strategy).
Keep attention masks aligned. A homogeneous-length batch can hide this bug;
test both a short sentence and a longer one. Do not delete long examples.

## Bug 2 - The reduction removes the feature axis
last_hidden_state is [B,L,H]. mean(dim=-1) produces [B,L], whereas the
existing classifier expects [B,H]. That creates a matrix multiplication
mismatch. For THIS supplied pretrained architecture, use encoded.pooler_output,
which is [B,H], then its existing dropout and classifier. Changing only the
reduction to mean(dim=1) makes the shape plausible but changes the intended
architecture and leaves its pooler outside the loss path; it is not the
specified repair. Do not confuse pooler_output with raw first-token state.

## Bug 3 - Optimizer owns a copied model's parameters
optim.py deep-copies the supplied model before selecting parameters. The
live model calculates loss and receives gradients. Its clone has separate
parameter objects with equal initial values, but receives no gradients from
that forward. AdamW steps the clone's parameters, leaving live weights unchanged.
Use the supplied live model directly. Names, counts, shapes and initial values
can all match while object identity differs. Compare sets of id(parameter).
The live gradients can also accumulate because optimizer.zero_grad is clearing
the clone rather than the model that ran backward.

## Why the checks are meaningful
Step counts and finite losses are necessary but insufficient. Independent
persisted-weight comparison shows actual changes. Optimizer ID checks test
ownership; B=1/4 and mixed lengths test boundaries; wrapper and checkpoint
comparisons verify the intended forward path survived the repairs.

## Reference commands
```bash
python solutions/convert.py --input-dir fixtures/raw --output-csv output/reference.csv
python tools/check_converter.py --script solutions/convert.py
python solutions/train.py --csv output/reference.csv --output-dir output/reference_run
python tools/check_training.py --train-script solutions/train.py --csv output/reference.csv
```

## Say it in English
"Truncation caps sequence length, but padding makes the batch rectangular."
"The reduction removed the feature dimension that the classifier needs."
"These tensors have equal values, but they are different parameter objects."
"The live model received gradients, but the optimizer managed another model."
"I verified both weight changes and the reloaded model's behavior."
