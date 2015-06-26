#A Container for QuantStudio applications
FROM ubuntu:14.04
MAINTAINER bleedtodry@hotmail.com

COPY sources.list /etc/apt/
RUN apt-get update 
RUN apt-get install -y build-essential curl python-pip python-dev python-numpy python-pandas

RUN pip install kafka-python

#ta-lib
COPY ./ta-lib-0.4.0-src.tar.gz /
RUN cd /;tar xf ta-lib-0.4.0-src.tar.gz; cd ta-lib; ./configure; make && make install && ldconfig

RUN pip install ta-lib

RUN apt-get install -y python-demjson

ADD . /data/engine

