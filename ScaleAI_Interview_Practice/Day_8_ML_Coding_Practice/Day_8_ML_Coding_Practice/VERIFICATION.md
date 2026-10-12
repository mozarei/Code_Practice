# Verification performed

Executed on Linux CPU with Python 3.12. Main packages: 2.7.1+cpu 4.57.1 2.5.3.

- 19 Python source files compiled; VS Code launch JSON and input JSON fixtures parsed.
- Reference converter passed 35 scenarios plus command-line help.
- All three original failures reproduced sequentially at 0, 0 and 16 logged steps.
- Independently compared source/reference: exactly one changed line in batching.py,
  model.py and optim.py; remaining training source matches the reference.
- Repaired candidate completed 16 updates / 58 visits for 29 rows, with both final B=1 batches.
- Fresh-code checker independently verified metrics, persisted encoder/head changes,
  optimizer parameter-object membership, complete finite gradients, mixed-length B=1/4,
  intended pretrained forward, reload equivalence and padding robustness.
- Broken current source still failed when stale successful checkpoint/metrics were present.
- A dimension-only mean-pooling workaround was rejected for changing the specified architecture.
- Fresh end-to-end checker also passed datasets of 1, 5 and 8 records.
- Four-page printable guide rendered and every page visually reviewed.

Intel macOS package pins are retained from Day 6: torch 2.2.2 and NumPy 1.26.4.
The private compatibility runtime could not execute successfully in this task;
no successful Day 8 run with torch 2.2.2 is claimed. Main verification used torch 2.7.1.
macOS, Windows, browser Codespaces and the VS Code graphical debugger were not executed.
No accuracy or loss-reduction threshold was used. Installation needs internet;
all exercise tokenizer/model loads use bundled local files and CPU.
