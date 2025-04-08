# Licensed under the MIT License.
# i18nco Copyright (C) 2022 numlinka.

__all__ = ["Internationalization", "I18nString"]

# std
import os
import csv
import json
import threading
from typing import Tuple, List, Dict, Optional, Union

# internal
from .utils import match_best_locale, decode_escape_sequences
from .typeins import TextKey, LocaleCode
from .constants import DEFAULT_ENCODING, en_US


class I18nString (str):
    """
    A specialized string class for handling internationalized (i18n) text.

    This class extends the built-in `str` class to support dynamic translation lookups
    and attribute-based access to nested translation keys. It is designed to work in
    conjunction with the `Internationalization` class to provide seamless multi-language
    support.
    """

    def _ctrl_relevance(self, visit: "Internationalization", keywords: str = "") -> None:
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
        return self._visit_.ctrl.translation(target)


class Internationalization (object):
    def __init__(self) -> None:
        """
        This class provides an interface for managing internationalization (i18n) translations.
        """
        self.ctrl = I18nControl(self)

    def _attribute_overload(self, target: TextKey) -> str:
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

    def __getattribute__(self, __name: str) -> I18nString:
        if __name.startswith("_") or __name == "ctrl":
            return super().__getattribute__(__name)

        return self.ctrl.translation(__name)

    def __call__(self, key: TextKey, locale: Optional[LocaleCode] = None) -> I18nString:
        return self.ctrl.translation(key, locale)



class I18nControl (object):
    def __init__(self, i18n: Internationalization) -> None:
        if not isinstance(i18n, Internationalization):
            raise TypeError(f"Expected `i18n` to be an instance of `Internationalization`, but got {type(i18n)}.")

        self.i18n = i18n
        self._lock = threading.RLock()
        self.__table_translation: Dict[LocaleCode: Dict[TextKey: str]] = {}
        self.__first_locale: LocaleCode = en_US
        self.__second_locale: LocaleCode = en_US

    @property
    def first_locale(self) -> LocaleCode:
        with self._lock:
            return self.__first_locale

    @property
    def second_locale(self) -> LocaleCode:
        with self._lock:
            return self.__second_locale

    @property
    def available_locales(self) -> Tuple[LocaleCode]:
        with self._lock:
            return tuple(self.__table_translation.keys())

    def set_locale(self, first_language: Optional[LocaleCode] = None,
            second_language: Optional[LocaleCode] = None, auto_adjust: bool = True) -> None:
        """
        Set the locale for language preferences.

        You can set two languages: a primary language (`first_language`) and a secondary language (`second_language`).
        The secondary language is used when a valid translation is not available in the primary language.
        By default, the secondary language is automatically adjusted based on the primary language.

        Args:
            first_language (LocaleCode, optional): The primary language to use. If None, the existing primary language
                                                   is retained.
            second_language (LocaleCode, optional): The secondary language to use. If None, the secondary language is
                                                    automatically adjusted based on the primary language.
            auto_adjust (bool): Whether to automatically adjust the secondary language based on the primary language.
                                This parameter has no effect if `second_language` is explicitly set.

        Raises:
            TypeError: If `first_language` or `second_language` is not a `LocaleCode` or None.

        Examples:
            Set only the primary language:
            >>> obj.set_locale(zh_CN, auto_adjust=False)

            Set only the secondary language:
            >>> obj.set_locale(second_language=zh_CN)

            Set both primary and secondary languages:
            >>> obj.set_locale(en_US, zh_CN)

            Set the primary language and automatically adjust the secondary language:
            >>> obj.set_locale(zh_CN)

            Automatically adjust the secondary language based on the existing primary language:
            >>> obj.set_locale()
        """
        if first_language is not None and not isinstance(first_language, LocaleCode):
            raise TypeError(f"Expected `first_language` to be `LocaleCode` or None, but got {type(first_language)}.")

        if second_language is not None and not isinstance(second_language, LocaleCode):
            raise TypeError(f"Expected `second_language` to be `LocaleCode` or None, but got {type(second_language)}.")

        with self._lock:
            if isinstance(first_language, LocaleCode):
                self.__first_locale = first_language

            if isinstance(second_language, LocaleCode):
                self.__second_locale = second_language

            elif second_language is None and auto_adjust:
                available_locales = [x for x in self.available_locales if x != self.__first_locale]
                best_locale = match_best_locale(self.__first_locale, available_locales)

                if best_locale is None:
                    self.__second_locale = en_US
                    return

                self.__second_locale = best_locale


    def set_translation(self, locale: Optional[Union[LocaleCode, List[LocaleCode]]] = None,
                        key: Optional[TextKey] = None, text: Optional[str] = None) -> None:
        """
        Set or remove the translation text for the specified language key.

        This method allows you to set or remove a translation for a specific key and language. If `text` is None,
        the translation for the specified key will be removed. If `key` is None, all translations for the specified
        language will be removed.

        Args:
            locale (LocaleCode, List[LocaleCode], optional): The language for which to set or remove the translation.
                                                         If None, the `first_language` (previously set) will be used.
            key (TextKey, optional): The key of the translation to set or remove. If None, all translations for the
                                 specified language will be removed.
            text (str, optional): The text to set for the translation. If None, the translation for the specified key
                              will be removed.

        Raises:
            TypeError: If the input types are incorrect.

        Examples:
            Set a translation for a specific key and language:
            >>> obj.set_translation(LocaleCode("en_US"), "welcome_message", "Welcome!")

            Set a translation for multiple languages:
            >>> obj.set_translation([LocaleCode("en_US"), LocaleCode("zh_CN")], "welcome_message", "Welcome!")

            Remove a translation for a specific key:
            >>> obj.set_translation(LocaleCode("en_US"), "welcome_message", None)

            Remove all translations for a specific language:
            >>> obj.set_translation(LocaleCode("en_US"), None, None)

            Set a translation using the default `first_language`:
            >>> obj.set_translation(None, "welcome_message", "Welcome!")
        """
        # if locale is not None and not isinstance(locale, LocaleCode):
        #     raise TypeError(f"Expected `locale` to be `LocaleCode` or `None`, but got {type(locale)}.")

        if key is not None and not isinstance(key, TextKey):
            raise TypeError(f"Expected `key` to be `TextKey` or `None`, but got {type(key)}.")

        if text is not None and not isinstance(text, str):
            raise TypeError(f"Expected `text` to be `str` or `None`, but got {type(text)}.")

        # TODO 判断可迭代对象
        # ! 这里使用 isinstance(locale, Iterable) 会出现无限递归错误,
        # ! 无论这个 Iterable 是来自于 collections 还是 typing.
        if isinstance(locale, (list, tuple)):
            for locale_code in locale:
                self.set_translation(locale_code, key, text)
            return

        if locale is not None and not isinstance(locale, LocaleCode):
            raise TypeError(f"Expected `locale` to be `LocaleCode` or `None`, but got {type(locale)}.")

        with self._lock:
            if locale is None:
                locale = self.first_locale

            if key is None:
                if locale in self.__table_translation:
                    del self.__table_translation[locale]
                return

            if text is None:
                if locale in self.__table_translation and key in self.__table_translation[locale]:
                    del self.__table_translation[locale][key]
                return

            if locale not in self.__table_translation:
                self.__table_translation[locale] = {}

            self.__table_translation[locale][key] = text

    def translation(self, key: TextKey, locale: Optional[LocaleCode] = None) -> I18nString:
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
            >>> translation = obj.translation("welcome_message", LocaleCode("en_US"))
            >>> print(translation)
            "Welcome!"

            Get a translation without specifying a locale (uses default or fallback language):
            >>> translation = obj.translation("welcome_message")
            >>> print(translation)
            "欢迎！"

            Get a translation for a non-existent key:
            >>> translation = obj.translation("unknown_key")
            >>> print(translation)
            "unknown_key"  # Returns the key itself as an I18nString object.
        """
        if not isinstance(key, TextKey):
            raise TypeError(f"Expected `key` to be `TextKey`, but got {type(key)}.")

        if locale is not None and not isinstance(locale, LocaleCode):
            raise TypeError(f"Expected `locale` to be `LocaleCode` or `None`, but got {type(locale)}.")

        with self._lock:
            target_locale = locale if locale is not None else self.first_locale
            result = self.__table_translation.get(target_locale, {}).get(key, None)

            if result is None and locale is None:
                result = self.__table_translation.get(self.second_locale, {}).get(key, None)

            if result is None:
                result = self.i18n._attribute_overload(key)

            reply = I18nString(result)
            reply._ctrl_relevance(self.i18n, key)
            return reply

    def load_lang_content(self, content: str, locale: Optional[LocaleCode] = None,
                          superiors: Optional[str] = None) -> None:
        """
        Load language content from a string.

        This method parses the provided language file content and loads it into the current object. If `locale` is
        specified, the content will be associated with that locale; otherwise, the default locale will be used.

        The `superiors` parameter allows you to specify a default prefix for all keys in the content.

        Args:
            content (str): The content of the language file to load.
            locale (LocaleCode, optional): The locale to associate with the content. If None, the default locale
                                           will be used.
            superiors (str, optional): A default prefix to add to all keys in the content.

        Raises:
            TypeError: If `locale` is not an instance of `LocaleCode` or `superiors` is not a string.

        Examples:
            Load content for a specific locale:
            >>> content = '''
            ... welcome = Welcome!
            ... '''
            >>> obj.load_lang_content(content, LocaleCode("en_US"))
            >>> obj.translation("welcome")
            "Welcome!"

            Load content with a default prefix:
            >>> content = '''
            ... welcome = Welcome!
            ... '''
            >>> obj.load_lang_content(content, superiors="app")
            >>> obj.translation("app.welcome")
            "Welcome!"

            Load content with a default prefix and override it using `#define`:
            >>> content = '''
            ... #define superiors custom
            ... welcome = Welcome!
            ... '''
            >>> obj.load_lang_content(content, superiors="app")
            >>> obj.translation("custom.welcome")
            "Welcome!"
            """
        if not isinstance(content, str):
            raise TypeError(f"Expected `content` to be `str`, but got {type(content)}.")

        elif not content:
            return

        if locale is None:
            locale = self.i18n.ctrl_get_locale()[0]

        elif not isinstance(locale, LocaleCode):
            raise TypeError(f"Expected `locale` to be `LocaleCode`, but got {type(locale)}.")

        if superiors is None:
            superiors = ""

        elif not isinstance(superiors, str):
            raise TypeError(f"Expected `superiors` to be `str`, but got {type(superiors)}.")

        content_lines = content.splitlines()
        multiline_mode = False
        multiline_line = []

        for line in content_lines:
            line = line.strip()

            if not multiline_mode:
                if line.startswith("#define"):
                    instruction = line.split(" ")
                    if len(instruction) <= 2:
                        continue

                    define = instruction[1]
                    values = [x for x in instruction[2:] if x]

                    if define == "locale":
                        if not values:
                            continue

                        locale = values

                    elif define == "superiors":
                        if not values or values[0] in [".", "/", "#"]:
                            superiors = ""

                        elif isinstance(values, str):
                            superiors = values

                        elif isinstance(values, list):
                            superiors = ".".join(values)

                    continue

                elif line.startswith("#"):
                    continue

                elif line.startswith(";"):
                    continue

                elif line.startswith("//"):
                    continue

                else:
                    lst = line.split("=", 1)
                    if len(lst) != 2:
                        continue

                    key = lst[0].strip()
                    text = lst[1].strip()

            else:
                text = line.strip()

            if text.endswith(" \\") or text == "\\":
                multiline_mode = True
                text = text[:-2]

            else:
                multiline_mode = False

            if len(text) >= 2 and text.startswith("\"") and text.endswith("\""):
                text = text[1:-1]

            if multiline_mode:
                multiline_line.append(text)
                continue

            final_key = f"{superiors}.{key}" if superiors != "" else key

            if multiline_line:
                multiline_line.append(text)
                text = "".join(multiline_line)
                multiline_line = []

            text = decode_escape_sequences(text)
            self.set_translation(locale, final_key, text)

        else:
            if multiline_line:
                final_key = f"{superiors}.{key}" if superiors != "" else key
                text = "".join(multiline_line)
                text = decode_escape_sequences(text)
                self.set_translation(locale, final_key, text)

    def load_lang(self, file_path: str, locale: Optional[LocaleCode] = None, superiors: Optional[str] = None,
                  *, encoding: str = DEFAULT_ENCODING) -> None:
        """
        Load language content from a file.

        This method reads the content of a language file and loads it into the current object. If `locale` is specified,
        the content will be associated with that locale; otherwise, the default locale will be used.

        The `superiors` parameter allows you to specify a default prefix for all keys in the content.

        Args:
            file_path (str): The path to the language file to load.
            locale (LocaleCode, optional): The locale to associate with the content. If None, the default locale
                                        will be used.
            superiors (str, optional): A default prefix to add to all keys in the content.
            encoding (str, optional): The encoding to use when reading the file. Defaults to `DEFAULT_ENCODING`.

        Raises:
            FileNotFoundError: If the specified file does not exist.
            ValueError: If the file content is empty or invalid.
            TypeError: If `locale` is not an instance of `LocaleCode` or `superiors` is not a string.

        Examples:
            Load content for a specific locale:
            >>> obj.load_lang("path/to/lang_file.txt", LocaleCode("en_US"))

            Load content with a default prefix:
            >>> obj.load_lang("path/to/lang_file.txt", superiors="app")

            Load content with a custom encoding:
            >>> obj.load_lang("path/to/lang_file.txt", encoding="utf-16")
        """
        with open(file_path, "r", encoding=encoding) as file_object:
            content = file_object.read()

        self.load_lang_content(content=content, locale=locale, superiors=superiors)

    def load_csv_i18n(self, file_path: str, *, encoding: str = DEFAULT_ENCODING) -> None:
        """
        Load internationalization content from a CSV file.

        This method reads the content of a CSV file and loads it into the current object. The CSV file must have a header
        row with at least three columns: `locale`, `key`, and `value`. Each row represents a translation entry.

        Args:
            file_path (str): The path to the CSV file to load.
            encoding (str, optional): The encoding to use when reading the file. Defaults to `DEFAULT_ENCODING`.

        Raises:
            FileNotFoundError: If the specified file does not exist.
            ValueError: If the file content is empty, invalid, or improperly formatted.
            UnicodeDecodeError: If the file cannot be decoded with the specified encoding.

        Examples:
            Load content from a CSV file:
            >>> obj.load_csv_i18n("path/to/translations.csv")

            Load content from a CSV file with a custom encoding:
            >>> obj.load_csv_i18n("path/to/translations.csv", encoding="utf-16")

            Example CSV file format:
            >>> locale,key,value
            ... en_US,greeting,Hello
            ... zh_CN,greeting,你好
        """
        with open(file_path, "r", encoding=encoding) as file_object:
            reader = csv.DictReader(file_object)

        for row in reader:
            row: dict
            locale = row["locale"]
            key = row["key"]
            value = row["value"]
            value = decode_escape_sequences(value)

            self.set_translation(locale, key, value)

    def load_dict(self, dictionary: Dict[TextKey, str], locale: LocaleCode, superiors: Optional[str] = None) -> None:
        """
        Load translation content from a dictionary.

        This method loads translation key-value pairs from a dictionary into the current object. The translations will be
        associated with the specified locale. If `superiors` is provided, it will be used as a default prefix for all keys.

        Args:
            dictionary (Dict[TextKey, str]): A dictionary containing translation key-value pairs.
            locale (LocaleCode): The locale to associate with the translations.
            superiors (str, optional): A default prefix to add to all keys. If a key is prefixed with `#define`,
                                    it will override this setting.

        Raises:
            ValueError: If the dictionary is empty or contains invalid data.
            TypeError: If `locale` is not an instance of `LocaleCode` or `superiors` is not a string.

        Examples:
            Load translations for a specific locale:
            >>> translations = {"greeting": "Hello", "farewell": "Goodbye"}
            >>> obj.load_dict(translations, LocaleCode("en_US"))

            Load translations with a default prefix:
            >>> translations = {"greeting": "Hello", "farewell": "Goodbye"}
            >>> obj.load_dict(translations, LocaleCode("en_US"), superiors="app")
        """
        if superiors is None:
            superiors = ""

        elif not isinstance(superiors, str):
            raise TypeError(f"Expected `superiors` to be of type `str`, but got {type(superiors)}.")

        for key, value in dictionary.items():
            final_key = f"{superiors}.{key}" if superiors != "" else key

            if isinstance(value, str):
                self.set_translation(locale, final_key, value)

            elif isinstance(value, dict):
                self.load_dict(value, locale, final_key)

    def load_json(self, file_path: str, locale: Optional[LocaleCode] = None, *, encoding: str = DEFAULT_ENCODING) -> None:
        """
        Load translation content from a JSON file.

        This method reads the content of a JSON file and loads it into the current object. If `locale` is specified,
        the content will be associated with that locale; otherwise, the default locale will be used.

        The JSON file should be formatted as a dictionary where keys are translation keys and values are translation texts.

        Args:
            file_path (str): The path to the JSON file to load.
            locale (LocaleCode, optional): The locale to associate with the content. If None, the default locale
                                           will be used.
            encoding (str, optional): The encoding to use when reading the file. Defaults to `DEFAULT_ENCODING`.

        Raises:
            FileNotFoundError: If the specified file does not exist.
            ValueError: If the file content is empty, invalid, or improperly formatted.
            TypeError: If `locale` is not an instance of `LocaleCode`.
            json.JSONDecodeError: If the file content is not valid JSON.

        Examples:
            Load content for a specific locale:
            >>> obj.load_json("path/to/translations.json", LocaleCode('en_US'))

            Load content without specifying a locale (uses default locale):
            >>> obj.load_json("path/to/translations.json")

            Load content with a custom encoding:
            >>> obj.load_json("path/to/translations.json", encoding="utf-16")
        """
        if superiors is None:
            superiors = ""

        elif not isinstance(superiors, str):
            raise TypeError(f"Excepted `superiors` to be of type `str`, but got {type(superiors)}.")

        with open(file_path, "r", encoding=encoding) as file_object:
            content = file_object.read()

        data = json.loads(content)
        self.load_dict(data, locale)

    def load_json_i18n(self, file_path: str, *, encoding: str = DEFAULT_ENCODING) -> None:
        """
        Load internationalization content from a JSON file.

        This method reads the content of a JSON file and loads it into the current object. The JSON file should be formatted
        as a dictionary where keys are locales and values are dictionaries of translation key-value pairs.

        Args:
            file_path (str): The path to the JSON file to load.
            encoding (str, optional): The encoding to use when reading the file. Defaults to `DEFAULT_ENCODING`.

        Raises:
            FileNotFoundError: If the specified file does not exist.
            ValueError: If the file content is empty, invalid, or improperly formatted.
            json.JSONDecodeError: If the file content is not valid JSON.

        Examples:
            Load content from a JSON file:
            >>> obj.load_json_i18n("path/to/translations.json")

            Load content from a JSON file with a custom encoding:
            >>> obj.load_json_i18n("path/to/translations.json", encoding="utf-16")

            Example JSON file format:
            >>> {
            ...     "en_US": {
            ...         "greeting": "Hello",
            ...         "farewell": "Goodbye"
            ...     },
            ...     "zh_CN": {
            ...         "greeting": "你好",
            ...         "farewell": "再见"
            ...     }
            ... }
        """
        with open(file_path, "r", encoding=encoding) as file_object:
            content = file_object.read()

        data = json.loads(content)
        for locale, dictionary in data.items():
            self.load_dict(dictionary, locale)

    def auto_load(self, path: str, *, locale: Optional[LocaleCode] = None) -> None:
        """
        Automatically load all language files from a directory.

        This method scans the specified directory and loads all supported language files (e.g., `.lang`, `.json`, `.csv`).
        The behavior depends on whether the `locale` parameter is specified:

        1. If `locale` is specified:
        - The directory should contain files without locale codes in their names.
        - All files will be associated with the specified `locale`.
        - Example structure:
            ```
            path
            ├── xxx.lang
            ├── xxx.lang
            ├── xxx.json
            └── xxx.csv
            ```

        2. If `locale` is not specified:
        - The directory can be structured in one of the following ways:
            - Flat structure: Files contain locale codes in their names (e.g., `zh_CN.lang`).
            ```
            path
            ├── zh_CN.lang
            ├── en_US.lang
            ├── ru_RU.lang
            ├── zh_CN.json
            └── xxx.csv
            ```
            - Nested structure: Files are organized into subdirectories named by locale codes.
            ```
            path
            ├── zh_CN
            │   ├── xxx.lang
            │   ├── xxx.lang
            │   └── xxx.json
            └── en_US
                ├── xxx.lang
                ├── xxx.lang
                └── xxx.json
            ```
        - The locale will be inferred from the file names or subdirectory names.

        Args:
            path (str): The path to the directory containing language files.
            locale (LocaleCode, optional): The locale to associate with the loaded content. If None, the locale will be
                                        inferred from the file names or subdirectory names.

        Raises:
            FileNotFoundError: If the specified directory does not exist.
            ValueError: If the directory is empty, contains no supported language files, or file/directory names are invalid.
            TypeError: If `locale` is not an instance of `LocaleCode`.

        Examples:
            Load files for a specific locale:
            >>> obj.auto_load("path/to/directory", locale=LocaleCode("en_US"))

            Load files and infer locale from file names (flat structure):
            >>> obj.auto_load("path/to/flat_directory")

            Load files and infer locale from subdirectory names (nested structure):
            >>> obj.auto_load("path/to/nested_directory")
        """
        for filename in os.listdir(path):
            filepath = os.path.join(path, filename)

            if os.path.isdir(filepath) and locale is Ellipsis:
                self.auto_load(filepath, locale=filename)

            if not os.path.isfile(filepath):
                continue

            lst = filename.rsplit(".", 1)
            if len(lst) < 2: continue
            name, suffix = lst

            if locale is None:
                if suffix == "json":    self.load_json(filepath, locale=name)
                elif suffix == "csv":   self.load_csv_i18n(filepath)
                elif suffix == "lang":  self.load_lang(filepath, locale=name)
                else: continue

            else:
                if suffix == "json":    self.load_json(filepath, locale=locale)
                elif suffix == "csv":   self.load_csv_i18n(filepath)
                elif suffix == "lang":  self.load_lang(filepath, locale=locale, superiors=name)
                else: continue
