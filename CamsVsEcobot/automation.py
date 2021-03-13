import folium
import importlib
import pandas as pd

import SaveEcoBotFinder
import IdMatcher
import CamsWrapper

importlib.reload(SaveEcoBotFinder)
importlib.reload(IdMatcher)
importlib.reload(CamsWrapper)

from SaveEcoBotFinder import SaveEcoBotFinder
from IdMatcher import IdMatcher
from CamsWrapper import CamsWrapper

# ATTENTION: host-specific values
MATCHER = IdMatcher("співставлення ID постів з ID Cams.csv", bannedStations=[3504, 2762])
FINDER = SaveEcoBotFinder(dirname="/media/osamoile/data/Ecobot_16_11_2020")
CAMS = CamsWrapper("Cams_2019_2020_pm2.5_Kyiv.csv")
DATES = [
    "2020-03-27", "2020-03-28", "2020-03-29", "2020-03-30",
    "2020-03-31", "2020-04-01", "2020-04-02", "2020-04-03", "2020-04-04",
    "2020-04-05", "2020-04-06", "2020-04-07", "2020-04-08", "2020-04-09",
    "2020-04-10", "2020-04-11", "2020-04-12", "2020-04-13", "2020-04-14",
    "2020-04-15", "2020-04-16", "2020-04-17", "2020-04-18", "2020-04-19",
    "2020-04-20", "2020-04-21", "2020-04-22", "2020-04-23", "2020-04-24",
    "2020-04-25", "2020-04-26", "2020-04-27", "2020-04-28", "2020-04-29",
    "2020-04-30", "2020-05-01", "2020-05-02", "2020-05-03", "2020-05-04",
    "2020-05-05", "2020-05-06", "2020-05-07", "2020-05-08", "2020-05-09",
    "2020-05-10", "2020-05-11", "2020-05-12", "2020-05-13", "2020-05-14",
    "2020-05-15", "2020-05-16", "2020-05-17", "2020-05-18", "2020-05-19",
    "2020-05-20", "2020-05-21", "2020-05-22", "2020-05-23", "2020-05-24",
    "2020-05-25",
]
# ATTENTION: host-specific values

def get_list_of_lists(date):
    lst = []
    for i in range(0, 24):
        lst.append([])

    # lst[x] - values for x:00

    for id in MATCHER.byCamsId(6564):
        post = FINDER.getById(id)
        if post:
            for i in range(0, 24):
                value = post.getValue(date, i)
                lst[i].append(value)
        print(str(id) + " done.")

    return lst

def get_averages(list_of_lists):
    averages = []
    for i in range(0, 24):
        tmp = [x for x in list_of_lists[i] if x != 0]
        avg = sum(tmp) / len(tmp)
        averages.append(avg)
    return averages

def get_lens(list_of_lists):
    lens = []
    for i in range(0, 24):
        tmp = [x for x in list_of_lists[i] if x != 0]
        lens.append(len(tmp))
    return lens


def process_date(date):
# date = "2020-03-25"
    cams = []
    dates = []
    hours = []
    for i in range(0, 24):
        cams.append(CAMS.filter(date, 6564, i))
        dates.append(date)
        hours.append(i)

    land_all = get_list_of_lists(date)
    land = get_averages(land_all)
    lens = get_lens(land_all)

    df = pd.DataFrame({"date": dates, "hour": hours, "cams": cams, "land": land, "len": lens})
    # print(df)
    df.to_csv("back-up.csv", mode='a', header=False)


for date in DATES:
    process_date(date)
    print(date + " done!")
