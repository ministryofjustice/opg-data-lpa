#!/bin/bash

set -oe pipefail

coverage run --source /var/task/lambda_functions/v1/functions/lpa -m pytest /var/task/lambda_functions/v1/tests

coverage report
