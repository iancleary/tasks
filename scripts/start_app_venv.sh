#!/usr/bin/env bash
set -x

# copy app for docker builds
export HOST=0.0.0.0
export PORT=8080
export DATABASE=data/data.db
python3 app/main.py