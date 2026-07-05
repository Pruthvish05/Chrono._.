import os
import json
from constants import CHRONO_DIR, COMMITS_DIR, HEAD_FILE, INDEX_FILE
from commits import load_commit_snapshot 

def checkout(commit_hash: str):
    """
    Restores the working directory to match the complete snapshot 
    of the specified commit_hash.
    """
    # 1. Verification Invariant
    if not os.path.exists(CHRONO_DIR):
        print("Chrono repository not initialized.")
        return

    commit_path = os.path.join(COMMITS_DIR, f"{commit_hash}.json")
    if not os.path.exists(commit_path):
        print(f"Error: Commit '{commit_hash}' not found in history.")
        return

    # 2. Fetch the Target Snapshot Map
    # This gives us the exact {"filename": "hash"} state we want to restore
    target_files = load_commit_snapshot(commit_hash)

    print(f"Switching working directory to snapshot: {commit_hash[:7]}...")

    # 3. Restore Files from Content-Addressable Storage
    # Loop through every file that belongs in this historical snapshot
    for filename, file_hash in target_files.items():
        # Read the raw content from the objects database
        # Note: Depending on your exact structure, objects might be directly under OBJECTS_DIR
        # or grouped by subdirectories. We assume direct lookup by hash for simplicity here.
        from constants import OBJECTS_DIR
        object_path = os.path.join(OBJECTS_DIR, file_hash)
        
        if not os.path.exists(object_path):
            print(f"Critical Error: Object blob '{file_hash}' for file '{filename}' is missing.")
            return

        with open(object_path, 'r') as obj_f:
            file_content = obj_f.read()

        # Write the content back to the real working directory
        # Systems note: In later versions, we'll use os.makedirs to handle nested folders safely
        with open(filename, 'w') as wp_f:
            wp_f.write(file_content)
            
        print(f" Restored: {filename}")

    # 4. Handle Deletions (Basic Clean up)
    # If a file exists in the *current* HEAD commit but NOT in our *target* checkout commit,
    # it means that file didn't exist back then, so we should remove it from disk.
    if os.path.exists(HEAD_FILE):
        with open(HEAD_FILE, 'r') as f:
            current_head = f.read().strip()
        
        if current_head:
            current_files = load_commit_snapshot(current_head)
            for old_file in current_files:
                if old_file not in target_files and os.path.exists(old_file):
                    os.remove(old_file)
                    print(f" Removed untracked file from this snapshot: {old_file}")

    # 5. Atomically Update HEAD Pointer
    with open(HEAD_FILE, 'w') as f:
        f.write(commit_hash)

    # 6. Clear Staging Area
    # Moving to a new commit resets your staging environment
    with open(INDEX_FILE, 'w') as f:
        json.dump({}, f, indent=4)

    print(f"HEAD is now at {commit_hash[:7]}.")