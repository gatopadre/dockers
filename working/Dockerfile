FROM ubuntu:20.04
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y \
    build-essential \
    python3 \
    python3-dev \
    python3-pip \
    python3-setuptools \
    python3-tk \
    python3-wheel 

RUN pip3 install --upgrade pip

