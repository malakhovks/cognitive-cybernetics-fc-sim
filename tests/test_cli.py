import os, tempfile, shutil
from subprocess import run, PIPE
def test_cli_run_and_summarize():
    tmp = tempfile.mkdtemp()
    try:
        results_dir = os.path.join(tmp, "results")
        reports_dir = os.path.join(tmp, "reports")
        run(["python", "-m", "src.cli", "run", "--config", "config/main.yaml", "--scenario", "pid", "--trials", "2", "--results", results_dir],
            stdout=PIPE, stderr=PIPE, text=True, check=True)
        assert os.path.isdir(os.path.join(results_dir, "pid"))
        out_csv = os.path.join(reports_dir, "summary.csv")
        run(["python", "-m", "src.cli", "summarize", "--results", results_dir, "--out", out_csv],
            stdout=PIPE, stderr=PIPE, text=True, check=True)
        assert os.path.isfile(out_csv)
    finally:
        shutil.rmtree(tmp)
