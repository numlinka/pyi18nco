# Licensed under the LGPL 3.0 License.
# simplepylibs by numlinka.
# unit test

# std
import unittest

# tests
import i18nco.utils


class TestUtils (unittest.TestCase):
    def test_decode_escape_sequences(self) -> None:
        alt = i18nco.utils.decode_escape_sequences
        self.assertEqual(alt(""), "")
        self.assertEqual(alt("\\n"), "\n")
        self.assertEqual(alt("\\t"), "\t")
        self.assertEqual(alt("\\\\"), "\\")
        self.assertEqual(alt("\\\""), "\"")

        self.assertEqual(alt("\\u001a"), "\u001a")
        self.assertEqual(alt("\\u004c"), "\u004c")
        self.assertEqual(alt("\\x7c"), "\x7c")
        self.assertEqual(alt("\\x64"), "\x64")

    def test_get_locale_code(self) -> None:
        alt = i18nco.utils.get_locale_code
        self.assertTrue(alt())

    def test_InstructionBreakdown_define(self) -> None:
        alt = i18nco.utils.InstructionBreakdown.define
        self.assertEqual(alt(""), ("", []))
        self.assertEqual(alt("#define"), ("", []))
        self.assertEqual(alt("#define a"), ("a", []))
        self.assertEqual(alt("#define a b"), ("a", ["b"]))
        self.assertEqual(alt("#define a b c"), ("a", ["b", "c"]))
        self.assertEqual(alt("#define a b c d"), ("a", ["b", "c", "d"]))
