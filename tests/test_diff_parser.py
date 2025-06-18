import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tempfile
import subprocess
import shutil
from chronocodex.core.diff_parser import extract_commit_diffs


def test_diff_parser_basic():
    # Setup temporary Git repo
    temp_dir = tempfile.mkdtemp()
    subprocess.run(["git", "init"], cwd=temp_dir)

    file_path = os.path.join(temp_dir, "test.py")
    with open(file_path, "w") as f:
        f.write("def foo():\n    return 1\n")
    subprocess.run(["git", "add", "test.py"], cwd=temp_dir)
    subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=temp_dir)

    with open(file_path, "a") as f:
        f.write("\ndef bar():\n    return 2\n")
    subprocess.run(["git", "commit", "-am", "Add bar function"], cwd=temp_dir)

    # Run parser
    results = extract_commit_diffs(temp_dir)
    assert len(results) == 2
    assert any("bar" in r["diff"] for r in results), "Expected to find 'bar' in diff"

    # Clean up
    shutil.rmtree(temp_dir)

if __name__ == "__main__":
    test_diff_parser_basic()
    print("[✓] test_diff_parser_basic passed.")
