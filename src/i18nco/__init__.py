# Licensed under the MIT License.
# i18nco Copyright (C) 2022 numlinka.

__all__ = [
    "I18nString",
    "Internationalization"
]

__name__ = "internationalization"
__author__ = "numlinka"
__license__ = "MIT"
__copyright__ = "Copyright (C) 2022 numlinka"
__version_info__ = (1, 4, 0)
__version__ = ".".join(map(str, __version_info__))

# internal
from .internationalization import I18nString, Internationalization
from . import utils
