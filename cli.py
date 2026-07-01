import sys
from repository import init
from objects import add
from commits import commit
from diff import diff
from checkout import checkout
from diff import diff

args = sys.argv
command = args[1] if len(args) > 1 else None
if command == "init":
    init()
elif command == "add":
    add(args[2])
elif command == "commit":
    commit(args[2])
elif command == "diff":
    diff(args[2])
elif command == "checkout":
    checkout(args[2])
elif command == "help":
    print("Available commands:")
    print("  init - Initialize a new repository")
    print("  add <file> - Add a file to the staging area")
    print("  commit <message> - Commit changes with a message")
    print("  diff <file> - Show differences for a file")
    print("  checkout <commit_id> - Checkout a specific commit")
elif command is None:
    print("No command provided. Use 'help' for available commands.")
elif command not in ["init", "add", "commit", "diff", "checkout", "help"]:
    print(f"Unknown command: {command}. Use 'help' for available commands.")