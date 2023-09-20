FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt update
RUN apt install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa

RUN apt install -y git zsh
RUN apt install -y python3-pip
RUN apt install -y python3.7 python3.7-distutils python3.7-dev python3.7-venv
RUN apt install -y python3.8 python3.8-distutils python3.8-dev python3.8-venv
RUN apt install -y python3.9 python3.9-distutils python3.9-dev python3.9-venv
RUN apt install -y python3.10 python3.10-distutils python3.10-dev python3.10-venv
RUN apt install -y python3.11 python3.11-distutils python3.11-dev python3.11-venv
