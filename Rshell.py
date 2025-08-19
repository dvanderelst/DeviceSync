# Rshell.py
import subprocess
from pathlib import Path

def print_rshell_output(stdout: str, stderr: str, show_checks=False):
    """Print rshell output, optionally filtering 'Checking' lines."""
    if stdout:
        for line in stdout.splitlines():
            if not show_checks and line.strip().startswith("Checking "):
                continue
            print(line)
    if stderr.strip():
        print("STDERR:", stderr.strip())

def rshell_mirror(port, dest_folder, dry_run=False, quiet=False):
    """
    Mirror the board's root contents into dest_folder using rshell rsync.
    Returns (success, stdout, stderr).

    success = True if copy worked, False if board was unavailable or rshell failed.
    """
    dest = Path(dest_folder).expanduser().resolve()
    dest.mkdir(parents=True, exist_ok=True)

    src = '/pyboard'
    cmd = ["rshell", "-p", port, "rsync", "-m", "-a"]
    if dry_run: cmd.append("-n")
    if quiet:   cmd.append("-q")
    cmd += [src, str(dest)]

    try:
        cp = subprocess.run(cmd, check=False, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError as e:
        return False, "", f"rshell not found: {e}"

    # Nonzero return code OR common error strings → treat as failure
    if cp.returncode != 0 or "could not open port" in cp.stderr.lower():
        msg = cp.stderr.strip() or f"rshell failed with rc={cp.returncode}"
        return False, cp.stdout, msg

    return True, cp.stdout, cp.stderr
