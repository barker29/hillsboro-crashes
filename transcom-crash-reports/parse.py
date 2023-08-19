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


def parsetext(text):
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
        entry = {}
        entry["date"] = text[m.start():m.end()]  # TODO: ISO date
        laststart = m.start()
    entry["description"] = text[laststart:]
    out.append(entry)
    for entry in out:
        timepattern = r"\d*:\d*\s*[ap]\.m\."
        m = re.search(timepattern, entry["description"])
        if m:
            entry["time"] = entry["description"][m.start():m.end()]
    print(out)


def main():
    # textfile("20230725_crashes.pdf", "20230725_crashes.txt")
    with open("20230725_clean.txt", "r") as fd:
        text = fd.read()
    parsetext(text)


if __name__ == "__main__":
    main()
