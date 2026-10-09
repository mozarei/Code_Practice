# Review answers - open after investigating

## Mock stage 1: model input name
batching.py renames input_ids to token_ids. TicketClassifier.forward accepts
input_ids, not token_ids. Preserve the tokenizer's original key. Correct
values, shapes and dtypes do not compensate for an incompatible keyword name.

## Mock stage 2: batch-size-one target shape
objective.py applies labels.unsqueeze(-1).squeeze(). For B=4 it restores [4];
for B=1 it collapses [1,1] to a scalar. Cross-entropy still receives batched
logits [1,2], so targets must be [1]. Here labels are already [B]: use them
unchanged. squeeze(-1) is appropriate if your actual input is [B,1], but the
correct fix must follow the input contract rather than blindly adding it.

## Mock stage 3: encoder disconnected from autograd
model.py runs self.backbone.bert inside torch.no_grad(). Head operations
outside that block remain tracked, so loss/backward succeed and the classifier
updates. Encoder parameters still have requires_grad=True and belong to the
full optimizer, but have no gradients from that forward. Their weights stay
unchanged and the full-fine-tuning check fails.
Remove that disabling context for training. The reference uses nullcontext(),
which leaves ambient gradient mode unchanged and still respects an outer
no_grad() during inference. Do not wrap every forward in enable_grad(): that
would override callers intentionally disabling gradients during evaluation.

## Six short drills
01: float token IDs -> retain integer IDs for embedding lookup.
02: [B,1] targets -> retain class-index targets [B].
03: detached loss -> backward the original tracked loss; detach only a logging copy.
04: frozen backbone -> enable it for THIS full-fine-tuning contract, before forward.
05: head-only optimizer -> pass model.parameters() for full fine-tuning.
06: zero_grad between backward and step -> clear before forward/backward instead.
Every reference drill uses the same correct base loop; each original differed
in one concept. That repetition is deliberate reinforcement.

## Reference verification commands
These reveal answers through executed reference code; use after your attempt.

```bash
python run_labs.py --lesson 5 --check --exercise-dir solutions/exercises
python solutions/convert.py --input-dir fixtures/raw --output-csv output/reference.csv
python tools/check_converter.py --script solutions/convert.py
python solutions/train.py --csv output/reference.csv --output-dir output/reference_run
python tools/check_training.py --train-script solutions/train.py --csv output/reference.csv
python tools/check_debugging.py --file solutions/debugging/case_01.py
```

## Explain the fix in natural English
"The backbone received gradients, but the optimizer did not manage its parameters."
"The encoder was included in the optimizer, but its forward pass was not tracked."
"Backward calculated gradients; step used them to update the weights."
"The final batch has one example, and squeeze removed the batch dimension."
"I verified the repair with a fresh run and independent weight snapshots."
