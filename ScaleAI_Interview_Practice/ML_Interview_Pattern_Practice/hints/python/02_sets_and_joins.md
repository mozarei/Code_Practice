# Hints: Sets, dictionaries and stable joins

## Problem 1

Hint 1: A set gives membership, but the output needs an ordered list.
Hint 2: Add a value to the output only the first time it enters seen.

## Problem 2

Hint 1: Build a lookup from ID to last final label.
Hint 2: Test key membership; if lookup[id] wrongly discards label zero. Emit by walking documents, not reviews.

## Problem 3

Hint 1: You need fast membership for both known and already-reported IDs.
Hint 2: Keep the result list separate from those sets.
