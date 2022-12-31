"""
Copyright (c) 2022 Andrew T. Barker

This software is distributed under the MIT License, see the LICENSE file
or https://mit-license.org/
"""

"""
This script is intended to do some very basic sanity checking of csv
files that may be hand-entered.
"""
import csv
import datetime
import os
import sys

EXPECTED_ENTRIES=17

tags = ["date",  # 0
        "time",
        "street0",
        "street1",  # 3
        "location-notes",
        "longitude",
        "lattitude",
        "total-fatality",  # 7
        "total-injury",
        "pedestrian-fatality",  # 9
        "pedestrian-injury",
        "bicycle-fatality",  # 11
        "bicyle-injury",
        "source",
        "links", # 14, previously two fields
        "notes",
        "entry-method"]

washco_xmin = -123.5
washco_xmax = -122.73
washco_ymin = 45.31
washco_ymax = 45.79


def check_url(url):
    if "://" not in url:
        return False
    if "http" not in url:
        return False
    return True


def validate(filename):
    """TODO:
    
    - better URL checking
    - arithmetic on the total fatality [done in friendly-table.py] / injury numbers
    - constants or keys or something for the literal numbers
    - maybe a list of URLs instead of only 2
    """
    with open(filename, "r", newline="") as fd:
        print("Checking ", filename)
        count = 0
        missing_coords = 0
        reader = csv.reader(fd)
        for j, p in enumerate(reader):
            # p = line.split(",")
            if len(p) != EXPECTED_ENTRIES:
                print("  line {0:d} does not have correct number of entries (found {1:d}, expected {2:d}).".format(j+1, len(p), EXPECTED_ENTRIES))
            if j == 0:
                for t1, t2 in zip(p, tags):
                    if t1.strip() != t2:
                        print("  header line does not match expected header:", t1, t2)
                        break
                continue
            try:
                d = datetime.date.fromisoformat(p[0])
            except ValueError:
                print("  line {0:d} item {1:d} is not a valid date.".format(j+1, 0))
            try:
                d = datetime.time.fromisoformat(p[1])
            except ValueError:
                print("  line {0:d} item {1:d} is not a valid time.".format(j+1, 1))
            for k in [5, 6]:
                if p[k] == "":
                    continue
                try:
                    num = float(p[k])
                except ValueError:
                    print("  line {0:d} item {1:d} (longitude/latitude) is not a number.".format(j+1, k))
            for k in [7, 8, 9, 10, 11, 12]:
                try:
                    n = int(p[k])
                except ValueError:
                    print("  line {0:d} item {1:d} (fatality/injury count) is not a number.".format(j+1, k))
            if int(p[7]) < int(p[9]) + int(p[11]):
                print("  line {0:d} total fatalities do not add up.".format(j+1))
            if int(p[8]) < int(p[10]) + int(p[12]):
                print("  line {0:d} total injuries do not add up.".format(j+1))
            count = count + 1
            if p[5] == "" or p[6] == "":
                missing_coords = missing_coords + 1
                if int(p[7]) > 0:
                    print("  line {0:d} with fatal crash is missing coordinates.".format(j+1))
            elif (float(p[5]) < washco_xmin or float(p[5]) > washco_xmax or
                  float(p[6]) < washco_ymin or float(p[6]) > washco_ymax):
                print("  line {0:d} lat/long is outside Washington County".format(j+1))
            if p[13] != "ODOT":
                urls = p[14].split(",")
                if len(urls) == 0:
                    print("  line {0:d} item {1:d}: non-ODOT data requires valid URL.".format(j+1, 14))
                for url in urls:
                    if not check_url(url):
                        print("  line {0:d} item {1:d}: non-ODOT data requires valid URL.".format(j+1, 14))
    print("Checked {0:d} entries, {1:d} are missing latitude/longitude info.".format(count, missing_coords))


if __name__ == "__main__":
    if len(sys.argv) == 1:
        validate(os.path.join("..", "collected-data", "database-2022.csv"))
    else:
        validate(sys.argv[1])
