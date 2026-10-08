# Read / watch / apply

Use the exact error to choose a resource. Read 10-20 minutes, close the page, then apply or
explain the concept in your own words. The core pack deliberately uses a manual training
loop so you can inspect the calls; Trainer is optional later reading.

| Topic | Primary resource | What to explain or inspect |
|---|---|---|
| CLI arguments | https://docs.python.org/3/library/argparse.html | How parser options become `args` attributes |
| JSON objects/lists | https://docs.python.org/3/library/json.html | Types returned by json.load; nested access |
| CSV escaping/reading | https://docs.python.org/3/library/csv.html | DictReader.fieldnames; iteration while file is open; newline handling |
| Files and sorting | https://docs.python.org/3/library/pathlib.html | glob, is_file and sorted; top-level versus recursive matching |
| Debugger | https://docs.python.org/3/library/pdb.html | Pause, inspect type/value, step and continue |
| VS Code debugging | https://code.visualstudio.com/docs/python/debugging | Interpreter, breakpoint, call stack, variable inspection |
| Tokenization and batches - read/watch | https://huggingface.co/learn/llm-course/chapter3/2?fw=pt | Raw strings -> token IDs/masks; padding and truncation; inspect a batch |
| Hugging Face training loop - read/watch | https://huggingface.co/learn/llm-course/chapter3/4?fw=pt | Model input/output contract; loss; backward; optimizer; CPU adaptation |
| PyTorch modules - read/watch | https://docs.pytorch.org/tutorials/beginner/introyt/modelsyt_tutorial.html | nn.Module, forward, registered parameters and calling a module |
| PyTorch gradients - read/watch | https://docs.pytorch.org/tutorials/beginner/introyt/autogradyt_tutorial.html | Computation graph and when gradients are available |
| PyTorch optimization | https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html | zero_grad, backward and step; train/eval distinction |
| Classification loss | https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html | Logits [batch,classes]; integer class indices [batch] |
| Included pretrained model | https://huggingface.co/prajjwal1/bert-tiny | A small pretrained encoder; why the new head still needs training |

The official HF course and PyTorch intro pages include embedded videos. Use their explanation
sections; do not copy their entire larger-dataset setup into this exercise. Course versions
may show newer APIs than this pack's pinned versions: Transformers 4.57.1 and PyTorch 2.7.1
(2.2.2 on Intel Mac). Follow the exercise's code and environment check.

## Answer these by inspecting your repaired run
1. Why is a Python list of records different from a list of text strings?
2. What shapes/dtypes do input_ids, attention_mask and labels have in your first batch?
3. Why can sequence length differ between batches even though batch size is fixed?
4. What are logits, and how do they differ from probabilities or predicted class IDs?
5. What does an HF classification model return, and which fields can callers use?
6. Why can a scalar loss be numerically valid yet unsuitable for backward propagation?
7. Does model.eval() by itself disable autograd? What changes under train()?
8. What evidence proves that training updated the pretrained encoder rather than only the head?
9. What does a successful reload establish? Why is it not evidence of good predictions?

## Scope for this screen
Prioritize conversion, repository navigation, traceback reading, types/shapes, tokenization,
forward/loss/gradient flow and speaking through a hypothesis. Skip distributed training,
GPUs, LoRA, system design, EDA and hyperparameter optimization in this practice block.
