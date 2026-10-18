def last_final(reviews, document_id):
    """Return the LAST review in input order matching document_id and status="final". A later draft does not cancel it. Return None if absent. Inputs are valid objects; compare IDs exactly."""
    raise NotImplementedError("Problem 1: implement this small transformation")


def latest_final(reviews, document_id):
    """Return the matching FINAL review with greatest integer timestamp. Break timestamp ties by the later input occurrence. Negative timestamps are valid. Return None if absent; input order need not be chronological."""
    raise NotImplementedError("Problem 2: implement this small transformation")


def first_non_none(values):
    """Return the first value that is not None. Zero, False, empty string and empty containers are valid results. Return None if there is no such value."""
    raise NotImplementedError("Problem 3: implement this small transformation")
