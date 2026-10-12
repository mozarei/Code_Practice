# Part 1 - Join documents and final reviews into CSV
Timed replay: 20 minutes. Learning pass: take the time you need.

Write a CLI using Python's argparse, json, csv and pathlib:
```bash
python convert.py --input-dir fixtures/raw --output-csv output/train.csv
```
Required flags: --input-dir, --output-csv and working --help.

Each JSON file has TWO lists. Reviews can be in a different order from documents:
```json
{
  "documents": [
    {"id": "a", "content": {"title": " Request A ", "body": " First body. "}},
    {"id": "b", "content": {"title": " Request B ", "body": " Second body. "}}
  ],
  "reviews": [
    {"document_id": "a", "status": "final", "decision": "review"},
    {"document_id": "b", "status": "draft"},
    {"document_id": "a", "status": "final", "decision": "allow"},
    {"document_id": "a", "status": "draft", "decision": null}
  ]
}
```
Emit only A, with text "Request A\nFirst body." and label 0.
The later final wins. The later draft does not cancel the final.

## Contract
1. Read sorted immediate REGULAR *.json files. Ignore other files/subfolders/
   JSON-named directories. Each file is an object containing documents and
   reviews lists. Empty lists are allowed when the overall export produces rows.
2. Every document is an object with id and content. id is a nonblank string;
   compare IDs EXACTLY as supplied, case sensitively, without trimming IDs.
   Duplicate document IDs WITHIN ONE FILE are errors. IDs may recur in a
   different file, where they refer to a separate export.
3. content is an object. title and body are nonblank strings. Validate ALL
   documents, even those that eventually have no final review.
4. Every review is an object. document_id is a nonblank string; status is
   exactly 'draft' or 'final'. A draft's decision is ignored and may be absent
   or any type. A final's decision must be exactly 'allow' or 'review'.
   Validate these fields even for reviews referring to unknown document IDs.
5. Within EACH FILE, select the LAST final review in reviews list order for
   each known document. Drafts never replace final decisions. Unknown document
   IDs in valid reviews are ignored. No final review -> do not emit that document.
6. Emit in documents list order, then sorted file order. Preserve separate
   documents with identical text and records across files. Do not emit in
   review order and do not globally merge reused IDs.
7. text = title.strip() + '\n' + body.strip(). Preserve all internal whitespace,
   commas, quotes, embedded newlines and Unicode. allow -> 0; review -> 1.
   Exact UTF-8 CSV columns/order: text,label. Ignore unrelated extra fields.
8. Reject malformed JSON, invalid containers/fields, no matching files or
   zero emitted rows. Return nonzero with useful stderr identifying file and
   zero-based 'documents record N' or 'reviews record N' when applicable.
9. Validate all inputs BEFORE opening output. Input errors must not create
   or overwrite CSV. Create output parent directories on success. Filesystem
   failures during writing are outside this practice contract.

Supplied fixtures: 32 documents, 29 emitted rows (15 allow/0, 14 review/1),
three with only draft reviews. They include reused IDs across files, out-of-order
reviews, Unicode/newlines and text longer than the training token limit.
Count CSV records with DictReader; multiline text makes physical lines misleading.

These detailed validation policies are chosen for this practice exercise;
the actual interview may specify simpler or different policies. Confirm its
required columns/mapping before coding. First make the base CSV; review edge
cases after preserving Part 2's time.

```bash
python tools/check_converter.py --only base
python tools/check_converter.py
```
The checker covers 35 scenarios plus CLI help. It tests output preservation
on errors, joins, last-final selection, per-file ID scope and exact escaping.
