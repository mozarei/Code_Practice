from collections import defaultdict

def flatten_paragraphs(documents):
    rows=[]
    for document in documents:
        for paragraph in document['paragraphs']:
            text=paragraph.strip()
            if text:rows.append({'document_id':document['id'],'text':text,'label':document['label']})
    return rows


def chunks(items, size):
    if type(size) is not int or size<=0:raise ValueError('Positive integer size required')
    return [items[start:start+size] for start in range(0,len(items),size)]


def rows_per_export(exports):
    rows=[]
    for export in exports:
        latest={}
        for review in export['reviews']:
            if review['status']=='final':latest[review['document_id']]=review['label']
        for document in export['documents']:
            if document['id'] in latest:rows.append([document['text'],latest[document['id']]])
    return rows
