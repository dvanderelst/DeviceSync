# Sync.py
# Wrapper around rsync to copy updates from temp -> backup,
# honoring ignores and keeping deleted/overwritten files in a trash folder.

import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

# Optional: pull defaults from your Config if present
try:
    import Config  # noqa: F401
    _CFG = {
        "trash_folder": getattr(Config, "trash_folder", ".trash"),
        "exclude_hidden": bool(getattr(Config, "exclude_hidden", False)),
        "excluded_folders": list(getattr(Config, "excluded_folders", []) or []),
        "excluded_files": list(getattr(Config, "excluded_files", []) or []),
        "use_hash": bool(getattr(Config, "use_hash", False)),  # maps to --checksum
    }
except Exception:
    _CFG = {
        "trash_folder": ".trash",
        "exclude_hidden": False,
        "excluded_folders": [],
        "excluded_files": [],
        "use_hash": False,
    }

def rsync_update(temp_dir: str,
                 backup_dir: str,
                 ignore_dirs=None,
                 ignore_files=None,
                 exclude_hidden=None,
                 checksum=None,
                 dry_run: bool = False,
                 progress: bool = True) -> str:
    """
    Sync temp_dir -> backup_dir using rsync, keeping deletions/overwrites in a trash bucket.

    Args:
        temp_dir: source (its *contents* are copied; trailing slash enforced)
        backup_dir: destination directory
        ignore_dirs: list of directory patterns to exclude (match anywhere), e.g. ["build", "node_modules"]
        ignore_files: list of file patterns to exclude (match anywhere), e.g. [".DS_Store", "*.tmp"]
        exclude_hidden: if True, exclude dotfiles/dirs anywhere ('.*' and '*/.*'); defaults to Config or False
        checksum: if True, use --checksum (content hashing). Defaults to Config.use_hash or False
        dry_run: if True, add -n (no changes), print what would happen
        progress: if True, print rsync progress/stats

    Returns:
        The path to the trash bucket used for this run.
    """
    if shutil.which("rsync") is None:
        raise RuntimeError("rsync not found on PATH. Please install rsync.")

    src = str(Path(temp_dir).resolve()) + "/"   # copy contents
    dst = str(Path(backup_dir).resolve())       # target dir

    # Defaults (Config fallback)
    if exclude_hidden is None:
        exclude_hidden = _CFG["exclude_hidden"]
    if checksum is None:
        checksum = _CFG["use_hash"]

    # Ignores (merge with Config)
    ignore_dirs = list((_CFG["excluded_folders"] or [])) + list(ignore_dirs or [])
    ignore_files = list((_CFG["excluded_files"] or [])) + list(ignore_files or [])

    # Trash bucket (timestamped)
    trash_root = Path(dst, _CFG["trash_folder"])
    trash_bucket = trash_root / datetime.now().strftime("%Y%m%d-%H%M%S")
    trash_bucket.parent.mkdir(parents=True, exist_ok=True)  # ensure .trash exists

    # Build rsync command
    cmd = ["rsync", "-aHAX", "--delete", "--backup", f"--backup-dir={str(trash_bucket)}"]

    # Safer output verbosity
    if progress:
        cmd += ["--itemize-changes", "--info=stats2,progress2"]

    # Exclude the trash folder itself (protect from --delete)
    cmd += [f"--exclude=/{_CFG['trash_folder']}/**"]

    # Exclude hidden files/dirs anywhere
    if exclude_hidden:
        cmd += ["--exclude=.*", "--exclude=*/.*"]

    # Exclude directory patterns (match anywhere)
    for d in ignore_dirs:
        # Exclude both the dir itself and its subtree anywhere it appears
        cmd += [f"--exclude={d}", f"--exclude={d}/**"]

    # Exclude file patterns (match anywhere; glob patterns allowed)
    for f in ignore_files:
        cmd += [f"--exclude={f}"]

    # Content checksum mode (slower; reads both sides)
    if checksum:
        cmd.append("--checksum")

    if dry_run:
        cmd.append("-n")  # no changes, just report

    # Finally add endpoints
    cmd += [src, dst]

    # Print and run
    print("[cmd]", " ".join(quote_arg(a) for a in cmd))
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"rsync failed with exit code {e.returncode}") from e

    return str(trash_bucket)

def quote_arg(a: str) -> str:
    """Minimal shell-style quoting for transparency when printing commands."""
    if any(c in a for c in " \t\n'\"*$[]?{}()|&;<>`\\"):
        return "'" + a.replace("'", "'\\''") + "'"
    return a

# --- Convenience aliases (optional) ---

def sync_temp_to_backup(temp_dir: str, backup_dir: str,
                        ignore_dirs=None, ignore_files=None,
                        dry_run: bool = False) -> str:
    """
    Opinionated defaults: exclude hidden, no checksum, progress on.
    """
    return rsync_update(
        temp_dir=temp_dir,
        backup_dir=backup_dir,
        ignore_dirs=ignore_dirs,
        ignore_files=ignore_files,
        exclude_hidden=True,
        checksum=False,
        dry_run=dry_run,
        progress=True,
    )
