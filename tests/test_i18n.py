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
        self.i18n_ctrl = i18nco.I18nControl(self.i18n)

    def test_access(self) -> None:
        self.i18n.ctrl_set_translation(None, "a.b", "access")
        self.assertEqual(self.i18n.a.b, "access")

    def test_fa(self) -> None:
        self.i18n.ctrl_set_translation(zh_CN, "ta1", "zh_CN-ta1")
        self.i18n.ctrl_set_locale(second_language=zh_CN)
        self.assertEqual(self.i18n.ta1, "zh_CN-ta1")
