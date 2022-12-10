#!/usr/bin/env bash

set -x

ruff ./
isort  ./
black ./
