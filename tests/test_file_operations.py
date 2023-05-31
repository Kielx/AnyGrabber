import csv
import hashlib
import shutil
from datetime import datetime

from utils.file_operations import get_anydesk_logs, create_timestamped_directory, create_folders_from_path, \
    generate_md5_file_checksum, copy_and_generate_checksum, generate_txt_report, generate_csv_report, \
    split_computer_datetime_dirname, get_reports_folder_list
import os
import re
import sys

sys.path.append('../')


class TestGetAnydeskLogs:
    """Class for testing get_anydesk_logs functionality"""

    @staticmethod
    def create_empty_file(filename: str) -> str:
        """" Create an empty file
        :param filename: string representation of filename i.e 'anydesk.log'
        :return: name of created file
        """
        with open(filename, 'w'):
            pass
        return filename

    @staticmethod
    def create_anydesk_log_file(filename: str, file_content: str | None = None) -> str:
        """ Create testable anydesk log file with given filename and content passed as parameter.
            If no file content is provided then the default value is provided.
            :param filename: string representation of filename i.e 'anydesk.log'
            :param file_content: string representation of content, if not provided a mock log fragment is created inside
            :return: name of file created
        """
        with open(filename, 'w') as f:
            f.write(file_content or 'info 2023-03-20 09:16:21.436       lsvc  12316   3304                   '
                                    'anynet.tcp_acceptor -'
                                    'UPnP forwarding failed. info 2023-03-20 09:16:21.550       lsvc  12316  15200   21'
                                    'anynet.any_socket - Client-ID: 565195815 (FPR: 7cce5d0f828b).  info 2023-03-20 '
                                    '09:16:21.550'
                                    'lsvc  12316  15200   21                anynet.any_socket - Logged in from '
                                    '5.173.22.15:52926 '
                                    'on relay 9b6827f2. info 2023-03-20 09:16:21.550       lsvc  12316  15200   21'
                                    'anynet.connection_mgr - Making a new connection to client '
                                    '7cce5d0f828bee46da866566be1bc75eb5d284f5.  info 2023-03-20 09:16:21.550       '
                                    'lsvc  12316'
                                    '15200   21                  fiber.scheduler - Spawning root fiber 23.')

        return filename

    def test_no_file_present(self):
        nonexistent_file = get_anydesk_logs('')
        assert nonexistent_file is None

    def test_empty_file(self):
        empty_file = self.create_empty_file('anydesk.log')
        empty_logs = get_anydesk_logs(empty_file)
        assert empty_logs == {}
        os.remove("anydesk.log")

    def test_file_with_default_log(self):
        file_with_logs = self.create_anydesk_log_file('anydesk.log')
        found_logs = get_anydesk_logs(file_with_logs)
        assert found_logs == {'20/03/2023, 09:16:21': '5.173.22.15:52926'}
        os.remove("anydesk.log")

    def test_file_with_custom_log(self):
        file_with_logs = self.create_anydesk_log_file('anydesk.log', 'This is a custom log')
        found_logs = get_anydesk_logs(file_with_logs)
        assert found_logs == {}
        os.remove("anydesk.log")

    def test_file_with_partial_log(self):
        file_with_logs = self.create_anydesk_log_file('anydesk.log', 'info 2023-03-20 09:16:21.550       lsvc  12316  '
                                                                     '15200   21            anynet.connection_mgr - '
                                                                     'Making a new connection to client '
                                                                     '7cce5d0f828bee46da866566be1bc75eb5d284f5.  ')
        found_logs = get_anydesk_logs(file_with_logs)
        assert found_logs == {}
        os.remove("anydesk.log")

    def test_file_with_multiple_logs(self):
        file_with_logs = self.create_anydesk_log_file('anydesk.log', 'info 2023-03-20 09:16:21.550       lsvc  12316  '
                                                                     '15200   21                anynet.any_socket - '
                                                                     'Logged in from 7.1.1.15:5926 on relay 9b6827f2. '
                                                                     '\n'
                                                                     'info 2023-03-20 19:16:21.550       lsvc  12316  '
                                                                     '15200   21                anynet.any_socket - '
                                                                     'Logged in from 255.255.255.255 on relay '
                                                                     '9b6827f2. ')
        found_logs = get_anydesk_logs(file_with_logs)
        assert found_logs == {'20/03/2023, 09:16:21': '7.1.1.15:5926',
                              '20/03/2023, 19:16:21': '255.255.255.255'}
        os.remove("anydesk.log")


class TestCreateTimestampedDirectory:

    def test_create_timestamped_directory(self):
        directory_name = create_timestamped_directory()
        assert os.path.exists(directory_name)
        assert re.search(f'{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}', directory_name)
        os.rmdir(directory_name)
        try:
            os.rmdir('REPORTS')
        except OSError:
            print("Directory can not be removed")


class TestCreateFoldersFromPath:

    def test_create_folders_from_path(self):
        test_path = 'C:/Users/test/test'
        cwd = os.getcwd()
        current_path = os.path.join(cwd, 'REPORTS', 'abc', 'daf')
        create_folders_from_path(test_path, current_path)
        assert os.path.exists(os.path.join(cwd, 'REPORTS', 'abc', 'daf', 'Users', 'test'))
        shutil.rmtree(f'{os.getcwd()}/REPORTS')


class TestGenerateMd5FileChecksum:

    def test_generate_md5_file_checksum(self):
        test_file = TestGetAnydeskLogs.create_empty_file('test_file.txt')
        test_file_hash = hashlib.md5(open('test_file.txt', 'rb').read()).hexdigest()
        assert generate_md5_file_checksum(test_file) == test_file_hash
        os.remove('test_file.txt')

    def test_copy_and_generate_checksum(self, capsys):
        test_file = TestGetAnydeskLogs.create_empty_file('test_file.txt')
        test_file_hash = hashlib.md5(open('test_file.txt', 'rb').read()).hexdigest()
        cwd = os.getcwd()
        current_path = os.path.join(cwd, 'REPORTS', 'abc', 'daf')
        os.makedirs(current_path)
        copy_and_generate_checksum(test_file, os.path.join(os.getcwd(), current_path))
        assert os.path.exists(os.path.join(os.getcwd(), 'REPORTS', 'abc', 'daf', 'test_file.txt'))
        assert os.path.exists(os.path.join(os.getcwd(), 'REPORTS', 'abc', 'daf', 'test_file.txt_checksum.txt'))
        assert test_file_hash == open(os.path.join(os.getcwd(), 'REPORTS', 'abc', 'daf', 'test_file.txt_checksum.txt'),
                                      'r').read()
        shutil.rmtree(os.path.join(os.getcwd(), 'REPORTS'))
        os.remove('test_file.txt')

        # Test IOError
        nonexistent_file = 'nonexistent_file.txt'
        path_to_nonexistent_file = os.path.join(os.getcwd(), nonexistent_file)
        copy_and_generate_checksum(path_to_nonexistent_file, os.getcwd())
        captured_error_print = capsys.readouterr()
        assert captured_error_print.out == 'Error occurred when trying to copy\n'


class TestGeneratingTextReport:
    def test_generate_txt_report_with_header(self):
        report_directory_path = os.path.dirname(os.path.abspath(__file__))
        mockup_logs = {
            "11/03/2023, 19:09:48": "91.233.186.189:53065"
        }
        # Generate a report with a header
        generate_txt_report(report_directory_path, True, mockup_logs)
        # Check that the report file was created
        assert os.path.exists(os.path.join(report_directory_path, "report.txt"))
        # Check that the report contains the expected header
        with open(os.path.join(report_directory_path, "report.txt"), "r") as f:
            assert f.readline().startswith("Report for")
        os.remove(os.path.join(report_directory_path, "report.txt"))

    def test_generate_txt_report_without_header(self):
        report_directory_path = os.path.dirname(os.path.abspath(__file__))
        # Generate a report without a header
        generate_txt_report(report_directory_path, write_header=False)
        # Check that the report file was created
        assert os.path.exists(os.path.join(report_directory_path, "report.txt"))
        # Check that the report does not contain a header
        with open(os.path.join(report_directory_path, "report.txt"), "r") as f:
            assert not f.readline().startswith("Report for")
        os.remove(os.path.join(report_directory_path, "report.txt"))

    def test_generate_txt_report_without_anydesk_logs(self):
        report_directory_path = os.path.dirname(os.path.abspath(__file__))
        # Generate a report without Anydesk logs
        generate_txt_report(report_directory_path, anydesk_logs_dict=None, write_header=False)
        # Check that the report file was created
        assert os.path.exists(os.path.join(report_directory_path, "report.txt"))
        # Check that the report indicates that no Anydesk logs were found
        with open(os.path.join(report_directory_path, "report.txt"), "r") as f:
            assert f.readline().startswith("No Anydesk logs")
        os.remove(os.path.join(report_directory_path, "report.txt"))


class TestGenerateCSVReport:

    def test_generate_csv_report(self):
        report_directory_path = os.path.dirname(os.path.abspath(__file__))
        # Create a temporary directory for the report
        mockup_logs = {
            "11/03/2023, 19:09:48": "91.233.186.189:53065"
        }
        filename = 'test.txt'
        # arrange
        expected_output = [['Date', 'IP', 'File'],
                           ['11/03/2023, 19:09:48', '91.233.186.189:53065', 'test.txt']]
        # act
        generate_csv_report(report_directory_path, True, mockup_logs, filename)
        with open(os.path.join(report_directory_path, 'report.csv'), "r") as f:
            reader = csv.reader(f)
            actual_output = [row for row in reader]
        # assert
        assert actual_output == expected_output
        os.remove(os.path.join(report_directory_path, 'report.csv'))

    def test_generate_csv_report_without_header(self):
        report_directory_path = os.path.dirname(os.path.abspath(__file__))
        # Create a temporary directory for the report
        mockup_logs = {
            "11/03/2023, 19:09:48": "91.233.186.189:53065"
        }
        filename = 'test.txt'
        # arrange
        expected_output = [['11/03/2023, 19:09:48', '91.233.186.189:53065', 'test.txt']]
        # act
        generate_csv_report(report_directory_path, False, mockup_logs, filename)
        with open(os.path.join(report_directory_path, 'report.csv'), "r") as f:
            reader = csv.reader(f)
            actual_output = [row for row in reader]
        # assert
        assert actual_output == expected_output
        os.remove(os.path.join(report_directory_path, 'report.csv'))

    def test_generate_empty_csv_report(self):
        report_directory_path = os.path.dirname(os.path.abspath(__file__))
        filename = 'test.txt'
        # arrange
        expected_output = [['No Anydesk logs found!', '', 'test.txt']]
        # act
        generate_csv_report(report_directory_path, False, None, filename)
        with open(os.path.join(report_directory_path, 'report.csv'), "r") as f:
            reader = csv.reader(f)
            actual_output = [row for row in reader]
        # assert
        assert actual_output == expected_output
        os.remove(os.path.join(report_directory_path, 'report.csv'))


def test_split_computer_datetime_dirname():
    assert split_computer_datetime_dirname('computer_11-03-2023_19-09-48') == {'computer_name': 'computer',
                                                                               'date': '11-03-2023', 'time': '19:09:48'}

    assert split_computer_datetime_dirname('test_computer--203;lk;asdfj_11-03-2023_19-09-48') == {
        'computer_name': 'test_computer--203;lk;asdfj',
        'date': '11-03-2023', 'time': '19:09:48'}

    assert split_computer_datetime_dirname('1234567890_11-03-2023_19-09-48') == {
        'computer_name': '1234567890',
        'date': '11-03-2023', 'time': '19:09:48'}

    assert split_computer_datetime_dirname('__11-03-2023_19-09-48') == {'computer_name': '_',
                                                                        'date': '11-03-2023', 'time': '19:09:48'}

    assert split_computer_datetime_dirname('asfdfasd') is None
    assert split_computer_datetime_dirname('asfdfasd_11-03-2023_12-dd-22') is None
    assert split_computer_datetime_dirname('asfdfasd_11-03-2023_bb-dd-ee') is None


def test_get_reports_folder_list(tmp_path):
    reports_folder = os.path.join(tmp_path, 'REPORTS')
    # Assert that the reports folder does not exist
    assert not os.path.isdir(reports_folder)
    # Assert that after running the function the reports folder is created and is empty
    assert get_reports_folder_list(reports_folder) == []
    # Assert that the reports folder exists
    assert os.path.isdir(reports_folder)
    assert os.path.exists(os.path.join(tmp_path, 'REPORTS'))
    os.mkdir(os.path.join(reports_folder, 'computer_11-03-2023_19-09-48'))
    os.mkdir(os.path.join(reports_folder, 'computer_11-03-2023_19-09-49'))
    os.mkdir(os.path.join(reports_folder, 'computer_11-03-2023_19-09-50'))
    assert sorted(get_reports_folder_list(reports_folder)) == sorted(['computer_11-03-2023_19-09-48',
                                                                      'computer_11-03-2023_19-09-49',
                                                                      'computer_11-03-2023_19-09-50'])
