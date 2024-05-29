"""
Copyright (c) 2024 Andrew T. Barker

This software is distributed under the MIT License, see the LICENSE file
or https://mit-license.org/
"""

"""
Try to produce a geojson file for geojson.io, which has useful help.

I made a gist and it works fine:

http://geojson.io/#id=gist:barker29/828fe2edc3f9a6454dae4af97f0e0332

In the geojson.io help there are other possibilities (like pointing to a file in a repo instead of a gist)
"""
import glob
import json
import os


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
    "20231128": "https://hillsboro-oregon.civicweb.net/document/230977/TC%20Crash%20Report%20Memo%2011.28.23.pdf",
    "20240123": "https://hillsboro-oregon.civicweb.net/document/232854/TC%20Crash%20Report%20Memo%201.23.24.pdf",
    "20240227": "https://hillsboro-oregon.civicweb.net/document/233521/TC%20Crash%20Report%20Memo%202.9.24.pdf",
    "20240326": "https://hillsboro-oregon.civicweb.net/document/234638/TC%20Crash%20Report%20Memo%203.20.24.pdf",
    "20240423": "https://hillsboro-oregon.civicweb.net/document/235693/TC%20Crash%20Report%20Memo%204.18.24.pdf",
    "20240528": "https://hillsboro-oregon.civicweb.net/document/236844/TC%20Crash%20Report%20Memo%205.22.24.pdf",
}


def load_data(path):
    """Loads data from all human.json file, returns list of dicts"""
    db = []
    for fn in sorted(glob.glob(os.path.join(path, "*_human.json"))):
        # print(fn)
        with open(fn, "r") as fd:
            db = db + json.load(fd)
    return db


def make_pt(lat, lon, date, report):
    newpt =  {
        "type": "Feature",
        "properties": {
            "date": date,
            "report": report
        },
        "geometry": {
            "coordinates": [
                lon,
                lat
            ],
            "type": "Point"
        }
    }
    return newpt


def make_geojson(db):
    out = {
        "type": "FeatureCollection",
        "features": [
            ]
    }
    for crash in db:
        if "fatal" not in crash["severity"]:
            continue
        report = links[crash["source"][:8]]
        out["features"].append(make_pt(crash["latitude"],
                                       crash["longitude"],
                                       crash["date"],
                                       report))
    return out


def main():
    db = load_data("../transcom-crash-reports")
    gj = make_geojson(db)
    with open("try.json", "w") as fd:
        json.dump(gj, fd, indent=4)


if __name__ == "__main__":
    main()

