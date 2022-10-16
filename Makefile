
.PHONY: help

# Shell that make should use
# Make changes to path persistent
# https://stackoverflow.com/a/13468229/13577666
SHELL := /bin/bash
PATH := $(PATH)

help:
# http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
# adds anything that has a double # comment to the phony help list
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ".:*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help

requirements:
requirements: ## Export the pdm requirements to a txt file
	pdm export -o requirements.txt --without-hashes

build: requirements
build: ## Build the docker image (via docker-compose)
	docker-compose build || docker compose build

up:
up: ## Run the docker image (via docker-compose)
	docker-compose up || docker compose up

detached:
detached: ## Run the docker image (via docker-compose) detached
	docker-compose up -d || docker compose up -d

run:
run: up

down:
down: ## Stop the docker image (via docker-compose)
	docker-compose down || docker compose down

stop:
stop: down
