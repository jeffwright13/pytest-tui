#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup, find_packages


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding="utf-8").read()


setup(
    name="pytest-tui",
    version="1.0.1",
    author="Jeff Wright",
    author_email="jeff.washcloth@gmail.com",
    license="MIT",
    url="https://github.com/jeffwright13/pytest-tui",
    description="Text User Interface (TUI) for Pytest, automatically launched after your test run is finished",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    py_modules=["pytest_tui"],
    python_requires=">=3.8",
    install_requires=[
        "ansi2html>=1.8.0",
        "Faker>=13.15.0",
        "pytest>=6.2.5",
        "pyTermTk>=0.10.8a0",
        "single-source>=0.3.0",
        "strip-ansi>=0.1.1",
        "textual>=0.1.18",
    ],
    classifiers=[
        "Framework :: Pytest",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    keywords="pytest pytest-plugin testing tui html pytermtk textual html",
    entry_points={
        "pytest11": ["pytest_tui = pytest_tui.plugin"],
        "console_scripts": [
            "tui1 = pytest_tui.tui1:main",
            "tui2 = pytest_tui.tui2:main",
            "tuihtml = pytest_tui.html:main",
        ],
    },
)
