#in this we will create our db in to the system namly
#.chrono/ and in that two folders objects/ , commits/ 
#am also tryna build a habit of writing comments and code in modules so that it can be easily read and maintained in future
import os
import json
import hashlib
def init():
    print(f"Initializing Chrono repository... in {os.getcwd()}")
    if not os.path.exists('.chrono'):
        os.makedirs('.chrono/objects')
        os.makedirs('.chrono/commits')
        with open('.chrono/index.json', 'w') as f:
            json.dump({}, f)
        with open('.chrono/HEAD', 'w') as f:
            f.write('')
        print("Chrono repository initialized.")
    else:
        print("Chrono repository already exists.")
init()
def add(filename):
    if not os.path.exists(filename):
        print(f"File '{filename}' does not exist.")
        return
    with open(filename, 'rb') as f:
        content = f.read()
    file_hash = hashlib.sha1(content).hexdigest()
    object_path = f'.chrono/objects/{file_hash}'
    if not os.path.exists(object_path):
        with open(object_path, 'wb') as f:
            f.write(content)
    with open('.chrono/index.json', 'r') as f:
        index=json.load(f)
    filepath = os.path.relpath(filename)
    index[filepath] = file_hash
    with open('.chrono/index.json', 'w') as f:
        json.dump(index, f,indent=4) 
    print(f"File added: {filename} (Hash: {file_hash})")
def commit(message: str):
    if not message:
        print("Commit message cannot be empty.")
        return
    if not os.path.exists('.chrono/index.json'):
        print("No files added to commit.")
        return
    with open('.chrono/index.json', 'r') as f:
        index = json.load(f)
    if not index:
        print("No changes to commit.")
        return
    if os.path.exists('.chrono/HEAD'):
        with open('.chrono/HEAD', 'r') as f:
            parent = f.read().strip()
    else:
        parent = None
    commit_data = {
        'message': message,
        'files': index,
        'timestamp': int(os.path.getmtime('.chrono/index.json')),
        'parent': parent
    }
    commit_hash = hashlib.sha1(json.dumps(commit_data).encode()).hexdigest()
    commit_path = f'.chrono/commits/{commit_hash}.json'
    with open(commit_path, 'w') as f:
        json.dump(commit_data, f, indent=4, sort_keys=True)
    with open('.chrono/HEAD', 'w') as f:
        f.write(commit_hash)
    with open('.chrono/json', 'w') as f:
        json.dump({}, f)
    print(f"Commit created: {commit_hash} with message: '{message}'")

def log():
    with open('.chrono/HEAD', 'r') as f:
        current_commit = f.read().strip()
    while current_commit:
        commit_path = f'.chrono/commits/{current_commit}.json'
        if not os.path.exists(commit_path):
            break
        with open(commit_path, 'r') as f:
            commit_data = json.load(f)
        print(f"Commit: {current_commit}")
        print(f"Message: {commit_data['message']}")
        print(f"Timestamp: {commit_data['timestamp']}")
        print("-" * 40)
        current_commit = commit_data['parent']
    if not current_commit:
        print("No commits found.")
# Example usage:
# add('example.txt')
# commit(' something didn\'t work')
log()



