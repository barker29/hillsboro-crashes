"""
Copyright (c) 2023 Andrew T. Barker

This software is distributed under the MIT License, see the LICENSE file
or https://mit-license.org/
"""

import json
import os
import sys


def make_table(db):
    """db is a list of dicts, probably loaded from one or more human .json
    files

    Returns a string containing a markdown table"""
    out = "| date | intersection |\n"
    out += "| --- | --- |\n"
    for crash in db:
        if "fatal" not in crash["severity"]:
            continue
        out += "|"


if __name__ == "__main__":
    db = []
    for fn in glob.glob("*_human.json"):
        print(fn)
        with open(fn, "r") as fd:
            db = db + json.load(fd)
    print(make_table(db))
