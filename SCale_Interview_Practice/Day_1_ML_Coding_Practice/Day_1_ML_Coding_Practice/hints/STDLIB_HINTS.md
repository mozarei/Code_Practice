# Open one hint at a time, only when needed

## First failure
Level 1: Inspect the CSV header and one parsed row before assuming its keys.
Level 2: Compare the documented consumer contract with the key used by the data reader.

## Next failure
Level 1: At the failed operation, inspect the size of each object and where it was created.
Level 2: Compare the number of model parameters with the number of feature values.

## Final failure
Level 1: Inspect a weight and a gradient before and after one update. What should the update do?
Level 2: Try a tiny positive step and compare loss before and after it; examine the update rule.

Record which hint you used. These hints do not count as an independent solve.
