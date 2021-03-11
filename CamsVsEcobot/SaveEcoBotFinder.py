import pandas as pd
import os

class SaveEcoBotFinder:
    def __init__(self, dirname: str):
        self._dir = dirname

    
    def getById(self, id: int):
        try:
            path = os.path.join(self._dir, "saveecobot_" + str(id) + ".csv")
            if os.path.exists(path):
                return self.SaveEcoBotWrapper(path)
            else:
                print(path + " doesn't exits")
                return None
        except pd.errors.EmptyDataError:
            return None
 


    class SaveEcoBotWrapper:
        def __init__(self, filename: str):
            self._csv = pd.read_csv(filename)

        def getValue(self, date: str, hour: int, phenomenon = "pm25"):
            # print(" %02d:00:00" % hour)
            table = self._csv[(self._csv["logged_at"] >= date + " %02d:00:00" % hour)
                               & (self._csv["logged_at"] <= date + " %02d:59:59" % hour)
                               & (self._csv["phenomenon"] == phenomenon)]
            # TODO: not sorted by time
            if table.size > 0:
                return table.iloc[0]["value"]
            else:
                return 0
