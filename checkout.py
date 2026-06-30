import os
import json
from constants import CHRONO_DIR, OBJECTS_DIR, COMMITS_DIR, INDEX_FILE, HEAD_FILE

def checkout(commit_hash):
    if not os.path.exists(os.path.join(COMMITS_DIR, f"{commit_hash}.json")):
        print(f"Commit '{commit_hash}' does not exist.")
        return
    with open(os.path.join(COMMITS_DIR, f"{commit_hash}.json"), 'r') as f:
        commit_data = json.load(f)
    files = commit_data['files']
    if not os.path.exists(CHRONO_DIR):
        print("Chrono repository not initialized. Please run 'init()' first.")
        return
    for file in os.listdir():
        if file == '.chrono':
            continue
        if file in files and os.path.isfile(file):
            os.remove(file)
    for filepath, file_hash in files.items():
        object_path = os.path.join(OBJECTS_DIR, file_hash)
        if os.path.exists(object_path):
            with open(object_path, 'rb') as f:
                content = f.read()
            with open(filepath, 'wb') as f:
                f.write(content)
    with open(HEAD_FILE, 'w') as f:
        f.write(commit_hash)
    print(f"Checked out commit: {commit_hash}")
    print(f"Restored files: {', '.join(files.keys())}")
    print(f"THIS WILL OVERWRITE CURRENT FILES IN THE DIRECTORY, MAKE SURE TO COMMIT YOUR CHANGES BEFORE CHECKING OUT ANOTHER COMMIT.")