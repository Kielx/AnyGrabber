import csv
import hashlib
import os
import platform
import socket
import re
import shutil
from datetime import datetime

import dateutil.parser as dparser

# Search string in the log file that is used to identify the line that contains the login information
search_string = 'Logged in from '


def get_computer_name():
    system_name = platform.system()
    if system_name == 'Windows':
        # Get the computer name on Windows
        computer_name = os.environ['COMPUTERNAME']
    elif system_name == 'Linux':
        # Get the computer name on Linux
        fqdn = socket.getfqdn()
        computer_name = fqdn.split('.')[0]
    elif system_name == 'Darwin':
        # Get the computer name on macOS
        hostname = socket.gethostname()
        computer_name = hostname.split('.')[0]
    else:
        # Unsupported operating system
        raise NotImplementedError("Operating system not supported")

    return computer_name


def get_anydesk_logs(filepath: str) -> dict[str, str] | None:
    """A function that reads a file and returns a list of strings that contain login information

    :param filepath: a path to a file that contains Anydesk logs
    :return: a dict with dates as keys and IP's as values that contain login information or None if file doesn't exist
    """
    try:
        with open(filepath, 'r') as f:
            log_entries = {}
            for l_no, line in enumerate(f):
                if search_string in line:
                    before_keyword, keyword, after_keyword = line.partition(search_string)
                    last_dot = after_keyword.rfind(' on relay')
                    after_keyword = after_keyword[0: last_dot]
                    date_of_login = dparser.parse(before_keyword[0:30], fuzzy=True)
                    date_of_login = date_of_login.strftime("%d/%m/%Y, %H:%M:%S")
                    log_entries[date_of_login] = after_keyword
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
    computer_name = get_computer_name()

    folder_path = f'{cwd}\\REPORTS\\{computer_name}_{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}'

    # Create a directory with a timestamp and computer name in the folder name
    os.makedirs(folder_path, exist_ok=True)

    return folder_path


def create_folders_from_path(s, folder_path):
    """A function that creates folders and subfolders from a path

    :param s: a path to a file
    :param folder_path: a path to a folder where the folders will be created
    :return: a path to the last folder created
    """

    # Use regular expression to match folder names
    pattern = r"(?:[A-Za-z]:[\\/])?([^\\/]+)[\\/]"
    matches = re.findall(pattern, s)
    # Create folders and subfolders in the specified directory
    path = folder_path
    for folder in matches:
        path = os.path.join(path, folder)
        if not os.path.exists(path):
            os.makedirs(path)

    return path


def generate_md5_file_checksum(filename: str) -> str:
    with open(filename, "rb") as f:
        file_hash = hashlib.md5()
        while chunk := f.read(8192):
            file_hash.update(chunk)
    # print(file_hash.digest())
    # print(file_hash.hexdigest())  # to get a printable str instead of bytes
    return file_hash.hexdigest()


def copy_and_generate_checksum(source_file: str, destination_folder_path: str) -> None:
    """A function that copies a file to a destination folder and generates a checksum for it"""
    try:
        shutil.copy2(source_file, destination_folder_path)
        md5_checksum = generate_md5_file_checksum(source_file)
        file_path = os.path.join(destination_folder_path, 'checksum.txt')
        f = open(file_path, "w")
        f.write(md5_checksum)
        f.close()
    except IOError:
        print("Error occurred when trying to copy")


def generate_txt_report(report_directory_path: str, write_header: bool = True,
                        anydesk_logs_dict: dict[str, str] | None =
                        None, filename: str | None = None
                        ) -> None:
    """A function that generates a report in the specified directory"""

    computer_name = get_computer_name()
    current_datetime = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    actual_path = os.path.join(report_directory_path, 'report.txt')

    with open(actual_path, "a") as f:
        if write_header:
            f.write(f"Report for {computer_name} generated on {current_datetime} \r\n")
            f.write("-------------------------------------------------- \r\n")
        if anydesk_logs_dict == {} or anydesk_logs_dict is None:
            f.write(f'No Anydesk logs found in file {filename} \r\n')
        else:
            f.write(f'Anydesk logs from file {filename} : \r\n')
            for entry in anydesk_logs_dict:
                f.write(entry + " - " + anydesk_logs_dict[entry] + "\r\n")


def generate_csv_report(report_directory_path: str, write_header: bool = True, anydesk_logs_dict: dict[str,
str] | None = None, filename: str | None = None
                        ) -> None:
    """A function that generates a report in the specified directory"""
    report_path = os.path.join(report_directory_path, 'report.csv')
    with open(report_path, "a", newline='') as f:
        writer = csv.writer(f, delimiter=',')
        if write_header:
            writer.writerow(['Date', 'IP', 'File'])
        if anydesk_logs_dict == {} or anydesk_logs_dict is None:
            writer.writerow(["No Anydesk logs found!", "", filename])
        else:
            for entry in anydesk_logs_dict:
                writer.writerow([entry, anydesk_logs_dict[entry], filename])
