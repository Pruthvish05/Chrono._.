import os
import json
from constants import CHRONO_DIR, COMMITS_DIR, HEAD_FILE, INDEX_FILE
from commits import load_commit_snapshot 

def checkout(commit_hash: str):
    if not os.path.exists(CHRONO_DIR):
        print("Chrono repository not initialized.")
        return
    commit_path = os.path.join(COMMITS_DIR, f"{commit_hash}.json")
    if not os.path.exists(commit_path):
        print(f"Error: Commit '{commit_hash}' not found in history.")
        return
    target_files = load_commit_snapshot(commit_hash)
    print(f"Switching working directory to snapshot: {commit_hash[:7]}...")
    # 3. Restore Files from Content-Addressable Storage
    for filename, file_hash in target_files.items():
        from constants import OBJECTS_DIR
        object_path = os.path.join(OBJECTS_DIR, file_hash)
        if not os.path.exists(object_path):
            print(f"Critical Error: Object blob '{file_hash}' for file '{filename}' is missing.")
            return
        with open(object_path, 'r') as obj_f:
            file_content = obj_f.read()
        file_dir = os.path.dirname(filename)
        if file_dir and not os.path.exists(file_dir):
            os.makedirs(file_dir, exist_ok=True)
            print(f" Created directory structure: {file_dir}/")
        with open(filename, 'w') as wp_f:
            wp_f.write(file_content)
            
        print(f" Restored: {filename}")
    if os.path.exists(HEAD_FILE):
        with open(HEAD_FILE, 'r') as f:
            current_head = f.read().strip()
        if current_head:
            current_files = load_commit_snapshot(current_head)
            for old_file in current_files:
                if old_file not in target_files and os.path.exists(old_file):
                    os.remove(old_file)
                    print(f" Removed untracked file from this snapshot: {old_file}")
    with open(HEAD_FILE, 'w') as f:
        f.write(commit_hash)
    with open(INDEX_FILE, 'w') as f:
        json.dump({}, f, indent=4)
    print(f"HEAD is now at {commit_hash[:7]}.")