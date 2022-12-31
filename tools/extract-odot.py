"""
Copyright (c) 2022 Andrew T. Barker

This software is distributed under the MIT License, see the LICENSE file
or https://mit-license.org/
"""

"""
Extract data from ODOT shapefiles

The original data comes from the "Safety" section of this webpage:

https://www.oregon.gov/odot/Data/Pages/GIS-Data.aspx

The goal is to extract only the entries from Washington County and
put them in the same .csv form that we use for our hand-entered
data. This script currently assumes a specific hard-coded location for
the ODOT data.

The main dependency is the pyshp library:

https://github.com/GeospatialPython/pyshp
"""
import csv
import os
import sys

import shapefile


tags = ["date",
        "time",
        "street0",
        "street1",
        "location-notes",
        "longitude",
        "lattitude",
        "total-fatality",
        "total-injury",
        "pedestrian-fatality",
        "pedestrian-injury",
        "bicycle-fatality",
        "bicyle-injury",
        "source",
        "links",  # previously two separate fields
        "notes",
        "entry-method"]


def print_record(fields, shapeRec):
    for f in fields:
        print(f[0], ":", shapeRec.record[f[0]])


def print_d_record(shapeRec):
    d = shapeRec.__dict__
    for k in d.keys():
        print(k, ":", d[k])


def get_streets(sr):
    """Given shapeRecord sr, return pair (street0, street1) wherre street0
    is where the crash happened and street1 is the nearest intersection; if
    crash occurs at intersection, ordering may not be entirely clear."""
    success = True
    if sr.record["ST_FULL_NM"] != "":
        street0 = sr.record["ST_FULL_NM"]
    elif sr.record["RTE_NM"] != "":
        street0 = sr.record["RTE_NM"]
    elif sr.record["HWY_MED_NM"] != "":
        street0 = sr.record["HWY_MED_NM"]
    else:
        success = False
    if sr.record["ISECT_ST_F"] != "":
        street1 = sr.record["ISECT_ST_F"]
    elif sr.record["MP_NO"] != "":
        street1 = "MP " + str(sr.record["MP_NO"])
    else:
        success = False
    if success:
        return (street0, street1)
    print("Couldn't get street pair:")
    for k in ["ST_FULL_NM", "RTE_NM", "HWY_MED_NM", "ISECT_ST_F"]:
        print(k, ":", sr.record[k])
    print_d_record(sr)
    raise ValueError


def make_crash_csv(odot_path):
    """Return a pre-csv list of list of strings based on odot data in given
    path"""
    keep_keys = ["CRASH_DT",    # date, ISO
                 "CRASH_HR_N",  # crash hour (floor, 24-hour time)
                 "CRASH_SVRT",  # severity? (2=fatal?
                 "FC_DESC",     # description of street?
                 "HIGHEST_IN",  # highest injury (1=fatal?
                 "HWY_MED_NM",  # highway name?
                 "LAT_DD",
                 "LONG_DD",
                 "ST_FULL_NM",  # name of actual street? (sometimes highway instead?)
                 "ISECT_ST_F",  # name of intersecting street
                 "RD_CHAR_LO",  # some other type of road descriptor
                 "RTE_NM",      # name of route
                 "TOT_FATAL_",  # bunch of TOT_ might be important
                 "TOT_INJ_CN",  # should be total total injury?
                 "TOT_INJ_LV",  # should be total injury level A? (serious)
                 "TOT_INJ__1",  # should be total level B? (moderate)
                 "TOT_INJ__2",  # level C?
                 "TOT_PED_FA",  # ped fatalities
                 "TOT_PEDCYC",  # total cyclists involved?
                 "TOT_PEDC_1",  # total cyclists fatalities?
                 "TOT_PEDC_2",  # total cyclists injuries?
    ]
    filter_field = "CNTY_NM"
    filter_value = "Washington"
    count = 0
    csv_data = []
    # filename = "../../crashes-gis/data" + str(year) + "/crashes" + str(year)
    with shapefile.Reader(odot_path) as sf:
        for rec in sf.iterRecords(fields=[filter_field]):
            if rec[filter_field] == filter_value:
                # load full record and shape
                shapeRec = sf.shapeRecord(rec.oid)
                if int(shapeRec.record["HIGHEST_IN"]) <= 2:
                    street0, street1 = get_streets(shapeRec)
                    lgt = shapeRec.record["LONGTD_DD"]
                    lat = shapeRec.record["LAT_DD"]
                    new_record = [str(shapeRec.record["CRASH_DT"]),
                                  shapeRec.record["CRASH_HR_N"] + ":00",
                                  street0,
                                  street1,
                                  shapeRec.record["RD_CHAR_LO"] + "/" + shapeRec.record["FC_DESC"],
                                  lgt,
                                  lat,
                                  shapeRec.record["TOT_FATAL_"],
                                  shapeRec.record["TOT_INJ_CN"],
                                  shapeRec.record["TOT_PED_FA"],
                                  shapeRec.record["TOT_PED_IN"],
                                  shapeRec.record["TOT_PEDC_1"],
                                  shapeRec.record["TOT_PEDC_2"],
                                  "ODOT",
                                  "",
                                  "",
                                  "extract-odot.py"]
                    # print(new_record)
                    csv_data.append(new_record)
                    count = count + 1
                    # if count > 60:
                    #     break
    return csv_data


def write_crash_csv(odot_path, outfile):
    csv_data = make_crash_csv(odot_path)
    with open(outfile, "w", newline="") as fd:
        writer = csv.writer(fd, lineterminator=os.linesep)
        writer.writerow(tags)
        writer.writerows(csv_data)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        write_crash_csv(sys.argv[1], "odot_crash_data.csv")
