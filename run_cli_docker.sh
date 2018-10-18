#!/bin/bash

docker build -t rimek/allegro-tools .

docker run -v $(pwd):/shared -it rimek/allegro-tools ./run_cli.sh "$@"
