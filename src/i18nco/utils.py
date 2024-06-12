# Licensed under the LGPL 3.0 License.
# i18nco by numlinka.

# std
import os
import re
from typing import Union

# self
from .schemas import *
from .constants import *


escape_sequence_re = re.compile(r'\\(u[0-9A-Fa-f]{4}|U[0-9A-Fa-f]{8}|x[0-9A-Fa-f]{2}|.)')


def decode_escape_sequences(text: str) -> str:
    def replace_escape(match):
        escape = match.group(1)
        if escape.startswith('u') or escape.startswith('U'):
            return chr(int(escape[1:], 16))
        elif escape.startswith('x'):
            return chr(int(escape[1:], 16))
        elif escape == 'n':
            return '\n'
        elif escape == 't':
            return '\t'
        elif escape == 'b':
            return '\b'
        elif escape == 'r':
            return '\r'
        elif escape == 'f':
            return '\f'
        elif escape == 'a':
            return '\a'
        elif escape == 'v':
            return '\v'
        else:
            return escape

    return escape_sequence_re.sub(replace_escape, text)


def get_locale_code() -> LocaleCode:
    """
    ## get system locale code
    ## 获取系统语言环境代码

    获取失败时返回一个空字符串
    """

    ors = os.environ.get("LANG", "")
    return ors.split(".")[0]


def match_best_locale(target: LocaleCode, available: LocaleCodeList) -> Union[LocaleCode, None]:
    """
    ## match best locale code
    ## 匹配最佳语言环境代码

    ### Parameters
    - target: LocaleCode
        目标语言环境代码
    - available: LocaleCodeList
        可用语言环境代码列表

    ### Returns
    - LocaleCode
        最佳语言环境代码
    """
    if not target or not available:
        return None

    if target in available:
        return target

    language_code = target.split("_")[0]
    for locale in available:
        if locale.startswith(language_code):
            return locale

    for _, table in WRITING_SYSTEM_TABLE.items():
        if target in table:
            break

    else:
        return None

    for locale in table:
        if locale in available:
            return locale

    return None


class InstructionBreakdown (object):
    @staticmethod
    def define(message: str) -> tuple[str, Union[str, list[str], None]]:
        if not message.startswith("#define"):
            return "", None

        commands = message.split(" ")
        if len(commands) > 2:
            define = commands[1]
            values = commands[2:]

        else:
            define = commands[1]
            value = None
            return define, value

        values = [x for x in values if x]
        if len(values) == 1:
            values = values[0]

        if not values:
            values = None

        return define, values


__all__ = [
    "decode_escape_sequences",
    "get_locale_code",
    "match_best_locale",
    "InstructionBreakdown"
]
