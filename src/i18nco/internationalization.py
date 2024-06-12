# Licensed under the LGPL 3.0 License.
# i18nco by numlinka.

# std
# from typing import *

# self
from .utils import *
from .schemas import *
from .i18nbase import *
from .components import *


class Internationalization (BaseI18n, I18nJsonLoad, I18nCSVLoad, I18nLangLoad, I18nAutoLoad):
    def con_set_first_locale(self, value: LocaleCode) -> None:
        self.con_set_locale(value)

    def con_set_second_locale(self, value: LocaleCode) -> None:
        self.con_set_locale(..., value)

    def con_get_first_locale(self) -> LocaleCode:
        with self._lock:
            return self._sc_first_locale

    def con_get_second_locale(self) -> LocaleCode:
        with self._lock:
            return self._sc_second_locale

    def con_auto_set_best_locale(self) -> None:
        """
        ## Automatically set the best language
        ## 自动设置最佳语言

        Adjust to the best locale code according to the system environment.
        根据系统环境调整最佳语言码.
        """
        system_code = get_locale_code()
        available_locales = self.con_get_available_locales()

        if system_code in available_locales:
            self.con_set_locale(system_code)
            return

        best = match_best_locale(system_code, available_locales)

        if best is not None:
            self.con_set_locale(best)

    def con_auto_adjust_best_locale(self) -> None:
        """
        ## Automatically adjust the best language
        ## 自动调整最佳语言

        Adjust to the best locale code based on current settings.
        根据当前设置调整最佳语言码.
        """
        first_locale = self.con_get_first_locale()
        second_locale = self.con_get_second_locale()
        available_locales = self.con_get_available_locales()

        best_first_locale = match_best_locale(first_locale, available_locales)
        best_second_locale = match_best_locale(second_locale, available_locales)

        if best_first_locale is not None:
            self.con_set_first_locale(best_first_locale)

        if best_second_locale is not None:
            self.con_set_second_locale(best_second_locale)


__all__ = ["Internationalization"]
