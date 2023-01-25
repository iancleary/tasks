# Ivy-Lee-Method

This repo contains an python backend web application using SQLite as a database, with SQLAlchemy as an Object-Relation Mapping.

The purpose of the application is simple, to support the tracking of tasks/items using the [Ivy Lee Method](https://jamesclear.com/ivy-lee).

> ## The Ivy Lee Method
>
> *The Ivy Lee method dates back to 1918, when Lee, a productivity consultant, was hired by Charles M. Schwab, the president of the Bethlehem Steel Corporation, to improve his company's efficiency. As the story goes, Lee offered his method to Schwab for free, and after three months, Schwab was so pleased with the results he wrote Lee a check for $25,000 - the equivalent of about $400,000 today.*
>
> During his 15 minutes with each executive, Ivy Lee explained his simple daily routine for achieving peak productivity:
>
>* At the end of each work day, write down the six most important things you need to accomplish tomorrow. Do not write down more than six tasks.
>
>* Prioritize those six items in order of their true importance.
>* When you arrive tomorrow, concentrate only on the first task. Work until the first task is finished before moving on to the second task.
>* Approach the rest of your list in the same fashion. At the end of the day, move any unfinished items to a new list of six tasks for the following day.
>    Repeat this process every working day.
>
> ### On Managing Priorities Well
>
> Here's what makes it so effective:
>
>* **It's simple enough to actually work.**
>
>* **It forces you to make tough decisions**
>* **It removes the friction of starting.**
>* **It requires you to single-task.**
>
> The bottom line? Do the most important thing first each day. It's the only productivity trick you need.

## Application

You can create, read, update, and delete:

* Things to do (in support of the Ivy Lee Method)
* Projects (to help with summaries of the things you've done for quarterly conversations with managers and performance reviews)

Upon completion, the date of the items will be tracked.

When creating items, the application will prevent you from having too many on your list at the same time.  The Ivy Lee Method subscribes you to only have 6 items in a day.  You should approach the first one first, and move down the list.

> Note: It won't delete items, but rather remove them from the list of 6 things on your important list.  This is to enforce the method, while being a ledger of items for your use.

At the end of each day, take time to update the list for the next day.  This helps clear out your mind and separate today from tomorrow, so you can be present.

## Dependencies

The project uses [pdm](https://pdm.fming.dev/latest/usage/project/) as a dependency manager, while exporting to a requirements.txt file and using pip to get around certain issues:

* build with docker and a ([requirements.txt](https://pdm.fming.dev/latest/usage/cli_reference/#exec-0--export)) file.
* lint in an environment that installs packages in a virtual environment with pip and not pdm ([mypy doesn't support the `__pypackages__` structure](https://github.com/pdm-project/pdm/discussions/751)).


## Configuration

This application subscribes to the [twelve-factor app methodology for configuration](https://12factor.net/config).

As such, all important configuration is handled by the environment (.env):

`.env`
```env
DATABASE=/data/prod.db
HOST=0.0.0.0
PORT=8000
ALLOW_ORIGINS=http://localhost,http://localhost:3000
ALLOWED_CREDENTIALS=True
ALLOWED_METHODS=*
ALLOWED_HEADERS=Access-Control-Allow-Origin"
```

## Deployment


The image is available from [docker.io/iancleary/ivy-lee-method](https://hub.docker.com/r/iancleary/ivy-lee-method)

----------

> Docker-compose example

`docker-compose.yml`

```docker-compose
---
version: "3.9"
services:
  web:
    image: docker.io/iancleary/ivy-lee-method:python3.10.8-slim
    env_file:
      - '._prod.env'
    ports:
      - "8000:8000"
    volumes:
      - './data:/data'
```

`._prod.env`

```env
DATABASE=/data/prod.db
HOST=0.0.0.0
PORT=8000
```
