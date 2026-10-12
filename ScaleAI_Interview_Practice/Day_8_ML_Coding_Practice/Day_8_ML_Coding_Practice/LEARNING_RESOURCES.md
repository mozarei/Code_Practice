# Focused official reading and watch links
Use the source tied to your current boundary, then return to code. HF current
docs can describe newer versions; the pack pins transformers 4.57.1 and its
actual behavior was verified. PyTorch API links below use the main pin 2.7.

| Topic | Source | Read/watch goal |
|---|---|---|
| Dictionaries / joins | https://docs.python.org/3/tutorial/datastructures.html#dictionaries | lookup, membership and replacement |
| JSON types | https://docs.python.org/3/library/json.html | object/list/string mappings |
| CSV / CLI | https://docs.python.org/3/library/csv.html and https://docs.python.org/3/library/argparse.html | quoting, multiline records, required flags |
| Padding / truncation | https://huggingface.co/docs/transformers/main/en/pad_truncation | different purposes of padding and truncation |
| Data processing - read/watch | https://huggingface.co/learn/llm-course/chapter3/2?fw=pt | variable-length batching; embedded videos |
| BERT representations | https://huggingface.co/docs/transformers/model_doc/bert | last_hidden_state and sequence-level pooled output |
| Full loop - read/watch | https://huggingface.co/learn/llm-course/chapter3/4?fw=pt | forward, loss, backward, step and persistence |
| Optimizers | https://docs.pytorch.org/docs/2.7/optim.html | parameter objects, groups, zero_grad and step |
| Copy / identity | https://docs.python.org/3/library/copy.html | assignment versus constructing copied objects |
| Debugger | https://docs.python.org/3/library/pdb.html | p, n, s, c, breakpoint |

Main preparation stays practical: Python data transformations and debugging
a supplied CPU trainer. Architecture derivations, EDA, tuning, GPU/distributed
setup and later-round product/system-design questions are outside this set.
