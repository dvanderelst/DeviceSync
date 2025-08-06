# MicroPython/CircuitPython Code Sync Tool

This is a lightweight tool to keep code on MicroPython or CircuitPython boards continuously synced to a local folder on your computer.

## 🚀 Why?

- **Backup protection**: Code on the board is mirrored locally.
- **Version control**: The local folder can be part of a Git repo.
- **Peace of mind**: Deleted files are moved to a local `.sync_trash` instead of being removed immediately.

---

## 📦 Features

- Select from predefined origin/target pairs
- Sync runs in a loop (default: every 5 seconds)
- Files are only copied if modified
- Deleted files/folders are moved to a `.sync_trash` folder
- Skips hidden files and protects against recursive deletion

---

## 📁 Project Structure

```
.
├── main.py             # Main entry point
├── Sync.py             # Core syncing logic
├── Utils.py            # Project selection + folder checking
├── sync_config.py      # Stores your project paths
└── .sync_trash/        # (created automatically inside each target folder)
```

---

## ⚙️ Configuration

Edit `sync_config.py` to define your sync projects:

```python
PROJECTS = {
    "3PI_robot": {
        "origin": "/media/dieter/MICROPY",
        "target": "/home/dieter/Dropbox/PythonRepos/3PI_robot/robot_code"
    },
    "SensorBoard": {
        "origin": "PLACEHOLDER",
        "target": "PLACEHOLDER"
    }
}
```

---

## 🖥️ Usage

1. Make sure your board is mounted (and visible at the configured path).
2. Run the sync script:

```bash
./main.py
```

3. Choose a project when prompted.
4. Confirm the source and target.
5. The script will:
   - Copy new or modified files
   - Move deleted files/folders to `.sync_trash`

---

## 💡 Tips

- Make `main.py` executable:
  ```bash
  chmod +x main.py
  ```
- Add a desktop shortcut or shell alias for convenience.
- The target folder can be a Git repository to track code changes.

---

## 🛡️ Safety

- Deleted files are **not permanently removed**. They are moved to a `.sync_trash` folder inside the target directory.
- The `.sync_trash` folder is excluded from sync and deletion logic.
- You can manually empty `.sync_trash` later or build an auto-clean feature.

---
