#!/usr/bin/env bash
set -x

scripts/copy_app.sh
scripts/create_production_requirements.sh

use_tag="iancleary/backend-main:$NAME"

DOCKERFILE="$NAME"

if [ "$NAME" == "latest" ] ; then
    DOCKERFILE="python3.10.8-slim"
fi

docker build -t "$use_tag" --file "./docker-images/${DOCKERFILE}.dockerfile" "./docker-images/"
