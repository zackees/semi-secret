"""
Setup file.
"""

import os
import re

from setuptools import setup

URL = "https://github.com/zackees/semi-secret"
KEYWORDS = "Semi Secret Key Value Storage, provides more security than plain text json file"
HERE = os.path.dirname(os.path.abspath(__file__))



if __name__ == "__main__":
    setup(
        maintainer="Zachary Vorhies",
        keywords=KEYWORDS,
        url=URL,
        package_data={"": ["assets/example.txt"]},
        include_package_data=True,
        extras_require={
            "dev": [
                "black",
                "isort",
                "mypy",
                "pytest",
                "tox",
                "ruff",
                "pytest-xdist",
            ]
        })

