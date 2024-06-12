# Licensed under the LGPL 3.0 License.
# i18nco by numlinka.

# std
import os
import csv
import json
from typing import *

# self
from .utils import *
from .schemas import *
from .i18nbase import BaseI18n


class I18nCSVLoad (object):
    def __init__(self) -> None:
        if isinstance(self, BaseI18n):
            raise TypeError("I18nCSVLoad is not a base class")

    def con_load_csv_i18n(self, file_path: str, *, encoding: str = "utf-8") -> None:
        self: BaseI18n
        with open(file_path, "r", encoding=encoding) as file_object:
            reader = csv.DictReader(file_object)

        for row in reader:
            row: dict
            locale = row["locale"]
            key = row["key"]
            value = row["value"]
            value = decode_escape_sequences(value)

            self.con_add_translation(locale, key, value)


class I18nJsonLoad (object):
    def __init__(self) -> None:
        if isinstance(self, BaseI18n):
            raise TypeError("I18nJsonLoad is not a base class")

    def con_load_dict(self, dictionary: Dict[TextKey, str], locale: LocaleCode = ..., superiors: str = ...) -> None:
        self: BaseI18n
        if superiors is Ellipsis:
            superiors = ""

        for key, value in dictionary.items():
            final_key = f"{superiors}.{key}" if superiors != "" else key

            if isinstance(value, str):
                self.con_add_translation(locale, final_key, value)

            elif isinstance(value, dict):
                self.con_load_dict(value, locale, final_key)

    def con_load_json(self, file_path: str, locale: LocaleCode = ..., *, encoding: str = "utf-8") -> None:
        self: BaseI18n
        if locale is ...:
            locale = self.con_get_locale()

        with open(file_path, "r", encoding=encoding) as file_object:
            content = file_object.read()

        data = json.loads(content)
        self.con_load_dict(data, locale)

    def con_load_json_i18n(self, file_path: str, *, encoding: str = "utf-8") -> None:
        self: BaseI18n
        with open(file_path, "r", encoding=encoding) as file_object:
            content = file_object.read()

        data = json.loads(content)
        for locale, dictionary in data.items():
            self.con_load_dict(dictionary, locale)


class I18nLangLoad (object):
    def __init__(self) -> None:
        if isinstance(self, BaseI18n):
            raise TypeError("I18nLangLoad is not a base class")

    def con_load_lang(self, file_path: str, locale: LocaleCode = ..., superiors: str = ...,
                      *, encoding: str = "utf-8") -> None:
        self: BaseI18n
        if locale is ...:
            locale = self.con_get_locale()

        if superiors is ...:
            superiors = ""

        with open(file_path, "r", encoding=encoding) as file_object:
            contents = file_object.readlines()

        multiline_mode = False
        multiline_line = []
        key = ""

        for line in contents:
            line = line.strip()
            print(superiors)

            if not multiline_mode:
                if line.startswith("#define"):
                    define, value = InstructionBreakdown.define(line)

                    if define == "locale":
                        if not value:
                            continue

                        locale = value

                    elif define == "superiors":
                        if not value or value == "." or value == "/":
                            superiors = ""

                        elif isinstance(value, str):
                            superiors = value

                        elif isinstance(value, list):
                            superiors = ".".join(value)

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
                    line = lst[1].strip()

            if line.endswith(" \\"):
                multiline_mode = True
                line = line[:-2]

            else:
                multiline_mode = False

            if len(line) >= 2 and line.startswith('"') and line.endswith('"'):
                line = line[1:-1]

            if multiline_mode:
                multiline_line.append(line)
                continue

            final_key = f"{superiors}.{key}" if superiors != "" else key

            if multiline_line:
                multiline_line.append(line)
                line = "\n".join(multiline_line)
                multiline_line = []

            line = decode_escape_sequences(line)
            self.con_add_translation(locale, final_key, line)

        else:
            if multiline_line:
                final_key = f"{superiors}.{key}" if superiors != "" else key
                line = "\n".join(multiline_line)
                line = decode_escape_sequences(line)
                self.con_add_translation(locale, final_key, line)


class I18nAutoLoad (object):
    def __init__(self):
        if isinstance(self, BaseI18n):
            raise TypeError("I18nAutoLoad is not a base class")

    def con_auto_load(self, path: str, *, locale: LocaleCode = ...):
        self: Union[I18nCSVLoad, I18nJsonLoad, I18nLangLoad, I18nAutoLoad]
        for filename in os.listdir(path):
            filepath = os.path.join(path, filename)

            if os.path.isdir(filepath) and locale is Ellipsis:
                self.con_auto_load(filepath, locale=filename)

            if not os.path.isfile(filepath):
                continue

            lst = filename.rsplit(".", 1)
            if len(lst) < 2:
                continue
            name, suffix = lst

            if locale is Ellipsis:
                if suffix == "json":
                    self.con_load_json(filepath, locale=name)
                elif suffix == "csv":
                    self.con_load_csv_i18n(filepath)
                elif suffix == "lang":
                    self.con_load_lang(filepath, locale=name)
                else:
                    continue

            else:
                if suffix == "json":
                    self.con_load_json(filepath, locale=locale)
                elif suffix == "csv":
                    self.con_load_csv_i18n(filepath)
                elif suffix == "lang":
                    self.con_load_lang(filepath, locale=locale, superiors=name)
                else:
                    continue


__all__ = [
    "I18nCSVLoad",
    "I18nJsonLoad",
    "I18nLangLoad",
    "I18nAutoLoad"
]
