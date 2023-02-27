from os import getenv

app_data_path = getenv('APPDATA')
app_data_filename = f'{app_data_path}/AnyDesk/ad.trace'
program_data_path = getenv('PROGRAMDATA')
program_data_filename = f'{program_data_path}/AnyDesk/ad_svc.trace'
search_string = 'Logged in from '


def get_appdata_logs():
    try:
        with open(app_data_filename, 'r') as f:
            for l_no, line in enumerate(f):
                # search string
                if search_string in line:
                    print('string found in a file')
                    print('Line Number:', l_no)
                    print('Line:', line)
                    before_keyword, keyword, after_keyword = line.partition(search_string)
                    last_dot = after_keyword.rfind(' on relay')
                    print(last_dot)
                    after_keyword = after_keyword[0: last_dot]
                    print(after_keyword)
    except IOError:
        return f'Could not open file {app_data_filename}'


def get_programdata_logs():
    try:
        with open(program_data_filename, 'r') as f:
            for l_no, line in enumerate(f):
                # search string
                if search_string in line:
                    print('string found in a file')
                    print('Line Number:', l_no)
                    print('Line:', line)
                    before_keyword, keyword, after_keyword = line.partition(search_string)
                    last_dot = after_keyword.rfind(' on relay')
                    print(last_dot)
                    after_keyword = after_keyword[0: last_dot]
                    print(after_keyword)
    except IOError:
        return f'Could not open file {program_data_filename}'
