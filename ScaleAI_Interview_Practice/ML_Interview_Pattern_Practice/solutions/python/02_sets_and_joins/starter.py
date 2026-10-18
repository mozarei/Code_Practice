from collections import defaultdict

def stable_unique(identifiers):
    seen=set();result=[]
    for identifier in identifiers:
        if identifier not in seen:
            seen.add(identifier);result.append(identifier)
    return result


def attach_labels(documents, reviews):
    latest={}
    for review in reviews:
        if review['status']=='final':latest[review['document_id']]=review['label']
    return [[doc['text'],latest[doc['id']]] for doc in documents if doc['id'] in latest]


def unknown_ids(known_ids, reviews):
    known=set(known_ids);reported=set();result=[]
    for review in reviews:
        identifier=review['document_id']
        if identifier not in known and identifier not in reported:
            reported.add(identifier);result.append(identifier)
    return result
