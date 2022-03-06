#Download base image ubuntu 20.04
FROM ubuntu:20.04

#Version information
LABEL maintainer="pedro.macias.gordaliza@gmail.com"
LABEL version="0.1"
LABEL description="RD coding test"

# Update Ubuntu Software repository
RUN apt update
# Python 3.8 for from the Ubuntu 20.4 official repository
RUN apt-get install -y python3 python3-pip 

#Copy the module
COPY . /opt/RD_coding_test
WORKDIR /opt/RD_coding_test

#Intall the required libraries
RUN pip install -r requirements.txt

WORKDIR /opt/RD_coding_test/src

