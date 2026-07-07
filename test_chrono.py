import os
import json
import shutil
import sys
import unittest
import repository
import objects
import commits
import checkout
import constants
# constants.CHRONO_DIR = os.path.join(".chrono_test",".chrono")
# constants.INDEX_FILE = os.path.join(constants.CHRONO_DIR, "index.json")
# constants.HEAD_FILE = os.path.join(constants.CHRONO_DIR, "HEAD")
# constants.COMMITS_DIR = os.path.join(constants.CHRONO_DIR, "commits")
class TestChronoVCS(unittest.TestCase):
    def setUp(self):
        self.test_dir = ".chrono_test"
        test_chrono_dir = os.path.join(self.test_dir, ".chrono")
        
        # 1. Update the base constants module
        constants.CHRONO_DIR = test_chrono_dir
        constants.OBJECTS_DIR = os.path.join(test_chrono_dir, "objects")
        constants.COMMITS_DIR = os.path.join(test_chrono_dir, "commits")
        constants.INDEX_FILE = os.path.join(test_chrono_dir, "index.json")
        constants.HEAD_FILE = os.path.join(test_chrono_dir, "HEAD")

        # 2. FORCE the updated paths into your individual modules directly
        import repository, objects, commits, checkout
        
        for module in [repository, objects, commits, checkout]:
            if hasattr(module, 'CHRONO_DIR'): constants.CHRONO_DIR = constants.CHRONO_DIR
            if hasattr(module, 'OBJECTS_DIR'): constants.OBJECTS_DIR = constants.OBJECTS_DIR
            if hasattr(module, 'COMMITS_DIR'): constants.COMMITS_DIR = constants.COMMITS_DIR
            if hasattr(module, 'INDEX_FILE'): constants.INDEX_FILE = constants.INDEX_FILE
            if hasattr(module, 'HEAD_FILE'): constants.HEAD_FILE = constants.HEAD_FILE

        # 3. Clean and build the fresh sandbox directory structure
        os.makedirs(self.test_dir, exist_ok=True)
        repository.init()

    def test_repository_initialization(self):
        self.assertTrue(os.path.exists(constants.CHRONO_DIR))
        self.assertTrue(os.path.exists(constants.OBJECTS_DIR))
        self.assertTrue(os.path.exists(constants.COMMITS_DIR))
        self.assertTrue(os.path.exists(constants.INDEX_FILE))
        self.assertTrue(os.path.exists(constants.HEAD_FILE))

    def test_add_and_commit_snapshot_flow(self):
        file_path = os.path.join(self.test_dir, "hello.txt")
        with open(file_path, "w") as f:
            f.write("Hello Chrono World!")
        objects.add(file_path)

        with open(constants.INDEX_FILE, "r") as f:
            index = json.load(f)
        self.assertIn(file_path, index)
        staged_hash = index[file_path]
        commit_hash = commits.commit("First test snapshot")
        with open(constants.INDEX_FILE, "r") as f:
            post_index = json.load(f)
        self.assertEqual(post_index, {})
        with open(constants.HEAD_FILE, "r") as f:
            current_head = f.read().strip()
        self.assertEqual(current_head, commit_hash)
        commit_file_path = os.path.join(constants.COMMITS_DIR, f"{commit_hash}.json")
        with open(commit_file_path, "r") as f:
            commit_data = json.load(f)
        self.assertEqual(commit_data["message"], "First test snapshot")
        self.assertEqual(commit_data["files"][file_path], staged_hash)

    def test_unmodified_files_persist_across_snapshots(self):
        file_a = os.path.join(self.test_dir, "file_a.txt")
        with open(file_a, "w") as f:
            f.write("File A data")
        objects.add(file_a)
        commit1_hash = commits.commit("Commit 1")
        file_b = os.path.join(self.test_dir, "file_b.txt")
        with open(file_b, "w") as f:
            f.write("File B data")
        objects.add(file_b)
        commit2_hash = commits.commit("Commit 2")
        commit2_path = os.path.join(constants.COMMITS_DIR, f"{commit2_hash}.json")
        with open(constants.INDEX_FILE, "r") as f:
            commit2_data = json.load(f)
        self.assertIn(file_a, commit2_data["files"])
        self.assertIn(file_b, commit2_data["files"])
        self.assertEqual(commit2_data["parent"], commit1_hash)

if __name__ == "__main__":
    unittest.main(argv=[sys.argv[0]], verbosity=2, exit=False)