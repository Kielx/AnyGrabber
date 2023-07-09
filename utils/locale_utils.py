import gettext
from bidict import bidict
from utils.config_utils import get_config_parameter_value

# Get default locale from config file
default_locale = get_config_parameter_value("locale")

# Set up gettext for translation based on default locale
lang = gettext.translation("Main", localedir='locale', languages=[default_locale])
lang.install()
_ = lang.gettext

# Set up bidirectional mappings for language and appearance mode
# They are used throughout the application to convert between
# language/appearance mode codes and their human-readable names
# They are used in the language and appearance mode settings and menus
#
# **To add a new language/appearance mode, add a new entry to the mappings**
#
language_mappings = bidict({
    "en-US": _("English"),
    "pl-PL": _("Polish"),
})

appearance_mode_mappings = bidict({
    "light": _("Light"),
    "dark": _("Dark"),
    "system": _("System"),
})
