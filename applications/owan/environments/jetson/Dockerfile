FROM nvcr.io/nvidia/l4t-ml:r32.6.1-py3 AS base

ENV DEBIAN_FRONTEND="noninteractive" \
    LC_ALL="C.UTF-8" \
    LANG="C.UTF-8" \
    PYTHONPATH="/home/gatheluck/owan/"

RUN apt update \
    && apt install --no-install-recommends -y \
        build-essential \
        curl \
        git \
        libffi-dev \
        libhdf5-dev \
        libssl-dev \
        make \
        openssh-client \
        ssh \
        python3-dev \
        python3-pip \
    # Following process is need to escape from following:
    # `ERROR: Cannot uninstall 'PyYAML'.
    # It is a distutils installed project and thus 
    # we cannot accurately determine which files belong to 
    # it which would lead to only a partial uninstall.`
    # https://note.com/junk_matsumoto/n/nc4f472ed0d80#orAz3
    && pip3 install pip==8.1.1 \
    && pip3 uninstall -y pyyaml \
    && pip3 install --upgrade pip
RUN pip3 install pyyaml

RUN pip3 install poetry \
    && poetry config virtualenvs.create false \
    && mkdir -p /home/gatheluck/owan/

WORKDIR /home/gatheluck/owan/
COPY Makefile pyproject.toml .flake8 ./
RUN poetry install

COPY src src