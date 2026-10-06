# Question 3: changed data contract

Review-block budget: 25 minutes. Implement `variant_convert.py` independently or carefully
adapt your converter. This CSV is for a different consumer; do not run the base trainer on it.

Each input file contains a TOP-LEVEL LIST of review records. Fields are `message.title`,
`message.body`, and `decision.approved`. There is no exclusion flag in this question.

- Same CLI: `--input-dir` and `--output-csv`, using argparse.
- Read immediate lowercase *.json files in sorted filename order; preserve record order.
  Ignore non-JSON files and subfolders.
- Title/body must be strings and nonempty after stripping outer whitespace. Preserve internal
  spaces, punctuation and newlines.
- `approved` must be a JSON boolean. Do not accept the strings `"true"`/`"false"`, numbers 0/1,
  null, or missing values as substitutes.
- Exact header: `sentence,target`. Sentence is title + ` | ` + body. Boolean true maps to
  integer target 0; false maps to integer target 1.
- Reject malformed input and a final empty dataset. Validate all input before opening output,
  so an invalid record cannot overwrite an existing output file. Record diagnostics must name
  file and zero-based record index.

```bash
python variant_convert.py --input-dir fixtures/variant_reviews --output-csv output/reviews.csv
python tools/check_variant.py
```

Supplied fixtures yield 3 rows. First parsed row: sentence `Request, review | Please review the
"draft".`, target `0`. Explain which assumptions you changed and why the original downstream
training code would not accept this header.
