import os
from constants import CHRONO_DIR, HEAD_FILE, OBJECTS_DIR, COMMITS_DIR, INDEX_FILE
import json
import difflib
def diff():
    # Implementation for diff functionality
    if not os.path.exists(CHRONO_DIR):
        print("Chrono repository not initialized. Please run 'init()' first.")
        return
    if not os.path.exists(HEAD_FILE):
        print("No commits found.")
        return
    with open(HEAD_FILE, 'r') as f:
        current_commit = f.read().strip()
    if not current_commit:
        print("No commits found.")
        return
    with open(os.path.join(COMMITS_DIR, f"{current_commit}.json"), 'r') as f:
        commit_data = json.load(f)
    for filepath, file_hash in commit_data['files'].items():
        object_path = os.path.join(OBJECTS_DIR, file_hash)
        if os.path.exists(object_path):
            with open(object_path, 'rb') as f:
                content = f.read().decode("utf-8", errors='ignore')
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    current_content = f.read()
                diff = difflib.unified_diff(
                    content.splitlines(),
                    current_content.splitlines(),
                    fromfile='current',
                    tofile='commit',
                    lineterm=''
                )
                print(f"Diff for {filepath}:")
                print('\n'.join(diff))
            else:
                print(f"File '{filepath}' does not exist in the current directory.")