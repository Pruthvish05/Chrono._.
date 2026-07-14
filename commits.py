import os
import json
import hashlib
import time
from constants import CHRONO_DIR, COMMITS_DIR, INDEX_FILE, HEAD_FILE

def load_commit_snapshot(commit_hash: str) -> dict:
    if not commit_hash:
        return {}
        
    commit_path = os.path.join(COMMITS_DIR, f"{commit_hash}.json")
    if not os.path.exists(commit_path):
        raise FileNotFoundError(f"Critical Error: Commit object '{commit_hash}' not found.")
        
    with open(commit_path, 'r') as f:
        commit_data = json.load(f)
        
    return commit_data.get('files', {})

def commit(message: str):
    # 1. Structural Invariant Verifications
    if not os.path.exists(CHRONO_DIR):
        print("Chrono repository not initialized. Please run 'init()' first.")
        return
        
    if not message:
        print("Commit message cannot be empty.")
        return
        
    if not os.path.exists(INDEX_FILE):
        print("No files added to commit.")
        return
    with open(INDEX_FILE, 'r') as f:
        index = json.load(f)
        
    if not index:
        print("No changes to commit.")
        return
    parent = None
    if os.path.exists(HEAD_FILE):
        with open(HEAD_FILE, 'r') as f:
            content = f.read().strip()
            if content:
                parent = content
    full_snapshot = load_commit_snapshot(parent) if parent else {}
    full_snapshot.update(index)
    commit_data = {
        'message': message,
        'files': full_snapshot,
        'timestamp': int(time.time()),
        'parent': parent
    }
    serialized_data = json.dumps(commit_data, sort_keys=True).encode()
    commit_hash = hashlib.sha1(serialized_data).hexdigest()
    commit_path = os.path.join(COMMITS_DIR, f"{commit_hash}.json")
    with open(commit_path, 'w') as f:
        json.dump(commit_data, f, indent=4, sort_keys=True)
        with open(HEAD_FILE, 'w') as r:
            r.write(commit_hash)
    with open(INDEX_FILE, 'w') as f:
        json.dump({}, f, indent=4)
    print(f"Commit created: {commit_hash} with message: '{message}'")
    return commit_hash

def log():
    if not os.path.exists(HEAD_FILE):
        print("Chrono repository not initialized or no commits made yet.")
        return
    with open(HEAD_FILE, 'r') as f:
        current_hash = f.read().strip()
    if not current_hash:
        print("No commits yet. Use 'chrono commit' to record your first snapshot.")
        return
    print("*--- Commit History ---*\n")
    while current_hash:
        commit_path = os.path.join(COMMITS_DIR, f"{current_hash}.json")
        if not os.path.exists(commit_path):
            print(f"Critical Error: Commit object '{current_hash}' is missing. History graph broken.")
            break
        with open(commit_path, 'r') as f:
            commit_data = json.load(f)
        raw_time = commit_data.get('timestamp', 0)
        formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(raw_time))
        message = commit_data.get('message', 'No message provided.')
        parent = commit_data.get('parent')
        print(f"Commit: {current_hash}")
        print(f"Date:   {formatted_time}")
        print(f"Message: {message}")
        print("files: " + ", ".join(commit_data.get('files', {}).keys()))
        print("-" * 40)
        current_hash = parent