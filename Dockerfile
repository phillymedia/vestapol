FROM python:3.9 as build


WORKDIR /vestapol

COPY requirements_dev.txt ./

COPY ./Makefile ./Makefile
COPY ./README.md ./README.md
COPY ./setup.py ./setup.py


RUN pip install -r ./requirement_dev.txt
RUN python setup.py install
