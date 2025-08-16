#!/usr/bin/env python3

import Utils
import Sync

both_exist = False
while not both_exist:
    project_name, project = Utils.select_project()

    origin = project['origin']
    target = project['target']
    excluded_folders = project['excluded_folders']
    excluded_files = project['excluded_files']

    excluded_files = Utils.parse_exclusion_string(excluded_files)
    excluded_folders = Utils.parse_exclusion_string(excluded_folders)
    both_exist = Utils.check_folders_exist(origin, target)

print('Starting sync...')
Sync.sync_loop(origin, target, excluded_folders, excluded_files)