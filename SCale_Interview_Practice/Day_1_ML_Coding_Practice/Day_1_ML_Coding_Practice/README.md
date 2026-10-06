# Day 1 - three-hour ML coding practice

Prepared for Mohammad Zarei, October 4, 2026. First interview: October 26.
These are original practice questions built around your supplied interview format.

## Start in VS Code
1. Extract this ZIP and open the extracted `Day_1_ML_Coding_Practice` folder with File > Open Folder.
2. Select your Python 3.10+ interpreter. Open Terminal > New Terminal at the project root.
3. Disable AI assistants and AI completion during attempts. Ordinary documentation is allowed.
4. Keep `solutions/` and `hints/` closed. Preserve an untouched copy for reattempts.
5. Run `python tools/check_environment.py`. If your system uses `python3`, use that name consistently.

Core Day 1 needs no third-party packages. Choose standard-library Route S by default. Route T
uses PyTorch if already installed. Do not spend this session installing ML packages. The optional
`.vscode/launch.json` configurations work with VS Code's Python Debugger extension; terminal
`breakpoint()` also works without that extension. Your local editor is similar to the Codespace,
but the actual interview uses a shared browser-based GitHub Codespace.

## Exactly 180 minutes

| Minutes | Task | Evidence |
| --- | --- | --- |
| 0-10 | Open project, select route, read contracts and clarify aloud | State columns, record shape and validation policy |
| 10-30 | Question 1: implement the CLI JSON-to-CSV converter | Valid two-column CSV; run the base check |
| 30-70 | Question 2: repair the selected three-bug training route | One hypothesis/change/rerun at a time |
| 70-100 | Converter scenario review | Run all checks; repair uncovered edge cases |
| 100-130 | Debugging reinforcement | Reproduce each fix and explain its evidence; review only after attempting |
| 130-155 | Question 3: changed-schema converter | Write and check a second CSV contract |
| 155-175 | Spoken explanation + log | Explain three causes and one tradeoff; revise English |
| 175-180 | Pick tomorrow's weak skill | One measurable next target |

If unfinished at a block boundary, log the gap and move on. The reference CSV lets you attempt
debugging independently. The separate nightly LeetCode hour is outside these 180 minutes.

## Run order

```bash
python tools/check_environment.py
python convert.py --input-dir fixtures/raw --output-csv output/train.csv
python tools/check_converter.py --only base
python src/train.py --csv output/train.csv
```

For the optional route, replace the last command with `python torch_src/train.py --csv output/train.csv`.
If the converter is unfinished, use `--csv fixtures/reference_train.csv` for the training command.

Later review:

```bash
python tools/check_converter.py
python tools/check_training.py --route stdlib --csv output/train.csv
python variant_convert.py --input-dir fixtures/variant_reviews --output-csv output/reviews.csv
python tools/check_variant.py
```

Read PART_1.md, PART_2.md and VARIANT.md for complete requirements. Checkers run your CLI in
temporary folders and leave your project fixtures unchanged. Checks report behavioral failures;
they are not a requirement to inspect the reference implementation.

## Ask your other session for help
Paste the question contract, exact command, full traceback, relevant code and your hypothesis.
Start with: "PRACTICE MODE: give one hint, not the solution." For direct explanations or full
answers after attempting, say: "REVIEW MODE: explain the root cause and corrected code."
A complete reusable daily-generation prompt is included in DAILY_COACH_PROMPT.txt.

## Sources / verification
Your supplied technical-screen sheet motivates the 20/40 minute format and no-AI practice.
The tiny models in this pack are learning exercises, not pretrained-model fine-tuning or security
products. The actual training objective and bugs have not been disclosed. See VERIFICATION.md
for executed checks and the optional PyTorch runtime limitation.

Official references:
- https://docs.python.org/3/library/json.html
- https://docs.python.org/3/library/csv.html
- https://docs.python.org/3/library/argparse.html
- https://docs.python.org/3/library/pdb.html
- https://code.visualstudio.com/docs/python/debugging
- https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html
