# runner.py — Central pipeline logic, isolated to avoid circular imports
# Author: Bradley R Kinnard
# License: MIT

from chronocodex.core.diff_parser import extract_commit_diffs
from chronocodex.core.summarizer import summarize_diff
from chronocodex.core.embedder import embed_text
from chronocodex.core.storage import store_commit

def run_pipeline(repo_path):
    """
    Run the full summarization and vectorization pipeline on a repo.
    """
    commits = extract_commit_diffs(repo_path)
    print(f"[INFO] Found {len(commits)} commits in repo: {repo_path}")

    for commit in commits:
        summary = summarize_diff(commit["diff"])
        vector = embed_text(summary)
        store_commit(
            commit_id=commit["commit"],
            timestamp=commit["timestamp"],
            author=commit["author"],
            summary=summary,
            vector=vector,
            date=commit["timestamp"]  # storing date explicitly
        )
        print(f"[✓] Stored commit {commit['commit']} — {summary}")
