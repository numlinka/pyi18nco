# Licensed under the LGPL 3.0 License.
# i18nco by numlinka.

# self
from .i18nabstract import AbstractI18n


class I18nString (str):
    __visit = ...
    __prefix = ...

    def con_set_attribute(self, visit: AbstractI18n, prefix: str = ""):
        self.__visit = visit
        self.__prefix = prefix

    def sformat(self, *args, **kwargs) -> str:
        result = self
        for indexed, value in enumerate(args):
            result = result.replace("{" + f"{indexed}" + "}", f"{value}")

        for key, value in kwargs.items():
            result = result.replace("{" + f"{key}" + "}", f"{value}")

        return result

    def __getattr__(self, __name: str):
        target = __name if self.__prefix == "" else f"{self.__prefix}.{__name}"
        return self.__visit.con_translation(target)


__all__ = ["I18nString"]
