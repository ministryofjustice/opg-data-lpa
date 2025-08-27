THIS_FILE := $(lastword $(MAKEFILE_LIST))
.PHONY: help build up start down destroy stop restart logs logs_api_gateway ps login_motoserver login_api_gateway
help:
	make -pRrq  -f $(THIS_FILE) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

create_secrets:
	chmod +x mock_aws_services/create_secret.sh
	sleep 5
	mock_aws_services/create_secret.sh
	docker-compose exec api_gateway python3 /var/www/mock_aws_services/create_secret.py

build:
	docker-compose build

up:
	docker-compose up -d mock-sirius motoserver api_gateway

up-bridge-ual:
	docker-compose -f docker-compose.yml -f docker-compose.bridge-ual.yml up -d mock-sirius motoserver api_gateway

down-bridge-ual:
	docker-compose -f docker-compose.yml -f docker-compose.bridge-ual.yml down

up-all:
	docker-compose up -d

down:
	docker-compose down $(c)

setup: build up create_secrets

setup-bridge-ual: build up-bridge-ual create_secrets

setup-all: build up-all create_secrets

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
