import pandas as pd
import os

class SaveEcoBotFinder:
    def __init__(self, dirname: str):
        self._dir = dirname


    class SaveEcoBotWrapper:
        def __init__(self, path: str):
            self._csv = pd.read_csv(path)
            if "logged_at" not in self._csv.columns:
                self._csv = pd.read_csv(path, header=None, names=["device_id", "phenomenon", "value", "logged_at", "value_text"])

        # def getValue(self, date: str, hour: int, phenomenon = "pm25"):
        #     # print(" %02d:00:00" % hour)
        #     table = self._csv[(self._csv["logged_at"] >= date + " %02d:00:00" % hour)
        #                        & (self._csv["logged_at"] <= date + " %02d:59:59" % hour)
        #                        & (self._csv["phenomenon"] == phenomenon)]
        #     # TODO: not sorted by time
        #     if table.size > 0:
        #         return table.iloc[0]["value"]
        #     else:
        #         return 0

        def getValue(self, date: str, phenomenon = "pm25"):
            table = self._csv[(self._csv["logged_at"].str.startswith(date))
                               & (self._csv["phenomenon"] == phenomenon)]
            table = table.drop_duplicates(subset=['logged_at'])
            return table["value"].tolist()

        def getCsv(self) -> pd.DataFrame:
            return self._csv


    def getById(self, id: int) -> SaveEcoBotWrapper:
        try:
            path = os.path.join(self._dir, "saveecobot_" + str(id) + ".csv")
            if os.path.exists(path):
                return self.SaveEcoBotWrapper(path)
            else:
                print(path + " doesn't exits")
                return None
        except pd.errors.EmptyDataError:
            return None
