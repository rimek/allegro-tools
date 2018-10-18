FROM python:3

RUN mkdir -p /shared
WORKDIR /shared

ADD . /shared
RUN pip install -Ur  requirements.txt

CMD python webapp.py
