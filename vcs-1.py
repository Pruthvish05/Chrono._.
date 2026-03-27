#in this we will create our db in to the system namly
#.chrono/ and in that two folders objects/ , commits/ 
import os
import json
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