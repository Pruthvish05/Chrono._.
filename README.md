# ⏳ Chrono

**A Version Control System built from scratch in Python to understand how Git works internally.**

Chrono is an educational implementation of a Version Control System (VCS). Instead of relying on Git libraries or copying Git's behavior blindly, Chrono implements the fundamental concepts behind modern version control systems from first principles.

The primary objective of this project is to gain a deep understanding of repository architecture, content-addressable storage, snapshots, commit history, and file restoration.

> **Current Version:** v1.0.0 (In Development)

---

# Features

## Repository Initialization

Initialize a new Chrono repository inside the current directory.

```bash
chrono init
```

Creates the following structure:

```text
.chrono/
├── objects/
├── commits/
├── index.json
└── HEAD
```

---

## Object Database

Chrono stores file contents separately from commit metadata.

Every file is:

```
File
   ↓
Read Contents
   ↓
SHA-1 Hash
   ↓
Stored inside objects/
```

Objects are immutable.

If two files contain identical data, only one copy is stored.

---

## Content Addressable Storage

Files are identified using SHA-1 hashes rather than filenames.

Example:

```
Hello World
        ↓
SHA-1
        ↓
a591a6d40bf420...
```

This minimizes duplicate storage and mirrors how Git stores objects.

---

## Staging Area

Files are staged before they become part of a commit.

```bash
chrono add filename.txt
```

The staging area is maintained inside:

```
.chrono/index.json
```

---

## Snapshot-Based Commits

Chrono stores project snapshots instead of line-by-line history.

Each commit contains:

- Commit message
- Timestamp
- Parent commit
- Mapping of tracked files to object hashes

Example:

```json
{
  "message": "Initial Commit",
  "timestamp": 1751234567,
  "files": {
    "main.py": "hash",
    "README.md": "hash"
  },
  "parent": ""
}
```

---

## Commit History

Traverse the complete commit history.

```bash
chrono log
```

Displays:

- Commit Hash
- Commit Message
- Timestamp

History is reconstructed by following parent commit references.

---

## Checkout (Time Travel)

Restore the working directory to any previous commit.

```bash
chrono checkout <commit_hash>
```

Checkout:

- Restores tracked files
- Updates HEAD
- Preserves repository history

---

## File Difference Viewer

Compare the current working directory with the latest committed snapshot.

```bash
chrono diff
```

Displays line-by-line differences using Python's `difflib`.

---

## Modular Architecture

Chrono follows a modular design.

```
chrono/
├── cli.py
├── repository.py
├── objects.py
├── commits.py
├── checkout.py
├── diff.py
├── constants.py
├── utils.py
└── __init__.py
```

Each module has a single responsibility, making the codebase easier to understand, test, and extend.

---

# Repository Architecture

```
Working Directory
        │
        ▼
add()
        │
        ▼
index.json (Staging Area)
        │
        ▼
commit()
        │
        ▼
commits/
        │
        ▼
HEAD
        │
        ▼
log() / checkout()
```

---

# Core Concepts Implemented

- Repository initialization
- Content-addressable object storage
- SHA-1 hashing
- Snapshot-based commits
- Parent commit chaining
- Staging area
- HEAD pointer
- Commit history traversal
- Repository checkout
- Unified file diff generation
- Modular software architecture

---

# Technologies Used

- Python 3
- `os`
- `json`
- `hashlib`
- `difflib`
- `time`

---

# Current Limitations

Chrono v1 intentionally focuses on local version control fundamentals.

The following features are **not** part of v1:

- Branches
- Merge
- Merge conflict resolution
- Remote repositories
- Push / Pull
- Clone
- Tags
- Ignore files (`.chronoignore`)
- Packfiles
- Object compression
- Garbage collection

These are planned for future versions.

---

# Educational Goals

Chrono is designed to teach:

- How a Version Control System works internally
- Repository architecture
- Snapshot-based history
- Object databases
- File hashing
- Commit graphs
- Data persistence
- Software architecture
- Modular Python design

---

# Future Roadmap

### v1

- Repository initialization
- Object database
- Staging area
- Snapshot commits
- Commit history
- Checkout
- Diff
- Modular architecture

### v2

- Branching
- Merge
- Merge conflict resolution
- Tags
- `.chronoignore`
- Improved CLI
- Better repository validation

### v3

- Remote repositories
- Push
- Pull
- Clone
- Object compression
- Packfiles
- Garbage collection

---

# License

This project is intended for educational and learning purposes.
