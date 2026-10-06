# Verification completed before delivery

- Python 3.12.14, PyTorch 2.7.1+cpu, Transformers 4.57.1; Linux CPU.
- All 14 Python sources compiled; VS Code launch JSON parsed. GUI launch was not exercised.
- The bundled offline checkpoint passed a tokenizer/model forward smoke test independently of candidate code.
- Reference converter passed 23 behavioral scenarios plus CLI help. Its full output contained 24 rows.
- A fresh copy of the candidate repository exposed all three intended failures in sequence.
  Each reference repair was applied independently; no fourth setup or training failure remained.
- Repaired candidate training completed 2 epochs, 12 optimizer updates and 48 visited examples.
- Losses were finite. Tracked encoder/head changes were {"encoder": 0.0011125914752483368, "classifier": 0.0009025838226079941}.
- The training completion checker passed, including offline model/tokenizer reload and finite [2,2] logits.
- An independent comparison of saved weights confirmed encoder and classifier weights changed.
- Three additional batch-contract checks covered single/variable batches and truncation of a long input.
- Runtime verification set HF_HUB_OFFLINE and TRANSFORMERS_OFFLINE; no model download was needed.
- The source checkpoint revision is recorded in models/bert-tiny/PROVENANCE.json; the loaded
  encoder query weights were checked against the upstream checkpoint before packaging.
- Additional compatibility run: PyTorch 2.2.2+cpu, NumPy 1.26.4, Transformers 4.57.1 on Linux
  passed offline setup, full reference fine-tuning and checkpoint completion/reload checks.
  This validates the package combination used for Intel Macs, not macOS hardware behavior.
- macOS/Windows installation and VS Code GUI behavior were not runtime-tested here.

Candidate files remain intentionally unfinished/broken. Training/checkpoint checks establish
pipeline execution, not model accuracy, generalization or a hiring outcome.
