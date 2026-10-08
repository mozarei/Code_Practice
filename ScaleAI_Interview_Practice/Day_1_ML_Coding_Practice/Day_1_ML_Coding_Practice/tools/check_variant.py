import argparse
from pathlib import Path
from check_helpers import ROOT, run_cases


def review(approved=True, title="A", body="B"):
    return {"message": {"title": title, "body": body}, "decision": {"approved": approved}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--script", type=Path, default=ROOT / "variant_convert.py")
    args = parser.parse_args()
    header = ["sentence", "target"]
    cases = [
        ("boolean mapping + escaping", {"files": {"a.json": [review(True, ' Résumé, "A" ', ' line1\nline2 '), review(False)]},
             "expected": [['Résumé, "A" | line1\nline2', "0"], ["A | B", "1"]], "header": header}),
        ("file and record ordering", {"files": {"z.json": [review(False, "Z")], "a.json": [review(True,"B"),review(False,"A")]},
             "expected": [["B | B", "0"], ["A | B", "1"], ["Z | B", "1"]], "header": header}),
        ("ignore unrelated files", {"files": {"a.json": [review()], "nested/bad.json": "bad", "note.txt":"bad"},
             "expected": [["A | B", "0"]], "header": header}),
        ("string approval rejected", {"files": {"bad.json": [review("true")]}, "error_name": "bad.json"}),
        ("integer approval rejected", {"files": {"bad.json": [review(1)]}, "error_name": "bad.json"}),
        ("missing approval rejected", {"files": {"bad.json": [{"message":{"title":"A","body":"B"},"decision":{}}]}, "error_name":"bad.json"}),
        ("blank text rejected", {"files": {"bad.json": [review(body="  ")]}, "error_name": "bad.json"}),
        ("wrong top-level shape", {"files": {"bad.json": {"examples": [review()]}}, "error_name": "bad.json"}),
        ("no records", {"files": {"a.json": []}}),
        ("null approval rejected", {"files": {"bad.json": [review(None)]}, "error_name": "bad.json", "error_record": 0}),
        ("malformed JSON rejected", {"files": {"bad.json": "["}, "error_name": "bad.json"}),
        ("no JSON files", {"files": {"note.txt": "ignored"}}),
        ("missing body rejected", {"files": {"bad.json": [{"message":{"title":"A"},"decision":{"approved":True}}]}, "error_name":"bad.json", "error_record":0}),
    ]
    for _, kwargs in cases:
        if kwargs.get("error_name") and isinstance(kwargs["files"]["bad.json"], list):
            kwargs["error_record"] = 0
    raise SystemExit(bool(run_cases(args.script.resolve(), cases)))
