# Question 2: repair the training codebase

Timed budget: 40 minutes. Choose ONE route for the timed attempt.
There are exactly three deliberate defects in each route, revealed sequentially.
No bug identities are disclosed here. Work inside the project and preserve the success checks.

## Route S: default Day 1 exercise

This is a real, small logistic-regression training loop implemented with Python's standard
library. It reads the CSV, extracts three numerical features, predicts a probability, computes
binary cross-entropy and a gradient, and updates weights. It is a baseline debugging exercise;
it does not use a pretrained transformer or fine-tune a Hugging Face model.

```bash
python src/train.py --csv output/train.csv
```

Read `src/train.py`, `src/data.py`, and `src/model.py`. Follow the traceback to the responsible
project line. Inspect values and contracts before changing code. Make one small change, rerun
the same command, and record the evidence. New errors may indicate progress.

## Route T: optional PyTorch exercise

Use this instead of Route S only if PyTorch is already available in the selected interpreter.
The CPU toy model has an embedding layer, masked mean pooling and a classifier. It is randomly
initialized, not a pretrained transformer. Inspect `torch_src/`.

```bash
python torch_src/train.py --csv output/train.csv
```

No downloads are needed for either route. The reference PyTorch route was reviewed and syntax-
checked here, but not executed because PyTorch was unavailable. Choose Route S to start today
without dependency setup. Installing packages is not part of the actual interview.

## Success criteria

- Loads all 12 fixture rows under the agreed CSV contract.
- A complete training run finishes with finite loss below its initial TRAINING loss.
- Parameters actually change. Keep the checks that verify this.
- You can explain each root cause, the inspected evidence, the repair and its limitations.
- Printed training loss/accuracy is not a held-out evaluation or evidence of model quality.

After repairing the route, run its completion checker:

```bash
python tools/check_training.py --route stdlib --csv output/train.csv
# If you selected PyTorch:
python tools/check_training.py --route torch --csv output/train.csv
```

If Part 1 is unfinished, replace `output/train.csv` with `fixtures/reference_train.csv`.
Checks against arbitrary alternate datasets may need different row-count expectations.

## Discussion questions after your attempt
1. What does each feature or tensor dimension mean?
2. Where did the violated contract first originate?
3. Why is your change a root-cause repair?
4. What observation distinguishes your hypothesis from another explanation?
5. Why is finishing without an exception insufficient evidence of training?
6. Which metrics are training metrics, and what can you infer from them?
7. What would you investigate next if the loss became nonfinite?

Use `breakpoint()` or VS Code's debugger. Search files with Cmd/Ctrl+Shift+F.
Hints and answers are separate. Open `hints/` only when requesting help and `solutions/` after
the attempt or when explicitly choosing review mode in your coaching session.
