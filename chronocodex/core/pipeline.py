import os
from chronocodex.core.diff_parser import extract_commit_diffs
from chronocodex.core.summarizer import summarize_diff
from chronocodex.core.embedder import embed_text
from chronocodex.core.storage import init_db, store_commit_vector
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


REPO_PATH = "/home/brad/chronocodex"

def run_pipeline(repo_path=REPO_PATH, max_commits=10):
    print("Initializing DB...")
    init_db()

    print(f"Extracting up to {max_commits} commits...")
    commits = extract_commit_diffs(repo_path, max_commits=max_commits)

    for commit in commits:
        if not commit['diff'].strip():
            print(f"Skipping {commit['commit']} (no diff)")
            continue

        print(f"Processing commit {commit['commit']}...")
        summary = summarize_diff(commit['diff'])
        vector = embed_text(summary)

        store_commit_vector(
            commit_id=commit['commit'],
            timestamp=commit['timestamp'],
            author=commit['author'],
            summary=summary,
            vector=vector
        )

    print("Pipeline complete.")

if __name__ == "__main__":
    run_pipeline()
