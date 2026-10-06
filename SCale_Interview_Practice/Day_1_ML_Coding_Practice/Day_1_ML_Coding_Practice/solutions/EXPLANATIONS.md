# Review only after your attempt

## Converter
Read only the agreed files and fields. Exclusion uses `is True` before field validation.
Collecting and validating rows before opening output preserves an existing file on validation
errors. `csv.DictWriter`, UTF-8 and `newline=""` handle escaping and cross-platform newlines.
The fixtures are small; a memory-bounded streaming approach would need a staging/temp output
if preserving the previous output on validation failure were still required.

## Standard-library defects
1. `src/data.py` reads `row["target"]` but the agreed header is `text,label`. Read `label` and
   convert it to int. Do not change the converter's header to satisfy an accidental consumer bug.
2. `src/model.py` initializes n_features - 1 parameters. Initialize one weight for each feature.
   Do not suppress the dimension check or let zip silently drop a feature.
3. `src/train.py` adds the loss gradient. Gradient descent subtracts learning_rate * gradient.
   Check a short update and loss, then run the full training command. Preserve final checks.

## Optional PyTorch defects
1. The parser defines --csv, but the caller accesses args.training_csv. Use args.csv.
2. Class-index labels for this cross-entropy objective are floating-point tensors. Use torch.long.
3. Gradients are cleared between backward and step. Move zero_grad before the forward/backward
   operations, then confirm that parameters change and the fixture's training loss decreases.

## Variant
Reconfirm top-level shape, nested paths, field names and boolean semantics. `type(value) is bool`
rejects integer 0/1, which otherwise compare equal to False/True in Python. Map true -> 0 and
false -> 1 as requested; the interpretation differs from a generic int(bool) conversion.

## Practice answers to discussion questions
State the expected representation, the observed value and the responsible producer. A run with
no errors could still have unchanged weights, an incorrect mask, or misleading metrics. Loss
decrease on this tiny training fixture checks update mechanics, not generalization. For a
nonfinite loss, inspect the first failing batch, input values, predictions, objective and update
magnitude before changing many settings. A security-related keyword feature is a teaching
feature and cannot establish robust prompt-injection detection.
