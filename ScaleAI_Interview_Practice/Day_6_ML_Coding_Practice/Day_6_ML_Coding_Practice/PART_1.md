# Part 1 - Ticket JSON to training CSV (20 minutes)

Write convert.py using the Python standard library. Working CLI:

```bash
python convert.py --input-dir fixtures/raw --output-csv output/train.csv
```

Required flags: --input-dir, --output-csv, and working --help.
Read immediate REGULAR *.json files, sorted by filename. Ignore other files,
subfolders, and directories ending in .json. Preserve record order and duplicates.

Each JSON file is an object with a tickets list. Each ticket is an object:

```json
{
  "tickets": [
    {
      "payload": {
        "title": "  Request 1  ",
        "paragraphs": ["  First paragraph. ", "  ", " Second paragraph. "]
      },
      "routing": "review",
      "synthetic": false
    },
    {"synthetic": true}
  ]
}
```

Contract:

1. Skip a ticket BEFORE validating its remaining fields only when synthetic
   is exactly boolean true. Numeric 1, string "true", false, null and missing
   are not the skip condition. All other tickets must be valid.
2. payload is an object. title is a string, nonempty after outer strip().
3. paragraphs is a list of strings. Strip each paragraph's outer whitespace;
   discard blank paragraphs. There must be at least one nonblank paragraph.
   A non-string paragraph is invalid, even if other paragraphs are valid.
4. text = stripped title + "\n" + nonblank stripped paragraphs joined with "\n".
   Preserve internal spaces, commas, quotes, Unicode and embedded newlines.
5. routing is exactly "normal" -> 0 or "review" -> 1. Other strings/types
   and missing routing are errors. Ignore unrelated extra fields.
6. Write UTF-8 CSV with exactly text,label in that order. Let csv handle
   escaping. Create the output's parent directories on success.
7. Reject invalid JSON/containers/fields, missing input directory, no matching
   JSON files or no retained rows. Empty tickets lists may accompany valid files.
   Return nonzero and print useful stderr. Name the failing file and zero-based
   "record N" for record errors.
8. Validate ALL input before opening output. Invalid input must not create
   a CSV or overwrite an existing CSV. Write-time filesystem failures are
   outside this exercise contract.

Example text: "Request 1\nFirst paragraph.\nSecond paragraph."; label 1.
Supplied fixture: 21 retained records (11 label 0, 10 label 1), three skipped.
Count CSV RECORDS with DictReader, not physical lines.

Clarify aloud before coding: required columns, label mapping, text assembly,
skip rules, and how to handle invalid records. Those choices in THIS exercise
are defined above; the real interview may define different policies.

```bash
python tools/check_converter.py --only base
python tools/check_converter.py
```

The full checker covers 26 scenarios plus CLI help, including BERT-compatible
column names, escaping, ordering, blank filtering and validation failures.
At the timer boundary, use the reference CSV for Part 2 if needed.
