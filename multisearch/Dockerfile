FROM python:3

RUN mkdir -p /shared
WORKDIR /shared

ADD ./requirements.txt .
RUN pip install -Ur  requirements.txt

# ADD . /shared
