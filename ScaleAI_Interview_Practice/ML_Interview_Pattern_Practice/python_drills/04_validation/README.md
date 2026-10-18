# Truthiness, strict types and missing fields

Three short, pure-function problems. No JSON reading or CSV writing. Inputs are already parsed. Do not mutate inputs.

## Problem 1: keep_records

Keep every record except those whose skip field is exactly boolean True. Missing, None, False, integer 1 and string "true" are retained. Records are valid dictionaries.

Example input arguments:
```json
[
  [
    {
      "skip": true
    },
    {
      "skip": 1
    },
    {
      "skip": "true"
    },
    {
      "skip": false
    },
    {
      "skip": null
    },
    {}
  ]
]
```
Expected: `[{"skip": 1}, {"skip": "true"}, {"skip": false}, {"skip": null}, {}]`

If you forget the method, search official Python docs for: **bool subclass of int; identity is vs equality**. First reduce your uncertainty to a two-line experiment.

## Problem 2: integer_label

Return value only if its actual type is int and it is 0 or 1. Reject booleans, floats, strings, None and other integers with ValueError.

Example input arguments:
```json
[
  0
]
```
Expected: `0`

If you forget the method, search official Python docs for: **isinstance bool int; type exact type check**. First reduce your uncertainty to a two-line experiment.

## Problem 3: field_state

Return "missing" if key absent, "null" for None, "empty" for the exact empty string, otherwise "value". Zero, False, whitespace strings and empty lists are values.

Example input arguments:
```json
[
  {},
  "x"
]
```
Expected: `"missing"`

If you forget the method, search official Python docs for: **dict.get default sentinel; in operator**. First reduce your uncertainty to a two-line experiment.

Run from the pack root:
```bash
python python_drills/04_validation/check.py --question 1
python python_drills/04_validation/check.py
```
For a predict-and-observe reference demo, add `--demo --question 1`. This intentionally reveals outputs after you predict. Edit starter.py; hints and reference code are separate.
