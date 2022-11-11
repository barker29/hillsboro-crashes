"""
Copyright (c) 2022 Andrew T. Barker

This software is distributed under the MIT License, see the LICENSE file
or https://mit-license.org/
"""

"""
Take some shapefiles etc. from Metro data files and extract it into
a more usable form.

This depends on the following libraries:
 - pyproj (https://pyproj4.github.io/pyproj/stable/)
 - pyshp (https://github.com/GeospatialPython/pyshp)
"""
import json
import pyproj
import shapefile


def county_limits(filename):
    """This is already lat/long"""
    with shapefile.Reader("metro-data-path/County_Lines_(poly)") as sf:
        for sr in sf.shapeRecords():
            if sr.record["COUNTY"] == "Washington":
                x, y = zip(*sr.shape.points)
    outputstruct = {"x": x,
                    "y": y}
    with open(filename, "w") as fd:
        json.dump(outputstruct, fd)


def get_coords_transformer():
    """Some metro data is in NAD83, this transforms to wgs84"""
    nad83oregonnorth = pyproj.CRS.from_proj4('+proj=lcc +lat_1=44.33333333333334 +lat_2=46 +lat_0=43.66666666666666 +lon_0=-120.5 +x_0=2500000 +y_0=0 +datum=NAD83 +units=us-ft +no_defs')
    wgs84 = pyproj.CRS.from_proj4('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')
    # lgt, lat = pyproj.transform(nad83oregonnorth, wgs84, x, y)
    transformer = pyproj.Transformer.from_crs(nad83oregonnorth, wgs84)
    return transformer


def city_limits(cityname):
    """returns dict {x: [], y: [], parts: []} where parts is the partition vector"""
    transformer = get_coords_transformer()
    with shapefile.Reader("metro-data-path/cty_fill") as shp:
        shapes = shp.shapes()
        records = shp.records()
        for idx in range(len(records)):
            if cityname == records[idx][1]:
                nad83_x, nad83_y = zip(*shapes[idx].points)
                x, y = transformer.transform(nad83_x, nad83_y)
                return {"x": x, "y": y, "parts": list(shapes[idx].parts)}


def all_city_limits(outfilename):
    cities = ["Beaverton",
              "Tigard",
              "Sherwood",
              "Tualatin",
              "Hillsboro",
              "Forest Grove",
              "Cornelius"]
    out = {}
    for city in cities:
        d = city_limits(city)
        out[city] = d
    with open(outfilename, "w") as fd:
        json.dump(out, fd, indent=4)


def roadlist():
    """Just to understand"""
    roadset = set()
    filename = "metro-data-path/maj_art"
    with shapefile.Reader(filename) as sf:
        for sr in sf.shapeRecords():
            ftype = sr.record["FTYPE"].strip()
            roadpair = (sr.record["STREETNAME"].strip(), ftype)
            if ftype != "RAMP":
                roadset.add(roadpair)
    for rp in sorted(list(roadset)):
        print(rp)


def washco_fence(xin, yin):
    # plt.xlim(-123.5, -122.73)
    # plt.ylim(45.31, 45.79)
    xout = []
    yout = []
    for x, y in zip(xin, yin):
        if x > -123.5 and x < -122.73 and y > 45.31 and y < 45.79:
            xout.append(x)
            yout.append(y)
    return xout, yout


def roads(outfilename):
    badroads = [("TUALATIN VALLEY HWY",""),  # bad
                ('SR-14', 'HWY'),
                ('BARNES', 'RD')]
    mayberoads = [("MURRAY", "BLVD"),
                  ('OAK', 'ST'),
                  ("GLENCOE", "RD"),]
    roads = [("CORNELIUS PASS", "RD"),
             ("CORNELL", "RD"),
             ("SUNSET", "HWY"),
             ("TUALATIN VALLEY", "HWY"),  # good
             ("HWY 217", ""),
             ("BASELINE", "RD"),
             ('BASELINE', 'ST'),
             ('PACIFIC', 'AVE'),
             ("FARMINGTON", "RD"),
             ("RIVER", "RD"),
             ("I5", "FWY"),
             ('BEAVERTON HILLSDALE', 'HWY'),
             ('10TH', 'AVE'),
             ('SCHOLLS FERRY', 'RD')]
    filename = "metro-data-path/maj_art"
    transformer = get_coords_transformer()
    out = {}
    with shapefile.Reader(filename) as sf:
        for sr in sf.shapeRecords():
            k = (sr.record["STREETNAME"], sr.record["FTYPE"])
            if k in roads:
                key = k[0] + " " + k[1]  # why isn't the key just k?
                nad83x, nad83y = zip(*sr.shape.points)
                allx, ally = transformer.transform(nad83x, nad83y)
                x, y = washco_fence(allx, ally)
                if len(x) == 0:
                    continue
                if key in out.keys():
                    out[key].append({"x": x, "y": y})
                else:
                    out[key] = [{"x": x, "y": y}]
    with open(outfilename, "w") as fd:
        json.dump(out, fd, indent=4)


if __name__ == "__main__":
    # county_limits("washingtoncounty.json")
    # all_city_limits("cities.json")
    roads("roads.json")
    # roadlist()
