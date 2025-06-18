#!/usr/bin/env python3
"""
Chronocodex CLI Interface

Author: Bradley Ryan Kinnard
License: MIT

Description:
Command-line interface for Chronocodex — a commit-level AI introspection framework.
Provides initialization, scanning, and natural language querying of Git repositories.
"""

import sys
import os
import argparse

# Ensure root path in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from chronocodex.core.diff_parser import extract_commit_diffs
from chronocodex.core.summarizer import summarize_diff
from chronocodex.core.embedder import embed_summary
from chronocodex.core.storage import init_db, store_commit
from chronocodex.core.timeline import generate_timeline, get_similar_summaries

def cmd_init():
    init_db()
    print("[✓] Initialized Chronocodex database.")

def cmd_scan(repo_path):
    print(f"[~] Scanning repository: {repo_path}")
    commits = extract_commit_diffs(repo_path)
    print(f"[~] Found {len(commits)} commits")

    for commit in commits:
        diff = commit["diff"]
        if not diff.strip():
            print(f"[!] Skipping empty diff: {commit['commit']}")
            continue

        summary = summarize_diff(diff)
        vector = embed_summary(summary)
        store_commit(commit["commit"], commit["timestamp"], commit["author"], summary, vector)
        print(f"[+] Stored commit {commit['commit'][:7]}: {summary[:60]}...")

    print("[✓] Scan complete.")

def cmd_query(query):
    print(f"[?] Query Results:")
    query_vector = embed_summary(query)
    results = get_similar_summaries(query_vector)
    for r in results:
        print(f"- {r['id']} (score={r['similarity']:.2f}): {r['summary']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chronocodex: LLM-Powered Codebase Timelining Tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Initialize Chronocodex DB")

    scan_parser = subparsers.add_parser("scan", help="Scan a Git repo")
    scan_parser.add_argument("--repo", default=".", help="Path to the Git repo")

    query_parser = subparsers.add_parser("query", help="Ask about code history")
    query_parser.add_argument("question", help="Natural language question")

    args = parser.parse_args()

    if args.command == "init":
        cmd_init()
    elif args.command == "scan":
        cmd_scan(args.repo)
    elif args.command == "query":
        cmd_query(args.question)
