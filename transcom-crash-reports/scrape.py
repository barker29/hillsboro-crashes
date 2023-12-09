"""
Copyright (c) 2023 Andrew T. Barker

This software is distributed under the MIT License, see the LICENSE file
or https://mit-license.org/
"""

"""
Try to scrape crash information from the crash reports
to the Hillsboro Transporation Committee
"""
from pypdf import PdfReader
import sys

def scrape(filename):
    text = ""
    reader = PdfReader(filename)
    for page in reader.pages:
        text = text + page.extract_text()
    return text


def textfile(infile, outfile):
    """Given .pdf infile, scrape the text and save it in
    outfile."""
    text = scrape(infile)
    with open(outfile, "w") as fd:
        fd.write(text)


if __name__ == "__main__":
    filename = "20230926_crashes.pdf"
    if len(sys.argv) > 1:
        filename = sys.argv[1] + "_crashes.pdf"
    textfile(filename, filename.replace(".pdf", ".txt"))

