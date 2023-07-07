import gettext
from bidict import bidict
from utils.config_utils import get_config_parameter_value


default_locale = get_config_parameter_value("locale")

lang = gettext.translation("HomeFrame", localedir='locale', languages=[default_locale])
lang.install()
_ = lang.gettext

language_mappings = bidict({
    "en-US": _("English"),
    "pl-PL": _("Polish"),
})

appearance_mode_mappings = bidict({
    "light": _("Light"),
    "dark": _("Dark"),
    "system": _("System"),
})
