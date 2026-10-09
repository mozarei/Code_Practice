# Official reading and watch material
Read the section tied to the current experiment, then return to code.
PyTorch API links are version 2.7, matching the main tested environment.
Intel Mac pin uses 2.2.2; these core concepts are also verified with that version.

| Topic | Primary source | Reading goal |
|---|---|---|
| Module structure | https://docs.pytorch.org/docs/2.7/generated/torch.nn.Module.html | children, named_modules, parameters, named_parameters, train/eval |
| Gradients / graph | https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html | leaf grads, backward, tracking and accumulation |
| Optimizers | https://docs.pytorch.org/docs/2.7/optim.html | params, groups, zero_grad and step |
| None versus zero | https://docs.pytorch.org/docs/2.7/generated/torch.optim.Optimizer.zero_grad.html | buffers and optimizer behavior |
| Cross-entropy | https://docs.pytorch.org/docs/2.7/generated/torch.nn.CrossEntropyLoss.html | class-index target shapes/dtypes; separate soft-target interface |
| Embedding | https://docs.pytorch.org/docs/2.7/generated/torch.nn.Embedding.html | integer lookup indices and output shape |
| BERT inputs | https://huggingface.co/docs/transformers/model_doc/bert | input_ids, attention_mask, token_type_ids |
| Full loop - read/watch | https://huggingface.co/learn/llm-course/chapter3/4?fw=pt | trace a real batch through model, loss, backward and step; embedded video |
| Data processing - read/watch | https://huggingface.co/learn/llm-course/chapter3/2?fw=pt | tokenizer, dynamic padding and batching; embedded video |
| JSON and CSV | https://docs.python.org/3/library/json.html and https://docs.python.org/3/library/csv.html | types, escaping and file handling |
| CLI | https://docs.python.org/3/library/argparse.html | flags, help and parsed args |
| Debugger | https://docs.python.org/3/library/pdb.html | p, n, s, c, q and breakpoint |

Study code execution first. Detailed attention derivations, distributed
training and hyperparameter tuning are lower priority for this coding screen.
They may matter in later rounds, whose exact module scope has not been provided.
