
.PHONY: help

# Shell that make should use
# Make changes to path persistent
# https://stackoverflow.com/a/13468229/13577666
SHELL := /bin/bash
PATH := $(PATH)

# Docker namespace, image name and version/tag
NS?= iancleary
IMAGE_NAME?= ivy-lee-method
LATEST?= latest

IMAGE=$(NS)/$(IMAGE_NAME)
PROD_DOCKER_COMPOSE?=-f docker-compose.prod.yml

# Shell that make should use
SHELL:=bash

# - to suppress if it doesn't exist
include make.env

help:
# http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
# adds anything that has a double # comment to the phony help list
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ".:*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help

venv:  ## Create a venv (python3 -m venv venv)
venv:
	python3 -m venv venv
	echo "source venv/bin/activate"

run: copy
run: ## Run the app (assuming within a venv)
	scripts/start_app_venv.sh

requirements:
requirements: ## Export the pdm requirements to a txt file
	scripts/create_production_requirements.sh

copy:
copy: ## Copy app to docker-images for docker local build
	scripts/copy_app.sh

clean:
clean: ## clean pdm exported requirements.txt
	scripts/clean.sh

lint:
lint: ## lint the code
	pdm run -v scripts/lint.sh

format:
format: ## format the code
	pdm run -v scripts/format-imports.sh

test:
test:  ## Test app with pytest outside of docker (with fresh data/test.db from tests/conftest.py)
	pdm run -v pytest tests

build: requirements copy
build: ## Make the latest build of the image
	docker-compose build || docker compose build || podman-compose build

push:
push: ## push the latest version to docker hub (version is defined in make.env)
	docker push $(IMAGE):$(VERSION)
	docker push $(IMAGE):$(LATEST)

up:
up: ## Run the docker image (via docker-compose)
	docker-compose up || docker compose up || podman-compose up

dev: build up
dev: ## Build and Run the docker image (build and up targets)

detached:
detached: ## Run the docker image (via docker-compose) detached
	docker-compose up -d || docker compose up -d || podman-compose up -d

down:
down: ## Stop the docker image (via docker-compose)
	docker-compose down || docker compose down || podman-compose down

stop:
stop: down

prod-up:
prod-up: ## Run the docker image (via docker-compose)
	docker-compose $(PROD_DOCKER_COMPOSE) up || docker compose $(PROD_DOCKER_COMPOSE) up || podman-compose $(PROD_DOCKER_COMPOSE) up

prod-detached:
prod-detached: ## Run the docker image (via docker-compose) detached
	docker-compose $(PROD_DOCKER_COMPOSE) up -d || docker compose $(PROD_DOCKER_COMPOSE) up -d || podman-compose $(PROD_DOCKER_COMPOSE) up -d

prod-down:
prod-down: ## Stop the docker image (via docker-compose)
	docker-compose $(PROD_DOCKER_COMPOSE) down || docker compose $(PROD_DOCKER_COMPOSE) down || podman-compose $(PROD_DOCKER_COMPOSE) down 

prod-stop:
prod-stop: prod-down
