# Licensed under the MIT License.
# i18nco Copyright (C) 2022 numlinka.

__all__ = ["Internationalization", "I18nString"]

# std
import threading
from typing import Tuple, List, Dict, Optional

# internal
from .typeins import *
from .constants import en_US


class Internationalization (object):
    def __init__(self) -> None:
        """
        This class provides an interface for managing internationalization (i18n) translations.
        """
        self._lock = threading.RLock()
        self._translation: Dict[LocaleCode: Dict[TextKey: str]] = {}
        self._first_locale: LocaleCode = en_US
        self._second_locale: LocaleCode = en_US

    def ctrl_set_locale(self, first_language: Optional[LocaleCode] = None, second_language: Optional[LocaleCode] = None):
        """
        Set the locale for language preferences.

        You can set two languages: a primary language (`first_language`) and a secondary language (`second_language`).
        The secondary language is used when a valid translation is not available in the primary language.

        Args:
            first_language (LocaleCode, optional): The primary language to use. If None, the existing primary language
                                                   is retained.
            second_language (LocaleCode, optional): The secondary language to use. If None, If None, the existing
                                                    secondary language is retained.

        Raises:
            TypeError: If `first_language` or `second_language` is not a `LocaleCode` or `None`.

        Examples:
            Set only the primary language:
            >>> obj.ctrl_set_locale(zh_CN)

            Set only the secondary language:
            >>> obj.ctrl_set_locale(second_language=zh_CN)

            Set both primary and secondary languages:
            >>> obj.ctrl_set_locale(zh_CN, en_US)
        """
        if first_language is not None and not isinstance(first_language, LocaleCode):
            raise TypeError(f"Expected `first_language` to be `LocaleCode` or `None`, but got {type(first_language)}.")

        if second_language is not None and not isinstance(second_language, LocaleCode):
            raise TypeError(f"Expected `second_language` to be `LocaleCode` or `None`, but got {type(second_language)}.")

        with self._lock:
            if first_language is not None:
                self._first_locale = first_language

            if second_language is not None:
                self._second_locale = second_language

    def ctrl_get_locale(self) -> Tuple[LocaleCode, LocaleCode]:
        """
        Get the current locale settings.

        This method returns a tuple containing the current primary and secondary locale codes. The primary locale
        is the preferred language, while the secondary locale is used as a fallback when a translation is not
        available in the primary language.

        Returns:
            out (Tuple[LocaleCode, LocaleCode]): A tuple where the first element is the primary locale and the second
                                                 element is the secondary locale.

        Examples:
            Get the current locale settings:
            >>> primary, secondary = obj.ctrl_get_locale()
            >>> print(primary, secondary)
            LocaleCode("en_US") LocaleCode("zh_CN")
        """
        with self._lock:
            return self._first_locale, self._second_locale

    def ctrl_available_locales(self) -> List[LocaleCode]:
        """
        Get the list of languages supported by the current object.

        This method returns a list of languages that the current object supports. Each language is represented
        as a `LocaleCode` object. The list can be used to determine available localization options.

        Returns:
            out (List[LocaleCode]): A list of supported languages, where each item is a `LocaleCode` object.

        Examples:
            Get the list of supported languages:
            >>> available_languages = obj.ctrl_available_locales()
            >>> print(available_languages)
            [LocaleCode("en_US"), LocaleCode("zh_CN"), LocaleCode("ru_RU")]
        """
        with self._lock:
            return list(self._translation.keys())

    def ctrl_set_translation(self, locale: Optional[LocaleCode] = None,
                             key: Optional[TextKey] = None, text: Optional[str] = None) -> None:
        """
        Set or remove the translation text for the specified language key.

        This method allows you to set or remove a translation for a specific key and language. If `text` is None,
        the translation for the specified key will be removed. If `key` is None, all translations for the specified
        language will be removed.

        Args:
            locale (LocaleCode, optional): The language for which to set or remove the translation.
                                                         If None, the `first_language` (previously set) will be used.
            key (TextKey, optional): The key of the translation to set or remove. If None, all translations for the
                                 specified language will be removed.
            text (str, optional): The text to set for the translation. If None, the translation for the specified key
                              will be removed.

        Raises:
            TypeError: If the input types are incorrect.

        Examples:
            Set a translation for a specific key and language:
            >>> obj.ctrl_set_translation(LocaleCode("en_US"), "welcome_message", "Welcome!")

            Remove a translation for a specific key:
            >>> obj.ctrl_set_translation(LocaleCode("en_US"), "welcome_message", None)

            Remove all translations for a specific language:
            >>> obj.ctrl_set_translation(LocaleCode("en_US"), None, None)

            Set a translation using the default `first_language`:
            >>> obj.ctrl_set_translation(None, "welcome_message", "Welcome!")
        """
        if locale is not None and not isinstance(locale, LocaleCode):
            raise TypeError(f"Expected `locale` to be `LocaleCode` or `None`, but got {type(locale)}.")

        if key is not None and not isinstance(key, TextKey):
            raise TypeError(f"Expected `key` to be `TextKey` or `None`, but got {type(key)}.")

        if text is not None and not isinstance(text, str):
            raise TypeError(f"Expected `text` to be `str` or `None`, but got {type(text)}.")

        with self._lock:
            if locale is None:
                locale = self._first_locale

            if key is None:
                if locale in self._translation:
                    del self._translation[locale]
                return

            if text is None:
                if locale in self._translation and key in self._translation[locale]:
                    del self._translation[locale][key]
                return

            if locale not in self._translation:
                self._translation[locale] = {}

            self._translation[locale][key] = text

    def _ctrl_self_translation(self, target: TextKey) -> str:
        if not isinstance(target, TextKey):
            raise TypeError(f"Expected target to be TextKey, but got {type(target)}.")

        try:
            result: Optional[str] = None
            for indexed, __name in enumerate(target.split(".")):
                result = super().__getattribute__(__name) if indexed == 0 else getattr(result, __name)

            if not isinstance(result, str):
                result = target

        except AttributeError as _:
            result = target

        return result

    def ctrl_translation(self, key: TextKey, locale: Optional[LocaleCode] = None) -> "I18nString":
        """
        Get the translation text for the specified language key.

        This method retrieves the translated text for a given key in the specified language. If the `locale` parameter
        is provided, the translation will be fetched for that specific language.

        If no translation is found for the specified key, an `I18nString` object containing the key itself will
        be returned.

        Args:
            key (TextKey): The key of the translation text to retrieve.
            locale (LocaleCode, optional): The language for which to retrieve the translation.

        Returns:
            out (I18nString): The translated text for the specified key and language. If no translation is found,
                              an `I18nString` object containing the key itself will be returned.

        Raises:
            TypeError: If the input types are incorrect.

        Examples:
            Get a translation for a specific key and language:
            >>> translation = obj.ctrl_translation("welcome_message", LocaleCode("en_US"))
            >>> print(translation)
            "Welcome!"

            Get a translation without specifying a locale (uses default or fallback language):
            >>> translation = obj.ctrl_translation("welcome_message")
            >>> print(translation)
            "欢迎！"

            Get a translation for a non-existent key:
            >>> translation = obj.ctrl_translation("unknown_key")
            >>> print(translation)
            "unknown_key"  # Returns the key itself as an I18nString object.
        """
        if not isinstance(key, TextKey):
            raise TypeError(f"Expected `key` to be `TextKey`, but got {type(key)}.")

        if locale is not None and not isinstance(locale, LocaleCode):
            raise TypeError(f"Expected `locale` to be `LocaleCode` or `None`, but got {type(locale)}.")

        with self._lock:
            target_locale = locale if locale is not None else self._first_locale
            result = self._translation.get(target_locale, {}).get(key, None)

            if result is None and locale is None:
                result = self._translation.get(self._second_locale, {}).get(key, None)

            if result is None:
                result = self._ctrl_self_translation(key)

            reply = I18nString(result)
            reply._ctrl_set_attribute(self, key)
            return reply


    def __getattribute__(self, __name: str) -> "I18nString":
        """
        Override the default attribute access behavior to support dynamic translation lookups.

        This method intercepts attribute access on instances of `Internationalization`. If the
        requested attribute name starts with an underscore (`_`) or the prefix `ctrl_`, it
        delegates to the default attribute access behavior (via `super().__getattribute__`).
        Otherwise, it treats the attribute name as a translation key and returns an `I18nString`
        instance representing the translated text.

        Args:
            __name (str): The name of the attribute being accessed.

        Returns:
            out (I18nString): If the attribute name is a translation key, returns an `I18nString`
                              instance representing the translated text. Otherwise, returns the
                              attribute value as usual.

        Examples:
            >>> i18n = Internationalization()
            >>> i18n.ctrl_set_translation(LocaleCode("en_US"), "welcome_message", "Welcome!")
            >>> translation = i18n.welcome_message  # Access via attribute
            >>> print(translation)
            "Welcome!"

            >>> i18n.ctrl_set_translation(LocaleCode("en_US"), "greeting.hello", "Hello!")
            >>> translation = i18n.greeting.hello  # Nested key access
            >>> print(translation)
            "Hello!"

            >>> private_attr = i18n._private_method()  # Access private method
        """
        if __name.startswith("_") or __name.startswith("ctrl_"):
            return super().__getattribute__(__name)

        return self.ctrl_translation(__name)


class I18nString(str):
    """
    A specialized string class for handling internationalized (i18n) text.

    This class extends the built-in `str` class to support dynamic translation lookups
    and attribute-based access to nested translation keys. It is designed to work in
    conjunction with the `Internationalization` class to provide seamless multi-language
    support.
    """

    def _ctrl_set_attribute(self, visit: Internationalization, keywords: str = "") -> None:
        """
        Set the `Internationalization` instance and the base translation key.

        This method associates the `I18nString` instance with an `Internationalization`
        object and sets the base translation key. The key can be used for nested
        translation lookups.

        Args:
            visit (Internationalization): The `Internationalization` instance to use for
                                          translation lookups.
            keywords (str, optional): The base translation key or path. Defaults to "".

        Examples:
            >>> i18n = Internationalization()
            >>> i18n_string = I18nString("Welcome!")
            >>> i18n_string.ctrl_set_attribute(i18n, "welcome_message")
        """
        self._visit_ = visit
        self._keywords_ = keywords

    def __getattr__(self, __name: str) -> "I18nString":
        """
        Dynamically resolve nested translation keys.

        This method allows dot notation (e.g., "welcome.message") to access nested
        translation keys. If the current `_keywords_` is not empty, it appends the new
        key to the existing path.

        Args:
            __name (str): The attribute name (translation key) to resolve.

        Returns:
            out (I18nString): A new `I18nString` instance representing the resolved translation.

        Examples:
            >>> i18n = Internationalization()
            >>> i18n_string = I18nString("Welcome!")
            >>> i18n_string.ctrl_set_attribute(i18n, "welcome")
            >>> message = i18n_string.message  # Resolves to "welcome.message"
        """
        target = __name if self._keywords_ == "" else f"{self._keywords_}.{__name}"
        return self._visit_.ctrl_translation(target)
