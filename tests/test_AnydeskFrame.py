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
