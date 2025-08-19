# BackupMenu.py
from pathlib import Path
import Config

def select_backup_folder(folders=None):
    """
    Show a numeric menu of existing folders. Returns the selected absolute Path or None.
    Assumes folders already exist. No auto-selection, no custom entry.
    """
    # Pre-resolve for display and existence check
    if folders is None: folders = Config.target_folders
    resolved = [Path(p).expanduser().resolve() for p in folders]

    while True:
        print("\nSelect a backup destination:")
        for i, p in enumerate(resolved):
            print(f"[{i}] {p}")

        choice = input("Enter number | q=cancel: ").strip().lower()
        if choice == "q":
            return None
        if choice.isdigit():
            idx = int(choice)
            if 0 <= idx < len(resolved):
                if resolved[idx].exists() and resolved[idx].is_dir():
                    return resolved[idx]
                else:
                    print("That folder does not exist or is not a directory. Try again.")
                    continue
        print("Invalid choice. Try again.")
