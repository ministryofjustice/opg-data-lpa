# opg-data-lpa

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

To run the API locally you should have aws-vault installed and have an account that has any user in identity
account (if you have access to aws then you have this).

You also should have identity as an entry in your `~/.aws/config` file (opg staff will have set this up by default).

You also need to have the AWS go sdk installed. If you do not then run `go get -u github.com/aws/aws-sdk-go/...`

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

## Manual setup

#### Set up local development environment outside of docker

If you wish to develop against this environment and don't want to be dealing with docker containers then there
is a bit more of an in depth set up process required.

1. Create a virtual environment
    ```bash
   python3 -m venv
   ```
   
1. Start the virtual env
   ```bash
   source venv/bin/activate
   ```

1. Add all the env vars:
   ```bash
   source .env
   ```
1. Install the dev requirements
   * Log into CodeArtifact
   ```bash
   aws-vault exec identity -- go run ./docs/support_scripts/aws/getcreds.go
   aws codeartifact login --tool pip --repository opg-pip-shared-code-dev --domain opg-moj --domain-owner 288342028542 --region eu-west-1
   
   # Or if you have stronger permissions
   
   aws-vault exec sirius-dev -- aws codeartifact login --tool pip --repository opg-pip-shared-code-dev --domain opg-moj --domain-owner 288342028542 --region eu-west-1
   ```

   * Install the dev requirements
   ```bash
   pip3 install -r lambda_functions/v1/requirements/dev-requirements.txt
   ```

1. Remove the codeartifact login
   ```bash
   rm ~/.pypirc
   ```
#### Running flask app locally

1. `cd lambda_functions/v1/functions/lpa/app`
1. `flask run`
1. Endpoints should be available on `http://localhost:5000`

## Unit Tests

1. [Set up local environment](#set-up-local-development-environment-outside-of-docker)

1. Run the tests command-line style
    ```bash
    python -m pytest -m "not (smoke_test or pact_test)"
    ```

1. Run the tests command-line style with coverage
    ```bash
    python -m pytest lambda_functions/v1/tests --cov=lambda_functions/v1/functions/lpa/app/api --cov-fail-under=80
    ```
1. Run the tests in PyCharm

    * Go to PyCharm > Preferences > Tools > Python Integrated Tools
    * Set the Default Test Runner to 'pytest'
    * Right click on the tests folder (or single file) > 'Run pytest in tests'

## Integration Tests
1. [Set up local environment](#set-up-local-development-environment-outside-of-docker)

1. Setup the tests:
     - In `integration_tests/v1/conftest.py`, check that the url you are pointing to is correct.
     - In `integration_tests/v1/conftest.py`, check that the `configs_to_test` is set to what you want to test against.
     - In `integration_tests/v1/conftest.py`, take note of the ids you will be testing against.

1.  Run the tests
    ```bash
    aws-vault exec identity -- python -m pytest -n2 --dist=loadfile --html=report.html --self-contained-html
    ```

## PACT

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

`http://localhost:9292/matrix/provider/lpa_data_sirius/consumer/lpa_data`

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
