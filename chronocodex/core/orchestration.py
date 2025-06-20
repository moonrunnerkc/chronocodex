#!/usr/bin/env python3
"""
orchestration.py — Real Git Commit Ingestor for Chronocodex

Author: Bradley R Kinnard
License: MIT

Usage:
  PYTHONPATH=. python chronocodex/core/orchestration.py
"""

import subprocess
import os
from chronocodex.core.embedder import embed_text
from chronocodex.core.storage import store_commit_vector, init_db  # ✅ updated import
from datetime import datetime
from chronocodex.core.summarizer import summarize_diff
from chronocodex.core.diff_parser import parse_git_diff

def run_pipeline(diff_text):
    """
    Parses and summarizes a given Git diff.
    """
    parsed = parse_git_diff(diff_text)
    return summarize_diff(parsed)

def get_commits(repo_path, max_count=50):
    os.chdir(repo_path)
    result = subprocess.run(
        ["git", "log", f"-n{max_count}", "--pretty=format:%H||%an||%ad", "--date=iso"],
        stdout=subprocess.PIPE,
        text=True
    )
    commits = []
    for line in result.stdout.strip().split("\n"):
        sha, author, date = line.split("||")
        diff = subprocess.run(["git", "show", sha], stdout=subprocess.PIPE, text=True).stdout
        commits.append({"commit": sha, "author": author, "timestamp": date, "diff": diff})
    return commits

def ingest_commits(repo_path):
    init_db()  # ✅ ensure DB schema is initialized
    commits = get_commits(repo_path)
    print(f"[INFO] Found {len(commits)} commits in repo: {repo_path}")
    for entry in commits:
        summary = run_pipeline(entry["diff"])
        vector = embed_text(summary)
        store_commit_vector(  # ✅ updated to match renamed canonical storage function
            commit_id=entry["commit"],
            timestamp=entry["timestamp"],
            author=entry["author"],
            summary=summary,
            vector=vector,
            date=entry["timestamp"].split("T")[0]  # ISO format YYYY-MM-DD
        )
        print(f"[✓] Stored commit {entry['commit']} — {summary}")

if __name__ == "__main__":
    repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    ingest_commits(repo_dir)
