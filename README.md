# Setup

## Installation

`pipx install pdm`

> <https://pdm.fming.dev/latest/usage/project/>


## non root docker

<https://stackoverflow.com/a/70520801

Since your development environment will almost always be different from your production environment in some way, I'd recommend using a non-Docker Python virtual environment for day-to-day development, have good (pytest) unit tests that can run outside the container, and do integration testing on the built container before deploying.