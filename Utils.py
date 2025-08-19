from pathlib import Path
import Config
import shutil


def ensure_folder(path=None, empty=False):
    """
    Ensure that a temporary folder exists.
    If empty=True, clear all contents of the folder.

    Returns the absolute Path object.
    """
    if path is None: path = Config.temp_folder
    folder = Path(path).expanduser().resolve()
    folder.mkdir(parents=True, exist_ok=True)

    if empty:
        for item in folder.iterdir():
            if item.is_file() or item.is_symlink():
                item.unlink(missing_ok=True)
            elif item.is_dir():
                shutil.rmtree(item, ignore_errors=True)

    return folder