"""Working small examples to read and run. These are reference examples, not graded tasks."""
def main():
    reviews=[{'id':'a','status':'final','label':1},
             {'id':'a','status':'final','label':0},
             {'id':'a','status':'draft','label':1}]
    latest={}
    for review in reviews:
        if review['status']=='final':latest[review['id']]=review['label']
    print('Last FINAL label remains zero:',latest)
    print('Key present:', 'a' in latest, 'value truthy:',bool(latest['a']))
    # Set for membership, list for output order.
    seen=set();ordered=[]
    for identifier in ['b','a','b']:
        if identifier not in seen:seen.add(identifier);ordered.append(identifier)
    print('Stable unique:',ordered)
    text='abcdef';modified=text[:2]+'XY'+text[4:]
    print('Original immutable string:',text,'replacement:',modified)
    print('Literal first replacement:','a.b a.b'.replace('a.b','X',1))
    print('Lexicographic:',sorted(['10_x','2_x','1_x']))
    print('Numeric key:',sorted(['10_x','2_x','1_x'],key=lambda s:int(s.split('_')[0])))
    print('True == 1:',True==1,'type(True) is int:',type(True) is int)
    zero=0
    print('None / blank / zero:',None is None,''=='',zero is None)
if __name__=='__main__':main()
