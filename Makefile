THIS_FILE := $(lastword $(MAKEFILE_LIST))
.PHONY: help build up start down destroy stop restart logs logs_api_gateway ps login_motoserver login_api_gateway
help:
	make -pRrq  -f $(THIS_FILE) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

everything:
	docker-compose -f docker-compose.yml up -d --build
	chmod +x mock_aws_services/create_secret.sh
	mock_aws_services/create_secret.sh
just_api:
	docker-compose -f docker-compose.yml up --build -d mock-sirius motoserver api_gateway
	chmod +x mock_aws_services/create_secret.sh
	mock_aws_services/create_secret.sh

down:
	docker-compose -f docker-compose.yml down $(c)

destroy:
	docker-compose down -v --rmi all --remove-orphans
ps:
	docker-compose -f docker-compose.yml ps
login-api-gateway:
	docker-compose -f docker-compose.yml exec api_gateway /bin/bash
logs:
	docker-compose -f docker-compose.yml logs --tail=100 -f $(c)
