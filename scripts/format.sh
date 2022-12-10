#!/usr/bin/env bash

set -x

ruff --fix ./
black ./
