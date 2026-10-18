def stable_unique(identifiers):
    """Return unique string IDs in first-occurrence order. Do not sort and do not mutate the input."""
    raise NotImplementedError("Problem 1: implement this small transformation")


def attach_labels(documents, reviews):
    """Join valid documents {id,text} to the last FINAL review {document_id,status,label}. Return [text,label] rows in document order; skip documents with no final review and ignore unknown IDs. Label 0 must be retained."""
    raise NotImplementedError("Problem 2: implement this small transformation")


def unknown_ids(known_ids, reviews):
    """Return unknown document IDs from reviews, once each in first-occurrence order. known_ids is a list of strings; each review has document_id."""
    raise NotImplementedError("Problem 3: implement this small transformation")
