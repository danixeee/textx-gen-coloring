# flake8: noqa
import codecs
import os
from platform import python_version

from setuptools import find_packages, setup

PACKAGE_NAME = "textx-gen-coloring"
VERSION = "0.1.0"
AUTHOR = "Daniel Elero"
AUTHOR_EMAIL = "danixeee@gmail.com"
DESCRIPTION = "a syntax highlight generator for textX languages"
KEYWORDS = "textX DSL python domain specific languages syntax highlighting"
LICENSE = "MIT"
URL = "https://github.com/danixeee/textx-gen-coloring"

packages = find_packages()

print("packages:", packages)

README = codecs.open(
    os.path.join(os.path.dirname(__file__), "README.md"), "r", encoding="utf-8"
).read()

ci_require = ["bandit", "pytest", "pytest-cov", "pytest-azurepipelines"]

dev_require = ["bandit==1.5.1"]

tests_require = ["coverage==4.5.3", "pytest==4.3.1", "pytest-cov==2.6.1"]

if python_version().startswith("3.6"):  # For python 3.6
    ci_require.append("black")
    dev_require.append("black")


setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type="text/markdown",
    url=URL,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    keywords=KEYWORDS,
    license=LICENSE,
    packages=packages,
    include_package_data=True,
    install_requires=["click", "jinja2", "textx"],
    entry_points={
        "textx_generators": ["textmate_gen = textx_gen_coloring:textmate_gen"],
        "textx_languages": ["coloring_lang = textx_gen_coloring:coloring_lang"],
    },
    extras_require={"ci": ci_require, "dev": dev_require, "test": tests_require},
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
