#!/bin/bash

source .env
export ALLEGRO_API_KEY

python webapp.py "$@"
