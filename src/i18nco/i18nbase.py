# Licensed under the LGPL 3.0 License.
# i18nco by numlinka.

# std
import threading
from typing import *

# self
from .schemas import *
from .constants import *
from .i18nstring import I18nString
from .i18nabstract import AbstractI18n


class BaseI18n (AbstractI18n):
    def __init__(self) -> None:
        self._lock = threading.RLock()

        self._sc_first_locale: LocaleCode = en_US
        self._sc_second_locale: LocaleCode = zh_CN

        self._sc_translation: Dict[LocaleCode: Dict[TextKey: str]] = {}

    def con_set_locale(self, first_language: LocaleCode = ..., second_language: LocaleCode = ...) -> None:
        if isinstance(first_language, LocaleCode) and first_language == second_language:
            raise ValueError("first_language and second_language must be different.")

        if isinstance(first_language, LocaleCode):
            with self._lock:
                if first_language == self._sc_second_locale:
                    self._sc_first_locale, self._sc_second_locale = \
                        self._sc_second_locale, self._sc_first_locale
                    return

                self._sc_first_locale = first_language

        if isinstance(second_language, LocaleCode):
            with self._lock:
                if second_language == self._sc_first_locale:
                    self._sc_first_locale, self._sc_second_locale = \
                        self._sc_second_locale, self._sc_first_locale
                    return

                self._sc_second_locale = second_language

    def con_get_locale(self) -> LocaleCode:
        return self.con_get_first_locale()

    def con_get_available_locales(self) -> LocaleCodeList:
        with self._lock:
            return list(self._sc_translation.keys())

    def con_add_translation(self, locale: Union[LocaleCode, LocaleCodeList], key: TextKey, text: str) -> None:
        if not isinstance(locale, (LocaleCode, list)):
            raise TypeError("locale must be LocaleCode (str).")

        if not isinstance(key, TextKey):
            raise TypeError("key must be TextKey (str).")

        if not isinstance(text, str):
            raise TypeError("value must be str.")

        with self._lock:
            if isinstance(locale, LocaleCode):
                if locale not in self._sc_translation:
                    self._sc_translation[locale] = {}

                self._sc_translation[locale][key] = text
                return

            for locale_ in locale:
                if locale_ not in self._sc_translation:
                    self._sc_translation[locale_] = {}
                self._sc_translation[locale_][key] = text

    def _con_get_self_translation(self, target: TextKey) -> str:
        try:
            result: object = None
            for indexed, __name in enumerate(target.split(".")):
                result = super().__getattribute__(__name) if indexed == 0 else getattr(result, __name)

            if not isinstance(result, str):
                # result = str(result)
                result = target

        except AttributeError as _:
            result = target

        return result

    def con_translation(self, key: TextKey) -> I18nString:
        with self._lock:

            table = self._sc_translation.get(self._sc_first_locale, {})
            result = table.get(key, None)

            if result is None:
                table = self._sc_translation.get(self._sc_second_locale, {})
                result = table.get(key, None)

            if result is None:
                result = self._con_get_self_translation(key)

            reply = I18nString(result)
            reply.con_set_attribute(self, key)
            return reply

    def __getattribute__(self, __name: str) -> Any:
        if __name.startswith("_") or __name.startswith("con_"):
            return super().__getattribute__(__name)

        return self.con_translation(__name)


__all__ = ["BaseI18n"]
