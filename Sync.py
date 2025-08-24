import subprocess
from datetime import datetime
from pathlib import Path
import Config

def quote_arg(a: str) -> str:
    """Minimal shell-style quoting for transparency when printing commands."""
    if any(c in a for c in " \t\n'\"*$[]?{}()|&;<>`\\"):
        return "'" + a.replace("'", "'\\''") + "'"
    return a

def rsync_update(temp_dir, backup_dir):
    excluded_folders=Config.excluded_folders
    excluded_files=Config.excluded_files
    exclude_hidden=Config.exclude_hidden
    cfg_trash = Config.cfg_trash
    progress = Config.progress
    use_checksum = Config.use_checksum

    src = (Path(temp_dir).resolve().as_posix() + "/")  # copy contents
    dst_path = Path(backup_dir).resolve()
    dst = dst_path.as_posix()
    # Ensure backup dir exists
    dst_path.mkdir(parents=True, exist_ok=True)

    # Trash bucket (timestamped)
    trash_root = Path(cfg_trash)
    if not trash_root.is_absolute(): trash_root = dst_path / cfg_trash
    trash_root.mkdir(parents=True, exist_ok=True)
    trash_bucket = trash_root / datetime.now().strftime("%Y%m%d-%H%M%S")
    trash_bucket.mkdir(parents=True, exist_ok=True)

    # Build rsync command
    cmd = ["rsync", "-aHAX", "--delete", "--backup", f"--backup-dir={str(trash_bucket)}"]
    # Safer output verbosity
    if progress: cmd += ["--itemize-changes", "--info=stats2,progress2"]
    # Exclude the trash folder itself (protect from --delete)
    protect = trash_root.relative_to(dst_path).as_posix().rstrip('/') + '/'
    cmd += [f"--filter=P {protect}"]
    # Exclude hidden files/dirs anywhere
    if exclude_hidden: cmd += ["--exclude=.*", "--exclude=*/.*"]
    # Exclude directory patterns (match anywhere)
    for d in excluded_folders: cmd += [f"--exclude={d}", f"--exclude={d}/**"]
    # Exclude file patterns (match anywhere; glob patterns allowed)
    for f in excluded_files: cmd += [f"--exclude={f}"]
    # Content checksum mode (slower; reads both sides)
    if use_checksum: cmd.append("--checksum")

    #todo: maybe add dry_run option to config?
    #if dry_run: cmd.append("-n")  # no changes, just report

    # Finally add endpoints
    cmd += [src, dst]
    with open("rsync_command.txt", "w") as f: f.write(str(cmd))
    # Print and run
    # print("[cmd]", " ".join(quote_arg(a) for a in cmd))
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"rsync failed with exit code {e.returncode}") from e
    return str(trash_bucket)



