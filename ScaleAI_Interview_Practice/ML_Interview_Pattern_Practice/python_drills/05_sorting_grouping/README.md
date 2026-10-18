# Ordering contracts and grouping

Three short, pure-function problems. No JSON reading or CSV writing. Inputs are already parsed. Do not mutate inputs.

## Problem 1: sort_export_names

Names are valid filenames beginning with a positive integer then underscore. Sort by numeric prefix, breaking numeric ties by the full filename lexicographically. This practice contract deliberately differs from ordinary filename sorting.

Example input arguments:
```json
[
  [
    "10_x.json",
    "2_x.json",
    "1_x.json"
  ]
]
```
Expected: `["1_x.json", "2_x.json", "10_x.json"]`

If you forget the method, search official Python docs for: **sorted key tuple int string split**. First reduce your uncertainty to a two-line experiment.

## Problem 2: sort_tickets

Sort valid ticket objects by severity: critical, high, normal, then any unknown severity. Preserve original order among equal-priority tickets, including different unknown values. Do not sort ties by ID.

Example input arguments:
```json
[
  [
    {
      "id": "z",
      "severity": "normal"
    },
    {
      "id": "a",
      "severity": "critical"
    },
    {
      "id": "b",
      "severity": "high"
    }
  ]
]
```
Expected: `[{"id": "a", "severity": "critical"}, {"id": "b", "severity": "high"}, {"id": "z", "severity": "normal"}]`

If you forget the method, search official Python docs for: **Python sorting stability; dict.get default**. First reduce your uncertainty to a two-line experiment.

## Problem 3: group_texts

Group valid {category,text} records into a plain dictionary category -> list of texts. Preserve text order and duplicates within each group. Include only categories seen in input.

Example input arguments:
```json
[
  [
    {
      "category": "review",
      "text": "B"
    },
    {
      "category": "allow",
      "text": "A"
    },
    {
      "category": "review",
      "text": "B"
    }
  ]
]
```
Expected: `{"review": ["B", "B"], "allow": ["A"]}`

If you forget the method, search official Python docs for: **collections.defaultdict list; dict.setdefault mutable values**. First reduce your uncertainty to a two-line experiment.

Run from the pack root:
```bash
python python_drills/05_sorting_grouping/check.py --question 1
python python_drills/05_sorting_grouping/check.py
```
For a predict-and-observe reference demo, add `--demo --question 1`. This intentionally reveals outputs after you predict. Edit starter.py; hints and reference code are separate.
