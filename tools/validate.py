"""
Copyright (c) 2022 Andrew T. Barker

This software is distributed under the MIT License, see the LICENSE file
or https://mit-license.org/
"""

"""
This script is intended to do some very basic sanity checking of csv
files that may be hand-entered.
"""
import datetime
import os
import sys

EXPECTED_ENTRIES=18

tags = ["date",
        "time",
        "street0",
        "street1",
        "location-notes",
        "longitude",
        "lattitude",
        "total-fatality",
        "total-injury",
        "pedestrian-fatality",
        "pedestrian-injury",
        "bicycle-fatality",
        "bicyle-injury",
        "source",
        "link0",
        "link1",
        "notes",
        "entry-method"]


def check_url(url):
    if "://" not in url:
        return False
    if "http" not in url:
        return False
    return True


def validate(filename):
    """TODO:
    
    - check if latitude/longitude is in a box that contains Washington County
    - better URL checking
    - arithmetic on the total fatality / injury numbers
    - constants or keys or something for the literal numbers
    """
    with open(filename, "r") as fd:
        count = 0
        missing_coords = 0
        for j,line in enumerate(fd):
            p = line.split(",")
            if len(p) != EXPECTED_ENTRIES:
                print("  line {0:d} does not have correct number of entries (fond {1:d}, expected {2:d}).".format(j+1, len(p), EXPECTED_ENTRIES))
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
            count = count + 1
            if p[5] == "" or p[6] == "":
                missing_coords = missing_coords + 1
            if p[13] != "ODOT":
                if not check_url(p[14]):
                    print("line {0:d} item {1:d}: non-ODOT data requires valid URL.".format(j+1, 14))
    print("Checked {0:d} entries, {1:d} are missing latitude/longitude info.".format(count, missing_coords))


if __name__ == "__main__":
    if len(sys.argv) == 1:
        validate(os.path.join("..", "collected-data", "database-2022.csv"))
    else:
        validate(sys.argv[1])
