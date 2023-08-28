"""
Copyright (c) 2023 Andrew T. Barker

This software is distributed under the MIT License, see the LICENSE file
or https://mit-license.org/
"""

import json
from matplotlib import pyplot as plt
import os


def fill_multipoly(ax, x, y, parts, color):
    for i in range(len(parts)-1):
        ax.fill(x[parts[i]:parts[i+1]], y[parts[i]:parts[i+1]], color=color)


def hillsboro_limits(ax):
    """mostly stolen from ../tools/make-map.py"""
    with open(os.path.join("..", "metro-data", "cities.json"), "r") as fd:
        city_limits = json.load(fd)
    color = (0.85, 0.85, 0.85)  # Hillsboro
    city = "Hillsboro"
    fill_multipoly(ax, city_limits[city]["x"], city_limits[city]["y"],
                   city_limits[city]["parts"], color)


def crashes(ax, db):
    x = []
    y = []
    for crash in db:
        if "latitude" in crash.keys() and "longitude" in crash.keys():
            color = (0.0, 0.0, 1.0)
            if "fatal" in crash["severity"]:
                color = (1.0, 0.0, 0.0)
            ax.plot(crash["longitude"], crash["latitude"],
                    "x", color=color, markersize=4)


def draw_map(db):
    """db is a list of dicts, probably loaded from one or more human .json files"""
    plt.figure(figsize=(8.0, 6.0))
    # backdrop(plt.gca())
    # cities(plt.gca(), labels=True)
    hillsboro_limits(plt.gca())
    # roads(plt.gca())
    crashes(plt.gca(), db)
    # plt.legend()
    # TODO: make the bounding box depend on where crashes actually occur?
    #       (ie, don't map emtpy western wasington county)
    # plt.xlim(-123.5, -122.73)
    # plt.ylim(45.31, 45.79)
    plt.axis("off")
    # outfile = os.path.join("..", "docs", "map" + str(year) + ".svg")
    # outfile = os.path.join("..", "docs", "map" + str(year) + ".png")
    # plt.savefig(outfile)
    plt.show()


if __name__ == "__main__":
    with open("20230725_human.json", "r") as fd:
        db = json.load(fd)
    draw_map(db)
