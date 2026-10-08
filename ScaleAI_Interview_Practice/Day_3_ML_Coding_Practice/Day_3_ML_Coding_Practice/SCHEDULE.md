# Two sessions, then one fresh replay

Session A (180 minutes) is in README.md: 15 clarification, 60 converter, 20 CSV checks,
70 debugging, 15 explanation/log. Record actual times, including time reading documentation.

Session B (up to 180 minutes):
| Minutes | Work |
|---|---|
| 0-15 | Explain yesterday's failure and hypothesis without looking at the answer |
| 15-90 | Continue the remaining debugging failures; inspect before changing code |
| 90-115 | Run completion checks; reload the checkpoint; explain what was verified |
| 115-145 | Finish converter edge cases and read only the docs tied to your gaps |
| 145-165 | Reproduce the most difficult repair; explain cause, fix and evidence |
| 165-180 | Update the log and choose one measurable next target |

If already finished, shorten Session B and do the fresh replay. No need to fill time with
unrelated topics. If unfinished, record the next concrete step and continue another session.

Fresh replay (60 minutes, setup already complete): Part 1 for 20 minutes; once the CSV works,
move to Part 2. Use the fallback CSV if needed at the boundary. Debug for the remaining
40 minutes. Stop the clock, record evidence and hints used, then resume open-book review.
Do not add robustness checks before delivering the base CSV if they consume debugging time.

Baseline to beat: approximately 180 converter minutes. Initial learning goal: one working
converter within 60 minutes, then a replay toward 30, 20 and finally 15 minutes. These are
practice targets; missing a target means repeat the relevant skill, not skip learning.
