<<<<<<< HEAD
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

=======
# pipeline.py — Entry Point
# Author: Bradley Ryan Kinnard
# License: MIT

import os
import sys

# ✅ Delegate actual logic to orchestration to avoid circular imports
from chronocodex.core.orchestration import ingest_commits

# Maintain reference to DB path for CLI/UI use if needed
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "chronocodex.db"))
REPO_PATH = os.getcwd()  # Uses the current working directory

# Ensure core path is available for CLI entry or module use
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def run_pipeline(repo_path=None, max_commits=10):
    repo_path = repo_path or os.getcwd()

    """
    Entry point for running the Chronocodex pipeline.

    Delegates all actual commit parsing and storage to orchestration.py
    to avoid circular imports and ensure modular pipeline structure.
    """
    print(f"[INFO] Running pipeline on: {repo_path}")
    ingest_commits(repo_path)
    print("[✓] Pipeline complete via orchestration.")

# CLI debug/test entry point
>>>>>>> 4a78c9d6 (Refactored for open-source release: portable pathing, CLI-ready, no hardcoded repo)
if __name__ == "__main__":
    run_pipeline()
