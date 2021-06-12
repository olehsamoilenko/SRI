import pandas as pd

class CamsWrapper:
    #   !  Only pm2.5  !
    def __init__(self, filename: str):
        self._csv = pd.read_csv(filename)

    def head(self):
        return self._csv.head()

    def uniqueCamsIds(self):
        return self._csv["ID_CAMS'"].unique()

    def uniqueDates(self):
        return self._csv["DATE'"].unique()

    def filter(self, date: str, camsPixelId: int):
        '''
        date format: 2019-01-02
        '''
        table = self._csv[
            (self._csv["DATE'"] == date + "'")
            & (self._csv["ID_CAMS'"] == camsPixelId)
        ]

        if table.size > 0:
            return table.iloc[0][2:26].tolist()
        else:
            return 0

    # def filter(self, date: str, camsPixelId: int, hour: int):
    #     '''
    #     date format: 2019-01-02
    #     '''
    #     table = self._csv[
    #         (self._csv["DATE'"] == date + "'")
    #         & (self._csv["ID_CAMS'"] == camsPixelId)
    #     ]
    #     if table.size > 0:
    #         return table.iloc[0]["%d:00" % hour]
    #     else:
    #         return 0
