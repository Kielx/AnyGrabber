import hashlib
from datetime import datetime
import shutil

import dateutil.parser as dparser
import os
import re

# Search string in the log file that is used to identify the line that contains the login information
search_string = 'Logged in from '


def get_anydesk_logs(filepath: str) -> list[str] | None:
    """A function that reads a file and returns a list of strings that contain login information

    :param filepath: a path to a file that contains Anydesk logs
    :return: a list of strings that contain login information or None if file doesn't exist
    """
    try:
        with open(filepath, 'r') as f:
            log_entries = []
            for l_no, line in enumerate(f):
                # search string
                if search_string in line:
                    before_keyword, keyword, after_keyword = line.partition(search_string)
                    last_dot = after_keyword.rfind(' on relay')
                    after_keyword = after_keyword[0: last_dot]
                    date_of_login = dparser.parse(before_keyword[0:30], fuzzy=True)
                    date_of_login = date_of_login.strftime("%d/%m/%Y, %H:%M:%S")
                    log_entries.append(date_of_login + "  -  " + after_keyword)
        return log_entries
    except IOError:
        return None


def create_timestamped_directory() -> str:
    """A function that creates a directory with a timestamp and computer name in the folder name

    :return: folder path
    """

    # Get the current working directory
    cwd = os.getcwd()

    # Get the computer name
    computer_name = os.environ['COMPUTERNAME']

    folder_path = f'{cwd}\\REPORTS\\{computer_name}_{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}'

    # Create a directory with a timestamp and computer name in the folder name
    os.makedirs(folder_path, exist_ok=True)

    return folder_path


def create_folders_from_path(s, folder_path):
    # Use regular expression to match folder names
    pattern = r"[\\/]?([^\\/]+)[\\/]"
    matches = re.findall(pattern, s)
    # Create folders and subfolders in the specified directory
    path = folder_path
    for folder in matches:
        path = os.path.join(path, folder)
        if not os.path.exists(path):
            os.makedirs(path)

    return path


def generate_md5_file_checksum(filename: str):
    with open(filename, "rb") as f:
        file_hash = hashlib.md5()
        while chunk := f.read(8192):
            file_hash.update(chunk)
    # print(file_hash.digest())
    # print(file_hash.hexdigest())  # to get a printable str instead of bytes
    return file_hash.hexdigest()


def copy_and_generate_checksum(source_file: str, destination_folder_path: str) -> str:
    """A function that copies a file to a destination folder and generates a checksum for it"""
    try:
        shutil.copy2(source_file, destination_folder_path)
        md5_checksum = generate_md5_file_checksum(source_file)
        f = open(destination_folder_path + "\\checksum.txt", "w")
        f.write(md5_checksum)
        f.close()
    except IOError:
        print("Error occurred when trying to copy")
