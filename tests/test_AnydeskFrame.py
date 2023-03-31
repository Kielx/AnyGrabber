import os
from frames.AnydeskFrame import AnydeskFrame


def test_turn_off_switches():
    # Arrange
    anydesk_frame = AnydeskFrame(master=None)

    # Test turning off switches independently
    anydesk_frame.find_files_switch.set(True)
    anydesk_frame.turn_off_switches([anydesk_frame.find_files_switch])
    assert anydesk_frame.find_files_switch.get() is False

    anydesk_frame.fetch_programdata_logs_switch.set(True)
    anydesk_frame.turn_off_switches([anydesk_frame.fetch_programdata_logs_switch])
    assert anydesk_frame.fetch_programdata_logs_switch.get() is False

    anydesk_frame.fetch_appdata_logs_switch.set(True)
    anydesk_frame.turn_off_switches([anydesk_frame.fetch_appdata_logs_switch])
    assert anydesk_frame.fetch_appdata_logs_switch.get() is False

    anydesk_frame.fetch_appdata_logs_switch.set(True)
    anydesk_frame.fetch_programdata_logs_switch.set(True)
    anydesk_frame.turn_off_switches([anydesk_frame.fetch_appdata_logs_switch,
                                     anydesk_frame.fetch_programdata_logs_switch])

    assert anydesk_frame.fetch_appdata_logs_switch.get() is False
    assert anydesk_frame.fetch_programdata_logs_switch.get() is False

    anydesk_frame.fetch_appdata_logs_switch.set(True)
    anydesk_frame.fetch_programdata_logs_switch.set(True)
    anydesk_frame.find_files_switch.set(True)

    anydesk_frame.turn_off_switches([anydesk_frame.fetch_appdata_logs_switch,
                                     anydesk_frame.fetch_programdata_logs_switch, anydesk_frame.find_files_switch])

    assert anydesk_frame.fetch_appdata_logs_switch.get() is False


def test_if_open_report_button_shows_after_search():
    # Arrange
    anydesk_frame = AnydeskFrame(master=None)

    assert anydesk_frame.open_report_button.grid_info() == {}
    anydesk_frame.search_filesystem_callback(search_location=os.getcwd())
    assert anydesk_frame.open_report_button.grid_info() != {}
    assert anydesk_frame.open_report_button.grid_info()["in"] == anydesk_frame
    os.remove('report.txt')


    anydesk_frame.switch_search_for_logs_in_location.set(True)
    anydesk_frame.turn_off_switches([anydesk_frame.switch_search_for_logs_in_location])
    assert anydesk_frame.switch_search_for_logs_in_location.get() is False

    anydesk_frame.switch_fetch_programdata_logs.set(True)
    anydesk_frame.turn_off_switches([anydesk_frame.switch_fetch_programdata_logs])
    assert anydesk_frame.switch_fetch_programdata_logs.get() is False

    anydesk_frame.switch_fetch_appdata_logs.set(True)
    anydesk_frame.turn_off_switches([anydesk_frame.switch_fetch_appdata_logs])
    assert anydesk_frame.switch_fetch_appdata_logs.get() is False

    anydesk_frame.switch_fetch_appdata_logs.set(True)
    anydesk_frame.switch_fetch_programdata_logs.set(True)
    anydesk_frame.turn_off_switches([anydesk_frame.switch_fetch_appdata_logs,
                                     anydesk_frame.switch_fetch_programdata_logs])

    assert anydesk_frame.switch_fetch_appdata_logs.get() is False
    assert anydesk_frame.switch_fetch_programdata_logs.get() is False

    anydesk_frame.switch_fetch_appdata_logs.set(True)
    anydesk_frame.switch_fetch_programdata_logs.set(True)
    anydesk_frame.switch_search_for_logs_in_location.set(True)

    anydesk_frame.turn_off_switches([anydesk_frame.switch_fetch_appdata_logs,
                                     anydesk_frame.switch_fetch_programdata_logs,
                                     anydesk_frame.switch_search_for_logs_in_location])

    assert anydesk_frame.switch_fetch_appdata_logs.get() is False
