#!/usr/bin/env bash

set -x

autoflake ./
isort  ./
black ./
