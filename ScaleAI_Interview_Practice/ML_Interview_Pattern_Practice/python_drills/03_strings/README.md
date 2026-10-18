# Immutable strings and precise text assembly

Three short, pure-function problems. No JSON reading or CSV writing. Inputs are already parsed. Do not mutate inputs.

## Problem 1: replace_span

Return a NEW string replacing the half-open range [start,end). Require 0 <= start <= end <= len(text), otherwise raise ValueError. Python string indices count Unicode code points, not UTF-8 bytes.

Example input arguments:
```json
[
  "abcdef",
  2,
  4,
  "XY"
]
```
Expected: `"abXYef"`

If you forget the method, search official Python docs for: **str immutable sequence slicing half-open range**. First reduce your uncertainty to a two-line experiment.

## Problem 2: replace_first

Replace only the first LITERAL occurrence of nonempty old. Return unchanged text when absent; reject empty old with ValueError. Dots and brackets are literal characters, not regex syntax.

Example input arguments:
```json
[
  "a.b a.b",
  "a.b",
  "X"
]
```
Expected: `"X a.b"`

If you forget the method, search official Python docs for: **str.replace count; literal vs regular expression**. First reduce your uncertainty to a two-line experiment.

## Problem 3: assemble_text

Title must be a nonblank string and paragraphs a list of strings. Trim only outer whitespace, discard blank paragraphs, require at least one nonblank paragraph. Return title + newline + paragraphs joined by newline. Preserve internal whitespace and punctuation; raise ValueError for invalid input.

Example input arguments:
```json
[
  " T ",
  [
    " first ",
    " ",
    " second\nline "
  ]
]
```
Expected: `"T\nfirst\nsecond\nline"`

If you forget the method, search official Python docs for: **str.strip str.join; whitespace preservation**. First reduce your uncertainty to a two-line experiment.

Run from the pack root:
```bash
python python_drills/03_strings/check.py --question 1
python python_drills/03_strings/check.py
```
For a predict-and-observe reference demo, add `--demo --question 1`. This intentionally reveals outputs after you predict. Edit starter.py; hints and reference code are separate.
