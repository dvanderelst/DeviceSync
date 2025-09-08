# exclude_folders/files are comma-separated strings
# They specify folder and file names that will not be deleted in the target
# Even if they are deleted/not present in the origin


PROJECTS = {
    "HydraPurr TEST": {
        "origin": "/media/dieter/CIRCUITPY",
        "target": "/home/dieter/Desktop/TESTCP/source_backup",
        "excluded_folders": ".idea,__pycache__,.git",
        "excluded_files": "README.md,notes.txt"
    },
    "HydraPurr": {
        "origin": "/media/dieter/CIRCUITPY",
        "target": "/home/dieter/Dropbox/PythonRepos/HydraPurr/BoardCode",
        "excluded_folders": ".idea,__pycache__,.git",
        "excluded_files": "README.md,notes.txt"
    },
    "CircuitExperiment": {
        "origin": "PLACE HOLDER",
        "target": "PLACE HOLDER",
        "excluded_folders": ".idea,__pycache__,.git",
        "excluded_files": "README.md,notes.txt"
    }
}
