from file_operations import get_anydesk_logs


def test_get_anydesk_logs():
    empty_logs = get_anydesk_logs('')
    assert empty_logs is None
