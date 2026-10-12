# Day 8 - Harder data preparation and training-state debugging

You completed Day 6. This set is a step up in reasoning and unfamiliar-code
navigation while preserving the confirmed first-screen format: roughly
20 minutes for a Python JSON-to-CSV CLI and 40 minutes for three sequential
bugs in a small CPU fine-tuning repository. Exact interview bugs are unknown.
No new installation or GPU work is part of the timed attempt.

## Start
Open this extracted folder in VS Code. Reuse your working Day 6 interpreter.
Read PART_1.md and PART_2.md, then run the independent setup check:

```bash
python tools/check_environment.py
```

Keep hints/ and solutions/ closed. Preserve an untouched copy for replay.
Ordinary docs/search are allowed in the mock; disable AI chat and completion.
Your teaching session is for review after the independent attempt.

## Three-hour session
| Minutes | Activity |
|---|---|
| 0-10 | Setup; restate contracts and ask clarifying questions aloud |
| 10-30 | Part 1 timed attempt; produce a usable CSV |
| 30-70 | Part 2 timed debugging attempt |
| 70-105 | Finish converter; run edge cases; discuss join complexity |
| 105-155 | Finish debugging; inspect boundaries; verify actual training |
| 155-175 | Explain root causes and do one transfer exercise |
| 175-180 | Record time, hints and next target |

This is a harder learning exercise. If it takes another session, finish the
reasoning before doing a fresh 20/40-minute replay. Full error-case coverage
is for review after the timed attempt; a working CSV is the first priority.

## Commands
```bash
python convert.py --input-dir fixtures/raw --output-csv output/train.csv
python tools/check_converter.py --only base
python src/train.py --csv output/train.csv
```

If conversion is unfinished at 20 minutes, protect the debugging block:
```bash
python src/train.py --csv fixtures/reference_train.csv
```

After repairing both parts:
```bash
python tools/check_converter.py
python tools/check_training.py --csv output/train.csv
```

Check the same reference CSV instead if you used the fallback. The training
checker runs CURRENT code in a fresh temporary directory, checks counts,
compares persisted encoder/head weights, and verifies model/optimizer contracts.
Old successful artifacts cannot pass broken current code.

Optional evidence tool AFTER your initial attempt:
```bash
python tools/inspect_training_state.py
python tools/inspect_training_state.py --pdb
```

It runs current source and prints tracked gradient norms, optimizer membership
and weight deltas. It will fail at any earlier unresolved bug. It does not repair code.

## Why this is harder
- Part 1 joins two lists by ID, resolves repeated final reviews, and preserves
  document order across files. It is more than directly copying fields.
- Part 2 spans batching, model representations and optimization helpers.
  You must distinguish types/shapes, graph connection, parameter identity,
  stored gradients and actual changes. Loss logs alone are insufficient.
- Mixed text lengths, long text, Unicode, reused IDs across exports and a
  final batch of one test whether fixes generalize.

## Setup if needed
Prefer your existing interpreter. Python 3.10-3.12, recommended 3.12.
macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python tools/check_environment.py
```
Windows PowerShell: py -3.12 -m venv .venv, then
.\.venv\Scripts\Activate.ps1, then the same pip/check commands.
Intel macOS pins torch 2.2.2 and NumPy 1.26.4; other platforms pin torch 2.7.1.
Linux may install the smaller CPU wheel first:
```bash
python -m pip install torch==2.7.1 --index-url https://download.pytorch.org/whl/cpu
python -m pip install -r requirements.txt
```
Package installation needs internet. Local model/tokenizer files are included;
exercises load offline on CPU without an account, API key or model download.
models/bert-tiny/PROVENANCE.json records the pretrained encoder source and
newly initialized two-class head. The dataset is synthetic engineering practice.

## Review material
REVIEW_LOG.md: evidence and English explanations.
TRANSFER_EXERCISES.md: optional post-repair variations.
LEARNING_RESOURCES.md: official reading/watch links.
NEW_SESSION_PROMPT.txt: one-hint coaching; wait for your reasoning.
hints/: Part 1 and each debugging stage, with three levels per stage.
solutions/: complete converter and repaired repository; explanations separate.
VERIFICATION.md: executed checks and actual platform limitations.
