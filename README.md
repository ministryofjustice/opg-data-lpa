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

### PACT

To run pact locally, the easiest way to interact with it is to use the client tools.

The best package to get started can be found here:

https://github.com/pact-foundation/pact-ruby-standalone/releases/latest

You can download the latest version to a directory, unzip it and run the individual tools
in the `/pact/bin` folder from the command line or put them in your PATH.
First you should put the contract in our local broker. The local broker is spun up as part
of the `docker-compose up -d` command and you can push in a contract manually from a json file
by using the below command (example json included in this repo):

```
curl -i -X PUT -d '@./docs/support_files/pact_contract.json' \
-H 'Content-Type: application/json' \
http://localhost:9292/pacts/provider/lpa_data_sirius/consumer/lpa_data/version/x12345
```

You can then check it has uploaded by browsing to `localhost:9292`.

To tag the pact we can now run this. We will want to tag the consumer as
the verification command is best used with tags:

```
curl -i -X PUT -H 'Content-Type: application/json' \
http://localhost:9292/pacticipants/lpa_data/versions/x12345/tags/v1
```

You can check it has worked here:

`http://localhost:9292/matrix/provider/OPG%20Data/consumer/Complete%20the%20deputy%20report`

Run the secret creation against mock

```python3 ./mock_aws_services/create_secret.py```

You can verify the pact as follows (assuming your path to pact-provider-verifier is correct):

```
../pact/bin/pact-provider-verifier --provider-base-url=http://localhost:4343 \
--custom-provider-header 'Authorization: asdf1234567890' \
--pact-broker-base-url="http://localhost:9292" \
--provider="lpa_data_sirius" \
--consumer-version-tag=v1 \
--provider-version-tag=v1 \
--publish-verification-results \
--provider-app-version=z12345
```
