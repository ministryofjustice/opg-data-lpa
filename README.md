# opg-data-lpa

## Purpose

OPG Data LPA is a repo to build a rest API for interactions with LPA. Currently it includes GET endpoints for
gathering information about LPAs from sirius.

In the future it may be expanded to have further GET endpoints or PUT, POST or DELETE endpoints for  strictly
LPA related functions.

## Tech stack

- API Gateway
- Lambda
- Dynamodb

## Languages used

- Terraform (for infrastructure)
- Python (for lambda code)
- OpenApi spec (for building the REST API against API Gateway)

## Local Environment

#### Running flask app locally, aka the quick way

1. Start a virtual environment
1. Add all the env vars: `source .env`
1. `cd lambda_functions/v1/functions/lpa/app`
1. flask run
1. Endpoints should be available on `http://localhost:5000`

#### Running everything in Docker

1. In the root folder: `docker-compose up`
1. Wait a minute
1. `cd mock_aws_services`
1. `python create_secret.py`
    * steps 3 & 4 are temporary, test data will soon be inserted automatically
1. Endpoints should be available on `http://0.0.0.0:4343`

## Unit Tests

Information on running unit tests

## Integration Tests

Information on running integration tests

## PACT

Information on running PACT
