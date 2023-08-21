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

control: ODOT, county, city
classification: arterial, collector, ...
fault? cause? type?
"""

import json
import readline


def prefill_input(prompt, prefill=""):
    """Fails silently in emacs shell"""
    readline.set_startup_hook(lambda: readline.insert_text(prefill))
    try:
        return input(prompt)
    finally:
        readline.set_startup_hook()


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
        # for key in ["street0", "street1", "in_intersection", "severity"]:
        #     item[key] = input(key + "> ")
        street0, street1 = guess_streets(item["description"])
        item["street0"] = prefill_input("street0> ", street0)
        item["street1"] = prefill_input("street1> ", street1)
        item["in_intersection"] = prefill_input("in_intersection> ", "yes")
        item["severity"] = input("severity> ")
        out.append(item)
    with open(fout, "w") as fd:
        json.dump(out, fd)


def test_streets(fin):
    with open(fin, "r") as fd:
        jo = json.load(fd)
    for item in jo:
        print(guess_streets(item["description"]))


if __name__ == "__main__":
    # human("20230725_clean.json", "20230725_human.json")
    # test_streets("20230725_clean.json")
    human("20230523_clean.json", "20230523_human.json")    


