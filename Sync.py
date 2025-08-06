import os
import shutil
import time
from pathlib import Path


def sync_loop(origin, target, interval=5):
    print(f"\n[✓] Syncing every {interval} seconds. Press Ctrl+C to stop.\n")
    try:
        while True:
            print("[🔁] Checking for changes...")
            files_copied = copy_updated_files(origin, target)
            files_deleted, dirs_deleted = remove_deleted_files(origin, target)

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

def remove_deleted_files(origin, target, exclude_hidden=True, trash_folder=".sync_trash"):
    origin = Path(origin)
    target = Path(target)
    trash = target / trash_folder
    trash.mkdir(parents=True, exist_ok=True)

    files_moved = 0
    dirs_moved = 0

    for root, dirs, files in os.walk(target, topdown=False):  # bottom-up to allow folder removal
        rel_root = Path(root).relative_to(target)

        # ⛔ Skip the trash folder itself and its contents
        if rel_root.parts and rel_root.parts[0] == trash_folder:
            continue

        origin_root = origin / rel_root

        # Move deleted files to trash
        for name in files:
            if exclude_hidden and name.startswith("."):
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
            if exclude_hidden and name.startswith("."):
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


# def remove_deleted_files(origin, target, exclude_hidden=True):
#     origin = Path(origin)
#     target = Path(target)
#
#     files_deleted = 0
#     dirs_deleted = 0
#
#     for root, dirs, files in os.walk(target, topdown=False):  # bottom-up to remove empty dirs
#         rel_root = Path(root).relative_to(target)
#         origin_root = origin / rel_root
#
#         # Delete files not in origin
#         for name in files:
#             if exclude_hidden and name.startswith("."):
#                 continue
#
#             target_file = Path(root) / name
#             origin_file = origin_root / name
#
#             if not origin_file.exists():
#                 try:
#                     target_file.unlink()
#                     print(f"[×] {target_file.relative_to(target)}")
#                     files_deleted += 1
#                 except Exception as e:
#                     print(f"[!] Failed to delete {target_file}: {e}")
#
#         # Delete empty dirs not in origin
#         for name in dirs:
#             target_dir = Path(root) / name
#             origin_dir = origin_root / name
#
#             if not origin_dir.exists():
#                 try:
#                     shutil.rmtree(target_dir)
#                     print(f"[×] {target_dir.relative_to(target)}/")
#                     dirs_deleted += 1
#                 except Exception as e:
#                     print(f"[!] Failed to delete {target_dir}: {e}")
#
#     return files_deleted, dirs_deleted
