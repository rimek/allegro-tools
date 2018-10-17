#!/bin/bash

PORT=9000

docker build -t rimek/allegro-tools .

docker run -v $(pwd):/shared -p $PORT:9000 -it rimek/allegro-tools python webapp.py "$@"
