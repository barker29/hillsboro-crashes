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


def roads(ax):
    """Stolen from ../tools/make-map.py, see also ../tools/gis-helper.py"""
    colors = ["gray", "orange", "blue", "purple", "black", "red", "orange", "orange", "purple", "black", "blue",
              "green", "cyan", "red", "purple", "green", "blue", "black"]
    with open(os.path.join("..", "metro-data", "roads.json"), "r") as fd:
        road_data = json.load(fd)
    legendset = []
    for r, color in zip(road_data.keys(), colors):
        for item in road_data[r]:
            if "I5" in r or "217" in r or "SUNSET" in r:
                color = (0.0, 0.0, 0.0)
            else:
                color=(0.45, 0.45, 0.45)
            ax.plot(item["x"], item["y"], color=color, linewidth=1.0)
            # if r in legendset:
            #     ax.plot(item["x"], item["y"], color=color)
            # else:
            #     ax.plot(item["x"], item["y"], color=color, label=r)
            #     legendset.append(r)


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
    """db is a list of dicts, probably loaded from one or more human .json files

    TODO: roads, see ../tools/gis-helper and start specializing for Hillsboro"""
    fig = plt.figure(figsize=(8.0, 6.0))
    fig.set_tight_layout(True)
    # backdrop(plt.gca())
    # cities(plt.gca(), labels=True)
    hillsboro_limits(plt.gca())
    roads(plt.gca())
    crashes(plt.gca(), db)
    # plt.legend()
    # TODO: make the bounding box depend on where crashes actually occur?
    #       (ie, don't map emtpy western wasington county)
    plt.xlim(-123.0193707343201, -122.85186472294419)
    plt.ylim(45.47142187468111, 45.58077218413512)    
    plt.axis("off")
    # outfile = os.path.join("..", "docs", "map" + str(year) + ".svg")
    # outfile = os.path.join("..", "docs", "map" + str(year) + ".png")
    # plt.savefig(outfile)
    plt.show()


if __name__ == "__main__":
    db = []
    for fn in ["20221122_human.json",
               "20230124_human.json",
               "20230425_human.json",
               "20230523_human.json",
               "20230725_human.json"]:
        with open(fn, "r") as fd:
            db = db + json.load(fd)
    draw_map(db)
