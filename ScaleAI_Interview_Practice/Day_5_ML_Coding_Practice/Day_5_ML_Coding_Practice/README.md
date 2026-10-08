# Day 5: conversation data prep and CPU fine-tuning debugging

Planned practice: October 8, 2026. First interview: October 26.
You completed the previous converter and investigated batching/training failures. Day 5 keeps
the two-part interview format and introduces a different schema plus three different defects.
The checkpoint and dependencies are the same as Day 3; the dataset and project errors are new.

## Start in VS Code
Extract the ZIP and open Day_5_ML_Coding_Practice. Keep an untouched copy for replay.
Reuse your working Day 3 Python environment via Python: Select Interpreter, or create one:
```bash
python3 -m venv .venv
source .venv/bin/activate
# Linux only: install a CPU wheel first rather than CUDA dependencies.
# python -m pip install torch==2.7.1 --index-url https://download.pytorch.org/whl/cpu
python -m pip install -r requirements.txt
python tools/check_environment.py
```
Use Python 3.10-3.12, preferably 3.12. Intel Mac requirements select PyTorch 2.2.2/NumPy 1.26.4;
Apple Silicon/Linux/Windows use PyTorch 2.7.1. Transformers is pinned to 4.57.1. Windows
PowerShell activation: .venv\Scripts\Activate.ps1. All model/tokenizer files are included;
there are no downloads during training and no API keys or HF login. Setup is outside the timer.
VS Code F5 configurations require the Python Debugger extension; terminal breakpoint() works too.

## Three-hour practice session
| Minutes | Work | Evidence |
|---|---|---|
| 0-10 | Read contracts; confirm columns/mapping aloud | Write assumptions, then start |
| 10-30 | Part 1 timed conversion | Usable CSV and base check |
| 30-70 | Part 2 timed debugging | Tracebacks, observations, minimal repairs |
| 70-100 | Review conversion and scenario checks | Correct the cases you missed |
| 100-150 | Finish debugging; research specific gaps | Current-code completion check |
| 150-170 | Explain repairs; English practice | Cause, repair, verification in your words |
| 170-180 | Record progress and next target | Time, hints, weak skill |

During the first 60-minute simulation, use documentation but disable AI tools/completion.
At the conversion boundary, switch to the fallback CSV if needed so debugging gets its 40 minutes.
After stopping the timer, use open-book coaching and staged hints. Take a second learning session
if needed. Measure independent reasoning and improving time rather than expecting instant speed.
The separate nightly LeetCode hour is outside these 180 minutes.

## Run order
Read PART_1.md and PART_2.md. Keep hints/ and solutions/ closed initially.
```bash
python convert.py --input-dir fixtures/raw --output-csv output/train.csv
python tools/check_converter.py --only base
python src/train.py --csv output/train.csv
```
Fallback: `python src/train.py --csv fixtures/reference_train.csv`.
After the attempt, run all converter checks and `python tools/check_training.py --csv output/train.csv`
(or that same fallback CSV). The training check makes a fresh temporary run, then verifies
tensor contracts, all batches, changed persisted weights and checkpoint reload.

The converter starter is intentionally unfinished; the trainer is intentionally broken.
Learn from observed errors before opening answers. The exercises target the supplied first-screen
skills; the real input schema, model and defects are not disclosed.

## Learning and review
LEARNING_RESOURCES.md: official documentation and read/watch links with focused questions.
REVIEW_LOG.md: evidence, time and spoken explanations. NEW_SESSION_PROMPT.txt: another-session
coaching prompt that requests one hint at a time and English corrections. Attach relevant files;
another session cannot be assumed to see this project. After learning, reattempt from a fresh ZIP.
See VERIFICATION.md for actual runtime checks and platform limitations.
