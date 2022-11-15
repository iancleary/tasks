# Setup

This repo contains an python backend web application using SQLite as a database, with SQLAlchemy as an Object-Relation Mapping.

The purpose of the application is simple, to support the tracking of things using the Ivy Lee Method.

You can create, read, update, and delete:

* Things to do (in support of the Ivy Lee Method)
* Projects (to help with summaries of the things you've done for quartely conversations with managers and performance reviews)

Upon completion, the date of the items will be tracked. 

When creating items, the application will prevent you from having too many on your list at the same time.  The Ivy Lee Method subscribes you to only have 6 items in a day.  You should approach the first one first, and move down the list.

At the end of each day, take time to update the list for the next day.  This helps clear out your mind and separate today from tomorrow, so you can be present.

## Dependencies

The project uses [pdm](https://pdm.fming.dev/latest/usage/project/) as a depdency manager, while exporting to a requirements.txt file and using pip to get around certain issues:

* build with docker and a ([requirements.txt](https://pdm.fming.dev/latest/usage/cli_reference/#exec-0--export)) file.
* lint in an environment that installs packages in a virtual environment with pip and not pdm ([mypy doesn't support the `__pypackages__` structure](https://github.com/pdm-project/pdm/discussions/751)).

## Deployment

[docker pull iancleary/backend-main](https://hub.docker.com/r/iancleary/backend-main)