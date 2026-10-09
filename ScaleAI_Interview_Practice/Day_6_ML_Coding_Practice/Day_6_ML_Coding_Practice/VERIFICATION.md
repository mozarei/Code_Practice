# Verification performed

Executed on Linux CPU with Python 3.12; packages: 2.7.1+cpu 4.57.1 2.5.3.
Also executed the compatibility combination torch 2.2.2+cpu / NumPy 1.26.4 /
transformers 4.57.1 on Linux, matching the Intel macOS dependency pins.

- 68 Python source files compiled; VS Code launch JSON parsed.
- All eleven lesson demonstrations executed; expected exception demos caught their failures.
- All eleven reference coding exercises passed behavioral checks, including repeated steps and B=1.
- Interactive runner tested: prediction prompt, failed-exercise gate, and explicit choice before advancing.
- Converter reference passed 26 input/error scenarios plus command-line help.
- Three mock failures reproduced sequentially at 0, 5 and 12 logged steps.
- Repaired candidate completed 12 updates / 42 example visits, including both final B=1 batches.
- Independent fresh-code checker verified persisted encoder/head weight changes, offline reload,
  finite logits and B=1/4 batch/loss contracts. Original broken code still failed with stale correct output.
- Six independent original drills failed; all six reference repairs passed repeated B=3/1 runs.
- Compatibility environment ran all demos/exercises, reference fresh mock and six repaired drills.
- Local pretrained model/tokenizer load offline. Setup installation itself requires internet.

macOS, Windows, browser Codespaces, and the VS Code graphical debugger were not executed here.
Terminal pdb uses the standard built-in debugger; exact loss values/errors can differ by version.
No accuracy or loss-decrease requirement was used. Fixtures are synthetic interview practice.
