#!/usr/bin/env bash

set -e
set -x

mypy ./
black ./ --check
isort --force-single-line-imports --trailing-comma --force-grid-wrap=0 --combine-as --line-width 88 --check-only ./