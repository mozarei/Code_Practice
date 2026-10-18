# Hints: Selection and last matching records

## Problem 1

Hint 1: Last in list order is different from maximum timestamp.
Hint 2: A forward scan can overwrite a saved match; a reversed scan can stop at the first match.

## Problem 2

Hint 1: Decide whether "latest" means position or timestamp.
Hint 2: Initialize to None, not timestamp zero. A >= comparison can implement the tie rule.

## Problem 3

Hint 1: Truthiness is not the same as missingness.
Hint 2: Compare to None with identity rather than using if value.
