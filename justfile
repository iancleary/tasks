# list recipes
help:
    just --list

now := `date +"%Y-%m-%d_%H.%M.%S"`
hostname := `uname -n`

PROD_DOCKER_COMPOSE := "docker-compose.prod.yml"

# Create a venv (python3 -m venv venv)
venv:
    python3.11 -m venv venv
    echo "source venv/bin/activate"

# Export the pdm requirements to a txt file
requirements:
    scripts/create_production_requirements.sh

# Copy app to docker-images for docker local build
copy:
    scripts/copy_app.sh

# clean pdm exported requirements.txt
clean:
    scripts/clean.sh

# lint the code
lint:
	pdm run -v scripts/lint.sh

# format the code
format:
	pdm run -v scripts/format-imports.sh

# Test app with pytest outside of docker (with fresh data/test.db from tests/conftest.py)
test:
	SQLALCHEMY_WARN_20=1 pdm run -v pytest -vv  tests

# Make the latest build of the image
build: requirements copy
	docker-compose build || docker compose build || podman-compose build

# Run the docker image (via docker-compose)
up:
	docker-compose up || docker compose up || podman-compose up
# Build and Run the docker image (build and up targets)
dev: build up

# Run the docker image (via docker-compose) detached
detached:
	docker-compose up -d || docker compose up -d || podman-compose up -d

# Stop the docker image (via docker-compose)
down:
	docker-compose down || docker compose down || podman-compose down

stop: down

# Run the docker image (via docker-compose)
prod-up:
	docker-compose {{PROD_DOCKER_COMPOSE}} up || docker compose {{PROD_DOCKER_COMPOSE}} up || podman-compose {{PROD_DOCKER_COMPOSE}} up

# Run the docker image (via docker-compose) detached
prod-detached:
	docker-compose {{PROD_DOCKER_COMPOSE}} up -d || docker compose {{PROD_DOCKER_COMPOSE}} up -d || podman-compose {{PROD_DOCKER_COMPOSE}} up -d

# Stop the docker image (via docker-compose)
prod-down:
	docker-compose {{PROD_DOCKER_COMPOSE}} down || docker compose {{PROD_DOCKER_COMPOSE}} down || podman-compose {{PROD_DOCKER_COMPOSE}} down

prod-stop: prod-down
