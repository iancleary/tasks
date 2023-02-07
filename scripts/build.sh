#!/usr/bin/env bash
set -x

scripts/copy_app.sh
scripts/create_production_requirements.sh

use_tag="iancleary/ivy-lee-method:$NAME"

DOCKERFILE="$NAME"

if [ "$NAME" == "latest" ] ; then
    DOCKERFILE="python3.11.1-slim"
fi

docker build -t "$use_tag" --file "./docker-images/${DOCKERFILE}.dockerfile" "./docker-images/"
