# main.py
import time
from pathlib import Path
import PortMenu
import FolderMenu
import Rshell
import Utils
import Sync

device = None
full_temp_folder = None
backup_folder = None

# ---------------------------
# Step 1: Select serial port
# ---------------------------
confirmation = 'n'
while confirmation != 'y':
    selected_port = PortMenu.select_port()
    device = selected_port['device']
    description = selected_port['description'] or "No description"
    print(f"Selected port: {description} on {device}")
    confirmation = input("Confirm selection (y/n): ").strip().lower()

print("Creating empty temp folder for rshell mirror...")
full_temp_folder = Utils.ensure_folder(empty=True)
print("Temp folder:", full_temp_folder)

# ---------------------------
# Step 2: Select backup folder
# ---------------------------
confirmation = 'n'
while confirmation != 'y':
    backup_folder = FolderMenu.select_backup_folder()
    backup_folder = Path(backup_folder).expanduser().resolve()
    print(f"Selected target folder: {backup_folder}")
    confirmation = input("Confirm selection (y/n): ").strip().lower()

print("Backup folder set to:", backup_folder)

# ---------------------------
# Step 3: Continuous sync loop
# ---------------------------
while True:
    print("\n" + "=" * 60)
    print(time.asctime())
    print("Trying to mirror the board contents...")
    ok, out, err = Rshell.rshell_mirror(device, dest_folder=full_temp_folder, dry_run=False, quiet=False)
    if not ok:
        print(f"[WARN] Could not mirror: {err}")
    else:
        trash_path = Sync.rsync_update(temp_dir=full_temp_folder, backup_dir=backup_folder)
    print('Done!')
    input("Press Enter to repeat...")