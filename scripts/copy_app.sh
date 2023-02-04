#!/usr/bin/env bash
set -x

cp -r app docker-images
cp -r alembic docker-images
cp alembic.ini docker-images/