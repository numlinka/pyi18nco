# Licensed under the MIT License.
# i18nco Copyright (C) 2022 numlinka.

# std
import unittest

# tests
import i18nco
from i18nco.constants import *


class TestUtils (unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.i18n = i18nco.Internationalization()

    def test_set_locale(self) -> None:
        self.i18n.ctrl.set_locale(zh_CN, en_US)
        self.assertEqual(self.i18n.ctrl.first_locale, zh_CN)
        self.assertEqual(self.i18n.ctrl.second_locale, en_US)

    def test_set_locale_auto_adjust(self) -> None:
        self.i18n.ctrl.set_translation(zh_CN, zh_CN, zh_CN_lang)
        self.i18n.ctrl.set_translation(zh_HK, zh_HK, zh_HK_lang)
        self.i18n.ctrl.set_locale(zh_CN)
        self.assertEqual(self.i18n.ctrl.second_locale, zh_HK)

    def test_set_translation(self) -> None:
        self.i18n.ctrl.set_translation(zh_CN, "lang_name", zh_CN_lang)
        self.i18n.ctrl.set_translation(en_US, "lang_name", en_US_lang)
        self.assertEqual(self.i18n.ctrl.translation("lang_name", zh_CN), zh_CN_lang)
        self.assertEqual(self.i18n.ctrl.translation("lang_name", en_US), en_US_lang)

    def test_set_translation_more(self) -> None:
        self.i18n.ctrl.set_translation([en_US, en_GB], "more_lang", "more lang")
        self.assertEqual(self.i18n.ctrl.translation("more_lang", en_US), "more lang")
        self.assertEqual(self.i18n.ctrl.translation("more_lang", en_GB), "more lang")

    def test_attribute_overload(self) -> None:
        self.assertEqual(self.i18n.attribute.overload, "attribute.overload")
        self.i18n.ctrl.set_translation(zh_CN, "attribute.overload", "属性重载")
        self.i18n.ctrl.set_locale(zh_CN)
        self.assertEqual(self.i18n.attribute.overload, "属性重载")
