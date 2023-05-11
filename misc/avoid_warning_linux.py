import fileinput
import os
import re
import sys
import getpass

def comment_lines(file_path, lines_to_comment):
    with fileinput.FileInput(file_path, inplace=True, backup='.bak') as file:
        for line_number, line in enumerate(file, start=1):
            if line_number in lines_to_comment:
                print(f"# {line}", end='')
            else:
                print(line, end='')


# Get the username of the current user
username = getpass.getuser()
# Get the user's Python version
python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
# Construct the path to the script based on the username and Python version
script_file = f"/home/{username}/anaconda3/envs/brainchulo/lib/python{python_version}/site-packages/chromadb/api/models/Collection.py"

# Specify the line numbers you want to comment (1-based index)
lines_to_comment = [51,52,53,54]  # Example: comment lines 4, 7, and 9

comment_lines(script_file, lines_to_comment)


# Remove the backup file created during processing
backup_file = f"{script_file}.bak"
if os.path.exists(backup_file):
    os.remove(backup_file)

