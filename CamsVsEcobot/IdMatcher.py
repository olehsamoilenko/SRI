import pandas as pd

class IdMatcher:
    def __init__(self, filename, bannedStations: list = []):
        self._csv = pd.read_csv(filename)
        self._banned = bannedStations

    def byCamsId(self, id: int):
        table = self._csv[self._csv["ID CAMS"] == id]
        column = table["ID посту"]
        res = column.tolist()
        for i in self._banned:
            try:
                res.remove(i)
            except ValueError:
                pass # ok, I don't care
        return res

    def getAllSupportedPostIds(self) -> list:
        return self._csv["ID посту"].tolist()

    def getAllSupportedCamsIds(self) -> list:
        return self._csv["ID CAMS"].unique().tolist()

    def getCamsIdByPostId(self, postId: int):
        res = self._csv[self._csv["ID посту"] == postId]
        return int(res.iloc[0]["ID CAMS"])

    @staticmethod
    def _toFloat(x) -> float:
        return float(x.replace(',', '.'))

    def getCoordinates(self, saveEcoBotId: int):
        table = self._csv[self._csv["ID посту"] == saveEcoBotId]
        return [self._toFloat(table.iloc[0]["x"]), self._toFloat(table.iloc[0]["y"])]
