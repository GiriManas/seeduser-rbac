import subprocess

# List of jobs: [DATASET_PATH, TRANSCRIPT_COL, SUMMARY_COL, OUT_PATH]
jobs = [
    ["/mnt/nas1/data/dataset1.csv", "transcript", "summary", "/mnt/nas1/output/out1.csv"],
    ["/mnt/nas1/data/dataset2.csv", "call_transcript", "gen_summary", "/mnt/nas1/output/out2.csv"],
    ["/mnt/nas1/data/dataset3.csv", "conversation", "phi_summary", "/mnt/nas1/output/out3.csv"],
]

PYTHON_SCRIPT = "rating_phi.py"

for job in jobs:
    dataset, transcript_col, summary_col, out_path = job
    cmd = ["python", PYTHON_SCRIPT, dataset, transcript_col, summary_col, out_path]
    print(f"\n🚀 Running: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True)
        print(f"✅ Finished: {out_path}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed: {cmd}\nError: {e}")