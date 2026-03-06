# exclude_folders/files are comma-separated strings
# They specify folder and file names that will not be deleted in the target
# Even if they are deleted/not present in the origin


PROJECTS = {
    "HydraPurr": {
        "origin": "/media/dieter/CIRCUITPY",
        "target": "/home/dieter/Dropbox/PythonRepos/HydraPurr/BoardCode",
        "excluded_folders": ".idea,__pycache__,.git",
        "excluded_files": "README.md,notes.txt"
    },
    "P&G model: joystick": {
        "origin": "/media/dieter/CIRCUITPY",
        "target": "/home/dieter/Dropbox/WorkStuff/PandG/code_model_joystick",
        "excluded_folders": ".idea,__pycache__,.git,.venv",
        "excluded_files": "README.md,notes.txt,cp_repl.sh"
    },
	"P&G model: swivel": {
	"origin": "/media/dieter/CIRCUITPY",
	"target": "/home/dieter/Dropbox/WorkStuff/PandG/code_model_swivel",
	"excluded_folders": ".idea,__pycache__,.git,.venv",
	"excluded_files": "README.md,notes.txt,cp_repl.sh"
    }
}
