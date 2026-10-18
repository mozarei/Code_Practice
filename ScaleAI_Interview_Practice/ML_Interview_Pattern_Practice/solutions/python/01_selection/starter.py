from collections import defaultdict

def last_final(reviews, document_id):
    selected=None
    for review in reviews:
        if review['document_id']==document_id and review['status']=='final':
            selected=review
    return selected


def latest_final(reviews, document_id):
    selected=None
    for review in reviews:
        if review['document_id']!=document_id or review['status']!='final':continue
        if selected is None or review['timestamp']>=selected['timestamp']:
            selected=review
    return selected


def first_non_none(values):
    for value in values:
        if value is not None:return value
    return None
