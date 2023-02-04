#! /usr/bin/env sh

echo "Running inside $(pwd)/prestart.sh, you could add migrations to this file, e.g.:"

echo "
#! /usr/bin/env bash
# Let the DB start
sleep 1;
# Run migrations
alembic upgrade head
"

sleep 1;
cd app/
alembic upgrade head
cd ..
