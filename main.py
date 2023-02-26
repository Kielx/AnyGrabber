from os import getenv

app_data_path = getenv('APPDATA')
program_data_path = getenv('PROGRAMDATA')
search_string = 'Logged in from '

with open(f'{app_data_path}/AnyDesk/ad.trace', 'r') as f:
    for l_no, line in enumerate(f):
        # search string
        if search_string in line:
            print('string found in a file')
            print('Line Number:', l_no)
            print('Line:', line)
            before_keyword, keyword, after_keyword = line.partition(search_string)
            last_dot = after_keyword.rfind(' on relay')
            print(last_dot)
            after_keyword = after_keyword[0 : last_dot]
            print(after_keyword)

with open(f'{program_data_path}/AnyDesk/ad_svc.trace', 'r') as f:
    for l_no, line in enumerate(f):
        # search string
        if search_string in line:
            print('string found in a file')
            print('Line Number:', l_no)
            print('Line:', line)
            before_keyword, keyword, after_keyword = line.partition(search_string)
            last_dot = after_keyword.rfind(' on relay')
            print(last_dot)
            after_keyword = after_keyword[0 : last_dot]
            print(after_keyword)