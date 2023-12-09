"""
Copyright (c) 2023 Andrew T. Barker

This software is distributed under the MIT License, see the LICENSE file
or https://mit-license.org/
"""

"""
The interactive stuff is pretty weak, not sure it is worth improvling.
One option is not using the native matplotlib stuff and using an actual
GUI framework, like Tk, see:

https://matplotlib.org/stable/gallery/user_interfaces/embedding_in_tk_sgskip.html
"""

import glob
import json
import math
from matplotlib import pyplot as plt
import os
import sys

def fill_multipoly(ax, x, y, parts, color):
    for i in range(len(parts)-1):
        ax.fill(x[parts[i]:parts[i+1]], y[parts[i]:parts[i+1]], color=color)


def hillsboro_limits(ax, color=(0.8, 0.8, 0.8)):
    """mostly stolen from ../tools/make-map.py"""
    with open(os.path.join("..", "metro-data", "cities.json"), "r") as fd:
        city_limits = json.load(fd)
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
    used_labels = []
    for crash in db:
        if "latitude" in crash.keys() and "longitude" in crash.keys():
            color = (0.0, 0.0, 1.0)
            symbol = "."
            severity = ""
            victim = "vehicle"
            if "serious" in crash["severity"]:
                color = (1.0, 1.0, 0.0)
                severity = "serious"
            if "fatal" in crash["severity"]:
                color = (1.0, 0.0, 0.0)
                severity = "fatal"
            if ("pedestrian" in crash["description"].lower() or
                "bicycl" in crash["description"].lower()):
                symbol = "x"
                victim = "pedestrian"
            nextlabel = severity + " " + victim
            if nextlabel in used_labels:
                ax.plot(crash["longitude"], crash["latitude"],
                        symbol, color=color, markersize=4)
            else:
                used_labels.append(nextlabel)
                ax.plot(crash["longitude"], crash["latitude"],
                        symbol, color=color, markersize=4, label=nextlabel)


class ClickHandler:
    def __init__(self, db, annot, fig):
        self.db = db
        self.annot = annot
        self.fig = fig

    def __call__(self, event):
        x = event.xdata
        y = event.ydata
        print("x", x, "y", y)
        closest = 200.0
        for crash in db:
            if "latitude" in crash.keys() and "longitude" in crash.keys():
                cx = crash["longitude"]
                cy = crash["latitude"]
                dist = math.sqrt((cx-x)*(cx-x) + (cy-y)*(cy-y))
                if dist < closest:
                    closest = dist
                    ccrash = crash
        cx = ccrash["longitude"]
        cy = ccrash["latitude"]
        print("  cx", cx, "cy", cy, "closest", closest)
        if closest < 0.005:
            print("    " + ccrash["date"] + ": " + ccrash["severity"] + ": " + ccrash["description"][0:200])
            self.annot.set(x=cx, y=cy, text=ccrash["date"])
            self.annot.set_visible(True)
        else:
            self.annot.set_visible(False)
        self.fig.canvas.draw_idle()


def draw_map(db, interactive=False):
    """db is a list of dicts, probably loaded from one or more human
    .json files"""
    fig = plt.figure(figsize=(7.5, 6.0))
    fig.set_tight_layout(True)
    # backdrop(plt.gca())
    # cities(plt.gca(), labels=True)
    hillsboro_limits(plt.gca())
    roads(plt.gca())
    crashes(plt.gca(), db)
    # plt.legend()
    # TODO: make the bounding box depend on where crashes actually occur?
    plt.xlim(-123.0193707343201, -122.85186472294419)
    plt.ylim(45.47142187468111, 45.58077218413512)    
    plt.axis("off")
    # outfile = os.path.join("..", "docs", "map" + str(year) + ".svg")
    # outfile = os.path.join("..", "docs", "map" + str(year) + ".png")
    # plt.savefig(outfile)
    plt.legend()
    if interactive:
        annot = plt.gca().annotate("", xy=(-123.0, 45.5))
        ch = ClickHandler(db, annot, fig)
        plt.connect('button_press_event', ch)
        plt.show()
    else:
        plt.savefig("hillsboro_crashes.png")


if __name__ == "__main__":
    db = []
    for fn in glob.glob("*_human.json"):
        with open(fn, "r") as fd:
            db = db + json.load(fd)
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        draw_map(db, interactive=True)
    else:
        draw_map(db)
