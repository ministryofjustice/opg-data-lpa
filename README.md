# opg-data-lpa

[![CircleCI](https://circleci.com/gh/ministryofjustice/opg-data-lpa/tree/main.svg?style=svg)](https://circleci.com/gh/ministryofjustice/opg-data-lpa/tree/main)

## Purpose

OPG Data LPA is a repo to build a rest API for interactions with LPA. Currently it includes GET endpoints for
gathering information about LPAs from sirius.

In the future it may be expanded to have further GET endpoints or PUT, POST or DELETE endpoints for  strictly
LPA related functions.

## Tech stack

- API Gateway
- Lambda
- Redis

## Languages used

- Terraform (for infrastructure)
- Python (for lambda code)
- OpenApi spec (for building the REST API against API Gateway)

## Running the API locally

- Run full setup script from the make file:

```
make setup
```

or if you want pact as well:

```
make setup-all
```

- Test the setup

```
curl -X GET http://localhost:4343/v1/healthcheck
curl -X GET http://localhost:4343/v1/lpa-online-tool/lpas/A39721583862
curl -X GET http://localhost:4343/v1/use-an-lpa/lpas/700000000047
```

That should be all you need to set it up locally.

## CI Pipeline

When working on a ticket you should name your branch as the jira identifier of the ticket you are working on.

When you push your changes to your branch and create a PR then the CircleCi workflow will run and create a branch
based environment in aws. This includes an api gateway instance, the lambda function and all the relevant DNS to access
the environment.

You can test against the endpoints by assuming a sirius dev role and hitting the following endpoint (replacing branch_name and api_path:

```
https://branch_name.dev.lpa.api.opg.service.justice.gov.uk/v1/api_path
```

Once merged you can do the same tests against dev by removing the branch_name portion of above url.

Environments get destroyed overnight and by default your environment is protected for the first night's destroy but
will be cleaned up on the subsequent night. If you want to work on it longer either recreate it by rerunning the workflow
or  change the protection TTL in dynamodb.

## Manual setup

### Set up local development environment outside of docker

If you wish to develop against this environment and don't want to be dealing with docker containers then there
is a bit more of an in depth set up process required.

1. Create a virtual environment

    ```shell
    python3 -m venv
    ```

1. Start the virtual env

    ```shell
    source venv/bin/activate
    ```

1. Add all the env vars:

    ```shell
    source .env
    ```

1. Install the dev requirements
    - Install the dev requirements

    ```shell
    pip3 install -r lambda_functions/v1/requirements/dev-requirements.txt
    ```

### Running flask app locally

1. `cd lambda_functions/v1/functions/lpa/app`
2. `FLASK_APP=lpa SIRIUS_BASE_URL=http://localhost:5001 flask run &`
3. Endpoints should be available on `http://localhost:5000`

## Unit Tests

1. [Set up local environment](#set-up-local-development-environment-outside-of-docker)

1. Run the tests command-line style

    ```shell
    python3 -m pytest -m "not (smoke_test or pact_test)"
    ```

1. Run the tests command-line style with coverage

    ```shell
    python3 -m pytest lambda_functions/v1/tests --cov=lambda_functions/v1/functions/lpa/app/api --cov-fail-under=80
    ```

1. Run the tests in PyCharm

    - Go to PyCharm > Preferences > Tools > Python Integrated Tools
    - Set the Default Test Runner to 'pytest'
    - Right click on the tests folder (or single file) > 'Run pytest in tests'

## Integration Tests

1. [Set up local environment](#set-up-local-development-environment-outside-of-docker)

1. Setup the tests:
    - In `integration_tests/v1/conftest.py`, check that the url you are pointing to is the correct one for your environment.

    ```python
    opg_data_lpa_dev_aws = {
    "name": "new collections api on aws dev",
    "healthcheck_endpoint": {
        "url": "https://uml-2131.dev.lpa.api.opg.service.justice.gov.uk/v1/healthcheck",
        "method": "GET",
    },
    "online_tool_endpoint": {
        "url": "https://uml-2131.dev.lpa.api.opg.service.justice.gov.uk/v1/lpa"
        "-online-tool/lpas",
        "method": "GET",
        "valid_lpa_online_tool_ids": ["A33718377316"],
        "invalid_lpa_online_tool_ids": ["banana"],
    },
    ```

    - In `integration_tests/v1/conftest.py`, check that the `configs_to_test` is set to what you want to test against.

    ```python
    configs_to_test = [opg_data_lpa_dev_aws]
    ```

    - In `integration_tests/v1/conftest.py`, take note of the ids you will be testing against.

    ```python
    "valid_sirius_uids": ["700000000138"],
    ```

1. Run the tests

    ```shell
    aws-vault exec identity -- python -m pytest -n2 --dist=loadfile --html=report.html --self-contained-html
    aws-vault exec identity -- python -m pytest -n2 --dist=loadfile --html=report.html --self-contained-html
    ```

## PACT

To run pact locally, the easiest way to interact with it is to use the client tools.

The best package to get started can be found here:

<https://github.com/pact-foundation/pact-ruby-standalone/releases/latest>

You can download the latest version to a directory, unzip it and run the individual tools
in the `/pact/bin` folder from the command line or put them in your PATH.
First you should put the contract in our local broker. The local broker is spun up as part
of the `docker-compose up -d` command and you can push in a contract manually from a json file
by using the below command (example json included in this repo):

```shell
curl -i -X PUT -d '@./docs/support_files/pact_contract.json' \
-H 'Content-Type: application/json' \
http://localhost:9292/pacts/provider/lpa_data_sirius/consumer/lpa_data/version/x12345
```

You can then check it has uploaded by browsing to `localhost:9292`.

To tag the pact we can now run this. We will want to tag the consumer as
the verification command is best used with tags:

```shell
curl -i -X PUT -H 'Content-Type: application/json' \
http://localhost:9292/pacticipants/lpa_data/versions/x12345/tags/v1
```

You can check it has worked here:

`http://localhost:9292/matrix/provider/lpa_data_sirius/consumer/lpa_data`

Run the secret creation against mock

```python3 ./mock_aws_services/create_secret.py```

You can verify the pact as follows (assuming your path to pact-provider-verifier is correct):

```shell
../pact/bin/pact-provider-verifier --provider-base-url=http://localhost:4343 \
--custom-provider-header 'Authorization: asdf1234567890' \
--pact-broker-base-url="http://localhost:9292" \
--provider="lpa_data_sirius" \
--consumer-version-tag=v1 \
--provider-version-tag=v1 \
--publish-verification-results \
--provider-app-version=z12345
```
