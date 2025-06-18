from git import Repo
from datetime import datetime
import os
import json

def extract_commit_diffs(repo_path, max_commits=50):
    repo = Repo(repo_path)

    # Define NULL_TREE hash for first commit
    null_tree_hash = repo.git.hash_object('-t', 'tree', '/dev/null')
    NULL_TREE = repo.tree(null_tree_hash)

    commits = list(repo.iter_commits('HEAD', max_count=max_commits))
    extracted = []

    for commit in commits:
        print(f"Processing commit: {commit.hexsha[:7]}")  # Debug

        if commit.parents:
            parent = commit.parents[0]
            diff_index = parent.diff(commit, create_patch=True)
        else:
            diff_index = commit.diff(NULL_TREE, create_patch=True)

        full_diff = ""
        for diff in diff_index:
            if diff.a_blob and diff.b_blob:
                try:
                    full_diff += diff.diff.decode('utf-8', errors='ignore')
                except Exception as e:
                    print(f"Skipping binary diff: {e}")
            elif diff.new_file and diff.b_blob:
                try:
                    full_diff += diff.b_blob.data_stream.read().decode('utf-8', errors='ignore')
                except Exception as e:
                    print(f"Skipping unreadable new file: {e}")

        extracted.append({
            "commit": commit.hexsha[:7],
            "timestamp": datetime.fromtimestamp(commit.committed_date).isoformat(),
            "author": commit.author.name,
            "diff": full_diff.strip()
        })

    return extracted


if __name__ == "__main__":
    repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "chronocodex"))
    print(f"Scanning repo at: {repo_path}")
    results = extract_commit_diffs(repo_path)
    print(json.dumps(results[:3], indent=2))
