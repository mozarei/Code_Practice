# Question 1: JSON to training CSV

Original practice exercise, not a disclosed Scale question. Timed budget: 20 minutes.
Implement `convert.py`. Use `argparse`, `json`, `csv`, and `pathlib` from the standard library.
The CLI must accept `--input-dir` and `--output-csv` and expose `--help`.

## Input and output contract

Each input JSON file is an object containing an `examples` list. Each retained example has
`document.title`, `document.body`, and `annotation.risk`. Other properties are irrelevant.

1. Read only immediate, lowercase `*.json` files. Do not recurse. Sort filenames lexicographically;
   preserve each file's record order. Duplicate examples must be preserved.
2. Each example must be an object. If its `excluded` value is exactly the JSON boolean `true`,
   skip it before validating its other fields. Missing flags, `false`, null, and the string `"true"`
   do not exclude a record. Do not coerce or type-check other flag values.
3. On retained records, title and body must both be strings and nonempty after `strip()`.
   Strip only leading/trailing whitespace. Preserve internal spaces, punctuation and newlines.
4. Build `text` as stripped title + one newline + stripped body.
5. Map exact category strings: `benign` -> integer 0, `risky` -> integer 1. No case normalization.
6. Write UTF-8 CSV with exactly `text,label` in that order. Use correct CSV quoting.
7. Reject missing/invalid required fields, unknown categories, malformed JSON, incorrect container
   shapes, no input JSON files, and an empty final retained dataset. Empty lists in individual
   files are allowed when another file supplies valid retained records.
8. For record validation errors, name the file and zero-based record index in the diagnostic.
   For container/JSON errors, name the file. Validate the input before opening the output file:
   validation failure must not create or overwrite the requested CSV. Output-directory creation
   is allowed after validation. Filesystem write failures are outside this drill's scope.

The supplied main fixtures produce 12 data rows: 6 benign and 6 risky. There are two excluded
records. The string-valued exclusion flag belongs to a valid retained example.
First parsed CSV row: text `Meeting notes\nPlease send the agenda for tomorrow.`, label `0`.
A CSV reader returns the serialized label as a string; the training reader must convert it.

```bash
python convert.py --input-dir fixtures/raw --output-csv output/train.csv
python tools/check_converter.py --only base
```

Move to debugging at minute 30 of your Day 1 session. If conversion is unfinished, use the
supplied `fixtures/reference_train.csv` for Part 2 and record that Part 1 needs more work.
Run all scenario checks during the later review block:

```bash
python tools/check_converter.py
```

## Clarify aloud before writing
What does each column mean? What is one row? Should malformed records fail? What ordering is
required? Are string flags equivalent to booleans? What header does the training reader expect?

## Optional personal checks
Before looking at provided checks, write one valid and one invalid JSON example yourself.
Read the resulting CSV with `csv.DictReader`; check its header, row count and one escaped field.
