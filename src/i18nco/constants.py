# Licensed under the LGPL 3.0 License.
# i18nco by numlinka.

# writing system | 文字系统
LATIN_ALPHABET = "Latin Alphabet"
CHINESE_CHARACTERS = "Chinese Characters"
CYRILLIC_ALPHABET = "Cyrillic Alphabet"
ARABIC_ALPHABET = "Arabic Alphabet"
DEVANAGARI_ALPHABET = "Devanagari Alphabet"
GREEK_ALPHABET = "Greek Alphabet"
JAPANESE_KANA = "Japanese Kana"
HANGUL = "Hangul"
THAI_ALPHABET = "Thai Alphabet"
HEBREW_ALPHABET = "Hebrew Alphabet"
KHMER_ALPHABET = "Khmer Alphabet"
ETHIOPIC_OR_GE_EZ_SCRIPT = "Ethiopic or Ge'ez Script"
GEORGIAN_ALPHABET = "Georgian Alphabet"
TAMIL_SCRIPT = "Tamil Script"


# Latin Alphabet | 拉丁文
en_US, en_US_lang = "en_US", "English (United States)"
en_GB, en_GB_lang = "en_GB", "English (United Kingdom)"
es_ES, es_ES_lang = "es_ES", "Español (España)"
fr_FR, fr_FR_lang = "fr_FR", "Français (France)"
de_DE, de_DE_lang = "de_DE", "Deutsch (Deutschland)"
it_IT, it_IT_lang = "it_IT", "Italiano (Italia)"
pt_PT, pt_PT_lang = "pt_PT", "Português (Portugal)"
pt_BR, pt_BR_lang = "pt_BR", "Português (Brasil)"
en_SG, en_SG_lang = "en_SG", "English (Singapore)"
ms_SG, ms_SG_lang = "ms_SG", "Bahasa Melayu (Singapura)"
en_MY, en_MY_lang = "en_MY", "English (Malaysia)"
ms_MY, ms_MY_lang = "ms_MY", "Bahasa Melayu (Malaysia)"

# Chinese Characters | 汉字
zh_CN, zh_CN_lang = "zh_CN", "简体中文 (中国)"
zh_HK, zh_HK_lang = "zh_HK", "繁體中文 (中國香港)"
zh_MO, zh_MO_lang = "zh_MO", "繁體中文 (中國澳門)"
zh_TW, zh_TW_lang = "zh_TW", "繁體中文 (中國台灣)"
zh_SG, zh_SG_lang = "zh_SG", "中文 (新加坡)"
zh_MY, zh_MY_lang = "zh_MY", "中文 (马来西亚)"

# Cyrillic Alphabet | 希利尔文
ru_RU, ru_RU_lang = "ru_RU", "Русский (Россия)"
uk_UA, uk_UA_lang = "uk_UA", "Українська (Україна)"
bg_BG, bg_BG_lang = "bg_BG", "Български (България)"
sr_RS, sr_RS_lang = "sr_RS", "Српски (Србија)"

# Arabic Alphabet | 阿拉伯文
ar_SA, ar_SA_lang = "ar_SA", "العربية (المملكة العربية السعودية)"
ar_EG, ar_EG_lang = "ar_EG", "العربية (مصر)"
fa_IR, fa_IR_lang = "fa_IR", "فارسی (ایران)"
ur_PK, ur_PK_lang = "ur_PK", "اُردُو (پاکستان)"

# Devanagari Alphabet | 梵文
hi_IN, hi_IN_lang = "hi_IN", "हिंदी (भारत)"
ne_NP, ne_NP_lang = "ne_NP", "नेपाली (नेपाल)"

# Greek Alphabet | 希腊文
el_GR, el_GR_lang = "el_GR", "Ελληνικά (Ελλάδα)"
el_CY, el_CY_lang = "el_CY", "Ελληνικά (Κύπρος)"

# Japanese Kana | 日文假名
ja_JP, ja_JP_lang = "ja_JP", "日本語 (日本)"

# Hangul | 韩文
ko_KR, ko_KR_lang = "ko_KR", "한국어 (대한민국)"
ko_KP, ko_KP_lang = "ko_KP", "조선말 (조선 민주주의 인민 공화국)"

# Thai Alphabet | 泰文
th_TH, th_TH_lang = "th_TH", "ไทย (ประเทศไทย)"

# Hebrew Alphabet | 希伯来文
he_IL, he_IL_lang = "he_IL", "עברית (ישראל)"
yi_001, yi_001_lang = "yi_001", "ייִדיש (יידיש)"

# Khmer Alphabet | 柬埔寨文
km_KH, km_KH_lang = "km_KH", "ភាសាខ្មែរ (កម្ពុជា)"

# Ethiopic or Ge'ez Script | 埃塞俄比亚文
am_ET, am_ET_lang = "am_ET", "አማርኛ (ኢትዮጵያ)"
ti_ER, ti_ER_lang = "ti_ER", "ትግርኛ (ኤርትራ)"
et_EE, et_EE_lang = "et_EE", "አማርኛ (ኢትዮጵያ)"

# Georgian Alphabet | 格鲁吉亚文
ka_GE, ka_GE_lang = "ka_GE", "ქართული (საქართველო)"

# Tamil Script | 泰米尔文
ta_IN, ta_IN_lang = "ta_IN", "தமிழ் (இந்தியா)"
ta_LK, ta_LK_lang = "ta_LK", "தமிழ் (இலங்கை)"
ta_MY, ta_MY_lang = "ta_MY", "தமிழ் (மலேசியா)"
ta_SG, ta_SG_lang = "ta_SG", "தமிழ் (சிங்கப்பூர்)"


LATIN_ALPHABET_TABLE = {
    en_US: en_US_lang,
    en_GB: en_GB_lang,
    es_ES: es_ES_lang,
    fr_FR: fr_FR_lang,
    de_DE: de_DE_lang,
    it_IT: it_IT_lang,
    pt_PT: pt_PT_lang,
    pt_BR: pt_BR_lang,
    en_SG: en_SG_lang,
    ms_SG: ms_SG_lang,
    en_MY: en_MY_lang,
    ms_MY: ms_MY_lang,
}

CHINESE_CHARACTERS_TABLE = {
    zh_CN: zh_CN_lang,
    zh_HK: zh_HK_lang,
    zh_MO: zh_MO_lang,
    zh_TW: zh_TW_lang,
    zh_SG: zh_SG_lang,
    zh_MY: zh_MY_lang,
    ja_JP: ja_JP_lang,
    ko_KR: ko_KR_lang,
    ko_KP: ko_KP_lang,
}

CYRILLIC_ALPHABET_TABLE = {
    ru_RU: ru_RU_lang,
    uk_UA: uk_UA_lang,
    bg_BG: bg_BG_lang,
    sr_RS: sr_RS_lang,
}

ARABIC_ALPHABET_TABLE = {
    ar_SA: ar_SA_lang,
    ar_EG: ar_EG_lang,
    fa_IR: fa_IR_lang,
    ur_PK: ur_PK_lang,
}
DEVANAGARI_ALPHABET_TABLE = {
    hi_IN: hi_IN_lang,
    ne_NP: ne_NP_lang,
}

GREEK_ALPHABET_TABLE = {
    el_GR: el_GR_lang,
    el_CY: el_CY_lang,
}

JAPANESE_KANA_TABLE = {
    ja_JP: ja_JP_lang,
}

HANGUL_TABLE = {
    ko_KR: ko_KR_lang,
    ko_KP: ko_KP_lang,
}

THAI_ALPHABET_TABLE = {
    th_TH: th_TH_lang,
}

HEBREW_ALPHABET_TABLE = {
    he_IL: he_IL_lang,
    yi_001: yi_001_lang,
}

KHMER_ALPHABET_TABLE = {
    km_KH: km_KH_lang,
}

ETHIOPIC_OR_GE_EZ_SCRIPT_TABLE = {
    am_ET: am_ET_lang,
    ti_ER: ti_ER_lang,
    et_EE: et_EE_lang,
}

GEORGIAN_ALPHABET_TABLE = {
    ka_GE: ka_GE_lang,
}

TAMIL_SCRIPT_TABLE = {
    ta_IN: ta_IN_lang,
    ta_LK: ta_LK_lang,
    ta_MY: ta_MY_lang,
    ta_SG: ta_SG_lang,
}


LANGUAGE_TABLE = {
    **LATIN_ALPHABET_TABLE,
    **CHINESE_CHARACTERS_TABLE,
    **CYRILLIC_ALPHABET_TABLE,
    **ARABIC_ALPHABET_TABLE,
    **DEVANAGARI_ALPHABET_TABLE,
    **GREEK_ALPHABET_TABLE,
    **JAPANESE_KANA_TABLE,
    **HANGUL_TABLE,
    **THAI_ALPHABET_TABLE,
    **HEBREW_ALPHABET_TABLE,
    **KHMER_ALPHABET_TABLE,
    **ETHIOPIC_OR_GE_EZ_SCRIPT_TABLE,
    **GEORGIAN_ALPHABET_TABLE,
    **TAMIL_SCRIPT_TABLE,
}

WRITING_SYSTEM_TABLE = {
    LATIN_ALPHABET: LATIN_ALPHABET_TABLE,
    CHINESE_CHARACTERS: CHINESE_CHARACTERS_TABLE,
    CYRILLIC_ALPHABET: CYRILLIC_ALPHABET_TABLE,
    ARABIC_ALPHABET: ARABIC_ALPHABET_TABLE,
    DEVANAGARI_ALPHABET: DEVANAGARI_ALPHABET_TABLE,
    GREEK_ALPHABET: GREEK_ALPHABET_TABLE,
    JAPANESE_KANA: JAPANESE_KANA_TABLE,
    HANGUL: HANGUL_TABLE,
    THAI_ALPHABET: THAI_ALPHABET_TABLE,
    HEBREW_ALPHABET: HEBREW_ALPHABET_TABLE,
    KHMER_ALPHABET: KHMER_ALPHABET_TABLE,
    ETHIOPIC_OR_GE_EZ_SCRIPT: ETHIOPIC_OR_GE_EZ_SCRIPT_TABLE,
}


__all__ = [x for x in globals() if not x.startswith("_")]
