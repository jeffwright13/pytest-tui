#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import os

from setuptools import find_packages, setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding="utf-8").read()


setup(
    name="pytest-tui",
    version="1.4.1",
    author="Jeff Wright",
    author_email="jeff.washcloth@gmail.com",
    license="MIT",
    url="https://github.com/jeffwright13/pytest-tui",
    description="Text User Interface (TUI) for Pytest, with optional auto-launch and HTML export",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    py_modules=["pytest_tui"],
    python_requires=">=3.8",
    install_requires=[
        "ansi2html>=1.8.0",
        "blessed>=1.19.1",
        "bullet>=2.2.0",
        "click>=8.1.3",
        "Faker>=13.15.0",
        "iniconfig>=1.1.1",
        "json2table>=1.1.5",
        "pytest-metadata>=2.0.2",
        "pytest>=6.2.5",
        "single-source>=0.3.0",
        "strip-ansi>=0.1.1",
        "textual>=0.1.18",
    ],
    setup_requires=['setuptools_scm'],
    include_package_data=True,
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
            "tuiconf = pytest_tui.__main__:tui_config",
            "tui = pytest_tui.__main__:tui_run",
            "tuih = pytest_tui.html1:main",
        ],
    },
)
