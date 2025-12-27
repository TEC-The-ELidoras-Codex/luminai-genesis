import sys
import subprocess

PY = sys.executable


def run_demo(seed):
    # Use a temporary data file per run to avoid state carryover from file-based DB
    import tempfile
    with tempfile.NamedTemporaryFile() as tf:
        p = subprocess.run(
            [PY, "tec_book/erasure_demo.py", "--seed", str(seed), "--noninteractive", "--data-file", tf.name],
            capture_output=True,
            text=True,
            timeout=20,
        )
        return p.stdout


def test_demo_seed_repro():
    out1 = run_demo(42)
    out2 = run_demo(42)
    assert out1 == out2
    assert "[demo] Using seed 42" in out1
    assert "SESSION SUMMARY" in out1
