FROM ubuntu:16.04

MAINTAINER Andreas Dewes

RUN apt-get update
RUN apt-get install -y python3
COPY docker_analyze.py /docker_analyze.py
CMD ["python3","/docker_analyze.py"]
