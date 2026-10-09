# Day 6 - Understand the training state, then debug it

Prepared for Mohammad Zarei. First technical interview: October 26, 2026.
You finished Day 5 on schedule. This set focuses on your biggest current gap:
gradients can exist while weights do not update. It includes eleven small
interactive labs, eleven checked coding exercises, a fresh two-part mock,
and six short debugging drills. The exact interview bugs are unknown.

## Start here

Open this extracted folder in VS Code. Reuse your working Day 3/5 interpreter.
Activate that environment and run these commands FROM THIS FOLDER:

```bash
python tools/check_environment.py
python run_labs.py --lesson 1
```

The runner explains ONE topic, asks you to predict, runs the experiment, then
points you to exercises/task_XX.py. Edit that file in VS Code while the runner
waits. Enter c to check it, r to rerun the experiment, or q to stop.
A failed check does not advance to the next lesson. After a pass, YOU choose
whether to continue. Prediction text is recorded in output/learning_log.jsonl;
it is not automatically graded. Discuss it with your coach using the prompt.

You can stop and resume any topic:

```bash
python run_labs.py --lesson 4
python run_labs.py --lesson 5 --demo
python run_labs.py --lesson 5 --check
python run_labs.py --lesson 10 --demo --pdb
```

--demo skips the question prompts for that ONE lesson. --all-demos is an
explicit batch mode for later review, not the recommended first learning path.
Lesson source lives in labs/lesson_XX.py: read the code while comparing its
printed results. Small dense models isolate the mechanics; lesson 9 uses
the real local BERT tokenizer. The mock uses a real pretrained BERT-tiny encoder.

## Suggested three-hour core session

| Minutes | Work |
|---|---|
| 0-5 | Environment check; open the model and exercise files |
| 5-50 | Labs 1-4: structure, parameters, forward and backward |
| 50-105 | Labs 5-7: optimizer ownership, clearing and freezing |
| 105-125 | Part 1: new converter, 20-minute attempt |
| 125-165 | Part 2: new debugging mock, 40-minute attempt |
| 165-180 | Record evidence and explain one fix without notes |

These are approximate learning allocations. If the fundamental exercises
need longer, finish them and take the mock in a second session. Do not rush
eleven new concepts to satisfy the clock. Labs 8-11 and the short drills are
the follow-up block: shapes, BERT inputs, pdb and the full loop. You can use
them immediately when a mock error reveals a gap. Keep setup outside mock timing.

## The interview-style mock

Read PART_1.md and PART_2.md before starting. During the mock, ordinary docs
are allowed; turn off AI chat and completion. Keep hints/ and solutions/ closed.

```bash
python convert.py --input-dir fixtures/raw --output-csv output/train.csv
python tools/check_converter.py --only base
python src/train.py --csv output/train.csv
```

If the CSV is unfinished at 20 minutes, preserve debugging time:

```bash
python src/train.py --csv fixtures/reference_train.csv
```

After your attempt, run the full checks:

```bash
python tools/check_converter.py
python tools/check_training.py --csv output/train.csv
```

Use fixtures/reference_train.csv in the second command if that was the file
you trained on. The training check reruns CURRENT code in a fresh temporary
folder; old output/run files cannot make broken code pass.

## Six independent short drills

```bash
python debugging/case_01.py
python tools/check_debugging.py --file debugging/case_01.py
```

Repeat for 02-06, one case at a time. Each has ONE intentional defect. The
common runner is correct and enforces full fine-tuning; do not edit its checks.
debugging/TRACEBACKS.md contains captured starter failures if you want to read
an error first. Debugging hints are separate from mock hints.

## Setup if you need a new environment

Python 3.10-3.12, preferably 3.12. Existing working interpreter is easiest.
On macOS/Linux, replace python3 with python3.12 if needed:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python tools/check_environment.py
```

Windows PowerShell: py -3.12 -m venv .venv, then
.\.venv\Scripts\Activate.ps1, then the same pip/check commands.
The pins select torch 2.2.2 and NumPy 1.26.4 on Intel macOS; other platforms
use torch 2.7.1. Linux can install the smaller CPU wheel first:

```bash
python -m pip install torch==2.7.1 --index-url https://download.pytorch.org/whl/cpu
python -m pip install -r requirements.txt
```

Installation needs internet; exercises and model loading run offline on CPU.
No Hugging Face account, GPU, API key or runtime model download is required.
These packages are already installed in the actual interview environment.

## Answers and review

solutions/ contains reference exercise code, the converter, repaired mock,
and repaired short drills. solutions/EXPLANATIONS.md explains root causes.
Do not open it before trying. Labs/EXPECTED_OBSERVATIONS.md summarizes the
experiments after you have made your predictions. Full reading links are
in LEARNING_RESOURCES.md. NEW_SESSION_PROMPT.txt supports one-hint coaching
and English corrections. REVIEW_LOG.md helps track your reasoning.
VERIFICATION.md lists what was executed and platform limitations.
