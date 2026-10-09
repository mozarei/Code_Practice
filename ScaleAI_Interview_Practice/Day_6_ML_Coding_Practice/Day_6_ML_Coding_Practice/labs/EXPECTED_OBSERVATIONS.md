# Compare after making predictions

Exact floating values may differ slightly between versions. Compare the
states, shapes and invariants, not identical loss decimals. Lesson prints
are the live results of code you can edit and rerun.

| Lesson | Main observation |
|---|---|
| 1 | Parent exposes 4 parameter tensors, backbone 2, head 2. Parent has 0 direct parameter tensors. There are 17 scalar parameter values in total. |
| 2 | Trainable parameters begin with grad=None. Connected parameters get gradients after backward; unused parameter remains None. Clearing restores None. |
| 3 | Tracked logits/loss have a grad_fn. Detached loss has none and cannot backward. eval alone does not disable gradients. |
| 4 | w=2, x=3, target=1: loss=25, grad=30, w remains 2 after backward; SGD lr=.1 changes w to -1. |
| 5 | Full optimizer: backbone and head update. Head-only optimizer: backbone has gradients but zero weight change. AdamW state is allocated on its first applicable step. |
| 6 | w=2 with loss=w^2: gradients 4 then 8 without clearing. False zeroes an existing gradient; True removes it. A head-only optimizer leaves excluded backbone gradients untouched. |
| 7 | Full: encoder grad and update. Unfrozen head-only: encoder grad, no update. Frozen: encoder grad=None and no update; head updates. |
| 8 | squeeze on [1,1] becomes scalar; squeeze(-1) becomes [1]. Class-index labels must have the intended vector shape and long dtype. |
| 9 | Embedding output [B,L,4]. Integer IDs select rows. Float IDs fail. IDs do not need gradients; embedding weights do. |
| 10 | Dataset dict -> batch dict -> logits [B,2] -> scalar loss -> parameter gradients -> weight changes. Both full and partial batches work. |
| 11 | Forward/loss build a graph; backward fills grads; step changes weights and AdamW state; the next zero_grad clears grads, not weights. |

Try changes only in a disposable copy of a lab, not the mock checks:
- Set learning rate to zero in lesson 5; compare nonzero gradients with zero updates.
- Use model.zero_grad instead of head_optimizer.zero_grad in lesson 6.
- Add a fresh forward and backward after clearing; inspect the new buffers.
- In lesson 8, try B=2, B=1 and B=4; predict every intermediate shape.
- In lesson 11, print optimizer.state for one parameter after step.

Exercises are separate from the demos. Passing a demo is not proof you can
implement the concept; use each task file and explain your implementation.
