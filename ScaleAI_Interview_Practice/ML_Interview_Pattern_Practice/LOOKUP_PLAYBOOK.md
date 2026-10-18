# Recognize the operation, then look up a small API

| Wording in the problem | Likely pattern | What to verify |
|---|---|---|
| Last matching record | Forward overwrite or reverse scan | List order or timestamp? |
| Latest timestamp | max/key or explicit comparison | Ties, negative values, no match |
| Have I seen this ID? | set membership | Must output order be preserved? |
| Find the value for this ID | dict lookup/join | Missing ID; label zero; per-file scope |
| Collect all texts by category | defaultdict(list) / setdefault | Separate lists; duplicates; order |
| Replace inside a string | Slice + concatenate, or str.replace | Half-open indices; literal vs regex |
| Sort with a custom rule | sorted(..., key=...) | Numeric vs lexicographic; stable ties |
| One record has many paragraphs | Nested scan/flatten | Skip blanks without losing label zero |
| Keep the final short batch | Slicing in range(..., step) | B=1 tail; no silent dropping |
| Training logs but no changes | Inspect graph, grad, optimizer, snapshot | Same objects? Independent before copy? |

## When you do not remember the method
1. Restate the requirement precisely, including one edge case.
2. Reduce it to the operation: membership, lookup, selection, grouping, slicing,
   sorting, or shape inspection. Search for that operation, not an entire solution.
3. Open an official API page and inspect signature, return type and one example.
4. Run a TWO-LINE experiment in the Python REPL. For instance:
   print('a.b a.b'.replace('a.b','X',1)) or print(bool(0), 0 is None).
5. Apply it, test the edge case, and explain why it follows the contract.

Search queries: "Python str.replace count", "Python sorting stable key tuple",
"Python dict get missing None sentinel", "Python defaultdict list",
"PyTorch Tensor detach shares storage", "Hugging Face BERT pooler_output shape".
Use ordinary documentation and search in a real mock; AI assistance is not allowed
in the actual interview. If stuck navigating, explain what you are looking for
and ask the interviewer for a focused hint, as the prep guidance allows.

Official sources:
- https://docs.python.org/3/library/argparse.html
- https://docs.python.org/3/library/csv.html
- https://docs.python.org/3/library/json.html
- https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str
- https://docs.python.org/3/howto/sorting.html
- https://docs.python.org/3/library/collections.html#collections.defaultdict
- https://docs.python.org/3/library/pdb.html
- https://docs.pytorch.org/docs/2.7/optim.html
- https://docs.pytorch.org/docs/2.7/generated/torch.Tensor.detach.html
- https://docs.pytorch.org/docs/2.7/generated/torch.nn.CrossEntropyLoss.html
- https://huggingface.co/docs/transformers/model_doc/bert
- https://huggingface.co/learn/llm-course/chapter3/2?fw=pt (read/watch)
- https://huggingface.co/learn/llm-course/chapter3/4?fw=pt (read/watch)

Newer documentation can show additional APIs. The pack pins transformers 4.57.1;
the tested main PyTorch API version is 2.7.1. Copy the core ideas, not unverified
newer keyword arguments.
