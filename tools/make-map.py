"""
Copyright (c) 2022 Andrew T. Barker

This software is distributed under the MIT License, see the LICENSE file
or https://mit-license.org/
"""

"""
Make some kind of map of crash data

washington county box (-123.49, 45.32) -- (-122.74, 45.78)
"""
import csv
import json
import os
from matplotlib import pyplot as plt


def fill_multipoly(ax, x, y, parts, color):
    for i in range(len(parts)-1):
        ax.fill(x[parts[i]:parts[i+1]], y[parts[i]:parts[i+1]], color=color)


def bounding_box_center(xin, yin):
    """x, y are lists"""
    xmin = min(xin)
    xmax = max(xin)
    ymin = min(yin)
    ymax = max(yin)
    return ((xmin + xmax) / 2.0,
            (ymin + ymax) / 2.0)


def backdrop(ax):
    with open(os.path.join("..", "metro-data", "washingtoncounty.json"), "r") as fd:
        county_lines = json.load(fd)
    ax.plot(county_lines["x"], county_lines["y"], color=(0, 0, 0), linewidth=1)


def cities(ax, labels=False):
    with open(os.path.join("..", "metro-data", "cities.json"), "r") as fd:
        city_limits = json.load(fd)
    colors = [(0.75, 0.75, 0.75),  # Beaverton
              (0.85, 0.85, 0.85),  # Tigard
              (0.85, 0.85, 0.85),  # Sherwood
              (0.75, 0.75, 0.75),  # Tualatin
              (0.85, 0.85, 0.85),  # Hillsboro
              (0.85, 0.85, 0.85),  # Forest Grove
              (0.75, 0.75, 0.75)]  # Cornelius
    label_locations = {
        "Beaverton": (-122.86062015234434 + 0.01, 45.483815269804246 + 0.02),
        "Tigard": (-122.85023740562367 + 0.05, 45.42484253056987),
        "Sherwood": (-122.89022150727112 + 0.02, 45.35875341023894),
        "Tualatin": (-122.81981138823438 + 0.01, 45.37481363681584),
        "Hillsboro": (-122.98561772863214 + 0.01, 45.52609702940812 - 0.01),
        "Forest Grove": (-123.16198929409559, 45.52346343765585),
        "Cornelius": (-123.09643363439488 + 0.02, 45.516987071388954 - 0.01)
    }
    for city, color in zip(city_limits.keys(), colors):
        fill_multipoly(ax, city_limits[city]["x"], city_limits[city]["y"],
                       city_limits[city]["parts"], color)
        if labels:
            x, y = bounding_box_center(city_limits[city]["x"], city_limits[city]["y"])
            # ax.text(min(city_limits[city]["x"]), y, city.upper(), color=(0.25, 0.25, 0.25), fontsize=5)
            labelx, labely = label_locations[city]
            # print(city, labelx, labely)
            ax.text(labelx, labely, city.upper(), color=(0.35, 0.35, 0.35), fontsize=5)


def roads(ax):
    # TODO: colors, presentation, labels?
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


def crashes(ax, year, color):
    """Plot fatalities from given year in given color"""
    x = []
    y = []
    if year >= 2022:
        filename = os.path.join("..", "collected-data", "database-" + str(year) + ".csv")
    else:
        filename = os.path.join("..", "odot-data", "odot_crash_data_" + str(year) + ".csv")
    with open(filename, "r", newline="") as fd:
        reader = csv.reader(fd)
        for k, line in enumerate(reader):
            if k > 0:
                # if int(line[7]) > 0:
                #     print(k, line[7], "fatalities", line[5], line[6])
                if int(line[7]) > 0 and line[5] != "":
                    x.append(float(line[5]))
                    y.append(float(line[6]))
    ax.plot(x, y, "x", color=color, markersize=4)


def main(year=2022):
    """An .svg is undeniably prettier but makes an enormous file, probably
    should do an ugly .png"""
    plt.figure(figsize=(8.0, 6.0))
    backdrop(plt.gca())
    cities(plt.gca(), labels=True)
    roads(plt.gca())
    crashes(plt.gca(), year, (1.0, 0.0, 0.0))
    # plt.legend()
    # TODO: make the bounding box depend on where crashes actually occur?
    #       (ie, don't map emtpy western wasington county)
    plt.xlim(-123.5, -122.73)
    plt.ylim(45.31, 45.79)
    plt.axis("off")
    # outfile = os.path.join("..", "docs", "map" + str(year) + ".svg")
    outfile = os.path.join("..", "docs", "map" + str(year) + ".png")
    plt.savefig(outfile)


if __name__ == "__main__":
    main()
