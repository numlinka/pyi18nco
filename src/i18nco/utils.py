# Licensed under the MIT License.
# i18nco Copyright (C) 2022 numlinka.

__all__ = [
    "decode_escape_sequences",
    "get_locale_code",
    "match_best_locale"
]

# std
import os
import re
import sys
import ctypes
import locale
from typing import List, Optional

# self
from .typeins import LocaleCode
from .constants import en_US, WRITING_SYSTEM_TABLE, UNITED_NATIONS_LANGUAGE_LIST


ESCAPE_SEQUENCE_RE = re.compile("\\\\(u[0-9A-Fa-f]{4}|U[0-9A-Fa-f]{8}|x[0-9A-Fa-f]{2}|.)")


def decode_escape_sequences(text: str) -> str:
    """
    Decodes escape sequences in a string to their corresponding characters.

    Supports multiple escape sequence formats including:
    - Unicode: \\uXXXX (16-bit), \\UXXXXXXXX (32-bit)
    - Hexadecimal: \\xXX
    - Common escape characters: \\n, \\t, \\b, \\r, \\f, \\a, \\v
    - Special cases: \\\\ (backslash), \\0 (null), \\_ (space)
    - Unrecognized escape sequences are preserved as-is

    Args:
        text (str): Input string containing escape sequences

    Returns:
        out (str): Decoded string with all escape sequences replaced by their corresponding characters
    """
    def replace_escape(match):
        escape = match.group(1)
        if escape.startswith("u") or escape.startswith("U"):
            return chr(int(escape[1:], 16))
        elif escape.startswith("x"):
            return chr(int(escape[1:], 16))
        elif escape == "n":
            return "\n"
        elif escape == "t":
            return "\t"
        elif escape == "b":
            return "\b"
        elif escape == "r":
            return "\r"
        elif escape == "f":
            return "\f"
        elif escape == "a":
            return "\a"
        elif escape == "v":
            return "\v"
        elif escape == "0":
            return "\0"
        elif escape == "\\":
            return "\\"
        elif escape == "_":
            return " "
        else:
            return escape

    return ESCAPE_SEQUENCE_RE.sub(replace_escape, text)


def get_locale_code() -> LocaleCode:
    """
    Get the system locale code in the format "lang_COUNTRY" (e.g., "en_US").
    Defaults to "en_US" if no locale can be determined.

    Returns:
        out (LocaleCode): The system locale code in the format "lang_COUNTRY" (e.g., "en_US").
    """
    locale_info = os.environ.get("LANG", "")
    locale_code = locale_info.split(".")[0] if locale_info else ""
    if locale_code:
        return locale_code

    try:
        locale_code = locale.getdefaultlocale()[0]
        if locale_code:
            return locale_code

    except AttributeError:
        pass

    if sys.platform == "win32":
        try:
            windll = ctypes.windll.kernel32
            language_id = windll.GetUserDefaultUILanguage()
            locale_code = locale.windows_locale.get(language_id, "")
            if locale_code:
                return locale_code

        except Exception:
            pass

    return en_US


def match_best_locale(target: LocaleCode, available: List[LocaleCode]) -> Optional[LocaleCode]:
    """
    Finds the best matching locale from available options for a target locale.

    The matching is performed in the following priority order:
    1. Exact match (e.g., target "en_US" matches available "en_US")
    2. Language code match (e.g., target "en_US" matches available "en_BG")
    3. Writing system match (e.g., target "en_US" matches available "de_DE")

    Args:
        target (LocaleCode): The target locale code to match against (e.g., "en_US")
        available (List[LocaleCode]): List of available locale codes (e.g., ["en_US", "en_GB"])

    Returns:
        out (LocaleCode | None): The best matching locale code from available options, or `None` if no match found.
    """
    if not isinstance(target, LocaleCode):
        raise TypeError(
            f"Expected `target` to be of type `LocaleCode`, but got {type(target)}.")

    if not isinstance(available, (list, tuple)) or not all(isinstance(locale, LocaleCode) for locale in available):
        raise TypeError(
            f"Expected `available` to be a `list` of `LocaleCode`, but got {type(available)}.")

    if target in available:
        return target

    language_code = target.split("_")[0]
    for locale_code in available:
        if locale_code.startswith(language_code):
            return locale_code

    for _, table in WRITING_SYSTEM_TABLE.items():
        if target not in table:
            continue

        for locale_code in table:
            if locale_code in available:
                return locale_code

    for language_code in UNITED_NATIONS_LANGUAGE_LIST:
        for locale_code in available:
            if locale_code.startswith(language_code):
                return locale_code

    return None
