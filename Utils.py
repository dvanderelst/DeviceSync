from sync_config import PROJECTS
from pathlib import Path

def select_project():
    while True:
        print("\nSelect a project to sync:\n")
        for i, name in enumerate(PROJECTS):
            print(f"{i+1}. {name}")
        print("0. Cancel")

        try:
            choice = int(input("\nEnter number: "))
            if choice == 0:
                return None, None, None

            project_name = list(PROJECTS.keys())[choice - 1]
        except (ValueError, IndexError):
            print("Invalid selection. Please try again.\n")
            continue

        origin = PROJECTS[project_name]['origin']
        target = PROJECTS[project_name]['target']

        print(f"\n[✓] You selected: {project_name}")
        print(f"    Origin: {origin}")
        print(f"    Target: {target}")

        confirm = input("\nConfirm selection? [Y/n]: ").strip().lower()
        if confirm in ('', 'y', 'yes'):
            return project_name, origin, target
        else:
            print("\n↩️  Going back to selection...\n")


def check_folders_exist(origin, target):
    origin_exists = Path(origin).exists()
    target_exists = Path(target).exists()

    if not origin_exists:
        print(f"[✗] Origin folder does not exist: {origin}")
    if not target_exists:
        print(f"[✗] Target folder does not exist: {target}")

    return origin_exists and target_exists

