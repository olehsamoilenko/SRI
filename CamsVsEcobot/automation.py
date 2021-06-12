import datetime
import folium
import importlib
import pandas as pd
import statistics

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
MATCHER = IdMatcher("співставлення ID постів з ID Cams.csv",
                    bannedStations=[3504, 2762, 1415, 2809, 1544,
    4230, 3498, 3497, 13055, 13028, 13026, 13020, 12992, 12991, 12989, 12982, 12978, 12958, 12957, 12954, 12952, 12951, 12910, 12911, 12912, 12914, 12917, 12918, 12920, 12921, 12923, 12924, 12925, 12926, 12927, 12928, 12929, 12930, 12931, 12932, 12933, 12934, 12935, 12936, 12937, 12938, 12939, 12940, 12941, 12944, 12945, 12946, 12947, 12948, 12909, 12907, 12905])
FINDER = SaveEcoBotFinder(dirname="/media/osamoile/data/Ecobot_16_11_2020")
CAMS = CamsWrapper("Cams_2019_2020_pm2.5_Kyiv.csv")
DATES = [
    #"2020-03-27",
    # "2020-03-28", "2020-03-29", "2020-03-30",
    # "2020-03-31", "2020-04-01", "2020-04-02",
    #"2020-04-03", "2020-04-04",
    #"2020-04-05", "2020-04-06", "2020-04-07", "2020-04-08", "2020-04-09",
    "2020-04-10", "2020-04-11", "2020-04-12", "2020-04-13", "2020-04-14",
    "2020-04-15", "2020-04-16", "2020-04-17", "2020-04-18", "2020-04-19",
    "2020-04-20", "2020-04-21", "2020-04-22", "2020-04-23", "2020-04-24",
    "2020-04-25", "2020-04-26", "2020-04-27", "2020-04-28", "2020-04-29",
    "2020-04-30", "2020-05-01", "2020-05-02", "2020-05-03", "2020-05-04",
    "2020-05-05", "2020-05-06", "2020-05-07", "2020-05-08", "2020-05-09",
    "2020-05-10", "2020-05-11", "2020-05-12", "2020-05-13", "2020-05-14",
    "2020-05-15", "2020-05-16", "2020-05-17", "2020-05-18", "2020-05-19",
    "2020-05-20", "2020-05-21", "2020-05-22", "2020-05-23", "2020-05-24",
    "2020-05-25", "2020-05-26", "2020-05-27", "2020-05-28", "2020-05-29", "2020-05-30", "2020-05-31",
    "2020-06-01", "2020-06-02", "2020-06-03", "2020-06-04",
    "2020-06-05", "2020-06-06", "2020-06-07", "2020-06-08", "2020-06-09",
    "2020-06-10", "2020-06-11", "2020-06-12", "2020-06-13", "2020-06-14",
    "2020-06-15", "2020-06-16", "2020-06-17", "2020-06-18", "2020-06-19",
    "2020-06-20", "2020-06-21", "2020-06-22", "2020-06-23", "2020-06-24",
    "2020-06-25", "2020-06-26", "2020-06-27", "2020-06-28", "2020-06-29", "2020-06-30",
    "2020-07-01", "2020-07-02", "2020-07-03", "2020-07-04",
    "2020-07-05", "2020-07-06", "2020-07-07", "2020-07-08", "2020-07-09",
    "2020-07-10", "2020-07-11", "2020-07-12", "2020-07-13", "2020-07-14",
    "2020-07-15", "2020-07-16", "2020-07-17", "2020-07-18", "2020-07-19",
    "2020-07-20", "2020-07-21", "2020-07-22", "2020-07-23", "2020-07-24",
    "2020-07-25", "2020-07-26", "2020-07-27", "2020-07-28", "2020-07-29", "2020-07-30", "2020-07-31"
]
# ATTENTION: host-specific values

def process_date(date, lst):
    for id in lst:
        land = 0
        post = FINDER.getById(id)
        if post:
            land_values = post.getValue(date)
            try:
                land = statistics.median(land_values)
            except statistics.StatisticsError:
                land = 0
            df = pd.DataFrame({"date": [date], "id": [id], "land": [land], "len": [len(land_values)]})
            print(df)
            df.to_csv("back-up.csv", mode='a', header=False, index=False)
        else:
            print("post 0")
        print(str(id) + " done.")


# post = FINDER.getById(3401)
# values = post.getValue("2020-04-03")
# print(len(values))

lst = []

for camsId in CAMS.uniqueCamsIds():
    lst += MATCHER.byCamsId(camsId)
print(lst)

start_date = datetime.date(2020, 2, 8)
end_date = datetime.date(2021, 10, 1)
delta = datetime.timedelta(days=1)

while start_date <= end_date:
    str_date = start_date.strftime("%Y-%m-%d")
    process_date(str_date, lst)
    start_date += delta
    print(str_date + " done!")

# process_date("2020-04-03", lst)
