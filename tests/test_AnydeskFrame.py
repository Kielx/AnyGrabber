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
