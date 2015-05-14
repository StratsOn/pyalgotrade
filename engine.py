#coding=utf-8

from pyalgotrade import strategy
from pyalgotrade import plotter
from pyalgotrade.tools import yahoofinance
from pyalgotrade.stratanalyzer import sharpe
from pyalgotrade.talibext import indicator

from kafka.client import KafkaClient
from kafka.producer import SimpleProducer

import sys

#向脚本传入参数
start = int(sys.argv[1])
end = int(sys.argv[2])
code = sys.argv[3]
sid = sys.argv[4]



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
    stat = plt.plotjson()
    return stat



if __name__ == '__main__':
    client = KafkaClient("localhost:9092")
    producer = SimpleProducer(client)

    # Stat = algoparser(start=2011, end=2012, code=algo, sid="yhoo")
    # print type(Stat)

    #读取储存在txt文件的算法
    with open(code, 'r') as f:
        code = f.read()

    args = {'start': start, 'end':end, 'code':code, "sid":sid}

    Stat = algoparser(**args)

    producer.send_message("plot", Stat)





