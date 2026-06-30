import json
import os
from constants import COMMITS_DIR,CHRONO_DIR, OBJECTS_DIR,INDEX_FILE,HEAD_FILE
def init():
    print(f"Initializing Chrono repository... in {os.getcwd()}")
    if not os.path.exists(CHRONO_DIR):
        os.makedirs(OBJECTS_DIR)
        os.makedirs(COMMITS_DIR)
        with open(INDEX_FILE, 'w') as f:
            json.dump({}, f)
        with open(HEAD_FILE, 'w') as f:
            f.write('')
        print("Chrono repository initialized.")
    else:
        print("Chrono repository already exists.")