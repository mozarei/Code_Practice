import argparse
import csv
import subprocess
import sys
from pathlib import Path
from check_helpers import ROOT, run_cases


def item(title="A", body="B", category="routine", **extra):
    return {"content": {"title": title, "body": body}, "review": {"category": category}, **extra}


def cases():
    files = {str(p.relative_to(ROOT/"fixtures/raw")): p.read_text(encoding="utf-8")
             for p in (ROOT/"fixtures/raw").rglob("*") if p.is_file()}
    with (ROOT/"fixtures/reference_train.csv").open(encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f))[1:]
    h = ["text","label"]
    result = [("base", {"files": files, "expected": rows, "header": h})]
    positives = [
        ("sorted filenames", {"z.json":{"records":[item("Z","last","urgent")]},
                              "a.json":{"records":[item("A","first")]}}, [["A\nfirst","0"],["Z\nlast","1"]]),
        ("record order and duplicates", {"a.json":{"records":[item("Z"),item("A"),item("Z")]}},
            [["Z\nB","0"],["A\nB","0"],["Z\nB","0"]]),
        ("Unicode quotes commas and internal whitespace", {"a.json":{"records":[item('  Résumé, "test"  ', '  سلام\nkeep  spaces  ')]}},
            [['Résumé, "test"\nسلام\nkeep  spaces','0']]),
        ("exact false filtering", {"a.json":{"records":[{"include":False},item(include="false"),item(include=None),item(include=0),item(include=True)]}},
            [["A\nB","0"]]*4),
        ("ignore other files subfolders and JSON-named directories", {"a.json":{"records":[item()]},"note.txt":"bad", "nested/bad.json":"bad", "folder.json/ignored.txt":"bad"},
            [["A\nB","0"]]),
        ("empty file alongside valid", {"a.json":{"records":[]}, "b.json":{"records":[item(category="urgent")]}}, [["A\nB","1"]]),
        ("extra fields and missing include", {"a.json":{"records":[item(metadata={"x":1})]}}, [["A\nB","0"]]),
    ]
    for name,files,rows in positives:
        result.append((name,{"files":files,"expected":rows,"header":h}))
    missing=item(); del missing["content"]["body"]
    bads = [
        ("missing body", {"records":[missing]},0),
        ("unknown category", {"records":[item(category="URGENT")]},0),
        ("boolean category", {"records":[item(category=True)]},0),
        ("null body", {"records":[item(body=None)]},0),
        ("blank title", {"records":[item(title="  ")]},0),
        ("blank body", {"records":[item(body=" \n ")]},0),
        ("invalid nested object", {"records":[{"content":[],"review":{"category":"routine"}}]},0),
        ("invalid record", {"records":[123]},0),
        ("wrong top container", [item()],None),
        ("wrong records container", {"records":{}},None),
        ("malformed JSON", '{"records": [',None),
    ]
    for name,payload,index in bads:
        result.append((name,{"files":{"bad.json":payload},"error_name":"bad.json","error_record":index}))
    result.extend([
        ("no input JSON", {"files":{"note.txt":"empty"}}),
        ("empty records", {"files":{"a.json":{"records":[]}}}),
        ("all skipped", {"files":{"a.json":{"records":[{"include":False}]}}}),
        ("later invalid record preserves output", {"files":{"bad.json":{"records":[item(),missing]}},"error_name":"bad.json","error_record":1}),
    ])
    return result


if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--script",type=Path,default=ROOT/"convert.py")
    parser.add_argument("--only",choices=["base","all"],default="all")
    args=parser.parse_args()
    script=args.script.resolve()
    selected=cases()[:1] if args.only=="base" else cases()
    failed=run_cases(script,selected)
    r=subprocess.run([sys.executable,str(script),"--help"],capture_output=True,text=True,timeout=10)
    if r.returncode or "--input-dir" not in r.stdout or "--output-csv" not in r.stdout:
        print("FAIL command-line help"); failed+=1
    else:
        print("PASS command-line help")
    raise SystemExit(bool(failed))
