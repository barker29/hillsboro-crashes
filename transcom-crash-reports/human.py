"""
Copyright (c) 2023 Andrew T. Barker

This software is distributed under the MIT License, see the LICENSE file
or https://mit-license.org/
"""

"""
Use human to read description in database and add fields

street0
street1
in-intersection
severity
"""

import json
import readline


def human(fin, fout):
    out = []
    with open(fin, "r") as fd:
        jo = json.load(fd)
    for item in jo:
        print(item["description"])
        for key in ["street0", "street1", "in_intersection", "severity"]:
            item[key] = input(key + "> ")
        out.append(item)
    with open(fout, "w") as fd:
        json.dump(out, fd)


if __name__ == "__main__":
    human("20230725_clean.json", "20230725_human.json")

        

