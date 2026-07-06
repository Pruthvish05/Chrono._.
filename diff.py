import os
import difflib
from constants import CHRONO_DIR, HEAD_FILE
from commits import load_commit_snapshot  # Re-using our snapshot reader!

def diff():
    if not os.path.exists(CHRONO_DIR):
        print("Chrono repository not initialized.")
        return
    parent_hash = None
    if os.path.exists(HEAD_FILE):
        with open(HEAD_FILE, 'r') as f:
            parent_hash = f.read().strip()
    if not parent_hash:
        print("No commits made yet. Nothing to compare against.")
        return
    latest_snapshot = load_commit_snapshot(parent_hash)
    for filename, file_hash in latest_snapshot.items():
        if not os.path.exists(filename):
            print(f"\n--- {filename} (Deleted in Working Directory) ---")
            continue
        from constants import OBJECTS_DIR
        object_path = os.path.join(OBJECTS_DIR, file_hash)
        with open(object_path, 'r') as f:
            committed_lines = f.readlines()
        with open(filename, 'r') as f:
            working_lines = f.readlines()
        comparison = difflib.unified_diff(
            committed_lines,
            working_lines,
            fromfile=f"a/{filename} (committed)",
            tofile=f"b/{filename} (working)",
            lineterm='' 
        )
        diff_list = list(comparison)
        if diff_list:
            print(f"\nShowing modifications for: {filename}")
            print("=" * 40)
            for line in diff_list:
                print(line)