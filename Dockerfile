FROM ubuntu:14.04

RUN apt-get update &&\
    apt-get install -qy python3 &&\
    apt-get install -qy python3-pip
ADD . /usr/src/app/
WORKDIR /usr/src/app
RUN pip3 install -r requirements.txt
RUN python3 setup.py install
EXPOSE 8000
