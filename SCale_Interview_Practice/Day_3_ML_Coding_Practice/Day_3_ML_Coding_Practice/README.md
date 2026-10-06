# Day 3: data preparation and real CPU fine-tuning debugging

Prepared for Mohammad Zarei. Practice day 3 is a sequence label, not a deadline.
Your baseline: Day 1 conversion took about 3 hours; you spent about 1.5 hours on the first
portion of Question 2. This pack keeps conversion familiar and develops ML debugging.
Complete it over two days if needed; measure progress against your own previous attempt.

These original exercises match the supplied first-screen skills and 20/40-minute structure.
The actual JSON schema, training objective, model and defects are unknown. This is practice,
not a reconstruction of undisclosed interview questions.

## Setup in VS Code - outside your practice timer
Extract the ZIP and open `Day_3_ML_Coding_Practice` with File > Open Folder. Keep an untouched
copy for replay. Use Python 3.10-3.12; Python 3.12 is recommended and was used for verification.
The package versions are pinned; later Python versions are outside this setup.

macOS / Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
# Linux only: install the CPU wheel first to avoid downloading CUDA libraries.
# python -m pip install torch==2.7.1 --index-url https://download.pytorch.org/whl/cpu
python -m pip install -r requirements.txt
python tools/check_environment.py
```
Windows PowerShell: use `py -3.12 -m venv .venv`, then `.venv\Scripts\Activate.ps1`, followed
by the same `python -m pip ...` and environment check. Package installation needs internet;
the exercises then load the included model/tokenizer offline. Requirements automatically
select PyTorch 2.2.2 and NumPy 1.26.4 for an Intel Mac, because PyTorch 2.2.x was the last
official macOS x86 release (https://pytorch.org/blog/pytorch2-2/). Apple Silicon,
Linux and Windows use PyTorch 2.7.1. The included checkpoint uses safetensors on both routes.
No HF login, GPU, API key,
model download or datasets package is needed. Use VS Code's Python: Select Interpreter to
select `.venv`. F5 configurations require the Python Debugger extension; terminal debugging
does not. The Mac/Windows installation paths were not runtime-tested by the author.

A missing-package/setup error is not an interview bug. Resolve it before starting. In the
real interview, everything is installed. Disable AI completion and assistants during solo
attempts; ordinary docs/search are allowed. Use your coaching session after the attempt
or in the open-book learning pass.

## First three-hour learning session
| Minutes | Work | Evidence |
|---|---|---|
| 0-15 | Read contracts; clarify columns and label mapping aloud | Write input/output assumptions |
| 15-75 | Implement the converter from a blank starter | Valid CSV and base check |
| 75-95 | Inspect the CSV; run scenario checks | Record rows/columns and failing cases |
| 95-165 | Run training; investigate the next failure | Traceback, observation, hypothesis, repair |
| 165-180 | Explain your work and fill REVIEW_LOG.md | One English correction and next target |

Stop at 3 hours; write down the next command and resume there. If the converter runs over
its learning budget, switch to `fixtures/reference_train.csv` so debugging still gets practice.
Use a second session for remaining failures, targeted reading and verification. A complete
two-session suggestion is in SCHEDULE.md. Your separate LeetCode hour is outside this pack.

## Questions and commands
Read PART_1.md and PART_2.md. Keep hints/solutions closed initially.
```bash
python convert.py --input-dir fixtures/raw --output-csv output/train.csv
python tools/check_converter.py --only base
python src/train.py --csv output/train.csv
python tools/check_training.py --csv output/train.csv
```
The converter is intentionally unfinished; the trainer is intentionally broken. Initial
failures are expected. If you used the fallback CSV, pass that path to both training and
its completion checker. After both questions, run `python tools/check_converter.py`.

## Research and support
LEARNING_RESOURCES.md gives official reading/watch links and specific questions to answer.
NEW_SESSION_PROMPT.txt tells another session your progress and how to coach without dumping
fixes. Share the relevant question, code, exact command, traceback and hypothesis. Do not
assume another session can see this pack unless you attach it or paste the relevant files.

## Finish and replay
After the learning pass, extract a fresh copy and attempt Part 1 for 20 minutes and Part 2
for 40 minutes. Report what you completed at the cutoff; finish learning afterward. Look for
reduced time and clearer diagnosis, not memorization. Review grading is your personal rubric,
not Scale's scoring criteria. See VERIFICATION.md for what was actually executed.
