FROM ubuntu:18.04

ENV TERM xterm-256color

SHELL ["/bin/bash", "-c"]

RUN apt-get update; apt-get upgrade; apt-get install -y net-tools; apt-get install -y nano; apt-get install -y software-properties-common; add-apt-repository -y ppa:deadsnakes/ppa;  apt-get install -y python3.7; apt-get install -y python3-pip

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.7 1; update-alternatives --config python

RUN mkdir -p nsx-automation/NsxClient_v3

WORKDIR /nsx-automation/NsxClient_v3

COPY . .

RUN pip3 install -r requirements.txt


CMD ["/bin/bash", "-c", "python3 NsxClient_docker.py"]
