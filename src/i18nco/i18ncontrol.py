# Licensed under the MIT License.
# i18nco Copyright (C) 2022 numlinka.

__all__ = ["I18nControl"]

# std
import os
import csv
import json
from typing import Tuple, List, Dict, Union, Optional

# int
from .typeins import *
from .constants import DEFAULT_ENCODING
from .internationalization import Internationalization, I18nString
from .utils import *


class I18nControl:
    def __init__(self, i18n: Optional[Internationalization] = None) -> None:
        """
        Initialize an I18nControl instance.

        I18nControl is an extension controller for `Internationalization`, providing more convenient ways to manage
        internationalization content. If no `Internationalization` object is provided, a new instance will be created
        automatically.

        Args:
            i18n (Internationalization, optional): The `Internationalization` object to use. If None, a new instance
                                                   will be created automatically.

        Raises:
            TypeError: If the provided `i18n` is not an instance of `Internationalization`.

        Examples:
            Initialize with an existing `Internationalization` object:
            >>> i18n = Internationalization()
            >>> controller = I18nControl(i18n)

            Initialize without an `Internationalization` object (a new instance will be created):
            >>> controller = I18nControl()
        """
        if i18n is None:
            self.i18n = Internationalization()

        elif isinstance(i18n, Internationalization):
            self.i18n = i18n

        else:
            raise TypeError(f"Expected `i18n` to be an instance of `Internationalization`, but got {type(i18n)}.")

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
        if isinstance(locale, list):
            for locale_code in locale:
                self.i18n.ctrl_set_translation(locale=locale_code, key=key, text=text)

        else:
            self.i18n.ctrl_set_translation(locale=locale, key=key, text=text)

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
        return self.i18n.ctrl_translation(key, locale)

    def available_locales(self) -> List[LocaleCode]:
        """
        Get the list of languages supported by the current object.

        This method returns a list of languages that the current object supports. Each language is represented
        as a `LocaleCode` object. The list can be used to determine available localization options.

        Returns:
            out (List[LocaleCode]): A list of supported languages, where each item is a `LocaleCode` object.

        Examples:
            Get the list of supported languages:
            >>> available_languages = obj.available_locales()
            >>> print(available_languages)
            [LocaleCode("en_US"), LocaleCode("zh_CN"), LocaleCode("ru_RU")]
        """
        return self.i18n.ctrl_available_locales()

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

        if first_language is None:
            first_language = self.i18n.ctrl_get_locale()[0]

        if second_language is None and auto_adjust:
            second_language = match_best_locale(first_language, self.available_locales())

        self.i18n.ctrl_set_locale(first_language, second_language)

    def get_locale(self) -> Tuple[LocaleCode, LocaleCode]:
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
            >>> primary, secondary = obj.get_locale()
            >>> print(primary, secondary)
            LocaleCode("en_US") LocaleCode("zh_CN")
        """
        return self.i18n.ctrl_get_locale()

    def load_lang_content(self, content: str, locale: Optional[LocaleCode] = None, superiors: Optional[str] = None) -> None:
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
