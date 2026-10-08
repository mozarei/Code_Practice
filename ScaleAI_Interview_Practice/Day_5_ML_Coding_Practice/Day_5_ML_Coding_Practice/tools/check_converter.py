import argparse
import csv
import subprocess
import sys
from pathlib import Path
from check_helpers import ROOT,run_cases


def item(text="A",flag=False,**extra):
    return {"messages":[{"role":"user","content":text}],"annotation":{"needs_review":flag},**extra}


def cases():
    files={str(p.relative_to(ROOT/"fixtures/raw")):p.read_text(encoding="utf-8")
           for p in (ROOT/"fixtures/raw").rglob("*") if p.is_file()}
    with (ROOT/"fixtures/reference_train.csv").open(encoding="utf-8",newline="") as f:
        rows=list(csv.reader(f))[1:]
    h=["text","label"]
    result=[("base",{"files":files,"expected":rows,"header":h})]
    conversation={"messages":[{"role":"system","content":None},{"role":"user","content":123},
        {"role":"assistant"},{"role":"user","content":"  Last\nmessage  "},
        {"role":"assistant","content":"later response"}],"annotation":{"needs_review":True}}
    positive=[
        ("sorted filenames",{"z.json":[item("Z",True)],"a.json":[item("A")]},[["A","0"],["Z","1"]]),
        ("last exact user message",{"a.json":[conversation]},[["Last\nmessage","1"]]),
        ("record order and duplicates",{"a.json":[item("Z"),item("A",True),item("Z")]},[["Z","0"],["A","1"],["Z","0"]]),
        ("quotes commas Unicode whitespace",{"a.json":[item('  Résumé, "test"\nسلام  keep  spaces  ')]},[['Résumé, "test"\nسلام  keep  spaces','0']]),
        ("exact true skipping",{"a.json":[{"skip":True},item(skip="true"),item(skip=False),item(skip=None),item(skip=1)]},[["A","0"]]*4),
        ("ignore files subfolders and JSON directories",{"a.json":[item()],"note.txt":"bad","nested/bad.json":"bad","folder.json/note.txt":"bad"},[["A","0"]]),
        ("empty file alongside valid",{"a.json":[],"b.json":[item()]},[["A","0"]]),
        ("unknown string role ignored",{"a.json":[{"messages":[{"role":"tool"},{"role":"user","content":"A"}],"annotation":{"needs_review":False}}]},[["A","0"]]),
    ]
    for name,files,rows in positive:result.append((name,{"files":files,"expected":rows,"header":h}))
    no_annotation=item();del no_annotation["annotation"]
    missing_content=item();del missing_content["messages"][0]["content"]
    invalids=[
        ("wrong top-level container",{"records":[item()]},None),
        ("record is not an object",[123],0),
        ("messages not a list",[{"messages":{},"annotation":{"needs_review":False}}],0),
        ("message is not an object",[{"messages":[123],"annotation":{"needs_review":False}}],0),
        ("role is not a string",[{"messages":[{"role":None,"content":"A"}],"annotation":{"needs_review":False}}],0),
        ("missing selected content",[missing_content],0),
        ("no user message",[{"messages":[{"role":"assistant","content":"A"}],"annotation":{"needs_review":False}}],0),
        ("empty messages",[{"messages":[],"annotation":{"needs_review":False}}],0),
        ("blank selected content",[item(" \n ")],0),
        ("non-string selected content",[item(None)],0),
        ("missing annotation",[no_annotation],0),
        ("numeric review flag rejected",[item(flag=1)],0),
        ("string review flag rejected",[item(flag="true")],0),
        ("null review flag rejected",[item(flag=None)],0),
        ("malformed JSON",'[{',None),
        ("later invalid record",[item(),no_annotation],1),
    ]
    for name,payload,index in invalids:
        result.append((name,{"files":{"bad.json":payload},"error_name":"bad.json","error_record":index}))
    result.extend([
        ("no JSON files",{"files":{"note.txt":"no records"}}),
        ("empty dataset",{"files":{"a.json":[]}}),
        ("all skipped",{"files":{"a.json":[{"skip":True}]}}),
    ])
    return result


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--script",type=Path,default=ROOT/"convert.py")
    parser.add_argument("--only",choices=["base","all"],default="all")
    args=parser.parse_args();script=args.script.resolve()
    selected=cases()[:1] if args.only=="base" else cases()
    failed=run_cases(script,selected)
    r=subprocess.run([sys.executable,str(script),"--help"],capture_output=True,text=True,timeout=10)
    if r.returncode or "--input-dir" not in r.stdout or "--output-csv" not in r.stdout:
        print("FAIL command-line help");failed+=1
    else:print("PASS command-line help")
    raise SystemExit(bool(failed))
