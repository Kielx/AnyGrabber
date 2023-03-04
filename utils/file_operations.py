import dateutil.parser as dparser

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
