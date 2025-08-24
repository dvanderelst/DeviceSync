temp_folder = '~/Desktop/mcu_tmp'
target_folders = ['~/Desktop/final_backup', '~/Desktop/another_backup']
excluded_folders = ['System Volume Information']

# Rsync options
progress = True
use_checksum = True
excluded_files = []
exclude_hidden = True
cfg_trash = ".sync_trash"