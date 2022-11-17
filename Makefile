
.PHONY: help

# Shell that make should use
# Make changes to path persistent
# https://stackoverflow.com/a/13468229/13577666
SHELL := /bin/bash
PATH := $(PATH)

# Docker namespace, image name and version/tag
NS?= iancleary
IMAGE_NAME?= backend-main
LATEST?= latest

IMAGE=$(NS)/$(IMAGE_NAME)

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

run:
run: ## Run the app (assuming within a venv)
	scripts/start_app_venv.sh

requirements: clean
requirements: ## Export the pdm requirements to a txt file
	scripts/create_requirements.sh

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
test:  ## Test app with pytest outside of docker
	export DATABASE=data/test.db && pdm run -v pytest tests

build: requirements copy
build: ## Make the latest build of the image (version is defined in make.env)
	cd docker-images && docker build --no-cache -f ${DOCKERFILE} --build-arg VERSION=${VERSION} -t ${IMAGE}:${VERSION} .

push:
push: ## push the latest version to docker hub (version is defined in make.env)
	docker push $(IMAGE):$(VERSION)
	docker push $(IMAGE):$(LATEST)

up:
up: ## Run the docker image (via docker-compose)
	docker-compose up || docker compose up

detached:
detached: ## Run the docker image (via docker-compose) detached
	docker-compose up -d || docker compose up -d

down:
down: ## Stop the docker image (via docker-compose)
	docker-compose down || docker compose down

stop:
stop: down
