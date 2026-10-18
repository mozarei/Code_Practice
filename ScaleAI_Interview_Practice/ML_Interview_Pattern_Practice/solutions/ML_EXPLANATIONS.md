# ML root causes - open after attempting the selected set
## 01_batch_inputs
1. A tokenizer expects strings; pass text fields, not full record dictionaries.
2. An embedding expects integer token indices; retain long input_ids.
3. Same-shaped all-one masks are semantically wrong when IDs contain padding.
   Keep the tokenizer's correct attention_mask.
## 02_outputs_targets
1. The Hugging Face ModelOutput object is not the raw tensor expected by the loss;
   use its logits field.
2. Class-index targets here are long [B], not float [B].
3. unsqueeze then unrestricted squeeze collapses B=1 to a scalar. Labels already
   have the intended [B] shape; leave them alone. For actual [B,1], squeeze(-1)
   removes only the known trailing dimension.
## 03_autograd
1. Detaching the loss disconnects backward; detach a logging copy instead.
2. Clearing gradients after backward and before step discards the work.
3. A frozen encoder contradicts this full-fine-tuning contract. Enable its
   parameters before forward. Changing requires_grad does not clear stale grads.
## 04_optimizer
1. deepcopy creates another model with different parameter objects. Optimize
   the model that actually ran forward/backward.
2. Classifier-only selection omits the encoder; select all required parameters.
   An omitted but unfrozen encoder can still receive and accumulate gradients.
3. Zero LR prevents gradient-based updates. Respect the supplied LR argument;
   do not tune it. Inspect actual param_groups rather than assuming settings.
## 05_representations
1. Truncation limits length, but padding makes mixed-length tensors rectangular.
2. Reducing [B,L,H] over H leaves [B,L], which the existing [C,H] head cannot use.
   Preserve this pretrained classifier's pooled [B,H] representation.
3. detach shares storage: the supposed before snapshot changes with the live
   parameter. Use detach().clone() for a disconnected independent snapshot.
   detach on the live after value is fine for measurement; do not remove every
   detach indiscriminately. Its location and intended role determine correctness.

Reference checks: python check_ml.py --set NAME --solution.
These examples concern specific toy contracts. Frozen encoders, head-only training
and detached logging tensors can be intentional in other applications.
