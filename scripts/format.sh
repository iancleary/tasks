#!/usr/bin/env bash

set -x

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place ./ --exclude=__init__.py
isort --force-single-line-imports --trailing-comma --force-grid-wrap=0 --combine-as --line-width 88  ./
black ./