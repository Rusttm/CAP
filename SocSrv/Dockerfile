# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /CAP/SocSrv

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . /CAP/SocSrv
COPY __init__.py /CAP

CMD ["python3", "SocSrvMain.py"]
