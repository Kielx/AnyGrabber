import gettext
import json

_ = gettext.gettext

config = open('config.json', 'r')
config_data = json.load(config)

if config_data["locale"] == "en-US":
    default_locale = "en-US"
elif config_data["locale"] == "pl-PL":
    default_locale = "pl-PL"
else:
    default_locale = "en-US"


def set_default_locale(locale_str):
    """Function that sets default language."""
    with open('config.json', 'r') as config_file:
        cfg = json.load(config_file)
    cfg["locale"] = locale_str
    with open('config.json', 'w') as config_file:
        json.dump(cfg, config_file)


def change_frame_locale(frame_name, locale_str=default_locale):
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
