THIS_FILE := $(lastword $(MAKEFILE_LIST))
.PHONY: help build up start down destroy stop restart logs logs_api_gateway ps login_motoserver login_api_gateway
help:
	make -pRrq  -f $(THIS_FILE) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

create_secrets:
	chmod +x mock_aws_services/create_secret.sh
	sleep 5
	mock_aws_services/create_secret.sh
	python3 mock_aws_services/create_secret.py

build:
	./build.sh

up:
	docker-compose -f docker-compose.yml up -d --no-recreate mock-sirius motoserver api_gateway

up-bridge-ual:
	docker-compose -f docker-compose.yml -f docker-compose.bridge-ual.yml up -d --no-recreate mock-sirius motoserver api_gateway

up-all:
	docker-compose -f docker-compose.yml up -d

down:
	docker-compose -f docker-compose.yml down $(c)

setup: build up create_secrets

setup-bridge-ual: build up-bridge-ual create_secrets

setup-all: build up-all create_secrets

destroy:
	docker-compose down -v --rmi all --remove-orphans

ps:
	docker-compose -f docker-compose.yml ps

login-api-gateway:
	docker-compose -f docker-compose.yml exec api_gateway /bin/bash

logs:
	docker-compose -f docker-compose.yml logs -f $(c)
