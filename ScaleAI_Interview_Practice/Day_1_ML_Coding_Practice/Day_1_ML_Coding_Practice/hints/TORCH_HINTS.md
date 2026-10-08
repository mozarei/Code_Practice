# Optional PyTorch route: open one hint at a time

First failure: compare the parser's argument names with the attribute used by its caller.
Next failure: inspect logits and label shapes/types against the loss-function contract.
Final failure: inspect gradients immediately after backward and immediately before the step.
Record assistance. Ask for a deeper hint only after demonstrating what you inspected.
