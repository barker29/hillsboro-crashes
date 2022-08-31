"""
Copyright (c) 2022 Andrew T. Barker

This software is distributed under the MIT License, see the LICENSE file
or https://mit-license.org/
"""

"""
Take A CSV file ane output a more readable markdown-style table
"""
import csv
import sys

def get_data_from_csv(filename):
    """Extract data from CSV, return list of lists"""
    out = []
    with open(filename, "r", newline="") as fd:
        reader = csv.reader(fd)
        for k, line in enumerate(reader):
            if k > 1:
                out.append(line)
    return out


def build_markdown_table(csv_data):
    """Return string for human-readable markdown table given CSV data

    Focused on fatalities for now"""
    out = "|date|location|deaths|bike/pedestrian|source|\n"
    out = out + "|---|---|---|---|---|\n"
    for item in csv_data:
        if int(item[7]) > 0:
            location = item[2] + " and " + item[3]
            bikeped = "no"
            if int(item[9]) > 0 or int(item[10]) > 0 or int(item[11]) > 0 or int(item[12]) > 0:
                bikeped = "yes"
            source = "[" + item[13] + "](" + item[14] + ")"
            out = out + "|{0:s}|{1:s}|{2:d}|{3:s}|{4:s}|\n".format(item[0], location, int(item[7]), bikeped, source)
    return out


def main(infile, outfile):
    csv_data = get_data_from_csv(infile)
    md_string = build_markdown_table(csv_data)
    print(md_string)
    # with open(outfile, "w") as fd:
    #     fd.write(md_string)


if __name__ == "__main__":
    # main(sys.argv[1], sys.argv[2])
    main("../collected-data/database-2022.csv", "")
