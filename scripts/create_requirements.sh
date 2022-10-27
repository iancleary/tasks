#!/usr/bin/env bash
set -x

# export requirements.txt file from pdm
pdm export -o docker-images/requirements.txt --without-hashes