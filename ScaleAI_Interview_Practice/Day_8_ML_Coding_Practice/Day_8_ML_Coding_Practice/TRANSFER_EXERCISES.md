# After repair - optional transfer exercises
These are not extra bugs and are outside the 60-minute mock. Pick ONE.

1. Re-run the checker using CSV subsets of 1, 5 and 8 records. Predict number
   of batches, total updates and total visits BEFORE executing. Keep batch size
   and epochs unchanged. Read records with csv, not text-line slicing.
2. Explain why a dictionary join is usually preferable to rescanning every
   review for every document. State the cost including input text and sorting.
3. Print the shapes of input_ids, attention_mask, last_hidden_state,
   pooler_output, logits and labels for B=1 and B=4. Explain every axis.
4. Construct a toy nn.Linear model and deepcopy it. Before training, compare
   equal weights and parameter object IDs. Backward through the original;
   inspect both models' gradients. Predict which optimizer step can change it.
5. In an untouched copy of the repaired repo, replace the single optimizer
   group with separate encoder and classifier groups, both at the same LR.
   Verify every live parameter appears exactly once. Avoid tuning their rates.

Evidence tool:
```bash
python tools/inspect_training_state.py
```
Explain why each observation follows from code; do not merely memorize its output.
