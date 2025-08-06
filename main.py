#!/usr/bin/env python3

import Utils
import Sync

both_exist = False
while not both_exist:
    project_name, origin, target = Utils.select_project()
    both_exist = Utils.check_folders_exist(origin, target)
print('Starting sync...')
Sync.sync_loop(origin, target)