def replace_span(text, start, end, replacement):
    """Return a NEW string replacing the half-open range [start,end). Require 0 <= start <= end <= len(text), otherwise raise ValueError. Python string indices count Unicode code points, not UTF-8 bytes."""
    raise NotImplementedError("Problem 1: implement this small transformation")


def replace_first(text, old, new):
    """Replace only the first LITERAL occurrence of nonempty old. Return unchanged text when absent; reject empty old with ValueError. Dots and brackets are literal characters, not regex syntax."""
    raise NotImplementedError("Problem 2: implement this small transformation")


def assemble_text(title, paragraphs):
    """Title must be a nonblank string and paragraphs a list of strings. Trim only outer whitespace, discard blank paragraphs, require at least one nonblank paragraph. Return title + newline + paragraphs joined by newline. Preserve internal whitespace and punctuation; raise ValueError for invalid input."""
    raise NotImplementedError("Problem 3: implement this small transformation")
