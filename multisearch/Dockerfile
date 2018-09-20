FROM python:3

RUN mkdir -p /shared
WORKDIR /shared

ADD ./requirements.txt .
RUN pip install -Ur  requirements.txt

# NOTE before pushing to dockerhub - remove that line
ADD ./api_key .

ADD ./app.py .
