import os
from constants import CHRONO_DIR, OBJECTS_DIR, COMMITS_DIR, INDEX_FILE, HEAD_FILE
import json
import hashlib
import time

def commit(message: str):
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
    if os.path.exists(HEAD_FILE):
        with open(HEAD_FILE, 'r') as f:
            parent = f.read().strip()
    else:
        parent = None
    commit_data = {
        'message': message,
        'files': index,
        'timestamp': int(time.time()),
        'parent': parent
    }
    commit_hash = hashlib.sha1(json.dumps(commit_data, sort_keys=True).encode()).hexdigest()
    commit_path = os.path.join(COMMITS_DIR, f"{commit_hash}.json")
    with open(commit_path, 'w') as f:
        json.dump(commit_data, 
                    f, 
                    indent=4,
                    sort_keys=True)
    with open(HEAD_FILE, 'w') as f:
        f.write(commit_hash)
    with open(INDEX_FILE, 'w') as f:
        json.dump({}, f)
    print(f"Commit created: {commit_hash} with message: '{message}'")