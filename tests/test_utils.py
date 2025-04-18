# Licensed under the MIT License.
# i18nco Copyright (C) 2022 numlinka.

# std
import unittest

# tests
import i18nco.utils
from i18nco.constants import *


class TestUtils (unittest.TestCase):
    def test_decode_escape_sequences(self) -> None:
        alt = i18nco.utils.decode_escape_sequences
        self.assertEqual(alt(""), "")
        self.assertEqual(alt("\\n"), "\n")
        self.assertEqual(alt("\\t"), "\t")
        self.assertEqual(alt("\\\\"), "\\")
        self.assertEqual(alt("\\\""), "\"")
        self.assertEqual(alt("\\\\a"), "\\a")

        self.assertEqual(alt("\\u001a"), "\u001a")
        self.assertEqual(alt("\\u004c"), "\u004c")
        self.assertEqual(alt("\\x7c"), "\x7c")
        self.assertEqual(alt("\\x64"), "\x64")

    def test_get_locale_code(self) -> None:
        alt = i18nco.utils.get_locale_code
        self.assertTrue(alt())

    def test_match_best_locale(self) -> None:
        alt = i18nco.utils.match_best_locale
        self.assertEqual(alt(en_US, [en_US, en_GB]), en_US)
        self.assertEqual(alt(en_US, [en_GB, en_US]), en_US)
        self.assertEqual(alt(en_US, [en_GB, ru_RU]), en_GB)
        self.assertEqual(alt(en_US, [zh_CN, ru_RU]), None)
