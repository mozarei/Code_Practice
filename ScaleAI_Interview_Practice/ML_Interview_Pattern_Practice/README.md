# Interview Pattern Practice Pack
Prepared after your completion of Day 8. First technical interview: October 26, 2026.

This is a reusable practice library, not another single full-day mock. It targets
the confirmed first-screen skills: Python data preparation plus debugging a small
CPU fine-tuning repository. Exact real-interview schemas and bugs remain unknown.

## What is included
- printable/Python_Commands_One_Page.pdf: one-page CLI, file, CSV and pdb reference.
- printable/BERT_Shapes_and_Pattern_Guide.pdf: actual BERT shapes, training state,
  quick debugging commands, pattern recognition, and how to find unfamiliar APIs.
- python_drills/: SIX folders, THREE focused problems each (18 total).
  Inputs are already Python objects; no repeated JSON reading or CSV writing.
- ml_drills/: FIVE independent folders, THREE sequential defects each (15 total).
  They share a local pretrained BERT-tiny checkpoint, CSV and correct harness.
- shape_lab.py: correct, readable real-BERT example that prints intermediate
  shapes, parameter shapes, gradients, singleton batches and storage identity.
- templates/: copyable converter skeleton, tiny pattern examples and debugger notes.
- hints/, solutions/: separate hints and reference implementations.
- LOOKUP_PLAYBOOK.md: what to search and what small experiment to run when stuck.
- NEW_SESSION_PROMPT.txt: one-problem coaching and English feedback.

## Start with the reference, then one short problem
Open the extracted folder in VS Code. Reuse your working Day 8 interpreter.
Python drills and templates use ONLY the standard library; they need no ML packages.

```bash
python templates/pattern_examples.py
python python_drills/01_selection/check.py --question 1
```

Read that folder's README.md and edit its starter.py. The first run intentionally
fails until you implement the function. Each folder has Q1, Q2 and Q3, independently
selectable. For a predict/observe REFERENCE demo (reveals expected outputs after you
predict), add --demo --question 1. Answer code remains in solutions/python/.

```bash
python python_drills/02_sets_and_joins/check.py --question 2
python check_python.py --folder 02_sets_and_joins
python check_python.py --all
```

Optional runnable boilerplate example (its documented simple schema):
```bash
python templates/convert_template.py --input-dir examples/template_raw --output-csv output/template.csv
```

## Python folders
| Folder | Three focused problems |
|---|---|
| 01_selection | Last final by list order; latest by timestamp/tie; first non-None |
| 02_sets_and_joins | Stable unique IDs; latest-label join; unknown reference IDs |
| 03_strings | Replace a span; literal first replacement; precise paragraph assembly |
| 04_validation | Exact-True skip; strict integer label; missing/null/empty/value |
| 05_sorting_grouping | Numeric filename order; stable priority order; group text |
| 06_scans_and_scope | Flatten paragraphs; keep a partial batch; reset joins per export |

## ML folders
Choose ONE folder, read its README, then run it. Every starter has exactly three
deliberate sequential defects. Later failures appear only after earlier repairs.
All folders use the same nine synthetic CSV records, 2 epochs, batch size 4,
max_length 64 and LR 1e-4. Finish 6 updates / 18 visits, keeping final B=1 batches.

```bash
python ml_drills/01_batch_inputs/run.py
python check_ml.py --set 01_batch_inputs
```

| Folder | Learning area |
|---|---|
| 01_batch_inputs | Tokenizer input, integer IDs, padding masks |
| 02_outputs_targets | Model outputs, class-index labels, B=1 shapes |
| 03_autograd | Graph connection, clearing, encoder trainability |
| 04_optimizer | Parameter identity, full coverage, group settings |
| 05_representations | Sequence features and independent weight snapshots |

The common harness provides explicit diagnostic checks as teaching aids. Keep
common_ml.py unchanged; repair the six source helpers INSIDE the selected folder.
A real interview may supply fewer checks. This pack trains the reasoning, not
recognition of a known error string. Full fine-tuning and the original classifier
architecture are required; quality/tuning/EDA/GPU work are outside scope.

The checker runs current code into a fresh temporary folder, compares independently
reloaded weights, tests B=1/4 and verifies snapshot storage. Old output cannot pass it.
--pdb pauses before the first model call. If collation fails earlier, put a breakpoint
inside that folder's batching.py instead. STARTER_TRACEBACK.txt shows only its original
first failure; later failures are not disclosed there.

## Shape and state laboratory
```bash
python shape_lab.py
python shape_lab.py --pdb
```
It uses actual pretrained BERT-tiny weights, not simulated tensor shapes. B, L, H
and C are named in the guide; values vary across models/batches. Memorize the
relationships rather than assuming every BERT has hidden size 128. Example output
is in examples/. The label interface here is integer class indices for cross-entropy;
probability targets are a separate supported interface, not used by these tasks.

## A practical three-hour block
45 min: one Python folder's three problems. 75 min: one ML folder. 20 min: shape
lab or a concept experiment. 25 min: review and explain. 15 min: replay one repair
without notes. These are learning allocations, not promises. Rotate through the
folders over several sessions; you do not need to finish all 33 tasks in one day.
Reserve a later fresh 20/40-minute whole-repo mock to practice interview pacing.

## Setup only if your working Day 8 environment is unavailable
Python 3.10-3.12, preferably 3.12. macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```
Windows PowerShell: py -3.12 -m venv .venv, then .\.venv\Scripts\Activate.ps1.
On Linux you may preinstall the CPU wheel before requirements:
```bash
python -m pip install torch==2.7.1 --index-url https://download.pytorch.org/whl/cpu
python -m pip install -r requirements.txt
```
Intel macOS dependency pins are inherited from earlier packs; actual tests here
use Linux torch 2.7.1+cpu. See VERIFICATION.md for precise executed checks.
Installation needs internet. All model/tokenizer loading uses bundled local files;
no GPU, HF account, model download or API key is needed for the exercises.

## Review mode
Use ordinary documentation/search during solo practice and disable AI assistance
for a realistic mock. Use NEW_SESSION_PROMPT.txt in your teaching session afterward.
For explicit reference checks, add --solution to check_python.py/check_ml.py.
Do not open solutions until you want answers. Personal printouts are prep aids;
follow the interviewer's tool rules during the actual assessment.
