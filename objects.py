import os
from constants import CHRONO_DIR, OBJECTS_DIR, COMMITS_DIR, INDEX_FILE, HEAD_FILE
import json
import hashlib
import difflib
import time
def add(filename):
    if not os.path.exists(CHRONO_DIR):
        print("Chrono repository not initialized. Please run 'init()' first.")
        return
    if not os.path.exists(filename):
        print(f"File '{filename}' does not exist.")
        return
    with open(filename, 'rb') as f:
        content = f.read()
    file_hash = hashlib.sha1(content).hexdigest()
    object_path = os.path.join(OBJECTS_DIR, file_hash)
    if not os.path.exists(object_path):
        with open(object_path, 'wb') as f:
            f.write(content)
    with open(INDEX_FILE, 'r') as f:
        index=json.load(f)
    filepath = os.path.relpath(filename)
    index[filepath] = file_hash
    with open(INDEX_FILE, 'w') as f:
        json.dump(index, f,indent=4) 
    print(f"File added: {filename} (Hash: {file_hash})")