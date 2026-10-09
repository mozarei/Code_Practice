# Mock hints - first level (open only for the current failure)
Stage 1: Inspect the keys the collator returns and the forward signature.
Stage 2: Compare the last batch's label shape with earlier batches.
Stage 3: Loss logs alone are insufficient. Inspect a tracked encoder parameter's
requires_grad, grad, optimizer membership and before/after value separately.
