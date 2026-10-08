# Official resources: choose by the observed failure

Read for 10-15 minutes, close the page, then inspect or apply what you learned. These resources
cover the component contracts; they are not a list of the three defect locations.

| Topic | Link | Question to answer |
|---|---|---|
| JSON and Python types | https://docs.python.org/3/library/json.html | Which values become list/dict/bool? |
| CSV | https://docs.python.org/3/library/csv.html | How do quotes/newlines survive writing and reading? |
| CLI | https://docs.python.org/3/library/argparse.html | How do flags become Path arguments? |
| File discovery | https://docs.python.org/3/library/pathlib.html | Which matches are regular files? |
| Tokenization/batching - read/watch | https://huggingface.co/learn/llm-course/chapter3/2?fw=pt | How does text become IDs, masks and tensors? |
| Complete HF training loop - read/watch | https://huggingface.co/learn/llm-course/chapter3/4?fw=pt | What moves from batch to model to loss to optimizer? |
| Embedding input/output | https://docs.pytorch.org/docs/2.7/generated/torch.nn.Embedding.html | What does an embedding look up, and what type is an index? |
| Classification loss | https://docs.pytorch.org/docs/2.7/generated/torch.nn.CrossEntropyLoss.html | Shapes/dtypes for class indices versus probability targets |
| Tensor dimensions | https://docs.pytorch.org/docs/2.7/generated/torch.Tensor.squeeze.html | What happens when batch size is one? |
| Optimizers | https://docs.pytorch.org/docs/2.7/optim.html | Which parameter objects does an optimizer own? |
| PyTorch gradients - read/watch | https://docs.pytorch.org/tutorials/beginner/introyt/autogradyt_tutorial.html | Gradient tracking, gradients and parameter updates |
| Debugging | https://docs.python.org/3/library/pdb.html | Step into helpers and inspect their locals |

HF course and PyTorch intro pages include videos. PyTorch reference links use version 2.7 to
match the primary tested environment; Intel Mac uses the compatible 2.2.2 package route.

## Inspection questions after attempting
1. Inspect raw CSV labels, dataset label values, token IDs, masks and class scores. Which are
   indices and which are continuous values? State each tensor's shape, dtype and device.
2. What differs between [B], [B,1] and a scalar? Show the difference when B=1.
3. Is a nonzero gradient sufficient evidence that a parameter was updated? Explain your evidence.
4. When is updating only a classifier a valid design, and what does this question's contract ask for?
5. What does a saved checkpoint reload prove, and what remains untested about model quality?
6. What assumptions did you clarify before implementing last-message selection?

Keep this practice focused on data preparation and debugging. System design, EDA, distributed
training and hyperparameter searches belong outside this first-screen block.
