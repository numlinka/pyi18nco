# Licensed under the MIT License.
# i18nco Copyright (C) 2022 numlinka.

__all__ = [
    "Internationalization",
    "I18nString",
    "I18nControl"
]

__name__ = "internationalization"
__author__ = "numlinka"
__license__ = "MIT"
__copyright__ = "Copyright (C) 2022 numlinka"
__version_info__ = (1, 3, 0)
__version__ = ".".join(map(str, __version_info__))

# internal
from .internationalization import Internationalization, I18nString
from .i18ncontrol import I18nControl
