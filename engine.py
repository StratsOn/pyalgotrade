#coding=utf-8

from pyalgotrade import strategy
from pyalgotrade import plotter
from pyalgotrade.tools import yahoofinance
from pyalgotrade.stratanalyzer import sharpe
from pyalgotrade.talibext import indicator

from kafka.client import KafkaClient
from kafka.producer import SimpleProducer

import sys,os

def algoparser(**kwargs):
    """
    编译用户代码
    :param args:
    :param kwargs:
              sid: 资产ID
              start: 策略开始时间
              end: 策略结束时间
              code: 用户策略代码（字符串）
              filename: 用户策略文件名(.py)
    :return:
    """
    sid = kwargs.pop('sid', None)
    start = kwargs.pop('start', None)
    end = kwargs.pop('end', None)
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
    print stat
    return stat



if __name__ == '__main__':
    if not os.environ.has_key('DOCKER_HOST'):
        os.environ['DOCKER_HOST'] = "172.17.42.1"
    print "%s:9092" % os.environ['DOCKER_HOST'].strip('\n')
    client = KafkaClient("%s:9092" % os.environ['DOCKER_HOST'].strip('\n'))
    producer = SimpleProducer(client, async=False, req_acks=SimpleProducer.ACK_AFTER_LOCAL_WRITE, ack_timeout=2000)

    #向脚本传入参数
    start = int(sys.argv[1])
    end = int(sys.argv[2])
    code = sys.argv[3]
    sid = sys.argv[4]

    args = {'start': start, 'end':end, 'code':code, "sid":sid}

    Stat = algoparser(**args)

    producer.send_message("plot", Stat)





