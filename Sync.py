import os
import shutil
import time
from pathlib import Path


def sync_loop(origin, target, excluded_folders=None, excluded_files=None, interval=5):
    print(f"\n[✓] Syncing every {interval} seconds. Press Ctrl+C to stop.\n")
    try:
        while True:
            print("[🔁] Checking for changes...")
            files_copied = copy_updated_files(origin, target)
            # check whether origin can still be accessed
            # if not, skip deletion step
            if Path(origin).exists():
                files_deleted, dirs_deleted = remove_deleted_files(origin, target, excluded_folders, excluded_files)
            else:
                print(f"[⚠] Origin folder not accessible. Skipping deletion step.")
                files_deleted, dirs_deleted = 0, 0
            print(f"[✔] {files_copied} copied, {files_deleted} deleted, {dirs_deleted} dirs removed.")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n[✋] Sync stopped by user.")


def copy_updated_files(origin, target, exclude_hidden=True):
    origin = Path(origin)
    target = Path(target)

    files_copied = 0

    for root, dirs, files in os.walk(origin):
        rel_root = Path(root).relative_to(origin)
        target_root = target / rel_root
        target_root.mkdir(parents=True, exist_ok=True)

        for name in files:
            if exclude_hidden and name.startswith("."):
                continue

            origin_file = Path(root) / name
            target_file = target_root / name

            try:
                if not target_file.exists() or os.path.getmtime(origin_file) > os.path.getmtime(target_file):
                    shutil.copy2(origin_file, target_file)
                    print(f"[→] {origin_file.relative_to(origin)}")
                    files_copied += 1
            except Exception as e:
                print(f"[!] Failed to copy {origin_file}: {e}")

    return files_copied


def remove_deleted_files(
    origin,
    target,
    excluded_folders=None,
    excluded_files=None,
    exclude_hidden=True,
    trash_folder=".sync_trash"
):
    """
    Removes files and folders in `target` that no longer exist in `origin`.
    Instead of deleting them, moves them to a .sync_trash folder in `target`.

    Args:
        origin (str or Path): Origin folder to compare against.
        target (str or Path): Target folder to clean.
        excluded_folders (list): Folder names in target to skip (e.g., ['.idea']).
        excluded_files (list): File names in target to skip (e.g., ['README.md']).
        exclude_hidden (bool): Whether to skip hidden files/folders (and their contents).
        trash_folder (str): Folder in `target` where deletions are stored.
    """
    origin = Path(origin)
    target = Path(target)
    trash = target / trash_folder
    trash.mkdir(parents=True, exist_ok=True)

    if excluded_folders is None:
        excluded_folders = []
    if excluded_files is None:
        excluded_files = []

    excluded_folder_set = set(excluded_folders) | {trash_folder}
    excluded_file_set = set(excluded_files)

    files_moved = 0
    dirs_moved = 0

    for root, dirs, files in os.walk(target, topdown=False):
        rel_root = Path(root).relative_to(target)

        # ⛔ Skip entire folder tree if any part is hidden or excluded
        if (
            (exclude_hidden and any(part.startswith(".") for part in rel_root.parts)) or
            (rel_root.parts and rel_root.parts[0] in excluded_folder_set)
        ):
            print(f"[⏩] Skipping hidden or excluded path: {rel_root}")
            continue

        origin_root = origin / rel_root

        # Move deleted files to trash
        for name in files:
            if name in excluded_file_set:
                print(f"[⏩] Skipping excluded file: {Path(root) / name}")
                continue
            if exclude_hidden and name.startswith("."):
                print(f"[⏩] Skipping hidden file: {Path(root) / name}")
                continue

            target_file = Path(root) / name
            origin_file = origin_root / name

            if not origin_file.exists():
                rel_path = target_file.relative_to(target)
                trash_path = trash / rel_path
                trash_path.parent.mkdir(parents=True, exist_ok=True)
                try:
                    shutil.move(str(target_file), str(trash_path))
                    print(f"[🗑] Moved to trash: {rel_path}")
                    files_moved += 1
                except Exception as e:
                    print(f"[!] Failed to move {target_file}: {e}")

        # Move deleted folders to trash
        for name in dirs:
            if name in excluded_folder_set:
                print(f"[⏩] Skipping excluded folder: {Path(root) / name}")
                continue
            if exclude_hidden and name.startswith("."):
                print(f"[⏩] Skipping hidden folder: {Path(root) / name}")
                continue

            target_dir = Path(root) / name
            origin_dir = origin_root / name

            if not origin_dir.exists():
                rel_path = target_dir.relative_to(target)
                trash_path = trash / rel_path
                try:
                    shutil.move(str(target_dir), str(trash_path))
                    print(f"[🗑] Moved folder to trash: {rel_path}/")
                    dirs_moved += 1
                except Exception as e:
                    print(f"[!] Failed to move folder {target_dir}: {e}")

    return files_moved, dirs_moved
