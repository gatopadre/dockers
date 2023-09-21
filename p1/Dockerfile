FROM ubuntu:latest
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y postgresql
RUN apt-get install -y postgresql-contrib
RUN apt-get install -y python3 python3-pip
RUN apt-get install -y python3-setuptools
RUN apt-get install -y python3-tk
RUN apt-get install -y python3-wheel
RUN pip3 install Django
RUN pip3 install psycopg2-binary
RUN mkdir /home/app
WORKDIR /home/app
COPY requirements.txt /home/app
RUN pip3 install -r requirements.txt
COPY /app/ /home/app/
USER postgres
RUN /etc/init.d/postgresql start && \
    psql -U postgres -c "ALTER USER postgres PASSWORD 'postgres';" && \
    python3 manage.py makemigrations && \
    python3 manage.py migrate && \
    /etc/init.d/postgresql stop
USER root

