try:

    import requests
    import pandas as pd
    import numpy as np
    from math import floor
    import datetime
    import time

    print("All modules are loaded ")

except Exception as e:

    print("Some Modules are Missing :{} ".format(e))


class StockReader(object):

    def __init__(self, ticker='AMD', end_date=None):
        self.ticker = ticker
        self.end_date = datetime.datetime.now()

    def get_df(self):

        """return Pandas Dataframe """

        unixtime = round(time.mktime(self.end_date.timetuple()))
        URL = "https://query1.finance.yahoo.com/v7/finance/download/{}?period1=1566569104&period2={}&interval=1d&events=history".format(STOCK,unixtime)
        df = pd.read_csv(URL)
        return df





