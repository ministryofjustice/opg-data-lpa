# opg-data-lpa

OPG Use My LPA: Managed by opg-org-infra &amp; Terraform

![path to live status](https://github.com/ministryofjustice/opg-data-lpa/actions/workflows/deploy.yml/badge.svg)
![licence-mit](https://img.shields.io/github/license/ministryofjustice/opg-data-lpa.svg)


[![repo standards badge](https://img.shields.io/badge/dynamic/json?color=blue&style=for-the-badge&logo=github&label=MoJ%20Compliant&query=%24.result&url=https%3A%2F%2Foperations-engineering-reports.cloud-platform.service.justice.gov.uk%2Fapi%2Fv1%2Fcompliant_public_repositories%2Fendpoint%2Fopg-data-lpa)](https://operations-engineering-reports.cloud-platform.service.justice.gov.uk/public-report/opg-data-lpa 'Link to report')

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
- OpenAPI spec (for building the REST API against API Gateway)

## Running the API locally

- Run full setup script from the Makefile:

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

When you push your changes to your branch and create a PR then Github Actions workflow will run and create a branch-based environment in AWS. This includes an API Gateway instance, the Lambda function and all the relevant DNS to access the environment.

You can test against the endpoints by assuming a Sirius dev role and hitting the following endpoint (replacing branch_name and api_path):

```
https://branch_name.dev.lpa.api.opg.service.justice.gov.uk/v1/api_path
```

Once merged you can do the same tests against dev by removing the branch_name portion of above url.

Environments get destroyed overnight and by default your environment is protected for the first night's destroy but
will be cleaned up on the subsequent night. If you want to work on it longer either recreate it by rerunning the workflow
or  change the protection TTL in DynamoDB.

## Manual setup

### Set up local development environment outside of docker

If you wish to develop against this environment and don't want to be dealing with Docker containers then there
is a bit more of an in depth set up process required.

1. Create a virtual environment

    ```shell
    python3 -m venv venv
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
    pip3 install -r lambda_functions/v1/requirements/dev-requirements.txt -r lambda_functions/v1/requirements/requirements.txt
    ```

### Running Flask app locally

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


These tests can also be run with docker, first [set up docker environment](#running-the-api-locally).
Then:
   ```shell
    docker-compose run unit-test-lpa-data
   ```

Some tests use a Pact mock service to record and assert interactions. These are saved to a JSON contract in `./pact` and then uploaded to the Pact Broker in the pipeline.

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
