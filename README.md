# Tasks

This repo contains an python backend web application that solves the problem of organizing items into lists in a flexible way.

The application uses SQLite as a database, with SQLAlchemy as an Object-Relation Mapping.  It is fully type annotated, fully tested, and no unecessary external dependecies.

## Application Structure

You can create, read, update, and delete:

* Lists tha contain sections
* Sections that contianed items
* Items that a name, description, created/due/deleted dates, and active/status values.

Upon completion or deletion, the datetime of that event will be tracked in the item.  Upon deletion, the item is marked inactive.  It can be permanantly deleted from a "Trash" or "Garbage" area.

## Conventions I follow when using the application

### Brainstormning versus Backlog Management

* Manage items you want to offload from you brain and create a list of sections that make sense to how you work

### Object and Key Result

* Write down my single objective for the next three months.
* Add to the description why it is important.
* Think about why if will create value for you.
* How will it make you feel part of something bigger?

Think about how you want to measure and track your progress, but don't incentivize yourself for OKRs.  It's not a good idea.

### Pruning and Offloading

* I caution against using this as something that manages you and where all items are equal importance.
* Note that there is not a field on the items for importance, priority, nor story points.  That is intentional.  This is not a tool to measure velocity, but help me organize and log data I want to persist.
* Do not log everything and it's okay to delete items that are part of the brainstorming process or any other iterative process where the intermediate items don't need to be kept.

### When and how I use the application

* I find a loose structure has worked best for me.  I try to not obsess over having to enter everything all at once nor enter everything.  I don't want to spend all my time tracking, but want a tool that can give me data sovereingty so I can use it for sensitive data.
* I have post it notes, a notepad, and a pencil where I work to make quick notes of items as they come up.

#### Time Batching and Forecasting

* I have found flow in using this log as a way to keep track of what I want or need to time batch, and not a log of every tiny thing that I ever do.  If it takes 5-15 minutes to check something, I will put a reminder on my calendar and move on.
* For major tasks, I put them in this application, time batch for the short amount of foreseeable future, and start to work.  Granted, if I know I need to block off time this week or next, I will, but I try to not go too far into the future with a high level of granualarity as that turns into managing uncertainty for little benefit (keep it to day blocks at that horizon).

### Methods I think work best as guides

I really have gotten a lot of value out of time batching.  Previous versions of this application focused on the Ivy Lee Method (described below).  I removed the structure/enforcement formally from the application.

The application still supports lists of variable length, so you can choose to abide by the method by using naming a section at the top "Ivy Lee" and ensuring it never has more than 6 items.

> #### The Ivy Lee Method
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
> ##### On Managing Priorities Well
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

## Dependencies

The project uses [pdm](https://pdm.fming.dev/latest/usage/project/) as a dependency manager, while exporting to a requirements.txt file and using pip to get around certain issues:

* build with docker and a ([requirements.txt](https://pdm.fming.dev/latest/usage/cli_reference/#exec-0--export)) file.
* lint in an environment that installs packages in a virtual environment with pip and not pdm ([mypy doesn't support the `__pypackages__` structure](https://github.com/pdm-project/pdm/discussions/751)).

## Configuration

This application subscribes to the [twelve-factor app methodology for configuration](https://12factor.net/config).

As such, all important configuration is handled by the environment (`.env`):

```env
DATABSE_URI=sqlite:////data/prod.db
HOST=0.0.0.0
PORT=8000
ALLOW_ORIGINS=http://localhost,http://localhost:3000
ALLOWED_CREDENTIALS=True
ALLOWED_METHODS=*
ALLOWED_HEADERS=Access-Control-Allow-Origin
TIMEZONE=America/Phoenix
```

When using docker and a local database mounted into the container, it is recommended for the DATABASE_URI to contain an absolute path.

> Timezones, please see the link: [List of Timezones on Wikipedia](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)

## Deployment

The image is available from [docker.io/iancleary/tasks](https://hub.docker.com/r/iancleary/tasks) and [ghcr.io/iancleary/tasks](https://github.com/users/iancleary/packages/container/package/tasks).

----------

> Docker-compose example

`docker-compose.yml`

```docker-compose
---
version: "3.9"
services:
  web:
    image: docker.io/iancleary/tasks:latest
    env_file:
      - '._prod.env'
    ports:
      - "8000:8000"
    volumes:
      - './data:/data'
```

`._prod.env` follows the structure shown above in [Configuration](#configuration).
