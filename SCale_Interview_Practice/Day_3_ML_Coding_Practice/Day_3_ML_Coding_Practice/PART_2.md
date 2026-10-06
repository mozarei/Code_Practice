# Question 2: repair a CPU Hugging Face fine-tuning repository

This question uses a real pretrained BERT-tiny encoder with a newly initialized two-class
classification head. The checkpoint and tokenizer are included locally. Fine-tuning updates
the pretrained encoder and classifier. The synthetic request labels are for engineering
practice; they are not a validated urgency classifier or a security product.

Your teammate's training command fails. Navigate the unfamiliar `src/` repository and repair
exactly three deliberate sequential defects until training and the completion check succeed.
Learning pass: take the time you need. Fresh replay: 40 minutes.

```bash
python src/train.py --csv output/train.csv
```
If your converter is unfinished, use the independent known-good dataset:
```bash
python src/train.py --csv fixtures/reference_train.csv
```

## Success contract
- Read all 24 supplied CSV records with the agreed `text,label` schema.
- Tokenize and batch them on CPU; keep the supplied batch size, length limit, epochs and LR.
- Complete two epochs: 12 optimizer updates, 48 examples visited.
- Losses and gradients are finite; tracked encoder and classifier parameters change.
- Save a reloadable local model/tokenizer checkpoint and `metrics.json` under `output/run`.
- Preserve the program's checks. Do not bypass training, fabricate metrics, suppress errors,
  change external library code, or make the run depend on downloading models.
- No accuracy threshold or loss-reduction target. Model quality, EDA, tuning and evaluation
  datasets are outside this debugging question.

```bash
python tools/check_training.py --csv output/train.csv
# If you used the supplied fallback CSV, check that same CSV instead:
python tools/check_training.py --csv fixtures/reference_train.csv
```

## Repository navigation
`src/train.py` is the entry point. `src/data.py`, `src/collation.py`, and `src/model.py` are
project-owned components. Locate their callers and state each component's responsibility.
Everything in `src/` may be inspected or repaired. The environment smoke test runs independently
of these modules; a setup failure is not one of the three interview-style defects.

For each failure, write: exact command -> full traceback -> last relevant project frame ->
observed value/type/shape -> hypothesis -> smallest repair -> rerun evidence.
If you are stuck locating a definition for more than a few minutes, say what you are looking for.

## Inspection practice after your first run
Use `breakpoint()` near the failure; inspect types, shapes and relevant attributes before
changing code. `p variable`, `p type(variable)`, `where`, `n`, `s`, and `c` are useful debugger
commands. Search all files with Cmd/Ctrl+Shift+F; use Go to Definition where available.

Record your own observations for these checkpoints:
- One CSV record and its label's Python type.
- The value given to the tokenizer and the tokenizer's returned keys.
- One batch: shape, dtype and device of every tensor; explain padding/truncation.
- What the model returns and what the loss function receives.
- How a training loss is connected to trainable parameters.
- What `train()`, `eval()`, `zero_grad()`, `backward()` and `step()` each do.

## Hints and solutions
Try the traceback and official docs first. If stuck, open only the hint file for your current
failure (`hints/1.md`, then `2.md`, then `3.md`). They contain staged hints. After attempting,
`solutions/EXPLANATIONS.md` explains all three repairs and gives reference commands.
Do not run solution files during the simulation; later replay from a fresh extracted ZIP.
