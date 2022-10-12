
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

build:
build: ## Build the docker image (via docker-compose)
	docker-compose build

up:
up: ## Run the docker image (via docker-compose)
	docker-compose up

run:
run: up

down:
down: ## Stop the docker image (via docker-compose)
	docker-compose down

stop:
stop: down
