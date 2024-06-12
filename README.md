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

### .lang

There is no single fixed format for `.lang` files, so I made up some special syntax myself.

First is the key-value pair format.

```lang
; zh_CN.lang

; This is a comment.
// This is also a comment.

hello = 你好
world = 世界

mode.singleton = 单例模式
```

After preparing the .lang file, load it using `con_load_lang`.

```Python
i18n.con_load_lang("./i18n/zh_CN.lang", "zh_CN")
```

Then get the corresponding translation through the `con_translation` method,
or directly access the property of the same name and let i18n overload it.

```Python
print(i18n.con_translation("hello"))
print(i18n.world)
print(i18n.mode.singleton)
```

You can pass the `superiors` argument to the `con_load_lang` method to specify default prefixes.

```Python
i18n.con_load_lang("./i18n/zh_CN.lang", "zh_CN", "text")

print(i18n.text.hello)
print(i18n.text.world)
print(i18n.text.mode.singleton)
```

Of course you can also define all of this in your `.lang` file using `#define`.

```lang
; Set the locale to zh_CN.
#define locale zh_CN

; Clear superiors settings
#define superiors

hello = 你好
world = 世界

#define superiors mode

singleton = 单例模式

; Set the locale to en_US and en_GB.
#define locale en_US en_GB

#define superiors

hello = Hello
world = World
```

### .json

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

If you want .json to be a multi-language file, you need to use the con_load_json_i18n method to load it.

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

### .csv

Usually we treat csv as a multilingual file and load it using `con_load_csv_i18n`.

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

Note that in the above format, `xxx` will be passed as the default prefix when loading
the `.lang` file. If you don't want this, use `#define` to override it in the file.

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
