from collections import defaultdict

def sort_export_names(names):
    return sorted(names,key=lambda name:(int(name.split('_',1)[0]),name))


def sort_tickets(tickets):
    rank={'critical':0,'high':1,'normal':2}
    return sorted(tickets,key=lambda ticket:rank.get(ticket['severity'],3))


def group_texts(records):
    groups=defaultdict(list)
    for record in records:groups[record['category']].append(record['text'])
    return dict(groups)
