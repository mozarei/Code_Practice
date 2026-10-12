import csv
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_case(script, files, expected=None, header=None, error_name=None, error_record=None):
    with tempfile.TemporaryDirectory() as folder:
        base = Path(folder)
        raw = base / "input folder"
        raw.mkdir()
        for name, payload in files.items():
            path = raw / name
            path.parent.mkdir(parents=True, exist_ok=True)
            content = payload if isinstance(payload, str) else json.dumps(payload, ensure_ascii=False)
            path.write_text(content, encoding="utf-8")
        out = base / "output folder" / "nested" / "train.csv"
        if expected is None:
            out.parent.mkdir(parents=True)
            out.write_bytes(b"KEEP THIS EXISTING FILE")
        result = subprocess.run(
            [sys.executable, str(script), "--input-dir", str(raw), "--output-csv", str(out)],
            cwd=base, capture_output=True, text=True, encoding="utf-8", timeout=10)
        if expected is None:
            assert result.returncode != 0, "Invalid input was accepted"
            assert result.stderr.strip(), "Expected a diagnostic on stderr"
            if error_name:
                assert error_name in result.stderr, "Diagnostic should name the bad file"
            if error_record is not None:
                assert f"record {error_record}" in result.stderr, "Diagnostic should name the record index"
            assert out.read_bytes() == b"KEEP THIS EXISTING FILE", "Validation failure overwrote output"
            out.unlink()
            retry = subprocess.run(result.args, cwd=base, capture_output=True, text=True, timeout=10)
            assert retry.returncode != 0, "Invalid input accepted on second run"
            assert not out.exists(), "Validation failure created a new output CSV"
        else:
            assert result.returncode == 0, result.stderr[-2000:]
            with out.open(encoding="utf-8", newline="") as f:
                reader = csv.reader(f)
                assert next(reader) == header, "Wrong header or column order"
                assert list(reader) == expected, "Rows, labels, order or escaping differ"
            first_bytes = out.read_bytes()
            again = subprocess.run(result.args, cwd=base, capture_output=True, text=True, timeout=10)
            assert again.returncode == 0, again.stderr
            assert out.read_bytes() == first_bytes, "Output changed across identical runs"


def run_cases(script, cases):
    failures = 0
    for name, kwargs in cases:
        try:
            run_case(script, **kwargs)
        except Exception as exc:
            failures += 1
            print("FAIL", name, "-", str(exc)[:1200])
        else:
            print("PASS", name)
    print(f"Result: {len(cases) - failures}/{len(cases)} scenarios passed")
    return failures
