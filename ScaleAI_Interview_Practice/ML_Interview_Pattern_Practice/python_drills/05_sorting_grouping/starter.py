def sort_export_names(names):
    """Names are valid filenames beginning with a positive integer then underscore. Sort by numeric prefix, breaking numeric ties by the full filename lexicographically. This practice contract deliberately differs from ordinary filename sorting."""
    raise NotImplementedError("Problem 1: implement this small transformation")


def sort_tickets(tickets):
    """Sort valid ticket objects by severity: critical, high, normal, then any unknown severity. Preserve original order among equal-priority tickets, including different unknown values. Do not sort ties by ID."""
    raise NotImplementedError("Problem 2: implement this small transformation")


def group_texts(records):
    """Group valid {category,text} records into a plain dictionary category -> list of texts. Preserve text order and duplicates within each group. Include only categories seen in input."""
    raise NotImplementedError("Problem 3: implement this small transformation")
