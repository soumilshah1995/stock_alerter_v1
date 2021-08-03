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
        URL = "https://query1.finance.yahoo.com/v7/finance/download/{}?period1=1566569104&period2={}&interval=1d&events=history".format(self.ticker,unixtime)
        df = pd.read_csv(URL)
        return df


class MACD(object):

    def __init__(self, df, slow_ma, fast_ma , smooth):

        self.df = df
        self.slow_ma    = slow_ma
        self.fast_ma    = fast_ma
        self.smooth     = smooth

    def get_macd(self):

        exp1 = self.df.Close.ewm(span=self.slow_ma, adjust=False).mean()
        exp2 =  self.df.Close.ewm(span=self.fast_ma, adjust=False).mean()
        exp2 =  self.df.Close.ewm(span=26, adjust=False).mean()

        self.df["macd"] = exp1-exp2
        self.df["signal"] = self.df.macd.ewm(span=self.smooth, adjust=False).mean()

        self.df["hist"] =self.df["macd"] - self.df["signal"]
        return self.df


def main():

    helper = StockReader(ticker='AMD')
    df = helper.get_df()
    helper_macd = MACD(df=df, slow_ma=12, fast_ma=26, smooth=9)
    df = helper_macd.get_macd()
    print(df.tail())

if __name__ == "__main__":
    main()




