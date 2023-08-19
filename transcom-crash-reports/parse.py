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
x
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


def main():
    textfile("20230725_crashes.pdf", "20230725_crashes.txt")


if __name__ == "__main__":
    main()
