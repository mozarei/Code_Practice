import argparse
import copy
import csv
import subprocess
import sys
from pathlib import Path
from check_helpers import ROOT,run_cases
def item(title='A',paragraphs=None,routing='normal',**extra):
    return {'payload':{'title':title,'paragraphs':['B'] if paragraphs is None else paragraphs},'routing':routing,**extra}
def wrap(items):return {'tickets':items}
def cases():
    files={str(p.relative_to(ROOT/'fixtures/raw')):p.read_text(encoding='utf-8')
           for p in (ROOT/'fixtures/raw').rglob('*') if p.is_file()}
    with (ROOT/'fixtures/reference_train.csv').open(encoding='utf-8',newline='') as f:rows=list(csv.reader(f))[1:]
    h=['text','label'];result=[('base',{'files':files,'expected':rows,'header':h})]
    positives=[
        ('sort and label mapping',{'z.json':wrap([item('Z',routing='review')]),'a.json':wrap([item()])},[['A\nB','0'],['Z\nB','1']]),
        ('trim and blank paragraph filtering',{'a.json':wrap([item(' T ',[' x ','  ',' y\nz '])])},[['T\nx\ny\nz','0']]),
        ('escaping and Unicode',{'a.json':wrap([item('Résumé, "test"',['سلام  keep  spaces','a\nb'])])},[['Résumé, "test"\nسلام  keep  spaces\na\nb','0']]),
        ('duplicates preserved',{'a.json':wrap([item(),item()])},[['A\nB','0']]*2),
        ('strict synthetic flag',{'a.json':wrap([{'synthetic':True},item(synthetic=1),item(synthetic='true'),item(synthetic=False),item(synthetic=None)])},[['A\nB','0']]*4),
        ('ignore unrelated paths',{'a.json':wrap([item()]),'note.txt':'bad','nested/no.json':'bad','folder.json/note.txt':'bad'},[['A\nB','0']]),
        ('empty alongside valid',{'a.json':wrap([]),'b.json':wrap([item()])},[['A\nB','0']]),
    ]
    result += [(name,{'files':files,'expected':rows,'header':h}) for name,files,rows in positives]
    bad_payload=item();bad_payload['payload']=None
    bad_title=item();bad_title['payload']['title']=123
    missing_routing=item();del missing_routing['routing']
    invalids=[
        ('top-level list',[item()],None),
        ('tickets not list',{'tickets':{}},None),
        ('record not object',wrap([123]),0),
        ('payload missing',wrap([{'routing':'normal'}]),0),
        ('payload wrong type',wrap([bad_payload]),0),
        ('title wrong type',wrap([bad_title]),0),
        ('blank title',wrap([item(' ')]),0),
        ('paragraphs wrong type',wrap([item(paragraphs='body')]),0),
        ('paragraph wrong type',wrap([item(paragraphs=['B',123])]),0),
        ('all blank paragraphs',wrap([item(paragraphs=['  ','\n'])]),0),
        ('no paragraphs',wrap([item(paragraphs=[])]),0),
        ('unknown routing',wrap([item(routing='NORMAL')]),0),
        ('missing routing',wrap([missing_routing]),0),
        ('malformed JSON','{',None),
        ('later invalid record',wrap([item(),item(routing=None)]),1),
    ]
    result += [(name,{'files':{'bad.json':payload},'error_name':'bad.json','error_record':index}) for name,payload,index in invalids]
    result += [('no files',{'files':{'note.txt':'ignore'}}),
               ('empty dataset',{'files':{'a.json':wrap([])}}),
               ('all synthetic',{'files':{'a.json':wrap([{'synthetic':True}])}})]
    return result
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--script',type=Path,default=ROOT/'convert.py')
    p.add_argument('--only',choices=['base','all'],default='all');a=p.parse_args()
    failures=run_cases(a.script.resolve(),cases()[:1] if a.only=='base' else cases())
    r=subprocess.run([sys.executable,str(a.script.resolve()),'--help'],capture_output=True,text=True,timeout=10)
    if r.returncode or '--input-dir' not in r.stdout or '--output-csv' not in r.stdout:
        print('FAIL CLI help');failures+=1
    else:print('PASS CLI help')
    raise SystemExit(bool(failures))
