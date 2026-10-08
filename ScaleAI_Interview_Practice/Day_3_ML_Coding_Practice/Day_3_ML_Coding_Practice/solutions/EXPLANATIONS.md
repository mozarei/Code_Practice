# Reference repairs - open only after attempting

1. collation.py passes a list of record dictionaries to the tokenizer. Extract each record's
   text string. Keep labels separately as a torch.long tensor. This is an input-type contract
   failure before the model runs.
2. model.py returns a SequenceClassifierOutput object while train.py expects a logits tensor
   for CrossEntropyLoss. Return outputs.logits. Alternatively callers could consistently use
   the HF output fields, but that would change this wrapper's stated interface.
3. train.py detaches the training loss before backward(). Its number is finite but it has no
   gradient graph. Use the original loss for backward and detach only a logging copy. Merely
   setting requires_grad on the detached tensor does not reconnect it to model parameters.

The corrected files are in this folder. Every deliberate candidate defect is a small change
to its reference file. data.py is shared and correct. Do not edit library source or checks.

## Reference verification commands, from the project root
```bash
python solutions/convert.py --input-dir fixtures/raw --output-csv output/reference.csv
python tools/check_converter.py --script solutions/convert.py
python solutions/train.py --csv output/reference.csv --output-dir output/reference_run
python tools/check_training.py --csv output/reference.csv --run-dir output/reference_run
```

Encoder weights are pretrained; the classification head was newly initialized before this
exercise. Updating both is genuine fine-tuning, though this tiny synthetic dataset does not
establish prediction quality. Successful training verifies finite calculations and parameter
updates; reloading verifies artifact compatibility. Neither establishes generalization.

## Examples of interview explanations
"The tokenizer received dictionaries. It needs a batch of strings, so I extracted the text
field and kept the labels separate."
"The wrapper returned the full model output. The loss function needs raw score tensors, so
I returned the logits field."
"The loss was detached before backpropagation. I preserved the training graph and detached
only the logging value. The rerun shows encoder and classifier weights changed."
