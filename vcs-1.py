
#am also tryna build a habit of writing comments and code in modules so that it can be easily read and maintained in future
import os
import json
import hashlib
import difflib
#in this we will create our db in to the system namly
#.chrono/ and in that two folders objects/ , commits/ 
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
#this is a function that well as the name suggests adds a file lol
#to the area u gotta create the file before hand though.
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
#commits the message and the files in which you are working not cool yet,
#more work is needed.
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
#this function logs onto all the commits u have made
#needs some touches it works for now though
def log():
    with open('.chrono/HEAD', 'r') as f:
        current_commit = f.read().strip()
    if not current_commit:
        print("No commits found.")
        return
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
#THE TIME-TRAVEL as i call it just delets the presnt for of file
#and transports the type of file you wanted to the present
#depends on your hash to be honest!
def checkout(commit_hash):
    if not os.path.exists(f'.chrono/commits/{commit_hash}.json'):
        print(f"Commit '{commit_hash}' does not exist.")
        return
    with open(f'.chrono/commits/{commit_hash}.json', 'r') as f:
        commit_data = json.load(f)
    files = commit_data['files']
    for file in os.listdir():
        if file == '.chrono':
            continue
        if file in files and os.path.isfile(file):
            os.remove(file)
    for filepath, file_hash in files.items():
        object_path = f'.chrono/objects/{file_hash}'
        if os.path.exists(object_path):
            with open(object_path, 'rb') as f:
                content = f.read()
            with open(filepath, 'wb') as f:
                f.write(content)
    with open('.chrono/HEAD', 'w') as f:
        f.write(commit_hash)
    print(f"Checked out commit: {commit_hash}")
    print(f"Restored files: {', '.join(files.keys())}")
    print(f"THIS WILL OVERWRITE CURRENT FILES IN THE DIRECTORY, MAKE SURE TO COMMIT YOUR CHANGES BEFORE CHECKING OUT ANOTHER COMMIT.")
def diff():
    # Implementation for diff functionality
    if not os.path.exists('.chrono/HEAD'):
        print("No commits found.")
        return
    with open('.chrono/HEAD', 'r') as f:
        current_commit = f.read().strip()
    if not current_commit:
        print("No commits found.")
        return
    with open(f'.chrono/commits/{current_commit}.json', 'r') as f:
        commit_data = json.load(f)
    for filepath, file_hash in commit_data['files'].items():
        object_path = f'.chrono/objects/{file_hash}'
        if os.path.exists(object_path):
            with open(object_path, 'rb') as f:
                content = f.read().decode()
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    current_content = f.read()
                diff = difflib.unified_diff(
                    current_content.splitlines(),
                    content.splitlines(),
                    fromfile='current',
                    tofile='commit',
                    lineterm=''
                )
                print(f"Diff for {filepath}:")
                print('\n'.join(diff))
            else:
                print(f"File '{filepath}' does not exist in the current directory.")
# Example usage:
# init()
# add('example.txt')
# commit(' something didn\'t work')
#log()
#add('example-2.txt')
#commit(' added example-2.txt')
# log()
# checkout('3b987a609cb70d580369da0049e396ed0dac20cc')




