#coding=utf-8

from pyalgotrade import strategy
from pyalgotrade import plotter
from pyalgotrade.tools import yahoofinance
from pyalgotrade.stratanalyzer import sharpe
from pyalgotrade.talibext import indicator


def algoparser(**kwargs):
    """
    编译用户代码
    :param args:
    :param kwargs:
              uid：用户ID
              sid: 资产ID
              start: 策略开始时间
              end: 策略结束时间
              capital: 用户初始资金
              code: 用户策略代码（字符串）
              filename: 用户策略文件名(.py)
    :return:
    """
    uid = kwargs.pop('uid', None)
    sid = kwargs.pop('sid', None)
    start = kwargs.pop('start', None)
    end = kwargs.pop('end', None)
    capital = kwargs.pop('end', None)
    code = kwargs.pop('code',None)

    Algo = compile(code, '<string>', 'exec')
    exec Algo

    instrument = sid
    feed = yahoofinance.build_feed([instrument], start, end, ".")

    strat = Strategy(feed, instrument)

    sharpeRatioAnalyzer = sharpe.SharpeRatio()
    strat.attachAnalyzer(sharpeRatioAnalyzer)

    plt = plotter.StrategyPlotter(strat,True,False,False)
    strat.run()
    plt.plot()




if __name__ == '__main__':
    algo = """
class Strategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__instrument = instrument
        self.__sma = None

    def onBars(self, bars):
        closeDs = self.getFeed()[self.__instrument].getCloseDataSeries()
        self.__sma = indicator.SMA(closeDs, 100)

    def getSMA(self):
        ret = None
        if self.__sma is not None:
            ret = self.__sma[-1]
        return ret
"""
    algoparser(start=2011, end=2012, code=algo, sid="yhoo")





