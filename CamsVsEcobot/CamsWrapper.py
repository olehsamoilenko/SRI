import pandas as pd

class CamsWrapper:
    #   !  Only pm2.5  !
    def __init__(self, filename: str):
        self._csv = pd.read_csv(filename)

    def head(self):
        return self._csv.head()

    def uniqueCamsIds(self):
        return self._csv["ID_CAMS'"].unique()

    def filterByDate(self, date: str):
        '''
        date format: 2019-01-02
        '''
        return self._csv[self._csv["DATE'"] == date + "'"]
