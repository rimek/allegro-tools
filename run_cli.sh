#!/bin/bash

docker build -t rimek/allegro-tools .

docker run -v $(pwd):/shared -it rimek/allegro-tools python ./cli.py "$@"
