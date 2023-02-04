#! /usr/bin/env sh

echo "Running inside /app/prestart.sh, you could add migrations to this file, e.g.:"

echo "
#! /usr/bin/env bash
# Let the DB start
sleep 5;
# Run migrations
alembic upgrade head
"

sleep 5;
alembic upgrade head
