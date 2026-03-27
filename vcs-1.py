#in this we will create our db in to the system namly
#.chrono/ and in that two folders objects/ , commits/ 
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
# Example usage:
add('example.txt')



