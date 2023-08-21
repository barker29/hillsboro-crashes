"""
Copyright (c) 2023 Andrew T. Barker

This software is distributed under the MIT License, see the LICENSE file
or https://mit-license.org/
"""

"""
Try to scrape crash information from the crash reports
to the Hillsboro Transporation Commission
"""
import glob
import json
import re

from pypdf import PdfReader


def standard_date(d):
    """input is string in month/day/year form, output
    is ISO YYYY-MM-DD format (still string, no python datetime)"""
    p = d.strip().split("/")
    out = p[2] + "-" + p[0].zfill(2) + "-" + p[1].zfill(2)
    return out


def standard_time(t):
    """input is time like 4:23 p.m., output is 16:23 (both strings)"""
    p = t.strip().split(":")
    if "p.m." in t:
        hour = str(int(p[0]) + 12).zfill(2)
    else:
        hour = p[0].zfill(2)
    out = hour + ":" + p[1][:2]
    return out


def scrape(filename):
    text = ""
    reader = PdfReader(filename)
    for page in reader.pages:
        text = text + page.extract_text()
    return text


def textfile(infile, outfile):
    text = scrape(infile)
    with open(outfile, "w") as fd:
        fd.write(text)


def parsetext(text, source=""):
    """Input is a string, output is a list of dicts, one
    for each crash"""
    out = []
    # split text by dates
    pattern = r"\d*/\d*/\d*"  # TODO: allow some whitespace? multiline?
    laststart = None
    for m in re.finditer(pattern, text):
        # print(m)
        # print(text[m.start():m.end()])
        if laststart is not None:
            entry["description"] = text[laststart:m.start()]
            out.append(entry)
        entry = {"source": source}
        entry["date"] = standard_date(text[m.start():m.end()])
        laststart = m.start()
    entry["description"] = text[laststart:]
    out.append(entry)
    for entry in out:
        timepattern = r"\d*:\d*\s*[ap]\.m\."
        m = re.search(timepattern, entry["description"])
        if m:
            entry["time"] = standard_time(entry["description"][m.start():m.end()])
    return out


def main():
    # textfile("20230725_crashes.pdf", "20230725_crashes.txt")
    filename = "20230725_clean.txt"
    with open(filename, "r") as fd:
        text = fd.read()
    jo = parsetext(text, filename)
    # print(jo)
    with open(filename.replace(".txt", ".json"), "w") as fd:
        json.dump(jo, fd)


if __name__ == "__main__":
    main()
