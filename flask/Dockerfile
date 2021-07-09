FROM ubuntu
FROM python:2.7

#RUN apt-get update && apt-get install --assume-yes --fix-missing python-pip git
#RUN apt-get update && apt-get install -y \python-pip
#FROM ubuntu:16.04
#RUN apt-get update && apt-get install -y --no-install-recommends \python2.7 \python2-pip 
WORKDIR /app
COPY . /app/
ENV PATH="/app/docker:${PATH}"

RUN chmod +x ./docker/*

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD ["/app/docker/entry-point.sh", "database:9042", "uwsgi", "app.ini"]
