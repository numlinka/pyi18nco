<div align="center">

<a style="text-decoration:none" href="https://github.com/numlinka/pylogop">
  <img width="128px" src="favicon.png" alt="pylogop">
</a>

# pyi18nco

_This is a simple and easy to use Python i18n library._

<a style="text-decoration:none" href="https://www.gnu.org/licenses/lgpl-3.0.en.html">
  <img src="https://img.shields.io/badge/License-LGPLv3-lightblue" alt="LGPLv3"/>
</a>
<a style="text-decoration:none" href="https://pypi.org/project/i18nco">
  <img src="https://img.shields.io/badge/PyPI-i18nco-lightblue" alt="PyPI"/>
</a>
<a style="text-decoration:none" href="https://www.python.org">
  <img src="https://img.shields.io/badge/Python-3.9+-lightblue" alt="Python3.9+"/>
</a>

<p></p>

English | [简体中文](README_zh.md)


<div align="left" style="max-width: 1000px;">

## Introduce

This is a simple and easy to use Python i18n library.
It is a library independent from [simplepylibs](https://github.com/numlinka/simplepylibs).


## Install

The preferred way to install i18nco is via pip.

```bash
pip install i18nco
```

To upgrade i18nco to the latest version, use the following command:

```shell
pip install --upgrade i18nco
```


## Usage

Here is a simple usage example:

```Python
import i18nco

i18n = i18nco.Internationalization()
i18n.con_auto_load("./i18n")
i18n.con_auto_set_best_locale()

print(i18n.con_translation("hello"))
print(i18n.hello)
```

In `Internationalization`, all methods start with `con_`.
When you access other properties, they will be overridden to the `con_translation` method.

con (control)

`con_auto_load()` will load the language files in the directory. The folder level cannot exceed 2 levels.

`con_auto_set_best_locale()` will automatically select the best language based on the system language.


## Language file 

I have tried to make `pyi18nco` support more language file formats, but their adaptability is still limited.

### .lang File Format Specification

Since .lang files do not have a fixed format, we have established some special syntax rules.

#### Key-Value Pair Format

```lang
; en_US.lang

; This is a comment
// This is also a comment

hello = Hello
world = World

mode.singleton = Singleton Mode

; Comments cannot appear after statements
mode.singleton = Singleton Mode ; This is not a comment

; If you want to preserve leading and trailing spaces, use "" to enclose the string
separation " | "

; Multiline text
robert = I have become death \
         the destroyer of worlds
```

#### Loading Language Files

After preparing the .lang file, use `con_load_lang` to load it:

```Python
# Load the en_US.lang file and set the language to en_US
i18n.con_load_lang("./i18n/en_US.lang", "en_US")

print(i18n.con_translation("hello"))  # Output: Hello
print(i18n.world)                     # Output: World
print(i18n.mode.singleton)            # Output: Singleton Mode
```

Note: If you do not pass the `locale` parameter, `pyi18nco` will automatically detect the system's current language.

You can pass the `superiors` parameter to the `con_load_lang` method to specify a default prefix:

```Python
# Load the en_US.lang file, set the language to en_US, and add the prefix "text"
i18n.con_load_lang("./i18n/en_US.lang", "en_US", "text")

print(i18n.text.hello)          # Output: Hello
print(i18n.text.world)          # Output: World
print(i18n.text.mode.singleton) # Output: Singleton Mode
```

#### Macro Definitions

You can use `#define` macro definitions to set the language code and `superiors`.
This can override the parameters passed to the `con_load_lang` method.

```lang
; Set the language code to zh_CN
#define locale zh_CN

; Clear the superiors setting
#define superiors
#define superiors .
#define superiors /

hello = 你好
world = 世界

; Set superiors to mode
#define superiors mode

singleton = Singleton Mode

; Set the language code to en_US and en_GB
#define locale en_US en_GB

#define superiors

hello = Hello
world = World
```

### .json File Format Specification

Normally, we consider `.json` to be a single-language file and load it using the `con_load_json` method.

```json
{
    "hello": "你好",
    "world": "世界"
}
```

```Python
i18n.con_load_json("./i18n/zh_CN.json", "zh_CN")
```

If you want `.json` to be a multi-language file, you need to use the con_load_json_i18n method to load it.

```json
{
    "zh_CN": {
        "hello": "你好",
        "world": "世界"
    },
    "en_US": {
        "hello": "Hello",
        "world": "World"
    }
}
```

```Python
i18.con_load_json_i18n("./i18n/xxx.json")
```

### .csv File Format Specification

Usually we treat `.csv` as a multilingual file and load it using `con_load_csv_i18n`.

```csv
locale,key,value
zh_CN,hello,你好
zh_CN,world,世界
en_US,hello,Hello
en_US,world,World
```

```Python
i18n.con_load_csv_i18n("./i18n/xxx.csv")
```


## Load language files

When using the `con_auto_set_best_locale` method you must ensure that the directory structure
is one of the following:

```text
├── i18n
│   ├── en_US
│   │   ├── xxx.lang
│   │   ├── xxx.json
│   │   └── xxx.csv
│   │
│   ├── zh_CN
│   │   ├── xxx.lang
│   │   ├── xxx.json
│   │   └── xxx.csv
│   │
│   └── ru_RU
│       ├── xxx.lang
│       ├── xxx.json
│       └── xxx.csv
```

Note: In the above format, `xxx` will be used as the default prefix when loading `.lang` files.
If you don't want this, you can override it in the file using `#define`.

### Directory Structure Example 2

Alternatively, you can use the following structure:

```
├── i18n
│   ├── en_US.lang
│   ├── zh_CN.lang
│   ├── ru_RU.lang
│   ├── xxx.lang
│   │
│   ├── en_US.json
│   ├── zh_CN.json
│   ├── ru_RU.json
│   ├── xxx.json
│   │
│   ├── xxx.csv
│   └── xxx.csv
```

</div>
</div>
