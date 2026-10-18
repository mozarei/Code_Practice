# Flattening, partial batches and per-file scope

Three short, pure-function problems. No JSON reading or CSV writing. Inputs are already parsed. Do not mutate inputs.

## Problem 1: flatten_paragraphs

Valid documents contain id, label and a list of string paragraphs. Emit {document_id,text,label} for each nonblank stripped paragraph, in document order then paragraph order. Preserve duplicate text and label zero.

Example input arguments:
```json
[
  [
    {
      "id": "a",
      "label": 0,
      "paragraphs": [
        " first ",
        " ",
        "second"
      ]
    },
    {
      "id": "b",
      "label": 1,
      "paragraphs": [
        "x",
        "x"
      ]
    }
  ]
]
```
Expected: `[{"document_id": "a", "text": "first", "label": 0}, {"document_id": "a", "text": "second", "label": 0}, {"document_id": "b", "text": "x", "label": 1}, {"document_id": "b", "text": "x", "label": 1}]`

If you forget the method, search official Python docs for: **nested for loops; list comprehension flatten**. First reduce your uncertainty to a two-line experiment.

## Problem 2: chunks

Return consecutive list chunks of at most size, retaining the final partial chunk. Empty input returns []. Require actual integer size > 0, rejecting booleans and invalid sizes with ValueError.

Example input arguments:
```json
[
  [
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8
  ],
  4
]
```
Expected: `[[0, 1, 2, 3], [4, 5, 6, 7], [8]]`

If you forget the method, search official Python docs for: **range step; list slicing partial final chunk**. First reduce your uncertainty to a two-line experiment.

## Problem 3: rows_per_export

Each valid export contains documents {id,text} and reviews {document_id,status,label}. Within EACH export choose the last FINAL label, then emit [text,label] in document order. Skip unreviewed documents; IDs may repeat across exports and must not share decisions.

Example input arguments:
```json
[
  [
    {
      "documents": [
        {
          "id": "a",
          "text": "first"
        }
      ],
      "reviews": [
        {
          "document_id": "a",
          "status": "final",
          "label": 0
        }
      ]
    },
    {
      "documents": [
        {
          "id": "a",
          "text": "second"
        }
      ],
      "reviews": [
        {
          "document_id": "a",
          "status": "final",
          "label": 1
        }
      ]
    }
  ]
]
```
Expected: `[["first", 0], ["second", 1]]`

If you forget the method, search official Python docs for: **variable scope; initialize dictionary inside outer loop**. First reduce your uncertainty to a two-line experiment.

Run from the pack root:
```bash
python python_drills/06_scans_and_scope/check.py --question 1
python python_drills/06_scans_and_scope/check.py
```
For a predict-and-observe reference demo, add `--demo --question 1`. This intentionally reveals outputs after you predict. Edit starter.py; hints and reference code are separate.
