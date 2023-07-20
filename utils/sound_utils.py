try:
    import winsound
except ImportError:
    winsound = None


def play_message_beep():
    if winsound is not None:
        winsound.MessageBeep()
