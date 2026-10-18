# Hints: Ordering contracts and grouping

## Problem 1

Hint 1: Read the requested ordering before choosing a sort key.
Hint 2: Use a tuple key: parsed integer first, full filename second.

## Problem 2

Hint 1: Python sorting is stable.
Hint 2: Map severity to a numeric rank, give unknown severities the same fallback rank, and do not add a tie key.

## Problem 3

Hint 1: Each category needs its own list.
Hint 2: defaultdict(list) or setdefault(key,[]) avoids repeated membership branches. Avoid sharing one mutable list across keys.
