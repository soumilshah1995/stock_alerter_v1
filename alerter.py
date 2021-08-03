try:

    import requests
    import pandas as pd
    import numpy as np
    from math import floor
    import datetime
    import time
    import matplotlib.pyplot as plt

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

    def get_macd(self, target_column='Close'):

        exp1 = self.df.Close.ewm(span=self.slow_ma, adjust=False).mean()
        exp2 =  self.df.Close.ewm(span=self.fast_ma, adjust=False).mean()
        exp2 =  self.df.Close.ewm(span=26, adjust=False).mean()

        self.df["macd"] = exp1-exp2
        self.df["signal"] = self.df.macd.ewm(span=self.smooth, adjust=False).mean()

        self.df["hist"] =self.df["macd"] - self.df["signal"]
        self.df = self.df[["Close", "macd", "hist", "signal"]]
        return self.df


class GenerateTradeSignal(object):

    def __init__(self, df):
        self.df = df

    def get_signals(self, prices):

        buy_price = []
        sell_price = []
        macd_signal = []

        signal = 0

        for i in range(len(self.df)):
            if self.df['macd'][i] > self.df['signal'][i]:

                if signal != 1:
                    buy_price.append(prices[i])
                    sell_price.append(np.nan)
                    signal = 1
                    macd_signal.append(signal)

                else:
                    buy_price.append(np.nan)
                    sell_price.append(np.nan)
                    macd_signal.append(0)
            elif self.df['macd'][i] < self.df['signal'][i]:

                if signal != -1:
                    buy_price.append(np.nan)
                    sell_price.append(prices[i])
                    signal = -1
                    macd_signal.append(signal)
                else:
                    buy_price.append(np.nan)
                    sell_price.append(np.nan)
                    macd_signal.append(0)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                macd_signal.append(0)
        return buy_price, sell_price, macd_signal

    def plot(self):

        df = self.df
        buy_price, sell_price, macd_signal = self.get_signals(prices=self.df.Close)

        ax1 = plt.subplot2grid((8,1), (0,0), rowspan = 5, colspan = 1)
        ax2 = plt.subplot2grid((8,1), (5,0), rowspan = 3, colspan = 1)

        ax1.plot(df['Close'], color = 'skyblue', linewidth = 2, label = 'AMD')

        ax1.plot(df.index, buy_price, marker = '^', color = 'green', markersize = 10, label = 'BUY SIGNAL', linewidth = 0)
        ax1.plot(df.index, sell_price, marker = 'v', color = 'r', markersize = 10, label = 'SELL SIGNAL', linewidth = 0)
        ax1.legend()

        ax1.set_title('AMD MACD SIGNALS')
        ax2.plot(df['macd'], color = 'grey', linewidth = 1.5, label = 'MACD')
        ax2.plot(df['signal'], color = 'skyblue', linewidth = 1.5, label = 'SIGNAL')

        for i in range(len(df)):
            if str(df['hist'][i])[0] == '-':
                ax2.bar(df.index[i], df['hist'][i], color = '#ef5350')
            else:
                ax2.bar(df.index[i], df['hist'][i], color = '#26a69a')

        plt.legend(loc = 'lower right')
        plt.show()


def main():

    """get the dataset """
    helper = StockReader(ticker='AMD')
    df = helper.get_df()

    """Get the MACD calculations """
    helper_macd = MACD(df=df, slow_ma=12, fast_ma=26, smooth=9)
    df = helper_macd.get_macd(target_column='Close')

    """get trade signals """
    helper = GenerateTradeSignal(df=df)
    helper.plot()

if __name__ == "__main__":
    main()




