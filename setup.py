# Licensed under the MIT License.
# i18nco Copyright (C) 2022 numlinka.
# setup

# site
from setuptools import setup


setup(
    name = "i18nco",
    version = "1.4.0",
    description = "This is a simple and easy to use Python i18n library.",
    long_description = open("README_PyPI.md", "r", encoding="utf-8").read(),
    long_description_content_type = "text/markdown",
    author = "numlinka",
    author_email = "numlinka@163.com",
    url = "https://github.com/numlinka/pyi18nco",
    package_dir={"": "src"},
    packages = ["i18nco"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    license = "LGPLv3",
    keywords = ["sample", "i18n"],
    install_requires = []
)
