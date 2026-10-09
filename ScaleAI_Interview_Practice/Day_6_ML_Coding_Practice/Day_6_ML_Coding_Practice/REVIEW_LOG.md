# Day 6 review log
Started: ____  Finished: ____  Interpreter/version: ____
Converter minutes: ____  Debugging minutes: ____  Hint count: ____

## For each lab
| Topic | Prediction | Observation | Why different? | Exercise passed? |
|---|---|---|---|---|
| 1-3: structure/graph | | | | |
| 4: backward | | | | |
| 5: optimizer | | | | |
| 6: clearing | | | | |
| 7: freezing | | | | |
| 8-9: contracts | | | | |
| 10-11: debug/loop | | | | |

## For each failure
Command and full error: ____
Project line/boundary: ____
Expected type/shape/dtype/device: ____
Observed values: ____
Hypothesis BEFORE editing: ____
Smallest repair: ____
Verification and remaining uncertainty: ____

## Can I explain this without notes?
- requires_grad vs grad vs optimizer membership vs actual weight change
- Why backward alone does not update weights
- Why a head-only optimizer does not clear excluded encoder gradients
- Frozen encoder vs encoder with gradients but no optimizer ownership
- no_grad vs eval; detach vs moving to CPU; detach vs detach().clone()
- Class-index labels at batch size one

## English practice
Original sentence: ____
Improved sentence preserving my tone: ____
Repeat aloud: "I expected ____, but observed ____. I will inspect ____."
Next measurable goal (one): ____
