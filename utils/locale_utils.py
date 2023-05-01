import gettext
from tkinter import *

_ = gettext.gettext


def change_frame_locale(frame_name, locale_str):
    """Function that changes locale of selected frame."""
    en = gettext.translation(frame_name, localedir='locale', languages=['en-US'])
    pl = gettext.translation(frame_name, localedir='locale', languages=['pl-PL'])
    global _
    if locale_str == "en-US":
        en.install()
        _ = en.gettext
    elif locale_str == "pl-PL":
        pl.install()
        _ = pl.gettext
    return _
