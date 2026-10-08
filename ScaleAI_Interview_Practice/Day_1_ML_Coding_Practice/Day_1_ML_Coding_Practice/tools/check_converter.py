"""Behavioral checks for your CLI; this file does not import a reference solution."""
import argparse
import csv
import json
import subprocess
import sys
from pathlib import Path
from check_helpers import ROOT, run_cases


def item(title="A", body="B", risk="benign", **extra):
    return {"document": {"title": title, "body": body},
            "annotation": {"risk": risk}, **extra}


def cases():
    base_files = {str(p.relative_to(ROOT / "fixtures/raw")): p.read_text(encoding="utf-8")
                  for p in (ROOT / "fixtures/raw").rglob("*") if p.is_file()}
    with (ROOT / "fixtures/reference_train.csv").open(encoding="utf-8", newline="") as f:
        expected = list(csv.reader(f))[1:]
    header = ["text", "label"]
    result = [("base", {"files": base_files, "expected": expected, "header": header})]
    positives = [
        ("sorted filenames", {"z.json": {"examples": [item("Z", "last", "risky")]},
                              "a.json": {"examples": [item("A", "first")]}},
         [["A\nfirst", "0"], ["Z\nlast", "1"]]),
        ("preserve record order", {"a.json": {"examples": [item("Z", "first"), item("A", "second", "risky")]}},
         [["Z\nfirst", "0"], ["A\nsecond", "1"]]),
        ("quotes commas Unicode newlines", {"a.json": {"examples": [item('  Résumé, "test"  ', '  سلام\nkeep  spaces  ')]}},
         [['Résumé, "test"\nسلام\nkeep  spaces', "0"]]),
        ("exact boolean exclusion", {"a.json": {"examples": [{"excluded": True},
                  item("T", "retain string", "risky", excluded="true"),
                  item("F", "retain false", excluded=False), item("N", "retain null", excluded=None)]}},
         [["T\nretain string", "1"], ["F\nretain false", "0"], ["N\nretain null", "0"]]),
        ("ignore non-JSON and subfolders", {"a.json": {"examples": [item()]},
                  "note.txt": "not JSON", "nested/bad.json": "not JSON"}, [["A\nB", "0"]]),
        ("empty file alongside valid data", {"empty.json": {"examples": []},
                  "valid.json": {"examples": [item()]}}, [["A\nB", "0"]]),
        ("extra fields and duplicate examples", {"a.json": {"examples": [item(extra=42), item(extra=99)]}},
         [["A\nB", "0"], ["A\nB", "0"]]),
    ]
    for name,files,rows in positives:
        result.append((name, {"files": files, "expected": rows, "header": header}))
    bad_record = item();del bad_record["document"]["body"]
    bad_annotation = item();del bad_annotation["annotation"]
    negatives = [
        ("missing body", {"bad.json": {"examples": [bad_record]}}, "bad.json"),
        ("missing annotation", {"bad.json": {"examples": [bad_annotation]}}, "bad.json"),
        ("unknown label", {"bad.json": {"examples": [item(risk="RISKY")]}}, "bad.json"),
        ("boolean label rejected", {"bad.json": {"examples": [item(risk=True)]}}, "bad.json"),
        ("empty body rejected", {"bad.json": {"examples": [item(body=" \n ")]}}, "bad.json"),
        ("empty title rejected", {"bad.json": {"examples": [item(title="  ")]}}, "bad.json"),
        ("null body rejected", {"bad.json": {"examples": [item(body=None)]}}, "bad.json"),
        ("invalid nested object", {"bad.json": {"examples": [{"document": [], "annotation": {"risk": "benign"}}]}}, "bad.json"),
        ("top-level list rejected", {"bad.json": [item()]}, "bad.json"),
        ("examples must be a list", {"bad.json": {"examples": {}}}, "bad.json"),
        ("record must be an object", {"bad.json": {"examples": [123]}}, "bad.json"),
        ("malformed JSON rejected", {"bad.json": '{"examples": ['}, "bad.json"),
        ("no JSON files", {"note.txt": "nothing to read"}, None),
        ("empty retained dataset", {"a.json": {"examples": []}}, None),
        ("all records excluded", {"a.json": {"examples": [{"excluded": True}]}}, None),
    ]
    for name,files,error in negatives:
        kwargs = {"files": files, "error_name": error}
        if error and isinstance(files[error], dict) and isinstance(files[error].get("examples"), list) and files[error]["examples"]:
            kwargs["error_record"] = 0
        result.append((name, kwargs))
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--script", type=Path, default=ROOT / "convert.py")
    parser.add_argument("--only", choices=["base", "all"], default="all")
    args = parser.parse_args()
    script = args.script.resolve()
    selected = cases()
    if args.only == "base": selected = selected[:1]
    failures = run_cases(script, selected)
    # A useful CLI should also expose its options without requiring an input file.
    help_result = subprocess.run([sys.executable, str(script), "--help"], capture_output=True, text=True, timeout=10)
    if help_result.returncode or "--input-dir" not in help_result.stdout or "--output-csv" not in help_result.stdout:
        print("FAIL command-line help");failures += 1
    else:
        print("PASS command-line help")
    raise SystemExit(bool(failures))
