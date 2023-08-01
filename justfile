# list recipes
help:
    just --list

now := `date +"%Y-%m-%d_%H.%M.%S"`
hostname := `uname -n`

PROD_DOCKER_COMPOSE := "docker-compose.prod.yml"

# Export the pdm requirements to a txt files
requirements:
    scripts/create_production_requirements.sh

# Copy app to docker-images for docker local build
copy:
    scripts/copy_app.sh

# clean pdm exported requirements.txt
clean:
	rm docker-images/requirements.txt
	rm -rf docker-images/app/

# lint the code
lint:
	pdm run scripts/lint.sh

# format the code
format:
	pdm run ruff --fix ./
	pdm run black ./

# Test app with pytest outside of docker (with fresh data/test.db from tests/conftest.py)
test:
	pdm run pytest -vv tests

pre-commit:
	pdm run pre-commit run --all-files

# Format and then run lint and test targets (like CI does)
ci: format lint test pre-commit
	rm data/test.db

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

# Open the URL for issues
issues:
	open https://github.com/iancleary/tasks/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc

# Open the URL for pull requests
prs:
	open https://github.com/iancleary/tasks/pulls?q=is%3Apr+is%3Aopen+sort%3Aupdated-desc
