THIS_FILE := $(lastword $(MAKEFILE_LIST))
.PHONY: help build up up-bridge-ual down-bridge-ual up-all down setup setup-bridge-ual setup-all destroy ps login-api-gateway logs unit-tests-all
help:
	make -pRrq  -f $(THIS_FILE) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

build:
	docker-compose build

up:
	docker-compose up -d api_gateway

up-bridge-ual:
	docker-compose -f docker-compose.yml -f docker-compose.bridge-ual.yml up -d api_gateway

down-bridge-ual:
	docker-compose -f docker-compose.yml -f docker-compose.bridge-ual.yml down

up-all:
	docker-compose up -d

down:
	docker-compose down $(c)

setup: build up

setup-bridge-ual: build up-bridge-ual

setup-all: build up-all

destroy:
	docker-compose down -v --rmi all --remove-orphans

ps:
	docker-compose ps

login-api-gateway:
	docker-compose exec api_gateway /bin/bash

logs:
	docker-compose logs --tail=100 -f $(c)

unit-tests-all:
	docker-compose run --rm unit-test-lpa-data
