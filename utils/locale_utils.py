import gettext
import json
from bidict import bidict

config = open('config.json', 'r')
config_data = json.load(config)
default_locale = config_data["locale"]
config.close()


def set_default_locale(locale_str):
    """Function that sets default language."""
    with open('config.json', 'r') as config_file:
        cfg = json.load(config_file)
    cfg["locale"] = locale_str
    with open('config.json', 'w') as config_file:
        json.dump(cfg, config_file)


lang = gettext.translation("HomeFrame", localedir='locale', languages=[default_locale])
lang.install()
_ = lang.gettext

language_mappings = bidict({
    "en-US": _("English"),
    "pl-PL": _("Polish"),
})
