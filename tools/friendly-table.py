"""
Copyright (c) 2022 Andrew T. Barker

This software is distributed under the MIT License, see the LICENSE file
or https://mit-license.org/
"""

"""
Take A CSV file ane output a more readable markdown-style table
"""
import csv
import datetime
import os
import sys

def get_data_from_csv(filename):
    """Extract data from CSV, return list of lists

    TODO: sort the dates, because they don't come that way in ODOT data"""
    out = []
    with open(filename, "r", newline="") as fd:
        reader = csv.reader(fd)
        for k, line in enumerate(reader):
            if k > 0:
                out.append(line)
    return out


def build_markdown_table(csv_data):
    """Return string for human-readable markdown table given CSV data

    Focused on fatalities for now"""
    out = "|date|location|deaths|bike/pedestrian|source|\n"
    out = out + "|---|---|---|---|---|\n"
    fatality_count = 0
    for item in csv_data:
        if int(item[7]) > 0:
            fatality_count = fatality_count + int(item[7])
            location = item[2] + " and " + item[3]
            bikeped = "no"
            if int(item[9]) > 0 or int(item[10]) > 0 or int(item[11]) > 0 or int(item[12]) > 0:
                bikeped = "yes"
            source = "[" + item[13] + "](" + item[14] + ")"
            out = out + "|{0:s}|{1:s}|{2:d}|{3:s}|{4:s}|\n".format(item[0], location, int(item[7]), bikeped, source)
    print("Total fatalities:", fatality_count)
    return out


def old_main(infile, outfile):
    """Load CSV from infile, produce markdown table in outfile."""
    csv_data = get_data_from_csv(infile)
    md_string = build_markdown_table(csv_data)
    md_string = md_string + "\n*Table generated on " + str(datetime.date.today()) + "*\n"
    if outfile is None:
        print(md_string)
    else:
        with open(outfile, "w") as fd:
            fd.write(md_string)


def deploy(infile):
    """Given CSV in infile, produce markdown table and deploy to github pages."""
    tag = "|date|location|"
    mdfile = os.path.join("..", "docs", "index.markdown")
    with open(mdfile, "r") as fd:
        text = fd.read()
    point = text.find(tag)
    csv_data = get_data_from_csv(infile)
    table_string = build_markdown_table(csv_data)
    table_string = table_string + "\n*Table generated on " + str(datetime.date.today()) + "*\n"
    with open(mdfile, "w") as fd:
        fd.write(text[:point])
        fd.write(table_string)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        deploy("../collected-data/database-2022.csv")
    elif len(sys.argv) == 2:
        old_main(sys.argv[1], None)
    else:
        old_main(sys.argv[1], sys.argv[2])
