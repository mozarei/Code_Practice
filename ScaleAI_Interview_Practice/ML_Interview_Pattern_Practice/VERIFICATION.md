# Verification performed

Executed on Linux CPU, Python 3.12. Package versions (torch / transformers / NumPy): 2.7.1+cpu 4.57.1 2.2.6.

- 18 Python reference problems passed all 86 behavior scenarios, including Unicode,
  strict types, stable ordering, label zero, singleton chunks, joins and unmodified inputs.
- Untouched Python starters correctly fail until implemented.
- All 15 ML failure stages were reproduced in the intended order across five folders.
  Each minimal repair exposed the next defect; every repaired candidate matched its reference.
- All five repaired candidates passed fresh-code checks: six updates / 18 visits for
  nine CSV records, both final B=1 batches, finite gradients/losses, live optimizer
  membership/settings, persisted encoder/head changes, mixed-length B=1/4 batches,
  independent snapshot storage and checkpoint reload/forward equivalence.
- A shape-only pooling workaround was rejected for changing the required classifier path.
- Real pretrained BERT shape example executed: B=2, L=10, H=128, C=2, V=30522;
  embeddings/hidden states, pooled vectors, logits, labels, scalar loss and gradients
  were inspected, including B=1 and detach/clone storage identity.
- Live terminal pdb was tested by pausing, printing a label shape and gradient state,
  continuing and completing the example.
- Reference demo waits for a prediction and can stop before revealing outputs.
- Converter template checked for required flags/help, sorted files, nested output
  directories, Unicode/quotes/newlines, friendly stderr and output preservation on
  invalid inputs. Working pattern examples executed. All 90 Python files compiled.
- One-page command sheet and three-page guide rendered; every page visually inspected.

macOS, Windows, browser Codespaces and the graphical VS Code debugger were not executed.
The Intel macOS dependency pins are inherited from the earlier pack, not newly tested here.
No accuracy or loss-decrease criterion was used. Fixtures are synthetic learning data.
Package installation needs internet; all exercise model/tokenizer loads use bundled files.
The shared harness provides explicit teaching diagnostics; actual interview checks can differ.
