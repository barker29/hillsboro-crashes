"""
Copyright (c) 2023 Andrew T. Barker

This software is distributed under the MIT License, see the LICENSE file
or https://mit-license.org/
"""
import datetime
import glob
import json
import os
import sys

# TODO: maybe put links in a separate .json file or something

links = {
    "20220628": "https://hillsboro-oregon.civicweb.net/document/45643/TC%20Crash%20Report%20Memo.pdf",
    "20220726": "https://hillsboro-oregon.civicweb.net/document/46501/TC%20Crash%20Report%20Memo%207.21.pdf",
    "20220927": "https://hillsboro-oregon.civicweb.net/document/49677/TC%20Crash%20Report%20Memo%209.12.22.pdf",
    "20221025": "https://hillsboro-oregon.civicweb.net/document/50837/TC%20Crash%20Report%20Memo%2010.15.22.pdf",
    "20221122": "https://hillsboro-oregon.civicweb.net/document/51927/TC%20Crash%20Report%20Memo%2011.9.22.pdf",
    "20230124": "https://hillsboro-oregon.civicweb.net/document/54139/TC%20Crash%20Report%20Memo%201.19.23.pdf",
    "20230425": "https://hillsboro-oregon.civicweb.net/document/57390/TC%20Crash%20Report%20Memo%204.25.23.pdf",
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
    out = "| Date | Intersection | Type | Report |\n"
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


def load_data():
    """Loads data from all human.json file, returns list of dicts"""
    db = []
    for fn in sorted(glob.glob("*_human.json")):
        # print(fn)
        with open(fn, "r") as fd:
            db = db + json.load(fd)
    return db        


def deploy(db, outmd=None):
    """Given crash data in db, produce markdown table and deploy to github
    pages."""
    begin_tag = "| Date | Intersection | Type | Report |"
    end_tag = "## This site's past life"
    if outmd is None:
        mdfile = os.path.join("..", "docs", "index.markdown")
    else:
        mdfile = outmd
    with open(mdfile, "r") as fd:
        text = fd.read()
    begin_point = text.find(begin_tag)
    end_point = text.find(end_tag)
    print("begin, end", begin_point, end_point)
    table_string = make_table(db)
    table_string = table_string + "\n*Table generated on " + str(datetime.date.today()) + "*\n\n"
    with open(mdfile, "w") as fd:
        fd.write(text[:begin_point])
        fd.write(table_string)
        fd.write(text[end_point:])


if __name__ == "__main__":
    db = load_data()
    # print(make_table(db))
    deploy(db)
