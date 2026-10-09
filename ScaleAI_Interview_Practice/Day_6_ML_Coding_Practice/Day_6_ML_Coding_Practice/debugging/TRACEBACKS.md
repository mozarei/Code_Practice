# Captured starter failures for the independent drills

Run the code yourself first if possible. Paths are normalized; package versions
can change exact exception wording. No repairs are included here.

## Case 01

```text
Traceback (most recent call last):
  File "Day_6_ML_Coding_Practice/debugging/case_01.py", line 17, in <module>
    if __name__=='__main__':run_case(build,prepare,update)
                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "Day_6_ML_Coding_Practice/debugging/common.py", line 24, in run_case
    loss=update(model,optimizer,inputs,targets)
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "Day_6_ML_Coding_Practice/debugging/case_01.py", line 12, in update
    logits=model(**inputs)
           ^^^^^^^^^^^^^^^
  File "/workspace/scratch/ab0bf07ae82f/day3_runtime/lib/python3.12/site-packages/torch/nn/modules/module.py", line 1751, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/workspace/scratch/ab0bf07ae82f/day3_runtime/lib/python3.12/site-packages/torch/nn/modules/module.py", line 1762, in _call_impl
    return forward_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "Day_6_ML_Coding_Practice/debugging/common.py", line 9, in forward
    tokens=self.backbone(input_ids)
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/workspace/scratch/ab0bf07ae82f/day3_runtime/lib/python3.12/site-packages/torch/nn/modules/module.py", line 1751, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/workspace/scratch/ab0bf07ae82f/day3_runtime/lib/python3.12/site-packages/torch/nn/modules/module.py", line 1762, in _call_impl
    return forward_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/workspace/scratch/ab0bf07ae82f/day3_runtime/lib/python3.12/site-packages/torch/nn/modules/sparse.py", line 190, in forward
    return F.embedding(
           ^^^^^^^^^^^^
  File "/workspace/scratch/ab0bf07ae82f/day3_runtime/lib/python3.12/site-packages/torch/nn/functional.py", line 2551, in embedding
    return torch.embedding(weight, input, padding_idx, scale_grad_by_freq, sparse)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
RuntimeError: Expected tensor for argument #1 'indices' to have one of the following scalar types: Long, Int; but got torch.FloatTensor instead (while checking arguments for embedding)

```

## Case 02

```text
Traceback (most recent call last):
  File "Day_6_ML_Coding_Practice/debugging/case_02.py", line 17, in <module>
    if __name__=='__main__':run_case(build,prepare,update)
                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "Day_6_ML_Coding_Practice/debugging/common.py", line 24, in run_case
    loss=update(model,optimizer,inputs,targets)
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "Day_6_ML_Coding_Practice/debugging/case_02.py", line 13, in update
    loss=F.cross_entropy(logits,targets)
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/workspace/scratch/ab0bf07ae82f/day3_runtime/lib/python3.12/site-packages/torch/nn/functional.py", line 3494, in cross_entropy
    return torch._C._nn.cross_entropy_loss(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
RuntimeError: 0D or 1D target tensor expected, multi-target not supported

```

## Case 03

```text
Traceback (most recent call last):
  File "Day_6_ML_Coding_Practice/debugging/case_03.py", line 17, in <module>
    if __name__=='__main__':run_case(build,prepare,update)
                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "Day_6_ML_Coding_Practice/debugging/common.py", line 24, in run_case
    loss=update(model,optimizer,inputs,targets)
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "Day_6_ML_Coding_Practice/debugging/case_03.py", line 14, in update
    loss.backward()
  File "/workspace/scratch/ab0bf07ae82f/day3_runtime/lib/python3.12/site-packages/torch/_tensor.py", line 648, in backward
    torch.autograd.backward(
  File "/workspace/scratch/ab0bf07ae82f/day3_runtime/lib/python3.12/site-packages/torch/autograd/__init__.py", line 353, in backward
    _engine_run_backward(
  File "/workspace/scratch/ab0bf07ae82f/day3_runtime/lib/python3.12/site-packages/torch/autograd/graph.py", line 824, in _engine_run_backward
    return Variable._execution_engine.run_backward(  # Calls into the C++ engine to run the backward pass
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
RuntimeError: element 0 of tensors does not require grad and does not have a grad_fn

```

## Case 04

```text
Traceback (most recent call last):
  File "Day_6_ML_Coding_Practice/debugging/case_04.py", line 18, in <module>
    if __name__=='__main__':run_case(build,prepare,update)
                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "Day_6_ML_Coding_Practice/debugging/common.py", line 30, in run_case
    assert parameter.requires_grad, f'Full fine-tuning requires trainable {name}'
           ^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: Full fine-tuning requires trainable backbone.weight

```

## Case 05

```text
Traceback (most recent call last):
  File "Day_6_ML_Coding_Practice/debugging/case_05.py", line 17, in <module>
    if __name__=='__main__':run_case(build,prepare,update)
                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "Day_6_ML_Coding_Practice/debugging/common.py", line 32, in run_case
    assert not torch.equal(before[name],parameter.detach()), f'Weight did not update: {name}'
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: Weight did not update: backbone.weight

```

## Case 06

```text
Traceback (most recent call last):
  File "Day_6_ML_Coding_Practice/debugging/case_06.py", line 18, in <module>
    if __name__=='__main__':run_case(build,prepare,update)
                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "Day_6_ML_Coding_Practice/debugging/common.py", line 31, in run_case
    assert parameter.grad is not None and torch.isfinite(parameter.grad).all(), f'Missing/invalid gradient: {name}'
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: Missing/invalid gradient: backbone.weight

```
