# opg-data-template

## Purpose

OPG Data template is a repo to build a rest API with a working basic GET endpoint that returns "OK".

It has the scaffolding for a flask based app as that is our preferred method of doing REST APIs currently.

This template may be used as the basis for future integrations. You can start by copying it to the new repo and
replacing everything that says `template` with the name of your integration. We don't spin up new projects often
enough to warrant anything more complicated than this currently.

Although all the settings here should be universal, it is worth checking that your project doesn't need additional or
different settings.

IMPORTANT: There is an additional stage that needs completing before you can spin up your environment.
You must add the sub domains in the `org-infra` repo first.

## Tech stack

- API Gateway
- Lambda
- Dynamodb

## Languages used

- Terraform (for infrastructure)
- Python (for lambda code)
- OpenApi spec (for building the REST API against API Gateway)

## Local Environment

Information about spinning up the local environment

## Unit Tests

Information on running unit tests

## Integration Tests

Information on running integration tests

## PACT

Information on running PACT
