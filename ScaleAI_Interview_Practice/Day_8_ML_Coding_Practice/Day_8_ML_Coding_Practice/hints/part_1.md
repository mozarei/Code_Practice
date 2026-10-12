# Part 1 staged hints - stop after the first useful hint
Level 1: Keep document order separate from how you look up review decisions.
Level 2: Process reviews in order; overwrite a stored decision only for final reviews.
Level 3: Build a per-file ID set and latest-final dictionary, then walk the original
document order. Reinitialize those structures for each export. Validate before writing.
