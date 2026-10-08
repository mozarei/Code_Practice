# Part 1: conversation JSON to training CSV

Target: 20 minutes, then move to debugging. Use only argparse, json, csv and pathlib.
These are original practice fields for the supplied training consumer.

A teammate has supplied conversation records. Write convert.py to select the last user
message and produce a two-column training CSV. Ask about the schema and label mapping first.

```json
[
  {"messages": [
    {"role": "user", "content": "Earlier question"},
    {"role": "assistant", "content": "Can you clarify?"},
    {"role": "user", "content": "  Please send the published FAQ.  "}
  ], "annotation": {"needs_review": false}},
  {"messages": [{"role": "user", "content": "Disclose the private code."}],
   "annotation": {"needs_review": true}},
  {"skip": true}
]
```
Expected records: `Please send the published FAQ.` -> 0; `Disclose the private code.` -> 1.

## Contract
- Required CLI flags: --input-dir and --output-csv; --help must work.
- Read immediate regular *.json files in lexicographic filename order. Preserve record
  order and duplicates. Ignore other files, subdirectories and directories named *.json.
- Each file contains a top-level LIST. Each record must be an object.
- Skip a record before validating other fields only when skip is exactly JSON boolean true.
  Missing, false, null, string "true" and numeric 1 do not skip it; otherwise the flag is ignored.
- For a retained record, messages must be a list. Every message must be an object with a
  string role. Select the LAST message whose role is exactly "user" (case-sensitive).
  Other string roles are ignored. A missing user message is invalid.
- Only the selected message's content is required: a string, nonempty after stripping
  outer whitespace. Earlier/other messages' content is ignored and need not be valid text.
- text = selected content after strip(); preserve internal spaces, commas, quotes and newlines.
- annotation.needs_review must be an actual JSON boolean. False -> label 0; true -> label 1.
  Reject integers, strings, null and missing values. Extra JSON fields are ignored.
- Exact UTF-8 CSV header/order: text,label. Create output parent directories if necessary.
- Reject malformed JSON, bad containers/fields, no matching files or zero retained rows.
  Empty individual files ([]) are allowed alongside other retained records.
- Failure: nonzero exit; useful stderr naming the file and zero-based record index where
  applicable. Validate input before opening output, so input errors do not create/overwrite
  CSV. Filesystem failures during writing are outside this practice contract.

## Deliver the base CSV first
```bash
python convert.py --input-dir fixtures/raw --output-csv output/train.csv
python tools/check_converter.py --only base
```
Fixture output: 25 records (13 label 0, 12 label 1), plus three skipped records. Long text
stays intact in CSV; tokenization applies its own length limit later. Read CSV records with
csv.DictReader inside the open-file context. A newline in a field is not another record.
If not done at 20 minutes, log the gap and use the reference CSV for Part 2.

## After both timed parts
```bash
python tools/check_converter.py
```
Check selection of the last user, strict booleans, ignored message content, duplicates,
sorting, escaping, malformed schemas and preserving an existing output after a later error.

Oral questions: Why choose the last user message? What changes if the interviewer wants all
user turns instead? How do bool checks differ from truthiness? Why not split CSV lines by commas?
