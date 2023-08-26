"""
Copyright (c) 2023 Andrew T. Barker

This software is distributed under the MIT License, see the LICENSE file
or https://mit-license.org/
"""

"""
This documents the workflow and progress we are making.

It should be a checklist or document or something, but I am a nerd
so it is a python script.
"""

import glob
import json
import os


def main():
    for fn in sorted(glob.glob("*_crashes.pdf")):
        datetag = fn[:8]
        print(datetag)
        print("  have .pdf of crash report:", fn)
        rawtext_file = fn.replace(".pdf", ".txt")
        if os.path.exists(rawtext_file):
            print("  have raw text:", rawtext_file)
        else:
            print("  no raw text, try parse.py:textfile")
            continue
        cleantext_file = rawtext_file.replace("crashes", "clean")
        if os.path.exists(cleantext_file):
            print("  have cleaned up text:", cleantext_file)
        else:
            print("  no clean text, clean it up by hand")
            continue
        basicjson = cleantext_file.replace(".txt", ".json")
        try:
            with open(basicjson, "r") as fd:
                jo = json.load(fd)
            entries = len(jo)
            datetimecount = 0
            for entry in jo:
                if "date" in entry.keys() and "time" in entry.keys():
                    datetimecount = datetimecount + 1
            print("  basic .json file:", basicjson, "{0:d} entries, {1:d} have date/time".format(entries, datetimecount))
        except FileNotFoundError:
            print("  no basic .json file, try parse.py:parsetext")
            continue
        humanjson = basicjson.replace("clean", "human")
        try:
            with open(humanjson, "r") as fd:
                jo = json.load(fd)
            # TODO: count coordinates, other tags
            coordcount = 0
            for entry in jo:
                if "latitude" in entry.keys():
                    coordcount = coordcount + 1
            print("  human .json file found, {0:d} entries, {1:d} have coordinates".format(len(jo), coordcount))
        except FileNotFoundError:
            print("  no human .json file, try human.py")
            continue


if __name__ == "__main__":
    main()

        
