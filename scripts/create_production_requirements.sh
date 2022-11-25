#!/usr/bin/env bash
set -x

# export requirements.txt file from pdm (without dev group)
pdm export -o docker-images/requirements.txt --without-hashes --production
