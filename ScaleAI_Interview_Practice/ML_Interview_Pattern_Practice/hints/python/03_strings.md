# Hints: Immutable strings and precise text assembly

## Problem 1

Hint 1: Strings do not support text[index] = character.
Hint 2: Combine the unchanged prefix, replacement and unchanged suffix using slices.

## Problem 2

Hint 1: The method for a literal replacement differs from a regex.
Hint 2: Inspect the optional count argument of str.replace.

## Problem 3

Hint 1: strip removes outer whitespace; split/join can unintentionally change interior spaces.
Hint 2: Validate types first, build cleaned nonblank parts, then join with a newline.
