# Licensed under the LGPL 3.0 License.
# i18nco by numlinka.
# setup

# site
from setuptools import setup


setup(
    name = "i18nco",
    version = "1.2.0",
    description = "This is a simple and easy to use Python i18n library.",
    long_description = open("README_PyPI.md", "r", encoding="utf-8").read(),
    long_description_content_type = "text/markdown",
    author = "numlinka",
    author_email = "numlinka@163.com",
    url = "https://github.com/numlinka/pyi18nco",
    packages = ["src/i18nco"],
    classifiers=[
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Programming Language :: Python :: 3",
    ],
    license = "LGPLv3",
    keywords = ["sample", "i18n"],
    install_requires = []
)
