# Question 1: JSON folder to training CSV

These are original practice requirements; Scale has not disclosed the actual fields or labels.
Learning pass: research as needed and record elapsed time. Replay target: 20 minutes; eventually 15.

Your teammate has provided raw request records. Write `convert.py` so the supplied training
reader can consume a two-column CSV. Use `argparse`, `json`, `csv`, and `pathlib` only.

```json
{"records": [
  {"content": {"title": "  Meeting, update  ", "body": "Send the \"draft\".\nKeep the reference."},
   "review": {"category": "routine"}, "include": true},
  {"include": false},
  {"content": {"title": "Outage", "body": "Escalate immediately."},
   "review": {"category": "urgent"}}
]}
```

## Confirm these requirements before coding
- CLI: `--input-dir` and `--output-csv`; both required; `--help` works.
- Read immediate regular files ending in `.json`, in lexicographic filename order.
  Preserve record order and duplicates; ignore other files and all subdirectories.
- Each file is an object containing a `records` list. Each record must be an object.
- Skip a record before validating its other fields only when `include` is exactly JSON
  boolean false. Missing, null, true, numeric 0 and the string `"false"` do not skip it.
  Otherwise the flag is not validated or converted.
- Retained records require string `content.title` and `content.body`, both nonempty after
  stripping outer whitespace. Preserve all internal spaces, commas, quotes and newlines.
- `text` = stripped title + one newline + stripped body.
- Exact, case-sensitive `review.category`: `routine` -> 0; `urgent` -> 1.
- Exact UTF-8 CSV header/order: `text,label`. Create output parent directories if needed.
- Ignore extra JSON fields. An empty `records` list is valid alongside other retained rows.
- Reject malformed JSON, invalid containers, missing/invalid required fields, unknown
  categories, no matching input files or an entirely empty retained dataset.
- On failure: nonzero exit and useful stderr. Name the file; for a record error, also
  name its zero-based index (for example `record 1`). Do not create or overwrite the CSV
  on an input-validation error. Validate inputs before opening the output for writing.
  Failure of the filesystem during writing is outside this exercise's contract.

## First pass: move to debugging after the base case
```bash
python convert.py --input-dir fixtures/raw --output-csv output/train.csv
python tools/check_converter.py --only base
```
Supplied fixtures: 24 retained rows, 12 per label, plus three skipped records. They contain
short/long text, punctuation, embedded newlines, Unicode and optional flags. The CSV itself
preserves the long text; truncation belongs to tokenization. Read it with `csv.DictReader`:
count records inside the `with` block and inspect `reader.fieldnames`. Embedded newlines
mean physical file line count is not the row count.

## After attempting both parts: expand your scenarios
```bash
python tools/check_converter.py
```
The checks include sorting, duplicates, escaping, exact boolean filtering, ignored paths,
malformed input, empty datasets and preservation of existing output on a later-record error.
Requirements are explicit; the checker has no hidden input rules. Keep the solution closed.

## Oral follow-ups
1. Which CSV columns does the training reader expect?
2. Why does `is False` differ from `== False` or `not value` here?
3. Why use `newline=""` and a CSV writer instead of joining strings with commas?
4. What can you deliver in 20 minutes, and what would you review afterward?
