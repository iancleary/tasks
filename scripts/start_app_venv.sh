#!/usr/bin/env bash
set -x

# copy app for docker builds
export HOST=0.0.0.0
export PORT=8080
export DATABASE=data/dev.db
# assuming the script is called from `make run`
# it will be run from ../ such that main.py
# relatively is app.main
# which ensures the import statements are consistent
# between make run and docker(-compose)
python3 -m app.main
