# Licensed under the LGPL 3.0 License.
# i18nco by numlinka.

# std
from abc import ABC, abstractmethod

# self
from .schemas import *


class AbstractI18n (ABC):
    @abstractmethod
    def con_set_locale(self) -> None: ...
    @abstractmethod
    def con_get_locale(self) -> LocaleCode: ...
    @abstractmethod
    def con_get_available_locales(self) -> LocaleCodeList: ...
    @abstractmethod
    def con_add_translation(self, locale: LocaleCode, key: TextKey, text: str) -> None: ...
    @abstractmethod
    def con_translation(self, key: TextKey) -> str: ...


__all__ = ["AbstractI18n"]
