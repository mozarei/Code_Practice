import argparse,copy,csv,subprocess,sys
from pathlib import Path
from check_helpers import ROOT,run_cases
def doc(identifier='a',title='T',body='B'):
    return {'id':identifier,'content':{'title':title,'body':body}}
def review(identifier='a',decision='allow',status='final'):
    return {'document_id':identifier,'status':status,'decision':decision}
def export(documents=None,reviews=None):
    return {'documents':[doc()] if documents is None else documents,'reviews':[review()] if reviews is None else reviews}
def cases():
    files={str(p.relative_to(ROOT/'fixtures/raw')):p.read_text(encoding='utf-8') for p in (ROOT/'fixtures/raw').rglob('*') if p.is_file()}
    with (ROOT/'fixtures/reference_train.csv').open(encoding='utf-8',newline='') as f:rows=list(csv.reader(f))[1:]
    h=['text','label'];result=[('base',{'files':files,'expected':rows,'header':h})]
    positives=[
        ('last FINAL wins',{'a.json':export(reviews=[review(decision='review'),review(decision='allow')])},[['T\nB','0']]),
        ('draft never cancels final',{'a.json':export(reviews=[review(decision='review'),review(status='draft',decision=None)])},[['T\nB','1']]),
        ('draft decision ignored',{'a.json':export(reviews=[{'document_id':'a','status':'draft'},review()])},[['T\nB','0']]),
        ('document order not review order',{'a.json':export([doc('z','Z'),doc('a','A')],[review('a','review'),review('z')])},[['Z\nB','0'],['A\nB','1']]),
        ('no final skips valid document',{'a.json':export([doc('a'),doc('b','B')],[review('a'),review('b',status='draft')])},[['T\nB','0']]),
        ('unknown final ignored after validation',{'a.json':export(reviews=[review('other','review'),review()])},[['T\nB','0']]),
        ('IDs local to file plus sorted filenames',{'z.json':export([doc('a','Z')],[review('a','review')]),'a.json':export()},[['T\nB','0'],['Z\nB','1']]),
        ('escaping and trim',{'a.json':export([doc('a',' Résumé, "test" ',' سلام  keep  spaces\nnext ')])},[['Résumé, "test"\nسلام  keep  spaces\nnext','0']]),
        ('IDs compare exactly',{'a.json':export([doc(' a','A'),doc('a','B')],[review(' a'),review('a','review')])},[['A\nB','0'],['B\nB','1']]),
        ('empty file alongside valid',{'a.json':export([],[]),'b.json':export()},[['T\nB','0']]),
        ('ignore unrelated paths',{'a.json':export(),'note.txt':'bad','nested/bad.json':'bad','folder.json/note.txt':'bad'},[['T\nB','0']]),
    ]
    result += [(name,{'files':files,'expected':rows,'header':h}) for name,files,rows in positives]
    invalids=[
        ('top-level list',[doc()],None),
        ('documents not list',{'documents':{},'reviews':[]},None),
        ('reviews missing',{'documents':[]},None),
        ('document not object',export([123],[]),0),
        ('blank document id',export([doc(' ')],[]),0),
        ('numeric document id',export([doc(1)],[]),0),
        ('duplicate document id',export([doc(),doc()],[]),1),
        ('invalid unreviewed document',export([doc(body=None)],[]),0),
        ('content not object',export([{'id':'a','content':[]}],[]),0),
        ('blank title',export([doc(title=' ')],[]),0),
        ('blank body',export([doc(body='\n ')],[]),0),
        ('review not object',export(reviews=[123]),0),
        ('blank review id',export(reviews=[review(' ')]),0),
        ('invalid draft id',export(reviews=[review(None,status='draft')]),0),
        ('unknown status',export(reviews=[review(status='FINAL')]),0),
        ('missing final decision',export(reviews=[{'document_id':'a','status':'final'}]),0),
        ('numeric final decision',export(reviews=[review(decision=1)]),0),
        ('invalid unknown final still rejected',export(reviews=[review(),review('other',decision='bad')]),1),
        ('later invalid record',export([doc('a'),doc('b',body=None)]),1),
        ('malformed JSON','{',None),
    ]
    result += [(name,{'files':{'bad.json':payload},'error_name':'bad.json','error_record':index}) for name,payload,index in invalids]
    result += [('no files',{'files':{'note.txt':'ignore'}}),('empty dataset',{'files':{'a.json':export([],[])}}),
               ('only drafts',{'files':{'a.json':export(reviews=[review(status='draft')])}})]
    return result
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--script',type=Path,default=ROOT/'convert.py');p.add_argument('--only',choices=['base','all'],default='all');a=p.parse_args()
    failed=run_cases(a.script.resolve(),cases()[:1] if a.only=='base' else cases())
    r=subprocess.run([sys.executable,str(a.script.resolve()),'--help'],capture_output=True,text=True,timeout=10)
    if r.returncode or '--input-dir' not in r.stdout or '--output-csv' not in r.stdout:print('FAIL CLI help');failed+=1
    else:print('PASS CLI help')
    raise SystemExit(bool(failed))
