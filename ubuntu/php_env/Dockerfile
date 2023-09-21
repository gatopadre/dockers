# base image
FROM ubuntu:18.04

# update packages and install php
RUN apt-get update -y && apt-get install -y php7.2

# copy php files
COPY . /app