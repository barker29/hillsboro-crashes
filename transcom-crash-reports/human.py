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

TODO: most of this so far could be automated

things I want:

coordinates
control: ODOT, county, city
classification: arterial, collector, ...
fault? cause? type?
"""

import json
import readline
import sys


def prefill_input(prompt, prefill=""):
    """Fails silently in emacs shell"""
    readline.set_startup_hook(lambda: readline.insert_text(prefill))
    try:
        return input(prompt)
    finally:
        readline.set_startup_hook()


def interpret_coordinates(s):
    """Input s is human-entered lat-long pair as string, maybe with order reversed.
    Returns (latitude, longitude) pair of floats."""
    sp = s.split(",")
    try:
        a = float(sp[0].strip())
        b = float(sp[1].strip())
    except ValueError:
        return (0.0, 0.0)
    washco_xmin = -123.5
    washco_xmax = -122.73
    washco_ymin = 45.31
    washco_ymax = 45.79
    if washco_xmin < a and a < washco_xmax and washco_ymin < b and b < washco_ymax:
        return (b, a)
    if washco_xmin < b and b < washco_xmax and washco_ymin < a and a < washco_ymax:
        return (a, b)


def guess_streets(d):
    """input d is a crash report, like the 'description' field.
    Returns pair (street0, street1), intent is not to fail but to
    return something even if wrong"""
    t0 = "intersection of"
    a = d.find(t0) + len(t0)
    b = d.find(" and ", a)
    c = d.find(".", b)
    if a == -1 or b == -1 or c == -1:
        return ("", "")
    return (d[a:b].strip(), d[b+5:c].strip())


def human(fin, fout):
    out = []
    with open(fin, "r") as fd:
        jo = json.load(fd)
    for item in jo:
        print(item["description"])
        street0, street1 = guess_streets(item["description"])
        if "street0" not in item.keys():
            item["street0"] = prefill_input("street0> ", street0)
        if "street1" not in item.keys():
            item["street1"] = prefill_input("street1> ", street1)
        if "in_intersection" not in item.keys():
            item["in_intersection"] = prefill_input("in_intersection> ", "yes")
        if "severity" not in item.keys():
            item["severity"] = input("severity> ")
        out.append(item)
    with open(fout, "w") as fd:
        json.dump(out, fd, sort_keys=True, indent=4)


def test_streets(fin):
    with open(fin, "r") as fd:
        jo = json.load(fd)
    for item in jo:
        print(guess_streets(item["description"]))


def test_coords():
    for k in range(3):
        s = input("coords> ")
        print(interpret_coordinates(s))


if __name__ == "__main__":
    # human("20230725_clean.json", "20230725_human.json")
    # test_streets("20230725_clean.json")
    # human("20230523_clean.json", "20230523_human.json")
    # test_coords()
    if len(sys.argv) > 1:
        human(sys.argv[1], sys.argv[1].replace("clean", "human"))
