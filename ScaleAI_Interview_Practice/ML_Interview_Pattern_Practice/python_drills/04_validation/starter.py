def keep_records(records):
    """Keep every record except those whose skip field is exactly boolean True. Missing, None, False, integer 1 and string "true" are retained. Records are valid dictionaries."""
    raise NotImplementedError("Problem 1: implement this small transformation")


def integer_label(value):
    """Return value only if its actual type is int and it is 0 or 1. Reject booleans, floats, strings, None and other integers with ValueError."""
    raise NotImplementedError("Problem 2: implement this small transformation")


def field_state(record, key):
    """Return "missing" if key absent, "null" for None, "empty" for the exact empty string, otherwise "value". Zero, False, whitespace strings and empty lists are values."""
    raise NotImplementedError("Problem 3: implement this small transformation")
