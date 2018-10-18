#!/bin/bash

PORT=9000

docker build -t rimek/allegro-tools .
docker run -v $(pwd):/shared -p $PORT:8000 -it rimek/allegro-tools ./run_webapp.sh "$@"
