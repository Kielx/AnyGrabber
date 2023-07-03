import os
import queue

import customtkinter

from frames.AnydeskFrame import AnydeskFrame


def test_turn_off_switches():
    # Arrange
    anydesk_frame = AnydeskFrame(master=None)

    # Test turning off switches independently
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


"""
Failing due to the fact that the app is not running in a window and it
def test_if_open_report_button_shows_after_search():
    # Arrange
    anydesk_frame = AnydeskFrame(master=app)
    test_queue = queue.Queue()
    assert anydesk_frame.open_report_button.grid_info() == {}
    anydesk_frame.search_filesystem_callback(os.getcwd(), test_queue)
    assert anydesk_frame.open_report_button.grid_info() != {}
    assert anydesk_frame.open_report_button.grid_info()["in"] == anydesk_frame
    try:
        os.remove('./tests/report.txt')
    except FileNotFoundError:
        pass
"""


def test_toggle_checkboxes_and_buttons_state():
    # Arrange
    anydesk_frame = AnydeskFrame(master=None)

    # Test toggling checkboxes
    anydesk_frame.switch_search_for_logs_in_location.set(True)
    anydesk_frame.switch_fetch_programdata_logs.set(True)
    anydesk_frame.switch_fetch_appdata_logs.set(True)

    anydesk_frame.switch_checkboxes_and_buttons_state([
        anydesk_frame.checkbox_search_for_logs_in_location,
        anydesk_frame.checkbox_fetch_programdata_logs,
        anydesk_frame.checkbox_fetch_appdata_logs,
        anydesk_frame.fetch_logs_button,
        anydesk_frame.open_report_button

    ], 'disabled')

    assert anydesk_frame.checkbox_search_for_logs_in_location.cget('state') == 'disabled'
    assert anydesk_frame.checkbox_fetch_programdata_logs.cget('state') == 'disabled'
    assert anydesk_frame.checkbox_fetch_appdata_logs.cget('state') == 'disabled'
    assert anydesk_frame.fetch_logs_button.cget('state') == 'disabled'
    assert anydesk_frame.open_report_button.cget('state') == 'disabled'

    anydesk_frame.switch_checkboxes_and_buttons_state([
        anydesk_frame.checkbox_search_for_logs_in_location,
        anydesk_frame.checkbox_fetch_programdata_logs,
        anydesk_frame.checkbox_fetch_appdata_logs,
        anydesk_frame.fetch_logs_button,
        anydesk_frame.open_report_button
    ], 'normal')

    assert anydesk_frame.checkbox_search_for_logs_in_location.cget('state') == 'normal'
    assert anydesk_frame.checkbox_fetch_programdata_logs.cget('state') == 'normal'
    assert anydesk_frame.checkbox_fetch_appdata_logs.cget('state') == 'normal'
    assert anydesk_frame.fetch_logs_button.cget('state') == 'normal'
    assert anydesk_frame.open_report_button.cget('state') == 'normal'
