FROM nvidia/cuda:11.0-devel-ubuntu20.04 AS base

ENV DEBIAN_FRONTEND="noninteractive" \
    LC_ALL="C.UTF-8" \
    LANG="C.UTF-8" \
    PYTHONPATH="/home/gatheluck/owan/" 

# Following is needed to install python 3.6 or 3.9
RUN apt update && apt install --no-install-recommends -y software-properties-common 
RUN add-apt-repository ppa:deadsnakes/ppa

RUN apt update && apt install --no-install-recommends -y \
    build-essential \
    curl \
    git \
    make \
    openssh-client \
    python3.6 \
    python3-dev \
    python3-pip \
    python-is-python3 \
    ssh

# Following is needed to swtich default python3 version
# For detail, please check following link
# https://unix.stackexchange.com/questions/410579/change-the-python3-default-version-in-ubuntu
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1 \
    && update-alternatives --set python3 /usr/bin/python3.6 \
    && pip3 install poetry

RUN mkdir -p /home/gatheluck/owan/
WORKDIR /home/gatheluck/owan/