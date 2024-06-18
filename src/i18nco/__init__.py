# Licensed under the LGPL 3.0 License.
# i18nco by numlinka.

__name__ = "internationalization"
__author__ = "numlinka"
__license__ = "LGPL 3.0"
__copyright__ = "Copyright (C) 2022 numlinka"

# self
from .i18nstring import *
from .internationalization import *


__version_info__ = (1, 2, 1)
__version__ = ".".join(map(str, __version_info__))


__all__ = [
    "I18nString",
    "Internationalization"
]
