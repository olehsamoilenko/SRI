import pandas as pd

class IdMatcher:
    def __init__(self, filename):
        self._csv = pd.read_csv(filename)

    def byCamsId(self, id: int):
        table = self._csv[self._csv["ID CAMS"] == id]
        column = table["ID посту"]
        return column.tolist()

    @staticmethod
    def _toFloat(x) -> float:
        return float(x.replace(',', '.'))

    def getCoordinates(self, saveEcoBotId: int):
        table = self._csv[self._csv["ID посту"] == saveEcoBotId]
        return [self._toFloat(table.iloc[0]["x"]), self._toFloat(table.iloc[0]["y"])]
