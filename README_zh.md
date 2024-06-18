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

[English](README.md) | 简体中文


<div align="left" style="max-width: 1000px;">

## 介绍

这是一个简单的和易于使用的 Python i18n 库。
它是从 [simplepylibs](https://github.com/numlinka/simplepylibs) 中独立出来的一部分。


## 安装

推荐使用 pip 安装 i18nco 。

```bash
pip install i18nco
```

要将 i18nco 升级到最新版本，请使用以下命令：

```shell
pip install --upgrade i18nco
```


## 使用

以下是一个简单的使用示例：

```Python
import i18nco

i18n = i18nco.Internationalization()
i18n.con_auto_load("./i18n")
i18n.con_auto_set_best_locale()

print(i18n.con_translation("hello"))
print(i18n.hello)
```

在 `Internationalization` 中，所有的方法都是以 `con_` (control) 开头的。
当你访问其它属性时均会被重载到 `con_translation` 方法。

`con_auto_load` 方法会加载目录下的语言文件，文件夹层级不能超过 2 层。

`con_auto_set_best_locale` 方法会基于系统语言自动选择最佳的语言。


## 语言文件

我尝试过让 `pyi18nco` 支持更多的语言文件格式，但它们的契合度仍然有限。

### .lang 文件格式说明

由于 .lang 文件没有固定的格式，我们制定了一些特殊的语法规则。

#### 键值对格式

```lang
; zh_CN.lang

; 这是一条注释
// 这也是一条注释

hello = 你好
world = 世界

mode.singleton = 单例模式

; 注释不能出现在语句后面
mode.singleton = 单例模式 ; 这不是一个注释

; 如果你希望保留首尾的空格，请使用 "" 符号包裹字符串
separation " | "

; 多行文本
robert = 我已成为死神 \
         世界的毁灭者
```

#### 加载语言文件

在准备好 .lang 文件之后，使用 `con_load_lang` 加载它：

```Python
# 加载 zh_CN.lang 文件并设置语言为 zh_CN
i18n.con_load_lang("./i18n/zh_CN.lang", "zh_CN")

print(i18n.con_translation("hello"))  # 输出：你好
print(i18n.world)                     # 输出：世界
print(i18n.mode.singleton)            # 输出：单例模式
```

注意：如果你没有传递 `locale` 参数，`pyi18nco` 会自动检测当前系统的语言。

可以为 `con_load_lang` 方法传递参数 `superiors` 来指定默认的前缀：

```Python
# 加载 zh_CN.lang 文件，设置语言为 zh_CN，并添加前缀 "text"
i18n.con_load_lang("./i18n/zh_CN.lang", "zh_CN", "text")

print(i18n.text.hello)          # 输出：你好
print(i18n.text.world)          # 输出：世界
print(i18n.text.mode.singleton) # 输出：单例模式
```

#### 宏定义

你可以使用 `#define` 宏定义来设置语言代码和 `superiors` ，它可以覆盖 `con_load_lang` 方法传递的参数。

```lang
; 设置语言代码为 zh_CN
#define locale zh_CN

; 清除 superiors 设置
#define superiors
#define superiors .
#define superiors /

hello = 你好
world = 世界

; 设置 superiors 为 mode
#define superiors mode

singleton = 单例模式

; 设置语言代码为 en_US 和 en_GB
#define locale en_US en_GB

#define superiors

hello = Hello
world = World
```

### .json 文件格式说明

通常，我们把 `.json` 视为单语言文件，使用 `con_load_json` 方法来加载它。

```json
{
    "hello": "你好",
    "world": "世界"
}
```

```Python
i18n.con_load_json("./i18n/zh_CN.json", "zh_CN")
```

如果你希望 `.json` 是多语言文件，则需要使用 `con_load_json_i18n` 方法来加载它。

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

### .csv 文件格式说明

通常，我们把 `.csv` 视为多语言文件，使用 `con_load_csv_i18n` 方法来加载它。

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


## 加载语言文件

在使用 `con_auto_set_best_locale` 方法时，你必须确保目录结构为以下之一：

### 目录结构示例 1

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

注意：在上述格式中，`xxx` 将被作为 `.lang` 文件加载时的默认前缀。
如果你不希望这样，可以在文件中使用 `#define` 来覆盖它。

### 目录结构示例 2

或者，你可以使用以下结构：

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


## 文档

懒


## 协议

该项目使用 LGPL-3.0 许可证。

</div>
</div>
