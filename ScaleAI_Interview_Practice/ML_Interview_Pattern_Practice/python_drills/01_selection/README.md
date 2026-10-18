# Selection and last matching records

Three short, pure-function problems. No JSON reading or CSV writing. Inputs are already parsed. Do not mutate inputs.

## Problem 1: last_final

Return the LAST review in input order matching document_id and status="final". A later draft does not cancel it. Return None if absent. Inputs are valid objects; compare IDs exactly.

Example input arguments:
```json
[
  [
    {
      "document_id": "a",
      "status": "final",
      "label": 1
    },
    {
      "document_id": "a",
      "status": "draft"
    },
    {
      "document_id": "a",
      "status": "final",
      "label": 0
    }
  ],
  "a"
]
```
Expected: `{"document_id": "a", "status": "final", "label": 0}`

If you forget the method, search official Python docs for: **reversed next generator default; Python for loop overwrite**. First reduce your uncertainty to a two-line experiment.

## Problem 2: latest_final

Return the matching FINAL review with greatest integer timestamp. Break timestamp ties by the later input occurrence. Negative timestamps are valid. Return None if absent; input order need not be chronological.

Example input arguments:
```json
[
  [
    {
      "document_id": "a",
      "status": "final",
      "timestamp": 8
    },
    {
      "document_id": "a",
      "status": "final",
      "timestamp": 3
    }
  ],
  "a"
]
```
Expected: `{"document_id": "a", "status": "final", "timestamp": 8}`

If you forget the method, search official Python docs for: **max key default; enumerate; tie breaking**. First reduce your uncertainty to a two-line experiment.

## Problem 3: first_non_none

Return the first value that is not None. Zero, False, empty string and empty containers are valid results. Return None if there is no such value.

Example input arguments:
```json
[
  [
    null,
    0,
    7
  ]
]
```
Expected: `0`

If you forget the method, search official Python docs for: **Python truth value testing is None**. First reduce your uncertainty to a two-line experiment.

Run from the pack root:
```bash
python python_drills/01_selection/check.py --question 1
python python_drills/01_selection/check.py
```
For a predict-and-observe reference demo, add `--demo --question 1`. This intentionally reveals outputs after you predict. Edit starter.py; hints and reference code are separate.
