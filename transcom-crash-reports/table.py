"""
Copyright (c) 2023 Andrew T. Barker

This software is distributed under the MIT License, see the LICENSE file
or https://mit-license.org/
"""
import glob
import json
import os
import sys

links = {
    "20230523": "https://hillsboro-oregon.civicweb.net/document/58545/TC%20Crash%20Report%20Memo%205.23.23.pdf",
    "20230725": "https://hillsboro-oregon.civicweb.net/document/60479/TC%20Crash%20Report%20Memo%207.25.23.pdf",
    "20230926": "https://hillsboro-oregon.civicweb.net/document/90968/TC%20Crash%20Report%20Memo%209.26.23.pdf",
    "20231024": "https://hillsboro-oregon.civicweb.net/document/164356/TC%20Crash%20Report%20Memo%2010.24.23.pdf",
    "20231128": "https://hillsboro-oregon.civicweb.net/document/230977/TC%20Crash%20Report%20Memo%2011.28.23.pdf"
}

def make_table(db):
    """db is a list of dicts, probably loaded from one or more human .json
    files

    Returns a string containing a markdown table"""
    out = "| date | intersection | type | report |\n"
    out += "| --- | --- | --- | --- |\n"
    for crash in db:
        if "fatal" not in crash["severity"]:
            continue
        out += "| "
        out += crash["date"] + " | "
        out += crash["street0"] + " and " + crash["street1"] + " | "
        if "pedestrian" in crash["description"].lower():
            out += "pedestrian"
        elif ("bicycle" in crash["description"].lower() or
              "cyclist" in crash["description"].lower()):
            out += "bicycle"
        out += " | "
        reportdate = crash["source"][:8]
        try:
            out += "[link](" + links[reportdate] + ")"
        except KeyError:
            pass
        out += " |\n"
    return out


if __name__ == "__main__":
    db = []
    for fn in sorted(glob.glob("*_human.json")):
        print(fn)
        with open(fn, "r") as fd:
            db = db + json.load(fd)
    print(make_table(db))
