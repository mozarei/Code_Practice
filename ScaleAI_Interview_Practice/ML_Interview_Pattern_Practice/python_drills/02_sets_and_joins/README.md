# Sets, dictionaries and stable joins

Three short, pure-function problems. No JSON reading or CSV writing. Inputs are already parsed. Do not mutate inputs.

## Problem 1: stable_unique

Return unique string IDs in first-occurrence order. Do not sort and do not mutate the input.

Example input arguments:
```json
[
  [
    "b",
    "a",
    "b",
    "c",
    "a"
  ]
]
```
Expected: `["b", "a", "c"]`

If you forget the method, search official Python docs for: **set membership; dict.fromkeys insertion order**. First reduce your uncertainty to a two-line experiment.

## Problem 2: attach_labels

Join valid documents {id,text} to the last FINAL review {document_id,status,label}. Return [text,label] rows in document order; skip documents with no final review and ignore unknown IDs. Label 0 must be retained.

Example input arguments:
```json
[
  [
    {
      "id": "b",
      "text": "B"
    },
    {
      "id": "a",
      "text": "A"
    }
  ],
  [
    {
      "document_id": "a",
      "status": "final",
      "label": 0
    },
    {
      "document_id": "b",
      "status": "final",
      "label": 1
    }
  ]
]
```
Expected: `[["B", 1], ["A", 0]]`

If you forget the method, search official Python docs for: **dictionary membership vs get; dictionary assignment replaces value**. First reduce your uncertainty to a two-line experiment.

## Problem 3: unknown_ids

Return unknown document IDs from reviews, once each in first-occurrence order. known_ids is a list of strings; each review has document_id.

Example input arguments:
```json
[
  [
    "a"
  ],
  [
    {
      "document_id": "x",
      "status": "final"
    },
    {
      "document_id": "a",
      "status": "final"
    },
    {
      "document_id": "x",
      "status": "final"
    },
    {
      "document_id": "y",
      "status": "final"
    }
  ]
]
```
Expected: `["x", "y"]`

If you forget the method, search official Python docs for: **set membership difference; preserve input order**. First reduce your uncertainty to a two-line experiment.

Run from the pack root:
```bash
python python_drills/02_sets_and_joins/check.py --question 1
python python_drills/02_sets_and_joins/check.py
```
For a predict-and-observe reference demo, add `--demo --question 1`. This intentionally reveals outputs after you predict. Edit starter.py; hints and reference code are separate.
